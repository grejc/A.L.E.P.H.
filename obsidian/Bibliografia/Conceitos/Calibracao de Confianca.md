---
id: Calibracao de Confianca
term: Calibração de Probabilidades e Confiabilidade
aliases:
- Confidence Calibration
- Probability Calibration
- Temperature Scaling
- Vector Scaling
- Expected Calibration Error
- ECE
- Calibração de Probabilidades e Confiabilidade
- Calibracao de Confianca
tags:
- conceito
- bibliografia
- alf-moe
---

# Calibração de Probabilidades e Confiabilidade

> **Sinônimos e Variantes:** Confidence Calibration, Probability Calibration, Temperature Scaling, Vector Scaling, Expected Calibration Error, ECE

## 📖 Definição Canônica
Propriedade de um classificador onde a probabilidade atribuída a uma classe predita corresponde exatamente à frequência empírica relativa de acerto (P(Y = y | P^ = p) = p).

- **Artigo de Definição Formal:** [[artigo_001]] — *On Calibration of Modern Neural Networks*
- **Evidência Canônica:** `EVID_001_01` (Seção 2 (Definitions), Página 2)
> [!quote] Evidência Canônica (`EVID_001_01`)
> *"Perfect calibration is defined as P(Y = y | P^ = p) = p for all p in [0, 1]. In other words, the confidence score represents a true probability of correctness."*
>
> **Afirmação:** Definição formal de calibração de confiança probabilística em classificadores.
>
> **Aplicação na Tese:** Fundamenta a definição matemática de calibração no módulo de gating calibrado do ALF-MoE (Capítulo 2 e 3).

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_001]] — *On Calibration of Modern Neural Networks* | 5/5 | Fundamento seminal de calibração em redes neurais modernas |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Calibração afim por Vector Scaling no módulo de gating do ALF-MoE |

## 🔍 Evidências Literais Associadas
### `EVID_001_01` — DEFINIÇÃO (Fonte: [[artigo_001]])
> [!quote] EVID_001_01
> **Localização:** Seção 2 (Definitions), Página 2
> **Afirmação Sustentada:** Definição formal de calibração de confiança probabilística em classificadores.
>
> *"Perfect calibration is defined as P(Y = y | P^ = p) = p for all p in [0, 1]. In other words, the confidence score represents a true probability of correctness."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta a definição matemática de calibração no módulo de gating calibrado do ALF-MoE (Capítulo 2 e 3).

### `EVID_001_02` — FUNDAMENTAÇÃO TEÓRICA (Fonte: [[artigo_001]])
> [!quote] EVID_001_02
> **Localização:** Seção 1 (Introduction) e Seção 3 (Observed Miscalibration), Páginas 1-3
> **Afirmação Sustentada:** Redes neurais profundas modernas tendem a ser superconfiantes e descalibradas devido a profundidade, largura e batch normalization.
>
> *"Depth, width, weight decay, and Batch Normalization are important factors influencing model calibration. While improvements in accuracy have been dramatic, modern neural networks are significantly less well-calibrated than older networks."*
>
> **Aplicação Tese ALF-MoE:** Justifica por que os escores de saída dos especialistas profundos (DNN, CNN, GRU, CAE, LSTM) não devem ser diretamente combinados sem mecanismo de calibração ou atenção aprendível.

### `EVID_001_03` — METODOLÓGICA (Fonte: [[artigo_001]])
> [!quote] EVID_001_03
> **Localização:** Seção 4.2 (Parametric Methods), Página 4
> **Afirmação Sustentada:** Vector Scaling e Temperature Scaling utilizam transformações afins sobre os logits para restaurar a calibração probabilística.
>
> *"Vector scaling extends Platt scaling to multi-class problems: z_i = W z_i + b where W is a diagonal matrix. Temperature scaling is the simplest variant where W = (1/T) I."*
>
> **Aplicação Tese ALF-MoE:** Fornece o embasamento metodológico exato para a formulação da equação de gating do ALF-MoE com transformação afim W_g e vetor de viés b_g.

### `EVID_004_02` — METODOLÓGICA (Fonte: [[artigo_004]])
> [!quote] EVID_004_02
> **Localização:** Seção 2.3 (Attention-Based Learnable Fusion and Gating), Páginas 6-7
> **Afirmação Sustentada:** Formulação matemática da fusão aprendível baseada em atenção logarítmica e calibração por Vector Scaling.
>
> *"The attention weights are computed as a = softmax(W_g log(alpha + epsilon) + b_g), allowing the network to dynamically learn cross-expert dependencies, followed by affine probability calibration."*
>
> **Aplicação Tese ALF-MoE:** Sustenta diretamente as Equações do Capítulo 1 e Capítulo 3 sobre o mecanismo de roteamento e fusão do ALF-MoE.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
