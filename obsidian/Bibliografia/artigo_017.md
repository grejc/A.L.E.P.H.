---
id: artigo_017
title: Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems
authors:
- Antanas Čenys
- Simran Kaur Hora
- Nikolaj Goranin
year: 2025
bibtex_key: emuiot2025
doi: 10.3390/s25165077
venue: Sensors 2025, 25(16), 5077
keywords:
- EmuIoT-VT
- Emulation Dataset
- IoT Security
- NIDS
- Virtual Testbed
- Network Traffic Generation
area: IoT Cyber Security / Emulation Datasets / Benchmark Creation
datasets:
- EmuIoT-VT (proposto)
- CIC-IDS-2017
- CICIoT2023
models:
- Random Forest
- Support Vector Machines
- Multi-Layer Perceptron (MLP)
- k-Nearest Neighbors (kNN)
aliases:
- Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems
- emuiot2025
- artigo_017
tags:
- bibliografia
- alf-moe
- artigo
---

# Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems

> **Citação ABNT Sugerida:** ČENYS, A.; HORA, S. K.; GORANIN, N.. Emulation-Based Dataset EmuIoT-VT for NIDS in IoT Systems. In: **Sensors 2025, 25(16), 5077**, 2025.
> **Chave BibTeX:** `emuiot2025` | **Arquivo TXT:** `Emulation-Based_Dataset_EmuIoT-VT_for_NIDS_in_IoT_Systems_2025.txt` | **DOI:** `10.3390/s25165077`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_017` |
| **Ano** | 2025 |
| **Área de Pesquisa** | IoT Cyber Security / Emulation Datasets / Benchmark Creation |
| **Veículo de Publicação** | Sensors 2025, 25(16), 5077 |
| **Datasets Utilizados** | EmuIoT-VT (proposto), CIC-IDS-2017, CICIoT2023 |
| **Modelos / Algoritmos** | Random Forest, Support Vector Machines, Multi-Layer Perceptron (MLP), k-Nearest Neighbors (kNN) |
| **Palavras-Chave** | EmuIoT-VT, Emulation Dataset, IoT Security, NIDS, Virtual Testbed, Network Traffic Generation |

## 🎯 Problema Abordado
A montagem de bancadas físicas de IoT em larga escala é proibitivamente cara e difícil de replicar; simuladores de tráfego simplificados desconsideram comportamentos de pilha de rede de sistemas operacionais reais (como TinyOS, Contiki e Linux embarcado).

## 🔬 Metodologia
Desenvolvimento do ambiente de emulação virtual EmuIoT-VT integrando nós emulados com instâncias completas de software embarcado comunicando-se por redes virtuais; injeção de múltiplos cenários de ataque (DDoS, sniffing, injeção de pacotes MQTT e CoAP) e captura direta de tráfego de rede.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O EmuIoT-VT oferece reprodutibilidade perfeita de condições de teste com mais de 3 milhões de pacotes e fluxos categorizados sob protocolos IoT especializados; modelos treinados no EmuIoT-VT demonstraram alta transferibilidade para tráfego físico real.

**Contribuições Centrais:**
- Metodologia completa de emulação de ambientes IoT de alta fidelidade.
- Disponibilização do dataset EmuIoT-VT com rastreabilidade de fluxos.
- Benchmark comparativo com datasets físicos como CICIoT2023.

## ⚠️ Limitações Identificadas
Restrições de recursos de hardware do nó hospedeiro da emulação ao escalar para centenas de instâncias concorrentes de sistemas operacionais emulados.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Emulação Virtual de IoT`, `Dataset EmuIoT-VT`, `Fidelidade de Pilha de Rede`, `Reprodutibilidade`
- **Problemas Focais:** `Alto custo de bancadas físicas`, `Irrealismo de simuladores sintéticos`
- **Métodos Empregados:** `Emulação baseada em containers e nós virtuais`, `Captura de tráfego MQTT/CoAP`, `Extração de fluxos`
- **Modelos e Arquiteturas:** `Random Forest`, `MLP`, `SVM`
- **Bases de Dados:** `EmuIoT-VT`
- **Resultados Chave:** `Alta reprodutibilidade e transferibilidade para redes físicas`
- **Limitações Reconhecidas:** `Escalabilidade limitada pelo servidor de emulação`
- **Evidências Citáveis:** `EVID_017_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Compara Com:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Fundamenta Dataset:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*

## 🎓 Integração com a Tese ALF-MoE

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CICIoT2023|CICIoT2023]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_017_01` — COMPARATIVA
> [!quote] EVID_017_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Datasets emulados com pilhas de software reais preenchem a lacuna entre simulações sintéticas simplificadas e bancadas físicas de alto custo.
> **Localização:** Seção 2 (Related Work and Methodology), Páginas 3-5
>
> *"Emulation-based testbeds provide architectural fidelity matching physical hardware while enabling deterministic repeatability and controlled injection of edge intrusion scenarios."*
>
> **Aplicabilidade na Tese ALF-MoE:** Útil para contextualizar alternativas metodológicas de geração de dados na revisão sobre datasets de cibersegurança.

## 📦 Entrada BibTeX
```bibtex
@article{emuiot2025,
  title = {Emulation-Based Dataset {EmuIoT-VT} for {NIDS} in {IoT} Systems},
  author = {Čenys, Antanas and Hora, Simran Kaur and Goranin, Nikolaj},
  journal = {Sensors},
  year = {2025},
  doi = {10.3390/s25165077},
  volume = {25},
  number = {16},
  pages = {5077},
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
