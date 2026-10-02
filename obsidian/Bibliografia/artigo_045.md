---
id: artigo_045
title: 'UGR‘16: A new dataset for the evaluation of cyclostationarity-based network
  IDSs'
authors:
- Gabriel Maciá-Fernández
- José Camacho
- Roberto Magán-Carrión
- Pedro García-Teodoro
- Roberto Therón
year: 2018
bibtex_key: ugr162021
doi: 10.1016/j.cose.2017.11.004
venue: Computers & Security, Volume 73, pp. 411-424
keywords:
- UGR'16
- Network Anomaly Detection
- Cyclostationarity
- ISP Dataset
- Long-term Traffic Capture
- Periodic Traffic Patterns
area: Network Intrusion Detection / ISP Datasets / Cyclostationary Analysis / Anomaly
  Detection
datasets:
- UGR'16 (proposto)
- KDD Cup 99 (comparativo)
models:
- Cyclostationary Spectral Analysis
- PCA Anomaly Detection
- Fourier Decomposition
- Flow Clustering
aliases:
- 'UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs'
- ugr162021
- artigo_045
tags:
- bibliografia
- alf-moe
- artigo
---

# UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs

> **Citação ABNT Sugerida:** MACIÁ-FERNÁNDEZ, G.; CAMACHO, J.; MAGÁN-CARRIÓN, R.; GARCÍA-TEODORO, P.; THERÓN, R.. UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs. In: **Computers & Security, Volume 73, pp. 411-424**, 2018.
> **Chave BibTeX:** `ugr162021` | **Arquivo TXT:** `UGR_16__A_New_Dataset_for_the_Evaluation_of_Cyclostationarity-Based_Network_IDSs.txt` | **DOI:** `10.1016/j.cose.2017.11.004`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_045` |
| **Ano** | 2018 |
| **Área de Pesquisa** | Network Intrusion Detection / ISP Datasets / Cyclostationary Analysis / Anomaly Detection |
| **Veículo de Publicação** | Computers & Security, Volume 73, pp. 411-424 |
| **Datasets Utilizados** | UGR'16 (proposto), KDD Cup 99 (comparativo) |
| **Modelos / Algoritmos** | Cyclostationary Spectral Analysis, PCA Anomaly Detection, Fourier Decomposition, Flow Clustering |
| **Palavras-Chave** | UGR'16, Network Anomaly Detection, Cyclostationarity, ISP Dataset, Long-term Traffic Capture, Periodic Traffic Patterns |

## 🎯 Problema Abordado
A esmagadora maioria dos datasets de NIDS é capturada em janelas curtas de poucas horas ou dias em ambientes de laboratório fechados, ignorando a ciclostacionariedade (periodicidade diária, semanal e sazonal) do tráfego real de provedores de Internet (ISPs) e a coexistência de ruído natural de longa duração.

## 🔬 Metodologia
Captura e publicação do dataset UGR'16 ao longo de 4 meses contínuos em um provedor de Internet (ISP) com conexões reais; injeção controlada de ataques reais e sintéticos (DoS, varreduras de porta, botnets, spam); caracterização do tráfego através de modelos de ciclostacionariedade e densidade espectral no domínio da frequência.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O dataset UGR'16 fornece mais de 16.9 bilhões de fluxos NetFlow reais; demonstração empírica de que ataques como DoS, abusos de rede e varreduras causam perturbações nítidas nas frequências harmônicas cíclicas do tráfego que são invisíveis em análises estatísticas atemporais.

**Contribuições Centrais:**
- Disponibilização do primeiro dataset de NIDS em nível de ISP capturado ao longo de múltiplos meses.
- Fundamentação da teoria de ciclostacionariedade aplicada à detecção de intrusão.
- Demonstração do valor do domínio da frequência para identificação de perturbações volumétricas e ataques cíclicos.

## ⚠️ Limitações Identificadas
O volume de dados de vários terabytes exige infraestruturas de big data (como Spark ou clusters dedicados) para treinamento direto de modelos profundos.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Dataset UGR'16`, `Ciclostacionariedade do Tráfego`, `Domínio da Frequência`, `Padrões Periódicos em ISP`
- **Problemas Focais:** `Datasets curtos ignoram sazonalidade e ciclicidade real`, `Ruído natural de longa duração confunde NIDS`
- **Métodos Empregados:** `Captura de 4 meses em ISP`, `Decomposição espectral de Fourier`, `Análise de ciclostacionariedade`
- **Modelos e Arquiteturas:** `Modelos espectrais`, `PCA`, `Detecção cíclica`
- **Bases de Dados:** `UGR'16 (16.9B fluxos)`
- **Resultados Chave:** `Identificação de assinaturas espectrais nítidas para DoS e varreduras periódicas`
- **Limitações Reconhecidas:** `Tamanho gigantesco dos arquivos brutos`
- **Evidências Citáveis:** `EVID_045_01`, `EVID_045_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Compara Com:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Avalia Dataset:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Comparado Com:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*

### Arestas no Grafo da Literatura
- `[[artigo_004]]` (*ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*) $\xrightarrow{\text{utiliza_metodologia}}$ `[[artigo_045]]`: Aplica decomposição no domínio da frequência (RFFT) inspirada na ciclostacionariedade comprovada no UGR'16.

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/UGR_16 Dataset|Dataset UGR'16 e Ciclostacionariedade]] — 🌟 **Definição Canônica**

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_009 — Categoria: Teoria / Metodologia|CLAIM_009 (Teoria / Metodologia)]] — *"O tráfego de rede exibe propriedades de ciclostacionariedade e densidade espectral no domínio da frequência que permitem discriminar anomalias periódicas e ataques volumétricos."*
  - *Aplicação na Tese:* Citação direta no Capítulo 1 e Capítulo 3 para justificar a janela de Hann e RFFT no especialista de frequência do ALF-MoE.

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: UGR'16|UGR'16]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_045_01` — DEFINIÇÃO
> [!quote] EVID_045_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição de tráfego de rede como um processo estocástico ciclostacionário que exibe padrões periódicos e harmônicos no domínio da frequência.
> **Localização:** Seção 2 (Cyclostationarity in Network Traffic), Páginas 413-415
>
> *"Network traffic exhibits cyclostationary properties where statistical moments vary periodically across daily, hourly, and weekly operational cycles, making frequency-domain representations optimal for capturing periodic baseline dynamics and harmonic disturbances."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 (item 4) e Capítulo 3 para fundamentar teoricamente a inclusão do especialista no domínio da frequência (CAE com janela de Hann e RFFT) no ALF-MoE.

### `EVID_045_02` — EMPÍRICA
> [!quote] EVID_045_02 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O dataset UGR'16 comprova que ataques volumétricos e varreduras causam distorções agudas na densidade espectral do tráfego.
> **Localização:** Seção 5 (Attack Detection and Evaluation), Páginas 418-422
>
> *"Empirical results on the four-month ISP capture demonstrate that malicious intrusions such as DoS and port scans manifest as significant structural deviations in spectral density components, distinctly separating from benign cyclostationary trends."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta o uso de Transformada de Fourier (RFFT) e filtragem frequencial para discriminação de ataques em redes de alta taxa.

## 📦 Entrada BibTeX
```bibtex
@article{ugr162021,
  title = {UGR‘16: A new dataset for the evaluation of cyclostationarity-based network IDSs},
  author = {Maciá-Fernández, Gabriel and Camacho, José and Magán-Carrión, Roberto and García-Teodoro, Pedro and Therón, Roberto},
  journal = {Computers \& Security},
  year = {2018},
  doi = {10.1016/j.cose.2017.11.004},
  volume = {73},
  pages = {411-424},
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
