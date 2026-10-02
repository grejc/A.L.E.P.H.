---
id: artigo_008
title: An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection
  and identification using network traffic
authors:
- Tinshu Sasi
- Arash Habibi Lashkari
- Rongxing Lu
- Pulei Xiong
- Shahrear Iqbal
year: 2025
bibtex_key: sasi2025efficient
doi: 10.1016/j.jiixd.2024.11.002
venue: Journal of Information and Intelligence 3 (2025) 375–400
keywords:
- IoT Security
- Self-Attention Mechanism
- 1D-CNN-LSTM
- Network Intrusion Detection
- CICIoT2023
- Feature Weighting
area: Network Security / Attention Mechanisms / Hybrid Deep Learning
datasets:
- CICIoT2023
- TON_IoT
- Edge-IIoTset
models:
- 1D-CNN
- Bidirectional LSTM (BiLSTM)
- Self-Attention Layer
- Focal Loss
- Multi-Head Attention variant
aliases:
- An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and
  identification using network traffic
- sasi2025efficient
- artigo_008
tags:
- bibliografia
- alf-moe
- artigo
---

# An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic

> **Citação ABNT Sugerida:** SASI, T.; LASHKARI, A. H.; LU, R.; XIONG, P.; IQBAL, S.. An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic. In: **Journal of Information and Intelligence 3 (2025) 375–400**, 2025.
> **Chave BibTeX:** `sasi2025efficient` | **Arquivo TXT:** `An efﬁcient self attention-based 1D-CNN-LSTM network for IoT attack detection and identiﬁcation using network trafﬁc.txt` | **DOI:** `10.1016/j.jiixd.2024.11.002`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_008` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Security / Attention Mechanisms / Hybrid Deep Learning |
| **Veículo de Publicação** | Journal of Information and Intelligence 3 (2025) 375–400 |
| **Datasets Utilizados** | CICIoT2023, TON_IoT, Edge-IIoTset |
| **Modelos / Algoritmos** | 1D-CNN, Bidirectional LSTM (BiLSTM), Self-Attention Layer, Focal Loss, Multi-Head Attention variant |
| **Palavras-Chave** | IoT Security, Self-Attention Mechanism, 1D-CNN-LSTM, Network Intrusion Detection, CICIoT2023, Feature Weighting |

## 🎯 Problema Abordado
O tráfego de redes IoT apresenta grande volume de ruído e alta redundância; modelos recorrentes padrão tratam todos os passos temporais e características com pesos homogêneos, o que compromete a identificação de ataques disfarçados ou sutis.

## 🔬 Metodologia
Modelo composto por 1D-CNN para filtragem espacial, camadas LSTM bidirecionais para capturar contexto temporal para frente e para trás, e um mecanismo de auto-atenção (Self-Attention) para atribuir dinamicamente maiores pesos às transições e atributos mais salientes da anomalia.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O mecanismo de atenção eleva o F1-score em mais de 3.5% em classes com assinaturas furtivas e reduz a taxa de falsos alarmes; acurácia superior a 99.4% no CICIoT2023 com 33 classes de ataques.

**Contribuições Centrais:**
- Integração de auto-atenção com CNN-LSTM para classificação fina de ataques em tráfego IoT.
- Validação experimental rigorosa em múltiplos datasets modernos de IoT com 33 classes de ameaças.
- Demonstração visual da interpretabilidade dos pesos de atenção atribuídos a atributos determinantes.

## ⚠️ Limitações Identificadas
Custo quadrático do mecanismo de atenção se aplicado sobre sequências temporais excessivamente longas sem pré-agregação de fluxo.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Self-Attention`, `1D-CNN-LSTM`, `Dynamic Attention Weighting`, `IoT Multi-class Attack Detection`
- **Problemas Focais:** `Ponderação uniforme e ruído em sequências temporais`, `Ataques furtivos diluídos em fluxos volumosos`
- **Métodos Empregados:** `Mecanismo de auto-atenção`, `Extração convolucional espacial`, `Modelagem bidirecional`
- **Modelos e Arquiteturas:** `Self-Attention 1D-CNN-BiLSTM`
- **Bases de Dados:** `CICIoT2023`, `TON_IoT`
- **Resultados Chave:** `F1-score > 99% em ataques de IoT com 33 classes`, `Ganhos expressivos em ataques sutis`
- **Limitações Reconhecidas:** `Overhead de cálculo de atenção sobre séries longas`
- **Evidências Citáveis:** `EVID_008_01`, `EVID_008_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Utiliza Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Relacionado:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
- **Fundamenta Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Compara Com:**
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: 1D-CNN-LSTM com mecanismo de auto-atenção
- [[Conceitos/CICIoT2023 Dataset|Dataset Benchmark CICIoT2023]] — Papel: Mecanismo de atenção aplicado ao CICIoT2023

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CICIoT2023|CICIoT2023]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_008_01` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_008_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Mecanismos de atenção permitem que modelos de aprendizado profundo priorizem dinamicamente representações relevantes e suprimam ruído em tráfego de rede.
> **Localização:** Seção 2 (Related Work and Motivation), Página 377
>
> *"Self-attention enables the neural model to assign non-uniform, dynamically computed weights to distinct feature dimensions and time intervals, effectively focusing computational capacity on salient intrusion indicators while suppressing ambient benign traffic noise."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta teoricamente por que o módulo ALF (Attention-Based Learnable Fusion) no ALF-MoE calcula pesos de atenção aprendíveis em vez de utilizar média aritmética estática.

### `EVID_008_02` — EMPÍRICA
> [!quote] EVID_008_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A inclusão de camadas de atenção sobre representações CNN-LSTM produz melhorias quantificáveis em precisão e F1-score em benchmarks multissegmentados.
> **Localização:** Seção 5 (Ablation Study and Results), Páginas 390-394
>
> *"The ablation study confirms that adding the self-attention layer to the CNN-LSTM architecture yields a 3.6% boost in macro F1-score across 33 attack classes on the CICIoT2023 benchmark."*
>
> **Aplicabilidade na Tese ALF-MoE:** Evidência experimental citável na discussão de metodologia e resultados comparativos.

## 📦 Entrada BibTeX
```bibtex
@article{sasi2025efficient,
  title = {An efficient self attention-based {1D-CNN-LSTM} network for {IoT} attack detection and identification using network traffic},
  author = {Sasi, Tinshu and Lashkari, Arash Habibi and Lu, Rongxing and Xiong, Pulei and Iqbal, Shahrear},
  journal = {Journal of Information and Intelligence},
  volume = {3},
  number = {4},
  pages = {375--400},
  year = {2025},
  publisher = {Elsevier},
  doi = {10.1016/j.jiixd.2024.11.002}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
