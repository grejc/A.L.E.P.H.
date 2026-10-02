---
id: CICIoT2023 Dataset
term: Dataset Benchmark CICIoT2023
aliases:
- CICIoT2023
- CIC IoT 2023
- IoT Benchmark 105 Devices
- Dataset Benchmark CICIoT2023
- CICIoT2023 Dataset
tags:
- conceito
- bibliografia
- alf-moe
---

# Dataset Benchmark CICIoT2023

> **Sinônimos e Variantes:** CICIoT2023, CIC IoT 2023, IoT Benchmark 105 Devices

## 📖 Definição Canônica
Conjunto de dados de larga escala para segurança em IoT capturado em bancada física com 105 dispositivos reais sob 33 classes de ataques em 7 perfis operacionais.

- **Artigo de Definição Formal:** [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Evidência Canônica:** `EVID_009_02` (Seção 4 (CICIoT2023 Dataset Structure), Páginas 8-11)
> [!quote] Evidência Canônica (`EVID_009_02`)
> *"The testbed incorporates 105 physical IoT devices across multiple vendors and architectures, capturing real-world interactions and executing 33 distinct attack types across 7 categories."*
>
> **Afirmação:** O dataset CICIoT2023 contém 33 tipos distintos de ataques executados em 105 dispositivos IoT de hardware real.
>
> **Aplicação na Tese:** Serve como citação canônica para a descrição dos dados de benchmark IoT na seção de metodologia da tese.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Avaliação do ALF-MoE em ataques de IoT |
| [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks* | 5/5 | Classificação CNN-LSTM no CICIoT2023 |
| [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic* | 5/5 | Mecanismo de atenção aplicado ao CICIoT2023 |
| [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment* | 5/5 | Trabalho seminal que concebeu o CICIoT2023 |

## 🔍 Evidências Literais Associadas
### `EVID_009_01` — DEFINIÇÃO (Fonte: [[artigo_009]])
> [!quote] EVID_009_01
> **Localização:** Seção 3 (Attack Scenarios and Profiles), Páginas 5-8
> **Afirmação Sustentada:** Caracterização e taxonomia dos ataques de negação de serviço volumétricos (DDoS e DoS) em ambientes de rede.
>
> *"DDoS and DoS attacks represent volumetric disturbances characterized by massive rates of packets-per-second designed to exhaust network bandwidth or server socket pools through flooding protocols (SYN, UDP, ICMP, HTTP)."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 (Contextualização) ao caracterizar o comportamento dos ataques de DoS/DDoS volumétricos.

### `EVID_009_02` — EMPÍRICA (Fonte: [[artigo_009]])
> [!quote] EVID_009_02
> **Localização:** Seção 4 (CICIoT2023 Dataset Structure), Páginas 8-11
> **Afirmação Sustentada:** O dataset CICIoT2023 contém 33 tipos distintos de ataques executados em 105 dispositivos IoT de hardware real.
>
> *"The testbed incorporates 105 physical IoT devices across multiple vendors and architectures, capturing real-world interactions and executing 33 distinct attack types across 7 categories."*
>
> **Aplicação Tese ALF-MoE:** Serve como citação canônica para a descrição dos dados de benchmark IoT na seção de metodologia da tese.

### `EVID_009_03` — COMPARATIVA (Fonte: [[artigo_009]])
> [!quote] EVID_009_03
> **Localização:** Seção 5 (Benchmark Results), Páginas 13-16
> **Afirmação Sustentada:** Modelos supervisionados sofrem para distinguir subvariantes de ataques com dinâmicas similares sem extração multidomínio.
>
> *"While binary classification reaches near-perfect accuracy (99.5%), multi-class discrimination across fine-grained DoS variations shows notable confusion when relying solely on basic flow counters."*
>
> **Aplicação Tese ALF-MoE:** Corrobora a necessidade de especialistas dedicados no ALF-MoE (ex: estatístico global + temporal de IAT) para desempatar variantes de ataques volumétricos.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
