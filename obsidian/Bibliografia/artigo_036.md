---
id: artigo_036
title: Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems
authors:
- Majed Luay
- Siamak Layeghy
- Seyedehfaezeh Hosseininoorbin
- Mohanad Sarhan
- Nour Moustafa
- Marius Portmann
year: 2025
bibtex_key: temporal2025
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: arXiv preprint arXiv:2503.04404v2
keywords:
- NetFlow Datasets
- Temporal Analysis
- Data Leakage
- Time-based Partitioning
- Network Intrusion Detection
- Evaluation Methodology
area: Network Intrusion Detection / Evaluation Methodology / Temporal Data Leakage
datasets:
- NetFlow-CIC-IDS2017
- NetFlow-UNSW-NB15
- NetFlow-NF-ToN-IoT
models:
- Random Forest (RF)
- Decision Tree (DT)
- Multi-Layer Perceptron (MLP)
- Deep Neural Network (DNN)
- Logistic Regression
aliases:
- Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems
- temporal2025
- artigo_036
tags:
- bibliografia
- alf-moe
- artigo
---

# Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems

> **Citação ABNT Sugerida:** LUAY, M.; LAYEGHY, S.; HOSSEININOORBIN, S.; SARHAN, M.; MOUSTAFA, N.; PORTMANN, M.. Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems. In: **arXiv preprint arXiv:2503.04404v2**, 2025.
> **Chave BibTeX:** `temporal2025` | **Arquivo TXT:** `Temporal_Analysis_of_NetFlow_Datasets_for_Network_Intrusion_Detection_Systems.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_036` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Intrusion Detection / Evaluation Methodology / Temporal Data Leakage |
| **Veículo de Publicação** | arXiv preprint arXiv:2503.04404v2 |
| **Datasets Utilizados** | NetFlow-CIC-IDS2017, NetFlow-UNSW-NB15, NetFlow-NF-ToN-IoT |
| **Modelos / Algoritmos** | Random Forest (RF), Decision Tree (DT), Multi-Layer Perceptron (MLP), Deep Neural Network (DNN), Logistic Regression |
| **Palavras-Chave** | NetFlow Datasets, Temporal Analysis, Data Leakage, Time-based Partitioning, Network Intrusion Detection, Evaluation Methodology |

## 🎯 Problema Abordado
O procedimento generalizado na literatura de NIDS de empregar divisão randômica (random k-fold split) para particionamento de treino/teste introduz grave contaminação temporal (data leakage); fluxos da mesma conexão ou campanha de ataque aparecem simultaneamente em treino e teste, inflando artificialmente as métricas de acurácia que despencam quando o modelo é posto em operação temporal real.

## 🔬 Metodologia
Investigação temporal detalhada sobre datasets padronizados de NetFlow (NetFlow-CIC-IDS2017, NetFlow-UNSW-NB15, NetFlow-NF-ToN-IoT); comparação controlada entre particionamento puramente temporal (treino no passado, teste estritamente no futuro) versus particionamento randômico tradicional; análise da degradação temporal do desempenho do modelo ao longo do tempo.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O particionamento randômico infla a acurácia em até 18.5% e o F1-macro em mais de 25% devido à sobreposição de pacotes da mesma conexão; a avaliação com split temporal estrito revela o verdadeiro desempenho operacional e evidencia que modelos sem atributos temporais sofrem rápida obsolescência conforme o padrão do tráfego evolui.

**Contribuições Centrais:**
- Demonstração quantitativa definitiva do efeito enganoso do particionamento randômico em NIDS.
- Proposta de protocolo de validação temporal estrita para datasets baseados em NetFlow.
- Medição do ritmo de degradação de desempenho em modelos supervisionados em produção.

## ⚠️ Limitações Identificadas
A divisão temporal requer anotação temporal precisa (timestamps de alta resolução de início e fim de fluxo) nem sempre disponível com rigor em datasets legados.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Análise Temporal de NetFlow`, `Data Leakage Temporal`, `Particionamento Temporal Estrito`, `Desvio de Conceito`
- **Problemas Focais:** `Acurácia superestimada por random split`, `Contaminação entre treino e teste no domínio do tempo`
- **Métodos Empregados:** `Comparação Time-based Split vs Random Split`, `Avaliação cronológica contínua`, `Medição de decaimento de F1`
- **Modelos e Arquiteturas:** `Random Forest`, `DNN`, `Decision Tree`
- **Bases de Dados:** `NetFlow-CIC-IDS2017`, `NetFlow-UNSW-NB15`
- **Resultados Chave:** `Random split infla acurácia em até 18.5% por vazamento de dados`, `Split temporal é indispensável para rigor acadêmico`
- **Limitações Reconhecidas:** `Requer timestamps com resolução milissegundos`
- **Evidências Citáveis:** `EVID_036_01`, `EVID_036_02`, `EVID_036_03`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Critica Metodologia:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- **Relacionado:**
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Fundamenta Metodologia:**
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_036]]`: Adota protocolo rigoroso de particionamento estritamente temporal para evitar data leakage.
- `[[artigo_036]]` $\xrightarrow{\text{estende_critica}}$ `[[artigo_006]]` (*Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*): Luay et al. comprovam que avaliações com random split inflacionam métricas reportadas na literatura de NIDS.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Análise temporal e avaliação de NIDS
- [[Conceitos/NetFlow e Padronizacao de Atributos|NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos]] — Papel: Análise temporal de bases NetFlow
- [[Conceitos/Data Leakage e Split Temporal|Data Leakage Temporal e Particionamento Estrito]] — 🌟 **Definição Canônica**

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_006 — Categoria: Metodologia|CLAIM_006 (Metodologia)]] — *"O particionamento randômico de dados (random split / k-fold) em datasets de NIDS baseados em fluxo induz grave contaminação temporal (data leakage) e superestimação irrealista de acurácia, sendo mandatório o particionamento puramente cronológico (temporal split) para avaliação científica rigorosa."*
  - *Aplicação na Tese:* Citação mandatória no Capítulo 1 e Capítulo 3 para justificar o protocolo experimental de split temporal na tese.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito|CONTROV_001 — Avaliação de NIDS: Random Split (k-fold) vs. Particionamento Temporal Estrito]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"O particionamento aleatório vaza correlações temporais entre conexões simultâneas de uma mesma rajada (data leakage), inflando artificialmente métricas em até 20% e mascarando a degradação temporal do modelo em ambiente de produção; apenas a divisão estritamente cronológica (temporal split) é metodologicamente válida."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa FUNDAMENTAÇÃO:** Teoria de contaminação e vazamento temporal (Data Leakage) em séries de tráfego
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa MÉTODO:** Particionamento cronológico estrito (Temporal Split) e métricas balanceadas (Macro F1)
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa EXPERIMENTO:** Comparação entre k-fold randômico vs divisão temporal cronológica em bases NetFlow
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa RESULTADO:** Demonstração de que random split inflaciona artificialmente métricas em até 20%
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa LIMITAÇÃO:** Queda perceptível de desempenho sob evolução natural de tráfego (concept drift)

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_036_01` — LIMITAÇÃO
> [!quote] EVID_036_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O particionamento randômico (random split) em conjuntos de dados de NIDS gera severo data leakage temporal e superestimação irrealista do desempenho do modelo.
> **Localização:** Seção 1 (Introduction) e Seção 3 (Temporal Data Leakage Analysis), Páginas 1-5
>
> *"Randomly splitting flow records into training and testing partitions inadvertently leaks temporal correlations, as packets belonging to the same underlying connection or attack burst appear in both sets, yielding artificially inflated accuracy scores that degrade in real-world deployments."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar o uso de particionamento estritamente temporal na avaliação experimental da tese.

### `EVID_036_02` — METODOLÓGICA
> [!quote] EVID_036_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A divisão temporal (treinar no passado e testar no futuro cronológico) é o único protocolo experimental metodologicamente válido para refletir a operação real de um NIDS.
> **Localização:** Seção 4 (Experimental Methodology: Time-based Evaluation), Páginas 6-9
>
> *"To obtain valid, generalizable performance estimates, network intrusion detection models must be evaluated strictly using chronological time-based splitting, training exclusively on historical intervals and testing on future unseen epochs."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta o protocolo de teste temporal adotado no capítulo de metodologia da tese.

### `EVID_036_03` — EMPÍRICA
> [!quote] EVID_036_03 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Modelos avaliados com divisão puramente temporal sofrem queda perceptível em relação à avaliação randômica, refletindo a complexidade de generalização temporal.
> **Localização:** Seção 5 (Results and Discussions), Páginas 10-14
>
> *"When shifting from random k-fold to strict chronological time-based partitioning, classifier macro F1-score experiences an average decrease of over 20%, exposing the vulnerability of static classifiers to natural temporal dynamics."*
>
> **Aplicabilidade na Tese ALF-MoE:** Serve como base comparativa para discutir resultados experimentais no Capítulo 5.

## 📦 Entrada BibTeX
```bibtex
@article{temporal2025,
  title = {Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems},
  author = {Luay, Majed and Layeghy, Siamak and Hosseininoorbin, Seyedehfaezeh and Sarhan, Mohanad and Moustafa, Nour and Portmann, Marius},
  journal = {arXiv preprint arXiv:2503.04404},
  year = {2025}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
