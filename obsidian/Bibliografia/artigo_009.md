---
id: artigo_009
title: 'CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT
  Environment'
authors:
- Euclides Carlos Pinto Neto
- Sajjad Dadkhah
- Raphael Ferreira
- Alireza Zohourian
- Rongxing Lu
- Ali A. Ghorbani
year: 2023
bibtex_key: ciciot2023
doi: 10.3390/s23135941
venue: Sensors 2023, 23(13), 5941
keywords:
- CICIoT2023
- IoT Dataset
- DDoS Attacks
- DoS Attacks
- Benchmark
- Network Intrusion Detection
- Real-Time Topology
area: Cybersecurity Datasets / Internet of Things / Attack Benchmarking
datasets:
- CICIoT2023 (proposto)
- CIC-IDS-2017 (comparativo)
models:
- Random Forest
- Adaboost
- Decision Tree
- Perceptron
- Logistic Regression
- MLP
- Deep Neural Networks (DNN)
aliases:
- 'CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment'
- ciciot2023
- artigo_009
tags:
- bibliografia
- alf-moe
- artigo
---

# CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment

> **Citação ABNT Sugerida:** NETO, E. C. P.; DADKHAH, S.; FERREIRA, R.; ZOHOURIAN, A.; LU, R.; GHORBANI, A. A.. CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment. In: **Sensors 2023, 23(13), 5941**, 2023.
> **Chave BibTeX:** `ciciot2023` | **Arquivo TXT:** `CICIoT2023_A_Real-Time_Dataset_and_Benchmark_for_Large-Scale_Attacks_in_IoT_Environment.txt` | **DOI:** `10.3390/s23135941`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_009` |
| **Ano** | 2023 |
| **Área de Pesquisa** | Cybersecurity Datasets / Internet of Things / Attack Benchmarking |
| **Veículo de Publicação** | Sensors 2023, 23(13), 5941 |
| **Datasets Utilizados** | CICIoT2023 (proposto), CIC-IDS-2017 (comparativo) |
| **Modelos / Algoritmos** | Random Forest, Adaboost, Decision Tree, Perceptron, Logistic Regression, MLP, Deep Neural Networks (DNN) |
| **Palavras-Chave** | CICIoT2023, IoT Dataset, DDoS Attacks, DoS Attacks, Benchmark, Network Intrusion Detection, Real-Time Topology |

## 🎯 Problema Abordado
A maioria dos datasets existentes para NIDS baseia-se em redes corporativas tradicionais ou topologias puramente simuladas que não refletem a diversidade de dispositivos de hardware IoT e a escala massiva dos ataques modernos (especialmente botnets e ataques volumétricos distribuídos).

## 🔬 Metodologia
Implementação de um laboratório físico com 105 dispositivos IoT reais (sensores inteligentes, câmeras IP, smart plugs, hubs residenciais e industriais), gerando tráfego sob 33 classes de ataques organizadas em 7 categorias principais (DDoS, DoS, Reconhecimento, Web, Brute Force, Spoofing e Mirai); extração padronizada de 46 atributos estatísticos e temporais de fluxo.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O dataset fornece mais de 46 milhões de fluxos rotulados; benchmarks de aprendizado supervisionado mostram alta detecção binária (acurácia > 99%), mas identificação multiclasse detalhada de variantes de DDoS (SYN Flood, UDP Flood, ICMP Flood, Slowloris) requer classificadores mais sofisticados devido à sobreposição de distribuições.

**Contribuições Centrais:**
- Criação e disponibilização pública do dataset benchmark CICIoT2023 com 105 dispositivos reais.
- Taxonomia formal de 33 tipos de ataques IoT em 7 perfis operacionais.
- Benchmark abrangente de modelos de aprendizado de máquina e redes neurais profundas.

## ⚠️ Limitações Identificadas
Desbalanceamento significativo em certos tipos de ataques web e necessidade de alta capacidade de armazenamento/processamento para treinamento com o dataset completo.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CICIoT2023`, `IoT Security`, `DDoS/DoS Taxonomy`, `Benchmark Dataset`, `Volumetric Perturbations`
- **Problemas Focais:** `Falta de datasets realistas com hardware IoT`, `Escala massiva de ataques contemporâneos`
- **Métodos Empregados:** `Testbed com 105 dispositivos reais`, `Execução de 33 ataques`, `Extração de 46 atributos de fluxo`
- **Modelos e Arquiteturas:** `DNN`, `Random Forest`, `Adaboost`, `MLP`
- **Bases de Dados:** `CICIoT2023`
- **Resultados Chave:** `Detecção binária > 99%`, `Dificuldade na discriminação multiclasse fina de variantes DoS/DDoS`
- **Limitações Reconhecidas:** `Tamanho massivo dos dados brutos e desbalanceamento de classes específicas`
- **Evidências Citáveis:** `EVID_009_01`, `EVID_009_02`, `EVID_009_03`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Dataset:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_017]] — *Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems*
- **Comparado Com:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
  - [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*

### Citações e Relações Recebidas na Base (Incoming)
- **Avalia Dataset:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Utiliza Dataset:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
- **Compara Com:**
  - [[artigo_017]] — *Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems*
  - [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{avalia_dataset}}$ `[[artigo_009]]`: Avalia o ALF-MoE no benchmark de ataques de IoT em larga escala CICIoT2023.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/CICIoT2023 Dataset|Dataset Benchmark CICIoT2023]] — 🌟 **Definição Canônica**

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa EXPERIMENTO:** Benchmark em conjuntos modernos de tráfego de rede (CIC-IDS-2017 e CICIoT2023)

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CICIoT2023|CICIoT2023]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_009_01` — DEFINIÇÃO
> [!quote] EVID_009_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Caracterização e taxonomia dos ataques de negação de serviço volumétricos (DDoS e DoS) em ambientes de rede.
> **Localização:** Seção 3 (Attack Scenarios and Profiles), Páginas 5-8
>
> *"DDoS and DoS attacks represent volumetric disturbances characterized by massive rates of packets-per-second designed to exhaust network bandwidth or server socket pools through flooding protocols (SYN, UDP, ICMP, HTTP)."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 (Contextualização) ao caracterizar o comportamento dos ataques de DoS/DDoS volumétricos.

### `EVID_009_02` — EMPÍRICA
> [!quote] EVID_009_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O dataset CICIoT2023 contém 33 tipos distintos de ataques executados em 105 dispositivos IoT de hardware real.
> **Localização:** Seção 4 (CICIoT2023 Dataset Structure), Páginas 8-11
>
> *"The testbed incorporates 105 physical IoT devices across multiple vendors and architectures, capturing real-world interactions and executing 33 distinct attack types across 7 categories."*
>
> **Aplicabilidade na Tese ALF-MoE:** Serve como citação canônica para a descrição dos dados de benchmark IoT na seção de metodologia da tese.

### `EVID_009_03` — COMPARATIVA
> [!quote] EVID_009_03 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Modelos supervisionados sofrem para distinguir subvariantes de ataques com dinâmicas similares sem extração multidomínio.
> **Localização:** Seção 5 (Benchmark Results), Páginas 13-16
>
> *"While binary classification reaches near-perfect accuracy (99.5%), multi-class discrimination across fine-grained DoS variations shows notable confusion when relying solely on basic flow counters."*
>
> **Aplicabilidade na Tese ALF-MoE:** Corrobora a necessidade de especialistas dedicados no ALF-MoE (ex: estatístico global + temporal de IAT) para desempatar variantes de ataques volumétricos.

## 📦 Entrada BibTeX
```bibtex
@article{ciciot2023,
  title = {{CICIoT2023}: A Real-Time Dataset and Benchmark for Large-Scale Attacks in {IoT} Environment},
  author = {Neto, Euclides Carlos Pinto and Dadkhah, Sajjad and Ferreira, Raphael and Zohourian, Alireza and Lu, Rongxing and Ghorbani, Ali A.},
  journal = {Sensors},
  year = {2023},
  doi = {10.3390/s23135941},
  volume = {23},
  number = {13},
  pages = {5941},
  publisher = {MDPI AG}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
