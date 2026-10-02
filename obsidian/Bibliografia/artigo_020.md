---
id: artigo_020
title: Feature Classification and Outlier Detection to Increased Accuracy in Intrusion
  Detection System
authors:
- Nachiket Sainis
- Durgesh Srivastava
- Rajeshwar Singh
year: 2018
bibtex_key: feature2018
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: International Journal of Applied Engineering Research ISSN 0973-4562 Volume
  13, Number 10 (2018) pp. 7249-7255
keywords:
- Intrusion Detection System
- Feature Classification
- Outlier Detection
- K-Means
- Support Vector Machines
- Accuracy Enhancement
area: Network Intrusion Detection / Feature Engineering / Outlier Filtering
datasets:
- KDD Cup 99
- NSL-KDD
models:
- k-Means Clustering
- Support Vector Machines (SVM)
- Naive Bayes
- Feature Selection Filter
aliases:
- Feature Classification and Outlier Detection to Increased Accuracy in Intrusion
  Detection System
- feature2018
- artigo_020
tags:
- bibliografia
- alf-moe
- artigo
---

# Feature Classification and Outlier Detection to Increased Accuracy in Intrusion Detection System

> **Citação ABNT Sugerida:** SAINIS, N.; SRIVASTAVA, D.; SINGH, R.. Feature Classification and Outlier Detection to Increased Accuracy in Intrusion Detection System. In: **International Journal of Applied Engineering Research ISSN 0973-4562 Volume 13, Number 10 (2018) pp. 7249-7255**, 2018.
> **Chave BibTeX:** `feature2018` | **Arquivo TXT:** `Feature_Classification_and_Outlier_Detection_to_Increased_Accuracy_in_Intrusion_Detection_System_2018.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_020` |
| **Ano** | 2018 |
| **Área de Pesquisa** | Network Intrusion Detection / Feature Engineering / Outlier Filtering |
| **Veículo de Publicação** | International Journal of Applied Engineering Research ISSN 0973-4562 Volume 13, Number 10 (2018) pp. 7249-7255 |
| **Datasets Utilizados** | KDD Cup 99, NSL-KDD |
| **Modelos / Algoritmos** | k-Means Clustering, Support Vector Machines (SVM), Naive Bayes, Feature Selection Filter |
| **Palavras-Chave** | Intrusion Detection System, Feature Classification, Outlier Detection, K-Means, Support Vector Machines, Accuracy Enhancement |

## 🎯 Problema Abordado
A alta dimensionalidade dos dados de fluxo de rede e a presença de instâncias ruidosas ou discrepantes (outliers) degradam a acurácia dos classificadores e elevam o índice de alarmes falsos em NIDS.

## 🔬 Metodologia
Abordagem em duas etapas: primeiramente detecção e remoção de outliers por agrupamento k-Means e distância Euclidiana, seguida por classificação supervisionada via SVM e Naive Bayes utilizando subconjuntos otimizados de atributos.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
A eliminação prévia de dados ruidosos combinada com seleção de atributos relevantes aumentou a acurácia de detecção em 4.8% e reduziu os falsos positivos em 3.2% em relação ao classificador direto sem pré-filtragem.

**Contribuições Centrais:**
- Pipeline de pré-processamento acoplando agrupamento para detecção de anomalias com classificação supervisionada.
- Demonstração do impacto de instâncias discrepantes sobre hiperplanos de SVM.
- Redução de tempo de processamento por poda de atributos irrelevantes.

## ⚠️ Limitações Identificadas
Avaliação baseada nos datasets KDD Cup 99 e NSL-KDD, cujos padrões de tráfego são antigos e desatualizados frente a protocolos modernos cifrados.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Feature Selection`, `Outlier Filtering`, `NIDS Pre-processing`, `Dimensionality Reduction`
- **Problemas Focais:** `Ruído e dimensionalidade excessiva em dados de NIDS`, `Falsos positivos por outliers`
- **Métodos Empregados:** `Agrupamento k-Means`, `Filtro de relevância de atributos`, `Classificação SVM`
- **Modelos e Arquiteturas:** `k-Means`, `SVM`, `Naive Bayes`
- **Bases de Dados:** `KDD Cup 99`, `NSL-KDD`
- **Resultados Chave:** `Aumento de 4.8% em acurácia e redução de falsos positivos`
- **Limitações Reconhecidas:** `Datasets legados com tráfego não representativo`
- **Evidências Citáveis:** `EVID_020_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*

## 🎓 Integração com a Tese ALF-MoE

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_020_01` — METODOLÓGICA
> [!quote] EVID_020_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A sanitização de atributos irrelevantes e a eliminação de ruídos nos conjuntos de tráfego é pré-requisito indispensável para estabilizar classificadores de intrusão.
> **Localização:** Seção 1 (Introduction) e Seção 3 (Proposed Methodology), Páginas 7249-7251
>
> *"Data preprocessing including outlier filtering and strategic feature reduction significantly stabilizes classifier convergence, yielding superior classification accuracy and suppressing false alarm rates."*
>
> **Aplicabilidade na Tese ALF-MoE:** Reforça as decisões de pré-processamento e normalização no pipeline de dados da metodologia da tese.

## 📦 Entrada BibTeX
```bibtex
@article{feature2018,
  title = {Feature Classification and Outlier Detection to Increased Accuracy in Intrusion Detection System},
  author = {Sainis, Nachiket and Srivastava, Durgesh and Singh, Rajeshwar},
  journal = {International Journal of Applied Engineering Research},
  year = {2018},
  volume = {13},
  number = {10},
  pages = {7249--7255}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
