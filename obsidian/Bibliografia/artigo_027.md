---
id: artigo_027
title: NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems
authors:
- Mohanad Sarhan
- Siamak Layeghy
- Nour Moustafa
- Marius Portmann
year: 2021
bibtex_key: netflow2020
doi: 10.1007/978-3-030-72802-1_9
venue: Lecture Notes of the Institute for Computer Sciences, Social Informatics and
  Telecommunications Engineering (LNICST), Vol. 370, pp. 117-135
keywords:
- NetFlow
- IPFIX
- Intrusion Detection Systems
- Machine Learning
- Standard Datasets
- CIC-IDS2017
- UNSW-NB15
- NetFlow v9
area: Network Security / Datasets Standardization / NetFlow / IPFIX
datasets:
- CIC-IDS-2017
- UNSW-NB15
- BoT-IoT
- ToN-IoT (todos convertidos para NetFlow-v9)
models:
- Decision Tree
- Random Forest
- Logistic Regression
- Naive Bayes
- Deep Feedforward Neural Networks
aliases:
- NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems
- netflow2020
- artigo_027
tags:
- bibliografia
- alf-moe
- artigo
---

# NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems

> **Citação ABNT Sugerida:** SARHAN, M.; LAYEGHY, S.; MOUSTAFA, N.; PORTMANN, M.. NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems. In: **Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering (LNICST), Vol. 370, pp. 117-135**, 2021.
> **Chave BibTeX:** `netflow2020` | **Arquivo TXT:** `NetFlow_Datasets_for_Machine_Learning-based_Network_Intrusion_Detection_Systems_2020.txt` | **DOI:** `10.1007/978-3-030-72802-1_9`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_027` |
| **Ano** | 2021 |
| **Área de Pesquisa** | Network Security / Datasets Standardization / NetFlow / IPFIX |
| **Veículo de Publicação** | Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering (LNICST), Vol. 370, pp. 117-135 |
| **Datasets Utilizados** | CIC-IDS-2017, UNSW-NB15, BoT-IoT, ToN-IoT (todos convertidos para NetFlow-v9) |
| **Modelos / Algoritmos** | Decision Tree, Random Forest, Logistic Regression, Naive Bayes, Deep Feedforward Neural Networks |
| **Palavras-Chave** | NetFlow, IPFIX, Intrusion Detection Systems, Machine Learning, Standard Datasets, CIC-IDS2017, UNSW-NB15, NetFlow v9 |

## 🎯 Problema Abordado
Datasets populares de NIDS são publicados em formatos proprietários amplamente divergentes e incompatíveis entre si (ex: formatos do CICFlowMeter vs formatos específicos do UNSW-NB15), inviabilizando transfer learning e treinamento cruzado entre bases.

## 🔬 Metodologia
Conversão sistemática e padronização de múltiplos conjuntos de dados de NIDS (CIC-IDS-2017, UNSW-NB15, BoT-IoT, ToN-IoT) para o padrão industrial NetFlow v9 / IPFIX com 43 atributos padronizados utilizando a ferramenta nfdump e geradores de fluxo conformes com RFC.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Os novos datasets NetFlow mantêm a capacidade discriminatória dos conjuntos originais enquanto reduzem drasticamente a complexidade de engenharia de atributos e viabilizam benchmarks comparativos justos sob o mesmo espaço amostral.

**Contribuições Centrais:**
- Criação e disponibilização de versões NetFlow padronizadas dos 4 maiores datasets públicos de NIDS.
- Benchmark cruzado comparando desempenho sob representação unificada de atributos.
- Adesão a padrões abertos da IETF (NetFlow/IPFIX) para aproximação com roteadores industriais.

## ⚠️ Limitações Identificadas
A perda de campos específicos de carga útil (payload) ou contadores proprietários de L7 presentes em ferramentas especializadas como o CICFlowMeter.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `NetFlow Datasets`, `Padronização NetFlow v9`, `IPFIX`, `Interoperabilidade Cross-Dataset`
- **Problemas Focais:** `Incompatibilidade entre formatos de datasets de NIDS`, `Inviabilidade de generalização entre bases`
- **Métodos Empregados:** `Conversão padronizada para 43 atributos NetFlow v9`, `Uso de nfdump`, `Benchmarking supervisionado cruzado`
- **Modelos e Arquiteturas:** `Random Forest`, `Decision Tree`, `DNN`
- **Bases de Dados:** `NetFlow-CIC-IDS2017`, `NetFlow-UNSW-NB15`, `NetFlow-BoT-IoT`
- **Resultados Chave:** `Preservação de acurácia com formato industrial leve e interoperável`
- **Limitações Reconhecidas:** `Omissão de atributos L7 proprietários`
- **Evidências Citáveis:** `EVID_027_01`, `EVID_027_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Padroniza Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- **Estende:**
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- **Fundamenta Metodologia:**
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*

### Arestas no Grafo da Literatura
- `[[artigo_040]]` (*Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*) $\xrightarrow{\text{estende_representacao}}$ `[[artigo_027]]`: Luay et al. estendem o formato NetFlow padronizado por Sarhan et al. adicionando atributos temporais de IAT.
- `[[artigo_043]]` (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*) $\xrightarrow{\text{consolida_padrao}}$ `[[artigo_027]]`: Sarhan et al. consolidam o conjunto padronizado NetFlow de 43 atributos para interoperabilidade cross-dataset.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Datasets padronizados de NetFlow para NIDS
- [[Conceitos/NetFlow e Padronizacao de Atributos|NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos]] — 🌟 **Definição Canônica**

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa MÉTODO:** Extração e agregação de fluxos bidirecionais padronizados via NFStream e NetFlow v9

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_027_01` — DEFINIÇÃO
> [!quote] EVID_027_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição do formato NetFlow v9 / IPFIX como padrão industrial para exportação e análise de tráfego de rede.
> **Localização:** Seção 2 (NetFlow Protocol Overview), Páginas 119-121
>
> *"NetFlow is an industry-standard network protocol developed by Cisco for collecting IP operational traffic metadata, exporting structured records containing packet counts, byte volumes, interface identifiers, and temporal durations without exposing payload contents."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a definição e a relevância de NetFlow no Capítulo 1 e Capítulo 2 da tese.

### `EVID_027_02` — ESTADO DA ARTE
> [!quote] EVID_027_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A conversão de datasets heterogêneos para representações de NetFlow permite interoperabilidade e treinamento de modelos transferíveis para roteadores reais.
> **Localização:** Seção 1 (Introduction) e Seção 5 (Benchmark Evaluation), Páginas 117-130
>
> *"By standardizing heterogeneous intrusion datasets into uniform NetFlow format, machine learning classifiers can be evaluated consistently and directly deployed onto real-world network routing infrastructure supporting IPFIX."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a decisão de utilizar atributos agregados no estilo NetFlow e conjuntos de atributos padronizados na metodologia da tese.

## 📦 Entrada BibTeX
```bibtex
@article{netflow2020,
  title = {NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems},
  author = {Sarhan, Mohanad and Layeghy, Siamak and Moustafa, Nour and Portmann, Marius},
  journal = {Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering},
  year = {2021},
  doi = {10.1007/978-3-030-72802-1_9},
  pages = {117-135},
  publisher = {Springer International Publishing}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
