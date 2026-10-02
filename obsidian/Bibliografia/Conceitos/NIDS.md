---
id: NIDS
term: Network Intrusion Detection System (NIDS)
aliases:
- NIDS
- Network-based IDS
- Sistema de Detecção de Intrusão em Redes
- Intrusion Detection System
- IDS de rede
- Network Intrusion Detection System (NIDS)
- NIDS
tags:
- conceito
- bibliografia
- alf-moe
---

# Network Intrusion Detection System (NIDS)

> **Sinônimos e Variantes:** NIDS, Network-based IDS, Sistema de Detecção de Intrusão em Redes, Intrusion Detection System, IDS de rede

## 📖 Definição Canônica
Sistema de segurança que monitora e analisa o tráfego de rede para identificar atividades suspeitas, acessos não autorizados e violações de políticas de segurança.

- **Artigo de Definição Formal:** [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- **Evidência Canônica:** `EVID_006_01` (Seção 1 (Introduction) e Seção 2 (Background), Páginas 1-3)
> [!quote] Evidência Canônica (`EVID_006_01`)
> *"Flow-based NIDS analyze statistical and temporal properties aggregated over network connections (flows) rather than inspecting raw payload, enabling scalability and compliance with pervasive end-to-end encryption."*
>
> **Afirmação:** Definição de NIDS baseados em fluxo de rede e por que eles substituem a inspeção profunda de pacotes (DPI).
>
> **Aplicação na Tese:** Citação direta para embasar a definição e necessidade de NIDS baseados em fluxo no Capítulo 1 e Capítulo 2 da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Arquitetura ALF-MoE para NIDS |
| [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* | 5/5 | Definição formal de NIDS baseado em fluxos |
| [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas* | 5/5 | NIDS distribuído em computação de nevoeiro |
| [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model* | 5/5 | NIDS recorrente híbrido GRU-BiLSTM |
| [[artigo_026]] — *NFStream: A flexible network data analysis framework* | 5/5 | Framework de análise de tráfego para NIDS |
| [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems* | 5/5 | Datasets padronizados de NetFlow para NIDS |
| [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4* | 5/5 | NIDS de alto desempenho em P4 |
| [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso* | 5/5 | NIDS híbrido em tempo real em SDN |
| [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* | 5/5 | Análise temporal e avaliação de NIDS |
| [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* | 5/5 | Engenharia de atributos temporais para NIDS |
| [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization* | 5/5 | Dataset benchmark CIC-IDS-2017 para NIDS |
| [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets* | 5/5 | Padronização de atributos para NIDS |
| [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU* | 5/5 | Modelo CNN-GRU para NIDS |
| [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems* | 5/5 | Autoencoder convolucional para NIDS embarcado |

## 🔍 Evidências Literais Associadas
### `EVID_006_01` — DEFINIÇÃO (Fonte: [[artigo_006]])
> [!quote] EVID_006_01
> **Localização:** Seção 1 (Introduction) e Seção 2 (Background), Páginas 1-3
> **Afirmação Sustentada:** Definição de NIDS baseados em fluxo de rede e por que eles substituem a inspeção profunda de pacotes (DPI).
>
> *"Flow-based NIDS analyze statistical and temporal properties aggregated over network connections (flows) rather than inspecting raw payload, enabling scalability and compliance with pervasive end-to-end encryption."*
>
> **Aplicação Tese ALF-MoE:** Citação direta para embasar a definição e necessidade de NIDS baseados em fluxo no Capítulo 1 e Capítulo 2 da tese.

### `EVID_013_01` — DEFINIÇÃO (Fonte: [[artigo_013]])
> [!quote] EVID_013_01
> **Localização:** Capítulo 2 (Fundamentação Teórica), Seção 2.3, Páginas 45-48
> **Afirmação Sustentada:** Definição de defesa em profundidade e arquitetura de detecção de intrusão hierárquica em infraestruturas distribuídas.
>
> *"A defesa em profundidade em ambientes distribuídos requer múltiplos anéis de segurança, posicionando sensores de monitoramento de fluxo nas bordas locais e concentradores analíticos em camadas intermediárias para minimizar o tempo de propagação do ataque."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta a contextualização de sistemas distribuídos e defesa em profundidade no Capítulo 1 e Capítulo 2 da tese.

### `EVID_030_01` — DEFINIÇÃO (Fonte: [[artigo_030]])
> [!quote] EVID_030_01
> **Localização:** Seção 1 (Introduction) e Seção 2 (P4 Background), Páginas 355-358
> **Afirmação Sustentada:** Definição de planos de dados programáveis em P4 como tecnologia chave para monitoramento e mitigação em alta taxa de transferência.
>
> *"The P4 programming language enables software-defined data planes to inspect, parse, and manipulate packets directly at line-rate within network switches, eliminating CPU packet drop bottlenecks."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 2 para embasar arquiteturas de monitoramento de alta taxa e defesa em profundidade.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
