# Relatório Completo de Análise Exploratória de Dados (EDA)

## Dataset: CSE-CIC-IDS2018 Melhorado (`CSECICIDS2018_improved.csv`)

  

---

  

## 1. Status e Metadados da Análise

  

- **Data da Análise:** 2026-09-25

- **Classificação:** Exploratória / Geração de Hipóteses e Engenharia de Features

- **Interpretação Causal Permitida:** Não (associações estatísticas observadas não implicam causalidade)

- **Modificação dos Dados Brutos:** Não (o dataset bruto de 34 GB permanece intacto e somente para leitura)

- **Imputação ou Remoção Automática em Dados Brutos:** Não realizada

- **Ambiente de Execução:** Python 3.11.9 (`~/.venv`), PyArrow 25.0.0, pandas 3.0.3, NumPy 2.4.6, SciPy 1.17.1, Seaborn 0.13.2, Matplotlib 3.11.1

  

> [!IMPORTANT]

> **Contrato de Privacidade e Segurança:** Todos os cabeçalhos, rótulos e células de rede foram tratados como dados não confiáveis. A quíntupla de identificação de rede (`Src IP`, `Src Port`, `Dst IP`, `Dst Port`, `Protocol`), chaves primárias (`id`, `Flow ID`), marcas temporais (`Timestamp`) e metadados operacionais (`Attempted Category`) foram devidamente auditados e excluídos do pipeline de features para prevenir *data leakage* e memorização espúria de topologia de laboratório.

  

---

  

## 2. Manifesto do Arquivo e Capacidade de I/O

  

- **Identificador do Arquivo:** `CSECICIDS2018_improved.csv`

- **Tamanho Físico em Disco:** 36.044.453.883 bytes (~34 GiB)

- **Volume Total de Registros:** 63.195.145 linhas

- **Total de Colunas Brutas:** 91 colunas

- **Formato:** UTF-8 Tabular Delimitado por Vírgula (CSV)

- **Mecanismo de Ingestão:** Streaming em lote multithread via PyArrow com tipagem estrita de schema (`block_size = 64 MiB`)

  

---

  

## 3. Dicionário de Variáveis e Estrutura de Medição

  

O dataset CSE-CIC-IDS2018 Improved foi construído para corrigir falhas severas de rotulagem, divisão de fluxos TCP e contagem temporal presentes na versão original do CIC-IDS2018 (gerada pelo CICFlowMeter-V3).

  

A segmentação dos atributos foi definida da seguinte forma:

  

### 3.1. Metadados e Atributos Identificadores Removidos (9 colunas)

Para garantir que modelos preditivos aprendam padrões intrínsecos de tráfego (tamanho de pacotes, dinâmica temporal, janelas, flags) e não atalhos mnemônicos da rede de captura:

1. `id`: Identificador sequencial de registro.

2. `Flow ID`: Hash/identificador único do fluxo.

3. `Src IP`: Endereço IP de origem (risco de memorização do IP da máquina atacante).

4. `Src Port`: Porta de origem efêmera.

5. `Dst IP`: Endereço IP de destino (risco de memorização do IP do servidor vítima).

6. `Dst Port`: Porta de destino de serviço (80, 443, 21, 22).

7. `Protocol`: Protocolo de transporte (6 = TCP, 17 = UDP).

8. `Timestamp`: Marcação temporal da captura (introduz vazamento temporal severo se não particionado por janelas temporais estritas).

9. `Attempted Category`: Metadado interno indicador do tipo de tentativa de ataque (utilizado para re-rotulamento e depois descartado).

  

### 3.2. Espaço de Features Mantido (81 Métricas Estatísticas de Tráfego de Rede)

Divididas em famílias operacionais:

- **Dinâmica Temporal de Fluxo e IAT (Inter-Arrival Time):** `Flow Duration`, `Flow IAT Mean`, `Flow IAT Std`, `Flow IAT Max`, `Flow IAT Min`, `Fwd IAT Total`, `Fwd IAT Mean`, `Fwd IAT Std`, `Fwd IAT Max`, `Fwd IAT Min`, `Bwd IAT Total`, `Bwd IAT Mean`, `Bwd IAT Std`, `Bwd IAT Max`, `Bwd IAT Min`, `Active Mean`, `Active Std`, `Active Max`, `Active Min`, `Idle Mean`, `Idle Std`, `Idle Max`, `Idle Min`, `Total TCP Flow Time`.

- **Estatísticas Volumétricas de Pacotes e Bytes:** `Total Fwd Packet`, `Total Bwd packets`, `Total Length of Fwd Packet`, `Total Length of Bwd Packet`, `Fwd Packet Length Max`, `Fwd Packet Length Min`, `Fwd Packet Length Mean`, `Fwd Packet Length Std`, `Bwd Packet Length Max`, `Bwd Packet Length Min`, `Bwd Packet Length Mean`, `Bwd Packet Length Std`, `Packet Length Min`, `Packet Length Max`, `Packet Length Mean`, `Packet Length Std`, `Packet Length Variance`, `Average Packet Size`, `Fwd Segment Size Avg`, `Bwd Segment Size Avg`.

- **Taxas de Vazão (Throughput e Frequência):** `Flow Bytes/s`, `Flow Packets/s`, `Fwd Packets/s`, `Bwd Packets/s`.

- **Controle de Camada de Transporte e Flags TCP:** `Fwd PSH Flags`, `Bwd PSH Flags`, `Fwd URG Flags`, `Bwd URG Flags`, `Fwd RST Flags`, `Bwd RST Flags`, `FIN Flag Count`, `SYN Flag Count`, `RST Flag Count`, `PSH Flag Count`, `ACK Flag Count`, `URG Flag Count`, `CWR Flag Count`, `ECE Flag Count`.

- **Janelas TCP e Cabeçalhos:** `Fwd Header Length`, `Bwd Header Length`, `FWD Init Win Bytes`, `Bwd Init Win Bytes`, `Fwd Act Data Pkts`, `Fwd Seg Size Min`, `Down/Up Ratio`.

- **Métricas de Subfluxo e Bulk:** `Subflow Fwd Packets`, `Subflow Fwd Bytes`, `Subflow Bwd Packets`, `Subflow Bwd Bytes`, `Fwd Bytes/Bulk Avg`, `Fwd Packet/Bulk Avg`, `Fwd Bulk Rate Avg`, `Bwd Bytes/Bulk Avg`, `Bwd Packet/Bulk Avg`, `Bwd Bulk Rate Avg`.

- **Protocolos de Controle:** `ICMP Code`, `ICMP Type`.

- **Rótulo Alvo:** `Label` (categórico, 15 classes pós-re-rotulagem).

  

---

  

## 4. Auditoria de Re-rotulamento: Classes "Attempted" -> "BENIGN"

  

### 4.1. Fundamentação Teórica e Operacional

Na taxonomia de sistemas de detecção de intrusão, fluxos marcados como **"Attempted"** representam ações de sondagem, varredura ou exploração disparadas pelos atacantes mas que **não obtiveram sucesso** (ex.: conexões recusadas por firewall, credenciais rejeitadas com erro de autenticação imediata, ou payloads HTTP bloqueados/inválidos). Em cenários de teste operacional realista, tais fluxos assemelham-se funcionalmente ao ruído de fundo ou a falhas comuns de conectividade. Reclassificá-los como `BENIGN` testa a capacidade do classificador de diferenciar ataques efetivos de meras conexões falhas sem gerar alarmes falsos excessivos.

  

### 4.2. Mapeamento Quantitativo em Larga Escala (63.195.145 Fluxos)

A varredura exaustiva do dataset completo revelou:

- **Total de Fluxos "Attempted":** 306.237 fluxos (0,485% do dataset global).

- **Total Original de BENIGN:** 59.353.486 fluxos (93,921%).

- **Total Pós-Re-rotulamento de BENIGN:** **59.659.723 fluxos (94,405%)**.

  

> [!WARNING]

> **DESCOBERTA CRÍTICA: Desaparecimento Empírico de `FTP-BruteForce`**

> A análise revelou que **100% dos fluxos de `FTP-BruteForce` no dataset melhorado (298.874 fluxos) estão rotulados como `Attempted`**. Não existe nenhum fluxo catalogado como ataque bem-sucedido de FTP Brute Force.

> Consequentemente, **ao re-rotular "Attempted" como "BENIGN", a classe `FTP-BruteForce` é totalmente absorvida pela classe `BENIGN`, deixando de existir no conjunto de ataques reais**.

  

Tabela detalhada da redistribuição:

  

| Classe Original                                  |      Tipo      | Contagem Bruta | Ação no Cenário | Classe Resultante                              |
| ------------------------------------------------ | :------------: | -------------: | :-------------: | :--------------------------------------------- |
| **BENIGN**                                       |    Legítimo    |     59.353.486 |   Preservado    | `BENIGN`                                       |
| **FTP-BruteForce - Attempted**                   |   Tentativa    |        298.874 |   Re-rotulado   | `BENIGN`                                       |
| **DoS GoldenEye - Attempted**                    |   Tentativa    |          4.301 |   Re-rotulado   | `BENIGN`                                       |
| **DoS Slowloris - Attempted**                    |   Tentativa    |          2.280 |   Re-rotulado   | `BENIGN`                                       |
| **Botnet Ares - Attempted**                      |   Tentativa    |            262 |   Re-rotulado   | `BENIGN`                                       |
| **DDoS-LOIC-UDP - Attempted**                    |   Tentativa    |            251 |   Re-rotulado   | `BENIGN`                                       |
| **Web Attack - Brute Force - Attempted**         |   Tentativa    |            137 |   Re-rotulado   | `BENIGN`                                       |
| **DoS Hulk - Attempted**                         |   Tentativa    |             86 |   Re-rotulado   | `BENIGN`                                       |
| **Infiltration - Dropbox Download - Attempted**  |   Tentativa    |             28 |   Re-rotulado   | `BENIGN`                                       |
| **Web Attack - SQL - Attempted**                 |   Tentativa    |             14 |   Re-rotulado   | `BENIGN`                                       |
| **Web Attack - XSS - Attempted**                 |   Tentativa    |              4 |   Re-rotulado   | `BENIGN`                                       |
| **DoS Hulk**                                     | Ataque Efetivo |      1.803.160 |     Mantido     | `DoS Hulk`                                     |
| **DDoS-HOIC**                                    | Ataque Efetivo |      1.082.293 |     Mantido     | `DDoS-HOIC`                                    |
| **DDoS-LOIC-HTTP**                               | Ataque Efetivo |        289.328 |     Mantido     | `DDoS-LOIC-HTTP`                               |
| **Botnet Ares**                                  | Ataque Efetivo |        142.921 |     Mantido     | `Botnet Ares`                                  |
| **SSH-BruteForce**                               | Ataque Efetivo |         94.197 |     Mantido     | `SSH-BruteForce`                               |
| **Infiltration - NMAP Portscan**                 | Ataque Efetivo |         89.374 |     Mantido     | `Infiltration - NMAP Portscan`                 |
| **DoS GoldenEye**                                | Ataque Efetivo |         22.560 |     Mantido     | `DoS GoldenEye`                                |
| **DoS Slowloris**                                | Ataque Efetivo |          8.490 |     Mantido     | `DoS Slowloris`                                |
| **DDoS-LOIC-UDP**                                | Ataque Efetivo |          2.527 |     Mantido     | `DDoS-LOIC-UDP`                                |
| **Infiltration - Communication Victim Attacker** | Ataque Efetivo |            204 |     Mantido     | `Infiltration - Communication Victim Attacker` |
| **Web Attack - Brute Force**                     | Ataque Efetivo |            131 |     Mantido     | `Web Attack - Brute Force`                     |
| **Web Attack - XSS**                             | Ataque Efetivo |            113 |     Mantido     | `Web Attack - XSS`                             |
| **Infiltration - Dropbox Download**              | Ataque Efetivo |             85 |     Mantido     | `Infiltration - Dropbox Download`              |
| **Web Attack - SQL**                             | Ataque Efetivo |             39 |     Mantido     | `Web Attack - SQL`                             |

  

![Distribuição de Classes e Re-rotulamento](/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/class_distribution_relabeling.png)

  

---

  

## 5. Estratégia de Amostragem de 10% com Preservação Integral de Minorias

  

### 5.1. Justificativa Metodológica

Em dados de cibersegurança caracterizados por **desbalanceamento extremo** (onde ataques representam 5,59% do tráfego e ataques raros possuem contagens de dezenas ou centenas de fluxos):

- Uma amostragem uniforme simples de 10% reduziria o ataque `Web Attack - SQL` para meras 4 instâncias, `Infiltration - Dropbox Download` para 8 instâncias e `Web Attack - XSS` para 11 instâncias. Isso inviabilizaria qualquer divisão estratificada de validação cruzada (*k-fold*).

- **Solução Adotada (Best Practice em IDS):** Preservar **100% das classes minoritárias/não volumétricas** (todas as classes com menos de 150.000 instâncias), aplicar amostragem determinística de 10% sobre os três ataques volumétricos massivos (`DoS Hulk`, `DDoS-HOIC`, `DDoS-LOIC-HTTP`), e subamostrar proporcionalmente a classe majoritária `BENIGN` para cravar a meta global exata de **10,0000%**.

  

### 5.2. Quotas e Execução da Amostragem (Seed = 42)

- **Tamanho Total do Dataset:** 63.195.145 linhas

- **Tamanho Exato da Amostra (10%):** **6.319.514 linhas**

- **Formato Gerado:** `CSECICIDS2018_improved_sample10.parquet` (994,35 MiB, compressão Snappy, leitura em frações de segundo).

  

| Classe Re-rotulada                      | População Total | Amostra Gerada (10% Global) | Taxa de Retenção (%) | Categoria Operacional      |
| :-------------------------------------- | --------------: | --------------------------: | :------------------: | :------------------------- |
| **BENIGN**                              |      59.659.723 |                   5.641.395 |        9,46%         | Majoritária (Subamostrada) |
| **DoS Hulk**                            |       1.803.160 |                     180.316 |        10,00%        | Volumétrica (10%)          |
| **DDoS-HOIC**                           |       1.082.293 |                     108.229 |        10,00%        | Volumétrica (10%)          |
| **DDoS-LOIC-HTTP**                      |         289.328 |                      28.933 |        10,00%        | Volumétrica (10%)          |
| **Botnet Ares**                         |         142.921 |                     142.921 |     **100,00%**      | Minoria Preservada         |
| **SSH-BruteForce**                      |          94.197 |                      94.197 |     **100,00%**      | Minoria Preservada         |
| **Infiltration - NMAP Portscan**        |          89.374 |                      89.374 |     **100,00%**      | Minoria Preservada         |
| **DoS GoldenEye**                       |          22.560 |                      22.560 |     **100,00%**      | Minoria Preservada         |
| **DoS Slowloris**                       |           8.490 |                       8.490 |     **100,00%**      | Minoria Preservada         |
| **DDoS-LOIC-UDP**                       |           2.527 |                       2.527 |     **100,00%**      | Minoria Preservada         |
| **Infiltration - Comm Victim Attacker** |             204 |                         204 |     **100,00%**      | Minoria Preservada         |
| **Web Attack - Brute Force**            |             131 |                         131 |     **100,00%**      | Minoria Preservada         |
| **Web Attack - XSS**                    |             113 |                         113 |     **100,00%**      | Minoria Preservada         |
| **Infiltration - Dropbox Download**     |              85 |                          85 |     **100,00%**      | Minoria Preservada         |
| **Web Attack - SQL**                    |              39 |                          39 |     **100,00%**      | Minoria Preservada         |
| **TOTAL**                               |  **63.195.145** |               **6.319.514** |     **10,0000%**     | **Consistência Perfeita**  |

  

![Representatividade da Amostra e Preservação de Minorias](/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/sample_vs_population_minorities.png)

  

---

  

## 6. Auditoria de Qualidade e Integridade de Dados

  

Durante o processamento em streaming da totalidade dos dados (63,2M linhas), foram constatadas as seguintes anomalias estruturais:

  

### 6.1. Valores Infinitos (`+inf`)

- Ocorrem exatamente **57 vezes** em `Flow Bytes/s` e **57 vezes** em `Flow Packets/s`.

- **Causa Raiz:** Ocorre quando `Flow Duration == 0` (fluxos compostos por pacotes isolados ou anomalias de timestamp do CICFlowMeter), gerando divisão por zero.

- **Recomendação para Modelagem:** Substituir por `np.nan` e imputar pela mediana condicional ou aplicar *clipping* no percentil 99,99.

  

### 6.2. Inconsistência de Tipagem Entre Dias de Coleta

- O dataset resulta da união das capturas de 10 dias de simulação. Em arquivos de determinados dias, colunas de contagem e flags foram gravadas como inteiros (`0`, `1`) e em outros como floats (`0.0`, `1.0`).

- **Solução Implementada:** O pipeline de ingestão e a amostra Parquet forçam tipagem numérica `float64` uniforme em todas as 81 features, eliminando falhas de parsing.

  

### 6.3. Colunas Constantes (Zero-Variância)

Foram identificadas 3 features completamente invariantes em todo o tráfego analisado:

1. `Fwd URG Flags` = 0 em todas as linhas.

2. `Bwd URG Flags` = 0 em todas as linhas.

3. `URG Flag Count` = 0 em todas as linhas.

- **Impacto:** Não agregam informação discriminativa e devem ser excluídas da matriz de treino para reduzir dimensionalidade e consumo de memória.

  

---

  

## 7. Análise Estatística Distribucional: Paramétrica vs. Robusta

  

A tabela abaixo compara medidas clássicas (Média, Desvio Padrão) e medidas robustas a outliers (Mediana, IQR, MAD) calculadas sobre a amostra estratificada:

  

| Feature | Média (Mean) | Desvio Padrão (Std) | Mediana (P50) | IQR (Q75 - Q25) | MAD (Med. Abs. Dev.) | Mínimo | Máximo | Assimetria (Skewness) |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Flow Duration` | 17.031.020 | 36.028.190 | 126.357 | 3.971.120 | 126.073 | 0,0 | 120.000.000 | +1,98 |
| `Total Fwd Packet` | 53,62 | 2.436,10 | 5,00 | 8,00 | 4,00 | 0,0 | 309.629 | +55,32 |
| `Total Bwd packets` | 9,51 | 192,12 | 4,00 | 6,00 | 3,00 | 0,0 | 122.171 | +140,35 |
| `Total Length Fwd Pkt`| 2.538,02 | 88.215,83 | 146,00 | 995,00 | 146,00 | 0,0 | 13.343.630 | +54,35 |
| `Total Length Bwd Pkt`| 6.495,76 | 275.211,40 | 210,00 | 1.502,00 | 210,00 | 0,0 | 156.368.700 | +132,14 |
| `Packet Length Mean` | 110,46 | 173,14 | 77,00 | 96,61 | 41,03 | 0,0 | 16.817,86 | +38,84 |
| `Average Packet Size`| 110,46 | 173,14 | 77,00 | 96,61 | 41,03 | 0,0 | 16.817,86 | +38,84 |
| `Flow Bytes/s` | 87.577,69 | 572.169,70 | 2.585,22 | 91.166,85 | 2.585,22 | 0,0 | 716.000.000 | +733,39 |
| `Flow Packets/s` | 12.207,59 | 114.776,90 | 55,25 | 1.569,44 | 54,98 | 0,017 | 5.000.000 | +12,32 |
| `Flow IAT Mean` | 877.133,80 | 2.599.541,00 | 24.193,50 | 268.537,20 | 23.926,50 | 0,0 | 119.998.100 | +13,66 |
| `FWD Init Win Bytes` | 7.107,95 | 11.472,50 | 8.192,00 | 8.192,00 | 7.935,00 | 0,0 | 65.535 | +3,54 |
| `Bwd Init Win Bytes` | 9.659,34 | 22.222,28 | 0,00 | 230,00 | 0,00 | 0,0 | 65.535 | +1,95 |

  

### Diagnósticos Estatísticos Fundamentais:

1. **Divergência Severa entre Média e Mediana:** Em `Flow Duration`, a média (17,03s) é 134 vezes maior que a mediana (0,126s). Em `Flow Bytes/s`, a média é 34 vezes a mediana. Isso evidencia distribuições de cauda ultralonga (Lei de Potência / Pareto) impulsionadas por saturação de conexões em ataques DDoS e pelo *timeout* padrão de 120 segundos do CICFlowMeter.

2. **Redundância Literal (Identidade Numérica):** As colunas `Packet Length Mean` e `Average Packet Size` possuem exatamente a mesma média, desvio, mediana e extremos. Trata-se de uma duplicação matemática gerada pelo extrator CICFlowMeter; uma delas deve ser descartada.

3. **Assimetria em Janelas TCP:** `Bwd Init Win Bytes` possui mediana 0, indicando que a maioria dos fluxos maliciosos (ou conexões sem resposta) nunca conclui o *three-way handshake* TCP, não recebendo janela de volta.

  

![Distribuições das Métricas de Rede por Família](/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/network_features_boxplots.png)

  

---

  

## 8. Análise de Multicolinearidade e Assinaturas TCP

  

### 8.1. Matriz de Correlação de Postos de Spearman

A correlação não-paramétrica de Spearman (robusta a outliers extremos) revelou blocos de multicolinearidade perfeita ou quase perfeita ($r_s \approx 1,00$):

- `Total Fwd Packet` $\leftrightarrow$ `Total Length of Fwd Packet` ($r_s = 0,92$)

- `Packet Length Mean` $\leftrightarrow$ `Average Packet Size` ($r_s = 1,00$)

- `Flow Duration` $\leftrightarrow$ `Flow IAT Max` ($r_s = 0,94$)

  

![Matriz de Correlação e Multicolinearidade de Spearman](/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/correlation_multicollinearity_heatmap.png)

  

### 8.2. Perfis de Assinatura de Flags TCP

A decomposição média das flags TCP por classe demonstra clara segregação comportamental:

- **Infiltration - NMAP Portscan:** Dominado quase exclusivamente por flags `SYN` sem o correspondente `ACK`, caracterizando varreduras stealth (SYN Stealth Scans).

- **SSH-BruteForce:** Múltiplas trocas `PSH`/`ACK` repetidas com tamanhos de pacotes curtos, típicas de tentativas sequenciais de autenticação SSH.

- **DDoS-HOIC e DDoS-LOIC-HTTP:** Elevadíssima densidade de pacotes `ACK` e `PSH` associados a rajadas de requisições HTTP GET/POST para esgotamento de conexões de servidor Web.

- **BENIGN:** Apresenta o ciclo de vida completo com encerramento ordeiro de conexão (`FIN`/`ACK`).

  

![Perfil Médio de Flags TCP](/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/tcp_flags_profile.png)

  

---

  

## 9. Recomendações Técnicas para Pré-Processamento e Modelagem

  

1. **Descarte das Colunas Redundantes e Constantes:**

- Remover as colunas de zero variância: `Fwd URG Flags`, `Bwd URG Flags`, `URG Flag Count`.

- Remover colunas duplicadas: descartar `Average Packet Size` (já representada por `Packet Length Mean`).

2. **Tratamento de Valores Infinitos:**

- Tratar os 57 infinitos em `Flow Bytes/s` e `Flow Packets/s` substituindo-os pelo percentil 99,99 ou pelo valor máximo representável para evitar estouro em algoritmos baseados em gradiente ou distâncias euclidianas.

3. **Transformações de Escala:**

- Evitar normalização MinMax pura devido ao valor máximo extremo (outliers na escala de centenas de milhões encolheriam 99% dos dados para próximo de zero).

- Utilizar transformação logarítmica com deslocamento ($\log_{10}(x + 1)$) ou `RobustScaler` (baseado em mediana e IQR) para atributos de duração e taxas.

4. **Estratégia de Validação:**

- Realizar divisão Treino/Teste estratificada baseada na amostra gerada `CSECICIDS2018_improved_sample10.parquet`.

- Como todas as classes raras (SQL Injection, XSS, Dropbox Download) foram preservadas em 100%, utilizar validação cruzada estratificada (*StratifiedKFold*) com $k=5$, garantindo presença de todas as classes em todas as dobras.

  

---

  

## 10. Proveniência e Reprodutibilidade

  

- **Arquivo de Origem:** `/run/media/null/VM_s/DATASETS/CSECICIDS2018_improved.csv`

- **Arquivo de Amostra Gerado:** `/run/media/null/VM_s/DATASETS/CSECICIDS2018_improved_sample10.parquet`

- **Tamanho da Amostra Gerada:** 994,35 MiB (6.319.514 linhas $\times$ 82 colunas)

- **Seed Determinística:** `42`

- **Data de Execução:** 2026-09-25

- **Scripts Executados:** Persistidos em `/home/null/.gemini/antigravity-cli/brain/0a9eb289-2c30-4dd1-8d03-8101f2f00ce8/scratch/`