# Relatório Técnico de Pré-Processamento — Agente 1

## Dataset: CSE-CIC-IDS2018 (Versão Canônica / Original AWS)

---

### Sumário Executivo

O conjunto de dados **CSE-CIC-IDS2018** (*Communications Security Establishment \& Canadian Institute for Cybersecurity*) representa um dos mais difundidos marcos de referência (*benchmarks*) na literatura de segurança cibernética para avaliação de sistemas de detecção de intrusão em ambientes de computação em nuvem corporativa. 

Este relatório documenta a íntegra do pipeline de pré-processamento executado pelo **Agente 1** sobre a versão canônica original do dataset, cobrindo desde a ingestão da telemetria bruta e o protocolo de amostragem representativa até a higienização de atributos, alinhamento sintático de cabeçalhos, purga de **10 variáveis de variância zero** (consolidando **66 features ativas**), isolamento anti-vazamento (*data leakage*), transformações numéricas e fatiamento dimensional para a arquitetura **ALF-MoE**.

---

## 1. Ficha Técnica e Metadados de Origem

- **Instituições Responsáveis:** Communications Security Establishment (CSE) e Canadian Institute for Cybersecurity (CIC) da University of New Brunswick (UNB).
- **Ano de Coleta:** 2018 (período de 14 a 23 de fevereiro de 2018, cobrindo 10 dias úteis de atividade contínua).
- **Ambiente Físico e Topologia de Rede:** Infraestrutura implantada na Amazon Web Services (AWS):
  - **Rede da Vítima (*Victim-Network*):** 5 departamentos corporativos segregados, sala de servidores (*Server Room*) centralizada, servidores Windows Server 2016 (Active Directory, DNS) e Ubuntu Linux (Web, FTP, BD), com mais de 500 computadores clientes heterogêneos (Windows 10/8.1/7, macOS, Linux).
  - **Rede de Ataque (*Attack-Network*):** Aproximadamente 50 instâncias Kali Linux e Windows 8.1 sob controle do time ofensivo desferindo vetores de ataque externos e de perímetro.
- **Mecanismo de Extração de Fluxos:** Ferramenta **CICFlowMeter-V3**, parametrizada com $\tau_{\mathrm{idle}} = 120\,\mathrm{s}$ e $\tau_{\mathrm{active}} = 1800\,\mathrm{s}$.
- **Volumetria Bruta Original:** 10 arquivos CSV diários, totalizando aproximadamente 16.233.002 registros e ~6,34 GB em disco.
- **Dimensionalidade Bruta:** 80 atributos brutos (79 métricas de tráfego + coluna de rótulo `Label`).
- **Arquivo Amostrado de Trabalho:** `CSE-CIC-IDS2018_sampled.csv` (1.454.518.563 bytes, ~1,45 GB, 3.712.942 fluxos).
- **Dimensão Ativa Final de Entrada ($D$):** **66 features** (após alinhamento canônico e purga de 10 colunas sem variância).

---

## 2. Estratégia de Amostragem e Mitigação de Desbalanceamento

Na versão bruta completa do CSE-CIC-IDS2018, o tráfego legítimo (*Benign*) supera em várias ordens de magnitude as categorias ofensivas, introduzindo redundâncias massivas de conexões de rotina (tais como requisições repetitivas de NTP, DNS e *polling* de estações clientes). 

Para viabilizar a convergência em tempo hábil e assegurar que a diversidade de vetores raros não fosse diluída, aplicou-se o seguinte protocolo determinístico de subamostragem:

```
[Base Bruta CSE-CIC-IDS2018: ~16,2 Milhões de Fluxos]
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
[Fluxos Maliciosos]              [Fluxos Benignos]
 Total: 2.748.235                Total: ~13,48 Milhões
       │                                 │
       ▼ (Retenção 100%)                 ▼ (Subamostragem 10%)
2.748.235 fluxos preservados     1.348.471 fluxos retidos
       │                                 │
       └────────────────┬────────────────┘
                        ▼
           [Fusão e Desduplicação Exata]
        Eliminação de réplicas de telemetria
                        ▼
      [Base Consolidada: 3.712.942 Registros]
                        │
       ┌────────────────┴────────────────┐
       ▼ (80% Desenvolvimento)           ▼ (20% Teste Independente)
   2.970.353 fluxos                   742.589 fluxos
   ├── Treino (80%): 2.376.282
   └── Validação (20%): 594.071
```

### Regras do Protocolo de Amostragem:
1. **Preservação Integral de Ataques (100%):** Todos os 2.748.235 fluxos classificados em qualquer das 14 categorias de ataque foram preservados intactos.
2. **Subamostragem Estratificada da Classe Benigna (10%):** O tráfego benigno foi subamostrado na proporção de 1:10, retendo 1.348.471 instâncias.
3. **Desduplicação Exata:** A eliminação de registros com vetores estatísticos idênticos resultou em **3.712.942 fluxos únicos**.

---

## 3. Mapeamento Passo a Passo do Pipeline e Módulos Empregados

O pré-processamento do dataset CSE-CIC-IDS2018 é orquestrado pelas classes [`Preprocessor`](file:///home/null/ALF-MoE/src/preprocessing.py) e [`CICDomainFeatures`](file:///home/null/ALF-MoE/src/domain_features.py).

### Etapa 1: Resolução de Caminhos e Ingestão em Memória
- **Módulos Utilizados:** `pathlib.Path`, `os`, `pandas`.
- **Implementação:** Método [`Preprocessor.load_dataset()`](file:///home/null/ALF-MoE/src/preprocessing.py#L505-L518).
- **Procedimento:** A classe [`PreprocessingConfig`](file:///home/null/ALF-MoE/src/config.py#L37-L70) avalia a existência prioritária de `CSE-CIC-IDS2018_sampled.parquet` ou `CSE-CIC-IDS2018_sampled.csv` no diretório configurado. O carregamento é executado via `pd.read_csv(self.dataset_path, low_memory=False)`.

### Etapa 2: Alinhamento Sintático de Schema e Resolução de Aliases
- **Módulos Utilizados:** `src.domain_features.CICDomainFeatures.match_columns()`.
- **Implementação:** [`Preprocessor._align_dataframe_columns()`](file:///home/null/ALF-MoE/src/preprocessing.py#L475-L503).
- **Problema Resolvido:** O extrator CICFlowMeter-V3 gerou o CSE-CIC-IDS2018 com abreviações truncadas nos cabeçalhos que quebram pipelines convencionais. O método `match_columns` contém um grafo de busca baseado no dicionário `alias_candidates` que normaliza automaticamente os nomes:

| Nome Bruto no CSV (CICFlowMeter-V3) | Nome Canônico Harmonizado (ALF-MoE) | Família de Atributo |
| :--- | :--- | :--- |
| `Tot Fwd Pkts` | `Total Fwd Packet` | Contador de Volume |
| `Tot Bwd Pkts` | `Total Bwd packets` | Contador de Volume |
| `TotLen Fwd Pkts` | `Total Length of Fwd Packet` | Volume de Bytes |
| `TotLen Bwd Pkts` | `Total Length of Bwd Packet` | Volume de Bytes |
| `Fwd Pkt Len Max` / `Min` / `Mean` / `Std` | `Fwd Packet Length Max` / `Min` / `Mean` / `Std` | Estatística Espacial |
| `Bwd Pkt Len Max` / `Min` / `Mean` / `Std` | `Bwd Packet Length Max` / `Min` / `Mean` / `Std` | Estatística Espacial |
| `Flow Byts/s` / `Flow Pkts/s` | `Flow Bytes/s` / `Flow Packets/s` | Taxa de Transferência |
| `Fwd IAT Tot` / `Bwd IAT Tot` | `Fwd IAT Total` / `Bwd IAT Total` | Intervalo Temporal |
| `Fwd Header Len` / `Bwd Header Len` | `Fwd Header Length` / `Bwd Header Length` | Cabeçalho L4 |
| `Fwd Pkts/s` / `Bwd Pkts/s` | `FWD Packets/s` / `Bwd Packets/s` | Taxa Direcional |
| `Pkt Len Min` / `Max` / `Mean` / `Std` / `Var` | `Packet Length Min` / `Max` / `Mean` / `Std` / `Variance` | Geometria de Pacotes |
| `FIN Flag Cnt` / `SYN` / `RST` / `PSH` / `ACK` / `URG` | `FIN Flag Count` / `SYN` / `RST` / `PSH` / `ACK` / `URG` | Sinalizadores TCP |
| `CWE Flag Count` | `CWR Flag Count` | Sinalizador TCP (RFC 3168) |
| `ECE Flag Cnt` | `ECE Flag Count` | Sinalizador TCP |
| `Pkt Size Avg` | `Average Packet Size` | Métrica Agregada |
| `Fwd Seg Size Avg` / `Bwd Seg Size Avg` | `Fwd Segment Size Avg` / `Bwd Segment Size Avg` | Métrica L4 |
| `Fwd Byts/b Avg` / `Fwd Pkts/b Avg` / `Fwd Blk Rate Avg` | `Fwd Bytes/Bulk Avg` / `Fwd Packet/Bulk Avg` / `Fwd Bulk Rate Avg` | Estatística de Rajada |
| `Bwd Byts/b Avg` / `Bwd Pkts/b Avg` / `Bwd Blk Rate Avg` | `Bwd Bytes/Bulk Avg` / `Bwd Packet/Bulk Avg` / `Bwd Bulk Rate Avg` | Estatística de Rajada |
| `Subflow Fwd Pkts` / `Subflow Fwd Byts` | `Subflow Fwd Packets` / `Subflow Fwd Bytes` | Subfluxos |
| `Subflow Bwd Pkts` / `Subflow Bwd Byts` | `Subflow Bwd Packets` / `Subflow Bwd Bytes` | Subfluxos |
| `Init Fwd Win Byts` / `Init Bwd Win Byts` | `Fwd Init Win bytes` / `Bwd Init Win bytes` | Janela TCP Inicial |

### Etapa 3: Expurgamento Anti-Leakage e Prevenção de Shortcut Learning
- **Módulos Utilizados:** `pandas.DataFrame.drop()`.
- **Implementação:** Linhas 495-498 de `src/preprocessing.py`.
- **Justificativa Teórica:** Para garantir que modelos preditivos aprendam padrões intrínsecos de tráfego e não atalhos da infraestrutura AWS, foram sumariamente eliminadas as colunas de identificação da rede:
  - `Dst Port`, `Protocol`, `Timestamp`.
  - A quíntupla completa de rede não integra o espaço de treino, impedindo a memorização do IP dos servidores da vítima ou das portas de ataque.

### Etapa 4: Purga de 10 Atributos de Variância Zero (76 $\to$ 66 Features Ativas)
- **Módulos Utilizados:** `pandas.Series.nunique()`, `numpy`.
- **Implementação:** Constante `EXPLICIT_DROP_COLUMNS` combinada com detecção dinâmica em [`Preprocessor._clean_raw_dataset()`](file:///home/null/ALF-MoE/src/preprocessing.py#L536-L552).
- **Detalhamento Crítico:** No dataset CSE-CIC-IDS2018 canônico, além das 3 flags URG explicitamente zeradas, outras 7 colunas possuem variância estritamente nula em todas as conexões, totalizando **10 colunas purgadas**:
  1. `Fwd URG Flags` (0 em 100% dos fluxos)
  2. `Bwd URG Flags` (0 em 100% dos fluxos)
  3. `URG Flag Count` (0 em 100% dos fluxos)
  4. `Bwd PSH Flags` (0 em 100% dos fluxos)
  5. `Fwd Bytes/Bulk Avg` (0 em 100% dos fluxos)
  6. `Fwd Packet/Bulk Avg` (0 em 100% dos fluxos)
  7. `Fwd Bulk Rate Avg` (0 em 100% dos fluxos)
  8. `Bwd Bytes/Bulk Avg` (0 em 100% dos fluxos)
  9. `Bwd Packet/Bulk Avg` (0 em 100% dos fluxos)
  10. `Bwd Bulk Rate Avg` (0 em 100% dos fluxos)
- **Resultado:** O espaço canônico base de 76 atributos é reduzido para **66 features ativas** ($D = 66$). Conforme registrado nos metadados de produção (`artifacts/CSE-CIC-IDS2018/2026-09-27_21:09:15/preprocess/CSE-CIC-IDS2018_metadata.json`), `n_features: 66`.

### Etapa 5: Tratamento de Indefinições Numéricas (NaN e Infinitos)
- **Módulos Utilizados:** `pandas.to_numeric()`, `numpy.isinf()`, `pandas.DataFrame.groupby()`.
- **Implementação:** Linhas 553-574 de `src/preprocessing.py`.
- **Procedimento:**
  1. Conexões de duração nula geram divisões por zero nas métricas de taxa (`Flow Bytes/s` e `Flow Packets/s`), resultando em valores `+inf`.
  2. Todos os infinitos são convertidos em `np.nan`.
  3. Realiza-se a imputação pela **mediana condicional da classe de ataque** correspondente:
     $$x_{ij} \leftarrow \operatorname{mediana}(\{x_{kj} \mid y_k = y_i, x_{kj} \in \mathbb{R}\})$$
  4. Caso todos os valores da classe sejam nulos, adota-se a mediana global calculada exclusivamente no conjunto de treino. Todas as medianas são salvas em `self.feature_medians_` para aplicação na inferência.

### Etapa 6: Mapeamento de Hierarquia de Ameaças (*Threat Levels*)
- **Módulos Utilizados:** Dicionário de mapeamento em [`Preprocessor.threat_classification()`](file:///home/null/ALF-MoE/src/preprocessing.py#L265-L310).
- **Abstração:**
  - **Level 0 (15 Classes Brutas):** `Benign`, `DDOS attack-HOIC`, `DDoS attacks-LOIC-HTTP`, `DDOS attack-LOIC-UDP`, `DoS attacks-Hulk`, `DoS attacks-SlowHTTPTest`, `DoS attacks-GoldenEye`, `DoS attacks-Slowloris`, `Bot`, `FTP-BruteForce`, `SSH-Bruteforce`, `Infilteration`, `Brute Force -Web`, `Brute Force -XSS`, `SQL Injection`.
  - **Level 2 (7 Meta-Categorias Consolidadas para Produção e Teste):**
    - `0: Benign`
    - `1: Botnet` (`Bot`)
    - `2: BruteForce` (`FTP-BruteForce`, `SSH-Bruteforce`)
    - `3: DDoS` (`DDOS attack-HOIC`, `DDoS attacks-LOIC-HTTP`, `DDOS attack-LOIC-UDP`)
    - `4: DoS` (`DoS attacks-Hulk`, `DoS attacks-SlowHTTPTest`, `DoS attacks-GoldenEye`, `DoS attacks-Slowloris`)
    - `5: Infiltration` (`Infilteration`)
    - `6: WebAttack` (`Brute Force -Web`, `Brute Force -XSS`, `SQL Injection`)

### Etapa 7: Particionamento Estratificado e Desduplicação
- **Módulos Utilizados:** `sklearn.model_selection.train_test_split`.
- **Implementação:** [`Preprocessor.generate_train_val_test()`](file:///home/null/ALF-MoE/src/preprocessing.py#L776-L846).
- **Divisão:**
  1. Deduplicação opcional sobre o subconjunto das features canônicas ativas.
  2. Split estratificado 80% desenvolvimento (2.970.353 fluxos) e 20% teste (742.589 fluxos), com `random_state=42`.
  3. Split interno estratificado no desenvolvimento: 80% treino (2.376.282 fluxos) e 20% validação (594.071 fluxos).

### Etapa 8: Ajuste Estrito (*Fit*) e Engenharia de Features
- **Módulos Utilizados:** `pandas.Series.skew()`, `numpy.log1p()`, `sklearn.preprocessing.RobustScaler()`, `sklearn.preprocessing.LabelEncoder()`.
- **Implementação:** [`Preprocessor.fit()`](file:///home/null/ALF-MoE/src/preprocessing.py#L662-L710).
- **Procedimentos Ajustados Exclusivamente no Treino:**
  1. **Detecção de Assimetria e $\log(1+x)$:** Colunas com $|\text{skew}| > 3{,}0$ e valores estritamente não negativos sofrem transformação $x' = \ln(1 + \max(x, 0))$.
  2. **RobustScaler:** Ajustado sobre a matriz $X_{\mathrm{train}}$ transformada com faixa interquartil $Q_{25}$ a $Q_{75}$.
  3. **LabelEncoder:** Mapeia as 7 meta-categorias para os inteiros $\{0, 1, 2, 3, 4, 5, 6\}$.
  4. **Pesos de Classe para Focal Loss:** Calculados via ponderação de raiz quadrada:
     $$w_c = \sqrt{\frac{N}{C \cdot N_c}}$$

| Classe (ID) | Rótulo (Level 2) | Suporte no Teste (20%) | Proporção Relativa | Peso Calculado ($w_c$) |
| :---: | :--- | :--- | :--- | :--- |
| **0** | `Benign` | 269.694 | 36,32% | **0,6272** |
| **1** | `Botnet` | 56.462 | 7,60% | **1,3707** |
| **2** | `BruteForce` | 31.335 | 4,22% | **1,8400** |
| **3** | `DDoS` | 249.274 | 33,57% | **0,6524** |
| **4** | `DoS` | 103.259 | 13,90% | **1,0136** |
| **5** | `Infiltration` | 32.379 | 4,36% | **1,8101** |
| **6** | `WebAttack` | 186 | 0,025% | **23,9060** |
| **Total** | -- | **742.589** | **100,00%** | -- |

### Etapa 9: Fatiamento de Domínios para o Comitê de Especialistas (MoE)
- **Módulos Utilizados:** [`Preprocessor.get_domain_indices()`](file:///home/null/ALF-MoE/src/preprocessing.py#L647-L660).
- **Mapeamento:**
  - `dnn`: 27 atributos em $\mathbf{x}_g$ (sinalizadores, contadores, médias globais). As 7 colunas bulk e `Bwd PSH Flags` purgadas não integravam $\mathbf{x}_g$, preservando a integridade das 27 features do especialista estatístico.
  - `cnn`: 20 atributos em $\mathbf{x}_s$ extraídos pelo `SliceLayer`. Dentro de `build_cnn_expert()`, os primeiros 16 índices canônicos são selecionados e projetados na matriz $4 \times 4 \times 1$.
  - `gru`: 32 atributos em $\mathbf{x}_v$ reorganizados em $8 \times 4$ passos temporais (tempos IAT).
  - `cae`: 27 atributos em $\mathbf{x}_f$ submetidos à janela de Hann e transformada rápida de Fourier RFFT.
  - `lstm`: 18 atributos em $\mathbf{x}_t$ reorganizados em $6 \times 3$ passos de inatividade/atividade.

### Etapa 10: Inferência em Tempo Real e Persistência de Artefatos
- **Módulos Utilizados:** `pickle`, `json`, [`Preprocessor.transform_features()`](file:///home/null/ALF-MoE/src/preprocessing.py#L739-L775).
- **Operação em Tempo Real:** O método `transform_features` recebe um fluxo individual ou lote via dicionário/DataFrame, aplica o mapa de aliases de `domain_features.py`, remove as 10 colunas purgadas, imputa valores ausentes com as medianas de treino, aplica log1p vetorizado e normaliza com o `RobustScaler`.
- **Arquivos Persistidos:** Salvos em `artifacts/CSE-CIC-IDS2018/<timestamp>/preprocess/`:
  - `CSE-CIC-IDS2018_artifacts.pkl`: Objeto preprocessor com o scaler ajustado, encoder e listas de colunas compiladas.
  - `CSE-CIC-IDS2018_metadata.json`: Manifesto de auditoria detalhando parâmetros, versões do runtime e mapeamentos.

---

## 4. Limitações Críticas Identificadas na Versão Original

A avaliação científica rigorosa conduzida sobre esta versão canônica do CSE-CIC-IDS2018 permitiu ratificar empiricamente os achados da literatura recente:

1. **Rótulo Malicioso em Porta Fechada (`FTP-BruteForce`):** O servidor na porta 21 rejeitou as conexões com pacotes `[RST, ACK]` em ambos os dias de ataque. O modelo aprende que conexões abortadas com RST em portas fechadas são maliciosas, um falso atalho metodológico.
2. **Janelas Temporais Cegas:** Milhares de conexões marcadas como ataque consistiam em fluxos nos quais nenhum payload malicioso trafegou.
3. **Agrupamento Indiscriminado em Infiltração:** A classe `Infilteration` misturou varreduras de porta (NMAP), acessos Dropbox e movimentação lateral, criando uma distribuição multimodal dispersa.

Essas limitações motivaram diretamente a criação e inclusão no projeto da versão corrigida ([[02_Agente_CSE_CIC_IDS2018_Corrigido|CSE-CIC-IDS2018 Corrigido]]), documentada pelo Agente 2.
