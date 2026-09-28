# DoS - GoldenEye

- **Classe no CSE-CIC-IDS2018:** `DoS GoldenEye`
- **Volume no Dataset Corrigido:** 22.560 fluxos
- **Camada OSI:** Camada 7 (Aplicação - HTTP)
- **Alvo no Laboratório:** Servidor Web DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal:** `goldeneye` / `goldeneye.py`
- **Disponibilidade no Kali Linux:**
  - Disponível nos repositórios ou via script oficial em Python (`goldeneye.py`).
  - Alternativa com características análogas de exaustão Keep-Alive: `slowhttptest` ou `siege`.

---

## 2. Como a Ferramenta Realiza o Ataque

O **GoldenEye** é uma ferramenta de ataque de negação de serviço na camada de aplicação que combina exaustão de conexões persistentes HTTP (*Keep-Alive Starvation*) com inibição agressiva de cache:

1. **Esgotamento de Keep-Alive:**
   A ferramenta abre múltiplas conexões HTTP válidas e envia requisições `GET` e `POST` contendo o cabeçalho `Connection: Keep-Alive` com temporizadores elevados (ex.: `Keep-Alive: 110`). Isso instrui o servidor web a manter os sockets e os processos/threads de worker abertos aguardando requisições adicionais na mesma conexão TCP.
2. **Inibição de Cache e Proxies:**
   Diferente de ataques ingênuos, o GoldenEye injeta combinações rigorosas de cabeçalhos anti-cache em cada requisição:
   - `Cache-Control: no-cache, no-store, max-age=0, must-revalidate`
   - `Pragma: no-cache`
   Isso força o servidor web de backend a recalcular e reconstruir o recurso dinamicamente, sem possibilidade de servir respostas cacheadas.
3. **Randomização de Métodos e Headers:**
   Alterna dinamicamente entre requisições `GET` e `POST`, injetando parâmetros randômicos na query e sorteando User-Agents conhecidos de navegadores modernos para dificultar filtros baseados em expressões regulares.
4. **Exaustão de Workers:**
   À medida que centenas de conexões são abertas e mantidas ocupadas por longos intervalos, o servidor web atinge seu limite de trabalhadores concorrentes (ex.: `MaxRequestWorkers` do Apache), recusando qualquer nova tentativa de conexão legítima.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ Ubuntu)

```bash
# Execução conforme documentação oficial do kali-tools
goldeneye http://[ALVO]:8080/ -w 10 -s 500 -m random -n
```

- `http://[ALVO]:8080/`: URL da aplicação web da vítima ([[Ambiente de Ataques]]).
- `-w 10`: Quantidade de workers concorrentes gerados pela ferramenta (padrão oficial: 10).
- `-s 500`: Quantidade de sockets concorrentes abertos por worker (padrão oficial: 500).
- `-m random`: Alterna aleatoriamente entre os métodos HTTP GET e POST (`get`, `post` ou `random`).
- `-n`: Desativa verificação estrita de certificado SSL/TLS (`--nosslcheck`).
- `-d`: Habilita modo debug para inspeção do handshake (opcional).

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `GoldenEyeTester`.


---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Elevada** | Sessões mantidas abertas deliberadamente pelos cabeçalhos `Keep-Alive`. |
| `Active Mean` / `Idle Mean` | **Padrão Intercalado** | Períodos de envio de requisições alternados com intervalos de espera pelo timeout. |
| `Total TCP Flow Time` | **Prolongado** | Manutenção persistente do descritor de conexão. |
| `Flow Packets/s` | **Moderado** | Menor que o HULK/HOIC (pois o foco é manter sockets abertos, não apenas flooding bruto). |
| `PSH Flag Count` | **Elevado** | Dados de requisição e resposta enviados repetidamente na mesma sessão TCP. |
| `Fwd Packet Length Std` | **Moderado a Alto** | Devido à mistura dinâmica de requisições GET e POST com tamanhos distintos. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[DoS - Slowloris]]
- [[DoS - Hulk]]
- [[Ambiente de Ataques]]
