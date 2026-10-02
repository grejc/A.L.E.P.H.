---
id: Convolutional Autoencoder (CAE)
term: Convolutional Autoencoder (CAE) e Detecção de Anomalias
aliases:
- CAE
- Autoencoder Convolucional
- Unsupervised Anomaly Detection
- Reconstruction Error
- HSAE
- Convolutional Autoencoder (CAE) e Detecção de Anomalias
- Convolutional Autoencoder (CAE)
tags:
- conceito
- bibliografia
- alf-moe
---

# Convolutional Autoencoder (CAE) e Detecção de Anomalias

> **Sinônimos e Variantes:** CAE, Autoencoder Convolucional, Unsupervised Anomaly Detection, Reconstruction Error, HSAE

## 📖 Definição Canônica
Rede neural composta por um codificador convolucional que comprime os dados de entrada em uma representação de gargalo latente e um decodificador que reconstrói o sinal original; anomalias são detectadas por elevados erros quadráticos de reconstrução sob distribuição legítima.

- **Artigo de Definição Formal:** [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Evidência Canônica:** `EVID_048_01` (Seção 3 (Convolutional Autoencoder Architecture), Páginas 3-5)
> [!quote] Evidência Canônica (`EVID_048_01`)
> *"Convolutional autoencoders leverage localized spatial weight sharing to filter out ambient measurement noise while encoding essential traffic structure into a highly compressed bottleneck representation."*
>
> **Afirmação:** Convolutional Autoencoders (CAE) oferecem representações comprimidas robustas a ruídos e perturbações morfológicas locais em dados de fluxo de rede.
>
> **Aplicação na Tese:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha do Convolutional Autoencoder (CAE) como o especialista dedicado a representações comprimidas e perdas de reconstrução no ALF-MoE.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Especialista CAE no ALF-MoE com janela de Hann e RFFT |
| [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble* | 5/5 | HSAE e ensemble de autoencoders para ataques zero-day |
| [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems* | 5/5 | CAE para NIDS robusto em hardware embarcado |

## 🔍 Evidências Literais Associadas
### `EVID_021_01` — FUNDAMENTAÇÃO TEÓRICA (Fonte: [[artigo_021]])
> [!quote] EVID_021_01
> **Localização:** Capítulo 2 (Fundamentação Teórica), Seção 2.4, Páginas 32-36
> **Afirmação Sustentada:** Autoencoders treinados exclusivamente sobre tráfego benigno detectam ataques inéditos (zero-day) através do aumento do erro de reconstrução.
>
> *"Ao treinar o autoencoder exclusivamente com fluxos legítimos, a rede aprende a variedade compacta do comportamento benigno; anomalias e ataques zero-day desviam dessa distribuição gerando erros de reconstrução estatisticamente superiores ao limiar estabelecido."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta o princípio de funcionamento do especialista CAE (Convolutional Autoencoder) do ALF-MoE para modelar desvios de normalidade.

### `EVID_048_01` — METODOLÓGICA (Fonte: [[artigo_048]])
> [!quote] EVID_048_01
> **Localização:** Seção 3 (Convolutional Autoencoder Architecture), Páginas 3-5
> **Afirmação Sustentada:** Convolutional Autoencoders (CAE) oferecem representações comprimidas robustas a ruídos e perturbações morfológicas locais em dados de fluxo de rede.
>
> *"Convolutional autoencoders leverage localized spatial weight sharing to filter out ambient measurement noise while encoding essential traffic structure into a highly compressed bottleneck representation."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha do Convolutional Autoencoder (CAE) como o especialista dedicado a representações comprimidas e perdas de reconstrução no ALF-MoE.

### `EVID_048_02` — EMPÍRICA (Fonte: [[artigo_048]])
> [!quote] EVID_048_02
> **Localização:** Seção 5 (Experimental Performance and Benchmarking), Páginas 7-10
> **Afirmação Sustentada:** O erro de reconstrução de autoencoders convolucionais proporciona excelente separabilidade de anomalias com pegada de memória mínima compatível com dispositivos de borda.
>
> *"The proposed 1D-CAE achieves an AUC-ROC of 0.984 on the CIC-IDS-2017 dataset requiring less than 45 KB of memory, substantially outperforming dense autoencoders and classical tree models in constrained embedded deployments."*
>
> **Aplicação Tese ALF-MoE:** Evidência experimental para sustentar a viabilidade e eficácia do especialista CAE na tese.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
