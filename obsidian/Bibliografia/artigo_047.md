---
id: artigo_047
title: Network Intrusion Detection Model Based on CNN and GRU
authors:
- Bo Cao
- Chenghai Li
- Yafei Song
- Yueyi Qin
- Chen Chen
year: 2022
bibtex_key: cao2022applsci
doi: 10.3390/app12094184
venue: Applied Sciences 2022, Volume 12, Issue 9, 4184
keywords:
- Network Intrusion Detection
- Convolutional Neural Network (CNN)
- Gated Recurrent Unit (GRU)
- Deep Learning
- Spatial-Temporal Features
- NSL-KDD
- UNSW-NB15
area: Network Intrusion Detection / Hybrid Deep Learning / Spatial-Temporal Synergy
datasets:
- NSL-KDD
- UNSW-NB15
models:
- 1D-CNN
- Gated Recurrent Unit (GRU)
- CNN-GRU Hybrid
- CNN-LSTM Baseline
- Random Forest
- SVM
aliases:
- Network Intrusion Detection Model Based on CNN and GRU
- cao2022applsci
- artigo_047
tags:
- bibliografia
- alf-moe
- artigo
---

# Network Intrusion Detection Model Based on CNN and GRU

> **Citação ABNT Sugerida:** CAO, B.; LI, C.; SONG, Y.; QIN, Y.; CHEN, C.. Network Intrusion Detection Model Based on CNN and GRU. In: **Applied Sciences 2022, Volume 12, Issue 9, 4184**, 2022.
> **Chave BibTeX:** `cao2022applsci` | **Arquivo TXT:** `applsci-12-04184-v2.txt` | **DOI:** `10.3390/app12094184`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_047` |
| **Ano** | 2022 |
| **Área de Pesquisa** | Network Intrusion Detection / Hybrid Deep Learning / Spatial-Temporal Synergy |
| **Veículo de Publicação** | Applied Sciences 2022, Volume 12, Issue 9, 4184 |
| **Datasets Utilizados** | NSL-KDD, UNSW-NB15 |
| **Modelos / Algoritmos** | 1D-CNN, Gated Recurrent Unit (GRU), CNN-GRU Hybrid, CNN-LSTM Baseline, Random Forest, SVM |
| **Palavras-Chave** | Network Intrusion Detection, Convolutional Neural Network (CNN), Gated Recurrent Unit (GRU), Deep Learning, Spatial-Temporal Features, NSL-KDD, UNSW-NB15 |

## 🎯 Problema Abordado
Modelos monolíticos clássicos de aprendizado de máquina não conseguem extrair simultaneamente correlações estruturais espaciais entre atributos e dependências temporais de tráfego de rede; modelos baseados unicamente em LSTM sofrem com lentidão de treinamento e alto consumo de memória devido ao número elevado de portas internas.

## 🔬 Metodologia
Modelo híbrido sequencial CNN-GRU: primeiramente uma rede convolucional unidimensional (1D-CNN) realiza a redução de dimensionalidade e extração de características espaciais locais dos atributos de conexão; em seguida, camadas Gated Recurrent Unit (GRU) aprendem a dinâmica sequencial e as variações transitórias temporais ao longo dos fluxos.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O modelo CNN-GRU atingiu acurácia de 99.4% no NSL-KDD e 92.8% no UNSW-NB15, superando baselines baseados em CNN-LSTM com velocidade de treinamento 28% mais rápida e menor consumo de parâmetros, comprovando a eficácia e eficiência computacional do GRU para processamento temporal em NIDS.

**Contribuições Centrais:**
- Demonstração quantitativa da superioridade computacional do GRU sobre o LSTM em NIDS.
- Arquitetura híbrida CNN-GRU com acurácia de ponta.
- Análise do equilíbrio ideal entre expressividade temporal e latência de inferência.

## ⚠️ Limitações Identificadas
Sensibilidade ao tamanho da janela de fluxo escolhida durante o pré-processamento de sequenciamento temporal.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CNN-GRU`, `GRU para NIDS`, `Eficiência Temporal`, `Extração Espacial 1D-CNN`
- **Problemas Focais:** `Lentidão e alto número de parâmetros de LSTMs profundas`, `Incapacidade de capturar espaço e tempo juntos`
- **Métodos Empregados:** `1D-CNN para redução espacial`, `GRU para dependências sequenciais`, `Otimização Adam`
- **Modelos e Arquiteturas:** `CNN-GRU`, `CNN-LSTM`, `CNN`, `GRU`
- **Bases de Dados:** `NSL-KDD`, `UNSW-NB15`
- **Resultados Chave:** `Acurácia de 99.4% e 92.8%`, `28% mais rápido que CNN-LSTM`
- **Limitações Reconhecidas:** `Dependência do comprimento de janela de lote`
- **Evidências Citáveis:** `EVID_047_01`, `EVID_047_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Compara Com:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
- **Relacionado:**
  - [[artigo_028]] — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*

### Citações e Relações Recebidas na Base (Incoming)
- **Fundamenta:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
- **Relacionado:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_024]] — *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*
  - [[artigo_028]] — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
  - [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_047]]`: Justifica o uso de GRU para modelar transições rápidas e cadência temporal com menor custo de treino.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Modelo CNN-GRU para NIDS
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: Modelo CNN-GRU profundo
- [[Conceitos/Gated Recurrent Unit (GRU)|Gated Recurrent Unit (GRU)]] — 🌟 **Definição Canônica**

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_047_01` — METODOLÓGICA
> [!quote] EVID_047_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** GRUs oferecem eficiência computacional superior a LSTMs enquanto preservam a capacidade de capturar a dinâmica temporal de fluxos de intrusão.
> **Localização:** Seção 2.2 (Gated Recurrent Unit) e Seção 3 (CNN-GRU Architecture), Páginas 3-6
>
> *"Compared with standard LSTM networks, GRUs utilize fewer tensor operations and lack a separate cell state, achieving comparable accuracy in sequential anomaly detection with roughly 30% lower parameter footprint and substantially reduced training and inference latency."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar por que o especialista GRU foi selecionado para modelar dinâmicas de curta cadência e IATs no ALF-MoE.

### `EVID_047_02` — EMPÍRICA
> [!quote] EVID_047_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A arquitetura sequencial CNN-GRU supera abordagens monolíticas isoladas com ganho substancial de precisão e taxa de detecção.
> **Localização:** Seção 4 (Experimental Results and Analysis), Páginas 7-10
>
> *"The combined CNN-GRU architecture demonstrates superior detection performance over standalone CNN or GRU models across all test categories on both NSL-KDD and UNSW-NB15 benchmarks."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a decomposição multimodal e a especialização das redes neurais na tese.

## 📦 Entrada BibTeX
```bibtex
@article{cao2022applsci,
  title = {{Network Intrusion Detection Model Based on CNN and GRU}},
  author = {Bo Cao and Chenghai Li and Yafei Song and Yueyi Qin and Chen Chen},
  journal = {Applied Sciences 2022, Volume 12, Issue 9, 4184},
  year = {2022},
  doi = {10.3390/app12094184},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
