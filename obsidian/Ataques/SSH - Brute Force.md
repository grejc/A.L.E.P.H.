# SSH - Brute Force

- **Classe no CSE-CIC-IDS2018:** `SSH-BruteForce`
- **Volume no Dataset Corrigido:** 94.197 fluxos
- **Camada OSI:** Camada 7 / Camada 4 (Autenticação SSH sobre TCP porta 22)
- **Alvo no Laboratório:** Serviço `sshd` no host Ubuntu da vítima ([[Atacante e Vítima]])
- **Status de Reprodução:** Reproduzível no laboratório

---

## 1. Ferramenta no Kali Linux

- **Ferramenta Principal:** `hydra` (THC-Hydra, nativo e padrão no Kali Linux)
- **Alternativas Nativas no Kali:** `medusa`, `ncrack`, `patator`
- **Verificação de Instalação:** O Hydra já vem pré-instalado em todas as distribuições padrão do Kali Linux:
  ```bash
  which hydra
  ```

---

## 2. Como a Ferramenta Realiza o Ataque

O **SSH-BruteForce** tem como objetivo obter acesso não autorizado a contas de sistema através de tentativas repetidas de combinações de usuários e senhas contra o protocolo SSH:

1. **Estabelecimento de Sessão TCP e Negociação Criptográfica:**
   Para cada tentativa (ou lote de tentativas permitidas por sessão), a ferramenta estabelece o handshake TCP de 3 vias (`SYN -> SYN/ACK -> ACK`) com a porta 22 do alvo.
2. **Troca de Chaves SSH (Key Exchange):**
   O cliente e o servidor negociam a versão do protocolo (`SSH-2.0`), trocam listas de cifras suportadas, realizam o algoritmo de troca de chaves Diffie-Hellman e inicializam o canal criptografado.
3. **Submissão do Pacote de Autenticação:**
   Dentro da camada segura do SSH, a ferramenta envia a mensagem `SSH_MSG_USERAUTH_REQUEST` contendo o método de autenticação por senha (`password`), o nome de usuário e a senha candidatos lidos de listas.
4. **Tratamento de Resposta e Desconexão:**
   - Se o servidor responder com `SSH_MSG_USERAUTH_FAILURE`, a ferramenta registra a falha. Dependendo da configuração de tarefas concorrentes e do parâmetro `MaxAuthTries` do `sshd`, a conexão é finalizada com um pacote `FIN` ou `RST`, ou reaproveitada para a próxima tentativa.
   - O Hydra gerencia dezenas de threads em paralelo (flag `-t`), acelerando a taxa de tentativas.

---

## 3. Modo de Execução no Testbed (Kali $\rightarrow$ Ubuntu)

```bash
# 1. Execução com Hydra (conforme documentação oficial do kali-tools)
hydra -l [USUARIO] -P [WORDLIST] ssh://[IP_VITIMA] -t 4 -f -V

# 2. Alternativa com Medusa (módulo nativo ssh)
medusa -h [IP_VITIMA] -u [USUARIO] -P [WORDLIST] -M ssh -t 4 -f

# 3. Alternativa com Patator (módulo nativo ssh_login)
patator ssh_login host=[IP_VITIMA] user=[USUARIO] password=FILE0 0=[WORDLIST] -t 4
```

- `-l [USUARIO]` / `-u [USUARIO]`: Define o nome de usuário alvo (ou lista via `-L` / `-U`).
- `-P [WORDLIST]`: Caminho para o dicionário de senhas (ex.: `/usr/share/wordlists/metasploit/unix_passwords.txt` ou lista customizada).
- `ssh://[IP_VITIMA]`: Especificação do protocolo e endereço IP da máquina vítima.
- `-t 4`: Quantidade de tarefas/conexões simultâneas (o padrão oficial do Hydra é 16; em laboratório recomenda-se 4 a 6 para evitar negação de serviço prematura no `sshd`).
- `-f`: Encerra o teste imediatamente ao identificar o primeiro par de credenciais válido.
- `-V`: Modo verboso, exibindo as credenciais tentadas a cada ciclo.

> [!NOTE]
> No framework de testes automatizados ([[AGENTS]]), este vetor é atribuído ao especialista `SshBruteAuditor`.


---

## 4. Assinatura e Impacto nas Features do NIDS (ALF-MoE)

Devido ao custo computacional da troca de chaves e à criptografia do SSH, os fluxos gerados possuem um perfil estocástico e estrutural bastante característico:

| Feature de Fluxo | Comportamento Observado | Justificativa Operacional |
| :--- | :---: | :--- |
| `Flow Duration` | **Curta e Uniforme** | Handshake $\rightarrow$ negociação $\rightarrow$ falha $\rightarrow$ fechamento imediato. |
| `Fwd Packet Length Std` / `Bwd Packet Length Std` | **Baixo** | O tamanho dos pacotes de negociação de cifras e envio de pacotes cifrados SSH é extremamente previsível e similar entre tentativas. |
| `Flow Packets/s` | **Moderado a Elevado** | Sequência ininterrupta de novas conexões TCP. |
| `RST Flag Count` / `FIN Flag Count` | **Elevado** | Finalizações contínuas de sessões rejeitadas. |
| `SYN Flag Count` | **Elevado** | Abertura sucessiva de conexões para cada nova tentativa ou após timeout. |
| `Fwd Init Win Bytes` | **Consistente** | Padrão característico da pilha TCP do cliente Linux. |

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Atacante e Vítima]]
- [[Web Attack - Brute Force]]
- [[Infiltration - NMAP Portscan]]
