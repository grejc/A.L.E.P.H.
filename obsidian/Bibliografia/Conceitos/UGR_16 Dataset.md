---
id: UGR_16 Dataset
term: Dataset UGR'16 e Ciclostacionariedade
aliases:
- UGR'16
- UGR16
- ISP Capture Dataset
- Cyclostationarity Benchmark
- Dataset UGR'16 e Ciclostacionariedade
- UGR_16 Dataset
tags:
- conceito
- bibliografia
- alf-moe
---

# Dataset UGR'16 e Ciclostacionariedade

> **Sinônimos e Variantes:** UGR'16, UGR16, ISP Capture Dataset, Cyclostationarity Benchmark

## 📖 Definição Canônica
Dataset capturado durante 4 meses contínuos em um provedor de Internet (ISP) para avaliação de anomalias cíclicas e detecção no domínio da frequência.

- **Artigo de Definição Formal:** [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*
- **Evidência Canônica:** `EVID_045_01` (Seção 2 (Cyclostationarity in Network Traffic), Páginas 413-415)
> [!quote] Evidência Canônica (`EVID_045_01`)
> *"Network traffic exhibits cyclostationary properties where statistical moments vary periodically across daily, hourly, and weekly operational cycles, making frequency-domain representations optimal for capturing periodic baseline dynamics and harmonic disturbances."*
>
> **Afirmação:** Definição de tráfego de rede como um processo estocástico ciclostacionário que exibe padrões periódicos e harmônicos no domínio da frequência.
>
> **Aplicação na Tese:** Citação direta no Capítulo 1 (item 4) e Capítulo 3 para fundamentar teoricamente a inclusão do especialista no domínio da frequência (CAE com janela de Hann e RFFT) no ALF-MoE.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Fundamento para o especialista de frequência do ALF-MoE |
| [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs* | 5/5 | Trabalho seminal que introduziu o UGR'16 |

## 🔍 Evidências Literais Associadas
### `EVID_045_01` — DEFINIÇÃO (Fonte: [[artigo_045]])
> [!quote] EVID_045_01
> **Localização:** Seção 2 (Cyclostationarity in Network Traffic), Páginas 413-415
> **Afirmação Sustentada:** Definição de tráfego de rede como um processo estocástico ciclostacionário que exibe padrões periódicos e harmônicos no domínio da frequência.
>
> *"Network traffic exhibits cyclostationary properties where statistical moments vary periodically across daily, hourly, and weekly operational cycles, making frequency-domain representations optimal for capturing periodic baseline dynamics and harmonic disturbances."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 (item 4) e Capítulo 3 para fundamentar teoricamente a inclusão do especialista no domínio da frequência (CAE com janela de Hann e RFFT) no ALF-MoE.

### `EVID_045_02` — EMPÍRICA (Fonte: [[artigo_045]])
> [!quote] EVID_045_02
> **Localização:** Seção 5 (Attack Detection and Evaluation), Páginas 418-422
> **Afirmação Sustentada:** O dataset UGR'16 comprova que ataques volumétricos e varreduras causam distorções agudas na densidade espectral do tráfego.
>
> *"Empirical results on the four-month ISP capture demonstrate that malicious intrusions such as DoS and port scans manifest as significant structural deviations in spectral density components, distinctly separating from benign cyclostationary trends."*
>
> **Aplicação Tese ALF-MoE:** Sustenta o uso de Transformada de Fourier (RFFT) e filtragem frequencial para discriminação de ataques em redes de alta taxa.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
