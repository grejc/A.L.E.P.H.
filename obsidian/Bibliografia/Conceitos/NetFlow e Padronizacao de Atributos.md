---
id: NetFlow e Padronizacao de Atributos
term: NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos
aliases:
- NetFlow
- NetFlow v9
- IPFIX
- Standard Feature Set
- 43 Features
- Flow Formats
- NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos
- NetFlow e Padronizacao de Atributos
tags:
- conceito
- bibliografia
- alf-moe
---

# NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos

> **Sinônimos e Variantes:** NetFlow, NetFlow v9, IPFIX, Standard Feature Set, 43 Features, Flow Formats

## 📖 Definição Canônica
Formato aberto e padronizado pela IETF para exportação e contabilização de metadados agregados de conexões IP em roteadores de rede, sem violação de privacidade de payload.

- **Artigo de Definição Formal:** [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- **Evidência Canônica:** `EVID_027_01` (Seção 2 (NetFlow Protocol Overview), Páginas 119-121)
> [!quote] Evidência Canônica (`EVID_027_01`)
> *"NetFlow is an industry-standard network protocol developed by Cisco for collecting IP operational traffic metadata, exporting structured records containing packet counts, byte volumes, interface identifiers, and temporal durations without exposing payload contents."*
>
> **Afirmação:** Definição do formato NetFlow v9 / IPFIX como padrão industrial para exportação e análise de tráfego de rede.
>
> **Aplicação na Tese:** Fundamenta a definição e a relevância de NetFlow no Capítulo 1 e Capítulo 2 da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems* | 5/5 | Conversão de datasets para o padrão NetFlow v9 |
| [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* | 5/5 | Análise temporal de bases NetFlow |
| [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* | 5/5 | Extensão temporal de NetFlow |
| [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets* | 5/5 | Definição formal do NetFlow Standard Feature Set de 43 atributos |

## 🔍 Evidências Literais Associadas
### `EVID_027_01` — DEFINIÇÃO (Fonte: [[artigo_027]])
> [!quote] EVID_027_01
> **Localização:** Seção 2 (NetFlow Protocol Overview), Páginas 119-121
> **Afirmação Sustentada:** Definição do formato NetFlow v9 / IPFIX como padrão industrial para exportação e análise de tráfego de rede.
>
> *"NetFlow is an industry-standard network protocol developed by Cisco for collecting IP operational traffic metadata, exporting structured records containing packet counts, byte volumes, interface identifiers, and temporal durations without exposing payload contents."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta a definição e a relevância de NetFlow no Capítulo 1 e Capítulo 2 da tese.

### `EVID_043_01` — DEFINIÇÃO (Fonte: [[artigo_043]])
> [!quote] EVID_043_01
> **Localização:** Seção 3 (The Proposed Standard Feature Set), Páginas 360-363
> **Afirmação Sustentada:** Definição do conjunto padronizado NetFlow de 43 atributos como solução para a fragmentação e incompatibilidade de datasets de NIDS.
>
> *"We propose a standard feature set of 43 features based on the NetFlow format that preserves the core predictive information while drastically reducing feature dimensionality across diverse intrusion datasets."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha e padronização do espaço de entrada de atributos tabulares na tese.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
