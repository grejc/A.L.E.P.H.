# DoS - Hulk (HTTP Unbearable Load King)

- **Classe no CSE-CIC-IDS2018:** `DoS Hulk`
- **Volume no Dataset Corrigido:** 1.803.160 fluxos (maior classe de ataque do dataset)
- **Camada OSI:** Camada 7 (Aplicação - HTTP)
- **Alvo no Laboratório:** Servidor Web / Aplicação [[Ambiente de Ataques]] (`http://[ALVO]:8080`)
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta:** `hulk` / `hulk.py` (Script Python / utilitário de teste de estresse HTTP)
- **Alternativas Nativas no Kali:** `slowhttptest` (com flooding HTTP), `siege`, `ab` (ApacheBench) ou `wrk`
- **Instalação / Disponibilidade:** Pode ser clonado e executado diretamente via Python no Kali Linux:
  ```bash
  # Execução via Python no Kali
  python3 hulk.py [URL_ALVO]
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **HULK** foi projetado especificamente para exaurir recursos de servidores web (CPU, memória e conexões concorrentes) através de uma sobrecarga contínua de requisições HTTP GET, implementando mecanismos de evasão para impedir o cache:

1. **Geração Randômica de URLs (Bypass de Cache):**
   A ferramenta anexa parâmetros aleatórios à query string de cada requisição (ex.: `http://[ALVO]:8080/?rnd=9812481`). Isso impede que servidores proxy, caches reversos (ex.: Varnish, Nginx) ou pools em memória entreguem respostas em cache, forçando o servidor web backend (ex.: Apache/PHP) a processar e renderizar a página repetidamente.
2. **Rotação Dinâmica de Cabeçalhos:**
   A cada requisição emitida, a ferramenta sorteia um `User-Agent` de uma lista pré-definida de navegadores conhecidos e insere referers fictícios, dificultando regras estáticas de firewall de aplicação (WAF).
3. **Inibição de Cache no Protocolo:**
   Inclui explicitamente cabeçalhos como `Cache-Control: no-cache` e `Pragma: no-cache`, instruindo todos os nós intermediários a encaminhar a requisição diretamente ao processo do servidor.
4. **Conexões Persistentes:**
   Utiliza cabeçalhos `Keep-Alive` para manter os sockets abertos enquanto despeja novos lotes de requisições, consumindo rapidamente o limite máximo de workers do servidor (`MaxRequestWorkers` do Apache).

---

## 3. Parâmetros e Modo de Execução no Testbed

```bash
# Execução conceitual contra o alvo de laboratório
python3 hulk.py http://[ALVO]:8080/
```

- `http://[ALVO]:8080/`: URL da aplicação web hospedada na vítima ([[Ambiente de Ataques]]).
- Cada thread gerada dispara em loop contínuo conexões HTTP GET sem pausas deliberadas.

---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Durante o ataque HULK, o tráfego capturado pelo extrator de fluxo ([[CICFlowMeter Features VS NFStream Features]]) apresenta um perfil altamente característico:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Packets/s` / `Flow Bytes/s` | **Extremamente Elevado** | Flooding contínuo de dados sem intervalo de descanso. |
| `Flow Duration` | **Baixa a Moderada** | Conexões rápidas com ciclos curtos de request/response até a queda do serviço. |
| `Fwd Packets/s` | **Muito Superior ao Normal** | Envio massivo de requisições GET em alta frequência. |
| `Flow IAT Mean` / `Flow IAT Min` | **Próximo de Zero** | Tempo entre chegadas de pacotes quase nulo devido ao envio contínuo. |
| `PSH Flag Count` | **Elevado** | Flag PSH ativada no envio de requisições HTTP para entrega imediata no socket. |
| `Fwd Packet Length Std` | **Moderado** | Variação gerada pela aleatoriedade do comprimento das URLs forjadas na query string. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Ambiente de Ataques]]
- [[Atacante e Vítima]]
- [[DDoS - HOIC]]
