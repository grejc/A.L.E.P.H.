---
id: artigo_015
title: 'A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection
  with a Hybrid GRU and BiLSTM Model'
authors:
- A. M. Algarni
- M. S. Alazmi
- S. Alazmi
year: 2025
bibtex_key: etasr10666_2025
doi: 10.48084/etasr.10666
venue: Engineering, Technology & Applied Science Research, Vol. 15, No. 3, 2025, pp.
  23605-23612
keywords:
- Intrusion Detection
- Cybersecurity
- Deep Learning
- Gated Recurrent Unit (GRU)
- Bidirectional LSTM (BiLSTM)
- Sequential Modeling
area: Network Intrusion Detection / Recurrent Neural Networks / Hybrid Architectures
datasets:
- CIC-IDS-2017
- NSL-KDD
models:
- GRU
- BiLSTM
- Hybrid GRU-BiLSTM
- LSTM padrão
- RNN simples
aliases:
- 'A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with
  a Hybrid GRU and BiLSTM Model'
- etasr10666_2025
- artigo_015
tags:
- bibliografia
- alf-moe
- artigo
---

# A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model

> **Citação ABNT Sugerida:** ALGARNI, A. M.; ALAZMI, M. S.; ALAZMI, S.. A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model. In: **Engineering, Technology & Applied Science Research, Vol. 15, No. 3, 2025, pp. 23605-23612**, 2025.
> **Chave BibTeX:** `etasr10666_2025` | **Arquivo TXT:** `ETASR_10666.txt` | **DOI:** `10.48084/etasr.10666`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_015` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Intrusion Detection / Recurrent Neural Networks / Hybrid Architectures |
| **Veículo de Publicação** | Engineering, Technology & Applied Science Research, Vol. 15, No. 3, 2025, pp. 23605-23612 |
| **Datasets Utilizados** | CIC-IDS-2017, NSL-KDD |
| **Modelos / Algoritmos** | GRU, BiLSTM, Hybrid GRU-BiLSTM, LSTM padrão, RNN simples |
| **Palavras-Chave** | Intrusion Detection, Cybersecurity, Deep Learning, Gated Recurrent Unit (GRU), Bidirectional LSTM (BiLSTM), Sequential Modeling |

## 🎯 Problema Abordado
Ataques de intrusão sofisticados distribuem suas ações em janelas temporais prolongadas para escapar de detectores estatísticos estáticos; modelos recorrentes simples sofrem com desvanecimento de gradiente ou alto custo computacional.

## 🔬 Metodologia
Arquitetura híbrida sequencial integrando Gated Recurrent Unit (GRU) e Bidirectional Long Short-Term Memory (BiLSTM); a camada GRU realiza filtragem e aprendizado rápido de curto prazo, enquanto o BiLSTM processa o contexto temporal em ambas as direções (passado e futuro do fluxo).

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O modelo híbrido GRU-BiLSTM alcançou acurácia de 98.6% no CIC-IDS-2017, superando modelos baseados apenas em LSTM ou apenas em GRU, com redução de 22% no tempo de convergência em relação a BiLSTM puro.

**Contribuições Centrais:**
- Proposição do modelo híbrido GRU-BiLSTM combinando eficiência computacional do GRU com expressividade temporal do BiLSTM.
- Demonstração empírica da complementaridade entre GRU e LSTM para segurança de redes.
- Resultados de ponta na classificação multiclasse no benchmark CIC-IDS-2017.

## ⚠️ Limitações Identificadas
A complexidade da modelagem bidirecional impede o processamento puramente streaming sem empacotamento prévio de blocos temporais de fluxo.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `GRU`, `BiLSTM`, `Sequential Intrusion Modeling`, `Temporal Context`
- **Problemas Focais:** `Ataques com dispersão temporal`, `Desvanecimento de gradiente em RNNs clássicas`, `Alto custo computacional de LSTMs profundas`
- **Métodos Empregados:** `Hibridização sequencial GRU + BiLSTM`, `Processamento bidirecional`, `Otimização de taxas de convergência`
- **Modelos e Arquiteturas:** `GRU-BiLSTM`, `GRU`, `BiLSTM`, `LSTM`
- **Bases de Dados:** `CIC-IDS-2017`, `NSL-KDD`
- **Resultados Chave:** `Acurácia de 98.6% no CIC-IDS-2017`, `22% de ganho em velocidade de treino frente a BiLSTM`
- **Limitações Reconhecidas:** `Requer armazenamento temporário para contexto reverso`
- **Evidências Citáveis:** `EVID_015_01`, `EVID_015_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
  - [[artigo_024]] — *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- **Compara Com:**
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: NIDS recorrente híbrido GRU-BiLSTM
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: Modelo profundo GRU-BiLSTM
- [[Conceitos/Gated Recurrent Unit (GRU)|Gated Recurrent Unit (GRU)]] — Papel: Modelo híbrido GRU-BiLSTM para NIDS

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_005 — Categoria: Empírico / Metodologia|CLAIM_005 (Empírico / Metodologia)]] — *"A dinâmica temporal e os intervalos entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) fornecem poder discriminatório essencial para identificar ameaças evasivas que mimetizam volumes benignos de tráfego, como canais de comando e controle (C2) e botnets."*
  - *Aplicação na Tese:* Suporte metodológico ao especialista GRU focado em sequências temporais.

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_015_01` — METODOLÓGICA
> [!quote] EVID_015_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** GRUs oferecem eficiência computacional superior a LSTMs enquanto capturam transições temporais de curto alcance com menos parâmetros.
> **Localização:** Seção 3 (Proposed Methodology: GRU and BiLSTM), Páginas 23607-23608
>
> *"Gated Recurrent Units (GRU) streamline the recurrent gating architecture by merging cell and hidden states through reset and update gates, achieving comparable sequential representation capability to LSTMs with significantly fewer trainable parameters and faster training convergence."*
>
> **Aplicabilidade na Tese ALF-MoE:** Justificativa direta para a inclusão do especialista GRU no ALF-MoE focado em variações sequenciais de curta cadência e IATs.

### `EVID_015_02` — EMPÍRICA
> [!quote] EVID_015_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A modelagem combinada de dependências sequenciais supera classificadores baseados puramente em estatísticas agregadas em fluxos de intrusão do CIC-IDS-2017.
> **Localização:** Seção 4 (Experimental Evaluation), Páginas 23609-23611
>
> *"On the CIC-IDS-2017 benchmark, recurrent models incorporating gating mechanisms attain an accuracy of 98.6% and a 4.1% reduction in false discovery rate compared to traditional feed-forward architectures."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a decisão de projeto de utilizar especialistas temporais dedicados para capturar a trajetória sequencial do tráfego malicioso.

## 📦 Entrada BibTeX
```bibtex
@article{etasr10666_2025,
  title = {{A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model}},
  author = {A. M. Algarni and M. S. Alazmi and S. Alazmi},
  journal = {Engineering, Technology & Applied Science Research, Vol. 15, No. 3, 2025, pp. 23605-23612},
  year = {2025},
  doi = {10.48084/etasr.10666},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
