# DDoS - LOIC HTTP (Low Orbit Ion Cannon - HTTP Mode)

- **Classe no CSE-CIC-IDS2018:** `DDoS-LOIC-HTTP`
- **Volume no Dataset Corrigido:** 289.328 fluxos
- **Camada OSI:** Camada 7 (Aplicação - HTTP)
- **Alvo no Laboratório:** Servidor Web DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível contra o container Web

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Original:** Low Orbit Ion Cannon (LOIC) em modo HTTP
- **Disponibilidade no Kali Linux:**
  - Execução da versão original em .NET via `mono LOIC.exe` ou `wine LOIC.exe`.
  - Scripts Python equivalentes de LOIC HTTP (`loic.py` / `pydos`).
  - Ferramentas nativas do Kali para flooding HTTP repetitivo: `slowhttptest` ou `ab` (Apache HTTP server benchmarking tool).
  ```bash
  # Emulação com ferramenta de requisições concorrentes nativa do Kali
  ab -n 100000 -c 150 http://[ALVO]:8080/
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **LOIC** no modo HTTP foi uma das ferramentas de estresse e negação de serviço mais populares em ataques voluntários descentralizados (hacktivismo):

1. **Flooding Simples de Requisições HTTP:**
   A ferramenta abre dezenas a centenas de conexões TCP na porta do servidor web (ex.: 80/8080) e envia requisições `GET / HTTP/1.0` ou `HTTP/1.1` em sequência ininterrupta.
2. **Ausência de Evasão Avançada (Assinatura Homogênea):**
   Diferente do HULK (que varia parâmetros de query) e do HOIC (que usa boosters com rotação de headers), o LOIC clássico utiliza cabeçalhos altamente estáticos e repetitivos.
3. **Consumo de Sockets e CPU:**
   Mesmo sem técnicas avançadas de evasão, o bombardeio massivo de novas conexões TCP e requisições HTTP esgota o pool de threads e a tabela de conexões ativas do servidor web.

---

## 3. Emulação no Testbed (Kali $\rightarrow$ Ubuntu)

```bash
# Execução conceitual com ab no Kali
ab -n 50000 -c 100 -r http://[ALVO]:8080/
```

- `-n 50000`: Quantidade total de requisições a serem emitidas.
- `-c 100`: Número de conexões concorrentes simultâneas.
- `-r`: Não aborta a execução mesmo se houver erros de socket/timeout do servidor.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Packets/s` | **Muito Elevado** | Grande densidade temporal de pacotes. |
| `Fwd Packet Length Std` | **Muito Baixo / Nulo** | Como as requisições HTTP são idênticas e sem query strings aleatórias, os pacotes de ida possuem tamanhos praticamente constantes. |
| `Packet Length Mean` | **Homogêneo** | Concentração em tamanhos padrão de cabeçalho HTTP mínimo. |
| `Flow IAT Mean` | **Muito Baixo** | Intervalos mínimos entre requisições consecutivas. |
| `SYN Flag Count` / `ACK Flag Count` | **Elevado** | Abertura contínua de handshakes TCP para sustentar o fluxo. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[DDoS - LOIC UDP]]
- [[DDoS - HOIC]]
- [[DoS - Hulk]]
- [[Ambiente de Ataques]]
