---
id: artigo_033
title: Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso
authors:
- Diego Abreu
- Antônio Abelém
year: 2022
bibtex_key: sistema2022
doi: 10.5753/sbrc.2022.222320
venue: Anais do XL Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos
  (SBRC 2022), pp. 322-335
keywords:
- Redes Definidas por Software (SDN)
- Sistemas de Detecção de Intrusão
- Tráfego Malicioso
- Classificação Híbrida
- Machine Learning em Tempo Real
area: Software Defined Networks (SDN) / Real-time NIDS / Hybrid Detection
datasets:
- CIC-IDS-2017
- Injeção de tráfego em rede SDN de bancada Mininet
models:
- Random Forest
- Decision Tree
- Support Vector Machines (SVM)
- OpenFlow Rule Engine
aliases:
- Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso
- sistema2022
- artigo_033
tags:
- bibliografia
- alf-moe
- artigo
---

# Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso

> **Citação ABNT Sugerida:** ABREU, D.; ABELÉM, A.. Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso. In: **Anais do XL Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2022), pp. 322-335**, 2022.
> **Chave BibTeX:** `sistema2022` | **Arquivo TXT:** `Sistema_Híbrido_e_On-line_de_Detecção_e_Classificação_de_Tráfego_Malicioso_20220805.txt` | **DOI:** `10.5753/sbrc.2022.222320`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_033` |
| **Ano** | 2022 |
| **Área de Pesquisa** | Software Defined Networks (SDN) / Real-time NIDS / Hybrid Detection |
| **Veículo de Publicação** | Anais do XL Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2022), pp. 322-335 |
| **Datasets Utilizados** | CIC-IDS-2017, Injeção de tráfego em rede SDN de bancada Mininet |
| **Modelos / Algoritmos** | Random Forest, Decision Tree, Support Vector Machines (SVM), OpenFlow Rule Engine |
| **Palavras-Chave** | Redes Definidas por Software (SDN), Sistemas de Detecção de Intrusão, Tráfego Malicioso, Classificação Híbrida, Machine Learning em Tempo Real |

## 🎯 Problema Abordado
O aumento substancial nas taxas de transmissão em redes corporativas impede a aplicação de modelos de aprendizado de máquina pesados sobre todos os pacotes em trânsito; a arquitetura tradicional desacoplada sofre de gargalos de comunicação entre plano de controle e plano de dados.

## 🔬 Metodologia
Sistema híbrido operando em Redes Definidas por Software (SDN) composto por dois módulos complementares: uma camada de triagem rápida online via regras e limiares estatísticos leves implementada nos switches OpenFlow, e uma camada analítica profunda assíncrona que processa fluxos suspeitos usando algoritmos supervisionados.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O sistema sustentou classificação em tempo real sem degradação na latência de tráfego legítimo, bloqueando ataques de DoS/DDoS em menos de 1.8 segundos com acurácia superior a 98.7% e redução de 84% no tráfego de telemetria enviado ao controlador.

**Contribuições Centrais:**
- Arquitetura híbrida de dois estágios para NIDS em SDN.
- Estratégia de redução de carga sobre o controlador mediante triagem nos switches.
- Validação experimental em emulador Mininet com tráfego realista.

## ⚠️ Limitações Identificadas
Dependência de regras e limiares na camada rápida que podem ser evadidos por ataques lentos de baixa cadência (low-and-slow).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `SDN NIDS`, `Arquitetura Híbrida`, `Classificação On-line`, `OpenFlow`
- **Problemas Focais:** `Sobrecarga do controlador SDN com análise massiva`, `Latência excessiva de reação a ataques`
- **Métodos Empregados:** `Triagem preliminar em switches OpenFlow`, `Classificação ML profunda sob demanda`, `Instalação reativa de regras de bloqueio`
- **Modelos e Arquiteturas:** `Random Forest`, `Decision Tree`, `OpenFlow Matcher`
- **Bases de Dados:** `CIC-IDS-2017`, `Tráfego Mininet`
- **Resultados Chave:** `Bloqueio em 1.8 segundos`, `Redução de 84% na telemetria enviada ao controlador`, `Acurácia de 98.7%`
- **Limitações Reconhecidas:** `Limiares rígidos vulneráveis a evasão furtiva`
- **Evidências Citáveis:** `EVID_033_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_026]] — *NFStream: A flexible network data analysis framework*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
- **Avalia Dataset:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_013]] — *Detecção e prevenção de intrusão em computação de nevoeiro e Internet das Coisas*
  - [[artigo_019]] — *F-NIDS: Sistema de Detecção de Intrusão baseado em Aprendizado Federado*
  - [[artigo_030]] — *P4-NIDS: High-Performance Network Monitoring and Intrusion Detection in P4*
- **Cria Dataset Utilizado Por:**
  - [[artigo_041]] — *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*

## 🎓 Integração com a Tese ALF-MoE

### Conceitos Teóricos Vinculados
- [[Conceitos/NIDS|Network Intrusion Detection System (NIDS)]] — Papel: NIDS híbrido em tempo real em SDN

### Clusters Temáticos
- **Datasets:** [[Rede_Intelectual#Benchmark: CIC-IDS-2017|CIC-IDS-2017]]
- **Arquiteturas:** [[Rede_Intelectual#Arquitetura: Plano de Dados P4 SDN|Plano de Dados P4 SDN]]

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_033_01` — METODOLÓGICA
> [!quote] EVID_033_01 (Relevância: 5/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A arquitetura em dois níveis (triagem rápida preliminar e inferência profunda sob demanda) reduz a sobrecarga de telemetria e assegura mitigação célere.
> **Localização:** Seção 3 (Arquitetura Proposta), Páginas 325-328
>
> *"A abordagem em duas fases realiza a triagem preliminar dos fluxos em velocidade de comutação no plano de dados e direciona apenas instâncias anômalas para os classificadores de aprendizado de máquina, otimizando o consumo computacional."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta as decisões de arquitetura no Capítulo 4 sobre a viabilidade operacional e redução de overhead na inferência do NIDS.

## 📦 Entrada BibTeX
```bibtex
@article{sistema2022,
  title = {Sistema Híbrido e On-line de Detecção e Classificação de Tráfego Malicioso},
  author = {Abreu, Diego and Abelém, Antônio},
  journal = {Anais do XL Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos (SBRC 2022)},
  year = {2022},
  doi = {10.5753/sbrc.2022.222320},
  pages = {322-335},
  publisher = {Sociedade Brasileira de Computação}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
