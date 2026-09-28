# Web Attack - SQL Injection

- **Classe no CSE-CIC-IDS2018:** `Web Attack - SQL`
- **Volume no Dataset Corrigido:** 39 fluxos (menor classe de ataque efetivo do dataset; mantida 100% na amostragem)
- **Camada OSI:** Camada 7 (Aplicação - Injeção de Comandos SQL em HTTP)
- **Alvo no Laboratório:** Módulo SQL Injection do DVWA ([[Ambiente de Ataques]]) na porta 8080
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal no Kali:** `sqlmap` (a ferramenta de referência mundial para auditoria e exploração automatizada de SQL Injection, pré-instalada no Kali)
- **Alternativas:** `ghauri`, `burpsuite` (Scanner/Intruder), scripts customizados com `requests` em Python
- **Verificação no Kali:**
  ```bash
  which sqlmap
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O ataque de **SQL Injection (SQLi)** ocorre quando dados fornecidos pelo usuário são concatenados diretamente em comandos ou consultas enviadas ao banco de dados relacional sem parametrização ou uso de *Prepared Statements*:

1. **Enumeração e Teste de Ponto de Injeção:**
   O `sqlmap` recebe a URL alvo e os parâmetros de entrada (ex.: `id=1` em `http://[ALVO]:8080/vulnerabilities/sqli/?id=1&Submit=Submit`). A ferramenta testa sistematicamente uma ampla variedade de payloads para identificar o tipo e a versão do Sistema Gerenciador de Banco de Dados (SGBD).
2. **Técnicas de Injeção Empregadas:**
   - **Boolean-based Blind:** Injeta expressões lógicas com resultados verdadeiros e falsos (ex.: `AND 1=1` vs `AND 1=2`), observando sutis variações na renderização da página web resultante.
   - **Error-based:** Injeta caracteres de quebra de sintaxe (como aspas `'` ou comandos inválidos) para forçar o SGBD (ex.: MySQL, MariaDB) a cuspir mensagens de erro detalhadas contendo dados de tabelas no corpo do HTML.
   - **UNION Query-based:** Adiciona operadores `UNION SELECT` para mesclar dados das tabelas internas do banco com os dados exibidos legitimamente na tela.
   - **Time-based Blind:** Injeta comandos que forçam pausas intencionais na execução do banco (ex.: `SLEEP(5)` no MySQL ou `pg_sleep(5)` no PostgreSQL), cronometrando a latência de resposta da aplicação para extrair informações caractere por caractere.
   - **Stacked Queries:** Envia comandos adicionais separados por ponto e vírgula `;`.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ DVWA)

```bash
# Execução automatizada com sqlmap (conforme documentação oficial do kali-tools)
sqlmap -u "http://[ALVO]:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=[SESSION_ID]; security=low" \
       -p id \
       --batch \
       --dbs
```

- `-u "URL"`: Endpoint vulnerável do DVWA ([[Ambiente de Ataques]]).
- `--cookie`: Cabeçalho com o cookie de autenticação ativo do DVWA.
- `-p id`: Força o teste exclusivamente no parâmetro vulnerável `id`, acelerando a validação e mantendo os fluxos focados no NIDS.
- `--batch`: Modo não interativo essencial para execução autônoma por agentes LLM, adotando as respostas padrão recomendadas.
- `--dbs`: Enumera os nomes dos bancos de dados como prova de conceito (PoC não destrutivo).
- `--technique=T`: (Opcional) Restringe a técnica a *Time-based Blind* (`SLEEP`), gerando a assinatura de alta duração de fluxo no NIDS.

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `SqlInjectionProbe`.


---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Durante a execução do `sqlmap`, o tráfego de rede reflete fases distintas com impactos nas features estatísticas:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Altamente Variável** | Fluxos curtos durante testes de erro/blind, mas com **picos drásticos de duração** em testes *Time-based* (`SLEEP`). |
| `Active Mean` vs `Idle Mean` | **Idle Mean Elevado (Time-based)** | O servidor retém a resposta HTTP deliberadamente enquanto o comando `SLEEP` é processado pelo SGBD. |
| `Fwd Packet Length Mean` | **Moderado** | Requisições HTTP com strings de injeção relativamente longas em relação a cliques normais. |
| `Bwd Packet Length Std` | **Variável** | Respostas de erro curtas alternadas com páginas completas contendo dados de tabelas despejados. |
| `Flow Packets/s` | **Moderado a Contínuo** | Requisições sequenciais de teste em regime de probing. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Ambiente de Ataques]]
- [[Web Attack - XSS]]
- [[Web Attack - Brute Force]]
