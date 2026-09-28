# Mapeamento de Ataques: CSE-CIC-IDS2018 Corrigido → Ferramentas Kali Linux

Este documento consolida o mapeamento de todos os ataques presentes no dataset **CSE-CIC-IDS2018 Corrigido (Melhorado)** para ferramentas disponíveis no ecossistema **Kali Linux**, detalhando seu modo de operação, impacto nas features de fluxo e viabilidade de reprodução no laboratório local ([[Atacante e Vítima]]).

---

## 1. Matriz Geral de Ataques e Ferramentas

| # | Classe no CSE-CIC-IDS2018 | Volume (Dataset Corrigido) | Ferramenta Kali Linux | Camada OSI | Status no Laboratório | Nota Detalhada |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- |
| 1 | **DoS Hulk** | 1.803.160 | `hulk` / `hulk.py` | Camada 7 (Aplicação) | Reproduzível | [[DoS - Hulk]] |
| 2 | **DDoS-HOIC** | 1.082.293 | `hoic` / `slowhttptest` (HTTP flood) | Camada 7 (Aplicação) | Reproduzível (Modo DoS L7) | [[DDoS - HOIC]] |
| 3 | **DDoS-LOIC-HTTP** | 289.328 | `loic` / `slowhttptest` | Camada 7 (Aplicação) | Reproduzível | [[DDoS - LOIC HTTP]] |
| 4 | **Botnet Ares** | 142.921 | `ares` / `metasploit` (C2 Beaconing) | Camada 7 (C2 HTTP) | Parcialmente Emulável | [[Botnet - Ares]] |
| 5 | **SSH-BruteForce** | 94.197 | `hydra` / `medusa` | Camada 7 / 4 (SSH/TCP) | Reproduzível | [[SSH - Brute Force]] |
| 6 | **Infiltration - NMAP Portscan** | 89.374 | `nmap` | Camada 4 / 3 (TCP/UDP/IP) | Reproduzível (Concluído) | [[Infiltration - NMAP Portscan]] |
| 7 | **DoS GoldenEye** | 22.560 | `goldeneye` / `goldeneye.py` | Camada 7 (Aplicação) | Reproduzível | [[DoS - GoldenEye]] |
| 8 | **DoS Slowloris** | 8.490 | `slowloris` / `slowhttptest` | Camada 7 (Aplicação) | Reproduzível | [[DoS - Slowloris]] |
| 9 | **DDoS-LOIC-UDP** | 2.527 | `hping3` (modo UDP Flood) | Camada 4 (Transporte) | Reproduzível | [[DDoS - LOIC UDP]] |
| 10 | **Infiltration - Comm Victim Attacker** | 204 | `metasploit` / `netcat` (Reverse Shell) | Camada 7 / 4 (TCP Interativo) | Emulável (Pós-Exploração) | [[Infiltration - Communication Victim Attacker]] |
| 11 | **Web Attack - Brute Force** | 131 | `hydra` / `burpsuite` / `ffuf` | Camada 7 (HTTP POST) | Reproduzível | [[Web Attack - Brute Force]] |
| 12 | **Web Attack - XSS** | 113 | `xsser` / `ffuf` / `zap` | Camada 7 (HTTP XSS) | Reproduzível | [[Web Attack - XSS]] |
| 13 | **Infiltration - Dropbox Download** | 85 | `curl` / `wget` (Download HTTPS) | Camada 7 (TLS/HTTPS) | **Fora de Escopo** | [[Infiltration - Dropbox Download]] |
| 14 | **Web Attack - SQL** | 39 | `sqlmap` | Camada 7 (HTTP Injection) | Reproduzível | [[Web Attack - SQL Injection]] |

> [!NOTE]
> Conforme auditado no [[EDA CSE-CIC-IDS2018 Corrigido]], a classe `FTP-BruteForce` continha 100% de fluxos rotulados como *Attempted* (tentativas sem sucesso) e foi absorvida em `BENIGN`. Portanto, as 14 classes acima constituem a totalidade dos ataques efetivos do benchmark.

---

## 2. Delimitação de Escopo e Justificativa de Ataques Não Reproduzidos

No planejamento experimental para validação do modelo **ALF-MoE** ([[Ambiente de Ataques]]), certos ataques presentes no dataset original não serão reproduzidos no testbed local. A fundamentação técnica para essa decisão é estruturada a seguir:

### 2.1. Infiltration - Dropbox Download (Fora de Escopo)

O ataque `Infiltration - Dropbox Download` possui apenas **85 fluxos** no dataset corrigido (representando meros **0,0001%** dos fluxos totais). Ele **não será reproduzido** pelas seguintes razões metodológicas e arquiteturais:

1. **Dependência de Infraestrutura Externa de Terceiros (SaaS Público):**
   No cenário original do CSE-CIC-IDS2018, um usuário da rede interna clicava em um link malicioso que baixava um artefato malicioso hospedado no serviço público do Dropbox via HTTPS. A reprodução desse cenário exigiria hospedar artefatos em servidores externos do Dropbox Inc., violando os termos de serviço da plataforma, sujeitando o laboratório a bloqueios automáticos por varredura de malware na nuvem e dependendo de conectividade com a Internet externa.
2. **Isolamento e Reprodutibilidade do Laboratório:**
   O ambiente experimental de testes ([[Atacante e Vítima]]) foi concebido como uma rede de laboratório isolada, controlada e determinística (Kali Linux atacante $\leftrightarrow$ Ubuntu vítima). Abrir dependência de serviços externos quebra o isolamento, adiciona latências não determinísticas e introduz variáveis incontroláveis de roteamento global.
3. **Cadeia de Exploração Específica de Endpoint Legado:**
   No dataset de 2018, o download do Dropbox era apenas o vetor de entrega (*delivery phase*) de um arquivo PDF malicioso desenhado para explorar uma vulnerabilidade de corrupção de memória específica do Adobe Acrobat Reader 9.0 em ambiente Windows Server 2012 / Windows 7. O ambiente de vítima atual é baseado em **Ubuntu Linux** com aplicações em **Docker**, tornando essa cadeia de exploração de endpoint obsoleta e sem efeito.
4. **Indistinguibilidade em Nível de Fluxo de Rede (NIDS L4/L7):**
   Do ponto de vista de extração estatística de fluxo (via NFStream ou CICFlowMeter), o tráfego gerado por um download do Dropbox consiste estritamente em uma conexão TLS/HTTPS convencional na porta 443 com certificado legítimo. O fluxo estatístico não contém assinaturas anômalas intrínsecas de ataque de rede: trata-se simplesmente de uma transferência criptografada de bytes. Como o NIDS opera sobre fluxos agregados sem descriptografar sessões TLS com DPI profundo, reproduzir esse download no laboratório equivaleria a registrar um tráfego de download comum, não agregando valor à avaliação de robustez do modelo.

### 2.2. Considerações sobre Infiltration - Communication Victim Attacker e Botnet Ares

- **Botnet Ares (142.921 fluxos):** O Ares é uma botnet cliente-servidor em Python. Sua assinatura principal é o *beaconing* HTTP periódico. Em vez de montar uma botnet distribuída complexa, esse padrão pode ser emulado de forma controlada através de scripts de polling HTTP ou sessões de agente de C2 ([[Botnet - Ares]]).
- **Infiltration - Communication Victim Attacker (204 fluxos):** Representa o canal interativo de shell reverso aberto após o comprometimento inicial. Pode ser emulado pontualmente via `netcat` ou `meterpreter` para validar fluxos interativos de terminal ([[Infiltration - Communication Victim Attacker]]).

---

## 3. Navegação pelas Notas de Ataques

- **Negação de Serviço (DoS / DDoS L7):**
  - [[DoS - Hulk]]
  - [[DDoS - HOIC]]
  - [[DDoS - LOIC HTTP]]
  - [[DoS - GoldenEye]]
  - [[DoS - Slowloris]]
- **Ataques Volumétricos de Transporte (L4):**
  - [[DDoS - LOIC UDP]]
- **Varredura e Infiltração:**
  - [[Infiltration - NMAP Portscan]] (e nota legada [[nmap]])
  - [[Infiltration - Communication Victim Attacker]]
  - [[Infiltration - Dropbox Download]] *(Fora de Escopo)*
- **Força Bruta e Botnets:**
  - [[SSH - Brute Force]]
  - [[Botnet - Ares]]
- **Ataques Web de Aplicação (DVWA):**
  - [[Web Attack - Brute Force]]
  - [[Web Attack - XSS]]
  - [[Web Attack - SQL Injection]]

---

## 4. Framework de Execução e Auditoria de Agentes

Para a execução de testes automatizados e assistidos por LLM agents na máquina atacante Kali, consulte as diretrizes de governança e auditoria em:
- [[AGENTS|AGENTS.md - PenTest Assistido por IA e Protocolo de Auditoria]]

