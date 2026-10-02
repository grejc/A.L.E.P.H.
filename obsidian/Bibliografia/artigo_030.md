---
id: artigo_030
title: 'P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4'
authors:
- Yaying Chen
- Siamak Layeghy
- Liam Daly Manocchio
- Marius Portmann
year: 2025
bibtex_key: p4nids2025
doi: 10.1007/978-3-031-92611-2_24
venue: Lecture Notes in Networks and Systems, Vol. 1204, pp. 355-373 (arXiv:2411.17987)
keywords:
- P4 Language
- Programmable Data Plane
- Hardware Offloading
- High-Performance NIDS
- Line-Rate Monitoring
- NetFlow Features
area: Network Security / Programmable Switches / P4 / High-Performance NIDS
datasets:
- CIC-IDS-2017
- NetFlow-v9 benchmarks
models:
- P4 Programmable Pipeline
- Match-Action Tables
- Stateful Register Arrays
- Software Machine Learning Controller
aliases:
- 'P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4'
- p4nids2025
- artigo_030
tags:
- bibliografia
- alf-moe
- artigo
---

# P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4

> **Citação ABNT Sugerida:** CHEN, Y.; LAYEGHY, S.; MANOCCHIO, L. D.; PORTMANN, M.. P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4. In: **Lecture Notes in Networks and Systems, Vol. 1204, pp. 355-373 (arXiv:2411.17987)**, 2025.
> **Chave BibTeX:** `p4nids2025` | **Arquivo TXT:** `P4-NIDS__High-Performance_Network_Monitoring_and_Intrusion_Detection_in_P4.txt` | **DOI:** `10.1007/978-3-031-92611-2_24`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_030` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Security / Programmable Switches / P4 / High-Performance NIDS |
| **Veículo de Publicação** | Lecture Notes in Networks and Systems, Vol. 1204, pp. 355-373 (arXiv:2411.17987) |
| **Datasets Utilizados** | CIC-IDS-2017, NetFlow-v9 benchmarks |
| **Modelos / Algoritmos** | P4 Programmable Pipeline, Match-Action Tables, Stateful Register Arrays, Software Machine Learning Controller |
| **Palavras-Chave** | P4 Language, Programmable Data Plane, Hardware Offloading, High-Performance NIDS, Line-Rate Monitoring, NetFlow Features |

## 🎯 Problema Abordado
NIDS baseados exclusivamente em software implementados em servidores convencionais não conseguem processar tráfego em velocidades de linha de redes modernas (10 Gbps, 40 Gbps e 100 Gbps), sofrendo com descarte massivo de pacotes durante picos volumétricos de tráfego.

## 🔬 Metodologia
Desenvolvimento do P4-NIDS utilizando a linguagem de plano de dados programável P4 sobre switches de hardware e software; descarregamento (offloading) da extração de fluxos, contadores de pacotes/bytes e filtragem inicial de ataques volumétricos diretamente nas ASICs do plano de dados em taxa de linha.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O P4-NIDS atinge processamento em velocidade de linha sem perda de pacotes em taxas superiores a 40 Gbps, mitigando ataques volumétricos de negação de serviço em microssegundos no plano de dados e encaminhando apenas fluxos ambíguos para classificadores avançados de aprendizado de máquina no plano de controle.

**Contribuições Centrais:**
- Arquitetura de NIDS em duas camadas: plano de dados em P4 para taxa de linha e plano de controle com ML.
- Implementação de registradores stateful para cálculo de métricas de fluxo diretamente em hardware.
- Demonstração experimental de mitigação com latência na faixa de microssegundos.

## ⚠️ Limitações Identificadas
Restrições de memória de registradores e limitações aritméticas das ASICs programáveis (ausência de suporte a operações de ponto flutuante ou cálculo de exponenciais no plano de dados do switch).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `P4 Language`, `Plano de Dados Programável`, `Processamento em Velocidade de Linha`, `Offloading em Hardware`
- **Problemas Focais:** `Gargalos de CPU em servidores de NIDS de software`, `Perda de pacotes em redes de 40/100 Gbps`
- **Métodos Empregados:** `Programação de tabelas Match-Action em P4`, `Uso de registradores de switch`, `Arquitetura híbrida Data Plane / Control Plane`
- **Modelos e Arquiteturas:** `P4-NIDS Pipeline`, `Switch ASIC Engine`
- **Bases de Dados:** `CIC-IDS-2017`, `Tráfego sintetizado em alta taxa`
- **Resultados Chave:** `Processamento em velocidade de linha sem perda a 40 Gbps`, `Mitigação em microssegundos`
- **Limitações Reconhecidas:** `Falta de operações de ponto flutuante no chip do switch`
- **Evidências Citáveis:** `EVID_030_01`, `EVID_030_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: NIDS de alto desempenho em P4

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado|Cadeia 2: Da Ineficácia Monolítica ao Mixture-of-Experts Calibrado]] — **Etapa LACUNA:** Otimização de inferência de MoE via quantização INT8 e aceleração em hardware P4

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Plano de Dados P4 SDN|Plano de Dados P4 SDN]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_030_01` — DEFINIÇÃO
> [!quote] EVID_030_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição de planos de dados programáveis em P4 como tecnologia chave para monitoramento e mitigação em alta taxa de transferência.
> **Localização:** Seção 1 (Introduction) e Seção 2 (P4 Background), Páginas 355-358
>
> *"The P4 programming language enables software-defined data planes to inspect, parse, and manipulate packets directly at line-rate within network switches, eliminating CPU packet drop bottlenecks."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 2 para embasar arquiteturas de monitoramento de alta taxa e defesa em profundidade.

### `EVID_030_02` — METODOLÓGICA
> [!quote] EVID_030_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Arquiteturas hierárquicas descarregam a filtragem preliminar e agregação de fluxo no plano de dados programável, liberando modelos analíticos de IA para fluxos complexos.
> **Localização:** Seção 3 (P4-NIDS Architecture Design), Páginas 359-363
>
> *"By offloading flow state tracking and coarse anomaly filtering to the P4 switch hardware, downstream machine learning systems are relieved from packet processing overhead, receiving pre-aggregated flow telemetry."*
>
> **Aplicabilidade na Tese ALF-MoE:** Justifica o desacoplamento entre módulos de extração de fluxo e a rede de inferência profunda no pipeline de produção.

## 📦 Entrada BibTeX
```bibtex
@article{p4nids2025,
  title = {{P4-NIDS}: High-Performance Network Monitoring and Intrusion Detection in {P4}},
  author = {Chen, Yaying and Layeghy, Siamak and Manocchio, Liam Daly and Portmann, Marius},
  journal = {Lecture Notes in Networks and Systems},
  year = {2025},
  doi = {10.1007/978-3-031-92611-2_24},
  pages = {355-373},
  publisher = {Springer Nature Switzerland}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
