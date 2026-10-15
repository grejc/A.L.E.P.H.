# Relatório Técnico de Pré-Processamento — Agente 3

## Dataset: CIC-UNSW-NB15 (Hardware IXIA PerfectStorm e Amostragem com Máxima Entropia)

---

### Sumário Executivo

O conjunto de dados **CIC-UNSW-NB15** é uma referência consolidada na literatura internacional para avaliação de NIDS sob cenários de alta densidade de tráfego sintético e realístico. Concebido pelo *Australian Centre for Cyber Security* (ACCS) na Universidade de New South Wales (UNSW Canberra), o dataset foi gerado a partir de uma plataforma de hardware dedicada **IXIA PerfectStorm**, combinando atividades operacionais humanas com vetores contemporâneos de ataque e modelagem de vulnerabilidades (CVE).

Este relatório documenta a engenharia de dados executada pelo **Agente 3** sobre a versão extraída via motor **CICFlowMeter**, destacando a neutralização do risco crítico de *shortcut learning* por endereços IP, o protocolo de amostragem de máxima entropia comportamental para prevenção de **GIGO**, a purga de 9 variáveis de variância nula (**67 features ativas**, com especialista DNN operando em **25 atributos**), a conciliação formal entre os volumes amostrais (139.583 brutos vs. 125.378 deduplicados) e o balanceamento das 10 classes canônicas para o modelo **ALF-MoE**.

---

## 1. Ficha Técnica e Metadados do Dataset

- **Instituição Desenvolvedora:** Australian Centre for Cyber Security (ACCS), UNSW Canberra.
- **Autores Principais:** Nour Moustafa e Jill Slay (2015).
- **Ambiente de Geração:** Laboratório *Cyber Range Lab* utilizando a ferramenta de hardware de nível de operadora **IXIA PerfectStorm**. A bancada injetou simultaneamente tráfego de fundo realista (navegação web, e-mail, streaming) e ataques automatizados em enlaces físicos Gigabit Ethernet, capturando mais de 100 GB de tráfego em arquivos PCAP puros.
- **Motor de Extração de Atributos:** Ferramenta **CICFlowMeter**, que processou os PCAPs brutos para gerar uma representação tabular bidirecional com os mesmos descritores estatísticos das séries do CIC.
- **Volumetria da População Bruta (`CIC-UNSW-NB15.csv`):** 1.914.305.081 bytes (~1,91 GB), 3.540.241 fluxos e 84 colunas brutas.
- **Composição Bruta da População:**
  - Tráfego Benigno: **3.450.658 fluxos (97,47%)**.
  - Tráfego Malicioso (9 famílias de ataque): **89.583 fluxos (2,53%)**.
- **Arquivo Amostrado de Trabalho:** `CIC-UNSW-NB15_sampled.csv` (79.305.798 bytes, ~79,3 MB, 139.583 fluxos).
- **Dimensão Ativa Final de Entrada ($D$):** **67 features** (após alinhamento canônico e purga de 9 colunas sem variância).

---

## 2. Diagnóstico de Vazamento de Dados (*Data Leakage*) e *Shortcut Learning*

A auditoria estatística realizada pelo Agente 3 nos metadados brutos revelou uma vulnerabilidade metodológica comum em datasets sintéticos:

> [!CRITICAL]
> **Vazamento Catastrófico por Endereçamento IP:**
> **100% de todos os 89.583 ataques** originam-se exclusivamente de quatro endereços IP pertencentes ao rack do testbed:
> - `175.45.176.0` (22.939 ataques)
> - `175.45.176.1` (22.927 ataques)
> - `175.45.176.3` (22.461 ataques)
> - `175.45.176.2` (21.256 ataques)
> Em contrapartida, o tráfego benigno é emitido pela sub-rede sintética `59.166.0.0/24` em direção a servidores `149.171.126.X`.

Caso os campos de IP fossem mantidos, qualquer rede neural atingiria 100% de acurácia memorizando simplesmente a sub-rede `175.45.176.0/24`, tornando o modelo completamente cego e inútil em redes operacionais reais. Por essa razão, a quíntupla de rede (`Src IP`, `Dst IP`, `Src Port`, `Dst Port`, `Protocol`) e marcas de tempo (`Timestamp`, `Flow ID`) são sumariamente eliminadas na primeira etapa de sanitização.

---

## 3. Protocolo de Amostragem com Máxima Entropia e Reconciliação Volumétrica

No dataset completo, a relação de desbalanceamento é severa: **38,5 fluxos legítimos para cada 1 fluxo malicioso**. A maioria esmagadora das conexões benignas é constituída por consultas DNS triviais e handshakes TCP curtos e idênticos.

Para evitar que o modelo sofra degradação por GIGO (*Garbage In, Garbage Out*) decorrente do excesso de instâncias triviais não informativas, aplicou-se a seguinte metodologia:

```
[População Bruta CIC-UNSW-NB15: 3.540.241 Fluxos]
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
 [Fluxos Maliciosos]               [Fluxos Benignos]
  Total: 89.583 fluxos              Total: 3.450.658 fluxos
         │                                 │
         ▼ (Retenção Estrita 100%)         ▼ (Amostragem de Máxima Entropia)
  89.583 ataques preservados        50.000 instâncias benignas selecionadas
         │                                 │
         └────────────────┬────────────────┘
                          ▼
       [Amostra de Trabalho: 139.583 Registros]
                          │
         ┌────────────────┴────────────────┐
         ▼ (Fluxo A: Sem Deduplicação)     ▼ (Fluxo B: Deduplicação Exploratória)
    Config Padrão (deduplicate=False)    Notas EDA (deduplicate=True)
         │                                 │
         ▼                                 ▼
   Total: 139.583 fluxos             Total: 125.378 fluxos únicos (-14.205)
   ├── Split 80% Dev: 111.666        ├── Split 80% Dev: 100.302
   │   ├── Treino: 89.333            │   ├── Treino: 80.241
   │   └── Validação: 22.333         │   └── Validação: 20.061
   └── Split 20% Teste: 27.917       └── Split 20% Teste: 25.076
```

### Explicação da Conciliação de Métricas (27.917 vs. 25.076 instâncias de teste):
1. **Fluxo A — Pipeline de Produção (Adotado no Treino e Avaliação Real):**
   - Configuração: `PreprocessingConfig(deduplicate=False)`.
   - População de entrada: 139.583 registros de `CIC-UNSW-NB15_sampled.csv`.
   - Divisão de 20% para teste: $139.583 \times 0{,}20 = \mathbf{27.917\text{ instâncias de teste}}$.
   - Esse é o valor real auditado nos relatórios de teste (`test_report.txt` e `test_report.json` em `artifacts/CIC-UNSW-NB15/2026-09-27_20:19:01/`).
2. **Fluxo B — Análise Exploratória Offline (Documentada nas Notas Iniciais):**
   - Conforme documentado no arquivo histórico [[Processamento dos Datasets|obsidian/Processamento dos Datasets.md]], a aplicação de `drop_duplicates(subset=features)` eliminou 14.205 fluxos com assinaturas idênticas, resultando em 125.378 fluxos (Treino: 80.241, Validação: 20.061, Teste: 25.076).

---

## 4. Particularidade Dimensional: Purga de 9 Variáveis sem Variância (67 Features Ativas)

Durante a rotina de sanitização preliminar [`Preprocessor._clean_raw_dataset()`](file:///home/null/ALF-MoE/src/preprocessing.py#L520-L575), a inspeção de variância dinâmica (`nunique(dropna=True) <= 1`) identificou que no CIC-UNSW-NB15 **nove colunas apresentavam variância estritamente nula**:

1. `Fwd URG Flags` (0 em 100% dos fluxos)
2. `Bwd URG Flags` (0 em 100% dos fluxos)
3. `URG Flag Count` (0 em 100% dos fluxos)
4. `Bwd PSH Flags` (0 em 100% dos fluxos)
5. `CWR Flag Count` (0 em 100% dos fluxos)
6. `ECE Flag Count` (0 em 100% dos fluxos)
7. `Fwd Bytes/Bulk Avg` (0 em 100% dos fluxos)
8. `Fwd Packet/Bulk Avg` (0 em 100% dos fluxos)
9. `Fwd Bulk Rate Avg` (0 em 100% dos fluxos)

Essas 9 variáveis foram automaticamente purgadas e registradas em `dropped_variance_columns`. Consequentemente, o **CIC-UNSW-NB15 opera com $D = 67$ features ativas** ($76 - 9 = 67$).

### Impacto Direto no Fatiamento MoE (`SliceLayer`):
- Como os atributos `CWR Flag Count` e `ECE Flag Count` pertencem originalmente ao grupo estatístico global $\mathbf{x}_g$ (que possui 27 features nos demais datasets), a purga desses dois campos reduz o vetor do **Especialista DNN para exatamente 25 features ativas** (`len(domain_indices["dnn"]) == 25`).
- Os demais especialistas permanecem intactos: CNN com 20 (16 canônicos), GRU com 32, CAE com 27 e LSTM com 18.

---

## 5. Mapeamento Passo a Passo do Pipeline e Módulos Empregados

### Etapa 1: Ingestão e Leitura
- **Módulos Utilizados:** `pandas.read_csv(low_memory=False)`.
- **Implementação:** [`Preprocessor.load_dataset()`](file:///home/null/ALF-MoE/src/preprocessing.py#L505-L518).
- **Procedimento:** Carrega o arquivo `CIC-UNSW-NB15_sampled.csv` e alinha as colunas com a nomenclatura canônica.

### Etapa 2: Alinhamento de Schema e Identificação do Target
- **Módulos Utilizados:** `src.domain_features.CICDomainFeatures.match_columns()`.
- **Procedimento:** O preprocessor reconhece a coluna `Label` e mapeia as 75 features numéricas restantes contra o espaço canônico do ALF-MoE.

### Etapa 3: Tratamento de Indefinições Numéricas
- **Módulos Utilizados:** `pandas.to_numeric()`, `pandas.DataFrame.groupby()`, `numpy`.
- **Procedimento:** Infinitos são substituídos por `NaN` e imputados pela mediana condicional de classe obtida no conjunto de treino.

### Etapa 4: Mapeamento de Hierarquia de Ameaças (*Threat Levels*)
- **Módulos Utilizados:** [`Preprocessor.threat_classification()`](file:///home/null/ALF-MoE/src/preprocessing.py#L311-L314).
- **Comportamento Específico:** Como as 10 classes do UNSW-NB15 já representam macro-famílias comportamentais canônicas, o preprocessor aplica um mapeamento direto de identidade (1:1):
  $$\operatorname{ThreatLevel}(c) = c, \quad \forall c \in \{0, 1, \dots, 9\}$$

### Tabela de Classes, Suporte Amostral de Teste e Ponderação ($w_c$):

| ID | Classe Canônica | Vetor de Ameaça | Suporte Teste (20%) | Proporção (%) | Peso Calculado ($w_c$) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **0** | `Analysis` | Varreduras pontuais de diretórios e sondagem HTTP | 77 | 0,28% | **6,0261** |
| **1** | `Backdoor` | Canais de acesso furtivo e persistência | 90 | 0,32% | **5,5501** |
| **2** | `Benign` | Tráfego operacional legítimo | 10.000 | 35,82% | **0,5284** |
| **3** | `DoS` | Saturação de recursos e largura de banda | 894 | 3,20% | **1,7680** |
| **4** | `Exploits` | Exploração de vulnerabilidades conhecidas (CVE) | 6.190 | 22,17% | **0,6715** |
| **5** | `Fuzzers` | Injeção de cargas corrompidas para indução de falhas | 5.923 | 21,22% | **0,6866** |
| **6** | `Generic` | Colisões criptográficas e ataques genéricos de cifras | 927 | 3,32% | **1,7361** |
| **7** | `Reconnaissance` | Varreduras de portas e enumeração de topologia | 3.347 | 11,99% | **0,9133** |
| **8** | `Shellcode` | Cargas executáveis para abertura de shell reversa | 420 | 1,50% | **2,5772** |
| **9** | `Worms` | Malware autoreplicável | 49 | 0,18% | **7,5193** |
| **Total**| -- | **10 Classes Canônicas** | **27.917** | **100,00%** | -- |

### Etapa 5: Engenharia de Features e Escalonamento no Treino
- **Módulos Utilizados:** `pandas.Series.skew()`, `numpy.log1p()`, `sklearn.preprocessing.RobustScaler()`, `sklearn.preprocessing.LabelEncoder()`.
- **Procedimento:**
  - 37 features apresentaram assimetria severa ($|\text{skew}| > 3{,}0$) e foram transformadas via $\ln(1 + \max(x, 0))$.
  - O `RobustScaler` é ajustado estritamente sobre $X_{\mathrm{train}}$ para evitar vazamento informacional.

### Etapa 6: Fatiamento Dinâmico MoE (`SliceLayer`)
- **Módulos Utilizados:** [`Preprocessor.get_domain_indices()`](file:///home/null/ALF-MoE/src/preprocessing.py#L647-L660).
- **Dimensões das Sub-Redes:**
  - `dnn`: **25 atributos** em $\mathbf{x}_g$ (após purga de `CWR Flag Count` e `ECE Flag Count`).
  - `cnn`: **20 atributos** em $\mathbf{x}_s$ extraídos pelo `SliceLayer` (16 canônicos projetados na grade $4 \times 4 \times 1$ em `cnn.py`).
  - `gru`: **32 atributos** em $\mathbf{x}_v$ formatados em $8 \times 4$.
  - `cae`: **27 atributos** em $\mathbf{x}_f$ submetidos à janela de Hann e RFFT.
  - `lstm`: **18 atributos** em $\mathbf{x}_t$ formatados em $6 \times 3$.

### Etapa 7: Inferência em Tempo Real e Serialização Atômica
- **Módulos Utilizados:** `pickle`, `json`, [`Preprocessor.transform_features()`](file:///home/null/ALF-MoE/src/preprocessing.py#L739-L775).
- **Execução:** O método `transform_features` recebe fluxos brutos em tempo real, elimina as 9 colunas sem variância, realiza imputação de valores com base no vetor congelado de medianas e escalona a matriz para $(N, 67)$.
- **Artefatos:** Salvos em `artifacts/CIC-UNSW-NB15/<timestamp>/preprocess/`:
  - `CIC-UNSW-NB15_artifacts.pkl`: Objeto preprocessor serializado contendo o scaler, encoder e listas de colunas compiladas.
  - `CIC-UNSW-NB15_metadata.json`: Manifesto com `n_features: 67`, `n_classes: 10`, `dropped_variance_columns: 9`.
