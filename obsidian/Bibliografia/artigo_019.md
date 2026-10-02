---
id: artigo_019
title: 'F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado'
authors:
- Jonathas Alves de Oliveira
- Vinícius P. Gonçalves
- Geraldo P. Rocha Filho
year: 2025
bibtex_key: fnids2025
doi: 10.5753/sbrc_estendido.2025.6896
venue: Anais Estendidos do XLIII Simpósio Brasileiro de Redes de Computadores e Sistemas
  Distribuídos (SBRC 2025), pp. 212-221
keywords:
- Aprendizado Federado
- Sistemas de Detecção de Intrusão
- Privacidade de Dados
- Segurança Colaborativa
- F-NIDS
area: Federated Learning / Collaborative NIDS / Privacy-Preserving Security
datasets:
- CIC-IDS-2017
- UNSW-NB15
models:
- Federated Averaging (FedAvg)
- Multi-Layer Perceptron (MLP)
- Deep Neural Network (DNN)
aliases:
- 'F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado'
- fnids2025
- artigo_019
tags:
- bibliografia
- alf-moe
- artigo
---

# F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado

> **Citação ABNT Sugerida:** OLIVEIRA, J. A. D.; GONÇALVES, V. P.; FILHO, G. P. R.. F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado. In: **Anais Estendidos do XLIII Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2025), pp. 212-221**, 2025.
> **Chave BibTeX:** `fnids2025` | **Arquivo TXT:** `F-NIDS__Sistema_de_Deteccao_de_Intrusao_baseado_em_Aprendizado_Federado.txt` | **DOI:** `10.5753/sbrc_estendido.2025.6896`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_019` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Federated Learning / Collaborative NIDS / Privacy-Preserving Security |
| **Veículo de Publicação** | Anais Estendidos do XLIII Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2025), pp. 212-221 |
| **Datasets Utilizados** | CIC-IDS-2017, UNSW-NB15 |
| **Modelos / Algoritmos** | Federated Averaging (FedAvg), Multi-Layer Perceptron (MLP), Deep Neural Network (DNN) |
| **Palavras-Chave** | Aprendizado Federado, Sistemas de Detecção de Intrusão, Privacidade de Dados, Segurança Colaborativa, F-NIDS |

## 🎯 Problema Abordado
O compartilhamento de dados brutos de tráfego de rede entre organizações para treinamento conjunto de NIDS é inviável devido a leis de privacidade (como LGPD e GDPR) e segredos corporativos; modelos locais isolados sofrem de baixa capacidade de detecção de ataques não vistos localmente.

## 🔬 Metodologia
Sistema F-NIDS empregando o algoritmo Federated Averaging (FedAvg) sobre modelos locais de redes neurais profundas instalados em múltiplos nós autônomos; apenas atualizações de pesos e gradientes são transmitidas ao servidor de agregação central.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O F-NIDS alcança acurácia de 97.4%, aproximando-se do treinamento centralizado tradicional (diferença inferior a 1.2%) enquanto mantém dados de tráfego estritamente confidenciais nas instalações dos clientes locais.

**Contribuições Centrais:**
- Arquitetura de NIDS federado colaborativo para redes corporativas.
- Avaliação sob particionamento de dados não-IID entre diferentes entidades.
- Demonstração da preservação da privacidade sem degradação crítica de acurácia.

## ⚠️ Limitações Identificadas
Vulnerabilidade a envenenamento de modelo (poisoning attacks) caso nós participantes injetem gradientes adversariais durante a rodada federada.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Aprendizado Federado`, `F-NIDS`, `Privacidade de Tráfego`, `Agregação Segura`
- **Problemas Focais:** `Impossibilidade de centralizar dados por sigilo e LGPD`, `Modelos locais com visão restrita`
- **Métodos Empregados:** `FedAvg`, `Treinamento descentralizado em clientes`, `Agregação periódica de pesos`
- **Modelos e Arquiteturas:** `DNN Federada`, `MLP`
- **Bases de Dados:** `CIC-IDS-2017`, `UNSW-NB15`
- **Resultados Chave:** `Acurácia de 97.4% comparável a modelo centralizado`, `Zero transmissão de tráfego bruto`
- **Limitações Reconhecidas:** `Comunicação em múltiplas rodadas e risco de envenenamento`
- **Evidências Citáveis:** `EVID_019_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

## 🎓 Integração com a Tese ALF-MoE

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]], [[Rede_Intelectual#Benchmark: UNSW-NB15|UNSW-NB15]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_019_01` — METODOLÓGICA
> [!quote] EVID_019_01 (Relevância: 4/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** O aprendizado federado viabiliza a cooperação entre múltiplos sensores de detecção de intrusão preservando a privacidade dos dados de rede.
> **Localização:** Seção 1 (Introdução) e Seção 3 (Arquitetura F-NIDS), Páginas 213-216
>
> *"O aprendizado federado permite que múltiplos participantes treinem colaborativamente um modelo global compartilhado sem necessidade de centralizar ou compartilhar publicamente seus registros de tráfego de rede sensíveis."*
>
> **Aplicabilidade na Tese ALF-MoE:** Contextualiza a evolução das arquiteturas de treinamento distribuído e privacidade de dados em NIDS no Capítulo 2.

## 📦 Entrada BibTeX
```bibtex
@article{fnids2025,
  title = {{F-NIDS}: Sistema de Detecção de Intrusão baseado em Aprendizado Federado},
  author = {de Oliveira, Jonathas Alves and Gonçalves, Vinícius P. and Rocha Filho, Geraldo P.},
  journal = {Anais Estendidos do XLIII Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2025)},
  year = {2025},
  doi = {10.5753/sbrc_estendido.2025.6896},
  pages = {212-221},
  publisher = {Sociedade Brasileira de Computação - SBC}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
