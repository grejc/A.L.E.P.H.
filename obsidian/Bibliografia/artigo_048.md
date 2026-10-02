---
id: artigo_048
title: A convolutional autoencoder architecture for robust network intrusion detection
  in embedded systems
authors:
- Niccolò Borgioli
- Federico Aromolo
- Linh Thi Xuan Phan
- Giorgio Buttazzo
year: 2024
bibtex_key: borgioli2024cae
doi: 10.1016/j.sysarc.2024.103283
venue: Journal of Systems Architecture, Volume 156, November 2024, 103283
keywords:
- Convolutional Autoencoder (CAE)
- Embedded Systems
- Network Intrusion Detection
- Robustness
- Unsupervised Anomaly Detection
- Reconstruction Error
area: Embedded NIDS / Convolutional Autoencoders / Robust Deep Learning / Resource-Constrained
  Security
datasets:
- CIC-IDS-2017
- Kitsune Network Attack Dataset
models:
- Convolutional Autoencoder (CAE)
- Dense Autoencoder (DAE)
- Isolation Forest (comparativo)
- Quantização INT8
aliases:
- A convolutional autoencoder architecture for robust network intrusion detection
  in embedded systems
- borgioli2024cae
- artigo_048
tags:
- bibliografia
- alf-moe
- artigo
---

# A convolutional autoencoder architecture for robust network intrusion detection in embedded systems

> **Citação ABNT Sugerida:** BORGIOLI, N.; AROMOLO, F.; PHAN, L. T. X.; BUTTAZZO, G.. A convolutional autoencoder architecture for robust network intrusion detection in embedded systems. In: **Journal of Systems Architecture, Volume 156, November 2024, 103283**, 2024.
> **Chave BibTeX:** `borgioli2024cae` | **Arquivo TXT:** `borgioli-jsa24.txt` | **DOI:** `10.1016/j.sysarc.2024.103283`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_048` |
| **Ano** | 2024 |
| **Área de Pesquisa** | Embedded NIDS / Convolutional Autoencoders / Robust Deep Learning / Resource-Constrained Security |
| **Veículo de Publicação** | Journal of Systems Architecture, Volume 156, November 2024, 103283 |
| **Datasets Utilizados** | CIC-IDS-2017, Kitsune Network Attack Dataset |
| **Modelos / Algoritmos** | Convolutional Autoencoder (CAE), Dense Autoencoder (DAE), Isolation Forest (comparativo), Quantização INT8 |
| **Palavras-Chave** | Convolutional Autoencoder (CAE), Embedded Systems, Network Intrusion Detection, Robustness, Unsupervised Anomaly Detection, Reconstruction Error |

## 🎯 Problema Abordado
Dispositivos embarcados de rede (gateways de IoT, switches locais e roteadores automotivos) possuem limitações severas de memória RAM e capacidade energética, tornando inviável a execução de grandes redes neurais; além disso, a presença de ruído nos dados brutos degrada facilmente detectores supervisionados superficiais.

## 🔬 Metodologia
Arquitetura Convolutional Autoencoder (CAE) compacta e robusta projetada para compressão e reconstrução de tráfego de rede; utilização de convoluções 1D com quantização pós-treinamento (INT8) para execução acelerada em núcleos ARM embarcados; detecção baseada no Mean Squared Error (MSE) de reconstrução sob tráfego legítimo.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O CAE proposto alcançou AUC-ROC de 0.984 no CIC-IDS-2017 consumindo menos de 45 KB de memória RAM, exibindo estabilidade contra ruídos de medição e superando autoencoders densos clássicos em até 8.2% na identificação de ataques anômalos.

**Contribuições Centrais:**
- Design otimizado de Convolutional Autoencoder com pegada de memória inferior a 50 KB.
- Demonstração da robustez de kernels convolucionais contra ruídos de medição em rede.
- Validação experimental rigorosa em plataformas reais de hardware embarcado (ARM Cortex).

## ⚠️ Limitações Identificadas
Sensibilidade a ataques lentos que injetam anomalias infinitesimais abaixo do limiar estático de erro quadrático de reconstrução.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Convolutional Autoencoder`, `NIDS Embarcado`, `Erro de Reconstrução MSE`, `Robustez contra Ruído`
- **Problemas Focais:** `Restrições extremas de memória em hardware embarcado`, `Sensibilidade de autoencoders simples a ruído`
- **Métodos Empregados:** `Convolução 1D comprimida`, `Treinamento não supervisionado em tráfego legítimo`, `Quantização INT8`
- **Modelos e Arquiteturas:** `CAE Embarcado`, `Dense Autoencoder`
- **Bases de Dados:** `CIC-IDS-2017`, `Kitsune`
- **Resultados Chave:** `AUC-ROC de 0.984 consumindo menos de 45 KB de RAM`, `Alta imunidade a ruídos operacionais`
- **Limitações Reconhecidas:** `Limiar fixo vulnerável a microperturbações sutis`
- **Evidências Citáveis:** `EVID_048_01`, `EVID_048_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_010]] — *DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles*
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Fundamenta:**
  - [[artigo_005]] — *A survey on state-of-the-art deep learning applications and challenges*
- **Relacionado:**
  - [[artigo_010]] — *DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles*
  - [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning*
  - [[artigo_021]] — *HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_048]]`: Adota Convolutional Autoencoder (CAE) para representação comprimida robusta a ruídos e erro de reconstrução.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: Autoencoder convolucional para NIDS embarcado
- [[Conceitos/Convolutional Autoencoder (CAE)|Convolutional Autoencoder (CAE) e Detecção de Anomalias]] — 🌟 **Definição Canônica**

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_007 — Categoria: Metodologia / Empírico|CLAIM_007 (Metodologia / Empírico)]] — *"Autoencoders convolucionais (CAE) treinados exclusivamente sobre tráfego legítimo são capazes de identificar anomalias desconhecidas e ataques zero-day através do aumento do erro de reconstrução, fornecendo imunidade a ruídos locais."*
  - *Aplicação na Tese:* Justifica a inclusão do especialista CAE no ALF-MoE (Capítulo 1 e 3).

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_004 — Detecção de Ataques Zero-Day: Classificadores Supervisionados vs. Modelagem Não-Supervisionada de Normalidade (Autoencoders / CAE)|CONTROV_004 — Detecção de Ataques Zero-Day: Classificadores Supervisionados vs. Modelagem Não-Supervisionada de Normalidade (Autoencoders / CAE)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"Modelos puramente supervisionados falham catastroficamente ao encontrar ataques zero-day ou mutações inéditas não presentes no treinamento; métodos não supervisionados baseados em modelagem de normalidade (como autoencoders convolucionais CAE/HSAE) são essenciais para isolar desvios de normalidade sem rótulos prévios."*

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa LACUNA:** Otimização de inferência de MoE via quantização INT8 e aceleração em hardware P4

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Autoencoders|Autoencoders]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_048_01` — METODOLÓGICA
> [!quote] EVID_048_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Convolutional Autoencoders (CAE) oferecem representações comprimidas robustas a ruídos e perturbações morfológicas locais em dados de fluxo de rede.
> **Localização:** Seção 3 (Convolutional Autoencoder Architecture), Páginas 3-5
>
> *"Convolutional autoencoders leverage localized spatial weight sharing to filter out ambient measurement noise while encoding essential traffic structure into a highly compressed bottleneck representation."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para justificar a escolha do Convolutional Autoencoder (CAE) como o especialista dedicado a representações comprimidas e perdas de reconstrução no ALF-MoE.

### `EVID_048_02` — EMPÍRICA
> [!quote] EVID_048_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O erro de reconstrução de autoencoders convolucionais proporciona excelente separabilidade de anomalias com pegada de memória mínima compatível com dispositivos de borda.
> **Localização:** Seção 5 (Experimental Performance and Benchmarking), Páginas 7-10
>
> *"The proposed 1D-CAE achieves an AUC-ROC of 0.984 on the CIC-IDS-2017 dataset requiring less than 45 KB of memory, substantially outperforming dense autoencoders and classical tree models in constrained embedded deployments."*
>
> **Aplicabilidade na Tese ALF-MoE:** Evidência experimental para sustentar a viabilidade e eficácia do especialista CAE na tese.

## 📦 Entrada BibTeX
```bibtex
@article{borgioli2024cae,
  title = {A convolutional autoencoder architecture for robust network intrusion detection in embedded systems},
  author = {Borgioli, Niccol{\`o} and Aromolo, Federico and Phan, Linh Thi Xuan and Buttazzo, Giorgio},
  journal = {Journal of Systems Architecture},
  year = {2024},
  volume = {156},
  pages = {103283},
  doi = {10.1016/j.sysarc.2024.103283},
  publisher = {Elsevier BV}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
