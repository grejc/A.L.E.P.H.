---
id: NFStream Framework
term: NFStream Framework de Analise de Fluxo
aliases:
- NFStream
- Flow Extraction Engine
- Real-Time DPI Framework
- NFStream Framework de Analise de Fluxo
- NFStream Framework
tags:
- conceito
- bibliografia
- alf-moe
---

# NFStream Framework de Analise de Fluxo

> **Sinônimos e Variantes:** NFStream, Flow Extraction Engine, Real-Time DPI Framework

## 📖 Definição Canônica
Framework open-source em Python e C de alto desempenho para extração, agregação e rotulagem de fluxos de rede bidirecionais em tempo real.

- **Artigo de Definição Formal:** [[artigo_026]] — *NFStream: A flexible network data analysis framework*
- **Evidência Canônica:** `EVID_026_02` (Seção 1 (Introduction) e Seção 3 (NFStream Architecture), Páginas 1-6)
> [!quote] Evidência Canônica (`EVID_026_02`)
> *"NFStream provides a flexible network data analysis framework designed to eliminate unreliability in legacy measurement tools, delivering high-speed bidirectional feature extraction directly compatible with modern machine learning libraries."*
>
> **Afirmação:** O NFStream fornece um framework robusto, flexível e reproduzível para extração em tempo real de atributos estatísticos e temporais para pipelines de ML.
>
> **Aplicação na Tese:** Fundamenta a escolha do pipeline de ingestão e extração de atributos no Capítulo 3 e Capítulo 4 (Pipeline de Inferência) da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Ingestão e preparação de dados do pipeline |
| [[artigo_026]] — *NFStream: A flexible network data analysis framework* | 5/5 | Trabalho seminal que desenvolveu o NFStream |

## 🔍 Evidências Literais Associadas
### `EVID_026_01` — DEFINIÇÃO (Fonte: [[artigo_026]])
> [!quote] EVID_026_01
> **Localização:** Seção 2 (Traffic Flow Measurement and Concepts), Páginas 2-4
> **Afirmação Sustentada:** Definição de fluxos de rede bidirecionais e agregação de propriedades estatísticas e temporais como unidade analítica padrão.
>
> *"A bidirectional network flow is defined as a sequence of packets sharing the same 5-tuple (source IP, destination IP, source port, destination port, transport protocol) within a specified temporal activity timeout, capturing symmetrical client-server conversational dynamics."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para definir formalmente fluxos bidirecionais de rede na tese.

### `EVID_026_02` — METODOLÓGICA (Fonte: [[artigo_026]])
> [!quote] EVID_026_02
> **Localização:** Seção 1 (Introduction) e Seção 3 (NFStream Architecture), Páginas 1-6
> **Afirmação Sustentada:** O NFStream fornece um framework robusto, flexível e reproduzível para extração em tempo real de atributos estatísticos e temporais para pipelines de ML.
>
> *"NFStream provides a flexible network data analysis framework designed to eliminate unreliability in legacy measurement tools, delivering high-speed bidirectional feature extraction directly compatible with modern machine learning libraries."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta a escolha do pipeline de ingestão e extração de atributos no Capítulo 3 e Capítulo 4 (Pipeline de Inferência) da tese.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
