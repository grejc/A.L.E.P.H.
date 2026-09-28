# DDoS - LOIC UDP (Low Orbit Ion Cannon - UDP Mode)

- **Classe no CSE-CIC-IDS2018:** `DDoS-LOIC-UDP`
- **Volume no Dataset Corrigido:** 2.527 fluxos
- **Camada OSI:** Camada 4 (Transporte - UDP Protocol 17)
- **Alvo no Laboratório:** Portas UDP arbitrárias na Máquina Vítima Ubuntu ([[Atacante e Vítima]])
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal no Kali:** `hping3` (gerador nativo de pacotes de rede e stress test em Camada 4)
- **Ferramenta Original:** LOIC (Low Orbit Ion Cannon) em modo UDP
- **Alternativas no Kali:** Scripts de flooding UDP em Python (`udp_flood.py`), `iperf3` (em modo UDP saturation) ou `nping`
- **Verificação no Kali:**
  ```bash
  which hping3
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **DDoS-LOIC-UDP** consiste em um ataque volumétrico bruto na camada de transporte explorando o protocolo UDP:

1. **Protocolo Não Orientado a Conexão (Sem Handshake):**
   Diferente do TCP, o UDP não requer estabelecimento de sessão (handshake de 3 vias) nem controle de fluxo por confirmações de recebimento (ACKs). O atacante pode transmitir dados na velocidade máxima que a interface de rede permitir.
2. **Bombardeio de Datagramas UDP:**
   A ferramenta dispara uma torrente contínua de datagramas UDP para portas de destino aleatórias ou fixas do host vítima.
3. **Sobrecarga do Kernel e Geração de ICMP:**
   - Quando os datagramas chegam a uma porta UDP que não possui um serviço escutando, a pilha de rede do kernel do sistema operacional (Ubuntu) é forçada a processar o pacote e responder com uma mensagem de erro `ICMP Destination Unreachable (Port Unreachable - Tipo 3, Código 3)`.
   - Se a taxa de pacotes for altíssima, a CPU da vítima fica sobrecarregada apenas processando interrupções de hardware da placa de rede (`softirq`) e gerando mensagens ICMP de erro, saturando a interface de rede.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ Ubuntu)

```bash
# Execução conceitual com hping3 em modo UDP flood no Kali
sudo hping3 --udp --flood --rand-dest -p [PORTA] [IP_VITIMA]
```

- `--udp`: Especifica o protocolo UDP (protocolo 17 no cabeçalho IP).
- `--flood`: Envia pacotes na taxa máxima suportada sem aguardar respostas (modo de estresse).
- `-p [PORTA]`: Porta UDP de destino (ou randômica).
- `[IP_VITIMA]`: Endereço IP da máquina Ubuntu.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Por operar estritamente em UDP, o perfil estatístico é radicalmente diferente dos ataques HTTP:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Protocol` | **17 (UDP)** | Protocolo de transporte estritamente UDP. |
| `Flow Packets/s` / `Fwd Packets/s` | **Extremamente Alto** | Rajada ininterrupta de datagramas. |
| `SYN / ACK / FIN / RST Flags` | **Todas Zeradas** | O protocolo UDP não possui flags TCP. |
| `Down/Up Ratio` | **0 ou Próximo de 0** | Tráfego predominantemente unidirecional (quase nenhuma resposta reversa). |
| `ICMP Type` / `ICMP Code` | **3 / 3 (quando registrado)** | Geração de respostas `ICMP Port Unreachable` pelo host vítima. |
| `Flow IAT Mean` | **Próximo de Zero** | Taxa contínua de transmissão em velocidade de linha. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[DDoS - LOIC HTTP]]
- [[Atacante e Vítima]]
