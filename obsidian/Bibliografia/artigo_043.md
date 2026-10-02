---
id: artigo_043
title: Towards a Standard Feature Set for Network Intrusion Detection System Datasets
authors:
- Mohanad Sarhan
- Siamak Layeghy
- Marius Portmann
year: 2022
bibtex_key: standard2021
doi: 10.1007/s11036-021-01843-0
venue: Mobile Networks and Applications (MONET), Volume 27, Issue 1, pp. 357-370
keywords:
- Feature Standardization
- NetFlow v9
- NIDS Datasets
- Machine Learning
- Cross-Dataset Evaluation
- Network Security
area: Network Intrusion Detection / Feature Engineering / Standardization
datasets:
- CIC-IDS-2017
- UNSW-NB15
- NF-UNSW-NB15
- NF-BoT-IoT
- NF-ToN-IoT
models:
- Decision Tree
- Random Forest
- Logistic Regression
- Naive Bayes
- Deep Neural Networks (DNN)
aliases:
- Towards a Standard Feature Set for Network Intrusion Detection System Datasets
- standard2021
- artigo_043
tags:
- bibliografia
- alf-moe
- artigo
---

# Towards a Standard Feature Set for Network Intrusion Detection System Datasets

> **Citação ABNT Sugerida:** SARHAN, M.; LAYEGHY, S.; PORTMANN, M.. Towards a Standard Feature Set for Network Intrusion Detection System Datasets. In: **Mobile Networks and Applications (MONET), Volume 27, Issue 1, pp. 357-370**, 2022.
> **Chave BibTeX:** `standard2021` | **Arquivo TXT:** `Towards_a_Standard_Feature_Set_for_Network_Intrusion_Detection_System_Datasets_2021.txt` | **DOI:** `10.1007/s11036-021-01843-0`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_043` |
| **Ano** | 2022 |
| **Área de Pesquisa** | Network Intrusion Detection / Feature Engineering / Standardization |
| **Veículo de Publicação** | Mobile Networks and Applications (MONET), Volume 27, Issue 1, pp. 357-370 |
| **Datasets Utilizados** | CIC-IDS-2017, UNSW-NB15, NF-UNSW-NB15, NF-BoT-IoT, NF-ToN-IoT |
| **Modelos / Algoritmos** | Decision Tree, Random Forest, Logistic Regression, Naive Bayes, Deep Neural Networks (DNN) |
| **Palavras-Chave** | Feature Standardization, NetFlow v9, NIDS Datasets, Machine Learning, Cross-Dataset Evaluation, Network Security |

## 🎯 Problema Abordado
A inexistência de um conjunto unificado de atributos entre datasets de NIDS impede a avaliação da capacidade de generalização dos modelos entre diferentes redes; modelos treinados no conjunto proprietário de um dataset não podem ser testados diretamente em outro.

## 🔬 Metodologia
Definição e validação do NetFlow Standard Feature Set (composto por 43 atributos padronizados baseados no formato da IETF NetFlow v9 / IPFIX); conversão de múltiplos datasets públicos para este padrão e realização de testes de generalização cruzada (treinar no dataset A e avaliar no dataset B).

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O conjunto padronizado de 43 atributos NetFlow retém a mesma performance preditiva que os conjuntos proprietários de 80+ atributos, reduzindo a complexidade computacional e permitindo, pela primeira vez, a realização de testes cruzados de generalização entre bases distintas de cibersegurança.

**Contribuições Centrais:**
- Proposta e validação do padrão de 43 atributos NetFlow para pesquisa em NIDS.
- Demonstração empírica de eficiência com redução de quase 50% no número de variáveis sem perda de acurácia.
- Primeiro benchmark sistemático de generalização cruzada entre datasets de segurança.

## ⚠️ Limitações Identificadas
Atributos estatísticos agregados tornam a detecção cega para ameaças que dependem de inspeção de payload textual em aplicações não cifradas legadas.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Padronização de Atributos`, `NetFlow 43 Features`, `Generalização Cruzada`, `Eficiência Dimensional`
- **Problemas Focais:** `Incompatibilidade de atributos entre datasets de NIDS`, `Inviabilidade de transferência entre bases`
- **Métodos Empregados:** `Seleção e mapeamento para 43 atributos NetFlow v9`, `Treinamento cruzado entre datasets`, `Benchmarking comparativo`
- **Modelos e Arquiteturas:** `Random Forest`, `DNN`, `Decision Tree`
- **Bases de Dados:** `CIC-IDS-2017`, `UNSW-NB15`
- **Resultados Chave:** `Retenção integral de performance com 43 atributos padronizados`, `Viabilização de testes cross-dataset`
- **Limitações Reconhecidas:** `Não processa strings textuais de carga útil`
- **Evidências Citáveis:** `EVID_043_01`, `EVID_043_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Utiliza:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Avalia Dataset:**
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- **Relacionado:**
  - [[artigo_020]] — *Feature Classification and Outlier Detection to Increased Accuracy in Intrusion Detection System*
  - [[artigo_023]] — *Machine Learning for Network Attacks Classification and Statistical Evaluation of Adversarial Learning Methodologies for Synthetic Data Generation*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*
- **Compara Com:**
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
- **Padroniza Dataset:**
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- **Estende:**
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_043]]`: Emprega representação padronizada de atributos inspirada no NetFlow Standard Feature Set de 43 atributos.
- `[[artigo_043]]` $\xrightarrow{\text{consolida_padrao}}$ `[[artigo_027]]` (*NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*): Sarhan et al. consolidam o conjunto padronizado NetFlow de 43 atributos para interoperabilidade cross-dataset.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Padronização de atributos para NIDS
- [[Conceitos/Criptografia Ponta a Ponta e TLS 1.3|Impacto da Criptografia Ponta a Ponta e TLS 1.3 em NIDS]] — 🌟 **Definição Canônica**
- [[Conceitos/NetFlow e Padronizacao de Atributos|NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos]] — Papel: Definição formal do NetFlow Standard Feature Set de 43 atributos

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_001 — Categoria: Teoria|CLAIM_001 (Teoria)]] — *"A adoção generalizada de mecanismos de criptografia ponta a ponta (como TLS 1.3, HTTPS e DoH) tornou a carga útil (payload) dos pacotes opaca aos dispositivos intermediários, debilitando a viabilidade de NIDS legados baseados em inspeção profunda de pacotes (DPI) e assinaturas estáticas."*
  - *Aplicação na Tese:* Citação direta no Capítulo 1 (parágrafo 3) para justificar por que métodos legados de DPI são insuficientes.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_002 — Inspeção de Tráfego Criptografado: DPI de Payload vs. Metadados de Fluxo (Flow-based / NetFlow)|CONTROV_002 — Inspeção de Tráfego Criptografado: DPI de Payload vs. Metadados de Fluxo (Flow-based / NetFlow)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"A adoção universal de criptografia ponta a ponta (TLS 1.3, HTTPS, DoH) torna a carga útil inteiramente opaca a intermediários, tornando o DPI tecnicamente ineficaz e forçando a migração para análise comportamental de metadados agregados de fluxo."*
- [[Contradicoes_e_Divergencias#CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)|CONTROV_005 — Qualidade e Sanitização de Datasets Canônicos (CIC-IDS-2017 e afins)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"O CIC-IDS-2017 bruto possui dezenas de milhares de fluxos duplicados, valores infinitos/ausentes e artefatos de captura que distorcem severamente a avaliação dos algoritmos caso não passem por higienização e sanitização estatística rigorosa."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa CONCEITO:** Opacidade da carga útil por criptografia TLS 1.3 / HTTPS / DoH
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa FUNDAMENTAÇÃO:** Ineficácia de DPI e necessidade de inspeção baseada em metadados de fluxo
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa MÉTODO:** Extração e agregação de fluxos bidirecionais padronizados via NFStream e NetFlow v9
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa RESULTADO:** Classificadores operam com alta acurácia sem acesso a texto claro de payload
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa LIMITAÇÃO:** Cegueira a ataques que dependem exclusivamente de semântica textual profunda de aplicação

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_043_01` — DEFINIÇÃO
> [!quote] EVID_043_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição do conjunto padronizado NetFlow de 43 atributos como solução para a fragmentação e incompatibilidade de datasets de NIDS.
> **Localização:** Seção 3 (The Proposed Standard Feature Set), Páginas 360-363
>
> *"We propose a standard feature set of 43 features based on the NetFlow format that preserves the core predictive information while drastically reducing feature dimensionality across diverse intrusion datasets."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha e padronização do espaço de entrada de atributos tabulares na tese.

### `EVID_043_02` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_043_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A adoção generalizada de criptografia ponta a ponta (como TLS 1.3 e HTTPS) inviabilizou a inspeção de carga útil e exige atributos padronizados baseados em fluxo.
> **Localização:** Seção 1 (Introduction), Páginas 357-358
>
> *"With the widespread deployment of end-to-end encryption protocols such as TLS 1.3, deep packet inspection methods have become ineffective, necessitating robust flow-based feature sets that extract intelligence from flow headers and transmission dynamics rather than payload contents."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação de sustentação direta no Capítulo 1 (parágrafo 3) para fundamentar por que TLS 1.3 debilita a viabilidade prática da inspeção tradicional de pacotes.

## 📦 Entrada BibTeX
```bibtex
@article{standard2021,
  title = {Towards a Standard Feature Set for Network Intrusion Detection System Datasets},
  author = {Sarhan, Mohanad and Layeghy, Siamak and Portmann, Marius},
  journal = {Mobile Networks and Applications},
  year = {2022},
  doi = {10.1007/s11036-021-01843-0},
  volume = {27},
  number = {1},
  pages = {357-370},
  publisher = {Springer Science and Business Media LLC}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
