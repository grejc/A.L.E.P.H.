---
id: artigo_007
title: An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks
authors:
- Mohammad Tariq Ikhlas
- Pohanyar Khowaja Khil
- Malik Muhammad Mueed Aslam
- Muhammad Khuram Shahzad
year: 2026
bibtex_key: ikhlas2026iot
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: arXiv preprint arXiv:2606.05776
keywords:
- Intrusion Detection System
- IoT Networks
- CNN-LSTM
- Deep Learning
- Attack Detection
area: IoT Cyber Security / Hybrid Deep Learning / NIDS
datasets:
- CICIoT2023
- BoT-IoT
models:
- 1D-CNN
- LSTM
- Dense Layers
- Dropout
- Adam Optimizer
aliases:
- An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks
- ikhlas2026iot
- artigo_007
tags:
- bibliografia
- alf-moe
- artigo
---

# An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks

> **Citação ABNT Sugerida:** IKHLAS, M. T.; KHIL, P. K.; ASLAM, M. M. M.; SHAHZAD, M. K.. An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks. In: **arXiv preprint arXiv:2606.05776**, 2026.
> **Chave BibTeX:** `ikhlas2026iot` | **Arquivo TXT:** `An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_007` |
| **Ano** | 2026 |
| **Área de Pesquisa** | IoT Cyber Security / Hybrid Deep Learning / NIDS |
| **Veículo de Publicação** | arXiv preprint arXiv:2606.05776 |
| **Datasets Utilizados** | CICIoT2023, BoT-IoT |
| **Modelos / Algoritmos** | 1D-CNN, LSTM, Dense Layers, Dropout, Adam Optimizer |
| **Palavras-Chave** | Intrusion Detection System, IoT Networks, CNN-LSTM, Deep Learning, Attack Detection |

## 🎯 Problema Abordado
Dispositivos IoT são altamente vulneráveis a botnets e ataques distribuídos devido a baixa capacidade computacional e falta de defesas integradas; necessidade de modelos híbridos que extraiam correlações espaciais e temporais simultaneamente.

## 🔬 Metodologia
Modelo híbrido CNN-LSTM em cascata: camadas convolucionais 1D realizam redução de dimensionalidade e extração de características espaciais primárias, seguidas por camadas LSTM para aprender dependências sequenciais ao longo do tempo.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O modelo híbrido CNN-LSTM atinge acurácia de 99.2% e F1-score de 98.9% no CICIoT2023, demonstrando que a combinação de convolução com recorrência supera redes monolíticas puramente densas ou puramente convolucionais.

**Contribuições Centrais:**
- Arquitetura integrada CNN-LSTM especializada em tráfego IoT.
- Benchmark no dataset recente CICIoT2023.
- Comprovação empírica do ganho gerado pela junção de camadas convolucionais e recorrentes.

## ⚠️ Limitações Identificadas
Atraso de processamento associado à complexidade da célula LSTM e degradação de vazão sob taxas de pacotes extremamente altas.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CNN-LSTM Hybrid`, `IoT Security`, `Spatial-Temporal Processing`
- **Problemas Focais:** `Ataques massivos em dispositivos IoT vulneráveis`, `Incapacidade de modelos simples em fluxos sequenciais`
- **Métodos Empregados:** `Convolução 1D para redução de espaço`, `LSTM para dependências de histórico`
- **Modelos e Arquiteturas:** `1D-CNN-LSTM`
- **Bases de Dados:** `CICIoT2023`, `BoT-IoT`
- **Resultados Chave:** `99.2% de acurácia no CICIoT2023`
- **Limitações Reconhecidas:** `Latência computacional da recorrência pura`
- **Evidências Citáveis:** `EVID_007_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Utiliza Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Relacionado:**
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_028]] — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
  - [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection*
- **Fundamenta Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Compara Com:**
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: CNN-LSTM em tráfego IoT
- [[Conceitos/CICIoT2023 Dataset|Dataset Benchmark CICIoT2023]] — Papel: Classificação CNN-LSTM no CICIoT2023

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CICIoT2023|CICIoT2023]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_007_01` — METODOLÓGICA
> [!quote] EVID_007_01 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A combinação de CNN com LSTM permite capturar sinergicamente correlações de atributos espaciais e a evolução temporal de fluxos de intrusão.
> **Localização:** Seção 3 (Proposed Methodology), Páginas 2-3
>
> *"By cascading 1D-CNN for localized spatial pattern extraction with LSTM cells for temporal trajectory tracking, the hybrid model achieves superior discriminatory power compared to standalone models."*
>
> **Aplicabilidade na Tese ALF-MoE:** Embasamento para os especialistas CNN e LSTM na decomposição do ALF-MoE, demonstrando a complementaridade entre essas famílias de redes.

## 📦 Entrada BibTeX
```bibtex
@article{ikhlas2026iot,
  title = {{An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks}},
  author = {Mohammad Tariq Ikhlas and Pohanyar Khowaja Khil and Malik Muhammad Mueed Aslam and Muhammad Khuram Shahzad},
  journal = {arXiv preprint arXiv:2606.05776},
  year = {2026},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
