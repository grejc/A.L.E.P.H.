# DoS - Slowloris

- **Classe no CSE-CIC-IDS2018:** `DoS Slowloris`
- **Volume no Dataset Corrigido:** 8.490 fluxos
- **Camada OSI:** Camada 7 (Aplicação - Incomplete HTTP Headers)
- **Alvo no Laboratório:** Servidor Web DVWA ([[Ambiente de Ataques]]) na porta 8080 (Apache)
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramentas Nativas / Disponíveis:**
  - `slowhttptest` (ferramenta padrão no Kali Linux para testes de estresse lento em HTTP).
  - `slowloris` / `python3-slowloris` (script Python original do Slowloris).
- **Instalação / Verificação:**
  ```bash
  # slowhttptest é o utilitário nativo mais flexível no Kali
  sudo apt install slowhttptest
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **Slowloris** é um ataque clássico de negação de serviço de baixa taxa de transferência (*Low and Slow / Slow-rate DoS*). Ele não busca sobrecarregar a largura de banda da vítima, mas sim estrangular os recursos de concorrência do servidor web:

1. **Abertura de Conexões TCP Concorrentes:**
   O atacante estabelece centenas de conexões TCP com o servidor HTTP/HTTPS da vítima.
2. **Envio de Cabeçalhos HTTP Parciais e Incompletos:**
   A ferramenta envia o início de uma requisição HTTP válida:
   ```http
   GET / HTTP/1.1\r\n
   Host: [ALVO]\r\n
   User-Agent: Mozilla/5.0 ...\r\n
   ```
   Entretanto, **omite deliberadamente a sequência de terminação obrigatória do protocolo HTTP** (que consiste em uma linha vazia com `\r\n\r\n`).
3. **Mecanismo de "Keep-Alive" Fictício por Fragmentação:**
   Como a requisição está incompleta, o servidor web mantém a conexão aberta e aloca uma thread inteira ou processo de worker (ex.: modelo Prefork do Apache) aguardando o restante dos cabeçalhos. Pouco antes do tempo limite de timeout do servidor expirar (ex.: a cada 10 a 15 segundos), o Slowloris envia um cabeçalho fictício adicional:
   ```http
   X-Custom-Header: 12345\r\n
   ```
4. **Esgotamento Completo de Conexões:**
   Isso reseta o temporizador de timeout da conexão no servidor. Com apenas alguns kilobytes de tráfego gerados pelo atacante, todas as threads disponíveis no servidor (`MaxClients` / `MaxRequestWorkers`) ficam presas. Quando um usuário legítimo tenta conectar, recebe erro de *timeout* ou conexão recusada.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ Ubuntu)

```bash
# Execução com slowhttptest em modo Slowloris (-H) no Kali (conforme kali-tools)
slowhttptest -c 1000 -H -g -o slowloris_test -i 10 -r 200 -t GET -u http://[ALVO]:8080/ -x 24 -p 3 -l 60
```

- `-c 1000`: Tenta manter 1000 conexões simultâneas com o alvo.
- `-H`: Habilita o modo Slowloris (*Slow Headers*).
- `-g`: Gera arquivos estatísticos de diagnóstico (`slowloris_test.csv` e gráficos).
- `-o slowloris_test`: Prefixo de saída para os relatórios de teste.
- `-i 10`: Intervalo de 10 segundos entre envios de dados parciais para manter a conexão aberta.
- `-r 200`: Conexões iniciadas por segundo (*connection rate*).
- `-t GET`: Método HTTP utilizado.
- `-u http://[ALVO]:8080/`: URL alvo do serviço DVWA ([[Ambiente de Ataques]]).
- `-x 24`: Tamanho máximo de 24 bytes para os fragmentos adicionais de cabeçalho.
- `-p 3`: Timeout de sonda de 3 segundos para detecção de indisponibilidade do serviço.
- `-l 60`: Limite estrito de 60 segundos de duração do teste (garante contenção e recuperação do laboratório, conforme [[AGENTS]]).

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `SlowlorisTester`.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

O Slowloris gera o perfil mais assimétrico e atípico entre todos os ataques DoS:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Extremamente Longo** | As conexões são mantidas intencionalmente por dezenas ou centenas de segundos. |
| `Flow Bytes/s` | **Praticamente Nulo** | Apenas alguns bytes são enviados a cada 10-15 segundos. |
| `Flow Packets/s` | **Mínimo** | Pacotes esparsos, sem nenhum padrão de flooding. |
| `Flow IAT Max` / `Flow IAT Mean` | **Muito Alto** | Intervalos longos entre pacotes consecutivos (próximos a 10-15 segundos). |
| `Total Length of Fwd Packet` | **Minúsculo** | O tamanho total transmitido consiste apenas nos pequenos fragmentos de cabeçalho. |
| `Active Mean` vs `Idle Mean` | **Idle Mean >> Active Mean** | O fluxo passa a maior parte de sua vida em estado de espera ociosa. |

> [!TIP]
> Essa discrepância drástica de `Flow Bytes/s` e `Flow Duration` em relação aos ataques volumétricos (Hulk, HOIC) torna o Slowloris um excelente teste para verificar se o modelo **ALF-MoE** aprendeu a correlacionar dinâmicas temporais de starvation e não apenas picos de volume.

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[DoS - GoldenEye]]
- [[DoS - Hulk]]
- [[Ambiente de Ataques]]
