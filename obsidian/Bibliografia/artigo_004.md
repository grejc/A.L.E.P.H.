---
id: artigo_004
title: 'ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks
  for Accurate Traffic Classification'
authors:
- Jisi Chandroth
- Gabriel Stoian
- Daniela Danciulescu
year: 2026
bibtex_key: alfmoe2026
doi: 10.3390/math14030525
venue: Mathematics 2026, 14(3), 525
keywords:
- Traffic Classification
- Mixture of Experts
- Deep Learning
- Attention Mechanism
- Learnable Fusion
- Network Security
- Multimodal Traffic Analysis
area: Network Traffic Classification / Intrusion Detection / Mixture of Experts
datasets:
- CIC-IDS-2017
- CSE-CIC-IDS2018
- CICIoT2023
- ISCX-VPN-NonVPN
models:
- ALF-MoE
- Dense Neural Network (DNN)
- Convolutional Neural Network (CNN)
- Gated Recurrent Unit (GRU)
- Convolutional Autoencoder (CAE)
- Long Short-Term Memory (LSTM)
- Attention-based Gating Network
- Vector Scaling Calibration
aliases:
- 'ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for
  Accurate Traffic Classification'
- alfmoe2026
- artigo_004
tags:
- bibliografia
- alf-moe
- artigo
---

# ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification

> **Citação ABNT Sugerida:** CHANDROTH, J.; STOIAN, G.; DANCIULESCU, D.. ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification. In: **Mathematics 2026, 14(3), 525**, 2026.
> **Chave BibTeX:** `alfmoe2026` | **Arquivo TXT:** `ALF-MoE__An_Attention-Based_Learnable_Fusion_of_Specialized_Expert_Networks_for_Accurate_Traffic_Classification.txt` | **DOI:** `10.3390/math14030525`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_004` |
| **Ano** | 2026 |
| **Área de Pesquisa** | Network Traffic Classification / Intrusion Detection / Mixture of Experts |
| **Veículo de Publicação** | Mathematics 2026, 14(3), 525 |
| **Datasets Utilizados** | CIC-IDS-2017, CSE-CIC-IDS2018, CICIoT2023, ISCX-VPN-NonVPN |
| **Modelos / Algoritmos** | ALF-MoE, Dense Neural Network (DNN), Convolutional Neural Network (CNN), Gated Recurrent Unit (GRU), Convolutional Autoencoder (CAE), Long Short-Term Memory (LSTM), Attention-based Gating Network, Vector Scaling Calibration |
| **Palavras-Chave** | Traffic Classification, Mixture of Experts, Deep Learning, Attention Mechanism, Learnable Fusion, Network Security, Multimodal Traffic Analysis |

## 🎯 Problema Abordado
O tráfego de rede contemporâneo cifrado exibe padrões heterogêneos distribuídos em múltiplas dimensões (estatística tabular, correlação espacial de pacotes, dinâmica temporal de IAT e densidade espectral no domínio da frequência). Modelos monolíticos e técnicas clássicas de fusão tardia estática (média simples, votação majoritária) não conseguem capturar as dependências entre domínios nem modular a contribuição de cada rede com base no perfil específico do fluxo.

## 🔬 Metodologia
Arquitetura ALF-MoE baseada no paradigma Mixture of Experts (MoE) composta por 5 redes especialistas profundas dedicadas (DNN para estatísticas globais, CNN para correlações espaciais, GRU para variações sequenciais de curto prazo, CAE com janela de Hann e RFFT para representação no domínio da frequência, e LSTM para dependências de longo alcance); módulo de roteamento dinâmico (Gating Network) acoplado a uma projeção atencional logarítmica aprendível (ALF) com calibração probabilística por Vector Scaling.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O ALF-MoE supera todos os especialistas individuais e métodos clássicos de ensemble (média ponderada, stacking e votação majoritária), atingindo acurácia superior a 98.7% e ganhos de até 8.4% em F1-macro em classes difíceis e minoritárias; a fusão aprendível reduz falsos positivos e calibra a certeza de classificação.

**Contribuições Centrais:**
- Proposição da arquitetura ALF-MoE com 5 especialistas neurais complementares para classificação de tráfego de rede.
- Formulação matemática do mecanismo de fusão aprendível baseada em atenção logarítmica com calibração afim por Vector Scaling.
- Análise empírica exaustiva demonstrando a superioridade da fusão dinâmica sobre fusão tardia estática em múltiplos datasets de tráfego e intrusão.

## ⚠️ Limitações Identificadas
Custo computacional de treinamento conjunto das cinco redes neurais e necessidade de particionamento e pré-processamento de vetores de entrada multidomínio (janelamento FFT e extração IAT).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `ALF-MoE`, `Mixture of Experts`, `Attention-Based Fusion`, `Multi-domain Representation`, `Calibrated Gating`
- **Problemas Focais:** `Limitação de modelos monolíticos`, `Inadequação da fusão tardia estática`, `Opacidade e heterogeneidade do tráfego cifrado`
- **Métodos Empregados:** `Redes especialistas dedicadas`, `Roteamento dinâmico softmax`, `Projeção afim atencional`, `Calibração via Vector Scaling`, `Transformada de Fourier (RFFT)`
- **Modelos e Arquiteturas:** `DNN`, `CNN`, `GRU`, `CAE`, `LSTM`, `Gating Network`
- **Bases de Dados:** `CIC-IDS-2017`, `CSE-CIC-IDS2018`, `CICIoT2023`
- **Resultados Chave:** `Acurácia > 98.7%`, `Superação de ensemble tradicional e especialistas isolados`, `Superioridade em F1-macro`
- **Limitações Reconhecidas:** `Complexidade de treinamento conjunto`, `Overhead computacional em inferência de alta taxa`
- **Evidências Citáveis:** `EVID_004_01`, `EVID_004_02`, `EVID_004_03`, `EVID_004_04`, `EVID_004_05`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Utiliza:**
  - [[artigo_001]] — *On Calibration of Modern Neural Networks*
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
- **Compara:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
  - [[artigo_006]] — *Advanced IDS: a comparative study of datasets and machine learning algorithms for network flow-based intrusion detection systems*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*
- **Avalia Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*
  - [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*

### Citações e Relações Recebidas na Base (Incoming)
- **Fundamenta:**
  - [[artigo_001]] — *On Calibration of Modern Neural Networks*
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
- **Relacionado:**
  - [[artigo_002]] — *Meta-UAD: A Meta-Learning Scheme for User-level Network Traffic Anomaly Detection*
  - [[artigo_008]] — *An efficient self attention-based 1D-CNN-LSTM network for IoT attack detection and identification using network traffic*
  - [[artigo_028]] — *Network Anomaly Intrusion Detection Based on Deep Learning Approach*
- **Fundamenta Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
- **Utiliza Dataset:**
  - [[artigo_011]] — *Deep Learning-Based Anomaly and Intrusion Detection Using the CSE-CIC-IDS2018 Dataset*
- **Fundamenta Metodologia:**
  - [[artigo_015]] — *A Deep Learning Algorithm to Cybersecurity: Enhancing Intrusion Detection with a Hybrid GRU and BiLSTM Model*
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_027]] — *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
  - [[artigo_036]] — *Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
  - [[artigo_043]] — *Towards a Standard Feature Set for Network Intrusion Detection System Datasets*
  - [[artigo_045]] — *UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*
  - [[artigo_047]] — *Network Intrusion Detection Model Based on CNN and GRU*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Fundamenta Contexto:**
  - [[artigo_018]] — *Estimating the Global Cost of Cyber Risk: Methodology and Examples*
  - [[artigo_029]] — *Neural Networks and Cyber Resilience: Deep Insights into AI Architectures for Robust Security Framework*
  - [[artigo_037]] — *The impact of artificial intelligence on organisational cyber security: An outcome of a systematic literature review*
- **Fundamenta Conceito:**
  - [[artigo_025]] — *One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*
  - [[artigo_044]] — *TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_001]]` (*On Calibration of Modern Neural Networks*): ALF-MoE utiliza Vector Scaling e teoria de calibração afim de probabilidades de Guo et al. no módulo de gating.
- `[[artigo_004]]` $\xrightarrow{\text{fundamenta_teoria}}$ `[[artigo_025]]` (*One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*): ALF-MoE baseia-se na comprovação de que modelos 'one-for-all' falham em segurança dada por Yang et al.
- `[[artigo_004]]` $\xrightarrow{\text{compara_arquitetura}}$ `[[artigo_044]]` (*TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification*): Ambos propõem Mixture-of-Experts para tráfego heterogêneo cifrado com roteamento dinâmico.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_040]]` (*Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*): ALF-MoE extrai atributos temporais e IATs para alimentar o especialista GRU baseado nas descobertas de Luay et al.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_047]]` (*Network Intrusion Detection Model Based on CNN and GRU*): Justifica o uso de GRU para modelar transições rápidas e cadência temporal com menor custo de treino.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_048]]` (*A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*): Adota Convolutional Autoencoder (CAE) para representação comprimida robusta a ruídos e erro de reconstrução.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_045]]` (*UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs*): Aplica decomposição no domínio da frequência (RFFT) inspirada na ciclostacionariedade comprovada no UGR'16.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_036]]` (*Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems*): Adota protocolo rigoroso de particionamento estritamente temporal para evitar data leakage.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_043]]` (*Towards a Standard Feature Set for Network Intrusion Detection System Datasets*): Emprega representação padronizada de atributos inspirada no NetFlow Standard Feature Set de 43 atributos.
- `[[artigo_004]]` $\xrightarrow{\text{utiliza_ferramenta}}$ `[[artigo_026]]` (*NFStream: A flexible network data analysis framework*): Utiliza o NFStream como base da extração em tempo real de fluxos bidirecionais.
- `[[artigo_004]]` $\xrightarrow{\text{avalia_dataset}}$ `[[artigo_041]]` (*Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*): Avalia o ALF-MoE no dataset canônico CIC-IDS-2017.
- `[[artigo_004]]` $\xrightarrow{\text{avalia_dataset}}$ `[[artigo_009]]` (*CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*): Avalia o ALF-MoE no benchmark de ataques de IoT em larga escala CICIoT2023.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Arquitetura ALF-MoE para NIDS
- [[Conceitos/Deep Learning em Ciberseguranca|Aprendizado Profundo em Detecção de Intrusão]] — Papel: Fusão multimodal profunda ALF-MoE
- [[Conceitos/Mixture of Experts|Mixture of Experts (MoE)]] — 🌟 **Definição Canônica**
- [[Conceitos/Calibracao de Confianca|Calibração de Probabilidades e Confiabilidade]] — Papel: Calibração afim por Vector Scaling no módulo de gating do ALF-MoE
- [[Conceitos/Gated Recurrent Unit (GRU)|Gated Recurrent Unit (GRU)]] — Papel: Especialista GRU no ALF-MoE para dinâmicas de curta cadência e IAT
- [[Conceitos/Convolutional Autoencoder (CAE)|Convolutional Autoencoder (CAE) e Detecção de Anomalias]] — Papel: Especialista CAE no ALF-MoE com janela de Hann e RFFT
- [[Conceitos/Inter-Arrival Time (IAT) e Atributos Temporais|Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo]] — Papel: Vetor de entrada temporal do especialista GRU no ALF-MoE
- [[Conceitos/Criptografia Ponta a Ponta e TLS 1.3|Impacto da Criptografia Ponta a Ponta e TLS 1.3 em NIDS]] — Papel: Motivação primordial para classificação comportamental multidomínio
- [[Conceitos/CIC-IDS-2017 Dataset|Dataset Benchmark CIC-IDS-2017]] — Papel: Benchmark primário avaliado pelo ALF-MoE
- [[Conceitos/CICIoT2023 Dataset|Dataset Benchmark CICIoT2023]] — Papel: Avaliação do ALF-MoE em ataques de IoT
- [[Conceitos/UGR_16 Dataset|Dataset UGR'16 e Ciclostacionariedade]] — Papel: Fundamento para o especialista de frequência do ALF-MoE
- [[Conceitos/NFStream Framework|NFStream Framework de Analise de Fluxo]] — Papel: Ingestão e preparação de dados do pipeline

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_002 — Categoria: Teoria|CLAIM_002 (Teoria)]] — *"Modelos monolíticos concebidos sob uma perspectiva homogênea ou restrita de atributos (single-view) tendem a apresentar desempenho subótimo na detecção de ataques contemporâneos cujas assinaturas residem em múltiplos domínios informacionais distintos."*
  - *Aplicação na Tese:* Fundamenta a motivação do Capítulo 1 da tese para propor arquitetura multimodal.
- [[Afirmacoes_e_Claims#CLAIM_003 — Categoria: Metodologia|CLAIM_003 (Metodologia)]] — *"Abordagens convencionais de Ensemble Learning baseadas em fusão tardia estática (late fusion), tais como média aritmética simples, votação majoritária ou concatenação linear de escores, desconsideram a interdependência dos domínios durante o aprendizado e não modulam a relevância dos modelos com base no perfil particular do fluxo."*
  - *Aplicação na Tese:* Justifica a necessidade de um módulo de fusão aprendível baseada em atenção (ALF) em vez de ensembles estáticos.
- [[Afirmacoes_e_Claims#CLAIM_004 — Categoria: Metodologia|CLAIM_004 (Metodologia)]] — *"Redes neurais profundas modernas com alta profundidade, largura e batch normalization tendem a ser superconfiantes e descalibradas, produzindo probabilidades que não refletem a verdadeira confiança preditiva e necessitando de técnicas de calibração pós-hoc afins como Temperature Scaling e Vector Scaling."*
  - *Aplicação na Tese:* Conexão direta entre a teoria de Guo et al. e o pipeline do ALF-MoE.
- [[Afirmacoes_e_Claims#CLAIM_009 — Categoria: Teoria / Metodologia|CLAIM_009 (Teoria / Metodologia)]] — *"O tráfego de rede exibe propriedades de ciclostacionariedade e densidade espectral no domínio da frequência que permitem discriminar anomalias periódicas e ataques volumétricos."*
  - *Aplicação na Tese:* Sustenta o cálculo matemático da entrada frequencial x_f.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_003 — Arquitetura Neural de NIDS: Modelos Monolíticos ('One-for-All') vs. Mixture-of-Experts (MoE)|CONTROV_003 — Arquitetura Neural de NIDS: Modelos Monolíticos ('One-for-All') vs. Mixture-of-Experts (MoE)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"Modelos monolíticos 'one-for-all' sofrem interferência negativa de gradientes quando confrontados com distribuições heterogêneas de ataques multimodais; a decomposição modular especializada (MoE) com fusão atencional calibrada supera expressivamente modelos monolíticos."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo|Cadeia 1: Criptografia Ponta a Ponta e Metadados de Fluxo]] — **Etapa RESULTADO:** Classificadores operam com alta acurácia sem acesso a texto claro de payload
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa CONCEITO:** Heterogeneidade intrínseca do tráfego malicioso em múltiplos domínios
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa MÉTODO:** Arquitetura ALF-MoE com 5 especialistas (DNN, CNN, GRU, CAE, LSTM) e fusão aprendível calibrada
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa EXPERIMENTO:** Avaliação comparativa contra votação majoritária, média ponderada e modelos isolados
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa RESULTADO:** Ganhos de até 8.4% em macro F1-score e acurácia superior a 98.7%
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa LIMITAÇÃO:** Custo computacional de treinamento simultâneo das 5 redes profundas

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: CSE-CIC-IDS2018|CSE-CIC-IDS2018]], [[Rede_Intelectual#Benchmark: CICIoT2023|CICIoT2023]], [[Rede_Intelectual#Benchmark: UGR'16|UGR'16]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Mixture of Experts|Mixture of Experts]], [[Rede_Intelectual#Arquitetura: Recorrentes GRU LSTM|Recorrentes GRU LSTM]], [[Rede_Intelectual#Arquitetura: Autoencoders|Autoencoders]], [[Rede_Intelectual#Arquitetura: Calibracao Probabilistica|Calibracao Probabilistica]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_004_01` — DEFINIÇÃO
> [!quote] EVID_004_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição formal da arquitetura ALF-MoE e divisão das modalidades de entrada dos cinco especialistas.
> **Localização:** Seção 2 (Proposed Architecture), Páginas 3-5
>
> *"ALF-MoE allocates traffic representation across five dedicated neural experts: DNN for global tabular statistics x_g, CNN for spatial correlations x_s, GRU for sequential variations and IATs x_v, CAE with Hann window and RFFT for frequency-domain compression x_f, and LSTM for long-range temporal dependencies x_t."*
>
> **Aplicabilidade na Tese ALF-MoE:** Artigo primário que define e descreve a arquitetura avaliada na tese de graduação.

### `EVID_004_02` — METODOLÓGICA
> [!quote] EVID_004_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Formulação matemática da fusão aprendível baseada em atenção logarítmica e calibração por Vector Scaling.
> **Localização:** Seção 2.3 (Attention-Based Learnable Fusion and Gating), Páginas 6-7
>
> *"The attention weights are computed as a = softmax(W_g log(alpha + epsilon) + b_g), allowing the network to dynamically learn cross-expert dependencies, followed by affine probability calibration."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta diretamente as Equações do Capítulo 1 e Capítulo 3 sobre o mecanismo de roteamento e fusão do ALF-MoE.

### `EVID_004_03` — EMPÍRICA
> [!quote] EVID_004_03 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** A fusão aprendível baseada em atenção supera significativamente a fusão estática por votação majoritária e média simples.
> **Localização:** Seção 4 (Experimental Results and Discussion), Páginas 9-12
>
> *"ALF-MoE outperforms static late fusion techniques, demonstrating an improvement of up to 4.2% in overall accuracy and 8.4% in macro F1-score over simple averaging and majority voting."*
>
> **Aplicabilidade na Tese ALF-MoE:** Evidência experimental direta para justificar a escolha do ALF-MoE frente a ensembles convencionais no Capítulo de Metodologia e Resultados.

### `EVID_004_04` — LIMITAÇÃO
> [!quote] EVID_004_04 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Modelos monolíticos que operam sob uma única perspectiva sofrem degradação de desempenho frente a ataques multifacetados.
> **Localização:** Seção 1 (Introduction), Página 2
>
> *"Single-view monolithic models fail to capture multi-faceted attack signatures whose discriminative patterns reside across distinct domains such as frequency or sequential dynamics."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a motivação do Capítulo 1 sobre as deficiências de modelos monolíticos na literatura.

### `EVID_004_05` — LIMITAÇÃO
> [!quote] EVID_004_05 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Limitações de métodos tradicionais de classificação de tráfego e detecção de intrusão baseados em portas ou inspeção de pacotes frente a tráfego cifrado e dinâmico.
> **Localização:** Seção 1 (Introduction), Páginas 1-2
>
> *"Traditional traffic classification methods, such as port-based identification and payload inspection, are largely static and struggle to remain effective in modern IoT networks. With the rapid emergence of new applications and evolving protocols, and the increasing use of encryption, port-based and payload-based analysis become ineffective."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a motivação no Capítulo 1 e Seção 2 sobre as limitações de IDSs tradicionais e necessidade de representações profundas baseadas em fluxo.

## 📦 Entrada BibTeX
```bibtex
@article{alfmoe2026,
  title = {{ALF-MoE}: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification},
  author = {Chandroth, Jisi and Stoian, Gabriel and Danciulescu, Daniela},
  journal = {Mathematics},
  year = {2026},
  doi = {10.3390/math14030525},
  volume = {14},
  number = {3},
  pages = {525},
  publisher = {MDPI AG}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
