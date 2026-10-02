---
id: artigo_011
title: Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018
  Dataset
authors:
- A. Aljebreen
- M. Algarni
- S. Alazmi
year: 2025
bibtex_key: etasr2025ids
doi: 10.48084/etasr.11173
venue: Engineering, Technology & Applied Science Research, Vol. 15, No. 4, 2025, pp.
  24782-24787
keywords:
- CSE-CIC-IDS2018
- Anomaly Detection
- Intrusion Detection
- Deep Learning
- DNN
- LSTM
area: Network Intrusion Detection / Deep Learning / CSE-CIC-IDS2018
datasets:
- CSE-CIC-IDS2018
models:
- DNN
- 1D-CNN
- LSTM
- Random Forest
aliases:
- Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset
- etasr2025ids
- artigo_011
tags:
- bibliografia
- alf-moe
- artigo
---

# Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset

> **Citação ABNT Sugerida:** ALJEBREEN, A.; ALGARNI, M.; ALAZMI, S.. Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset. In: **Engineering, Technology & Applied Science Research, Vol. 15, No. 4, 2025, pp. 24782-24787**, 2025.
> **Chave BibTeX:** `etasr2025ids` | **Arquivo TXT:** `Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset.txt` | **DOI:** `10.48084/etasr.11173`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_011` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Intrusion Detection / Deep Learning / CSE-CIC-IDS2018 |
| **Veículo de Publicação** | Engineering, Technology & Applied Science Research, Vol. 15, No. 4, 2025, pp. 24782-24787 |
| **Datasets Utilizados** | CSE-CIC-IDS2018 |
| **Modelos / Algoritmos** | DNN, 1D-CNN, LSTM, Random Forest |
| **Palavras-Chave** | CSE-CIC-IDS2018, Anomaly Detection, Intrusion Detection, Deep Learning, DNN, LSTM |

## 🎯 Problema Abordado
Detecção de ataques sofisticados em ambientes corporativos de grande porte com tráfego massivo e heterogêneo utilizando o dataset CSE-CIC-IDS2018; desafios de escalabilidade e falsos positivos de modelos supervisionados.

## 🔬 Metodologia
Comparação entre Redes Neurais Profundas Totalmente Conectadas (DNN), Redes Convolucionais 1D (CNN) e Long Short-Term Memory (LSTM) treinadas sobre o conjunto completo e amostrado do benchmark CSE-CIC-IDS2018 após pré-processamento e normalização Min-Max.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O modelo LSTM obteve a melhor sensibilidade na detecção de ataques de longa duração (Infiltration e Botnet) com acurácia global de 97.8%, enquanto a DNN obteve a maior velocidade de inferência na classificação de ataques volumétricos (DDoS).

**Contribuições Centrais:**
- Avaliação comparativa de DNN vs CNN vs LSTM no CSE-CIC-IDS2018.
- Demonstração das vantagens de arquiteturas recorrentes em ataques distribuídos e de longa cadência.
- Análise do trade-off entre tempo de inferência e capacidade de discriminação.

## ⚠️ Limitações Identificadas
Custo de memória elevado ao processar o volume total de dezenas de milhões de fluxos do dataset CSE-CIC-IDS2018 sem subamostragem estratégica.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CSE-CIC-IDS2018`, `Enterprise NIDS`, `Deep Learning Benchmark`, `LSTM vs DNN`
- **Problemas Focais:** `Ataques corporativos multietapa`, `Alto volume de tráfego de rede`
- **Métodos Empregados:** `Comparação de arquiteturas neurais`, `Pré-processamento Min-Max`
- **Modelos e Arquiteturas:** `DNN`, `1D-CNN`, `LSTM`
- **Bases de Dados:** `CSE-CIC-IDS2018`
- **Resultados Chave:** `LSTM lidera em ataques graduais/temporais (Botnet/Infiltration); DNN é mais rápida em volumétricos`
- **Limitações Reconhecidas:** `Alto consumo de memória em conjuntos completos`
- **Evidências Citáveis:** `EVID_011_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Utiliza Dataset:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- **Relacionado:**
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: Deep learning no CSE-CIC-IDS2018

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CSE-CIC-IDS2018|CSE-CIC-IDS2018]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_011_01` — COMPARATIVA
> [!quote] EVID_011_01 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Redes recorrentes (LSTM) apresentam melhor sensibilidade para ataques multifásicos e graduais (como Botnet e Infiltração), enquanto DNNs oferecem menor latência para ataques volumétricos.
> **Localização:** Seção 4 (Results and Discussion), Páginas 24785-24786
>
> *"Experimental comparisons reveal that LSTM networks demonstrate superior capability in distinguishing subtle multi-stage attacks like Infiltration and Botnets, while fully connected DNNs offer significantly lower computational latency for high-volume DDoS flows."*
>
> **Aplicabilidade na Tese ALF-MoE:** Evidência crucial para justificar por que o ALF-MoE inclui tanto um especialista denso (DNN) quanto especialistas recorrentes (GRU e LSTM) operando em conjunto.

## 📦 Entrada BibTeX
```bibtex
@article{etasr2025ids,
  title = {{Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset}},
  author = {A. Aljebreen and M. Algarni and S. Alazmi},
  journal = {Engineering, Technology & Applied Science Research, Vol. 15, No. 4, 2025, pp. 24782-24787},
  year = {2025},
  doi = {10.48084/etasr.11173},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
