---
id: artigo_025
title: One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts
  (MoE)
authors:
- Xu Yang
- Shaowei Wang
- Jiayuan Zhou
- Wenhan Zhu
year: 2025
bibtex_key: moevd2025
doi: 10.1145/3715736
venue: Proceedings of the ACM on Software Engineering (PACMSE / FSE 2025), Vol. 2,
  No. FSE, Article 166, pp. 446-464
keywords:
- Mixture of Experts (MoE)
- Vulnerability Detection
- One-for-All Limitation
- Deep Learning
- Software Security
- Routing Network
area: Software Security / Deep Learning / Mixture of Experts (MoE)
datasets:
- Big-Vul
- Devign
- D2A
- ReVeal
models:
- MoEVD
- CodeBERT
- GraphCodeBERT
- Top-k Gating Network
- Mixture of Experts
- Monolithic Transformer Baselines
aliases:
- One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts
  (MoE)
- moevd2025
- artigo_025
tags:
- bibliografia
- alf-moe
- artigo
---

# One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)

> **Citação ABNT Sugerida:** YANG, X.; WANG, S.; ZHOU, J.; ZHU, W.. One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE). In: **Proceedings of the ACM on Software Engineering (PACMSE / FSE 2025), Vol. 2, No. FSE, Article 166, pp. 446-464**, 2025.
> **Chave BibTeX:** `moevd2025` | **Arquivo TXT:** `MoEVD__Enhancing_Vulnerability_Detection_by_Mixture-of-Experts_(MoE)_2025.txt` | **DOI:** `10.1145/3715736`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_025` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Software Security / Deep Learning / Mixture of Experts (MoE) |
| **Veículo de Publicação** | Proceedings of the ACM on Software Engineering (PACMSE / FSE 2025), Vol. 2, No. FSE, Article 166, pp. 446-464 |
| **Datasets Utilizados** | Big-Vul, Devign, D2A, ReVeal |
| **Modelos / Algoritmos** | MoEVD, CodeBERT, GraphCodeBERT, Top-k Gating Network, Mixture of Experts, Monolithic Transformer Baselines |
| **Palavras-Chave** | Mixture of Experts (MoE), Vulnerability Detection, One-for-All Limitation, Deep Learning, Software Security, Routing Network |

## 🎯 Problema Abordado
O paradigma tradicional de modelo único monolítico ('one-for-all') falha na detecção de vulnerabilidades e ameaças porque diferentes tipos de falhas de segurança exigem raciocínio sobre propriedades estruturais e semânticas totalmente distintas; um modelo monolítico sofre com interferência negativa de gradientes (negative transfer) entre classes heterogêneas.

## 🔬 Metodologia
Arquitetura MoEVD empregando Mixture of Experts (MoE) onde múltiplos especialistas neurais são especializados em diferentes categorias de vulnerabilidade e tipos de código, coordenados por uma rede de roteamento que direciona cada amostra aos especialistas mais capacitados.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O MoEVD supera significativamente todos os modelos monolíticos de ponta, alcançando aumento de até 11.2% no F1-score e demonstrando formalmente que a especialização modular elimina o conflito de otimização em dados de segurança heterogêneos.

**Contribuições Centrais:**
- Demonstração empírica e teórica de que modelos monolíticos falham em domínios heterogêneos de segurança.
- Aplicação pioneira de Mixture-of-Experts para discriminação modular de vulnerabilidades.
- Formulação de roteamento com mitigação de colapso de especialistas.

## ⚠️ Limitações Identificadas
Desafio de balanceamento de carga entre os especialistas durante o treinamento para evitar que um pequeno subconjunto de redes domine todas as decisões de roteamento (expert collapse).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Mixture of Experts`, `Falha do Paradigma One-for-All`, `Especialização Modular`, `Roteamento Dinâmico`
- **Problemas Focais:** `Interferência negativa em modelos monolíticos`, `Heterogeneidade extrema de ameaças`
- **Métodos Empregados:** `Redes especialistas desacopladas`, `Rede de roteamento de aprendizado de pesos`, `Perda auxiliar de balanceamento`
- **Modelos e Arquiteturas:** `MoEVD`, `CodeBERT MoE`
- **Bases de Dados:** `Big-Vul`, `Devign`
- **Resultados Chave:** `Ganhos de até 11.2% em F1 frente a modelos monolíticos`
- **Limitações Reconhecidas:** `Risco de subutilização de especialistas sem calibração adequada`
- **Evidências Citáveis:** `EVID_025_01`, `EVID_025_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Conceito:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*
- **Relacionado:**
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{fundamenta_teoria}}$ `[[artigo_025]]`: ALF-MoE baseia-se na comprovação de que modelos 'one-for-all' falham em segurança dada por Yang et al.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Mixture of Experts|Mixture of Experts (MoE)]] — Papel: MoEVD demonstrando que 'One-for-All Does Not Work' em segurança

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_002 — Categoria: Teoria|CLAIM_002 (Teoria)]] — *"Modelos monolíticos concebidos sob uma perspectiva homogênea ou restrita de atributos (single-view) tendem a apresentar desempenho subótimo na detecção de ataques contemporâneos cujas assinaturas residem em múltiplos domínios informacionais distintos."*
  - *Aplicação na Tese:* Sustenta o argumento teórico de falha de modelos 'one-for-all' em segurança.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_003 — Arquitetura Neural de NIDS: Modelos Monolíticos ('One-for-All') vs. Mixture-of-Experts (MoE)|CONTROV_003 — Arquitetura Neural de NIDS: Modelos Monolíticos ('One-for-All') vs. Mixture-of-Experts (MoE)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"Modelos monolíticos 'one-for-all' sofrem interferência negativa de gradientes quando confrontados com distribuições heterogêneas de ataques multimodais; a decomposição modular especializada (MoE) com fusão atencional calibrada supera expressivamente modelos monolíticos."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa CONCEITO:** Heterogeneidade intrínseca do tráfego malicioso em múltiplos domínios
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa FUNDAMENTAÇÃO:** Falha de modelos monolíticos ('One-for-All') por interferência negativa de gradientes

### Clusters Temáticos
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Mixture of Experts|Mixture of Experts]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_025_01` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_025_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Modelos monolíticos que tentam generalizar para todas as classes heterogêneas de segurança sofrem de transferência negativa e subotimização.
> **Localização:** Seção 1 (Introduction) e Seção 2 (Motivation), Páginas 446-449
>
> *"Monolithic one-for-all models inherently struggle with negative gradient interference when forced to learn wildly divergent feature distributions across disparate vulnerability classes, severely impairing overall discriminatory precision."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 2 para fundamentar teoricamente por que modelos monolíticos são inadequados para tráfego heterogêneo de NIDS, justificando a arquitetura MoE.

### `EVID_025_02` — EMPÍRICA
> [!quote] EVID_025_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A divisão modular de conhecimento entre múltiplos especialistas profundos supera consistentemente arquiteturas densas de tamanho equivalente.
> **Localização:** Seção 5 (Experimental Results), Páginas 456-459
>
> *"The MoE architecture achieves statistically significant improvements over single deep networks of equivalent or greater parameter count, confirming that specialization is more effective than raw model capacity."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a escolha da arquitetura MoE frente a modelos monolíticos mais profundos na discussão metodológica da tese.

## 📦 Entrada BibTeX
```bibtex
@inproceedings{moevd2025,
  title = {One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)},
  author = {Yang, Xu and Wang, Shaowei and Zhou, Jiayuan and Zhu, Wenhan},
  year = {2025},
  doi = {10.1145/3715736},
  volume = {2},
  number = {FSE},
  pages = {446-464},
  publisher = {Association for Computing Machinery (ACM)},
  booktitle = {Proceedings of the ACM on Software Engineering}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
