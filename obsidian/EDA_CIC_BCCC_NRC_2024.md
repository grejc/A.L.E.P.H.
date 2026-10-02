# Relatório Consolidado de Análise Exploratória de Dados (EDA)
## Dataset de Cibersegurança: CIC-BCCC-NRC-2024 vs. Amostra Representativa

---

### Sumário Executivo

Este documento compila a **Análise Exploratória de Dados (EDA)** detalhada e comparativa entre o dataset de tráfego de rede **`CIC-BCCC-NRC-2024.csv`** (11,48 GB, 22.860.449 fluxos) e a sua partição amostrada correspondente **`CIC-BCCC-NRC-2024_sampled.csv`** (1,32 GB, 3.264.221 fluxos), gerada pelo *Canadian Institute for Cybersecurity (CIC)* em conjunto com o *National Research Council (NRC)* em 2024.

O objetivo desta auditoria estatística é:
1. Validar a **integridade estrutural** dos dados brutos (valores nulos, infinitos e tipos de dados);
2. Documentar a remoção de **características identificadoras** (5-tuple de rede e metadados) para prevenir *shortcut learning* e vazamento de dados (*data leakage*);
3. Analisar a **estratégia de amostragem** aplicada e quantificar a fidelidade da amostra frente à população;
4. Identificar **anomalias severas de amostragem**, com destaque para a quase extinção da classe `DDoS TCP SYN Flood`;
5. Avaliar **divergências de distribuição** por meio dos testes estatísticos de **Kolmogorov-Smirnov (KS)** e **Distância de Wasserstein**;
6. Mapear a **multicolinearidade** entre as features e fornecer diretrizes técnicas para pré-processamento e treinamento de modelos preditivos.

---

## 1. Ficha Técnica dos Arquivos e Integridade dos Dados

| Parâmetro | Dataset Original (`CIC-BCCC-NRC-2024.csv`) | Amostra (`CIC-BCCC-NRC-2024_sampled.csv`) |
| :--- | :--- | :--- |
| **Tamanho em Disco** | 11.488.285.232 bytes (10,70 GiB) | 1.328.339.724 bytes (1,24 GiB) |
| **Total de Linhas (Fluxos)** | 22.860.449 (+1 cabeçalho) | 3.264.221 (+1 cabeçalho) |
| **Total de Colunas (Features)** | 85 colunas | 71 colunas |
| **Proporção Amostral** | 100,00% (População) | 14,28% |
| **Valores Nulos / Ausentes (NaN)** | **0 (0,00%)** | **0 (0,00%)** |
| **Valores Infinitos (+inf / -inf)**| **0 (0,00%)** | **0 (0,00%)** |
| **Colunas com Variância Zero** | 6 colunas constantes | 0 (removidas previamente) |
| **Status de Leitura** | UTF-8 retangular íntegro | UTF-8 retangular íntegro |

> **Nota de Integridade:** Diferente de edições anteriores de datasets do CIC (como o CIC-IDS2017, no qual divisões por zero geravam valores `Infinity` ou `NaN` nas colunas de taxa), o `CIC-BCCC-NRC-2024` foi devidamente tratado na origem, apresentando **ausência total de valores ausentes ou infinitos**.

---

## 2. Auditoria e Racional das Colunas Omitidas na Amostra (85 vs. 71)

A diferença de 14 colunas entre o dataset original (85) e a amostra (71) decorre de critérios metodológicos de engenharia de dados:

### 2.1 Identificadores Diretos (6 colunas)
- **Features:** `Flow ID`, `Src IP`, `Src Port`, `Dst IP`, `Dst Port`, `Timestamp`.
- **Justificativa:** Em tarefas de detecção de intrusão com Aprendizado de Máquina, modelos supervisionados tendem a associar o rótulo malicioso aos endereços IP das máquinas atacantes ou portas de serviço do laboratório. Isso cria modelos com acurácia de teste artificialmente próxima de 100%, mas totalmente ineficazes em ambientes operacionais reais (*data leakage*). Sua exclusão é obrigatória.

### 2.2 Colunas com Variância Zero / Constantes (6 colunas)
- `Protocol`: 100% dos 22.860.449 fluxos são do protocolo TCP (valor constante `6`).
- `Bwd PSH Flags`: 100% das instâncias possuem valor `0`.
- `Bwd URG Flags`: 100% das instâncias possuem valor `0`.
- `Fwd Bytes/Bulk Avg`: 100% das instâncias possuem valor `0`.
- `Fwd Packet/Bulk Avg`: 100% das instâncias possuem valor `0`.
- `Fwd Bulk Rate Avg`: 100% das instâncias possuem valor `0`.
- **Justificativa:** Features com variância zero transmitem zero entropia da informação e prejudicam modelos lineares com matrizes singulares.

### 2.3 Colunas Redundantes (2 colunas)
- `Fwd Header Length` e `Bwd Header Length`: Colunas fortemente colineares com o tamanho mínimo de segmento (`Fwd Seg Size Min`) e comprimento total de pacotes.

---

## 3. Análise da Estratégia de Amostragem

A análise matemática das taxas de amostragem por classe revelou um protocolo de amostragem estratificada com regras híbridas:

1. **Taxa Padrão (~14,89%):** Classes de alto volume (> 5.000 amostras) foram amostradas a uma taxa estrita de **14,887%** (razão próxima a 1/6,717).
2. **Preservação de Classes Minoritárias:** Classes com menos de 5.000 amostras no dataset original foram retidas em **95% a 100%**, impedindo o desaparecimento de ataques raros (ex: `Telnet Brute Force` reteve 99,42%, `MQTT DoS Publish Flood` reteve 100,00%).
3. **Anomalia Crítica de Amostragem (`DDoS TCP SYN Flood`):**
   - No original: **843.527 fluxos** (3,69% de todo o tráfego).
   - Na amostra: **apenas 605 fluxos** (0,018% da amostra).
   - Taxa de retenção: **0,0717%** (redução de 99,93%).
   - Outra anomalia: `Port Scanning` reteve apenas **1,30%** (9.987 no original $ightarrow$ 130 na amostra).

```
+-------------------------------------------------------------------------------+
|  RESUMO DO IMPACTO DA ANOMALIA DE SYN FLOOD                                  |
+------------------------------------+--------------------+---------------------+
| Métrica                            | Dataset Original   | Amostra Sampled     |
+------------------------------------+--------------------+---------------------+
| Volume DDoS TCP SYN Flood          | 843.527 fluxos     | 605 fluxos          |
| Média Flow Packets/s (Geral)       | 15.129,45 pkts/s   | 697,41 pkts/s       |
| Média Flow Bytes/s (Geral)         | 324.798,5 B/s      | 29.470,4 B/s        |
| Desvio Percentual de Taxa          | Referência (0%)    | -95,39% (Packets/s) |
+------------------------------------+--------------------+---------------------+
```

> **Diagnóstico:** Os fluxos de `DDoS TCP SYN Flood` possuem características extremas (duração média de apenas 34 microsegundos, com taxa média de 137.827 pacotes/s e 8,27 MB/s). A eliminação quase total desses fluxos na amostra fez com que a média global de taxa de pacotes despencasse mais de 95%.

---

## 4. Galeria de Visualizações Analíticas

### Figura 1: Distribuição das 25 Maiores Classes e Taxa Efetiva de Amostragem
![Figura 1](eda_analysis/figures/fig1_attack_distribution_comparison.png)
*O painel superior exibe as contagens em escala logarítmica. O painel inferior destaca a taxa padrão de ~14,89% e expõe a queda crítica para 0,07% no DDoS TCP SYN Flood (marcado em vermelho).*

---

### Figura 2: Equilíbrio Macro da Variável Alvo (`Label`)
![Figura 2](eda_analysis/figures/fig2_binary_label_balance.png)
*A proporção macro de classes permaneceu estável: 10,31% de tráfego Benigno no original contra 10,75% na amostra.*

---

### Figura 3: Desvios de Densidade (KDE) em Features Críticas
![Figura 3](eda_analysis/figures/fig3_feature_distribution_shift.png)
*Evidência do pico de fluxos ultrarrápidos presente em `Flow Duration` (em torno de log10 ≈ 1,2) e taxas elevadas em `Flow Packets/s` no original, os quais foram suprimidos na amostra.*

---

### Figura 4: Matriz de Correlação de Postos de Spearman (20 Features-Chave)
![Figura 4](eda_analysis/figures/fig4_correlation_matrix.png)
*Identificação visual de fortes multicolinearidades: correlações superiores a 0,95 entre Packet Length Mean, Flow Bytes/s e desvios de tamanho de pacote.*

---

### Figura 5: Ranking de Divergência de Kolmogorov-Smirnov (KS)
![Figura 5](eda_analysis/figures/fig5_sampling_fidelity_ks.png)
*Features temporais e de taxa apresentam alta divergência estatística (KS > 0,40, em vermelho), enquanto métricas de comprimento de pacote retêm alta fidelidade (KS < 0,06, em azul).*

---

### Figura 6: Perfis de Fluxo por Família de Ataque
![Figura 6](eda_analysis/figures/fig6_attack_characteristics.png)
*Assinaturas de tráfego: ataques Web/Injeção apresentam pacotes volumosos (payloads de script/SQL), enquanto DoS/DDoS e Reconhecimento concentram-se em pacotes pequenos e tempos extremos.*

---

## 5. Tabela Comparativa de Todas as 49 Classes

A tabela a seguir documenta exaustivamente todas as 49 classes do dataset:

| # | Nome do Ataque / Classe | Contagem Original | Contagem Amostra | % Original | % Amostra | Taxa de Amostragem (%) | Diferença de Share (%) |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `DDoS RSTFIN Flood` | 3,938,280 | 586,310 | 17.2275% | 17.9617% | 14.89% | +0.7342% |
| 2 | `ACK Flood` | 2,905,508 | 432,556 | 12.7098% | 13.2514% | 14.89% | +0.5417% |
| 3 | `DDoS PSHACK Flood` | 2,547,096 | 379,198 | 11.1419% | 11.6168% | 14.89% | +0.4749% |
| 4 | `Benign Traffic` | 2,357,186 | 350,925 | 10.3112% | 10.7507% | 14.89% | +0.4395% |
| 5 | `DoS TCP Flood` | 2,246,556 | 334,454 | 9.8273% | 10.2461% | 14.89% | +0.4188% |
| 6 | `SYN Flood` | 1,803,982 | 268,565 | 7.8913% | 8.2275% | 14.89% | +0.3363% |
| 7 | `Sparta SSH Brute Force` | 1,122,758 | 167,148 | 4.9114% | 5.1206% | 14.89% | +0.2093% |
| 8 | `MQTT Brute Force` | 1,015,917 | 151,242 | 4.4440% | 4.6333% | 14.89% | +0.1893% |
| 9 | `Recon Port Scan` | 954,954 | 128,973 | 4.1773% | 3.9511% | 13.51% | -0.2262% |
| 10 | `DDoS TCP SYN Flood` | 843,527 | 605 | 3.6899% | 0.0185% | 0.07% | -3.6714% |
| 11 | `XSS` | 707,858 | 105,381 | 3.0964% | 3.2284% | 14.89% | +0.1319% |
| 12 | `Backdoor` | 557,184 | 60,632 | 2.4373% | 1.8575% | 10.88% | -0.5799% |
| 13 | `MQTT DDoS Publish Flood` | 413,913 | 61,620 | 1.8106% | 1.8877% | 14.89% | +0.0771% |
| 14 | `DDoS ACK Fragmentation` | 405,824 | 60,416 | 1.7752% | 1.8509% | 14.89% | +0.0756% |
| 15 | `MQTT DoS Connect Flood` | 238,031 | 35,436 | 1.0412% | 1.0856% | 14.89% | +0.0444% |
| 16 | `Password Attack` | 179,170 | 26,673 | 0.7838% | 0.8171% | 14.89% | +0.0334% |
| 17 | `Recon OS Scan` | 127,490 | 18,979 | 0.5577% | 0.5814% | 14.89% | +0.0237% |
| 18 | `MITM` | 110,112 | 16,392 | 0.4817% | 0.5022% | 14.89% | +0.0205% |
| 19 | `DoS SYN Flood` | 73,222 | 10,900 | 0.3203% | 0.3339% | 14.89% | +0.0136% |
| 20 | `Recon Vulnerability Scan` | 47,810 | 7,117 | 0.2091% | 0.2180% | 14.89% | +0.0089% |
| 21 | `Recon Ping Sweep` | 47,194 | 7,025 | 0.2064% | 0.2152% | 14.89% | +0.0088% |
| 22 | `Scan Aggressive` | 25,704 | 3,826 | 0.1124% | 0.1172% | 14.88% | +0.0048% |
| 23 | `Dictionary Brute Force` | 18,151 | 2,702 | 0.0794% | 0.0828% | 14.89% | +0.0034% |
| 24 | `MITM ARP Spoofing` | 17,294 | 2,574 | 0.0757% | 0.0789% | 14.88% | +0.0032% |
| 25 | `Ransomware` | 16,676 | 2,482 | 0.0729% | 0.0760% | 14.88% | +0.0031% |
| 26 | `Scan UDP Attack` | 16,301 | 2,426 | 0.0713% | 0.0743% | 14.88% | +0.0030% |
| 27 | `Mirai ACK Flood` | 16,186 | 2,409 | 0.0708% | 0.0738% | 14.88% | +0.0030% |
| 28 | `DDoS HTTP Flood` | 15,795 | 2,351 | 0.0691% | 0.0720% | 14.88% | +0.0029% |
| 29 | `Port Scanning` | 9,987 | 130 | 0.0437% | 0.0040% | 1.30% | -0.0397% |
| 30 | `Scan Port OS` | 9,839 | 1,464 | 0.0430% | 0.0448% | 14.88% | +0.0018% |
| 31 | `DDoS ICMP Fragmentation` | 9,775 | 1,455 | 0.0428% | 0.0446% | 14.88% | +0.0018% |
| 32 | `Uploading Attack` | 9,516 | 1,416 | 0.0416% | 0.0434% | 14.88% | +0.0018% |
| 33 | `SQL Injection` | 8,755 | 1,303 | 0.0383% | 0.0399% | 14.88% | +0.0016% |
| 34 | `Scan Host Port` | 7,212 | 1,073 | 0.0315% | 0.0329% | 14.88% | +0.0013% |
| 35 | `Vulnerability Scanner` | 5,424 | 807 | 0.0237% | 0.0247% | 14.88% | +0.0010% |
| 36 | `DoS UDP Flood` | 4,963 | 4,847 | 0.0217% | 0.1485% | 97.66% | +0.1268% |
| 37 | `Mirai HTTP Flood` | 3,908 | 2,105 | 0.0171% | 0.0645% | 53.86% | +0.0474% |
| 38 | `Mirai Host Brute Force` | 3,725 | 3,648 | 0.0163% | 0.1118% | 97.93% | +0.0955% |
| 39 | `DoS ICMP Flood` | 3,512 | 3,463 | 0.0154% | 0.1061% | 98.60% | +0.0907% |
| 40 | `DDoS UDP Flood` | 2,576 | 2,521 | 0.0113% | 0.0772% | 97.86% | +0.0660% |
| 41 | `DDoS ICMP Flood` | 2,552 | 2,514 | 0.0112% | 0.0770% | 98.51% | +0.0659% |
| 42 | `MQTT Malformed` | 2,246 | 2,157 | 0.0098% | 0.0661% | 96.04% | +0.0563% |
| 43 | `DoS DNS Flood` | 1,702 | 1,696 | 0.0074% | 0.0520% | 99.65% | +0.0445% |
| 44 | `Mirai UDP Plain` | 1,630 | 1,557 | 0.0071% | 0.0477% | 95.52% | +0.0406% |
| 45 | `Mirai UDP Flood` | 1,242 | 620 | 0.0054% | 0.0190% | 49.92% | +0.0136% |
| 46 | `MQTT DoS Publish Flood` | 953 | 953 | 0.0042% | 0.0292% | 100.00% | +0.0250% |
| 47 | `Telnet Brute Force` | 694 | 690 | 0.0030% | 0.0211% | 99.42% | +0.0181% |
| 48 | `Recon Host Discovery` | 424 | 422 | 0.0019% | 0.0129% | 99.53% | +0.0111% |
| 49 | `OS Fingerprinting` | 135 | 63 | 0.0006% | 0.0019% | 46.67% | +0.0013% |

---

## 6. Tabela Comparativa de Distribuição das Features (Estatística Descritiva e Testes de Hipótese)

Métricas calculadas sobre 1.000.000 de instâncias de cada partição com semente aleatória reproduzível (`seed=42`):

| Feature | Média Original | Média Amostra | Desvio Rel. (%) | Mediana Original | Mediana Amostra | KS Stat | Dist. Wasserstein |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Flow Duration` | 2.90e+07 | 3.40e+07 | +17.49% | 4.79e+06 | 1.34e+07 | 0.7029 | 3.14e+07 |
| `Total Fwd Packet` | 5.29e+00 | 7.70e+00 | +45.61% | 2.00e+00 | 3.00e+00 | 0.4777 | 4.69e+00 |
| `Total Bwd packets` | 2.02e+00 | 4.45e+00 | +120.31% | 1.00e+00 | 1.00e+00 | 0.4057 | 2.32e+00 |
| `Total Length of Fwd Packet` | 5.57e+02 | 1.61e+03 | +188.98% | 0.00e+00 | 0.00e+00 | 0.0534 | 4.72e+03 |
| `Total Length of Bwd Packet` | 1.21e+03 | 3.98e+03 | +228.78% | 0.00e+00 | 0.00e+00 | 0.0397 | 1.41e+04 |
| `Fwd Packet Length Mean` | 2.42e+01 | 3.74e+01 | +54.57% | 0.00e+00 | 0.00e+00 | 0.0488 | 2.42e+01 |
| `Bwd Packet Length Mean` | 3.50e+01 | 3.47e+01 | -0.74% | 0.00e+00 | 0.00e+00 | 0.0476 | 1.34e+01 |
| `Flow Bytes/s` | 3.25e+05 | 2.95e+04 | -90.93% | 0.00e+00 | 0.00e+00 | 0.0995 | 3.59e+04 |
| `Flow Packets/s` | 1.51e+04 | 6.97e+02 | -95.39% | 1.03e+00 | 3.12e-01 | 0.6950 | 3.09e+04 |
| `Flow IAT Mean` | 7.77e+06 | 9.08e+06 | +16.79% | 1.37e+06 | 3.50e+06 | 0.6928 | 8.73e+06 |
| `Flow IAT Max` | 1.34e+07 | 1.63e+07 | +21.58% | 3.29e+06 | 7.34e+06 | 0.7009 | 1.51e+07 |
| `Packet Length Mean` | 2.94e+01 | 4.20e+01 | +42.88% | 0.00e+00 | 0.00e+00 | 0.0552 | 2.34e+01 |
| `Packet Length Std` | 4.04e+01 | 4.74e+01 | +17.51% | 0.00e+00 | 0.00e+00 | 0.0597 | 2.66e+01 |
| `Average Packet Size` | 3.78e+01 | 5.23e+01 | +38.34% | 0.00e+00 | 0.00e+00 | 0.0481 | 3.04e+01 |
| `SYN Flag Count` | 6.25e-01 | 8.57e-01 | +37.05% | 0.00e+00 | 0.00e+00 | 0.2929 | 4.51e-01 |
| `ACK Flag Count` | 4.23e+00 | 8.87e+00 | +109.79% | 1.00e+00 | 2.00e+00 | 0.2909 | 4.51e+00 |
| `FIN Flag Count` | 6.41e-01 | 7.68e-01 | +19.87% | 0.00e+00 | 0.00e+00 | 0.2382 | 4.67e-01 |
| `RST Flag Count` | 8.20e-01 | 7.10e-01 | -13.41% | 1.00e+00 | 1.00e+00 | 0.2143 | 4.07e-01 |
| `FWD Init Win Bytes` | 5.18e+03 | 8.59e+03 | +65.76% | 5.12e+02 | 5.12e+02 | 0.5662 | 4.85e+03 |
| `Bwd Init Win Bytes` | 5.08e+02 | 8.96e+02 | +76.22% | 0.00e+00 | 0.00e+00 | 0.1216 | 3.06e+02 |
| `Down/Up Ratio` | 4.49e-01 | 3.74e-01 | -16.70% | 0.00e+00 | 0.00e+00 | 0.4733 | 5.15e-01 |
| `Active Mean` | 8.86e+05 | 1.09e+06 | +23.57% | 0.00e+00 | 0.00e+00 | 0.1151 | 1.03e+06 |
| `Idle Mean` | 1.16e+07 | 1.40e+07 | +20.64% | 0.00e+00 | 6.83e+06 | 0.4863 | 1.31e+07 |

---

## 7. Recomendações Metodológicas para Modelagem e Machine Learning

1. **Remoção Mandatória de Identificadores:**
   - Descartar impreterivelmente `Flow ID`, `Src IP`, `Src Port`, `Dst IP`, `Dst Port`, `Protocol` e `Timestamp`.
2. **Mitigação da Anomalia de `DDoS TCP SYN Flood`:**
   - Modelos treinados estritamente na amostra sofrerão de cegueira a ataques de SYN flood. Recomenda-se extrair uma cota adicional (ex: 50.000 a 100.000 fluxos) da classe `DDoS TCP SYN Flood` do dataset original e inseri-los na base de treino.
3. **Tratamento de Multicolinearidade:**
   - `Average Packet Size`, `Fwd Segment Size Avg` e `Packet Length Mean` contêm informações quase idênticas. Aplicar seleção de atributos ou PCA antes de treinar classificadores lineares ou redes neurais.
4. **Normalização e Escalação de Features Heavy-Tailed:**
   - Devido à assimetria extrema das taxas e durações, utilizar $\log_{1p}(x)$ ou `RobustScaler` (baseado em mediana e IQR) para que gradientes não sejam dominados por outliers.

---

## 8. Reprodutibilidade e Proveniência

- **Data da Execução:** 2026-09-30
- **Sistema Operacional:** Linux (Kernel 6.x, x86_64)
- **Python Runtime:** Python 3.11.9 (`~/.venv`)
- **Scripts Geradores:**
  - `eda_analysis/compare_classes.py`: Auditoria de classes e amostragem
  - `eda_analysis/check_orig_integrity.py`: Auditoria de nulos e infinitos em streaming
  - `eda_analysis/compare_distributions.py`: Testes estatísticos de KS e Wasserstein
  - `eda_analysis/generate_figures.py`: Geração das 6 figuras analíticas
- **Localização dos Arquivos no Projeto:**
  - Relatório: `eda_analysis/RELATORIO_EDA_CIC_BCCC_NRC_2024.md`
  - Figuras: `eda_analysis/figures/`
