# Infiltration - Dropbox Download

- **Classe no CSE-CIC-IDS2018:** `Infiltration - Dropbox Download`
- **Volume no Dataset Corrigido:** 85 fluxos (0,0001% do dataset global; preservado 100% na amostragem estratificada)
- **Camada OSI:** Camada 7 (Transferência de Arquivo TLS/HTTPS na porta 443)
- **Status no Laboratório:** **NÃO REPRODUZIDO (FORA DE ESCOPO)**

---

## 1. Contexto e Origem no CSE-CIC-IDS2018

No experimento original conduzido pelo Canadian Institute for Cybersecurity (CIC) em 2018, a classe `Infiltration - Dropbox Download` representou a fase de entrega de artefato malicioso (*delivery phase*) dentro de um cenário de infiltração multifásica:

1. Um usuário interno da rede corporativa simulada recebia um e-mail contendo um link para download de um arquivo supostamente legítimo.
2. Ao clicar no link, a máquina da vítima realizava o download de um documento PDF comprometido hospedado na plataforma pública do **Dropbox** via protocolo criptografado HTTPS (porta 443/TCP).
3. O arquivo continha um exploit projetado para corromper a memória de uma versão vulnerável do **Adobe Acrobat Reader 9.0** em um sistema operacional **Windows**, instalando uma backdoor do Metasploit que subsequentemente abria a sessão de C2 ([[Infiltration - Communication Victim Attacker]]) e desencadeava o escaneamento de portas ([[Infiltration - NMAP Portscan]]).

---

## 2. Ferramenta Equivalente no Kali Linux

Caso fosse executado em ambiente teórico, o tráfego seria gerado por utilitários de transferência web seguros via TLS/HTTPS:
- **Ferramentas:** `curl`, `wget` ou navegadores automatizados (`chromium`, `firefox-esr`).
- **Comando Conceitual:**
  ```bash
  # Download conceitual de arquivo via HTTPS
  wget --no-check-certificate https://www.dropbox.com/s/[TOKEN]/payload.bin
  ```

---

## 3. Dinâmica de Rede e Assinatura de Fluxo

Em termos de características de rede capturadas por ferramentas de fluxo ([[CICFlowMeter Features VS NFStream Features]]):
- **Handshake TLS 1.2/1.3:** Inicialização padrão na porta 443 com troca de certificados digitais válidos emitidos para domínios da infraestrutura do Dropbox / CDN (ex.: Cloudflare, Fastly, AWS).
- **Transferência Monodirecional de Dados:** Fluxo com grande volume de dados no sentido reverso (`Total Length of Bwd Packet` elevado) e poucos pacotes de confirmação no sentido de ida (`Fwd Packets`), típico de qualquer download de arquivo via web.
- **Indistinguibilidade Estatística:** Do ponto de vista estritamente estatístico de fluxo de rede, **o tráfego é 100% indistinguível de um download legítimo de documento ou software via HTTPS**. O NIDS não descriptografa a sessão TLS para inspecionar o conteúdo binário em trânsito.

---

## 4. Justificativa Formal de Exclusão do Escopo de Reprodução

A reprodução prática deste ataque no ambiente de laboratório ([[Atacante e Vítima]]) foi **formalmente descartada** com base nos seguintes critérios metodológicos e operacionais:

### 4.1. Dependência de Infraestrutura Externa e Serviços de Terceiros (SaaS)
A reprodução fiel exigiria hospedar ativamente artefatos de teste em servidores comerciais do Dropbox Inc. Essa prática esbarra em:
- **Violação de Termos de Serviço (ToS):** Hospedagem de payloads binários ou simuladores de exploração viola os termos de uso de provedores de nuvem pública.
- **Mecanismos Anti-Malware em Nuvem:** Servidores do Dropbox utilizam varreduras automatizadas que excluem ou bloqueiam links de compartilhamento de arquivos com assinaturas anômalas, inviabilizando testes reprodutíveis.
- **Dependência de Conectividade WAN Externa:** Introduz variabilidade incontrolável de latência, jitter e tráfego de Internet pública que contamina o ambiente estritamente controlado do laboratório.

### 4.2. Incompatibilidade com o Testbed Local (Linux/Docker)
O exploit do cenário original de 2018 visava uma vulnerabilidade específica de corrupção de memória do Adobe Acrobat Reader 9.0 em ambiente Windows. A máquina vítima do laboratório experimental é um notebook **Acer Nitro V15 rodando Ubuntu Linux** com serviços conteinerizados em **Docker** ([[Ambiente de Ataques]]). Essa cadeia de exploração de endpoint é nula e irrelevante no ecossistema atual.

### 4.3. Irrelevância Quantitativa no Dataset
No dataset completo corrigido de 63 milhões de fluxos, existem apenas **85 registros** catalogados como `Infiltration - Dropbox Download` (representando 0,0001% do total). Trata-se de uma anomalia de amostragem no dataset original que não justifica a mobilização de infraestrutura externa.

### 4.4. Limitação Inerente de NIDS Baseados em Fluxo
Como o **ALF-MoE** opera sobre features estatísticas agregadas de fluxo (sem descriptografia profunda de TLS), um fluxo de download via Dropbox tem as mesmas características de um fluxo benéfico de atualização de pacotes ou navegação web segura. Tentar classificar "download do Dropbox" como intrusão com base apenas em pacotes de fluxo levaria a modelos com overfitting espúrio em IPs da CDN do Dropbox.

---

## 5. Relação com outras Notas

- [[00 - Mapeamento de Ataques Kali Linux]]
- [[Infiltration - Communication Victim Attacker]]
- [[Infiltration - NMAP Portscan]]
- [[Atacante e Vítima]]
- [[Ambiente de Ataques]]
