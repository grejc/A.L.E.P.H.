# Web Attack - XSS (Cross-Site Scripting)

- **Classe no CSE-CIC-IDS2018:** `Web Attack - XSS`
- **Volume no Dataset Corrigido:** 113 fluxos (classe minoritária estrita mantida 100% na amostragem)
- **Camada OSI:** Camada 7 (Aplicação - Injeção de Scripts em HTTP)
- **Alvo no Laboratório:** Módulos XSS (Reflected, Stored, DOM) do DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Especializada no Kali:** `xsser` (ferramenta automatizada de auditoria e injeção de XSS pré-instalada no Kali)
- **Alternativas de Fuzzing Web:** `ffuf`, `wfuzz`, `owasp-zap`, `burpsuite`
- **Verificação no Kali:**
  ```bash
  which xsser
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O ataque de **Cross-Site Scripting (XSS)** explora a ausência de sanitização e escape adequado de entradas de dados fornecidas pelo usuário que são refletidas ou armazenadas e executadas no navegador web de outros clientes:

1. **Injeção de Payloads:**
   A ferramenta envia sequências de caracteres de script (JavaScript/HTML) em parâmetros de requisições HTTP GET ou POST (ex.: `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, `"><svg onload=alert(1)>`).
2. **Avaliação da Resposta (Reflected XSS):**
   A ferramenta inspeciona o corpo da resposta HTTP (`HTML DOM`) para verificar se os caracteres injetados foram retornados sem codificação de entidades HTML (`&lt;`, `&gt;`). Se o payload for refletido integralmente, a vulnerabilidade é confirmada.
3. **Persistência de Payloads (Stored XSS):**
   Em formulários de mensagens ou comentários (como no módulo *XSS Stored* do DVWA), o payload é salvo no banco de dados e executado sempre que qualquer usuário carrega a página correspondente.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ DVWA)

```bash
# 1. Execução com xsser (conforme documentação oficial do kali-tools)
xsser -u "http://[ALVO]:8080/vulnerabilities/xss_r/" \
      -g "/vulnerabilities/xss_r/?name=XSS" \
      --cookie="PHPSESSID=[SESSION_ID]; security=low" \
      --auto \
      --auto-set=30

# 2. Alternativa com ffuf e wordlist de XSS (modo não interativo)
ffuf -u "http://[ALVO]:8080/vulnerabilities/xss_r/?name=FUZZ" \
     -w /usr/share/seclists/Fuzzing/XSS/XSS-Cheat-Sheet-PortSwigger.txt \
     -H "Cookie: PHPSESSID=[SESSION_ID]; security=low" \
     -t 5 -noninteractive -s
```

- `-u "URL"`: Endpoint base da aplicação DVWA ([[Ambiente de Ataques]]).
- `-g "...?name=XSS"`: Define a injeção via método GET utilizando o marcador padrão `XSS`.
- `--cookie`: Cabeçalho de autenticação com a sessão ativa do DVWA.
- `--auto`: Fuzzing automatizado a partir da base nativa do `xsser`.
- `--auto-set=30`: Limita o lote a 30 vetores para testes rápidos e controlados.
- `-noninteractive` (no `ffuf`): Execução headless para agentes autônomos.

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `XssFuzzProbe`.


---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Em sistemas NIDS operando em nível estatístico de fluxos de rede (como CICFlowMeter e NFStream, sem decodificação profunda de payload de aplicação):

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Curta** | Transações HTTP normais de envio de requisição e recebimento de resposta HTML. |
| `Fwd Packet Length Mean` | **Ligeiramente Superior** | Devido ao tamanho adicional dos caracteres de injeção e URL-encoding (`%3Cscript...`). |
| `Total Fwd Packets` / `Total Bwd Packets` | **Pequeno** | Tipicamente poucos pacotes por fluxo (requisição + resposta completa). |
| `Flow Packets/s` | **Baixo a Moderado** | Fuzzing sequencial com pausas curtas de análise. |
| `Down/Up Ratio` | **Equilibrado ou Maior para Bwd** | Resposta HTML com o conteúdo da página costuma ser maior que o pacote de envio. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Ambiente de Ataques]]
- [[Web Attack - SQL Injection]]
- [[Web Attack - Brute Force]]
