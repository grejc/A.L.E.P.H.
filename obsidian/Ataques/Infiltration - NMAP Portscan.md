# Infiltration - NMAP Portscan

- **Classe no CSE-CIC-IDS2018:** `Infiltration - NMAP Portscan`
- **Volume no Dataset Corrigido:** 89.374 fluxos
- **Camada OSI:** Camada 4 e Camada 3 (Varredura TCP/UDP sobre IP)
- **Alvo no Laboratório:** Máquina Vítima Ubuntu ([[Atacante e Vítima]])
- **Status de Reprodução:** Reproduzível (documentado em detalhes na nota [[nmap]])

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal:** `nmap` (Network Mapper, ferramenta padrão nativa do Kali Linux)
- **Documentação de Comandos Locais:** Consulte a nota dedicada [[nmap]] para ver os perfis básico, moderado e agressivo já estruturados no projeto.

---

## 2. Como a Ferramenta Realiza o Ataque

O **NMAP Portscan** é a fase preliminar de reconhecimento em um ciclo de intrusão, utilizada para mapear portas abertas, detectar serviços ativos, versões e sistemas operacionais:

1. **Varredura SYN Stealth (Half-Open - `-sS`):**
   - O atacante envia um pacote TCP com flag `SYN` para uma porta alvo.
   - Se a porta estiver aberta, o alvo responde com `SYN/ACK`. O Nmap imediatamente envia um pacote `RST` para derrubar a conexão antes de completar o handshake, impedindo que aplicações legadas registrem o log da conexão completa.
   - Se a porta estiver fechada, o alvo responde com `RST`.
   - Se a porta estiver filtrada por firewall, não há resposta ou recebe-se uma mensagem de erro ICMP.
2. **Varredura Completa TCP Connect (`-sT`):**
   Realiza o handshake completo de 3 vias (`SYN -> SYN/ACK -> ACK`), utilizado quando o usuário não possui privilégios de raw socket (root).
3. **Detecção de Versão de Serviço (`-sV`) e Sistema Operacional (`-O`):**
   Envia sondas com payloads específicos de protocolos conhecidos (HTTP, SSH, SMB, DNS) e compara os banners retornados com uma base de dados de assinaturas de serviços.
4. **Variação de Temporizadores (`-T0` a `-T5`):**
   O Nmap ajusta dinamicamente a taxa de envio de sondas, a espera por respostas e o paralelismo. O perfil agressivo (`-T4`) ou insano (`-T5`) envia milhares de sondas por segundo.

---

## 3. Modos de Execução no Laboratório

Conforme detalhado em [[nmap]], os comandos utilizados no setup experimental cobrem diferentes níveis de intensidade:

```bash
# 1. Básico (Rápido)
nmap -vv --reason -oA [nome_do_arquivo] [ALVO]

# 2. Moderado / Agressivo (Varredura completa de portas + detecção de serviços)
nmap -p 1-65535 -A -T4 --version-all --osscan-guess -vv --reason -oA [nome_do_arquivo] [ALVO]

# 3. Agressivo com Scripts NSE
nmap -p 1-65535 -A -T5 --version-all --osscan-guess --script="vuln,discovery,intrusive" -vv --reason -oA [nome_do_arquivo] [ALVO]
```

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

No extrator de fluxos ([[CICFlowMeter Features VS NFStream Features]]), as sondas do Nmap geram um padrão estatístico único:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Extremamente Curto** | Sondas rápidas de meio handshake ou pacotes rejeitados com RST imediato. |
| `Total Length of Fwd Packet` | **Mínimo** | Pacotes sem payload de dados (40 a 60 bytes de cabeçalho TCP/IP). |
| `Fwd Packets/s` | **Muito Alto** | Disparo sequencial ou paralelo massivo de sondas. |
| `Down/Up Ratio` | **Muito Baixo ou Zero** | Portas fechadas ou filtradas resultam em ausência total de tráfego de retorno. |
| `SYN Flag Count` / `RST Flag Count` | **Dominantes** | Sondas com flag SYN disparadas pelo atacante e respostas RST da vítima. |
| `FWD Init Win Bytes` | **Específico do Nmap** | O Nmap frequentemente forja tamanhos de janela TCP fixos (ex.: 1024, 2048, 3072, 4096). |

---

## 5. Relação com outras Notas

- [[nmap]]
- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Atacante e Vítima]]
- [[Infiltration - Communication Victim Attacker]]
