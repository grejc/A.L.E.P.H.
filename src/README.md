# ALF-MoE: Attention-based Learnable Fusion of Experts for Network Intrusion Detection

O **ALF-MoE** é uma arquitetura de aprendizado profundo de ponta para Sistemas de Detecção e Prevenção de Intrusão em Redes (NIDS/NIPS). O sistema divide o tráfego tabular canônico (padrão CICFlowMeter de 76 features) em subespaços de domínio especializados, processando-os através de cinco especialistas neurais heterogêneos coordenados por uma Rede de Roteamento Dinâmico (Gating Network) com Refinamento Atencional Calibrado e Módulo de Fusão Ponderada (ALF).

---

## 🏛️ Arquitetura do Sistema

```
                            Entrada Tabular Única (D = 76 Features)
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────┐
        │              │               │               │              │
  Slice x_g (29) Slice x_s (20)  Slice x_v (32)  Slice x_f (27) Slice x_t (18)  Vetor Global (76)
        │              │               │               │              │               │
     ┌──▼──┐        ┌──▼──┐         ┌──▼──┐         ┌──▼──┐        ┌──▼──┐         ┌──▼──┐
     │ DNN │        │ CNN │         │ GRU │         │ CAE │        │LSTM │         │ GN  │
     │ 2D  │        │ 2D  │         │ IAT │         │Hann+│        │State│         │Alpha│
     │     │        │(4x5)│         │(8x4)│         │RFFT │        │(6x3)│         │Score│
     └──┬──┘        └──┬──┘         └──┬──┘         └──┬──┘        └──┬──┘         └──┬──┘
        │ y^(1)        │ y^(2)         │ y^(3)         │ y^(4)        │ y^(5)         │
        └──────────────┴───────────────┼───────────────┴──────────────┘               ▼
                                       │                                   Attention Refinement
                                       │                                   a_k = softmax(W·log α)
                                       │                                              │ a_1..a_5
                                       ▼                                              │
                    ┌─────────────────────────────────────────────────────────────────▼┐
                    │            Fusão por Soma Ponderada Estrita (ALF)                │
                    │                  Z = sum_{k=1}^5 a_k · y^(k)                     │
                    └─────────────────────────────────┬────────────────────────────────┘
                                                      │ Vetor Fundido Z
                                               ┌──────▼──────┐
                                               │ Dense + BN  │
                                               │  LeakyReLU  │
                                               │ Dense Logits│
                                               └──────┬──────┘
                                                      ▼
                                            Predição Final 'ALF'
```

### 1. Especialistas Neurais Heterogêneos
1. **DNN (General Statistical Domain - 29 features)**:
   Mapeia distribuições estatísticas globais do fluxo de rede. Capacidade balanceada (256 $\rightarrow$ 128), Batch Normalization, LeakyReLU e Dropout moderado (0.1) para prevenir o colapso de classes raras.
2. **CNN 2D (Spatial Geometry Domain - 20 features)**:
   Reconhece padrões espaciais e correlações de geometria de pacotes. Reshape para matriz $4 \times 5$, convoluções 2D, Batch Normalization e projeção densa.
3. **GRU (Short-term Temporal Domain / IATs - 32 features)**:
   Processa intervalos de chegada (IATs) e taxas de transmissão como série temporal de 8 passos ($T_v = 8, d_v = 4$) com camadas Bidirecionais.
4. **CAE (Frequency Domain Autoencoder - 27 features)**:
   Aplica janelamento periódica de Hann e magnitude espectral via RFFT ($x_f = |\text{RFFT}(x \cdot w)|$). Codifica com Conv1D, decodifica com Conv1DTranspose e calcula a perda de reconstrução MSE $\mathcal{L}_{\text{rec}}$.
5. **LSTM (Long-term Temporal State Domain - 18 features)**:
   Analisa a dinâmica temporal de longo prazo do ciclo de vida da conexão em 6 etapas cronológicas ($T_t = 6, d_t = 3$).

### 2. Gating Network e Refinamento Atencional
- Avalia o vetor tabular completo (76 features) para computar a distribuição adaptativa $\alpha$.
- A camada corrigida `AttentionRefinementLayer` implementa a calibração atencional:
  $$a = \text{softmax}\left(\frac{W_g \cdot \log(\alpha + \epsilon) + b_g}{\tau}\right)$$
- **Correção Técnica Crucial**: Elimina a saturação rígida de `tanh` (que travava a atenção em $[0.056, 0.41]$), adotando escalonamento com temperatura aprendível $\tau$, permitindo que a atenção convirja com nitidez ($> 0.90$) para o especialista mais apto.

### 3. Módulo ALF (Attention-based Learnable Fusion)
- Agrega as predições probabilísticas estritamente via soma ponderada:
  $$Z = \sum_{k=1}^5 a_k \cdot y^{(k)}$$
- **Correção Técnica Crucial**: Não possui skip-connection residual que concatena os especialistas diretamente na saída final. Todo o fluxo de gradiente passa por $Z$, forçando o aprendizado cooperativo e especializado.
- **Compilação Multi-Task Balanceada**:
  $$\mathcal{L}_{\text{total}} = 1.0 \cdot \mathcal{L}_{\text{ALF}} + 0.2 \sum_{k=1}^5 \mathcal{L}_{\text{expert}}^{(k)}$$
  com `FocalLoss(gamma=2.0, alpha=class_weights)` sem dupla ponderação.

---

## 📁 Estrutura de Arquivos

```
ALF-MoE/
├── config.py                 # Configurações globais centralizadas e hiperparâmetros ótimos
├── domain_features.py        # Mapeamento canônico das 76 features e subespaços (100% idêntico)
├── preprocessing.py          # Preprocessor robusto (RobustScaler, log1p em skew>3, split sem leakage)
├── neural/
│   ├── __init__.py           # Exportação limpa das camadas e modelos
│   ├── extra_layers.py       # HannFFTLayer, CAELoss, WeightedSumFusion, FocalLoss, AttentionRefinementLayer
│   ├── dnn.py                # Especialista DNN robusto (256->128, BN, LeakyReLU, Dropout 0.1)
│   ├── cnn.py                # Especialista CNN 2D espacial (4x5)
│   ├── gru.py                # Especialista GRU temporal curto (8x4)
│   ├── cae.py                # Especialista Convolutional Autoencoder (Hann + RFFT + Conv1D + MSE)
│   ├── lstm.py               # Especialista LSTM temporal longo (6x3)
│   ├── gating.py             # Gating Network com refinamento atencional
│   └── model.py              # Classe ALFMoEModel com entrada tabular única e fusão estrita Z
├── reports.py                # Geração de curvas 2x2, heatmaps (.csv e .png) e relatórios estruturados
├── train.py                  # Script executável direto para treinamento completo
├── evaluate.py               # Script executável direto para avaliação no conjunto de teste
├── inference.py              # Pipeline de inferência com auditoria SIEM JSONL e defesa ativa nftables
├── plugins/
│   ├── __init__.py
│   └── extractor.py          # Plugin NFStream para captura em tempo real das 76 features
└── README.md                 # Documentação completa e guia de uso
```

---

## 🚀 Como Executar

Utilize o ambiente virtual Python configurado (`~/.venv`):

### 1. Treinamento Completo
Para treinar o modelo no dataset CSE-CIC-IDS2018 com todos os hiperparâmetros ótimos pré-definidos:
```bash
~/.venv/bin/python train.py
```
Opções adicionais:
```bash
~/.venv/bin/python train.py --epochs 10 --batch-size 128 --lr 0.001 --threat-level 2
```

Artefatos gerados automaticamente em `artifacts/CSE-CIC-IDS2018/<timestamp>/`:
- `model/alf_moe.weights.h5` e `model/alf_moe.keras`: Pesos treinados
- `reports/training_curves.png`: Curvas 2x2 (Loss, F1, Accuracy, Precision/Recall)
- `reports/confusion_matrix_normalized.png` e `.csv`: Matriz de confusão normalizada
- `reports/gating_attention_heatmap.png` e `.csv`: Distribuição de atenção da Gating Network
- `reports/expert_comparison_heatmap.png` e `.csv`: F1-Score dos especialistas vs ALF-MoE
- `reports/alf_moe_metrics_heatmap.png` e `.csv`: Métricas de Precisão, Recall e F1 do ALF
- `reports/training_report.json` e `.txt`: Relatório completo com tempo e vazão de treino
- `reports/test_report.json` e `.txt`: Relatório completo de teste com latência em ms/fluxo

### 2. Avaliação de Desempenho
Para avaliar o modelo treinado mais recente (ou pasta específica):
```bash
~/.venv/bin/python evaluate.py
```
Ou especificando o diretório de artefatos:
```bash
~/.venv/bin/python evaluate.py --artifacts-dir artifacts/CSE-CIC-IDS2018/2026-09-25_02:00:00
```

### 3. Inferência de Produção e Defesa Ativa
Para executar a demonstração sintética do pipeline, auditoria SIEM e agente de mitigação:
```bash
~/.venv/bin/python inference.py --demo
```
Para escuta contínua de pacotes na interface de rede com classificação em tempo real e bloqueio automático de invasores:
```bash
sudo ~/.venv/bin/python inference.py --interface eth0
```
Para inferência em lote a partir de arquivo CSV:
```bash
~/.venv/bin/python inference.py --csv /caminho/para/fluxos.csv
```

---

## 🛡️ Defesa Ativa e Auditoria SIEM

- **Proteção Anti-Auto-Bloqueio**: O agente descobre dinamicamente todos os IPs atribuídos às interfaces do host, loopback (`127.0.0.1`, `::1`) e rota de gateway padrão. Conexões originadas no próprio host que contactam destinos maliciosos bloqueiam estritamente o IP externo remoto.
- **Firewall Kernel Linux**: Cria conjunto temporizado no `nftables` (`flags timeout; timeout 300s;`), descartando pacotes do agressor por 5 minutos sem degradação de CPU.
- **Notificação TCP Ativa**: Servidor raw socket escuta requisições de portas hostis e responde com mensagem de advertência (`"I SEE YOU!"`).
- **Auditoria Forense JSONL**: Cada fluxo processado gera um evento estruturado em `logs/audit_inference_<timestamp>.jsonl` contendo 5-tuple, predição consolidada, confiança, distribuição de pesos da Gating Network e ação de bloqueio adotada.
