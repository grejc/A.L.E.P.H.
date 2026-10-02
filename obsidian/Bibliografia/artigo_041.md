---
id: artigo_041
title: Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization
authors:
- Iman Sharafaldin
- Arash Habibi Lashkari
- Ali A. Ghorbani
year: 2018
bibtex_key: Sharafaldin2018TowardGA
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Proceedings of the 4th International Conference on Information Systems Security
  and Privacy (ICISSP 2018), pp. 108-116
keywords:
- CIC-IDS-2017
- Intrusion Detection Dataset
- Dataset Evaluation Criteria
- Traffic Characterization
- Network Attacks
- B-Profile
- M-Profile
area: Network Security / Datasets Creation / Traffic Characterization
datasets:
- CIC-IDS-2017 (proposto)
- KDD Cup 99
- NSL-KDD
- UNSW-NB15 (comparativos)
models:
- CICFlowMeter
- Random Forest
- k-Nearest Neighbors (kNN)
- Multi-Layer Perceptron (MLP)
- Naïve Bayes
- Support Vector Machines (SVM)
aliases:
- Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization
- Sharafaldin2018TowardGA
- artigo_041
tags:
- bibliografia
- alf-moe
- artigo
---

# Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization

> **Citação ABNT Sugerida:** SHARAFALDIN, I.; LASHKARI, A. H.; GHORBANI, A. A.. Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. In: **Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP 2018), pp. 108-116**, 2018.
> **Chave BibTeX:** `Sharafaldin2018TowardGA` | **Arquivo TXT:** `Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_041` |
| **Ano** | 2018 |
| **Área de Pesquisa** | Network Security / Datasets Creation / Traffic Characterization |
| **Veículo de Publicação** | Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP 2018), pp. 108-116 |
| **Datasets Utilizados** | CIC-IDS-2017 (proposto), KDD Cup 99, NSL-KDD, UNSW-NB15 (comparativos) |
| **Modelos / Algoritmos** | CICFlowMeter, Random Forest, k-Nearest Neighbors (kNN), Multi-Layer Perceptron (MLP), Naïve Bayes, Support Vector Machines (SVM) |
| **Palavras-Chave** | CIC-IDS-2017, Intrusion Detection Dataset, Dataset Evaluation Criteria, Traffic Characterization, Network Attacks, B-Profile, M-Profile |

## 🎯 Problema Abordado
Datasets históricos de NIDS (como DARPA98 e KDD Cup 99) são gravemente defasados, redundantes e carecem de tráfego de rede contemporâneo e ataques modernos; inexistência de critérios formais estabelecidos para validar a representatividade de novos datasets de segurança.

## 🔬 Metodologia
Definição de 11 critérios fundamentais para geração de datasets válidos de IDS (Complete Network Configuration, Complete Traffic, Labeled Flows, Complete Interaction, Capture Complete, Diverse Protocols, Attack Diversity, Anonymity, Heterogeneity, Feature Set, Metadata); geração do dataset benchmark CIC-IDS-2017 utilizando perfis comportamentais humanos (B-Profiles) e perfis de ataque automatizados (M-Profiles) em topologia física e virtual.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Disponibilização pública do dataset CIC-IDS-2017 cobrindo 5 dias de tráfego com mais de 2.8 milhões de fluxos e 14 classes de ataque contemporâneas (Brute Force SSH/FTP, DoS, DDoS, Heartbleed, Web Attacks, Infiltration, Botnet); extração de 84 atributos de fluxo via CICFlowMeter.

**Contribuições Centrais:**
- Estabelecimento dos 11 critérios canônicos para avaliação de datasets de NIDS.
- Criação e publicação do dataset amplamente utilizado CIC-IDS-2017.
- Modelagem comportamental de tráfego benigno via perfis estatísticos (B-Profile).

## ⚠️ Limitações Identificadas
Erros na ordenação de pacotes no extrator CICFlowMeter original resultando em valores negativos de IAT e fluxos redundantes (documentados posteriormente pela comunidade acadêmica).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CIC-IDS-2017`, `Critérios para Datasets Válidos`, `Caracterização de Tráfego`, `B-Profile e M-Profile`
- **Problemas Focais:** `Obsolescência dos datasets KDD/DARPA`, `Falta de critérios formais de representatividade`
- **Métodos Empregados:** `11 critérios de validação`, `Simulação de usuários reais (B-Profiles)`, `Injeção controlada de 14 ataques`, `CICFlowMeter`
- **Modelos e Arquiteturas:** `Random Forest`, `kNN`, `MLP`, `SVM`
- **Bases de Dados:** `CIC-IDS-2017`
- **Resultados Chave:** `Dataset de referência mundial com 2.8M fluxos e 84 atributos`
- **Limitações Reconhecidas:** `Inconsistências pontuais de implementação no extrator de fluxo original`
- **Evidências Citáveis:** `EVID_041_01`, `EVID_041_02`, `EVID_041_03`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Cria Dataset Utilizado Por:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_019]] — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
  - [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Duplicado Em:**
  - [[artigo_042]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (Duplicate Copy)*

### Citações e Relações Recebidas na Base (Incoming)
- **Avalia Dataset:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_019]] — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
  - [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Comparado Com:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Relacionado:**
  - [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
  - [[artigo_023]] — *Machine Learning for Network Attacks Classification and Statistical Evaluation of Adversarial Learning Methodologies for Synthetic Data Generation*
- **Compara Com:**
  - [[artigo_017]] — *Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems*
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*
- **Padroniza Dataset:**
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- **Critica Metodologia:**
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- **Duplicata Exata De:**
  - [[artigo_042]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (Duplicate Copy)*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{avalia_dataset}}$ `[[artigo_041]]`: Avalia o ALF-MoE no dataset canônico CIC-IDS-2017.
- `[[artigo_006]]` (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*) $\xrightarrow{\text{critica_e_sanitiza}}$ `[[artigo_041]]`: Guadarrama et al. analisam criticamente inconsistências e redundâncias do CIC-IDS-2017.
- `[[artigo_042]]` (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization (Duplicate Copy)*) $\xrightarrow{\text{duplicata_exata}}$ `[[artigo_041]]`: artigo_042 é idêntico byte a byte ao artigo_041 (Toward Generating a New Intrusion Detection Dataset...).

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Dataset benchmark CIC-IDS-2017 para NIDS
- [[Conceitos/CIC-IDS-2017 Dataset|Dataset Benchmark CIC-IDS-2017]] — 🌟 **Definição Canônica**

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito|CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito]]
  - **Posição A (Visão Convencional):** *"O particionamento aleatório k-fold (random split) é amplamente aceito e padrão em benchmarks de NIDS para avaliação de classificadores de tráfego de rede."*
- [[Contradicoes_e_Divergencias#CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)|CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)]]
  - **Posição A (Visão Convencional):** *"O dataset público CIC-IDS-2017 reflete fielmente o tráfego corporativo moderno e pode ser utilizado diretamente para treinamento de modelos de aprendizado de máquina."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa EXPERIMENTO:** Benchmark em conjuntos modernos de tráfego de rede (CIC-IDS-2017 e CICIoT2023)
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa CONCEITO:** Validação científica fidedigna de sistemas NIDS

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_041_01` — DEFINIÇÃO
> [!quote] EVID_041_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição dos 11 critérios necessários para que um conjunto de dados de detecção de intrusão seja considerado válido e representativo.
> **Localização:** Seção 2 (Eleven Criteria for a Valid Dataset), Páginas 109-111
>
> *"A valid intrusion detection dataset must satisfy eleven fundamental criteria: Complete Network Configuration, Complete Traffic, Labeled Flows, Complete Interaction, Capture Complete, Diverse Protocols, Attack Diversity, Anonymity, Heterogeneity, Feature Set, and Metadata."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a discussão metodológica sobre seleção de datasets e requisitos de representatividade no Capítulo 2 e Capítulo 3.

### `EVID_041_02` — ESTADO DA ARTE
> [!quote] EVID_041_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O dataset CIC-IDS-2017 foi concebido para capturar tráfego de rede moderno e 14 classes de ataque contemporâneas refletindo redes corporativas reais.
> **Localização:** Seção 4 (Attack Scenarios and Profiles), Páginas 112-114
>
> *"CIC-IDS-2017 covers modern attack profiles including Brute Force, Heartbleed, Botnet, DoS, DDoS, Web Attacks, and Infiltration, extracted across five continuous days of network interaction."*
>
> **Aplicabilidade na Tese ALF-MoE:** Artigo primário de citação obrigatória ao apresentar o benchmark CIC-IDS-2017 utilizado nos experimentos da tese.

### `EVID_041_03` — METODOLÓGICA
> [!quote] EVID_041_03 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** O uso de perfis comportamentais (B-Profiles) gera tráfego de fundo realista para evitar que algoritmos de ML identifiquem ataques apenas por anomalias sintéticas simples.
> **Localização:** Seção 3 (Generating the Dataset), Páginas 111-112
>
> *"B-Profiles model real human behavioral patterns across HTTP, HTTPS, FTP, SSH, and email protocols, preventing machine learning models from exploiting trivial artificial artifacts."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a legitimidade do tráfego benigno no treinamento dos classificadores.

## 📦 Entrada BibTeX
```bibtex
@inproceedings{Sharafaldin2018TowardGA,
  title={Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization},
  author={Iman Sharafaldin and Arash Habibi Lashkari and Ali A. Ghorbani},
  booktitle={International Conference on Information Systems Security and Privacy},
  year={2018},
  url={https://api.semanticscholar.org/CorpusID:4707749}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
