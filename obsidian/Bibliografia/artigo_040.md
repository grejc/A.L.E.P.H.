---
id: artigo_040
title: 'Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection'
authors:
- Majed Luay
- Siamak Layeghy
- Niloufar Noorbin
- Mohanad Sarhan
- Gayan Kulatilleke
- Nour Moustafa
- Marius Portmann
year: 2026
bibtex_key: timematters2025
doi: 10.1109/access.2026.3688204
venue: IEEE Access, Volume 14, pp. 66899-66913, 2026
keywords:
- NetFlow
- Temporal Features
- Inter-Arrival Time (IAT)
- Machine Learning
- Network Intrusion Detection
- Flow-based Features
area: Network Intrusion Detection / Temporal Feature Engineering / NetFlow
datasets:
- NF-CIC-IDS2017-v2
- NF-UNSW-NB15-v2
- NF-BoT-IoT-v2
- NF-ToN-IoT-v2
models:
- Random Forest
- Extra Trees
- XGBoost
- Multi-Layer Perceptron (MLP)
- Convolutional Neural Network (CNN)
- GRU
aliases:
- 'Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection'
- timematters2025
- artigo_040
tags:
- bibliografia
- alf-moe
- artigo
---

# Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection

> **Citação ABNT Sugerida:** LUAY, M.; LAYEGHY, S.; NOORBIN, N.; SARHAN, M.; KULATILLEKE, G.; MOUSTAFA, N.; PORTMANN, M.. Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection. In: **IEEE Access, Volume 14, pp. 66899-66913, 2026**, 2026.
> **Chave BibTeX:** `timematters2025` | **Arquivo TXT:** `Time_Matters_Temporal_NetFlow_Features_for_ML-Based_Network_Intrusion_Detection.txt` | **DOI:** `10.1109/access.2026.3688204`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_040` |
| **Ano** | 2026 |
| **Área de Pesquisa** | Network Intrusion Detection / Temporal Feature Engineering / NetFlow |
| **Veículo de Publicação** | IEEE Access, Volume 14, pp. 66899-66913, 2026 |
| **Datasets Utilizados** | NF-CIC-IDS2017-v2, NF-UNSW-NB15-v2, NF-BoT-IoT-v2, NF-ToN-IoT-v2 |
| **Modelos / Algoritmos** | Random Forest, Extra Trees, XGBoost, Multi-Layer Perceptron (MLP), Convolutional Neural Network (CNN), GRU |
| **Palavras-Chave** | NetFlow, Temporal Features, Inter-Arrival Time (IAT), Machine Learning, Network Intrusion Detection, Flow-based Features |

## 🎯 Problema Abordado
Conjuntos padrão de atributos NetFlow baseiam-se predominantemente em sumários estatísticos tabulares estáticos (contagem total de pacotes e bytes por conexão), ignorando a dinâmica temporal intrínseca e a cadência entre chegadas consecutivas de pacotes (IAT); essa omissão compromete severamente a separabilidade de ataques furtivos (como C2, Botnets e varreduras distribuídas) que mantêm volumes globais similares ao tráfego legítimo.

## 🔬 Metodologia
Engenharia de um conjunto estendido de atributos temporais extraídos sobre janelas deslizantes de fluxo e vetores de IAT (média, desvio padrão, assimetria, curtose e autocorrelação de tempos entre pacotes em ambas as direções direta e reversa); avaliação comparativa do ganho discriminatório em múltiplos algoritmos de aprendizado de máquina e redes neurais profundas.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
A incorporação explícita de atributos temporais de fluxo e IAT elevou o F1-score em mais de 12.3% em ataques evasivos (Botnets e Infiltração) e reduziu os falsos positivos em mais de 40%, provando que 'o tempo importa' de forma determinante na modelagem comportamental de tráfego de rede.

**Contribuições Centrais:**
- Formulação matemática e engenharia de novos atributos temporais de NetFlow.
- Demonstração empírica da indispensabilidade do tempo para detecção de ameaças furtivas.
- Publicação de versões estendidas dos principais datasets públicos de NIDS com atributos temporais.

## ⚠️ Limitações Identificadas
Cálculo de momentos estatísticos superiores (como curtose e assimetria) de IAT sobre fluxos muito longos impõe custo adicional de processamento na fase de agregação de fluxo.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Atributos Temporais de NetFlow`, `Inter-Arrival Time (IAT)`, `Dinâmica de Cadência`, `Separação de Ataques Furtivos`
- **Problemas Focais:** `Atributos puramente estáticos falham em ataques evasivos`, `C2 e Botnets mimetizam volumes benignos`
- **Métodos Empregados:** `Cômputo de estatísticas temporais de IAT`, `Janelas deslizantes`, `Integração em pipelines de ML`
- **Modelos e Arquiteturas:** `GRU`, `CNN`, `XGBoost`, `Random Forest`
- **Bases de Dados:** `NF-CIC-IDS2017-v2`, `NF-UNSW-NB15-v2`
- **Resultados Chave:** `Aumento de 12.3% no F1 de ataques furtivos`, `Redução de 40% em falsos alarmes`
- **Limitações Reconhecidas:** `Overhead de cálculo estatístico de IAT em tempo real`
- **Evidências Citáveis:** `EVID_040_01`, `EVID_040_02`, `EVID_040_03`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Estende:**
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Relacionado:**
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*
- **Fundamenta Metodologia:**
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_040]]`: ALF-MoE extrai atributos temporais e IATs para alimentar o especialista GRU baseado nas descobertas de Luay et al.
- `[[artigo_040]]` $\xrightarrow{\text{estende_representacao}}$ `[[artigo_027]]` (*NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*): Luay et al. estendem o formato NetFlow padronizado por Sarhan et al. adicionando atributos temporais de IAT.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Engenharia de atributos temporais para NIDS
- [[Conceitos/Inter-Arrival Time (IAT) e Atributos Temporais|Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo]] — 🌟 **Definição Canônica**
- [[Conceitos/NetFlow e Padronizacao de Atributos|NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos]] — Papel: Extensão temporal de NetFlow

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_002 — Categoria: Teoria|CLAIM_002 (Teoria)]] — *"Modelos monolíticos concebidos sob uma perspectiva homogênea ou restrita de atributos (single-view) tendem a apresentar desempenho subótimo na detecção de ataques contemporâneos cujas assinaturas residem em múltiplos domínios informacionais distintos."*
  - *Aplicação na Tese:* Demonstra a cegueira de representações single-view para ameaças temporais.
- [[Afirmacoes_e_Claims#CLAIM_005 — Categoria: Empírico / Metodologia|CLAIM_005 (Empírico / Metodologia)]] — *"A dinâmica temporal e os intervalos entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) fornecem poder discriminatório essencial para identificar ameaças evasivas que mimetizam volumes benignos de tráfego, como canais de comando e controle (C2) e botnets."*
  - *Aplicação na Tese:* Justificativa direta para o especialista temporal GRU e o uso de IAT no ALF-MoE.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito|CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"O particionamento aleatório vaza correlações temporais entre conexões simultâneas de uma mesma rajada (data leakage), inflando artificialmente métricas em até 20% e mascarando a degradação temporal do modelo em ambiente de produção; apenas a divisão estritamente cronológica (temporal split) é metodologicamente válida."*

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_040_01` — DEFINIÇÃO
> [!quote] EVID_040_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição do tempo entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) e sua função como atributo temporal fundamental em fluxos de rede.
> **Localização:** Seção 2 (Temporal Features in Network Traffic), Páginas 66901-66903
>
> *"Packet Inter-Arrival Time (IAT) quantifies the elapsed duration between consecutive packet arrivals within a bidirectional flow, providing an essential mathematical descriptor of communication cadences and pacing strategies."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para definir o subvetor temporal de IATs processado pelo especialista GRU no ALF-MoE.

### `EVID_040_02` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_040_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Soluções baseadas em representação puramente estática ou de perspectiva única falham em discriminar ataques cujos perfis distintivos residem na dimensão temporal.
> **Localização:** Seção 1 (Introduction), Páginas 66899-66901
>
> *"Conventional single-view NetFlow models relying strictly on static cumulative byte and packet counters remain blind to evasive threats such as low-and-slow command-and-control channels, where discriminative patterns exist exclusively in inter-packet arrival timings."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação mandatória no Capítulo 1 para fundamentar as limitações de modelos com representação de perspectiva única (single-view representation).

### `EVID_040_03` — EMPÍRICA
> [!quote] EVID_040_03 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A inclusão de atributos temporais de IAT melhora o F1-score em mais de 12% na detecção de botnets e canais de comando e controle em múltiplos datasets.
> **Localização:** Seção 4 (Experimental Results), Páginas 66907-66911
>
> *"Integrating temporal NetFlow features into machine learning classifiers delivers an average improvement of over 12% in F1-score across evasive attack categories including Botnet and Infiltration on the NF-CIC-IDS2017-v2 dataset."*
>
> **Aplicabilidade na Tese ALF-MoE:** Evidência experimental para sustentar a eficácia do especialista sequencial/temporal na tese.

## 📦 Entrada BibTeX
```bibtex
@article{timematters2025,
  title = {Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection},
  author = {Luay, Majed and Layeghy, Siamak and Noorbin, Niloufar and Sarhan, Mohanad and Kulatilleke, Gayan and Moustafa, Nour and Portmann, Marius},
  journal = {IEEE Access},
  year = {2026},
  doi = {10.1109/access.2026.3688204},
  volume = {14},
  pages = {66899-66913},
  publisher = {Institute of Electrical and Electronics Engineers (IEEE)}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
