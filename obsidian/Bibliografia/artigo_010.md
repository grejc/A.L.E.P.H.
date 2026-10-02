---
id: artigo_010
title: 'DAIRE: A lightweight AI model for real-time detection of Controller Area Network
  attacks in the Internet of Vehicles'
authors:
- Shahid Alam
- Amina Jameel
- Zahida Parveen
- Ehab Alnfrawy
- Adeela Ashraf
- Raza Uddin
- Jamal Aqib
year: 2026
bibtex_key: daire2025
doi: 10.1016/j.mlwa.2026.100859
venue: Machine Learning with Applications 23 (2026) 100859
keywords:
- Controller Area Network
- Internet of Vehicles
- Intrusion Detection
- Lightweight AI
- Real-Time Detection
- CAN Attacks
area: In-Vehicle Networks / CAN Bus Security / Lightweight Machine Learning
datasets:
- Car-Hacking Dataset
- Survival Analysis CAN Dataset
models:
- DAIRE (Lightweight Neural Model)
- Decision Tree
- Support Vector Machine
- kNN
- Random Forest
aliases:
- 'DAIRE: A lightweight AI model for real-time detection of Controller Area Network
  attacks in the Internet of Vehicles'
- daire2025
- artigo_010
tags:
- bibliografia
- alf-moe
- artigo
---

# DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles

> **Citação ABNT Sugerida:** ALAM, S.; JAMEEL, A.; PARVEEN, Z.; ALNFRAWY, E.; ASHRAF, A.; UDDIN, R.; AQIB, J.. DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles. In: **Machine Learning with Applications 23 (2026) 100859**, 2026.
> **Chave BibTeX:** `daire2025` | **Arquivo TXT:** `DAIRE__A_lightweight_AI_model_for_real-time_detection_of_Controller_Area_Network_attacks_in_the_Internet_of_Vehicles.txt` | **DOI:** `10.1016/j.mlwa.2026.100859`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_010` |
| **Ano** | 2026 |
| **Área de Pesquisa** | In-Vehicle Networks / CAN Bus Security / Lightweight Machine Learning |
| **Veículo de Publicação** | Machine Learning with Applications 23 (2026) 100859 |
| **Datasets Utilizados** | Car-Hacking Dataset, Survival Analysis CAN Dataset |
| **Modelos / Algoritmos** | DAIRE (Lightweight Neural Model), Decision Tree, Support Vector Machine, kNN, Random Forest |
| **Palavras-Chave** | Controller Area Network, Internet of Vehicles, Intrusion Detection, Lightweight AI, Real-Time Detection, CAN Attacks |

## 🎯 Problema Abordado
O protocolo Controller Area Network (CAN) amplamente utilizado em sistemas automotivos não possui mecanismos nativos de criptografia ou autenticação, tornando veículos conectados vulneráveis a injeção de pacotes maliciosos; modelos profundos convencionais são pesados demais para execução sob restrições estritas de tempo real e memória das ECUs automotivas.

## 🔬 Metodologia
Modelo DAIRE combinando seleção leve de atributos por entropia, representação condensada de identificadores CAN e rede neural compacta otimizada para baixíssima latência de inferência em microcontroladores.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O DAIRE atinge taxa de detecção superior a 99.8% com latência de inferência de apenas 0.42 milissegundos por mensagem CAN, viabilizando execução em tempo real em Unidades de Controle Eletrônico (ECUs).

**Contribuições Centrais:**
- Arquitetura de IA ultraleve para detecção de anomalias em redes intraveiculares.
- Avaliação de latência e consumo de memória compatíveis com microcontroladores embarcados.
- Detecção eficaz de ataques de DoS, Fuzzy, Spoofing e Gear/RPM injection em redes CAN.

## ⚠️ Limitações Identificadas
Especializado na estrutura de quadros e temporização do barramento CAN; não aplicável diretamente a tráfego IP/TCP de rede tradicional sem adaptação de protocolo.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CAN Bus Security`, `Lightweight Neural Network`, `In-Vehicle Intrusion Detection`, `Sub-millisecond Latency`
- **Problemas Focais:** `Ausência de segurança nativa no barramento CAN`, `Restrições extremas de latência e memória em ECUs`
- **Métodos Empregados:** `Seleção de atributos baseada em entropia`, `Classificação neural compacta`
- **Modelos e Arquiteturas:** `DAIRE`, `Random Forest`, `SVM`
- **Bases de Dados:** `Car-Hacking Dataset`, `Survival Analysis Dataset`
- **Resultados Chave:** `Acurácia > 99.8%`, `Latência de 0.42 ms por quadro CAN`
- **Limitações Reconhecidas:** `Restrito a quadros de barramento veicular`
- **Evidências Citáveis:** `EVID_010_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*

## 🎓 Integração com a Tese ALF-MoE

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: Car-Hacking (CAN)|Car-Hacking (CAN)]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_010_01` — METODOLÓGICA
> [!quote] EVID_010_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Em sistemas embarcados com restrições rígidas de tempo real, a latência de inferência deve ser minimizada para permitir mitigação antes do comprometimento físico.
> **Localização:** Seção 1 (Introduction) e Seção 4 (Results), Páginas 2-7
>
> *"In cyber-physical and in-vehicle systems, detection latency must remain below one millisecond to prevent malicious commands from altering physical vehicle actuators."*
>
> **Aplicabilidade na Tese ALF-MoE:** Contextualiza a importância de restrições de latência na inferência de NIDS quando aplicados a sistemas de missão crítica.

## 📦 Entrada BibTeX
```bibtex
@article{daire2025,
  title = {{DAIRE}: A lightweight {AI} model for real-time detection of Controller Area Network attacks in the Internet of Vehicles},
  author = {Alam, Shahid and Jameel, Amina and Parveen, Zahida and Alnfrawy, Ehab and Ashraf, Adeela and Uddin, Raza and Aqib, Jamal},
  journal = {Machine Learning with Applications},
  year = {2026},
  doi = {10.1016/j.mlwa.2026.100859},
  volume = {23},
  pages = {100859},
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
