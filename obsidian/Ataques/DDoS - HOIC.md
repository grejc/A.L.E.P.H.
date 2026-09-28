# DDoS - HOIC (High Orbit Ion Cannon)

- **Classe no CSE-CIC-IDS2018:** `DDoS-HOIC`
- **Volume no Dataset Corrigido:** 1.082.293 fluxos (segunda maior classe volumétrica)
- **Camada OSI:** Camada 7 (Aplicação - HTTP)
- **Alvo no Laboratório:** Servidor Web DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível em modo DoS HTTP de alta densidade

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Original:** High Orbit Ion Cannon (HOIC)
- **Execução no Kali Linux:**
  - Originalmente desenvolvido em BASIC/Windows, pode ser executado via `wine hoic.exe` no Kali Linux.
  - Implementações nativas equivalentes em Python/C (ex.: `hoic.py`) ou geradores de estresse HTTP multithreaded de alta vazão no Kali, como `wrk`, `slowhttptest` ou `siege`.
  ```bash
  # Exemplo conceitual com gerador HTTP de alta densidade nativo no Kali
  wrk -t8 -c256 -d60s http://[ALVO]:8080/
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **HOIC** foi desenvolvido como uma evolução direta do LOIC para ataques de negação de serviço distribuídos em larga escala, trazendo inovações voltadas para evasão e alto paralelismo:

1. **Multithreading Agressivo:**
   A ferramenta permite abrir até 256 threads simultâneas por processo atacante. Cada thread abre conexões TCP independentes disparando rajadas ininterruptas de requisições HTTP POST e GET.
2. **Sistema de "Boosters" (Scripts .hoic):**
   A grande inovação do HOIC foi a introdução de módulos chamados *boosters*. São pequenos scripts de texto que determinam dinamicamente a rotação de URLs alvo, headers HTTP randômicos, cabeçalhos de referer eUser-Agents, evitando que sistemas de defesa (WAFs e regras estáticas de firewall) bloqueiem o ataque por assinatura fixa de cabeçalho.
3. **Saturação de Pool de Conexões e Largura de Banda:**
   Ao disparar centenas de requisições simultâneas sem aguardar o recebimento integral do corpo da resposta, o servidor web é levado rapidamente ao esgotamento de descritores de sockets (`file descriptors`) e estouro de capacidade de conexões TCP pendentes.

---

## 3. Emulação no Testbed (Kali $\rightarrow$ Ubuntu)

No cenário original do CSE-CIC-IDS2018, dezenas de nós zumbis coordenados executavam o HOIC. No ambiente de laboratório com uma única máquina atacante ([[Atacante e Vítima]]):
- O ataque é executado com alto número de threads/concorrência paralela contra a porta 8080 da vítima.
- O padrão de tráfego gerado mimetiza os fluxos individuais de clientes participando do cluster de ataque.

```bash
# Execução com parâmetros conceituais de teste de estresse HTTP L7 no Kali
siege -c 200 -t 60S "http://[ALVO]:8080/ POST"
```

- `-c 200`: 200 usuários/conexões concorrentes simultâneas.
- `-t 60S`: Duração de 60 segundos de rajada ininterrupta.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Packets/s` | **Extremo** | Dezenas de conexões paralelas disparando requisições em regime contínuo. |
| `Flow Bytes/s` | **Alto** | Grande volume de dados trafegados entre requisições e respostas/erros HTTP. |
| `Fwd Act Data Pkts` | **Elevado** | Alta taxa de pacotes com dados efetivos na direção cliente $\rightarrow$ servidor. |
| `Subflow Fwd Packets` | **Elevado** | Rajadas contínuas de subfluxos com alto volume de pacotes de ida. |
| `Bwd Packets/s` | **Decai Progressivamente** | Conforme o servidor entra em colapso e deixa de responder às conexões. |
| `ACK Flag Count` | **Massivo** | Manutenção de centenas de sessões TCP com confirmações de transporte constantes. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[DoS - Hulk]]
- [[DDoS - LOIC HTTP]]
- [[Ambiente de Ataques]]
