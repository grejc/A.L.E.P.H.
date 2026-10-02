---
id: artigo_014
title: Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning
authors:
- João Paulo Araujo Bonomo
year: 2025
bibtex_key: canml2025
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Trabalho de Conclusão de Curso (Graduação em Ciências da Computação), Universidade
  Federal de Santa Catarina (UFSC)
keywords:
- Redes Intraveiculares
- Controller Area Network (CAN)
- Machine Learning
- Detecção de Intrusão
- Segurança Automotiva
area: Automotive Cybersecurity / CAN Bus Intrusion Detection / Machine Learning
datasets:
- Car-Hacking Dataset (HCRL - Korea University)
- CAN-intrusion-dataset
models:
- Decision Trees (DT)
- Random Forest (RF)
- k-Nearest Neighbors (kNN)
- Multilayer Perceptron (MLP)
- Naive Bayes
- Support Vector Machines (SVM)
aliases:
- Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning
- canml2025
- artigo_014
tags:
- bibliografia
- alf-moe
- artigo
---

# Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning

> **Citação ABNT Sugerida:** BONOMO, J. P. A.. Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning. In: **Trabalho de Conclusão de Curso (Graduação em Ciências da Computação), Universidade Federal de Santa Catarina (UFSC)**, 2025.
> **Chave BibTeX:** `canml2025` | **Arquivo TXT:** `Detecção_de_Ataques_em_Redes_Intraveiculares_CAN_com_Técnicas_de_Machine_Learning_2025.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_014` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Automotive Cybersecurity / CAN Bus Intrusion Detection / Machine Learning |
| **Veículo de Publicação** | Trabalho de Conclusão de Curso (Graduação em Ciências da Computação), Universidade Federal de Santa Catarina (UFSC) |
| **Datasets Utilizados** | Car-Hacking Dataset (HCRL - Korea University), CAN-intrusion-dataset |
| **Modelos / Algoritmos** | Decision Trees (DT), Random Forest (RF), k-Nearest Neighbors (kNN), Multilayer Perceptron (MLP), Naive Bayes, Support Vector Machines (SVM) |
| **Palavras-Chave** | Redes Intraveiculares, Controller Area Network (CAN), Machine Learning, Detecção de Intrusão, Segurança Automotiva |

## 🎯 Problema Abordado
Vulnerabilidade das redes automotivas CAN devido à ausência de autenticação e criptografia de mensagens, permitindo ataques de falsificação de ID, injeção contínua (DoS) e ataques fuzzy que afetam a dirigibilidade e a segurança dos ocupantes do veículo.

## 🔬 Metodologia
Investigação sistemática de algoritmos de aprendizado de máquina supervisionado sobre sequências de identificadores e intervalos de tempo entre mensagens no barramento CAN automotivo; análise comparativa de pré-processamento temporal e janelas deslizantes.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Random Forest e Decision Trees alcançaram métricas de acurácia e F1-score próximas a 99.9% na detecção de ataques de DoS e Fuzzy; ataques de spoofing direcionados (Gear/RPM) exigem atributos temporais de frequência de envio para evitar falsos negativos.

**Contribuições Centrais:**
- Revisão estruturada dos protocolos e vulnerabilidades do barramento CAN automotivo.
- Comparação empírica de múltiplos algoritmos de classificação de ataques em rede CAN.
- Demonstração do papel crucial dos intervalos temporais (IAT) na discriminação de injeções fraudulentas de quadros.

## ⚠️ Limitações Identificadas
Dependência de matriz de dados de treinamento capturada sob condições de direção normais pré-estabelecidas; sensibilidade a mudanças de comportamento em diferentes modelos de veículos.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `CAN Bus Security`, `In-Vehicle NIDS`, `Machine Learning`, `IAT Dynamics`
- **Problemas Focais:** `Ausência de criptografia em redes veiculares`, `Ataques de DoS, Fuzzy e Spoofing em ECUs`
- **Métodos Empregados:** `Janelamento temporal`, `Extração de delta de tempo (IAT)`, `Classificação supervisionada`
- **Modelos e Arquiteturas:** `Random Forest`, `Decision Tree`, `MLP`, `kNN`
- **Bases de Dados:** `Car-Hacking Dataset`
- **Resultados Chave:** `Acurácia > 99.9% para DoS/Fuzzy`, `Necessidade de IAT para spoofing gradual`
- **Limitações Reconhecidas:** `Variação conforme o modelo e fabricante do veículo`
- **Evidências Citáveis:** `EVID_014_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_010]] — *DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles*
  - [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_010]] — *DAIRE: A lightweight AI model for real-time detection of Controller Area Network attacks in the Internet of Vehicles*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Inter-Arrival Time (IAT) e Atributos Temporais|Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo]] — Papel: IAT como discriminador crítico em redes intraveiculares CAN

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_005 — Categoria: Empírico / Metodologia|CLAIM_005 (Empírico / Metodologia)]] — *"A dinâmica temporal e os intervalos entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) fornecem poder discriminatório essencial para identificar ameaças evasivas que mimetizam volumes benignos de tráfego, como canais de comando e controle (C2) e botnets."*
  - *Aplicação na Tese:* Demonstração independente da relevância do IAT em redes veiculares e industriais.

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: Car-Hacking (CAN)|Car-Hacking (CAN)]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_014_01` — METODOLÓGICA
> [!quote] EVID_014_01 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A frequência de transmissão e o intervalo entre mensagens consecutivas (IAT) são os discriminadores mais sensíveis para detectar anomalias e injeções fraudulentas.
> **Localização:** Capítulo 4 (Metodologia e Resultados), Seção 4.3, Páginas 52-56
>
> *"A análise dos intervalos entre chegadas de mensagens (Inter-Arrival Time) revela anomalias na cadência de envio característica de injeções de DoS e spoofing, constituindo o atributo de maior poder discriminatório no barramento."*
>
> **Aplicabilidade na Tese ALF-MoE:** Reforça a justificativa metodológica para a inclusão de atributos de IAT e o especialista temporal (GRU) no ALF-MoE.

## 📦 Entrada BibTeX
```bibtex
@mastersthesis{canml2025,
  title = {Detecção de Ataques em Redes Intraveiculares {CAN} com Técnicas de Machine Learning},
  author = {Bonomo, João Paulo Araujo},
  year = {2025},
  school = {Universidade Federal de Santa Catarina},
  type = {Trabalho de Conclusão de Curso (Graduação)}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
