---
id: Inter-Arrival Time (IAT) e Atributos Temporais
term: Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo
aliases:
- IAT
- Packet Inter-Arrival Time
- Tempo Entre Chegadas
- Temporal Features
- Flow Cadence
- Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo
- Inter-Arrival Time (IAT) e Atributos Temporais
tags:
- conceito
- bibliografia
- alf-moe
---

# Inter-Arrival Time (IAT) e Atributos Temporais de Fluxo

> **Sinônimos e Variantes:** IAT, Packet Inter-Arrival Time, Tempo Entre Chegadas, Temporal Features, Flow Cadence

## 📖 Definição Canônica
Intervalo temporal decorrido entre a chegada de pacotes consecutivos em um fluxo bidirecional de rede, refletindo a cadência operacional de protocolos e estratégias de temporização de ataques.

- **Artigo de Definição Formal:** [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*
- **Evidência Canônica:** `EVID_040_01` (Seção 2 (Temporal Features in Network Traffic), Páginas 66901-66903)
> [!quote] Evidência Canônica (`EVID_040_01`)
> *"Packet Inter-Arrival Time (IAT) quantifies the elapsed duration between consecutive packet arrivals within a bidirectional flow, providing an essential mathematical descriptor of communication cadences and pacing strategies."*
>
> **Afirmação:** Definição do tempo entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) e sua função como atributo temporal fundamental em fluxos de rede.
>
> **Aplicação na Tese:** Citação direta no Capítulo 1 e Capítulo 3 para definir o subvetor temporal de IATs processado pelo especialista GRU no ALF-MoE.

## 📚 Artigos Relacionados na Base
| Artigo | Relevância | Papel no Conceito |
| :--- | :---: | :--- |
| [[artigo_004]] — *ALF-MoE: An Attention-Based Learnable Fusion of Specialized Expert Networks for Accurate Traffic Classification* | 5/5 | Vetor de entrada temporal do especialista GRU no ALF-MoE |
| [[artigo_014]] — *Detecção de Ataques em Redes Intraveiculares CAN com Técnicas de Machine Learning* | 5/5 | IAT como discriminador crítico em redes intraveiculares CAN |
| [[artigo_040]] — *Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection* | 5/5 | Demonstração empírica de que 'Time Matters' em NetFlow |

## 🔍 Evidências Literais Associadas
### `EVID_014_01` — METODOLÓGICA (Fonte: [[artigo_014]])
> [!quote] EVID_014_01
> **Localização:** Capítulo 4 (Metodologia e Resultados), Seção 4.3, Páginas 52-56
> **Afirmação Sustentada:** A frequência de transmissão e o intervalo entre mensagens consecutivas (IAT) são os discriminadores mais sensíveis para detectar anomalias e injeções fraudulentas.
>
> *"A análise dos intervalos entre chegadas de mensagens (Inter-Arrival Time) revela anomalias na cadência de envio característica de injeções de DoS e spoofing, constituindo o atributo de maior poder discriminatório no barramento."*
>
> **Aplicação Tese ALF-MoE:** Reforça a justificativa metodológica para a inclusão de atributos de IAT e o especialista temporal (GRU) no ALF-MoE.

### `EVID_040_01` — DEFINIÇÃO (Fonte: [[artigo_040]])
> [!quote] EVID_040_01
> **Localização:** Seção 2 (Temporal Features in Network Traffic), Páginas 66901-66903
> **Afirmação Sustentada:** Definição do tempo entre chegadas consecutivas de pacotes (Inter-Arrival Time - IAT) e sua função como atributo temporal fundamental em fluxos de rede.
>
> *"Packet Inter-Arrival Time (IAT) quantifies the elapsed duration between consecutive packet arrivals within a bidirectional flow, providing an essential mathematical descriptor of communication cadences and pacing strategies."*
>
> **Aplicação Tese ALF-MoE:** Citação direta no Capítulo 1 e Capítulo 3 para definir o subvetor temporal de IATs processado pelo especialista GRU no ALF-MoE.

### `EVID_040_02` — FUNDAMENTAÇÃO TEÓRICA (Fonte: [[artigo_040]])
> [!quote] EVID_040_02
> **Localização:** Seção 1 (Introduction), Páginas 66899-66901
> **Afirmação Sustentada:** Soluções baseadas em representação puramente estática ou de perspectiva única falham em discriminar ataques cujos perfis distintivos residem na dimensão temporal.
>
> *"Conventional single-view NetFlow models relying strictly on static cumulative byte and packet counters remain blind to evasive threats such as low-and-slow command-and-control channels, where discriminative patterns exist exclusively in inter-packet arrival timings."*
>
> **Aplicação Tese ALF-MoE:** Citação mandatória no Capítulo 1 para fundamentar as limitações de modelos com representação de perspectiva única (single-view representation).

### `EVID_040_03` — EMPÍRICA (Fonte: [[artigo_040]])
> [!quote] EVID_040_03
> **Localização:** Seção 4 (Experimental Results), Páginas 66907-66911
> **Afirmação Sustentada:** A inclusão de atributos temporais de IAT melhora o F1-score em mais de 12% na detecção de botnets e canais de comando e controle em múltiplos datasets.
>
> *"Integrating temporal NetFlow features into machine learning classifiers delivers an average improvement of over 12% in F1-score across evasive attack categories including Botnet and Infiltration on the NF-CIC-IDS2017-v2 dataset."*
>
> **Aplicação Tese ALF-MoE:** Evidência experimental para sustentar a eficácia do especialista sequencial/temporal na tese.

## 🧭 Navegação
- ⬅️ [[Conceitos_Centrais|Compêndio de Conceitos Centrais]]
- 🏠 [[00_Indice_Bibliografico|Índice Geral da Bibliografia]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual]]
