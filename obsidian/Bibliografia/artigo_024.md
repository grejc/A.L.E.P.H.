---
id: artigo_024
title: 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces'
authors:
- Albert Gu
- Tri Dao
year: 2024
bibtex_key: mamba2025
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Proceedings of the 41st International Conference on Machine Learning (ICML
  2024)
keywords:
- Mamba
- State Space Models (SSM)
- Selective State Spaces
- Linear-Time Sequence Modeling
- Hardware-Aware Algorithm
area: Deep Learning / Sequence Modeling / State Space Models
datasets:
- The Pile
- Language Modeling Benchmarks
- DNA sequence benchmarks
- Audio synthesis datasets
models:
- Mamba Block
- Structured State Space Models (S4)
- Selective State Spaces
- FlashAttention (comparativo)
- Transformer-LLMs
aliases:
- 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces'
- mamba2025
- artigo_024
tags:
- bibliografia
- alf-moe
- artigo
---

# Mamba: Linear-Time Sequence Modeling with Selective State Spaces

> **Citação ABNT Sugerida:** GU, A.; DAO, T.. Mamba: Linear-Time Sequence Modeling with Selective State Spaces. In: **Proceedings of the 41st International Conference on Machine Learning (ICML 2024)**, 2024.
> **Chave BibTeX:** `mamba2025` | **Arquivo TXT:** `Mamba__Linear-Time_Sequence_Modeling.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_024` |
| **Ano** | 2024 |
| **Área de Pesquisa** | Deep Learning / Sequence Modeling / State Space Models |
| **Veículo de Publicação** | Proceedings of the 41st International Conference on Machine Learning (ICML 2024) |
| **Datasets Utilizados** | The Pile, Language Modeling Benchmarks, DNA sequence benchmarks, Audio synthesis datasets |
| **Modelos / Algoritmos** | Mamba Block, Structured State Space Models (S4), Selective State Spaces, FlashAttention (comparativo), Transformer-LLMs |
| **Palavras-Chave** | Mamba, State Space Models (SSM), Selective State Spaces, Linear-Time Sequence Modeling, Hardware-Aware Algorithm |

## 🎯 Problema Abordado
A atenção do Transformer escala com complexidade temporal e espacial quadrática O(N^2) em relação ao comprimento da sequência, tornando a inferência e o processamento de longos contextos proibitivamente lentos e intensivos em memória; modelos de espaço de estados lineares (SSMs) anteriores eram invariantes no tempo e incapazes de realizar seleção dinâmica de conteúdo.

## 🔬 Metodologia
Proposição do Mamba, integrando State Space Models com parâmetros seletivos dependentes de entrada (Selective SSM) associados a um algoritmo ciente de hardware (hardware-aware scan) que opera eficientemente na SRAM da GPU sem materialização do estado intermediário completo.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O Mamba atinge vazão 5 vezes superior à de Transformers padrão durante inferência sequencial, escala linearmente com o tamanho da sequência O(N) e supera Transformers de tamanho equivalente em tarefas densas de linguagem e modelagem temporal contínua.

**Contribuições Centrais:**
- Introdução de mecanismos de seleção dinâmica dependentes de entrada para modelos de espaço de estados.
- Algoritmo de paralelização e fusão de núcleos ciente de hardware com complexidade O(N).
- Superação do padrão Transformer em eficiência e desempenho em múltiplas modalidades temporais.

## ⚠️ Limitações Identificadas
Dificuldades em tarefas puramente baseadas em busca de correspondência exata associativa fora de domínio (associative recall) em comparação com o mecanismo de atenção completa global.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Mamba`, `Selective State Space Models`, `Modelagem Sequencial Linear`, `Hardware-Aware Scan`
- **Problemas Focais:** `Complexidade quadrática O(N^2) do Transformer`, `Invariância temporal de SSMs tradicionais`
- **Métodos Empregados:** `Parâmetros seletivos dependentes de entrada`, `Fusão de kernel para SRAM de GPU`, `Decodificação em tempo constante O(1)`
- **Modelos e Arquiteturas:** `Mamba`, `S4`, `Transformer`
- **Bases de Dados:** `The Pile`, `Benchmarks de sequências longas`
- **Resultados Chave:** `5x mais rápido em inferência`, `Complexidade O(N)`, `Excelente desempenho em dados temporais contínuos`
- **Limitações Reconhecidas:** `Ainda recente na aplicação a tráfego de redes tabulares`
- **Evidências Citáveis:** `EVID_024_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*

## 🎓 Integração com a Tese ALF-MoE

### Clusters Temáticos
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: State Space Models|State Space Models]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_024_01` — ESTADO DA ARTE
> [!quote] EVID_024_01 (Relevância: 4/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Modelos de espaço de estados seletivos (SSM) alcançam modelagem de contexto temporal de longo alcance com complexidade linear no comprimento da sequência.
> **Localização:** Seção 1 (Introduction) e Seção 3 (Selective State Spaces), Páginas 1-5
>
> *"By making state space parameters functions of the input, selective state space models filter out irrelevant information and compress context dynamically with linear-time computational scaling in sequence length."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fornece fundamentação teórica de ponta na revisão de literatura sobre modelagem de sequências e alternativas computacionais lineares a mecanismos quadráticos de atenção.

## 📦 Entrada BibTeX
```bibtex
@inproceedings{mamba2025,
  title = {Mamba: Linear-Time Sequence Modeling with Selective State Spaces},
  author = {Gu, Albert and Dao, Tri},
  year = {2024},
  booktitle = {Proceedings of the 41st International Conference on Machine Learning}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
