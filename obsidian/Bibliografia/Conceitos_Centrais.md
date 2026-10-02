---
title: Conceitos Centrais da Base Bibliográfica ALF-MoE
aliases:
- Conceitos Centrais
- Conceitos_Centrais
tags:
- conceitos
- bibliografia
- alf-moe
---

# 🧠 Conceitos Centrais da Base Bibliográfica ALF-MoE

> Este compêndio sintetiza os **14 conceitos teóricos e tecnológicos centrais** catalogados na base de 48 artigos científicos, com definições formais rigorosas, evidências literais citáveis e articulação direta com a arquitetura ALF-MoE.

---

## 📊 Matriz Geral dos 14 Conceitos
| # | Conceito / Termo | Nota Individual | Artigo Definidor | Evidência Canônica | Qtd. Artigos Rel. |
| :-: | :--- | :--- | :--- | :---: | :-: |
| 1 | **Network Intrusion Detection System (NIDS)** | [[Conceitos/NIDS]] | [[artigo_006]] | `EVID_006_01` | 14 |
| 2 | **Aprendizado Profundo em Detecção de Intrusão** | [[Conceitos/Deep Learning em Ciberseguranca]] | [[artigo_005]] | `EVID_005_01` | 10 |
| 3 | **Mixture of Experts (MoE)** | [[Conceitos/Mixture of Experts]] | [[artigo_004]] | `EVID_004_01` | 3 |
| 4 | **Calibração de Probabilidades e Confiabilidade** | [[Conceitos/Calibracao de Confianca]] | [[artigo_001]] | `EVID_001_01` | 2 |
| 5 | **Gated Recurrent Unit (GRU)** | [[Conceitos/Gated Recurrent Unit (GRU)]] | [[artigo_047]] | `EVID_047_01` | 3 |
| 6 | **Convolutional Autoencoder (CAE) e Detecção de Anomalias** | [[Conceitos/Convolutional Autoencoder (CAE)]] | [[artigo_048]] | `EVID_048_01` | 3 |
| 7 | **Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo** | [[Conceitos/Inter-Arrival Time (IAT) e Atributos Temporais]] | [[artigo_040]] | `EVID_040_01` | 3 |
| 8 | **Impacto da Criptografia Ponta a Ponta e TLS 1.3 em NIDS** | [[Conceitos/Criptografia Ponta a Ponta e TLS 1.3]] | [[artigo_043]] | `EVID_043_02` | 3 |
| 9 | **NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos** | [[Conceitos/NetFlow e Padronizacao de Atributos]] | [[artigo_027]] | `EVID_027_01` | 4 |
| 10 | **Data Leakage Temporal e Particionamento Estrito** | [[Conceitos/Data Leakage e Split Temporal]] | [[artigo_036]] | `EVID_036_01` | 2 |
| 11 | **Dataset Benchmark CIC-IDS-2017** | [[Conceitos/CIC-IDS-2017 Dataset]] | [[artigo_041]] | `EVID_041_02` | 3 |
| 12 | **Dataset Benchmark CICIoT2023** | [[Conceitos/CICIoT2023 Dataset]] | [[artigo_009]] | `EVID_009_02` | 4 |
| 13 | **Dataset UGR'16 e Ciclostacionariedade** | [[Conceitos/UGR_16 Dataset]] | [[artigo_045]] | `EVID_045_01` | 2 |
| 14 | **NFStream Framework de Analise de Fluxo** | [[Conceitos/NFStream Framework]] | [[artigo_026]] | `EVID_026_02` | 2 |

---

## Network Intrusion Detection System (NIDS) (`NIDS`)
> 📄 **Nota dedicada:** [[Conceitos/NIDS|Abrir nota completa]]
> **Sinônimos e Variantes:** NIDS, Network-based IDS, Sistema de Detecção de Intrusão em Redes, Intrusion Detection System, IDS de rede

**Definição Formal Canônica:**
Sistema de segurança que monitora e analisa o tráfego de rede para identificar atividades suspeitas, acessos não autorizados e violações de políticas de segurança.

- **Artigo Definidor:** [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
- **Evidência Textual (`EVID_006_01`):** *"Flow-based NIDS analyze statistical and temporal properties aggregated over network connections (flows) rather than inspecting raw payload, enabling scalability and compliance with pervasive end-to-end encryption."*
- **Aplicação na Tese:** Citação direta para embasar a definição e necessidade de NIDS baseados em fluxo no Capítulo 1 e Capítulo 2 da tese.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Arquitetura ALF-MoE para NIDS)
- [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* (Relevância: 5/5 | Papel: Definição formal de NIDS baseado em fluxos)
- [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas* (Relevância: 5/5 | Papel: NIDS distribuído em computação de nevoeiro)
- [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model* (Relevância: 5/5 | Papel: NIDS recorrente híbrido GRU-BiLSTM)
- [[artigo_026]] — *NFStream: A flexible network data analysis framework* (Relevância: 5/5 | Papel: Framework de análise de tráfego para NIDS)
- [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems* (Relevância: 5/5 | Papel: Datasets padronizados de NetFlow para NIDS)
- [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4* (Relevância: 5/5 | Papel: NIDS de alto desempenho em P4)
- [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso* (Relevância: 5/5 | Papel: NIDS híbrido em tempo real em SDN)
- [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* (Relevância: 5/5 | Papel: Análise temporal e avaliação de NIDS)
- [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* (Relevância: 5/5 | Papel: Engenharia de atributos temporais para NIDS)
- [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization* (Relevância: 5/5 | Papel: Dataset benchmark CIC-IDS-2017 para NIDS)
- [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets* (Relevância: 5/5 | Papel: Padronização de atributos para NIDS)
- [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU* (Relevância: 5/5 | Papel: Modelo CNN-GRU para NIDS)
- [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems* (Relevância: 5/5 | Papel: Autoencoder convolucional para NIDS embarcado)

---

## Aprendizado Profundo em Detecção de Intrusão (`Deep Learning em Ciberseguranca`)
> 📄 **Nota dedicada:** [[Conceitos/Deep Learning em Ciberseguranca|Abrir nota completa]]
> **Sinônimos e Variantes:** Deep Learning, Aprendizado Profundo, Redes Neurais Profundas, DNN, DL for NIDS

**Definição Formal Canônica:**
Paradigma de aprendizado de máquina fundamentado em redes neurais multicamadas capazes de extrair representações hierárquicas não-lineares automaticamente a partir de dados complexos de tráfego.

- **Artigo Definidor:** [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
- **Evidência Textual (`EVID_005_01`):** *"Deep learning architectures have revolutionized predictive modeling by autonomously extracting hierarchical features from complex, high-dimensional inputs, eliminating manual feature crafting."*
- **Aplicação na Tese:** Fundamenta a transição metodológica de NIDS baseados em regras ou ML clássico para representações baseadas em Aprendizado Profundo no Capítulo 1 e 2.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Fusão multimodal profunda ALF-MoE)
- [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges* (Relevância: 5/5 | Papel: Survey exaustivo de arquiteturas de deep learning)
- [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks* (Relevância: 5/5 | Papel: CNN-LSTM em tráfego IoT)
- [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic* (Relevância: 5/5 | Papel: 1D-CNN-LSTM com mecanismo de auto-atenção)
- [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset* (Relevância: 5/5 | Papel: Deep learning no CSE-CIC-IDS2018)
- [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model* (Relevância: 5/5 | Papel: Modelo profundo GRU-BiLSTM)
- [[artigo_028]] — *Network Anomaly Intrusion Detection Based on Deep Learning Approach* (Relevância: 5/5 | Papel: Detecção de anomalias com CNN e RNN)
- [[artigo_029]] — *Neural Networks and Cyber Resilience: Deep Insights into AI Architectures for Robust Security Framework* (Relevância: 5/5 | Papel: Resiliência cibernética via redes neurais)
- [[artigo_034]] — *Strengthening Network Security: Deep Learning Models for Intrusion Detection* (Relevância: 5/5 | Papel: Otimização de modelos profundos de NIDS)
- [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU* (Relevância: 5/5 | Papel: Modelo CNN-GRU profundo)

---

## Mixture of Experts (MoE) (`Mixture of Experts`)
> 📄 **Nota dedicada:** [[Conceitos/Mixture of Experts|Abrir nota completa]]
> **Sinônimos e Variantes:** Mistura de Especialistas, MoE, Specialized Expert Networks, Gating Network, Learnable Fusion

**Definição Formal Canônica:**
Arquitetura modular de aprendizado de máquina onde múltiplas sub-redes neurais especializadas (especialistas) aprendem subconjuntos ou modalidades do espaço de entrada, coordenadas dinamicamente por uma rede de roteamento (gating network).

- **Artigo Definidor:** [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Evidência Textual (`EVID_004_01`):** *"ALF-MoE allocates traffic representation across five dedicated neural experts: DNN for global tabular statistics x_g, CNN for spatial correlations x_s, GRU for sequential variations and IATs x_v, CAE with Hann window and RFFT for frequency-domain compression x_f, and LSTM for long-range temporal dependencies x_t."*
- **Aplicação na Tese:** Artigo primário que define e descreve a arquitetura avaliada na tese de graduação.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Arquitetura ALF-MoE com 5 especialistas e fusão atencional)
- [[artigo_025]] — *One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)* (Relevância: 5/5 | Papel: MoEVD demonstrando que 'One-for-All Does Not Work' em segurança)
- [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification* (Relevância: 5/5 | Papel: TrafficMoE com roteamento ciente de heterogeneidade)

---

## Calibração de Probabilidades e Confiabilidade (`Calibracao de Confianca`)
> 📄 **Nota dedicada:** [[Conceitos/Calibracao de Confianca|Abrir nota completa]]
> **Sinônimos e Variantes:** Confidence Calibration, Probability Calibration, Temperature Scaling, Vector Scaling, Expected Calibration Error, ECE

**Definição Formal Canônica:**
Propriedade de um classificador onde a probabilidade atribuída a uma classe predita corresponde exatamente à frequência empírica relativa de acerto (P(Y = y | P^ = p) = p).

- **Artigo Definidor:** [[artigo_001]] — *On Calibration of Modern Neural Networks*
- **Evidência Textual (`EVID_001_01`):** *"Perfect calibration is defined as P(Y = y | P^ = p) = p for all p in [0, 1]. In other words, the confidence score represents a true probability of correctness."*
- **Aplicação na Tese:** Fundamenta a definição matemática de calibração no módulo de gating calibrado do ALF-MoE (Capítulo 2 e 3).

**Artigos Relacionados:**
- [[artigo_001]] — *On Calibration of Modern Neural Networks* (Relevância: 5/5 | Papel: Fundamento seminal de calibração em redes neurais modernas)
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Calibração afim por Vector Scaling no módulo de gating do ALF-MoE)

---

## Gated Recurrent Unit (GRU) (`Gated Recurrent Unit (GRU)`)
> 📄 **Nota dedicada:** [[Conceitos/Gated Recurrent Unit (GRU)|Abrir nota completa]]
> **Sinônimos e Variantes:** GRU, Recurrent Neural Network, Gated Recurrence, Reset Gate, Update Gate

**Definição Formal Canônica:**
Variante de rede neural recorrente que utiliza portas de atualização (update) e reinicialização (reset) acopladas para controlar o fluxo de informação temporal sem estado de célula separado, oferecendo eficiência computacional superior a LSTMs.

- **Artigo Definidor:** [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*
- **Evidência Textual (`EVID_047_01`):** *"Compared with standard LSTM networks, GRUs utilize fewer tensor operations and lack a separate cell state, achieving comparable accuracy in sequential anomaly detection with roughly 30% lower parameter footprint and substantially reduced training and inference latency."*
- **Aplicação na Tese:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar por que o especialista GRU foi selecionado para modelar dinâmicas de curta cadência e IATs no ALF-MoE.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Especialista GRU no ALF-MoE para dinâmicas de curta cadência e IAT)
- [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model* (Relevância: 5/5 | Papel: Modelo híbrido GRU-BiLSTM para NIDS)
- [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU* (Relevância: 5/5 | Papel: Comparativo e eficiência do GRU em NIDS frente a LSTM)

---

## Convolutional Autoencoder (CAE) e Detecção de Anomalias (`Convolutional Autoencoder (CAE)`)
> 📄 **Nota dedicada:** [[Conceitos/Convolutional Autoencoder (CAE)|Abrir nota completa]]
> **Sinônimos e Variantes:** CAE, Autoencoder Convolucional, Unsupervised Anomaly Detection, Reconstruction Error, HSAE

**Definição Formal Canônica:**
Rede neural composta por um codificador convolucional que comprime os dados de entrada em uma representação de gargalo latente e um decodificador que reconstrói o sinal original; anomalias são detectadas por elevados erros quadráticos de reconstrução sob distribuição legítima.

- **Artigo Definidor:** [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Evidência Textual (`EVID_048_01`):** *"Convolutional autoencoders leverage localized spatial weight sharing to filter out ambient measurement noise while encoding essential traffic structure into a highly compressed bottleneck representation."*
- **Aplicação na Tese:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha do Convolutional Autoencoder (CAE) como o especialista dedicado a representações comprimidas e perdas de reconstrução no ALF-MoE.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Especialista CAE no ALF-MoE com janela de Hann e RFFT)
- [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble* (Relevância: 5/5 | Papel: HSAE e ensemble de autoencoders para ataques zero-day)
- [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems* (Relevância: 5/5 | Papel: CAE para NIDS robusto em hardware embarcado)

---

## Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo (`Inter-Arrival Time (IAT) e Atributos Temporais`)
> 📄 **Nota dedicada:** [[Conceitos/Inter-Arrival Time (IAT) e Atributos Temporais|Abrir nota completa]]
> **Sinônimos e Variantes:** IAT, Packet Inter-Arrival Time, Tempo Entre Chegadas, Temporal Features, Flow Cadence

**Definição Formal Canônica:**
Intervalo temporal decorrido entre a chegada de pacotes consecutivos em um fluxo bidirecional de rede, refletindo a cadência operacional de protocolos e estratégias de temporização de ataques.

- **Artigo Definidor:** [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Evidência Textual (`EVID_040_01`):** *"Packet Inter-Arrival Time (IAT) quantifies the elapsed duration between consecutive packet arrivals within a bidirectional flow, providing an essential mathematical descriptor of communication cadences and pacing strategies."*
- **Aplicação na Tese:** Citação direta no Capítulo 1 e Capítulo 3 para definir o subvetor temporal de IATs processado pelo especialista GRU no ALF-MoE.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Vetor de entrada temporal do especialista GRU no ALF-MoE)
- [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning* (Relevância: 5/5 | Papel: IAT como discriminador crítico em redes intraveiculares CAN)
- [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* (Relevância: 5/5 | Papel: Demonstração empírica de que 'Time Matters' em NetFlow)

---

## Impacto da Criptografia Ponta a Ponta e TLS 1.3 em NIDS (`Criptografia Ponta a Ponta e TLS 1.3`)
> 📄 **Nota dedicada:** [[Conceitos/Criptografia Ponta a Ponta e TLS 1.3|Abrir nota completa]]
> **Sinônimos e Variantes:** TLS 1.3, HTTPS, DoH, Encrypted Traffic, End-to-End Encryption, Payload Opacity

**Definição Formal Canônica:**
Protocolos de segurança da camada de transporte que encapsulam a totalidade da carga útil em cifras criptográficas autenticadas, tornando os métodos legados de inspeção profunda de pacotes (DPI) inteiramente ineficazes.

- **Artigo Definidor:** [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Evidência Textual (`EVID_043_02`):** *"With the widespread deployment of end-to-end encryption protocols such as TLS 1.3, deep packet inspection methods have become ineffective, necessitating robust flow-based feature sets that extract intelligence from flow headers and transmission dynamics rather than payload contents."*
- **Aplicação na Tese:** Citação de sustentação direta no Capítulo 1 (parágrafo 3) para fundamentar por que TLS 1.3 debilita a viabilidade prática da inspeção tradicional de pacotes.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Motivação primordial para classificação comportamental multidomínio)
- [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets* (Relevância: 5/5 | Papel: Fundamentação de TLS 1.3 e necessidade de atributos de fluxo)
- [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification* (Relevância: 5/5 | Papel: TrafficMoE especializado em tráfego cifrado TLS 1.3)

---

## NetFlow v9 / IPFIX e Conjunto Padronizado de 43 Atributos (`NetFlow e Padronizacao de Atributos`)
> 📄 **Nota dedicada:** [[Conceitos/NetFlow e Padronizacao de Atributos|Abrir nota completa]]
> **Sinônimos e Variantes:** NetFlow, NetFlow v9, IPFIX, Standard Feature Set, 43 Features, Flow Formats

**Definição Formal Canônica:**
Formato aberto e padronizado pela IETF para exportação e contabilização de metadados agregados de conexões IP em roteadores de rede, sem violação de privacidade de payload.

- **Artigo Definidor:** [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
- **Evidência Textual (`EVID_027_01`):** *"NetFlow is an industry-standard network protocol developed by Cisco for collecting IP operational traffic metadata, exporting structured records containing packet counts, byte volumes, interface identifiers, and temporal durations without exposing payload contents."*
- **Aplicação na Tese:** Fundamenta a definição e a relevância de NetFlow no Capítulo 1 e Capítulo 2 da tese.

**Artigos Relacionados:**
- [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems* (Relevância: 5/5 | Papel: Conversão de datasets para o padrão NetFlow v9)
- [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* (Relevância: 5/5 | Papel: Análise temporal de bases NetFlow)
- [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* (Relevância: 5/5 | Papel: Extensão temporal de NetFlow)
- [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets* (Relevância: 5/5 | Papel: Definição formal do NetFlow Standard Feature Set de 43 atributos)

---

## Data Leakage Temporal e Particionamento Estrito (`Data Leakage e Split Temporal`)
> 📄 **Nota dedicada:** [[Conceitos/Data Leakage e Split Temporal|Abrir nota completa]]
> **Sinônimos e Variantes:** Data Leakage, Vazamento de Dados, Temporal Split, Random Split, Cronological Partitioning

**Definição Formal Canônica:**
Erro metodológico severo em aprendizado de máquina onde dados de teste contaminam o conjunto de treinamento através de sobreposições de conexões contemporâneas em divisões randômicas.

- **Artigo Definidor:** [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
- **Evidência Textual (`EVID_036_01`):** *"Randomly splitting flow records into training and testing partitions inadvertently leaks temporal correlations, as packets belonging to the same underlying connection or attack burst appear in both sets, yielding artificially inflated accuracy scores that degrade in real-world deployments."*
- **Aplicação na Tese:** Citação direta indispensável no Capítulo 1 e Capítulo 3 para justificar o uso de particionamento estritamente temporal na avaliação experimental da tese.

**Artigos Relacionados:**
- [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* (Relevância: 5/5 | Papel: Análise crítica de métodos de particionamento)
- [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems* (Relevância: 5/5 | Papel: Estudo empírico definitivo de data leakage temporal em NIDS)

---

## Dataset Benchmark CIC-IDS-2017 (`CIC-IDS-2017 Dataset`)
> 📄 **Nota dedicada:** [[Conceitos/CIC-IDS-2017 Dataset|Abrir nota completa]]
> **Sinônimos e Variantes:** CIC-IDS-2017, CICIDS2017, PCAP 2017 Benchmark, UNB Dataset

**Definição Formal Canônica:**
Dataset de referência internacional desenvolvido pelo Canadian Institute for Cybersecurity contendo 5 dias de tráfego, 2.8 milhões de fluxos e 14 classes de ataque contemporâneas sob perfis B-Profile e M-Profile.

- **Artigo Definidor:** [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
- **Evidência Textual (`EVID_041_02`):** *"CIC-IDS-2017 covers modern attack profiles including Brute Force, Heartbleed, Botnet, DoS, DDoS, Web Attacks, and Infiltration, extracted across five continuous days of network interaction."*
- **Aplicação na Tese:** Artigo primário de citação obrigatória ao apresentar o benchmark CIC-IDS-2017 utilizado nos experimentos da tese.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Benchmark primário avaliado pelo ALF-MoE)
- [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems* (Relevância: 5/5 | Papel: Estudo comparativo e sanitização do CIC-IDS-2017)
- [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization* (Relevância: 5/5 | Papel: Trabalho seminal que criou o CIC-IDS-2017)

---

## Dataset Benchmark CICIoT2023 (`CICIoT2023 Dataset`)
> 📄 **Nota dedicada:** [[Conceitos/CICIoT2023 Dataset|Abrir nota completa]]
> **Sinônimos e Variantes:** CICIoT2023, CIC IoT 2023, IoT Benchmark 105 Devices

**Definição Formal Canônica:**
Conjunto de dados de larga escala para segurança em IoT capturado em bancada física com 105 dispositivos reais sob 33 classes de ataques em 7 perfis operacionais.

- **Artigo Definidor:** [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Evidência Textual (`EVID_009_02`):** *"The testbed incorporates 105 physical IoT devices across multiple vendors and architectures, capturing real-world interactions and executing 33 distinct attack types across 7 categories."*
- **Aplicação na Tese:** Serve como citação canônica para a descrição dos dados de benchmark IoT na seção de metodologia da tese.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Avaliação do ALF-MoE em ataques de IoT)
- [[artigo_007]] — *An Improved CNN-LSTM Based Intrusion Detection System for IoT Networks* (Relevância: 5/5 | Papel: Classificação CNN-LSTM no CICIoT2023)
- [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic* (Relevância: 5/5 | Papel: Mecanismo de atenção aplicado ao CICIoT2023)
- [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment* (Relevância: 5/5 | Papel: Trabalho seminal que concebeu o CICIoT2023)

---

## Dataset UGR'16 e Ciclostacionariedade (`UGR_16 Dataset`)
> 📄 **Nota dedicada:** [[Conceitos/UGR_16 Dataset|Abrir nota completa]]
> **Sinônimos e Variantes:** UGR'16, UGR16, ISP Capture Dataset, Cyclostationarity Benchmark

**Definição Formal Canônica:**
Dataset capturado durante 4 meses contínuos em um provedor de Internet (ISP) para avaliação de anomalias cíclicas e detecção no domínio da frequência.

- **Artigo Definidor:** [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*
- **Evidência Textual (`EVID_045_01`):** *"Network traffic exhibits cyclostationary properties where statistical moments vary periodically across daily, hourly, and weekly operational cycles, making frequency-domain representations optimal for capturing periodic baseline dynamics and harmonic disturbances."*
- **Aplicação na Tese:** Citação direta no Capítulo 1 (item 4) e Capítulo 3 para fundamentar teoricamente a inclusão do especialista no domínio da frequência (CAE com janela de Hann e RFFT) no ALF-MoE.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Fundamento para o especialista de frequência do ALF-MoE)
- [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs* (Relevância: 5/5 | Papel: Trabalho seminal que introduziu o UGR'16)

---

## NFStream Framework de Analise de Fluxo (`NFStream Framework`)
> 📄 **Nota dedicada:** [[Conceitos/NFStream Framework|Abrir nota completa]]
> **Sinônimos e Variantes:** NFStream, Flow Extraction Engine, Real-Time DPI Framework

**Definição Formal Canônica:**
Framework open-source em Python e C de alto desempenho para extração, agregação e rotulagem de fluxos de rede bidirecionais em tempo real.

- **Artigo Definidor:** [[artigo_026]] — *NFStream: A flexible network data analysis framework*
- **Evidência Textual (`EVID_026_02`):** *"NFStream provides a flexible network data analysis framework designed to eliminate unreliability in legacy measurement tools, delivering high-speed bidirectional feature extraction directly compatible with modern machine learning libraries."*
- **Aplicação na Tese:** Fundamenta a escolha do pipeline de ingestão e extração de atributos no Capítulo 3 e Capítulo 4 (Pipeline de Inferência) da tese.

**Artigos Relacionados:**
- [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* (Relevância: 5/5 | Papel: Ingestão e preparação de dados do pipeline)
- [[artigo_026]] — *NFStream: A flexible network data analysis framework* (Relevância: 5/5 | Papel: Trabalho seminal que desenvolveu o NFStream)

---

## 🧭 Navegação
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
