# Detalhamento da Estrutura da Tese: ALF-MoE

Este documento consolida a estrutura final da tese de graduação, alinhada rigorosamente à base de código em `src/`, aos dados consolidados nas análises exploratórias (EDAs) e à fundamentação bibliográfica presente em `UndergraduateThesis/bibliography/pdf_txt/bibliografia/README.md`.

---

## Estrutura Definitiva da Tese

- **1. INTRODUÇÃO**
  - 1.1 Contextualização e Motivação
  - 1.2 Definição do Problema
  - 1.3 Objetivos
    - 1.3.1 Objetivo Geral
    - 1.3.2 Objetivos Específicos
  - 1.4 Principais Contribuições
  - 1.5 Organização do Trabalho
- **2. FUNDAMENTAÇÃO TEÓRICA E TRABALHOS CORRELATOS**
  - 2.1 Ataques Cibernéticos e Sistemas de Detecção de Intrusão (NIDS)
    - 2.1.1 Taxonomia de Ataques de Rede
    - 2.1.2 Métodos de Identificação e Mitigação
  - 2.2 Aprendizado Profundo para Segurança de Redes
    - 2.2.1 Redes Convolucionais e Recorrentes (CNN, LSTM, GRU)
    - 2.2.2 Redes Autoencoders (CAE) e DNNs
    - 2.2.3 Mixture of Experts (MoE) e Mecanismos de Atenção
  - 2.3 Trabalhos Correlatos
    - 2.3.1 NIDS Baseados em Aprendizado Profundo
    - 2.3.2 Abordagens Ensemble e MoE em Cibersegurança
    - 2.3.3 Síntese Comparativa (Quadro 1 revisado)
- **3. MATERIAIS E METODOLOGIA**
  - 3.1 Datasets Utilizados
    - 3.1.1 CSE-CIC-IDS2018 Canônico e Corrigido (Liu et al., 2022)
    - 3.1.2 CIC-BCCC-NRC TabularIoTAttack-2024 (Consolidação de 9 datasets IoT)
    - 3.1.3 CIC-UNSW-NB15 (Subamostragem representativa e preservação de ataques)
  - 3.2 Pipeline de Pré-processamento e Engenharia de Features
    - 3.2.1 Espaço Canônico de 73 Features e Domínios Especializados
    - 3.2.2 Tratamento de Desbalanceamento de Classes (Focal Loss com $\alpha_t$ e $\gamma=2.0$)
  - 3.3 Arquitetura Proposta: ALF-MoE
    - 3.3.1 Visão Geral do Sistema e Fluxo de Dados
    - 3.3.2 Modelos Especialistas (DNN, CNN, GRU, CAE, LSTM)
    - 3.3.3 Gating Network com Refinamento Afim e Compressão $\tanh$
    - 3.3.4 Mecanismo Attention-based Learnable Fusion (ALF) com Cabeça Densa Profunda
  - 3.4 Protocolo Experimental de Treinamento e Avaliação
    - 3.4.1 Funções de Perda Multi-Tarefa e Otimização Adam
    - 3.4.2 Métricas de Desempenho e Eficiência Computacional
- **4. PIPELINE DE EXTRAÇÃO E AMBIENTE DE INFERÊNCIA**
  - 4.1 Captura e Processamento de Tráfego em Tempo Real
    - 4.1.1 Extração com Motor NFStream (C/Cython)
    - 4.1.2 Mapeamento e Alinhamento de Features (NFStream $\to$ CICFlowMeter)
  - 4.2 Setup de Inferência Operacional e Contenção Ativa
    - 4.2.1 Arquitetura do Ambiente de Execução e Contenção via Nftables
    - 4.2.2 Síntese Operacional do Pipeline de Inferência e Contenção Ativa *(Substituiu testes de estresse não realizados)*
- **5. RESULTADOS E DISCUSSÃO**
  - 5.1 Desempenho nos Datasets de Benchmark (Resultados Offline)
    - 5.1.1 Análise por Classe e Desempenho Global (com Justificativas Técnicas de Confusão)
    - 5.1.2 Análise Comparativa dos Especialistas e do Bloco ALF *(Renomeado de Estudo de Ablação)*
  - 5.2 Avaliação da Extração e Inferência em Tráfego Operacional/PCAPs
    - 5.2.1 Impacto do Mapeamento NFStream $\to$ CICFlowMeter
    - 5.2.2 Throughput, Latência e Consumo Computacional (Offline vs. Streaming)
    - 5.2.3 Avaliação Operacional em Tráfego Benigno e Taxa de Falsos Positivos *(Integrado a partir da antiga Seção 5.3)*
- **6. CONCLUSÃO**
  - 6.1 Síntese do Trabalho
  - 6.2 Limitações Identificadas (Calibração Operacional e Atraso Estrutural de Fluxo)
  - 6.3 Trabalhos Futuros (Telemetria em Kernel via eBPF/XDP e Filtragem de Pacotes)

> [!NOTE]
> **Seções Removidas do Escopo:**
> - As seções antigas **4.2.2** e **5.3** (Campanhas com humanos, PTES, emulação Caldera, ataques adversariais dirigidos por LLMs/Nemotron 3.5 e validação de compliance alucinada) foram integralmente suprimidas da tese e das notas, por divergirem da implementação real do projeto. A análise de falsos positivos em tráfego estritamente benigno foi preservada e incorporada na Seção 5.2.3.

---

## Status Detalhado das Correções e Resoluções Técnicas

### 1. Página 14 - §3º (Correção Ortográfica)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/01_introducao.tex`).
- **Ação:** Revisão gramatical e adequação da concordância de termos técnicos e pontuação acadêmica no terceiro parágrafo da introdução.

---

### 2. Páginas 16 e 17 (Formulação do CAE, Gating Network e ALF)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/01_introducao.tex` e `03_metodologia.tex`).
- **Resolução Técnica:**
  1. **Especialista Autoencoder Convolucional (CAE):**
     - Embasado diretamente no artigo de Borgioli et al. (2024) (`@article{borgioli2024cae}`).
     - Aplica janelamento temporal de Hann e Transformada Rápida de Fourier Real (RFFT) sobre as 73 features de entrada ($N=73$), gerando $M = \lfloor 73/2 \rfloor + 1 = 37$ coeficientes espectrais complexos. A magnitude espectral $S[k] = |X[k]|$ alimenta um codificador Convolucional 1D com 3 camadas (`Conv1D(16, 3)`, `Conv1D(32, 3)`, `Conv1D(64, 3)`), comprimido para um *bottleneck* latente de dimensão 16. O decodificador espelhado (`Conv1DTranspose`) reconstrói o espectro de magnitude, otimizado via erro quadrático médio (MSE) com peso $\lambda_{\mathrm{rec}}=1.0$.
  2. **Gating Network:**
     - Alinhada à implementação de `src/models/moe_model.py` (`AttentionRefinementLayer`).
     - A rede recebe as ponderações atencionais $\boldsymbol{\alpha}$, calcula a projeção afim $\mathbf{z}_{\mathrm{refined}} = \mathbf{W}_g \ln(\boldsymbol{\alpha} + \epsilon) + \mathbf{b}_g$, aplica compressão simétrica via tangente hiperbólica $\mathbf{g} = \tanh(\mathbf{z}_{\mathrm{refined}})$ (evitando a extinção prematura de especialistas com valores nulos) e distribui os pesos normalizados por meio de Softmax com temperatura $\tau=1.0$:
       $$a_k = \frac{\exp(g_k / \tau)}{\sum_{j=1}^K \exp(g_j / \tau)}$$
  3. **Módulo ALF (Attention-based Learnable Fusion):**
     - Alinhado estritamente à classe `ALFFusionModule` em `src/models/moe_model.py`.
     - Elimina formulações teóricas de empilhamento de tensores 3D ou bypass residual que não existiam no código. Realiza a combinação linear ponderada dos logits preditos pelos $K=5$ especialistas:
       $$\mathbf{z} = \sum_{k=1}^K a_k \hat{\mathbf{y}}^{(k)}$$
     - O vetor resultante $\mathbf{z}$ é alimentado em um cabeçote de classificação profundo composto por:
       `Dense(128) -> BatchNormalization -> LeakyReLU(0.2) -> Dropout(0.1) -> Dense(64) -> BatchNormalization -> LeakyReLU(0.2) -> Dense(C) -> Softmax`.

---

### 3. Página 18 (Nomenclatura de Datasets, Bibliografia e Hipótese Científica)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/01_introducao.tex`).
- **Resolução Técnica:**
  1. **Nomenclatura Padronizada:** Adoção estrita de **"CIC-UNSW-NB15"** em toda a extensão do trabalho para referenciar a versão processada do benchmark australiano.
  2. **Remoção de CIC-BCCC-NRC-2024 de Exemplos Benignos:** O dataset CIC-BCCC-NRC-2024 possui ~89% de fluxos maliciosos e apenas ~11% benignos, não podendo ser citado como exemplo de desbalanceamento pró-benigno (85-99%). A menção foi substituída por CSE-CIC-IDS2018 e CIC-UNSW-NB15, conforme validado nos EDAs [[EDA_CIC_BCCC_NRC_2024]] e [[EDA_CIC_UNSW_NB15]].
  3. **Embasamento Bibliográfico de Decomposição Espacial e Temporal:**
     - Adicionadas as referências SOTA da pasta de bibliografia:
       - **Wang, Houng e Lin (2023)** (`wang2023deep`, *Sensors*, DOI: 10.3390/s23042171): comprova que o mapeamento convolucional sobre atributos estatísticos de tráfego captura correlações morfológicas locais entre campos do fluxo.
       - **Cao et al. (2022)** (`cao2022applsci`, *Applied Sciences*, DOI: 10.3390/app12094184): demonstra quantitativamente que redes recorrentes (GRU/LSTM) capturam dinâmicas de transição temporal e tempos de inter-chegada (IAT) com 28% de aceleração computacional frente a modelos recorrentes monolíticos profundos.
       - **TimeMatters (2025)** (`timematters2025`): fundamenta a relevância de atributos inter-chegada e dinâmica de janelas TCP.
       - **Standard et al. (2021)** (`standard2021`): fundamenta o particionamento de tráfego tabular para NIDS.
  4. **Indagação Científica Central:** Reformulada para refletir com rigor a tese:
     > *"Em que medida uma arquitetura Mixture of Experts com decomposição multimodal de domínios informacionais e fusão atencional ponderada (ALF-MoE) é capaz de mitigar a perda de sensibilidade em ataques de tráfego minoritários e correlacionados, mantendo um perfil de latência e throughput computacionalmente viável para operação em tempo real?"*

---

### 4. Páginas 20 e 21 (Alinhamento de Contribuições com a Implementação Real)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/01_introducao.tex`).
- **Resolução Técnica:**
  - Contribuições ajustadas para o espaço canônico de 73 features ativas particionadas em 5 domínios (`src/config.py`);
  - Incorporação da análise de latência em batelada (offline) e latência passo-a-passo (streaming via NFStream a 54,23 ms);
  - Eliminação de qualquer alegação sobre mitigação de ataques por LLM ou testes humanos da Seção 1.4.

---

### 5. Página 28 (Fundamentação de NIDS e NIPS)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/02_fundamentacao.tex`).
- **Resolução Técnica:**
  - Adicionadas referências bibliográficas robustas para taxonomia e operação de NIDS/NIPS:
    - `advancedids2024`: abordagens modernas de detecção de intrusão baseadas em fluxo;
    - `fogids2024`: arquiteturas distribuídas e de borda para NIDS;
    - `p4nids2025`: filtragem em alta velocidade e comutação programável.

---

### 6. Página 41 e Tabela 1 / Quadro 1 (Revisão da Síntese Comparativa)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/02_fundamentacao.tex`).
- **Resolução Técnica:**
  - Removidas menções a testes com agentes LLM e validação de compliance;
  - Quadro 1 revisado: a linha "Esta Tese" foi ajustada para destacar:
    - *Abordagem:* MoE Cooperativo Multimodal com Fusão Atencional Aprendível (ALF) e 5 especialistas;
    - *Tipo de Detecção:* Multiclasse com tratamento de classes minoritárias via Focal Loss ($\gamma=2.0$);
    - *Validação Operacional:* Avaliação offline em 4 benchmarks consolidados e inferência em tempo real via NFStream acoplado a regras de contenção dinâmica no subsistema nftables do kernel Linux.

---

### 7. Página 45 (Timeout Ativo $\tau_{\mathrm{active}}=240\,\text{s}$)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/03_metodologia.tex` e `04_pipeline_inferencia.tex`).
- **Resolução Técnica:**
  - Explicitado textualmente que $\tau_{\mathrm{active}}=240\,\text{s}$ constitui uma escolha empírica de projeto do pipeline para amortizar o overhead de exportação de fluxos contínuos e garantir estabilidade estatística em conexões persistentes, e não um padrão fechado da indústria.

---

### 8. Página 46 e Quadro 1 do Capítulo 3 (Revisão de Datasets e Metadados dos EDAs)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/03_metodologia.tex`).
- **Resolução Técnica e Métricas Consolidadas:**
  1. **CSE-CIC-IDS2018 Canônico:**
     - 80 features brutas $\to$ 76 colunas candidatas (remoção de 4 identificadores) $\to$ 73 features ativas (remoção das 3 flags URG de variância zero).
     - 15 classes originais de ataque e tráfego benigno; 3.712.942 fluxos na amostra balanceada (100% ataques, 10% benigno).
  2. **CSE-CIC-IDS2018 Corrigido (Liu et al., 2022):**
     - Baseado em [[EDA CSE-CIC-IDS2018 Corrigido]] e `liu2022error` (`@inproceedings{liu2022error}`).
     - População bruta de 63.195.145 linhas e 91 colunas;
     - Remoção de 9 identificadores (`id`, `Flow ID`, `Src IP`, `Src Port`, `Dst IP`, `Dst Port`, `Protocol`, `Timestamp`, `Attempted Category`);
     - 81 métricas mantidas $\to$ 76 sem colineares $\to$ 73 features ativas no espaço canônico;
     - 15 classes efetivas consolidadas após re-rotulamento de categorias *Attempted* para Benign (com a reclassificação de 100% de `FTP-BruteForce` para Benign, devido à rejeição das portas na captura real com pacotes `[RST, ACK]`).
  3. **CIC-BCCC-NRC TabularIoTAttack-2024:**
     - Baseado em [[EDA_CIC_BCCC_NRC_2024]] e documentação oficial da UNB/CIC (produto de 9 datasets IoT consolidados).
     - População bruta de 22.860.449 fluxos e 85 atributos;
     - Amostra de 15% (3.264.221 fluxos) preservando 100% das 14 classes raras e alocação Hare-Niemeyer nas demais;
     - 71 features mantidas na amostra CSV $\to$ 73 features no espaço canônico;
     - 49 classes L0 agrupadas em 9 macro-classes L2 operacionais.
  4. **CIC-UNSW-NB15:**
     - Baseado em [[EDA_CIC_UNSW_NB15]].
     - População de 3.540.241 fluxos e 84 colunas;
     - Amostra representativa com 139.583 fluxos (50.000 benignos selecionados por cobertura e 89.583 ataques 100% retidos);
     - 73 features canônicas ativas; 10 classes (Benign + 9 famílias de intrusão).

---

### 9. Página 54 - Seção 3.3.2 (Revisão do Especialista CAE)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/03_metodologia.tex`).
- **Resolução Técnica:**
  - Descrição técnica detalhada da janela Hann, RFFT e mapeamento de 73 features para 37 coeficientes espectrais;
  - Convoluções unidimensionais com ativações LeakyReLU e perda de reconstrução MSE ($\lambda_{\mathrm{rec}}=1.0$).

---

### 10. Página 56 - Seção 3.4.1 (Hiperparâmetros de Treinamento)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/03_metodologia.tex`).
- **Resolução Técnica:** Alinhado estritamente às constantes de `src/config.py`:
  - **Otimizador:** Adam ($\eta=10^{-3}$, $\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-7}$);
  - **Tamanho de Lote:** 128 instâncias;
  - **Número Máximo de Épocas:** 10 épocas;
  - **Escalonador:** `ReduceLROnPlateau` (fator 0.5, paciência de 2 épocas, $\eta_{\min}=10^{-5}$);
  - **Parada Precoce:** `EarlyStopping` (paciência de 4 épocas monitorando `val_ALF_F1-Score`);
  - **Função de Perda:** Focal Loss ($\gamma=2.0$, pesos $\alpha_t = \sqrt{1 / f_c}$ normalizados);
  - **Perda Multi-Tarefa:** $\mathcal{L}_{\mathrm{total}} = 1.0 \cdot \mathcal{L}_{\mathrm{ALF}} + 0.2 \sum_{k=1}^K \mathcal{L}_k + 1.0 \cdot \mathcal{L}_{\mathrm{rec}}$.

---

### 11. Página 57 - Seção 3.4.2.2 (Métricas de Eficiência Computacional)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/03_metodologia.tex`).
- **Resolução Técnica:**
  - Formalizadas as métricas de tempo de pré-processamento de tensores, latência média por fluxo em batelada, latência em modo streaming passo-a-passo e uso de VRAM/RAM do pool de inferência.

---

### 12. Seção 4.1 (Revisão Integral da Extração em Tempo Real)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/04_pipeline_inferencia.tex`).
- **Resolução Técnica:**
  - Detalhamento do motor C/Cython do NFStream operando sob `statistical_analysis=True`;
  - Princípio da Responsabilidade Única (SRP) no módulo `FeatureExtractor`;
  - Solução arquitetural para evitar travamento por *CUDA fork* em processos assíncronos (`spawn` e pooling centralizado de inferência em GPU);
  - Conversão explícita de unidades temporais de milissegundos do NFStream para microssegundos do padrão CICFlowMeter ($\times 1000$);
  - Descarte preventivo das 3 flags URG invariantes.

---

### 13. Seção 4.2 (Ambiente Operacional e Contenção Ativa)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/04_pipeline_inferencia.tex`).
- **Resolução Técnica:**
  - Preservadas as especificações de hardware (Kali Linux 7.1.5, Intel Core i7-10750H, 16 GB DDR4, NVIDIA GeForce RTX 2060 6 GB GDDR6);
  - Detalhado o módulo `ActiveDefenseAgent`: aplicação de regras dinâmicas no subsistema `nftables` via conjunto de expiração (`timeout 300s`), resolução de endereço IP ofensor via `select_target` e auditoria de contenção via `InferenceAuditor`;
  - Substituição da Seção 4.2.2 pela *Síntese Operacional do Pipeline de Inferência e Contenção Ativa*, removendo totalmente testes humanos e agentes LLM.

---

### 14. Seção 5.1.1 (Justificativas Técnicas de Confusões de Classes)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/05_resultados.tex`).
- **Resolução Técnica Fundamentada:**
  1. **CSE-CIC-IDS2018 Canônico (Infiltration vs. WebAttack):**
     - Em campanhas de infiltração, o invasor inicialmente explora vulnerabilidades em servidores web (SQLi, buffer overflow) para em seguida pivotar na rede interna. Sem inspeção de carga útil (DPI) na camada 7, a assinatura estatística de fluxo L4 (tamanho de pacotes HTTP/HTTPS e taxas de transmissão) é estatisticamente idêntica entre o vetor de entrada e os WebAttacks típicos.
  2. **CSE-CIC-IDS2018 Corrigido (Benign vs. Infiltration - Dropbox Download):**
     - O tráfego do ataque consiste no download de binário malicioso através de uma conexão HTTPS legítima com os servidores do serviço Dropbox. O handshake TLS, tamanho de buffer e tempos de inter-chegada reproduzem com exatidão o tráfego corporativo benigno, sendo impossível de desambiguar sem quebra de criptografia SSL/TLS.
  3. **CIC-BCCC-NRC TabularIoTAttack-2024 (MITM vs. Botnet):**
     - Em ambientes de redes IoT, ataques Man-In-The-Middle (via ARP poisoning e injeção periódica) e canais de comando e controle (C&C) de Botnets manifestam assinaturas idênticas: baixa volumetria de pacotes, rajadas esparsas com payloads reduzidos e intervalos regulares de keep-alive para manutenção de sessão.
  4. **CIC-UNSW-NB15 (Teto de Bayes decorrente de Conflitos Sintéticos):**
     - Conforme documentado no relatório [[EDA_CIC_UNSW_NB15]], foram identificados **558 registros conflitantes** na amostra (e 1.123 no dataset completo) que compartilham vetores de atributos estatísticos 100% idênticos, mas com rótulos opostos (`Benign` versus `Exploits`/`Reconnaissance`), gerados pelo simulador comercial IXIA PerfectStorm. Isso impõe um limite bayesiano teórico (teto de Bayes) intrínseco aos dados, impedindo convergência assintótica a 100% de precisão por qualquer classificador puramente tabular.

---

### 15. Seção 5.1.2 (Análise Comparativa dos Especialistas e do Bloco ALF)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/05_resultados.tex`).
- **Resolução Técnica:**
  - Seção formalmente renomeada de "Estudo de ablação" para **"Análise Comparativa dos Especialistas e do Bloco ALF"**;
  - Texto focado na dinâmica de atribuição de pesos pelo Gating Network e como o módulo ALF aproveita a complementaridade dos 5 especialistas (CNN para correlações espaciais, GRU/LSTM para dependências temporais, DNN para métricas agregadas e CAE para detecção espectral de anomalias).

---

### 16. Seção 5.2.2 e 5.2.3 (Throughput, Latência e Falsos Positivos Operacionais)
- **Status:** **Resolvido** (em `UndergraduateThesis/chapters/05_resultados.tex`).
- **Resolução Técnica:**
  - Discriminado o throughput de inferência em GPU (~18.450 fluxos/segundo em lote);
  - Latência de inferência passo-a-passo (streaming) consolidada em **$54,23\,\text{ms}$** por fluxo (composta por pré-processamento tabular, conversão em tensores nos 5 formatos especializados e propagação direta pelo modelo ALF-MoE);
  - Explicado o gargalo estrutural de agregação de fluxo imposto pelo temporizador de inatividade do NFStream ($\tau_{\mathrm{idle}}=120\,\text{s}$), que só exporta o fluxo após seu encerramento na rede;
  - Incorporada a análise da antiga Seção 5.3 como **Subseção 5.2.3**: avaliação sob 24.000 fluxos benignos contínuos de longa duração, registrando **0% de falsos positivos (FPR = 0,00%)** graças ao limiar de decisão $\tau=0.85$ e à lista de permissões (*whitelist*) de protocolos de descoberta local (SSDP, mDNS, Spotify Connect).

---

## Relação de Arquivos e Referências Cruzadas do Repositório

| Arquivo / Documento | Papel no Projeto | Localização |
| :--- | :--- | :--- |
| `main.pdf` | Documento compilado da Tese (94 páginas) | `UndergraduateThesis/main.pdf` |
| `references.bib` | Base bibliográfica ABNT com 56 entradas | `UndergraduateThesis/references.bib` |
| `src/config.py` | Definição dos 73 atributos, 5 domínios e hiperparâmetros | `src/config.py` |
| `src/models/moe_model.py` | Implementação do CAE, Gating e ALF | `src/models/moe_model.py` |
| `src/inference/stream_capture.py` | Pipeline de inferência streaming com NFStream | `src/inference/stream_capture.py` |
| `src/inference/active_defense.py` | Agente de contenção dinâmica nftables | `src/inference/active_defense.py` |
| [[Processamento dos Datasets]] | Metodologia de amostragem dos datasets | `obsidian/Processamento dos Datasets.md` |
| [[EDA CSE-CIC-IDS2018 Corrigido]] | Auditoria estatística do dataset corrigido (63M fluxos) | `obsidian/EDA CSE-CIC-IDS2018 Corrigido.md` |
| [[EDA_CIC_BCCC_NRC_2024]] | Auditoria da amostra de 15% e anomalias de amostragem | `obsidian/EDA_CIC_BCCC_NRC_2024.md` |
| [[EDA_CIC_UNSW_NB15]] | Auditoria de teto de Bayes, duplicatas e sub-redes | `obsidian/EDA_CIC_UNSW_NB15.md` |
| [[Features por Expert]] | Mapeamento detalhado dos atributos para os 5 especialistas | `obsidian/Features por Expert.md` |