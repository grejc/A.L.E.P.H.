# Arquitetura e Engenharia do Pipeline de Pré-Processamento Multi-Dataset

## Visão Geral Unificada, Módulos Compartilhados e Integração com o Modelo ALF-MoE

---

### Sumário Executivo

A integridade empírica, a robustez e a generalização de Sistemas de Detecção de Intrusão em Redes baseados em Aprendizado Profundo (*Deep Learning-based NIDS*) dependem ontologicamente da pureza estatística e da adequação matemática dos dados de telemetria ingeridos. No projeto **ALF-MoE** (*Attention-based Learnable Fusion of Specialized Expert Networks*), o subsistema de pré-processamento desempenha o papel crítico de converter fluxos de rede brutos heterogêneos em tensores numéricos padronizados, prevenindo o fenômeno destrutivo de **GIGO** (*Garbage In, Garbage Out*), eliminando riscos de **vazamento de dados** (*data leakage*) e impedindo o aprendizado mnemônico de atalhos de rede (*shortcut learning*).

Este documento sintetiza a arquitetura unificada do pipeline implementada no módulo Python [`src/preprocessing.py`](file:///home/null/ALF-MoE/src/preprocessing.py) em conjunto com a ontologia de domínios em [`src/domain_features.py`](file:///home/null/ALF-MoE/src/domain_features.py), o arquivo de configuração central [`src/config.py`](file:///home/null/ALF-MoE/src/config.py) e o subsistema de inferência em tempo real em [`src/inference.py`](file:///home/null/ALF-MoE/src/inference.py).

---

## 1. Matriz Comparativa dos Datasets Suportados

O pipeline do ALF-MoE suporta de forma nativa e unificada **quatro grandes benchmarks de tráfego de rede**, harmonizando seus atributos no vetor canônico de características estatísticas:

| Parâmetro / Dimensão | CSE-CIC-IDS2018 (Original) | CSE-CIC-IDS2018 (Corrigido / Improved) | CIC-UNSW-NB15 | CIC-BCCC-NRC-2024 (TabularIoTAttack) |
| :--- | :--- | :--- | :--- | :--- |
| **Origem e Autoria** | CIC & CSE (AWS, 2018) | Auditoria Liu et al. (IEEE CNS 2022) | ACCS / UNSW Canberra (2015) | CIC, BCCC & NRC (2024) |
| **Ambiente de Captura** | Nuvem AWS (Corporativo) | Nuvem AWS (Auditoria SOTA) | Hardware IXIA PerfectStorm | Laboratórios Físicos e Híbridos IoT/IoMT |
| **Volumetria Bruta** | 16,2M fluxos (~6,34 GB CSV) | 63,2M fluxos (~36,0 GB CSV / 1,04 GB Parquet) | 3,54M fluxos (~1,91 GB CSV) | 22,86M fluxos (~11,48 GB CSV) |
| **Volumetria Amostrada** | 3.712.942 fluxos (1,45 GB CSV) | Amostra estratificada controlada | 139.583 fluxos (79,3 MB CSV) $\to$ 125.378 deduplicados | 3.264.221 fluxos (1,32 GB CSV) |
| **Colunas Brutas** | 80 colunas (CICFlowMeter-V3) | 91 colunas brutas | 84 colunas | 85 colunas brutas |
| **Espaço Canônico Base** | 76 colunas canônicas | 76 colunas canônicas | 76 colunas canônicas | 76 colunas canônicas |
| **Colunas Purgadas (Variância Zero)** | **10 colunas** (3 URG + 7 bulk/PSH) | **3 colunas** (3 URG flags) | **9 colunas** (3 URG + 6 bulk/flags) | **3 colunas** (3 URG flags) |
| **Features Ativas Finais ($D$)** | **66 features** | **73 features** | **67 features** | **73 features** |
| **Classes Granulares (TL0)** | 15 classes | 15 classes ativas (25 originais) | 10 classes canônicas | 49 classes granulares |
| **Meta-Categorias (TL1)** | 7 classes consolidadas | 9 classes consolidadas | 10 classes (mapeamento 1:1) | 9 classes consolidadas |
| **Partição de Teste (20%)** | 742.589 instâncias | 1.263.903 instâncias | 27.917 instâncias (139k pool) / 25.076 (125k dedup) | 652.845 instâncias |
| **Proporção Benign (Teste)** | 36,32% | 89,27% | 35,82% | 10,75% |
| **Fatiamento MoE (DNN, CNN, GRU, CAE, LSTM)** | 27, 20 (16), 32, 27, 18 | 27, 20 (16), 32, 27, 18 | **25**, 20 (16), 32, 27, 18 | 27, 20 (16), 32, 27, 18 |

---

## 2. Mapa dos Módulos Utilizados em Cada Etapa

O ciclo de vida de dados do ALF-MoE é dividido em dois grandes fluxos operacionais complementares:
1. **Pipeline de Treinamento em Lote (*Offline Training Pipeline*):** Ingestão, higienização, balanceamento, divisão estratificada anti-leakage e persistência atômica de artefatos.
2. **Pipeline de Inferência em Tempo Real (*Online Serving Pipeline*):** Ingestão de pacotes e fluxos em tempo real via NFStream/PCAP, alinhamento determinístico de colunas, sanitização, log1p vetorizado, escalonamento e roteamento pelo comitê MoE.

### Fluxograma Integrado: Do Dado Bruto à Inferência

```
[DADOS BRUTOS: CSV / Parquet]                           [TRÁFEGO EM TEMPO REAL: NFStream / PCAP]
             │                                                              │
             ▼                                                              ▼
 1. Ingestão em Streaming ────────► [pyarrow / pandas]          1'. Extração de Fluxos ──► [NFStream / Scapy]
             │                                                              │
             ▼                                                              ▼
 2. Alinhamento de Schema ────────► [src.domain_features.CICDomainFeatures.match_columns]
             │                                                              │
             ▼                                                              ▼
 3. Expurgamento Anti-Leakage ────► [Preprocessor._align_dataframe_columns: descarta 5-tuple, IDs, Timestamp]
             │                                                              │
             ▼                                                              ▼
 4. Purga de Variância Zero ──────► [Preprocessor._clean_raw_dataset: EXPLICIT_DROP + nunique <= 1]
             │                                                              │
             ▼                                                              │
 5. Imputação por Mediana ────────► [pandas.Series.fillna(mediana_condicional_classe)]
             │                                                              │
             ▼                                                              │
 6. Mapeamento de Ameaças ────────► [Preprocessor.threat_classification: TL0 / TL1]
             │                                                              │
             ▼                                                              │
 7. Deduplicação Opcional ────────► [pandas.DataFrame.drop_duplicates(subset=canonical_features)]
             │                                                              │
             ▼                                                              │
 8. Particionamento Estratificado ─► [sklearn.model_selection.train_test_split (80/20 Dev/Test)]
             │                                                              │
             ▼                                                              │
 9. Ajuste Estrito no Treino ─────► [Preprocessor.fit() exclusively on Train]      │
    ├─ Skewness: |skew| > 3.0 ────► [scipy.stats.skew, pandas.Series.skew]         │
    ├─ Log1p: ln(1 + max(x, 0)) ──► [numpy.log1p]                                  │
    ├─ RobustScaler (IQR 25-75) ──► [sklearn.preprocessing.RobustScaler]            │
    ├─ LabelEncoder ──────────────► [sklearn.preprocessing.LabelEncoder]            │
    └─ Class Weights: sqrt(N/C*Nc)─► [Preprocessor.compute_class_weights]           │
             │                                                              │
             ├──────────────────────────────────────────────────────────────┘
             ▼                                                              │
10. Transformação Consistente ────► [Preprocessor.transform() / transform_features()]
             │                                                              │
             ▼                                                              ▼
11. Fatiamento MoE (SliceLayer) ──► [Preprocessor.get_domain_indices()]
    ├── slice_dnn  ──►  Especialista DNN   (Shape: 27 ou 25)
    ├── slice_cnn  ──►  Especialista CNN   (Shape: 20 -> 16 canônicos -> 4x4x1)
    ├── slice_gru  ──►  Especialista GRU   (Shape: 32 -> 8x4)
    ├── slice_cae  ──►  Especialista CAE   (Shape: 27 -> Hann + RFFT)
    └── slice_lstm ──►  Especialista LSTM  (Shape: 18 -> 6x3)
             │                                                              │
             ▼                                                              ▼
12. Serialização e Carga Atômica ─► [pickle.dump (.pkl) / json.dump (.json) em artifacts/]
```

### Detalhamento dos Módulos e Funções por Etapa

| Etapa | Módulo / Biblioteca | Classe / Função | Parâmetros Chave | Papel Funcional |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestão Tabular** | `pandas` | `pd.read_csv()` | `low_memory=False` | Leitura padrão de CSVs de médio porte |
| **Ingestão Otimizada** | `pyarrow.parquet` | `pd.read_parquet()` | `engine="pyarrow"` | Leitura vetorizada de altíssima velocidade para Parquet |
| **Ingestão em Streaming** | `pyarrow.csv` | `csv.read_csv()` | `block_size=67108864` (64 MiB) | Streaming por blocos sem saturação de RAM em arquivos de 34+ GiB |
| **Alinhamento de Schema** | `src.domain_features` | `CICDomainFeatures.match_columns()` | `alias_candidates` (dicionário) | Tradução case-insensitive, remoção de espaços e resolução de sinônimos |
| **Tradução NFStream** | `src.domain_features` | `CICDomainFeatures.nfstream_to_cic_map()` | `with_udps_prefix=True` | Mapeamento biunívoco de plugins UDPS do NFStream para features canônicas |
| **Higienização Anti-Leakage** | `src.preprocessing` | `Preprocessor._align_dataframe_columns()` | Drop de 5-tuple e Timestamp | Eliminação de atalhos de rede (IPs, portas, IDs) para prevenir shortcut learning |
| **Purga de Variância Nula** | `src.preprocessing` | `Preprocessor._clean_raw_dataset()` | `EXPLICIT_DROP_COLUMNS` + `nunique <= 1` | Purga das flags URG constantes e de colunas adicionais sem variância |
| **Imputação Numérica** | `numpy` & `pandas` | `replace([np.inf, -np.inf], np.nan)` | `.groupby(target)[col].median()` | Substituição de indefinições de divisão por zero pela mediana condicional |
| **Análise de Assimetria** | `scipy.stats` / `pandas` | `df[col].skew()` | `skew_threshold = 3.0` | Detecção de variáveis com caudas longas para estabilização de gradientes |
| **Transformação Log** | `numpy` | `np.log1p(np.maximum(x, 0.0))` | Não-negatividade forçada | Compressão monotônica da amplitude dinâmica de contadores e taxas |
| **Escalonamento Robusto** | `sklearn.preprocessing` | `RobustScaler()` | `quantile_range=(25.0, 75.0)` | Padronização baseada em mediana e IQR ($Q_{75} - Q_{25}$), imune a outliers |
| **Codificação Alvo** | `sklearn.preprocessing` | `LabelEncoder()` | `.fit_transform()` | Mapeamento bijetivo de rótulos categóricos em inteiros $0 \dots C-1$ |
| **Balanceamento Focal** | `src.preprocessing` | `compute_class_weights()` | `strategy="sqrt"` | Ponderação atenuada $w_c = \sqrt{N / (C \cdot N_c)}$ para a Focal Loss |
| **Particionamento** | `sklearn.model_selection` | `train_test_split()` | `stratify=y`, `random_state=42` | Divisão estratificada sem vazamento estatístico ou temporal |
| **Fatiamento MoE** | `src.preprocessing` | `Preprocessor.get_domain_indices()` | Índices das 5 famílias funcionais | Mapeamento dinâmico de colunas ativas para o `SliceLayer` |
| **Inferência em Tempo Real** | `src.preprocessing` | `Preprocessor.transform_features()` | `raw_data: Union[dict, Series, DataFrame]` | Pipeline de pré-processamento de baixa latência ($< 0{,}02\,\mathrm{ms}$) para produção |
| **Persistência Atômica** | `pickle` & `json` | `Preprocessor.save_artifacts()` | Atomic swap via arquivo `.tmp` | Persistência transacional e segura de transformadores (.pkl) e manifestos (.json) |

---

## 3. Os 5 Especialistas Neurais e o Fatiamento de Domínios (`SliceLayer`)

A inovação estrutural central do ALF-MoE reside na decomposição do vetor tabular em **5 domínios ortogonais da telemetria de rede**. O método [`Preprocessor.get_domain_indices()`](file:///home/null/ALF-MoE/src/preprocessing.py#L647-L660) mapeia dinamicamente os índices das features ativas para a camada funcional [`SliceLayer`](file:///home/null/ALF-MoE/src/neural/extra_layers.py) do Keras:

```
Vetor Canônico x ∈ ℝ^D (D = 73, 67 ou 66)
  ├── x_g ∈ ℝ^(27 ou 25) ──►  Especialista DNN   (Métricas Globais, Sinalizadores TCP, Contadores)
  ├── x_s ∈ ℝ^20 (16 can) ──►  Especialista CNN   (Geometria Espacial de Pacotes: Matriz 4x4x1)
  ├── x_v ∈ ℝ^32         ──►  Especialista GRU   (Dinâmica Sequencial de Tempos: Tensores 8x4)
  ├── x_f ∈ ℝ^27         ──►  Especialista CAE   (Rajadas e Frequência: Hann-Window + RFFT -> Autoencoder)
  └── x_t ∈ ℝ^18         ──►  Especialista LSTM  (Intervalos Longos de Active/Idle: Tensores 6x3)
```

### Detalhamento Arquitetural de Cada Especialista:

1. **Domínio Estatístico Global ($\mathbf{x}_g \in \mathbb{R}^{27}$ ou $\mathbb{R}^{25} \to \text{Especialista DNN}$):**
   - **Composição:** Duração do fluxo, contadores agregados de pacotes/bytes de ida e volta, taxas médias de tráfego, sinalizadores de controle TCP (SYN, ACK, FIN, RST, PSH, CWR, ECE), tamanhos médios de pacotes, contadores de subfluxo e tamanhos de janela TCP inicial (`Init Win bytes`).
   - **Dimensão:** 27 atributos em CSE-CIC-IDS2018 (Original), CSE-CIC-IDS2018 (Corrigido) e CIC-BCCC-NRC-2024. No dataset CIC-UNSW-NB15, as flags `CWR Flag Count` e `ECE Flag Count` têm variância nula e são purgadas, resultando em **25 atributos**.
   - **Camadas Neurais:** Perceptron multicamadas com camadas densas (256 e 128 unidades), ativações LeakyReLU(0.2), Dropout(0.1) e projeção para $C$ classes.

2. **Domínio Espacial de Pacotes ($\mathbf{x}_s \in \mathbb{R}^{20} \to 16 \text{ canônicos} \to 4 \times 4 \times 1 \to \text{Especialista CNN}$):**
   - **Composição:** O `SliceLayer` extrai 20 atributos referentes a dimensões de pacote (mínimo, máximo, média, desvio padrão e variância em forward e backward, tamanhos médios de segmento, comprimentos de cabeçalho, taxa direcional de pacotes e ratio down/up).
   - **Mecanismo de Projeção Canônica:** No módulo [`src/neural/cnn.py`](file:///home/null/ALF-MoE/src/neural/cnn.py#L49-L60), para preservar rigorosamente a correlação espacial 2D em grade quadrada sem distorção de escala, selecionam-se os primeiros 16 índices canônicos de comprimento de pacote (`SliceLayer(list(range(16)))`), descartando deliberadamente o atributo `Flow Packets/s` (escala temporal divergente) e reorganizando o tensor em uma matriz bidimensional **$4 \times 4 \times 1$**.
   - **Camadas Neurais:** Convoluções 2D (filtros 64 e 128 com kernel $2 \times 2$), Batch Normalization, LeakyReLU(0.2), Dropout(0.2) e densa de 128 unidades.

3. **Domínio Temporal de Curto Prazo e Velocidade ($\mathbf{x}_v \in \mathbb{R}^{32} \to 8 \times 4 \to \text{Especialista GRU}$):**
   - **Composição:** 32 métricas de tempo entre chegadas (*Inter-Arrival Time* -- IAT): médias, desvios padrões, mínimos e máximos para tráfego bidirecional, fluxo de avanço (*forward*) e fluxo de retrocesso (*backward*), além de taxas instantâneas e tempos parciais.
   - **Estruturação:** Reformatadas matricialmente em **8 timesteps com 4 descritores cada**.
   - **Camadas Neurais:** Célula GRU bidirecional com 64 unidades, Dropout(0.1) e projeção densa de 128 unidades.

4. **Domínio Frequencial e Tráfego em Rajada ($\mathbf{x}_f \in \mathbb{R}^{27} \to \text{Especialista CAE}$):**
   - **Composição:** 27 atributos modelando dinâmicas contínuas, variâncias de pacote, durações e taxas de rajada (*bulk transmission*).
   - **Processamento Espectral:** Submetidos à camada customizada `HannFFTLayer`, que aplica uma janela de Hann:
     $$w(n) = 0{,}5 - 0{,}5 \cos\left(\frac{2\pi n}{L-1}\right)$$
     e calcula a magnitude espectral عبر Transformada Rápida de Fourier Real ($\operatorname{RFFT}$).
   - **Camadas Neurais:** Autoencoder Convolucional 1D com filtros (16, 32, 64) e regularização de reconstrução ($\lambda_{\mathrm{rec}} = 1{,}0, \lambda_{\mathrm{reg}} = 10^{-4}$).

5. **Domínio de Estado de Longo Prazo ($\mathbf{x}_t \in \mathbb{R}^{18} \to 6 \times 3 \to \text{Especialista LSTM}$):**
   - **Composição:** 18 métricas de repouso e atividade: *Idle Min/Max/Mean/Std* e *Active Min/Max/Mean/Std*, complementadas por durações e taxas de pacotes.
   - **Estruturação:** Reformatadas em **6 timesteps com 3 descritores de persistência**.
   - **Camadas Neurais:** Célula LSTM com 64 unidades, Dropout(0.1) e projeção densa de 128 unidades.

---

## 4. Garantia Matemática Anti-Leakage e Protocolo de Ajuste (`fit` vs. `transform`)

O pipeline impõe um isolamento formal entre as partições de dados:

$$\mathcal{D}_{\mathrm{treino}} \cap \mathcal{D}_{\mathrm{val}} = \emptyset, \quad (\mathcal{D}_{\mathrm{treino}} \cup \mathcal{D}_{\mathrm{val}}) \cap \mathcal{D}_{\mathrm{teste}} = \emptyset$$

1. **Imputação de Mediana Congelada:** O vetor de medianas $\mathbf{m} = [m_1, m_2, \dots, m_D]^T$ é calculado exclusivamente sobre $\mathcal{D}_{\mathrm{treino}}$. Durante o `transform` (ou `transform_features` em produção), qualquer valor ausente é preenchido deterministicamente com esse vetor.
2. **Seleção de Assimetria no Treino:** As variáveis submetidas à compressão logarítmica são selecionadas se e somente se sua assimetria amostral em $\mathcal{D}_{\mathrm{treino}}$ ultrapassar o limiar:
   $$\gamma_1(j) = \frac{\frac{1}{N_{\mathrm{treino}}} \sum_{i=1}^{N_{\mathrm{treino}}} (x_{ij} - \bar{x}_j)^3}{\left(\frac{1}{N_{\mathrm{treino}}} \sum_{i=1}^{N_{\mathrm{treino}}} (x_{ij} - \bar{x}_j)^2\right)^{3/2}}, \quad |\gamma_1(j)| > 3{,}0$$
   A transformação aplica $x_{ij}' = \ln(1 + \max(x_{ij}, 0))$.
3. **Escalonamento Robusto Imune a Outliers:** Os quantis $Q_{50}$ (mediana), $Q_{25}$ e $Q_{75}$ do `RobustScaler` são congelados a partir de $\mathcal{D}_{\mathrm{treino}}$:
   $$\tilde{x}_{ij} = \frac{x_{ij}' - Q_{50}(x_{\cdot j}^{\mathrm{treino}})}{Q_{75}(x_{\cdot j}^{\mathrm{treino}}) - Q_{25}(x_{\cdot j}^{\mathrm{treino}})}$$
4. **Resiliência a Rótulos Desconhecidos na Inferência:** Se uma classe desconhecida surgir durante a inferência online, o preprocessor executa um fallback determinístico para a classe benigna padrão (`BENIGN`), assegurando operação ininterrupta do NIDS.

---

## 5. Estrutura dos Relatórios Técnicos por Agente Especializado

Para detalhar as particularidades de engenharia, amostragem, anomalias e distribuições de cada um dos quatro datasets, a documentação é dividida em relatórios autônomos gerados pelos respectivos agentes:

- [[01_Agente_CSE_CIC_IDS2018_Original|Agente 1: CSE-CIC-IDS2018 Canônico / Original AWS]] — Documentação da base corporativa original AWS (16,2M fluxos $\to$ 3.712.942 amostrados), alinhamento sintático com o extrator CICFlowMeter-V3, purga de 10 colunas sem variância (66 features ativas), 15 classes TL0 e 7 meta-categorias TL1.
- [[02_Agente_CSE_CIC_IDS2018_Corrigido|Agente 2: CSE-CIC-IDS2018 Corrigido / Improved]] — Documentação da versão melhorada (63,2M fluxos, 34 GiB), incorporando a auditoria de Liu et al. (IEEE CNS 2022), ingestão com streaming PyArrow, correção de porta fechada em FTP, reclassificação de fluxos "Attempted", 73 features ativas e 9 meta-categorias TL1.
- [[03_Agente_CIC_UNSW_NB15|Agente 3: CIC-UNSW-NB15 (IXIA PerfectStorm)]] — Documentação da base IXIA de alta densidade, prevenção de shortcut learning por IP, protocolo de amostragem com máxima entropia comportamental, purga de 9 colunas sem variância (67 features ativas, DNN com 25 atributos) e 10 classes canônicas.
- [[04_Agente_CIC_BCCC_NRC_2024|Agente 4: CIC-BCCC-NRC-2024 (TabularIoTAttack-2024)]] — Documentação do benchmark IoT contemporâneo com 9 sub-datasets (22,8M fluxos), amostragem estratificada Hare-Niemeyer, auditoria da anomalia na retenção de SYN Flood, 73 features ativas e agrupamento de 49 classes granulares (TL0) em 9 macro-famílias (TL1).
