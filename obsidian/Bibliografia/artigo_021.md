---
id: artigo_021
title: 'HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day
  e sua Extensão Ensemble'
authors:
- Fabiano Carlos da Silva
year: 2025
bibtex_key: hsae2025
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Dissertação de Mestrado em Ciência da Computação, Universidade Federal de Pernambuco
  (UFPE)
keywords:
- Detecção de Intrusão
- Ataques Zero-Day
- Autoencoder Híbrido
- Ensemble Learning
- Aprendizado Não Supervisionado
- HSAE
area: Network Intrusion Detection / Unsupervised Learning / Autoencoders / Zero-Day
  Attacks
datasets:
- CIC-IDS-2017
- CSE-CIC-IDS2018
- UNSW-NB15
models:
- Convolutional Autoencoder (CAE)
- Dense Autoencoder
- HSAE
- Ensemble de Autoencoders
- Limiarização Estatística de Reconstrução
aliases:
- 'HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day
  e sua Extensão Ensemble'
- hsae2025
- artigo_021
tags:
- bibliografia
- alf-moe
- artigo
---

# HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble

> **Citação ABNT Sugerida:** SILVA, F. C. D.. HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble. In: **Dissertação de Mestrado em Ciência da Computação, Universidade Federal de Pernambuco (UFPE)**, 2025.
> **Chave BibTeX:** `hsae2025` | **Arquivo TXT:** `HSAE: Um_Autoencoder_Hibrido_Nao_Supervisionado_para_Deteccao_de_Ataques_Zero-Day_e_sua_Extensao_Ensemble.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_021` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Network Intrusion Detection / Unsupervised Learning / Autoencoders / Zero-Day Attacks |
| **Veículo de Publicação** | Dissertação de Mestrado em Ciência da Computação, Universidade Federal de Pernambuco (UFPE) |
| **Datasets Utilizados** | CIC-IDS-2017, CSE-CIC-IDS2018, UNSW-NB15 |
| **Modelos / Algoritmos** | Convolutional Autoencoder (CAE), Dense Autoencoder, HSAE, Ensemble de Autoencoders, Limiarização Estatística de Reconstrução |
| **Palavras-Chave** | Detecção de Intrusão, Ataques Zero-Day, Autoencoder Híbrido, Ensemble Learning, Aprendizado Não Supervisionado, HSAE |

## 🎯 Problema Abordado
Classificadores supervisionados dependem de rótulos prévios de ataques e falham na detecção de ataques inéditos (zero-day); métodos não supervisionados baseados em autoencoders simples sofrem com alta taxa de falsos positivos devido à complexidade da distribuição de tráfego legítimo.

## 🔬 Metodologia
Desenvolvimento do HSAE (Hybrid Semi-Supervised / Unsupervised Autoencoder) combinando camadas convolucionais 1D e blocos densos para reconstrução de sinal de tráfego benigno; extensão da arquitetura através de um ensemble de múltiplos autoencoders especializados operando em subespaços complementares de atributos com decisão agregada.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O ensemble HSAE superou métodos de ponta na identificação de classes de ataque completamente omitidas do treinamento (zero-day), obtendo AUC-ROC de 0.962 no CIC-IDS-2017 e reduzindo pela metade a taxa de falsos alarmes em comparação com autoencoders individuais isolados.

**Contribuições Centrais:**
- Arquitetura híbrida de autoencoder não supervisionado HSAE.
- Framework de ensemble de múltiplos autoencoders para redução de variância e falsos positivos.
- Metodologia rigorosa de avaliação zero-day ocultando classes inteiras de ataque do treinamento.

## ⚠️ Limitações Identificadas
Cálculo do limiar de reconstrução (thresholding) requer calibragem cuidadosa sob variações de tráfego em rede real para evitar falsos alarmes sazonais.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Autoencoder Híbrido`, `Ensemble de Autoencoders`, `Detecção de Zero-Day`, `Erro de Reconstrução`
- **Problemas Focais:** `Cegueira a ataques inéditos em modelos supervisionados`, `Falsos positivos em autoencoders isolados`
- **Métodos Empregados:** `Treinamento apenas com tráfego legítimo`, `Reconstrução convolucional e densa`, `Combinação em ensemble`
- **Modelos e Arquiteturas:** `HSAE`, `CAE`, `Ensemble HSAE`
- **Bases de Dados:** `CIC-IDS-2017`, `CSE-CIC-IDS2018`, `UNSW-NB15`
- **Resultados Chave:** `AUC-ROC de 0.962 em zero-day omitido`, `Redução de 50% em falsos alarmes`
- **Limitações Reconhecidas:** `Sensibilidade na escolha estática do threshold`
- **Evidências Citáveis:** `EVID_021_01`, `EVID_021_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Fundamenta Metodologia:**
  - [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification*
- **Relacionado:**
  - [[artigo_025]] — *One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_025]] — *One-for-All Does Not Work! Enhancing Vulnerability Detection by Mixture-of-Experts (MoE)*
  - [[artigo_048]] — *A convolutional autoencoder architecture for robust network intrusion detection in embedded systems*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/Convolutional Autoencoder (CAE)|Convolutional Autoencoder (CAE) e Detecção de Anomalias]] — Papel: HSAE e ensemble de autoencoders para ataques zero-day

### Afirmações / Claims Sustentados
- [[Afirmacoes_e_Claims#CLAIM_007 — Categoria: Metodologia / Empírico|CLAIM_007 (Metodologia / Empírico)]] — *"Autoencoders convolucionais (CAE) treinados exclusivamente sobre tráfego legítimo são capazes de identificar anomalias desconhecidas e ataques zero-day através do aumento do erro de reconstrução, fornecendo imunidade a ruídos locais."*
  - *Aplicação na Tese:* Embasamento conceitual da detecção não supervisionada via erro de reconstrução.

### Controvérsias da Literatura
- [[Contradicoes_e_Divergencias#CONTROV_004 — Detecção de Ataques Zero-Day: Classificadores Supervisionados vs. Modelagem Não-Supervisionada de Normalidade (Autoencoders / CAE)|CONTROV_004 — Detecção de Ataques Zero-Day: Classificadores Supervisionados vs. Modelagem Não-Supervisionada de Normalidade (Autoencoders / CAE)]]
  - **Posição B (Visão Crítica / Adotada pela Tese):** *"Modelos puramente supervisionados falham catastroficamente ao encontrar ataques zero-day ou mutações inéditas não presentes no treinamento; métodos não supervisionados baseados em modelagem de normalidade (como autoencoders convolucionais CAE/HSAE) são essenciais para isolar desvios de normalidade sem rótulos prévios."*

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: CSE-CIC-IDS2018|CSE-CIC-IDS2018]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Autoencoders|Autoencoders]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_021_01` — FUNDAMENTAÇÃO TEÓRICA
> [!quote] EVID_021_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Autoencoders treinados exclusivamente sobre tráfego benigno detectam ataques inéditos (zero-day) através do aumento do erro de reconstrução.
> **Localização:** Capítulo 2 (Fundamentação Teórica), Seção 2.4, Páginas 32-36
>
> *"Ao treinar o autoencoder exclusivamente com fluxos legítimos, a rede aprende a variedade compacta do comportamento benigno; anomalias e ataques zero-day desviam dessa distribuição gerando erros de reconstrução estatisticamente superiores ao limiar estabelecido."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta o princípio de funcionamento do especialista CAE (Convolutional Autoencoder) do ALF-MoE para modelar desvios de normalidade.

### `EVID_021_02` — METODOLÓGICA
> [!quote] EVID_021_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A combinação de múltiplos autoencoders em conjunto (ensemble) atenua expressivamente a taxa de falsos alarmes em comparação com modelos individuais isolados.
> **Localização:** Capítulo 4 (Proposta HSAE Ensemble), Seção 4.2, Páginas 68-72
>
> *"A agregação de decisões de múltiplos modelos especializados em ensemble reduz a variância individual das estimativas de erro, suprimindo em mais de 50% falsos alarmes transitórios causados por rajadas benignas atípicas."*
>
> **Aplicabilidade na Tese ALF-MoE:** Citado na Introdução e no Capítulo de Fundamentação para justificar por que o aprendizado em conjunto é superior a classificadores isolados.

## 📦 Entrada BibTeX
```bibtex
@mastersthesis{hsae2025,
  title = {HSAE: Um Autoencoder Híbrido Não Supervisionado para Detecção de Ataques Zero-Day e sua Extensão Ensemble},
  author = {Silva, Fabiano Carlos da},
  year = {2025},
  school = {Universidade Federal de Pernambuco},
  type = {Dissertação de Mestrado}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
