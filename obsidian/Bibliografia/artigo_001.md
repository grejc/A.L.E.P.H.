---
id: artigo_001
title: On Calibration of Modern Neural Networks
authors:
- Chuan Guo
- Geoff Pleiss
- Yu Sun
- Kilian Q. Weinberger
year: 2017
bibtex_key: guo2017calibration
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Proceedings of the 34th International Conference on Machine Learning (ICML
  2017), PMLR 70:1321-1330
keywords:
- Confidence Calibration
- Modern Neural Networks
- Temperature Scaling
- Expected Calibration Error
- Reliability Diagrams
- Vector Scaling
area: Machine Learning / Incerteza e Calibração de Modelos Neurais
datasets:
- CIFAR-10
- CIFAR-100
- SVHN
- ImageNet
- Birds
- Cars
- 20 Newsgroups
models:
- ResNet
- DenseNet
- LeNet
- Temperature Scaling
- Vector Scaling
- Matrix Scaling
- Platt Scaling
- Isotonic Regression
- Histogram Binning
aliases:
- On Calibration of Modern Neural Networks
- guo2017calibration
- artigo_001
tags:
- bibliografia
- alf-moe
- artigo
---

# On Calibration of Modern Neural Networks

> **Citação ABNT Sugerida:** GUO, C.; PLEISS, G.; SUN, Y.; WEINBERGER, K. Q.. On Calibration of Modern Neural Networks. In: **Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR 70:1321-1330**, 2017.
> **Chave BibTeX:** `guo2017calibration` | **Arquivo TXT:** `1706.04599v2.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_001` |
| **Ano** | 2017 |
| **Área de Pesquisa** | Machine Learning / Incerteza e Calibração de Modelos Neurais |
| **Veículo de Publicação** | Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR 70:1321-1330 |
| **Datasets Utilizados** | CIFAR-10, CIFAR-100, SVHN, ImageNet, Birds, Cars, 20 Newsgroups |
| **Modelos / Algoritmos** | ResNet, DenseNet, LeNet, Temperature Scaling, Vector Scaling, Matrix Scaling, Platt Scaling, Isotonic Regression, Histogram Binning |
| **Palavras-Chave** | Confidence Calibration, Modern Neural Networks, Temperature Scaling, Expected Calibration Error, Reliability Diagrams, Vector Scaling |

## 🎯 Problema Abordado
Redes neurais profundas modernas com normalização por lote (Batch Normalization), alta profundidade e menor decaimento de peso alcançam acurácias superiores, porém são mal calibradas (produzem probabilidades superconfiantes que não refletem a verdadeira probabilidade de acerto).

## 🔬 Metodologia
Avaliação sistemática de fatores arquiteturais sobre calibração empírica usando Expected Calibration Error (ECE), Maximum Calibration Error (MCE) e Negative Log-Likelihood (NLL); comparação empírica de métodos pós-processamento de calibração paramétricos e não paramétricos.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Temperature scaling (escalonamento por temperatura com parâmetro único T > 1 aplicado aos logits) reduz drasticamente o ECE (frequentemente para menos de 1%) sem alterar a acurácia ou a ordenação das classes; Vector Scaling estende a formulação afim preservando separabilidade.

**Contribuições Centrais:**
- Descoberta de que redes modernas são significativamente menos calibradas que redes da década de 1990 apesar de maior acurácia.
- Identificação de profundidade, largura e batch normalization como fatores primários de descalibração.
- Demonstração de que Temperature Scaling e Vector Scaling são métodos pós-processamento simples, rápidos e altamente eficazes.

## ⚠️ Limitações Identificadas
A calibração pós-hoc com conjunto de validação estático assume distribuição IID e pode degradar sob deslocamento severo de distribuição (covariate shift) ou ataques adversariais.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Confidence Calibration`, `Expected Calibration Error`, `Temperature Scaling`, `Vector Scaling`, `Reliability Diagrams`
- **Problemas Focais:** `Superconfiança em redes profundas`, `Descalibração induzida por profundidade e batch norm`, `Probabilidades não confiáveis para tomada de decisão crítica`
- **Métodos Empregados:** `Temperature Scaling`, `Vector Scaling`, `Matrix Scaling`, `Histogram Binning`, `Isotonic Regression`
- **Modelos e Arquiteturas:** `ResNet`, `DenseNet`, `LeNet`
- **Bases de Dados:** `CIFAR-100`, `ImageNet`, `SVHN`
- **Resultados Chave:** `Temperature scaling reduz ECE substancialmente sem alterar acurácia top-1`
- **Limitações Reconhecidas:** `Dependência de conjunto de validação representativo e IID`
- **Evidências Citáveis:** `EVID_001_01`, `EVID_001_02`, `EVID_001_03`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
  - [[artigo_029]] — *Neural Networks and Cyber Resilience: Deep Insights into AI Architectures for Robust Security Framework*

### Citações e Relações Recebidas na Base (Incoming)
- **Utiliza:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_029]] — *Neural Networks and Cyber Resilience: Deep Insights into AI Architectures for Robust Security Framework*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_001]]`: ALF-MoE utiliza Vector Scaling e teoria de calibração afim de probabilidades de Guo et al. no módulo de gating.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Calibracao de Confianca|Calibração de Probabilidades e Confiabilidade]] — 🌟 **Definição Canônica**

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_004 — Categoria: Metodologia|CLAIM_004 (Metodologia)]] — *"Redes neurais profundas modernas com alta profundidade, largura e batch normalization tendem a ser superconfiantes e descalibradas, produzindo probabilidades que não refletem a verdadeira confiança preditiva e necessitando de técnicas de calibração pós-hoc afins como Temperature Scaling e Vector Scaling."*
  - *Aplicação na Tese:* Fundamenta teoricamente a inclusão da calibração afim por Vector Scaling no módulo de gating do ALF-MoE (Capítulo 1 e 3).

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa MÉTODO:** Arquitetura ALF-MoE com 5 especialistas (DNN, CNN, GRU, CAE, LSTM) e fusão aprendível calibrada

### Clusters Temáticos
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Calibracao Probabilistica|Calibracao Probabilistica]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_001_01` — DEFINIÇÃO
> [!quote] EVID_001_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição formal de calibração de confiança probabilística em classificadores.
> **Localização:** Seção 2 (Definitions), Página 2
>
> *"Perfect calibration is defined as P(Y = y | P^ = p) = p for all p in [0, 1]. In other words, the confidence score represents a true probability of correctness."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a definição matemática de calibração no módulo de gating calibrado do ALF-MoE (Capítulo 2 e 3).

### `EVID_001_02` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_001_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Redes neurais profundas modernas tendem a ser superconfiantes e descalibradas devido a profundidade, largura e batch normalization.
> **Localização:** Seção 1 (Introduction) e Seção 3 (Observed Miscalibration), Páginas 1-3
>
> *"Depth, width, weight decay, and Batch Normalization are important factors influencing model calibration. While improvements in accuracy have been dramatic, modern neural networks are significantly less well-calibrated than older networks."*
>
> **Aplicabilidade na Tese ALF-MoE:** Justifica por que os escores de saída dos especialistas profundos (DNN, CNN, GRU, CAE, LSTM) não devem ser diretamente combinados sem mecanismo de calibração ou atenção aprendível.

### `EVID_001_03` — METODOLÓGICA
> [!quote] EVID_001_03 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Vector Scaling e Temperature Scaling utilizam transformações afins sobre os logits para restaurar a calibração probabilística.
> **Localização:** Seção 4.2 (Parametric Methods), Página 4
>
> *"Vector scaling extends Platt scaling to multi-class problems: z_i = W z_i + b where W is a diagonal matrix. Temperature scaling is the simplest variant where W = (1/T) I."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fornece o embasamento metodológico exato para a formulação da equação de gating do ALF-MoE com transformação afim W_g e vetor de viés b_g.

### `EVID_001_04` — EMPÍRICA
> [!quote] EVID_001_04 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A calibração pós-processamento por Temperature Scaling reduz significativamente o Expected Calibration Error (ECE) sem alterar ou degradar a acurácia de classificação.
> **Localização:** Seção 4.2 (Temperature Scaling) e Seção 5 (Results), Páginas 4-6
>
> *"Because the parameter T does not change the maximum of the softmax function, the class prediction remains unchanged. In other words, temperature scaling does not affect the model's accuracy... Temperature scaling is surprisingly effective at reducing Expected Calibration Error (ECE)."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a constatação de que calibrar as predições probabilísticas otimiza o ECE e a confiabilidade das saídas sem perda na acurácia do modelo.

## 📦 Entrada BibTeX
```bibtex
@inproceedings{guo2017calibration,
  title = {On Calibration of Modern Neural Networks},
  author = {Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q.},
  booktitle = {International Conference on Machine Learning (ICML)},
  pages = {1321--1330},
  year = {2017},
  organization = {PMLR}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
