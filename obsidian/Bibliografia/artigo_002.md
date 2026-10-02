---
id: artigo_002
title: 'Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection'
authors:
- Tongtong Feng
- Qi Qi
- Lingqi Guo
- Jingyu Wang
year: 2024
bibtex_key: feng2024metauad
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: arXiv preprint arXiv:2408.17031
keywords:
- Network Traffic Anomaly Detection
- Meta-Learning
- Few-Shot Learning
- User-Level Heterogeneity
area: Network Intrusion Detection / Meta-Learning / Traffic Anomaly Detection
datasets:
- Tráfego real de rede de campus corporativo / ISP
- ISCX-IDS2012
models:
- Model-Agnostic Meta-Learning (MAML)
- Multi-Layer Perceptron (MLP)
- Convolutional Neural Network (CNN)
aliases:
- 'Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection'
- feng2024metauad
- artigo_002
tags:
- bibliografia
- alf-moe
- artigo
---

# Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection

> **Citação ABNT Sugerida:** FENG, T.; QI, Q.; GUO, L.; WANG, J.. Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection. In: **arXiv preprint arXiv:2408.17031**, 2024.
> **Chave BibTeX:** `feng2024metauad` | **Arquivo TXT:** `2408.17031v2.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_002` |
| **Ano** | 2024 |
| **Área de Pesquisa** | Network Intrusion Detection / Meta-Learning / Traffic Anomaly Detection |
| **Veículo de Publicação** | arXiv preprint arXiv:2408.17031 |
| **Datasets Utilizados** | Tráfego real de rede de campus corporativo / ISP, ISCX-IDS2012 |
| **Modelos / Algoritmos** | Model-Agnostic Meta-Learning (MAML), Multi-Layer Perceptron (MLP), Convolutional Neural Network (CNN) |
| **Palavras-Chave** | Network Traffic Anomaly Detection, Meta-Learning, Few-Shot Learning, User-Level Heterogeneity |

## 🎯 Problema Abordado
A heterogeneidade comportamental do tráfego entre usuários e a escassez de dados rotulados para novos usuários degradam a generalização dos modelos clássicos de detecção de anomalias.

## 🔬 Metodologia
Framework Meta-UAD baseado em meta-aprendizado (MAML) com redes neurais que aprendem inicializações de parâmetros rapidamente adaptáveis a novos perfis de tráfego de rede a partir de poucas amostras.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O Meta-UAD atinge alta acurácia com apenas 5 a 10 pacotes rotulados por perfil de usuário, superando métodos puramente supervisionados ou transfer learning convencional em cenários de alta heterogeneidade.

**Contribuições Centrais:**
- Formulação do problema de detecção de anomalias em nível de usuário sob heterogeneidade comportamental.
- Arquitetura meta-learning rápida adaptável com poucas amostras.
- Demonstração empírica de robustez contra desvios de perfil de tráfego.

## ⚠️ Limitações Identificadas
Requer etapa de meta-treinamento com histórico representativo de múltiplos perfis e custo computacional adicional durante o meta-ajuste.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Meta-Learning`, `User Heterogeneity`, `Traffic Anomaly Detection`
- **Problemas Focais:** `Heterogeneidade de perfis de usuário`, `Poucos dados rotulados por usuário`
- **Métodos Empregados:** `Meta-UAD`, `MAML`, `Few-shot fine-tuning`
- **Modelos e Arquiteturas:** `CNN`, `MLP adaptativo`
- **Bases de Dados:** `Tráfego de campus`, `ISCX-IDS2012`
- **Resultados Chave:** `Adaptação com 5-10 amostras superando baselines supervisionados`
- **Limitações Reconhecidas:** `Custo de meta-treinamento prévio`
- **Evidências Citáveis:** `EVID_002_01`, `EVID_002_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*

## 🎓 Integração com a Tese ALF-MoE

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa LACUNA:** Mecanismos de aprendizado contínuo adaptativo para NIDS em produção

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_002_01` — MOTIVAÇÃO
> [!quote] EVID_002_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A heterogeneidade de padrões de tráfego na rede invalida a hipótese de distribuição única para todos os fluxos.
> **Localização:** Seção 1 (Introduction), Página 1
>
> *"User-level network traffic patterns exhibit extreme heterogeneity, making one-size-fits-all models ineffective when deployed across diverse user behaviors."*
>
> **Aplicabilidade na Tese ALF-MoE:** Reforça a motivação de que uma única representação ou modelo monolítico é incapaz de capturar a heterogeneidade intrínseca de redes modernas.

### `EVID_002_02` — EMPÍRICA
> [!quote] EVID_002_02 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Abordagens de meta-aprendizado superam classificadores estáticos em cenários com escassez de dados para classes raras ou novas.
> **Localização:** Seção 5 (Experiments and Results), Página 4
>
> *"Meta-UAD achieves up to 14.2% higher F1-score than baseline deep learning models when only five labeled flows per class are available."*
>
> **Aplicabilidade na Tese ALF-MoE:** Serve de suporte para a discussão sobre robustez em classes minoritárias e adaptação a variações contextuais de rede.

## 📦 Entrada BibTeX
```bibtex
@article{feng2024metauad,
  title = {{Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection}},
  author = {Tongtong Feng and Qi Qi and Lingqi Guo and Jingyu Wang},
  journal = {arXiv preprint arXiv:2408.17031},
  year = {2024},
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
