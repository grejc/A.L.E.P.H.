---
id: artigo_006
title: 'Advanced IDS: a comparative study of datasets and machine learning algorithms
  for network flow-based intrusion detection systems'
authors:
- José Carlos Mondragón Guadarrama
- Paula Branco
- Guy-Vincent Jourdan
- Andres Eduardo Gutierrez-Rodriguez
- Rajesh Roshan Biswal
year: 2025
bibtex_key: advancedids2024
doi: 10.1007/s10489-025-06422-4
venue: Applied Intelligence (2025) 55:608
keywords:
- Network Intrusion Detection
- Flow-based NIDS
- Machine Learning
- Datasets Comparison
- CIC-IDS2017
- CSE-CIC-IDS2018
- Data Leakage
area: Network Intrusion Detection / Comparative Benchmark / Evaluation Methodology
datasets:
- CIC-IDS-2017
- CSE-CIC-IDS2018
- UNSW-NB15
- ISCX-IDS2012
models:
- Random Forest (RF)
- Decision Tree (DT)
- k-Nearest Neighbors (kNN)
- Multi-Layer Perceptron (MLP)
- Support Vector Machines (SVM)
- XGBoost
aliases:
- 'Advanced IDS: a comparative study of datasets and machine learning algorithms for
  network flow-based intrusion detection systems'
- advancedids2024
- artigo_006
tags:
- bibliografia
- alf-moe
- artigo
---

# Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems

> **Citação ABNT Sugerida:** GUADARRAMA, J. C. M.; BRANCO, P.; JOURDAN, G.; GUTIERREZ-RODRIGUEZ, A. E.; BISWAL, R. R.. Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems. In: **Applied Intelligence (2025) 55:608**, 2025.
> **Chave BibTeX:** `advancedids2024` | **Arquivo TXT:** `Advanced_IDS_a_comparative_study_of_datasets_and_m.txt` | **DOI:** `10.1007/s10489-025-06422-4`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_006` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Intrusion Detection / Comparative Benchmark / Evaluation Methodology |
| **Veículo de Publicação** | Applied Intelligence (2025) 55:608 |
| **Datasets Utilizados** | CIC-IDS-2017, CSE-CIC-IDS2018, UNSW-NB15, ISCX-IDS2012 |
| **Modelos / Algoritmos** | Random Forest (RF), Decision Tree (DT), k-Nearest Neighbors (kNN), Multi-Layer Perceptron (MLP), Support Vector Machines (SVM), XGBoost |
| **Palavras-Chave** | Network Intrusion Detection, Flow-based NIDS, Machine Learning, Datasets Comparison, CIC-IDS2017, CSE-CIC-IDS2018, Data Leakage |

## 🎯 Problema Abordado
Falta de rigor metodológico e comparação consistente entre datasets modernos baseados em fluxos de rede e algoritmos de ML/DL para NIDS; existência de vícios de avaliação, classes severamente desbalanceadas e falhas em estratégias de particionamento de dados.

## 🔬 Metodologia
Estudo comparativo experimental sistemático avaliando múltiplos algoritmos de aprendizado de máquina supervisionado em múltiplos datasets públicos de tráfego de rede sob pré-processamento controlado, análise de desbalanceamento e métricas de desempenho robustas (F1-macro, G-mean, balanceamento de precisão/recall).

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Modelos ensemble baseados em árvores e redes neurais profundas obtêm os melhores resultados gerais, mas o desempenho decai acentuadamente em classes raras de ataque; o particionamento inadequado induz superestimação artificial de acurácia; pré-processamento de atributos de fluxo é determinante.

**Contribuições Centrais:**
- Framework comparativo unificado para avaliação de datasets de NIDS baseados em fluxo.
- Quantificação do impacto do desbalanceamento severo de classes sobre classificadores de rede.
- Diretrizes metodológicas para evitar viés de avaliação na literatura de cibersegurança.

## ⚠️ Limitações Identificadas
Muitos datasets públicos apresentam erros de rotulagem, fluxos duplicados e tráfego que não reflete a diversidade do tráfego corporativo moderno em tempo real.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Flow-based NIDS`, `Evaluation Benchmark`, `Dataset Comparison`, `Imbalance Problem`
- **Problemas Focais:** `Inconsistências em datasets de NIDS`, `Avaliação enviesada por acurácia global`, `Data leakage em particionamento`
- **Métodos Empregados:** `Padronização de pré-processamento`, `Avaliação com F1-macro e G-mean`, `Análise de sensibilidade a desbalanceamento`
- **Modelos e Arquiteturas:** `Random Forest`, `MLP`, `XGBoost`, `kNN`
- **Bases de Dados:** `CIC-IDS-2017`, `CSE-CIC-IDS2018`, `UNSW-NB15`
- **Resultados Chave:** `Ensembles e redes neurais lideram, mas sofrem em classes minoritárias sem tratamento adequado`
- **Limitações Reconhecidas:** `Imperfeições intrínsecas aos datasets sintéticos gerados em laboratório`
- **Evidências Citáveis:** `EVID_006_01`, `EVID_006_02`, `EVID_006_03`, `EVID_006_04`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Relacionado:**
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_002]] — *Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection*
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
  - [[artigo_020]] — *Feature Classification and Outlier Detection to Increased Accuracy in Intrusion Detection System*
  - [[artigo_023]] — *Machine Learning for Network Attacks Classification and Statistical Evaluation of Adversarial Learning Methodologies for Synthetic Data Generation*
- **Compara:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Utiliza Dataset:**
  - [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
- **Critica Metodologia:**
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_006]]` $\xrightarrow{\text{critica_e_sanitiza}}$ `[[artigo_041]]` (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*): Guadarrama et al. analisam criticamente inconsistências e redundâncias do CIC-IDS-2017.
- `[[artigo_036]]` (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*) $\xrightarrow{\text{estende_critica}}$ `[[artigo_006]]`: Luay et al. comprovam que avaliações com random split inflacionam métricas reportadas na literatura de NIDS.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — 🌟 **Definição Canônica**
- [[Conceitos/Data Leakage e Split Temporal|Data Leakage Temporal e Particionamento Estrito]] — Papel: Análise crítica de métodos de particionamento
- [[Conceitos/CIC-IDS-2017 Dataset|Dataset Benchmark CIC-IDS-2017]] — Papel: Estudo comparativo e sanitização do CIC-IDS-2017

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_001 — Categoria: Teoria|CLAIM_001 (Teoria)]] — *"A adoção generalizada de mecanismos de criptografia ponta a ponta (como TLS 1.3, HTTPS e DoH) tornou a carga útil (payload) dos pacotes opaca aos dispositivos intermediários, debilitando a viabilidade de NIDS legados baseados em inspeção profunda de pacotes (DPI) e assinaturas estáticas."*
  - *Aplicação na Tese:* Fundamenta a transição de DPI para NIDS baseado em fluxos.
- [[Afirmacoes_e_Claims#CLAIM_006 — Categoria: Metodologia|CLAIM_006 (Metodologia)]] — *"O particionamento randômico de dados (random split / k-fold) em datasets de NIDS baseados em fluxo induz grave contaminação temporal (data leakage) e superestimação irrealista de acurácia, sendo mandatório o particionamento puramente cronológico (temporal split) para avaliação científica rigorosa."*
  - *Aplicação na Tese:* Reforça o rigor metodológico na divisão de dados.
- [[Afirmacoes_e_Claims#CLAIM_008 — Categoria: Metodologia|CLAIM_008 (Metodologia)]] — *"A acurácia global é uma métrica enganosa para avaliação de NIDS em redes contemporâneas devido ao desbalanceamento severo de classes, sendo mandatório o uso de F1-macro e métricas balanceadas por classe."*
  - *Aplicação na Tese:* Justifica as métricas primárias de avaliação no Capítulo 3 e Capítulo 5.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito|CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito]]
  - **Posição A (Visão Convencional):** *"O particionamento aleatório k-fold (random split) é amplamente aceito e padrão em benchmarks de NIDS para avaliação de classificadores de tráfego de rede."*
- [[Contradicoes_e_Divergencias#CONTROV_002 — Inspeção de Tráfego Criptografado: DPI de Payload vs. Metadados de Fluxo (Flow-based / NetFlow)|CONTROV_002 — Inspeção de Tráfego Criptografado: DPI de Payload vs. Metadados de Fluxo (Flow-based / NetFlow)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"A adoção universal de criptografia ponta a ponta (TLS 1.3, HTTPS, DoH) torna a carga útil inteiramente opaca a intermediários, tornando o DPI tecnicamente ineficaz e forçando a migração para análise comportamental de metadados agregados de fluxo."*
- [[Contradicoes_e_Divergencias#CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)|CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"O CIC-IDS-2017 bruto possui dezenas de milhares de fluxos duplicados, valores infinitos/ausentes e artefatos de captura que distorcem severamente a avaliação dos algoritmos caso não passem por higienização e sanitização estatística rigorosa."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa FUNDAMENTAÇÃO:** Ineficácia de DPI e necessidade de inspeção baseada em metadados de fluxo
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa CONCEITO:** Validação científica fidedigna de sistemas NIDS
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa MÉTODO:** Particionamento cronológico estrito (Temporal Split) e métricas balanceadas (Macro F1)

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: CSE-CIC-IDS2018|CSE-CIC-IDS2018]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_006_01` — DEFINIÇÃO
> [!quote] EVID_006_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição de NIDS baseados em fluxo de rede e por que eles substituem a inspeção profunda de pacotes (DPI).
> **Localização:** Seção 1 (Introduction) e Seção 2 (Background), Páginas 1-3
>
> *"Flow-based NIDS analyze statistical and temporal properties aggregated over network connections (flows) rather than inspecting raw payload, enabling scalability and compliance with pervasive end-to-end encryption."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta para embasar a definição e necessidade de NIDS baseados em fluxo no Capítulo 1 e Capítulo 2 da tese.

### `EVID_006_02` — COMPARATIVA
> [!quote] EVID_006_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Acurácia global é uma métrica enganosa em NIDS devido ao desbalanceamento extremo entre tráfego benigno e ataques raros.
> **Localização:** Seção 5 (Performance Evaluation Metrics), Página 9
>
> *"Overall accuracy is misleading in intrusion detection because benign flows typically represent over 80-99% of total traffic. A naive classifier predicting always benign achieves high accuracy while failing to detect critical intrusions. Macro-averaged F1-score is essential."*
>
> **Aplicabilidade na Tese ALF-MoE:** Justifica a adoção obrigatória de F1-macro e métricas balanceadas por classe na avaliação experimental do ALF-MoE.

### `EVID_006_03` — LIMITAÇÃO
> [!quote] EVID_006_03 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Datasets populares de NIDS sofrem com artefatos de captura, desbalanceamento severo e redundância de registros.
> **Localização:** Seção 4 (Datasets Characteristics and Flaws), Páginas 6-8
>
> *"Widely used benchmark datasets including CIC-IDS-2017 contain substantial duplicate records, missing values, and skewed class distributions that distort machine learning evaluation unless rigorously sanitized."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a necessidade de sanitização, remoção de duplicatas e pré-processamento rigoroso no Capítulo 3 (Metodologia).

### `EVID_006_04` — LIMITAÇÃO
> [!quote] EVID_006_04 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Limitações de métodos tradicionais de detecção de intrusão baseados em regras e assinaturas fixas frente a ataques desconhecidos, variantes de dia zero e tráfego cifrado.
> **Localização:** Seção 2 (Background and Motivation), Páginas 2-4
>
> *"Signature-based intrusion detection systems rely on predefined patterns and struggle with novel zero-day attacks and polymorphic threats. Moreover, widespread encryption hinders payload inspection, demanding automated machine learning and flow-level behavioral modeling."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a motivação no Capítulo 1 para superação de IDSs tradicionais baseados em assinatura.

## 📦 Entrada BibTeX
```bibtex
@article{advancedids2024,
  title = {Advanced {IDS}: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems},
  author = {Guadarrama, José Carlos Mondragón and Branco, Paula and Jourdan, Guy-Vincent and Gutierrez-Rodriguez, Andres Eduardo and Biswal, Rajesh Roshan},
  journal = {Applied Intelligence},
  year = {2025},
  doi = {10.1007/s10489-025-06422-4}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
