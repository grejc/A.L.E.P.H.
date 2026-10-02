---
id: artigo_013
title: Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas
authors:
- Cristiano Antônio de Souza
year: 2023
bibtex_key: fogids2024
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: Tese de Doutorado em Engenharia de Automação e Sistemas, Universidade Federal
  de Santa Catarina (UFSC)
keywords:
- Computação de Nevoeiro
- Internet das Coisas
- Sistemas de Detecção de Intrusão
- Segurança Distribuída
- Prevenção de Intrusão
area: Distributed Systems / Fog Computing / IoT Cyber Security / NIDS
datasets:
- BoT-IoT
- CIC-IDS2017
- NSL-KDD
models:
- Random Forest
- Support Vector Machines
- Redes Neurais Multicamadas (MLP)
- Algoritmos Genéticos para Seleção de Atributos
- Regras Determinísticas Snort/Suricata
aliases:
- Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas
- fogids2024
- artigo_013
tags:
- bibliografia
- alf-moe
- artigo
---

# Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas

> **Citação ABNT Sugerida:** SOUZA, C. A. D.. Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas. In: **Tese de Doutorado em Engenharia de Automação e Sistemas, Universidade Federal de Santa Catarina (UFSC)**, 2023.
> **Chave BibTeX:** `fogids2024` | **Arquivo TXT:** `Deteccao_e_prevencao_de_intrusao_em_computacao_de_nevoeiro_e_Internet_das_Coisas.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_013` |
| **Ano** | 2023 |
| **Área de Pesquisa** | Distributed Systems / Fog Computing / IoT Cyber Security / NIDS |
| **Veículo de Publicação** | Tese de Doutorado em Engenharia de Automação e Sistemas, Universidade Federal de Santa Catarina (UFSC) |
| **Datasets Utilizados** | BoT-IoT, CIC-IDS2017, NSL-KDD |
| **Modelos / Algoritmos** | Random Forest, Support Vector Machines, Redes Neurais Multicamadas (MLP), Algoritmos Genéticos para Seleção de Atributos, Regras Determinísticas Snort/Suricata |
| **Palavras-Chave** | Computação de Nevoeiro, Internet das Coisas, Sistemas de Detecção de Intrusão, Segurança Distribuída, Prevenção de Intrusão |

## 🎯 Problema Abordado
A centralização do processamento de detecção de intrusão na nuvem impõe latência inaceitável e sobrecarga de largura de banda para redes IoT massivas; a computação em nevoeiro (fog computing) descentraliza os serviços, mas os nós intermediários possuem restrições computacionais e necessitam de cooperação hierárquica para mitigar ameaças.

## 🔬 Metodologia
Proposição de uma arquitetura hierárquica e distribuída de detecção e prevenção de intrusões (Fog-IDPS) organizada em três camadas (Edge, Fog e Cloud), integrando módulos de monitoramento contínuo em nós de nevoeiro, detecção híbrida (anomalia e assinatura) e orquestração autônoma de políticas de mitigação.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
A arquitetura em nevoeiro reduziu o tempo de resposta e contenção de ataques em até 78% em comparação com soluções puramente em nuvem, mantendo taxa de detecção superior a 98.4% com baixo consumo de memória nos nós intermediários de nevoeiro.

**Contribuições Centrais:**
- Arquitetura abrangente de três camadas para detecção e prevenção de intrusão em IoT e nevoeiro.
- Protocolo de cooperação e sincronização de assinaturas e vetores de anomalia entre nós de borda.
- Validação experimental em bancada real com tráfego IoT e ataques de botnet/DDoS.

## ⚠️ Limitações Identificadas
Heterogeneidade severa dos nós de nevoeiro (gateways e roteadores) limita a execução de modelos de aprendizado profundo de grande porte sem quantização ou offloading.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Computação de Nevoeiro`, `IDPS Hierárquico`, `Segurança Distribuída`, `Defesa em Profundidade`
- **Problemas Focais:** `Latência excessiva de envio para nuvem`, `Gargalos de banda em redes IoT massivas`
- **Métodos Empregados:** `Arquitetura de três camadas (Borda/Nevoeiro/Nuvem)`, `Seleção de atributos genéticos`, `Filtragem distribuída`
- **Modelos e Arquiteturas:** `Random Forest`, `MLP`, `Snort`
- **Bases de Dados:** `BoT-IoT`, `CIC-IDS2017`
- **Resultados Chave:** `78% de redução no tempo de contenção frente a nuvem pura`, `Detecção > 98.4%`
- **Limitações Reconhecidas:** `Recursos restritos nos gateways de nevoeiro`
- **Evidências Citáveis:** `EVID_013_01`, `EVID_013_02`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_009]] — *CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment*
  - [[artigo_019]] — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_019]] — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
  - [[artigo_033]] — *Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: NIDS distribuído em computação de nevoeiro

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_013_01` — DEFINIÇÃO
> [!quote] EVID_013_01 (Relevância: 5/5 | Grau: Prova a afirmação)
> **Afirmação Sustentada:** Definição de defesa em profundidade e arquitetura de detecção de intrusão hierárquica em infraestruturas distribuídas.
> **Localização:** Capítulo 2 (Fundamentação Teórica), Seção 2.3, Páginas 45-48
>
> *"A defesa em profundidade em ambientes distribuídos requer múltiplos anéis de segurança, posicionando sensores de monitoramento de fluxo nas bordas locais e concentradores analíticos em camadas intermediárias para minimizar o tempo de propagação do ataque."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a contextualização de sistemas distribuídos e defesa em profundidade no Capítulo 1 e Capítulo 2 da tese.

### `EVID_013_02` — METODOLÓGICA
> [!quote] EVID_013_02 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A análise agregada por fluxos estatísticos é mandatória para permitir que nós intermediários processem o tráfego sem inspecionar a carga útil de pacotes individuais.
> **Localização:** Capítulo 3 (Proposta de Arquitetura), Seção 3.2, Páginas 82-85
>
> *"Devido às restrições de memória dos nós de nevoeiro e ao uso de canais cifrados, o monitoramento por fluxos de dados agregados torna-se a estratégia viável para detecção contínua em tempo real."*
>
> **Aplicabilidade na Tese ALF-MoE:** Justifica o uso de representação estatística baseada em fluxos de tráfego nos pipelines de NIDS.

## 📦 Entrada BibTeX
```bibtex
@phdthesis{fogids2024,
  title = {Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas},
  author = {Souza, Cristiano Antônio de},
  year = {2023},
  school = {Universidade Federal de Santa Catarina},
  type = {Tese de Doutorado}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
