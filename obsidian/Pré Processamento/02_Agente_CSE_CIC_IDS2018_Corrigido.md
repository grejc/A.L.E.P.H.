# Relatório Técnico de Pré-Processamento — Agente 2

## Dataset: CSE-CIC-IDS2018 Corrigido / Improved (`CSECICIDS2018_improved`)

---

### Sumário Executivo

O dataset **CSE-CIC-IDS2018 Corrigido** (*Improved*) constitui a versão tecnicamente auditada e saneada do benchmark da AWS, incorporando os avanços científicos introduzidos por **Liu et al. (IEEE CNS 2022)** para neutralizar falhas ontológicas severas de rotulagem, inconsistências no encerramento de conexões TCP e contaminação por *data leakage*. 

Este relatório documenta a íntegra da engenharia de pré-processamento executada pelo **Agente 2** sobre a base corrigida de **34 GiB (63,2 milhões de fluxos brutos)** e sua partição colunar Parquet de alto rendimento. O documento detalha as rotinas de *streaming I/O*, expurgo de 9 identificadores, reclassificação semântica de fluxos com portas fechadas, alinhamento canônico, purga de 3 flags URG sem variância (**73 features ativas**), balanceamento de classes ultra-raras, fatiamento dimensional e integração direta com a arquitetura neural **ALF-MoE**.

---

## 1. Contexto Científico e Motivação da Auditoria (Liu et al., 2022)

Em 2022, pesquisadores da University of New South Wales, Defence Science and Technology Group e KU Leuven publicaram o estudo seminal:

```bibtex
@inproceedings{liu2022error,
  title={Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018},
  author={Liu, Lisa and Engelen, Gints and Lynar, Timothy and Essam, Daryl and Joosen, Wouter},
  booktitle={2022 IEEE Conference on Communications and Network Security (CNS)},
  pages={254--262},
  year={2022},
  organization={IEEE},
  doi={10.1109/CNS56114.2022.9947235}
}
```

A investigação identificou que o gerador original (CICFlowMeter-V3) rotulou os fluxos de rede baseando-se estritamente na janela temporal em que os scripts de ataque foram disparados, sem inspecionar se a interação ofensiva havia de fato ocorrido.

### As Quatro Falhas Catastróficas Corrigidas:

1. **Ataque em Porta Fechada (`FTP-BruteForce`):**
   Durante os dois dias de execução do ataque de força bruta contra o serviço FTP, o servidor na porta 21 respondeu exclusivamente com pacotes com sinalizadores `[RST, ACK]`. Essa assinatura comprova que o serviço de FTP estava inativo no sistema operacional hospedeiro, de modo que a pilha TCP do kernel rejeitou imediatamente todas as conexões antes de qualquer handshake ou tentativa de senha. Na base original, milhões desses pacotes foram marcados como ataque; o modelo aprendia que "pacotes RST de portas fechadas" configuravam ataque de força bruta. Na versão corrigida, **100% dos fluxos foram reclassificados como `BENIGN`**.
2. **Reclassificação de Categorias de Tentativa (*Attempted Categories*):**
   Milhares de fluxos etiquetados como ataque consumado consistiam em meras tentativas que não geraram interação hostil (campo `Attempted Category != -1`). Conforme diretriz de Liu et al. (2022), para prevenir o aprendizado espúrio (*Garbage In, Garbage Out*), **todas as conexões do tipo "Attempted" foram reclassificadas como tráfego benigno (`BENIGN`)**.
3. **Desagregação Granular de Infiltração:**
   A classe monolítica `Infilteration` original agrupava atividades com características físico-matemáticas diametralmente opostas. A versão melhorada reestruturou o vetor em três categorias realísticas:
   - `Infiltration - NMAP Portscan`: Varredura massiva de portas com pacotes curtos e alta frequência.
   - `Infiltration - Communication Victim Attacker`: Canal de Comando e Controle (C2) interno de tráfego intermitente.
   - `Infiltration - Dropbox Download`: Exfiltração/download pontual via HTTPS (apenas 85 fluxos no total bruto).
4. **Correção de Timeouts e Bounding de Fluxos TCP:**
   O extrator original encerrava prematuramente fluxos TCP bidirecionais ao receber flags de FIN fora de ordem, duplicando métricas estatísticas e inflando artificialmente as contagens.

---

## 2. Ficha Técnica dos Arquivos e I/O de Alta Performance

| Parâmetro | Versão Bruta CSV (`CSECICIDS2018_improved.csv`) | Versão Otimizada Parquet (`CSECICIDS2018_improved.parquet`) |
| :--- | :--- | :--- |
| **Tamanho Físico em Disco** | 36.044.453.883 bytes (~34 GiB) | 1.042.648.008 bytes (~1,04 GB) |
| **Total de Linhas (Fluxos)** | 63.195.145 registros | 63.195.145 registros |
| **Total de Colunas Brutas** | 91 colunas | 91 colunas tipadas |
| **Mecanismo de Ingestão** | Streaming multithread com `pyarrow.csv` (`block_size = 64 MiB`) | Carregamento colunar vetorizado via `pyarrow.parquet` |
| **Tempo Típico de Ingestão** | ~180 segundos em SSD NVMe | **< 4,5 segundos** (redução de 97,5% no I/O) |

---

## 3. Mapeamento Passo a Passo do Pipeline e Módulos Empregados

O pré-processamento do dataset corrigido é gerenciado pelo módulo [`src/preprocessing.py`](file:///home/null/ALF-MoE/src/preprocessing.py) em sintonia com a ontologia em [`src/domain_features.py`](file:///home/null/ALF-MoE/src/domain_features.py).

```
[CSECICIDS2018_improved.parquet / .csv]
                    │
                    ▼
     1. Ingestão Vetorizada PyArrow ──────────► [pyarrow.parquet, pyarrow.csv]
                    │
                    ▼
     2. Expurgamento de 9 Identificadores ────► [pandas.DataFrame.drop]
        (id, Flow ID, 5-tuple, Timestamp,
         Attempted Category)
                    │
                    ▼
     3. Destilação e Alinhamento de Schema ───► [src.domain_features.CICDomainFeatures]
        (91 colunas brutas ──► 81 métricas ──► 76 canônicas)
                    │
                    ▼
     4. Purga de Variância Nula ──────────────► [src.preprocessing.Preprocessor._clean_raw_dataset]
        (Fwd URG Flags, Bwd URG Flags, URG Flag Count) ──► 73 Features Ativas
                    │
                    ▼
     5. Imputação por Mediana Condicional ────► [pandas.DataFrame.groupby(target)[col]]
        (Tratamento de NaN e Infinitos)
                    │
                    ▼
     6. Agrupamento de Ameaças (Threat L2) ───► [src.preprocessing.Preprocessor.threat_classification]
        (15 Classes Ativas ──► 9 Meta-Categorias Consolidadas)
                    │
                    ▼
     7. Particionamento Estratificado ────────► [sklearn.model_selection.train_test_split]
        (20% Teste Independente: 1.263.903 fluxos; 80% Desenvolvimento)
                    │
                    ▼
     8. Engenharia de Features no Treino ─────► [scipy.stats, numpy.log1p, RobustScaler]
        ├─ Skewness (|skew| > 3.0) ──► Log1p
        ├─ RobustScaler (IQR 25-75)
        ├─ LabelEncoder (Classes 0 a 8)
        └─ Class Weights: Ponderação Atenuada sqrt(N / C*Nc)
                    │
                    ▼
     9. Fatiamento MoE (SliceLayer) ──────────► [src.preprocessing.Preprocessor.get_domain_indices]
        (DNN: 27 | CNN: 20 -> 16 canônicos | GRU: 32 | CAE: 27 | LSTM: 18)
                    │
                    ▼
    10. Serialização e Inferência Online ─────► [pickle, json, Preprocessor.transform_features]
```

### Etapa 1: Ingestão de Alto Rendimento
- **Módulos Utilizados:** `pyarrow.parquet`, `pyarrow.csv`, `pandas`.
- **Implementação:** Linhas 505-518 de `src/preprocessing.py`.
- **Procedimento:** O preprocessor busca nativamente a extensão `.parquet` antes de recorrer ao `.csv`. Ao processar arquivos parquet, a engine PyArrow carrega os tensores diretamente em memória paginada com alocação zero-copy.

### Etapa 2: Expurgamento Rigoroso de 9 Identificadores e Metadados Anti-Leakage
- **Módulos Utilizados:** `pandas.DataFrame.drop()`.
- **Justificativa Metodológica:** Para assegurar que o modelo não memorize a topologia da rede de testes da AWS nem se beneficie de metadados internos da auditoria:
  1. `id`: Identificador sequencial primário.
  2. `Flow ID`: Hash único da conexão.
  3. `Src IP`: Endereço IP de origem.
  4. `Src Port`: Porta de transporte efêmera do cliente.
  5. `Dst IP`: Endereço IP do servidor alvo na AWS.
  6. `Dst Port`: Porta de serviço (80, 443, 21, 22).
  7. `Protocol`: Protocolo encapsulado (TCP = 6, UDP = 17).
  8. `Timestamp`: Carimbo de data/hora (eliminação de atalhos cronológicos).
  9. `Attempted Category`: Flag auxiliar da auditoria de Liu et al. (2022).

### Etapa 3: Alinhamento de Schema e Redução Dimensional (91 $\to$ 81 $\to$ 76 $\to$ 73)
- **Módulos Utilizados:** `src.domain_features.CICDomainFeatures.match_columns()`.
- **Procedimento:** As 91 colunas brutas do dataset corrigido contêm metadados operacionais e 81 métricas de tráfego. O preprocessor mapeia essas métricas contra a lista `CICDomainFeatures.raw` (76 colunas canônicas) e elimina explicitamente as 3 colunas de sinalizadores URG sem variância (`EXPLICIT_DROP_COLUMNS`), estabelecendo o vetor de **73 features ativas**.

### Etapa 4: Imputação Numérica Condicional
- **Módulos Utilizados:** `pandas.Series.replace()`, `pandas.DataFrame.groupby()`, `numpy`.
- **Procedimento:**
  - Valores infinitos (`+inf`, `-inf`) decorrentes de divisões por zero em fluxos ultra-rápidos com duração nula são substituídos por `NaN`.
  - A imputação ocorre pela mediana da respectiva classe de tráfego computada no conjunto de treino.
  - Caso haja ausência total na classe, utiliza-se a mediana global de treino armazenada em `feature_medians_`.

### Etapa 5: Hierarquia Semântica de Ameaças (*Threat Levels*)
- **Módulos Utilizados:** [`Preprocessor.threat_classification()`](file:///home/null/ALF-MoE/src/preprocessing.py#L186-L264).
- **Mapeamento:**
  - **Threat Level 0 (15 Classes Efetivas Ativas):**
    `BENIGN`, `DoS Hulk`, `Botnet Ares`, `DDoS-HOIC`, `SSH-BruteForce`, `Infiltration - NMAP Portscan`, `DDoS-LOIC-HTTP`, `DoS GoldenEye`, `DoS Slowloris`, `DDoS-LOIC-UDP`, `Infiltration - Communication Victim Attacker`, `Web Attack - Brute Force`, `Web Attack - XSS`, `Infiltration - Dropbox Download`, `Web Attack - SQL`.
  - **Threat Level 2 (9 Meta-Categorias Consolidadas):**
    - `0: BENIGN` (incorporando tráfego normal e todos os fluxos *Attempted* e conexões com porta fechada)
    - `1: Botnet` (`Botnet Ares`)
    - `2: DDoS` (`DDoS-HOIC`, `DDoS-LOIC-HTTP`, `DDoS-LOIC-UDP`)
    - `3: DoS` (`DoS Hulk`, `DoS GoldenEye`, `DoS Slowloris`)
    - `4: Infiltration - Communication Victim Attacker`
    - `5: Infiltration - Dropbox Download`
    - `6: Infiltration - NMAP Portscan`
    - `7: SSH-BruteForce`
    - `8: Web Attack` (`Web Attack - Brute Force`, `Web Attack - XSS`, `Web Attack - SQL`)

### Etapa 6: Particionamento Estratificado e Suporte Amostral de Teste
- **Módulos Utilizados:** `sklearn.model_selection.train_test_split`.
- **Divisão:** 80% desenvolvimento e 20% teste independente (`stratify=y`, `random_state=42`).
- **Suporte de Teste:** O conjunto de teste consolidou **1.263.903 fluxos avaliados**, espelhando de forma realista a predominância de tráfego legítimo em redes corporativas (89,27% BENIGN).

### Tabela de Distribuição e Ponderação de Classes (Threat Level 2):

| Classe (ID) | Macro-Categoria (L2) | Suporte de Teste (20%) | Proporção (%) | Peso Calculado ($w_c$) |
| :---: | :--- | :--- | :--- | :--- |
| **0** | `BENIGN` | 1.128.279 | 89,269% | **0,3528** |
| **1** | `Botnet` | 28.584 | 2,262% | **2,2165** |
| **2** | `DDoS` | 27.938 | 2,210% | **2,2420** |
| **3** | `DoS` | 42.273 | 3,345% | **1,8227** |
| **4** | `Infiltration - Communication Victim Attacker` | 41 | 0,003% | **58,7948** |
| **5** | `Infiltration - Dropbox Download` | 17 | 0,001% | **90,3918** |
| **6** | `Infiltration - NMAP Portscan` | 17.875 | 1,414% | **2,8030** |
| **7** | `SSH-BruteForce` | 18.839 | 1,491% | **2,7302** |
| **8** | `Web Attack` | 57 | 0,005% | **49,8277** |
| **Total** | -- | **1.263.903** | **100,00%** | -- |

### Etapa 7: Atenuação de Assimetria ($\log(1+x)$) e Escalonamento Robusto
- **Módulos Utilizados:** `pandas.Series.skew()`, `numpy.log1p()`, `sklearn.preprocessing.RobustScaler()`.
- **Procedimento:**
  - 35 atributos identificados com $|\text{skew}| > 3{,}0$ no conjunto de treino sofreram transformação $\ln(1 + \max(x, 0))$.
  - O `RobustScaler` centraliza os dados na mediana e divide pelo IQR:
    $$\tilde{x}_{ij} = \frac{x_{ij}' - Q_{50}}{Q_{75} - Q_{25}}$$
  - Essa técnica impede que rajadas gigantescas de pacotes dos ataques DoS e DDoS distorçam o espaço latente dos especialistas.

### Etapa 8: Mapeamento de Domínios para os 5 Especialistas MoE
- **Módulos Utilizados:** [`Preprocessor.get_domain_indices()`](file:///home/null/ALF-MoE/src/preprocessing.py#L647-L660).
- **Subtensores:**
  - `dnn`: 27 atributos em $\mathbf{x}_g$.
  - `cnn`: 20 atributos em $\mathbf{x}_s$ extraídos pelo `SliceLayer`. Dentro de `build_cnn_expert()`, os 16 primeiros são selecionados e projetados na pseudo-imagem $4 \times 4 \times 1$.
  - `gru`: 32 atributos em $\mathbf{x}_v$ formatados em $8 \times 4$ passos temporais.
  - `cae`: 27 atributos em $\mathbf{x}_f$ pré-processados pela janela de Hann e RFFT.
  - `lstm`: 18 atributos em $\mathbf{x}_t$ formatados em $6 \times 3$ passos de inatividade/atividade.

### Etapa 9: Inferência em Tempo Real e Persistência de Artefatos
- **Módulos Utilizados:** `pickle`, `json`, [`Preprocessor.transform_features()`](file:///home/null/ALF-MoE/src/preprocessing.py#L739-L775), [`src/inference.py`](file:///home/null/ALF-MoE/src/inference.py).
- **Integração Operacional:** No motor de inferência, fluxos ao vivo vindos do extrator NFStream são pré-processados pelo `Preprocessor.transform_features()` com latência média de **$0{,}0118\,\mathrm{ms}$ por fluxo** (vazão de mais de 84.000 fluxos/s).
- **Artefatos Persistidos:** Salvos em `artifacts/CSECICIDS2018_improved/<timestamp>/preprocess/`:
  - `CSECICIDS2018_improved_artifacts.pkl`: Objeto preprocessor contendo o scaler ajustado, encoders e medianas.
  - `CSECICIDS2018_improved_metadata.json`: Manifesto com hashes de integridade, parâmetros e versões do ambiente (`Python 3.11.9`, `scikit-learn 1.9.0`, `pandas 3.0.3`, `numpy 2.4.6`).
