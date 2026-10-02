---
id: CIC-IDS-2017 Dataset
term: Dataset Benchmark CIC-IDS-2017
aliases:
- CIC-IDS-2017
- CICIDS2017
- PCAP 2017 Benchmark
- UNB Dataset
- Dataset Benchmark CIC-IDS-2017
- CIC-IDS-2017 Dataset
tags:
- conceito
- bibliografia
- alf-moe
---

# Dataset Benchmark CIC-IDS-2017

> **Sinônimos e Variantes:** CIC-IDS-2017, CICIDS2017, PCAP 2017 Benchmark, UNB Dataset

## 📖 Definição Canônica
Dataset de referência internacional desenvolvido pelo Canadian Institute for Cybersecurity contendo 5 dias de tráfego, 2.8 milhões de fluxos e 14 classes de ataque contemporâneas sob perfis B-Profile e M-Profile.

- **Artigo de Definição Formal:** [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- **Evidência Canônica:** `EVID_041_02` (Seção 4 (Attack Scenarios and Profiles), Páginas 112-114)
> [!quote] Evidência Canônica (`EVID_041_02`)
> *"CIC-IDS-2017 covers modern attack profiles including Brute Force, Heartbleed, Botnet, DoS, DDoS, Web Attacks, and Infiltration, extracted across five continuous days of network interaction."*
>
> **Afirmação:** O dataset CIC-IDS-2017 foi concebido para capturar tráfego de rede moderno e 14 classes de ataque contemporâneas refletindo redes corporativas reais.
>
> **Aplicação na Tese:** Artigo primário de citação obrigatória ao apresentar o benchmark CIC-IDS-2017 utilizado nos experimentos da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Benchmark primário avaliado pelo ALF-MoE |
| [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* | 5/5 | Estudo comparativo e sanitização do CIC-IDS-2017 |
| [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization* | 5/5 | Trabalho seminal que criou o CIC-IDS-2017 |

## 🔍 Evidências Literais Associadas
### `EVID_041_01` — DEFINIÇÃO (Fonte: [[artigo_041]])
> [!quote] EVID_041_01
> **Localização:** Seção 2 (Eleven Criteria for a Valid Dataset), Páginas 109-111
> **Afirmação Sustentada:** Definição dos 11 critérios necessários para que um conjunto de dados de detecção de intrusão seja considerado válido e representativo.
>
> *"A valid intrusion detection dataset must satisfy eleven fundamental criteria: Complete Network Configuration, Complete Traffic, Labeled Flows, Complete Interaction, Capture Complete, Diverse Protocols, Attack Diversity, Anonymity, Heterogeneity, Feature Set, and Metadata."*
>
> **Aplicação Tese ALF-MoE:** Fundamenta a discussão metodológica sobre seleção de datasets e requisitos de representatividade no Capítulo 2 e Capítulo 3.

### `EVID_041_02` — ESTADO DA ARTE (Fonte: [[artigo_041]])
> [!quote] EVID_041_02
> **Localização:** Seção 4 (Attack Scenarios and Profiles), Páginas 112-114
> **Afirmação Sustentada:** O dataset CIC-IDS-2017 foi concebido para capturar tráfego de rede moderno e 14 classes de ataque contemporâneas refletindo redes corporativas reais.
>
> *"CIC-IDS-2017 covers modern attack profiles including Brute Force, Heartbleed, Botnet, DoS, DDoS, Web Attacks, and Infiltration, extracted across five continuous days of network interaction."*
>
> **Aplicação Tese ALF-MoE:** Artigo primário de citação obrigatória ao apresentar o benchmark CIC-IDS-2017 utilizado nos experimentos da tese.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
