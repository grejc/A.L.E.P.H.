---
id: Data Leakage e Split Temporal
term: Data Leakage Temporal e Particionamento Estrito
aliases:
- Data Leakage
- Vazamento de Dados
- Temporal Split
- Random Split
- Cronological Partitioning
- Data Leakage Temporal e Particionamento Estrito
- Data Leakage e Split Temporal
tags:
- conceito
- bibliografia
- alf-moe
---

# Data Leakage Temporal e Particionamento Estrito

> **Sinônimos e Variantes:** Data Leakage, Vazamento de Dados, Temporal Split, Random Split, Cronological Partitioning

## 📖 Definição Canônica
Erro metodológico severo em aprendizado de máquina onde dados de teste contaminam o conjunto de treinamento através de sobreposições de conexões contemporâneas em divisões randômicas.

- **Artigo de Definição Formal:** [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- **Evidência Canônica:** `EVID_036_01` (Seção 1 (Introduction) e Seção 3 (Temporal Data Leakage Analysis), Páginas 1-5)
> [!quote] Evidência Canônica (`EVID_036_01`)
> *"Randomly splitting flow records into training and testing partitions inadvertently leaks temporal correlations, as packets belonging to the same underlying connection or attack burst appear in both sets, yielding artificially inflated accuracy scores that degrade in real-world deployments."*
>
> **Afirmação:** O particionamento randômico (random split) em conjuntos de dados de NIDS gera severo data leakage temporal e superestimação irrealista do desempenho do modelo.
>
> **Aplicação na Tese:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar o uso de particionamento estritamente temporal na avaliação experimental da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* | 5/5 | Análise crítica de métodos de particionamento |
| [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* | 5/5 | Estudo empírico definitivo de data leakage temporal em NIDS |

## 🔍 Evidências Literais Associadas
### `EVID_036_01` — LIMITAÇÃO (Fonte: [[artigo_036]])
> [!quote] EVID_036_01
> **Localização:** Seção 1 (Introduction) e Seção 3 (Temporal Data Leakage Analysis), Páginas 1-5
> **Afirmação Sustentada:** O particionamento randômico (random split) em conjuntos de dados de NIDS gera severo data leakage temporal e superestimação irrealista do desempenho do modelo.
>
> *"Randomly splitting flow records into training and testing partitions inadvertently leaks temporal correlations, as packets belonging to the same underlying connection or attack burst appear in both sets, yielding artificially inflated accuracy scores that degrade in real-world deployments."*
>
> **Aplicação Tese ALF-MoE:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar o uso de particionamento estritamente temporal na avaliação experimental da tese.

### `EVID_036_02` — METODOLÓGICA (Fonte: [[artigo_036]])
> [!quote] EVID_036_02
> **Localização:** Seção 4 (Experimental Methodology: Time-based Evaluation), Páginas 6-9
> **Afirmação Sustentada:** A divisão temporal (treinar no passado e testar no futuro cronológico) é o único protocolo experimental metodologicamente válido para refletir a operação real de um NIDS.
>
> *"To obtain valid, generalizable performance estimates, network intrusion detection models must be evaluated strictly using chronological time-based splitting, training exclusively on historical intervals and testing on future unseen epochs."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta o protocolo de teste temporal adotado no capítulo de metodologia da tese.

### `EVID_036_03` — EMPÍRICA (Fonte: [[artigo_036]])
> [!quote] EVID_036_03
> **Localização:** Seção 5 (Results and Discussions), Páginas 10-14
> **Afirmação Sustentada:** Modelos avaliados com divisão puramente temporal sofrem queda perceptível em relação à avaliação randômica, refletindo a complexidade de generalização temporal.
>
> *"When shifting from random k-fold to strict chronological time-based partitioning, classifier macro F1-score experiences an average decrease of over 20%, exposing the vulnerability of static classifiers to natural temporal dynamics."*
>
> **Aplicação Tese ALF-MoE:** Serve como base comparativa para discutir resultados experimentais no Capítulo 5.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
