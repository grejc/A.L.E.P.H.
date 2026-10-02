---
title: Rede Intelectual, Cadeias Epistemológicas e Clusters da Base
aliases:
- Rede Intelectual
- Rede_Intelectual
- Cadeias Epistemológicas
tags:
- rede-intelectual
- epistemologia
- bibliografia
- alf-moe
---

# 🕸️ Rede Intelectual e Cadeias Epistemológicas da Literatura

> Mapeamento das **17 arestas estruturadas de relacionamento direto**, **3 cadeias intelectuais epistemológicas completas** (com 7 etapas cada: Conceito $\to$ Fundamentação $\to$ Método $\to$ Experimento $\to$ Resultado $\to$ Limitação $\to$ Lacuna) e clusters de datasets e arquiteturas.

---

## 📍 Grafo de Relacionamentos Diretos (17 Arestas Estruturadas)
| Origem | Relação | Destino | Detalhes da Conexão |
| :--- | :---: | :--- | :--- |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_001]] (*On Calibration of Modern Neural Networks*) | ALF-MoE utiliza Vector Scaling e teoria de calibração afim de probabilidades de Guo et al. no módulo de gating. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `fundamenta_teoria` | [[artigo_025]] (*One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*) | ALF-MoE baseia-se na comprovação de que modelos 'one-for-all' falham em segurança dada por Yang et al. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `compara_arquitetura` | [[artigo_044]] (*TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*) | Ambos propõem Mixture-of-Experts para tráfego heterogêneo cifrado com roteamento dinâmico. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_040]] (*Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*) | ALF-MoE extrai atributos temporais e IATs para alimentar o especialista GRU baseado nas descobertas de Luay et al. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_047]] (*Network Intrusion Detection Model Based on CNN and GRU*) | Justifica o uso de GRU para modelar transições rápidas e cadência temporal com menor custo de treino. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_048]] (*A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*) | Adota Convolutional Autoencoder (CAE) para representação comprimida robusta a ruídos e erro de reconstrução. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_045]] (*UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*) | Aplica decomposição no domínio da frequência (RFFT) inspirada na ciclostacionariedade comprovada no UGR'16. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) | Adota protocolo rigoroso de particionamento estritamente temporal para evitar data leakage. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_metodologia` | [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) | Emprega representação padronizada de atributos inspirada no NetFlow Standard Feature Set de 43 atributos. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `utiliza_ferramenta` | [[artigo_026]] (*NFStream: A flexible network data analysis framework*) | Utiliza o NFStream como base da extração em tempo real de fluxos bidirecionais. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `avalia_dataset` | [[artigo_041]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*) | Avalia o ALF-MoE no dataset canônico CIC-IDS-2017. |
| [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) | `avalia_dataset` | [[artigo_009]] (*CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*) | Avalia o ALF-MoE no benchmark de ataques de IoT em larga escala CICIoT2023. |
| [[artigo_006]] (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*) | `critica_e_sanitiza` | [[artigo_041]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*) | Guadarrama et al. analisam criticamente inconsistências e redundâncias do CIC-IDS-2017. |
| [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) | `estende_critica` | [[artigo_006]] (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*) | Luay et al. comprovam que avaliações com random split inflacionam métricas reportadas na literatura de NIDS. |
| [[artigo_040]] (*Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*) | `estende_representacao` | [[artigo_027]] (*NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*) | Luay et al. estendem o formato NetFlow padronizado por Sarhan et al. adicionando atributos temporais de IAT. |
| [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) | `consolida_padrao` | [[artigo_027]] (*NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*) | Sarhan et al. consolidam o conjunto padronizado NetFlow de 43 atributos para interoperabilidade cross-dataset. |
| [[artigo_042]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (Duplicate Copy)*) | `duplicata_exata` | [[artigo_041]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*) | artigo_042 é idêntico byte a byte ao artigo_041 (Toward Generating a New Intrusion Detection Dataset...). |

---

## 🧬 As 3 Cadeias Intelectuais Epistemológicas
### Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo ^Cadeia_1_Criptografia_e_Fluxo
> Esta cadeia retrata a transição epistemológica imposta pela consolidação de protocolos criptográficos (TLS 1.3, HTTPS, DoH). A obsolescência do DPI força a migração para representações de tráfego baseadas em NetFlow/NFStream, possibilitando a detecção precisa de intrusões sem violação de privacidade nem acesso a cargas úteis em texto claro.

| Etapa Epistemológica | Descrição | Artigos Vinculados |
| :--- | :--- | :--- |
| **CONCEITO** | Opacidade da carga útil por criptografia TLS 1.3 / HTTPS / DoH | [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*); [[artigo_044]] (*TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*) |
| **FUNDAMENTAÇÃO** | Ineficácia de DPI e necessidade de inspeção baseada em metadados de fluxo | [[artigo_006]] (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*); [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) |
| **MÉTODO** | Extração e agregação de fluxos bidirecionais padronizados via NFStream e NetFlow v9 | [[artigo_026]] (*NFStream: A flexible network data analysis framework*); [[artigo_027]] (*NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*); [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) |
| **EXPERIMENTO** | Benchmark em conjuntos modernos de tráfego de rede (CIC-IDS-2017 e CICIoT2023) | [[artigo_009]] (*CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*); [[artigo_041]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*) |
| **RESULTADO** | Classificadores operam com alta acurácia sem acesso a texto claro de payload | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*); [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) |
| **LIMITAÇÃO** | Cegueira a ataques que dependem exclusivamente de semântica textual profunda de aplicação | [[artigo_043]] (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*); [[artigo_046]] (*Web Attacks Analysis and Mitigation Techniques*) |
| **LACUNA** | Necessidade de correlacionar fluxos com telemetria de host e grafos de conhecimento CTI | [[artigo_035]] (*TRACE: Timely Retrieval and Alignment for Cybersecurity Knowledge Graph Construction and Expansion*); [[artigo_038]] (*The Procedural Semantics Gap in Structured CTI: A Measurement-Driven STIX Analysis for APT Emulation*) |

---

### Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado ^Cadeia_2_Mixture_of_Experts
> Esta cadeia mapeia a fundamentação teórica de por que classificadores homogêneos monolíticos falham em tráfego multimodal (interferência de gradientes) e como o ALF-MoE introduz 5 especialistas desacoplados com fusão atencional calibrada por transformações afins.

| Etapa Epistemológica | Descrição | Artigos Vinculados |
| :--- | :--- | :--- |
| **CONCEITO** | Heterogeneidade intrínseca do tráfego malicioso em múltiplos domínios | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*); [[artigo_025]] (*One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*) |
| **FUNDAMENTAÇÃO** | Falha de modelos monolíticos ('One-for-All') por interferência negativa de gradientes | [[artigo_025]] (*One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*); [[artigo_044]] (*TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*) |
| **MÉTODO** | Arquitetura ALF-MoE com 5 especialistas (DNN, CNN, GRU, CAE, LSTM) e fusão aprendível calibrada | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*); [[artigo_001]] (*On Calibration of Modern Neural Networks*) |
| **EXPERIMENTO** | Avaliação comparativa contra votação majoritária, média ponderada e modelos isolados | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) |
| **RESULTADO** | Ganhos de até 8.4% em macro F1-score e acurácia superior a 98.7% | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) |
| **LIMITAÇÃO** | Custo computacional de treinamento simultâneo das 5 redes profundas | [[artigo_004]] (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) |
| **LACUNA** | Otimização de inferência de MoE via quantização INT8 e aceleração em hardware P4 | [[artigo_030]] (*P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*); [[artigo_048]] (*A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*) |

---

### Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split ^Cadeia_3_Metodologia_de_Avaliacao
> Esta cadeia documenta a denúncia metodológica do vazamento temporal em validação cruzada clássica (random split), demonstrando a inflação artificial de métricas e consolidando o particionamento temporal cronológico como exigência científica incontornável.

| Etapa Epistemológica | Descrição | Artigos Vinculados |
| :--- | :--- | :--- |
| **CONCEITO** | Validação científica fidedigna de sistemas NIDS | [[artigo_006]] (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*); [[artigo_041]] (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*) |
| **FUNDAMENTAÇÃO** | Teoria de contaminação e vazamento temporal (Data Leakage) em séries de tráfego | [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) |
| **MÉTODO** | Particionamento cronológico estrito (Temporal Split) e métricas balanceadas (Macro F1) | [[artigo_006]] (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*); [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) |
| **EXPERIMENTO** | Comparação entre k-fold randômico vs divisão temporal cronológica em bases NetFlow | [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) |
| **RESULTADO** | Demonstração de que random split inflaciona artificialmente métricas em até 20% | [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) |
| **LIMITAÇÃO** | Queda perceptível de desempenho sob evolução natural de tráfego (concept drift) | [[artigo_036]] (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) |
| **LACUNA** | Mecanismos de aprendizado contínuo adaptativo para NIDS em produção | [[artigo_002]] (*Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection*); [[artigo_032]] (*Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE)*) |

---

## Clusters de Datasets de Benchmark ^clusters-datasets
> Agrupamento dos artigos conforme as bases de tráfego analisadas:

### Benchmark: CIC-IDS-2017 ^dataset-cic-ids-2017
> **Total de Artigos Associados:** 17

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_006]] (2025) — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- [[artigo_013]] (2023) — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
- [[artigo_015]] (2025) — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
- [[artigo_019]] (2025) — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
- [[artigo_021]] (2025) — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
- [[artigo_023]] (2026) — *Machine Learning for Network Attacks Classification and Statistical Evaluation of Adversarial Learning Methodologies for Synthetic Data Generation*
- [[artigo_027]] (2021) — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- [[artigo_030]] (2025) — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
- [[artigo_033]] (2022) — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
- [[artigo_034]] (2023) — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
- [[artigo_036]] (2025) — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- [[artigo_040]] (2026) — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- [[artigo_041]] (2018) — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- [[artigo_042]] (2018) — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (Duplicate Copy)*
- [[artigo_043]] (2022) — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- [[artigo_048]] (2024) — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*

### Benchmark: CSE-CIC-IDS2018 ^dataset-cse-cic-ids2018
> **Total de Artigos Associados:** 4

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_006]] (2025) — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- [[artigo_011]] (2025) — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
- [[artigo_021]] (2025) — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*

### Benchmark: CICIoT2023 ^dataset-ciciot2023
> **Total de Artigos Associados:** 5

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_007]] (2026) — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
- [[artigo_008]] (2025) — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
- [[artigo_009]] (2023) — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- [[artigo_017]] (2025) — *Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems*

### Benchmark: UNSW-NB15 ^dataset-unsw-nb15
> **Total de Artigos Associados:** 9

- [[artigo_006]] (2025) — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- [[artigo_019]] (2025) — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
- [[artigo_021]] (2025) — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
- [[artigo_023]] (2026) — *Machine Learning for Network Attacks Classification and Statistical Evaluation of Adversarial Learning Methodologies for Synthetic Data Generation*
- [[artigo_027]] (2021) — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- [[artigo_028]] (2023) — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
- [[artigo_036]] (2025) — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- [[artigo_043]] (2022) — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- [[artigo_047]] (2022) — *Network Intrusion Detection Model Based on CNN and GRU*

### Benchmark: UGR'16 ^dataset-ugr-16
> **Total de Artigos Associados:** 2

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_045]] (2018) — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*

### Benchmark: Car-Hacking (CAN) ^dataset-car-hacking-can
> **Total de Artigos Associados:** 2

- [[artigo_010]] (2026) — *DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles*
- [[artigo_014]] (2025) — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning*

---

## Clusters de Arquiteturas Neurais e Modelos ^clusters-arquiteturas
> Agrupamento dos artigos conforme a família arquitetural investigada:

### Arquitetura: Mixture of Experts ^arch-mixture-of-experts
> **Total de Artigos Associados:** 3

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_025]] (2025) — *One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*
- [[artigo_044]] (2026) — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*

### Arquitetura: Recorrentes GRU LSTM ^arch-recorrentes-gru-lstm
> **Total de Artigos Associados:** 9

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_007]] (2026) — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
- [[artigo_008]] (2025) — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
- [[artigo_011]] (2025) — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
- [[artigo_015]] (2025) — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
- [[artigo_028]] (2023) — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
- [[artigo_034]] (2023) — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
- [[artigo_040]] (2026) — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- [[artigo_047]] (2022) — *Network Intrusion Detection Model Based on CNN and GRU*

### Arquitetura: Autoencoders ^arch-autoencoders
> **Total de Artigos Associados:** 3

- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- [[artigo_021]] (2025) — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
- [[artigo_048]] (2024) — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*

### Arquitetura: Calibracao Probabilistica ^arch-calibracao-probabilistica
> **Total de Artigos Associados:** 2

- [[artigo_001]] (2017) — *On Calibration of Modern Neural Networks*
- [[artigo_004]] (2026) — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*

### Arquitetura: Plano de Dados P4 SDN ^arch-plano-de-dados-p4-sdn
> **Total de Artigos Associados:** 2

- [[artigo_030]] (2025) — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
- [[artigo_033]] (2022) — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*

### Arquitetura: State Space Models ^arch-state-space-models
> **Total de Artigos Associados:** 1

- [[artigo_024]] (2024) — *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*

---

## 🧭 Navegação
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
