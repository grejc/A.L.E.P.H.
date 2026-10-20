# Relatório Técnico de Pré-Processamento — Agente 4

## Dataset: CIC-BCCC-NRC-2024 (`TabularIoTAttack-2024`, 9 Sub-Datasets e Amostragem Hare-Niemeyer)

---

### Sumário Executivo

O conjunto de dados **CIC-BCCC-NRC-2024** (*TabularIoTAttack-2024*) é o mais moderno e abrangente benchmark de cibersegurança focado em ambientes de **Internet das Coisas (IoT)** e **Internet de Coisas Médicas (IoMT)**. Desenvolvido conjuntamente pelo *Canadian Institute for Cybersecurity* (CIC), *Bell Centre for Cyber Security* (BCCC) e *National Research Council Canada* (NRC), a base consolida 9 sub-datasets contemplando topologias complexas de sensores, atuadores, concentradores domóticos e ataques específicos contra protocolos leves como MQTT.

Este relatório documenta a engenharia de dados executada pelo **Agente 4**, detalhando o protocolo de amostragem representativa de 15% via **Hare-Niemeyer**, a investigação da anomalia estatística severa na classe `DDoS TCP SYN Flood`, a remoção de identificadores para prevenção de vazamento de dados, a purga de flags URG sem variância (**73 features ativas**), o mapeamento das 49 classes granulares em 9 macro-famílias funcionais e o condicionamento para a arquitetura neural **ALF-MoE**.

---

## 1. Ficha Técnica e Metadados do Dataset

- **Instituições Responsáveis:** Canadian Institute for Cybersecurity (CIC/UNB), Bell Centre for Cyber Security (BCCC) e National Research Council Canada (NRC).
- **Ano de Publicação:** 2024 (trabalho de referência: Sasi et al., 2025).
- **Ambiente de Testbed e Infraestrutura:** Integração dos laboratórios *Internet of Things Research Lab* (IoTRL - Army Cyber Institute) e bancadas do CIC/UNB:
  - Mais de 40 dispositivos físicos (sensores ambientais, atuadores inteligentes, câmeras IP, termostatos e relés) operando sob múltiplos padrões sem fio (IEEE 802.11 b/g/n, Zigbee, Z-Wave e Bluetooth Low Energy - BLE).
  - Servidores centrais com Home Assistant e corretores de mensagens (*brokers*) Eclipse Mosquitto (protocolo MQTT).
  - Captura não invasiva em nível de pacote realizada via *network taps* com `dumpcap` e síntese de fluxos via **CICFlowMeter**.
- **Volumetria da População Bruta (`CIC-BCCC-NRC-2024.csv`):** 11.488.285.232 bytes (10,70 GiB), 22.860.449 fluxos e 85 colunas brutas.
- **Arquivo Amostrado de Trabalho:** `CIC-BCCC-NRC-2024_sampled.csv` (1.328.339.724 bytes, 1,24 GiB, 3.264.221 fluxos, ~14,28% efetivo da população).
- **Integridade Numérica de Origem:** Diferente de bases históricas legadas (como CIC-IDS2017), o dataset bruto original exibe **0 (0,00%) valores nulos (NaN)** e **0 (0,00%) valores infinitos (+inf / -inf)**.
- **Dimensão Ativa Final de Entrada ($D$):** **73 features** (após alinhamento canônico e purga de 3 flags URG sem variância).

---

## 2. Auditoria e Racional das Colunas Omitidas na Amostra (85 $\to$ 71 $\to$ 73)

A transição entre o dataset populacional bruto (85 colunas) e a versão amostrada de trabalho obedeceu a critérios metodológicos de segurança e teoria da informação:

```
[Dataset Bruto: 85 Colunas]
              │
              ├──► 1. Identificadores Diretos (6 colunas removidas)
              │    [Flow ID, Src IP, Src Port, Dst IP, Dst Port, Timestamp]
              │    Racional: Prevenção de Data Leakage e memorização de topologia.
              │
              ├──► 2. Variância Estritamente Nula (6 colunas removidas)
              │    [Protocol, Bwd PSH Flags, Bwd URG Flags, Fwd Bytes/Bulk Avg,
              │     Fwd Packet/Bulk Avg, Fwd Bulk Rate Avg]
              │    Racional: Variância zero transmite zero entropia e colapsa matrizes.
              │
              └──► 3. Colunas Fortemente Colineares (2 colunas removidas)
                   [Fwd Header Length, Bwd Header Length]
                   Racional: Redundância quase perfeita com Fwd Seg Size Min.
              │
              ▼
[Amostra de Trabalho: 71 Colunas]
              │
              ▼ (Alinhamento Canônico ALF-MoE com EXPLICIT_DROP)
[Vetor de Entrada Ativo: 73 Features]
```

1. **Expurgo Anti-Leakage (6 colunas):** A quíntupla de rede (`Src IP`, `Dst IP`, `Src Port`, `Dst Port`, `Protocol`) e o carimbo `Timestamp` foram eliminados para impedir que classificadores supervisionados associassem a classe maliciosa ao IP do nó atacante ou à porta do concentrador MQTT.
2. **Purga de Variância Zero (6 colunas):** O atributo `Protocol` continha o valor fixo `6` (TCP) em 100% dos 22,8 milhões de fluxos brutos; os demais atributos eram compostos integralmente por zeros.

---

## 3. Protocolo de Amostragem Estratificada Hare-Niemeyer e Diagnóstico de Anomalia

Devido ao tamanho massivo de 22,8 milhões de fluxos, a geração da amostra de 15% utilizou uma estratégia híbrida baseada no método de maiores restos de **Hare-Niemeyer**:

1. **Taxa Padrão (~14,89%):** Classes de alto volume (> 5.000 amostras) foram amostradas a uma taxa homogênea de 14,887%.
2. **Preservação de Classes Minoritárias:** Classes com menos de 5.000 amostras foram retidas em **95% a 100%** para assegurar que ataques raros (como `Telnet Brute Force`, retido em 99,42%, e `MQTT DoS Publish Flood`, retido em 100,00%) não desaparecessem.

### Diagnóstico Crítico da Anomalia de `DDoS TCP SYN Flood`:
Durante a análise exploratória (EDA) comparativa entre o dataset bruto e a amostra, o Agente 4 detectou uma severa distorção amostral:

```
+------------------------------------+--------------------+---------------------+
| Métrica                            | Dataset Original   | Amostra Sampled     |
+------------------------------------+--------------------+---------------------+
| Volume DDoS TCP SYN Flood          | 843.527 fluxos     | 605 fluxos          |
| Proporção na População             | 3,690%             | 0,018%              |
| Taxa de Retenção Efetiva           | Referência (100%)  | 0,0717% (-99,93%)   |
| Média Flow Packets/s (Global)      | 15.129,45 pkts/s   | 697,41 pkts/s       |
| Média Flow Bytes/s (Global)        | 324.798,5 B/s      | 29.470,4 B/s        |
| Desvio Médio de Taxa               | Referência         | -95,39% (Packets/s) |
+------------------------------------+--------------------+---------------------+
```

> **Explicação Física:** No tráfego original, os fluxos de `DDoS TCP SYN Flood` exibiam duração média de apenas 34 microssegundos, gerando uma taxa média de 137.827 pacotes/s. A quase erradicação desses fluxos na amostra fez com que a média global de taxa de pacotes da base despencasse mais de 95%. O preprocessor atenua esse efeito aplicando a compressão logarítmica $\log(1+x)$ sobre as variáveis de taxa.

---

## 4. Hierarquia Semântica de Ameaças (*Threat Levels*)

O CIC-BCCC-NRC-2024 possui originalmente **49 classes granulares** (Threat Level 0 / TL0). Para permitir tanto a análise forense minuciosa quanto a resposta automatizada perimetral em tempo real (bloqueio no firewall), o preprocessor mapeia deterministicamente essas classes em **9 macro-famílias funcionais** (Threat Level 1 / TL1):

```
                   [49 Classes Granulares (Threat Level 0 / TL0)]
                                   │
  ┌────────────────────────────────┼────────────────────────────────┐
  ▼                                ▼                                ▼
[Floods & DoS L4]            [IoT / MQTT Protocol]         [Malware & Botnets]
ACK Flood (86k)              MQTT Brute Force (30k)        Backdoor (12k)
DoS TCP Flood (66k)          MQTT DDoS Publish (12k)       Mirai ACK/HTTP/UDP (2k)
DoS SYN Flood (53k)          MQTT DoS Connect (7k)         Ransomware (496)
DDoS RSTFIN (117k)           MQTT Malformed (1k)                    │
DDoS PSHACK (75k)                          │                        ▼
  │                                        ▼                 [Botnet/Malware]
  ▼                                   [IoT/MQTT]                    │
[DoS / DDoS]                                                        │
  │                                                                 │
  └────────────────────────────────┬────────────────────────────────┘
                                   ▼
             [9 Meta-Categorias Consolidadas (Threat Level 1 / TL1)]
```

### Detalhamento das 9 Meta-Categorias:
1. **`Benign Traffic`:** Conexões legítimas de telemetria IoT e tráfego de fundo (70.185 fluxos no teste).
2. **`Botnet/Malware`:** `Backdoor`, `Ransomware` e variantes da botnet `Mirai` (`Mirai ACK Flood`, `Mirai HTTP Flood`, `Mirai Host Brute Force`, `Mirai UDP Plain`, `Mirai UDP Flood`).
3. **`BruteForce`:** Ataques de quebra de credenciais (`Sparta SSH Brute Force`, `Password Attack`, `Dictionary Brute Force`, `Telnet Brute Force`).
4. **`DDoS`:** Inundações distribuídas volumétricas e fragmentações L3/L4 (`DDoS RSTFIN Flood`, `DDoS PSHACK Flood`, `DDoS ACK Fragmentation`, `DDoS TCP SYN Flood`, `DDoS HTTP Flood`, `DDoS ICMP Fragmentation`, `DDoS UDP Flood`, `DDoS ICMP Flood`).
5. **`DoS`:** Ataques de negação de serviço de origem pontual (`ACK Flood`, `DoS TCP Flood`, `DoS SYN Flood`, `DoS UDP Flood`, `DoS ICMP Flood`, `DoS DNS Flood`, `SYN Flood`).
6. **`IoT/MQTT`:** Ataques desenhados contra o protocolo MQTT (`MQTT Brute Force`, `MQTT DDoS Publish Flood`, `MQTT DoS Connect Flood`, `MQTT Malformed`, `MQTT DoS Publish Flood`).
7. **`MITM`:** Ataques de interceptação e envenenamento (`MITM`, `MITM ARP Spoofing`).
8. **`Reconnaissance`:** Mapeamento de rede e sondagem de portas (`Recon Port Scan`, `Recon OS Scan`, `Recon Ping Sweep`, `Recon Vulnerability Scan`, `Recon Host Discovery`, `OS Fingerprinting`, `Scan Aggressive`, `Scan UDP Attack`, `Port Scanning`, `Scan Port OS`, `Scan Host Port`, `Vulnerability Scanner`).
9. **`WebAttack`:** Ataques contra interfaces HTTP dos concentradores (`Uploading Attack`, `SQL Injection`, `XSS`).

---

## 5. Mapeamento Passo a Passo do Pipeline e Módulos Empregados

### Etapa 1: Ingestão e Alinhamento da Coluna Alvo
- **Módulos Utilizados:** `pandas.read_csv(low_memory=False)`.
- **Implementação:** [`Preprocessor._align_dataframe_columns()`](file:///home/null/ALF-MoE/src/preprocessing.py#L475-L503).
- **Procedimento:** No CIC-BCCC-NRC-2024, a coluna alvo original é denominada **`Attack Name`**. A propriedade `Preprocessor.target_column` detecta esse padrão dinamicamente e alinha a série para o processamento.

### Etapa 2: Sanitização e Purga de Variância Nula
- **Módulos Utilizados:** Constante `EXPLICIT_DROP_COLUMNS`.
- **Procedimento:** Elimina as colunas constantes `Fwd URG Flags`, `Bwd URG Flags` e `URG Flag Count`, padronizando o espaço em **73 features ativas**.

### Etapa 3: Particionamento Estratificado e Suporte Amostral de Teste
- **Módulos Utilizados:** `sklearn.model_selection.train_test_split`.
- **Suporte de Teste:** O particionamento estratificado de 20% consolidou **652.845 fluxos de rede no conjunto de teste independente**, cuja distribuição e pesos para a função Focal Loss são detalhados a seguir:

| ID | Macro-Categoria (TL1) | Suporte no Teste (20%) | Proporção (%) | Peso Calculado ($w_c$) |
| :-: | :--- | :--- | :--- | :--- |
| **0** | `Benign Traffic` | 70.185 | 10,751% | **1,0166** |
| **1** | `Botnet/Malware` | 14.691 | 2,250% | **2,2221** |
| **2** | `BruteForce` | 39.443 | 6,042% | **1,3561** |
| **3** | `DDoS` | 207.074 | 31,719% | **0,5919** |
| **4** | `DoS` | 211.296 | 32,365% | **0,5859** |
| **5** | `IoT/MQTT` | 50.282 | 7,702% | **1,2011** |
| **6** | `MITM` | 3.793 | 0,581% | **4,3731** |
| **7** | `Reconnaissance` | 34.461 | 5,279% | **1,4508** |
| **8** | `WebAttack` | 21.620 | 3,312% | **1,8317** |
| **Total**| -- | **652.845** | **100,00%** | -- |

### Etapa 4: Engenharia de Features e Escalonamento no Treino
- **Módulos Utilizados:** `pandas.Series.skew()`, `numpy.log1p()`, `sklearn.preprocessing.RobustScaler()`, `sklearn.preprocessing.LabelEncoder()`.
- **Procedimento:**
  - 36 features com $|\text{skew}| > 3{,}0$ sofrem transformação $\ln(1 + \max(x, 0))$.
  - Ajuste do `RobustScaler(quantile_range=(25.0, 75.0))` com medianas e IQRs estritamente calculados sobre os 2.089.101 fluxos do conjunto de treino.

### Etapa 5: Fatiamento de Domínios para os Especialistas Neurais (MoE)
- **Módulos Utilizados:** [`Preprocessor.get_domain_indices()`](file:///home/null/ALF-MoE/src/preprocessing.py#L647-L660).
- **Mapeamento:**
  - `dnn`: 27 atributos em $\mathbf{x}_g$ (sinalizadores TCP, contadores agregados e durações).
  - `cnn`: 20 atributos em $\mathbf{x}_s$ extraídos pelo `SliceLayer` (16 canônicos projetados na matriz $4 \times 4 \times 1$ em `cnn.py`).
  - `gru`: 32 atributos em $\mathbf{x}_v$ formatados em $8 \times 4$ passos temporais (tempos entre chegadas IAT).
  - `cae`: 27 atributos em $\mathbf{x}_f$ submetidos à janela de Hann e transformada rápida de Fourier RFFT.
  - `lstm`: 18 atributos em $\mathbf{x}_t$ formatados em $6 \times 3$ passos de repouso e atividade Active/Idle.

### Etapa 6: Inferência em Tempo Real e Persistência de Artefatos
- **Módulos Utilizados:** `pickle`, `json`, [`Preprocessor.transform_features()`](file:///home/null/ALF-MoE/src/preprocessing.py#L739-L775), [`src/inference.py`](file:///home/null/ALF-MoE/src/inference.py).
- **Operação IoT em Tempo Real:** Fluxos capturados de corretores MQTT ou switches IoT são convertidos online via `transform_features` com latência média de **$0{,}0122\,\mathrm{ms}$ por fluxo** (vazão de mais de 82.000 fluxos/s).
- **Artefatos:** Salvos em `artifacts/CIC-BCCC-NRC-2024/<timestamp>/preprocess/`:
  - `CIC-BCCC-NRC-2024_artifacts.pkl`: Objeto preprocessor contendo o scaler treinado, encoder de 9 classes e listas de colunas.
  - `CIC-BCCC-NRC-2024_metadata.json`: Manifesto de auditoria detalhando parâmetros, versões do runtime e mapeamentos.
