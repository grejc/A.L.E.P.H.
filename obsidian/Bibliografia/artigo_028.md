---
id: artigo_028
title: Network Anomaly Intrusion Detection Based on Deep Learning Approach
authors:
- Yung-Chung Wang
- Yi-Chun Houng
- Hao-Xun Lin
year: 2023
bibtex_key: wang2023deep
doi: 10.3390/s23042171
venue: Sensors 2023, 23(4), 2171
keywords:
- Network Anomaly Detection
- Deep Learning
- Convolutional Neural Network
- Recurrent Neural Network
- Intrusion Detection
- Feature Mapping
area: Network Intrusion Detection / Deep Learning / Spatial-Temporal Hybrids
datasets:
- NSL-KDD
- UNSW-NB15
models:
- CNN
- RNN
- CNN-RNN Hybrid
- Random Forest
- Support Vector Machine
aliases:
- Network Anomaly Intrusion Detection Based on Deep Learning Approach
- wang2023deep
- artigo_028
tags:
- bibliografia
- alf-moe
- artigo
---

# Network Anomaly Intrusion Detection Based on Deep Learning Approach

> **Citação ABNT Sugerida:** WANG, Y.; HOUNG, Y.; LIN, H.. Network Anomaly Intrusion Detection Based on Deep Learning Approach. In: **Sensors 2023, 23(4), 2171**, 2023.
> **Chave BibTeX:** `wang2023deep` | **Arquivo TXT:** `Network Anomaly Intrusion Detection Based on Deep Learning Approach.txt` | **DOI:** `10.3390/s23042171`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_028` |
| **Ano** | 2023 |
| **Área de Pesquisa** | Network Intrusion Detection / Deep Learning / Spatial-Temporal Hybrids |
| **Veículo de Publicação** | Sensors 2023, 23(4), 2171 |
| **Datasets Utilizados** | NSL-KDD, UNSW-NB15 |
| **Modelos / Algoritmos** | CNN, RNN, CNN-RNN Hybrid, Random Forest, Support Vector Machine |
| **Palavras-Chave** | Network Anomaly Detection, Deep Learning, Convolutional Neural Network, Recurrent Neural Network, Intrusion Detection, Feature Mapping |

## 🎯 Problema Abordado
Métodos clássicos de machine learning dependem de seleção manual de atributos e falham em reconhecer correlações intrincadas em tráfego de rede complexo; necessidade de abordagens profundas que aprendam representações latentes automaticamente.

## 🔬 Metodologia
Modelo composto por uma etapa convolucional para mapear atributos de fluxo em matrizes bidimensionais simulando imagens de tráfego, seguida por camadas recorrentes para aprender transições temporais ao longo da conexão.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O modelo híbrido CNN-RNN superou os classificadores tradicionais, alcançando acurácia de 98.2% no NSL-KDD e 93.5% no UNSW-NB15, provando que o mapeamento convolucional combinado à recorrência extrai características que algoritmos rasos não conseguem separar.

**Contribuições Centrais:**
- Técnica de transformação de vetores de fluxo em estruturas espaciais para processamento convolucional.
- Pipeline híbrido integrando convolução e recorrência para NIDS.
- Comparação sistemática contra algoritmos tradicionais de aprendizado de máquina.

## ⚠️ Limitações Identificadas
O mapeamento artificial de vetores 1D de fluxo em imagens 2D impõe suposições arbitrárias de adjacência espacial entre atributos.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Spatial-Temporal Hybrid`, `Mapeamento Espacial de Fluxo`, `Extração Convolucional`, `Aprendizado Profundo`
- **Problemas Focais:** `Limitação de modelos rasos de ML`, `Necessidade de extração automática de atributos`
- **Métodos Empregados:** `Mapeamento de atributos em matriz 2D`, `Convolução espacial`, `Passagem recorrente`
- **Modelos e Arquiteturas:** `CNN-RNN`, `CNN`, `RNN`, `SVM`
- **Bases de Dados:** `NSL-KDD`, `UNSW-NB15`
- **Resultados Chave:** `Acurácia de 98.2% e 93.5%`, `Superioridade sobre modelos rasos`
- **Limitações Reconhecidas:** `Adjacência espacial artificial entre atributos tabulares`
- **Evidências Citáveis:** `EVID_028_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

### Citações e Relações Recebidas na Base (Incoming)
- **Fundamenta:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
- **Relacionado:**
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: Detecção de anomalias com CNN e RNN

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_028_01` — METODOLÓGICA
> [!quote] EVID_028_01 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** O mapeamento de atributos estatísticos de tráfego em matrizes espaciais permite que redes convolucionais aprendam correlações morfológicas locais entre campos do fluxo.
> **Localização:** Seção 3 (Deep Learning Architecture and Feature Representation), Páginas 5-7
>
> *"Reshaping normalized network traffic features into spatial dimensional matrices enables convolutional kernels to capture localized inter-feature correlations and structural motifs across connection attributes."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a formulação do especialista convolucional (CNN) no ALF-MoE (Capítulo 1 e 3), que processa matrizes dimensionais derivadas dos atributos de tráfego.

## 📦 Entrada BibTeX
```bibtex
@article{wang2023deep,
  title = {{Network Anomaly Intrusion Detection Based on Deep Learning Approach}},
  author = {Yung-Chung Wang and Yi-Chun Houng and Hao-Xun Lin},
  journal = {Sensors 2023, 23(4), 2171},
  year = {2023},
  doi = {10.3390/s23042171},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
