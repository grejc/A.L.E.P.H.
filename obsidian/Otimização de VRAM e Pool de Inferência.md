# Decisões de Arquitetura: Otimização de VRAM e Pool de Inferência Dinâmica (ALF-MoE)

Este documento formaliza as decisões de arquitetura e engenharia de software implementadas no pipeline de inferência em produção do **ALF-MoE** (`src/inference.py`).

---

## 1. Contexto, Sintomas e Motivação

### 1.1 O Gargalo da Inferência Unitária ($N=1$)
Nos testes empíricos de desempenho no hardware de produção (GPU NVIDIA GeForce RTX 4050 Laptop 6GB), a execução do grafo neural do ALF-MoE apresentou o seguinte comportamento:
* **1 item isolado**: ~100 ms de latência total de inferência (throughput de ~10 a 26 fluxos/segundo).
* **128 itens em lote**: ~75 ms de latência total para o lote completo (throughput de ~1.700 a 2.300 fluxos/segundo, ou **~0,42 ms a 0,58 ms por fluxo**).

Essa discrepância decorre do custo fixo de despacho de kernels CUDA na GPU e transferência de memória via barramento PCIe. A malha neural do ALF-MoE integra 5 especialistas heterogêneos (DNN, CNN, GRU, CAE, LSTM) associados à Gating Network e fusão ALF. Processar uma única amostra deixa mais de 98% dos Streaming Multiprocessors (SMs) ociosos enquanto consome o tempo integral de despacho do driver.

### 1.2 O Sintoma Crítico: Crescimento da Latência Ponta a Ponta (`e2e`)
Ao analisar os registros históricos em `logs/audit_inference_*.log`, constatou-se que o tempo decorrido entre a primeira observação do pacote na rede e a decisão de classificação (`latency_until_inference` / `e2e`) acumulava atrasos exponenciais conforme o volume de tráfego aumentava:
* A cada fluxo que expirava, o loop de captura síncrono era pausado por ~50ms a 100ms para inferir $N=1$.
* Quando 10 fluxos expiravam em rajada, o décimo fluxo aguardava ~1 segundo na fila; com 100 fluxos, o atraso atingia 10 segundos, comprometendo a eficácia da Defesa Ativa (NIPS) no firewall.

---

## 2. Decisão Arquitetural 1: Gestão Estrita de Memória de Vídeo (VRAM)

O TensorFlow, por padrão, utiliza uma política de alocação agressiva (*greedy preallocation*), reservando até 90% da VRAM física da GPU (~5,5 GB na RTX 4050 de 6 GB) para alocadores internos, além de alocar estados de momento do otimizador caso o modelo seja carregado de forma descuidada.

### 2.1 Diretrizes Implementadas
1. **Teto Virtual Rígido de VRAM (512 MB)**:
   * Implementado via `tf.config.set_logical_device_configuration(gpu, [tf.config.LogicalDeviceConfiguration(memory_limit=512)])`.
   * Impede categoricamente que o runtime ultrapasse 512 MB de VRAM física, permitindo que a GPU execute simultaneamente outras tarefas e aplicações gráficas do sistema host.
2. **Carregamento Otimizado para Produção (`compile=False`)**:
   * O modelo e pesos são instanciados e carregados sem compilar otimizadores (como o Adam). Isso poupa os tensores de momentum ($m$) e variância ($v$), reduzindo o consumo de memória dos parâmetros em 50%.
   * Para contornar a limitação de reconstrução de subcamadas do Keras 3 (como as camadas `Conv1DTranspose` do Autoencoder CAE), a arquitetura é reconstruída deterministicamente pelo `ALFMoEModel` e preenchida via `load_weights`.
3. **Modo Fallback CPU (0 MB de VRAM)**:
   * Suporte a `device="cpu"` via `tf.config.set_visible_devices([], "GPU")`, garantindo alocação zero de memória gráfica para ambientes sem aceleração por hardware ou containers restritos.
4. **Padrão Singleton de Acesso ao Modelo**:
   * O `ModelInferenceEngine` é mantido como instância única no processo principal via `get_inference_engine()`, eliminando duplicações de grafo e contexto CUDA.

### 2.2 Telemetria de VRAM Medida
* **VRAM em Repouso**: ~23 MB (driver/sistema operacional).
* **VRAM Pico sob Lote Completo (128 itens)**: **~176 MB** (muito abaixo do teto de 512 MB).

---

## 3. Decisão Arquitetural 2: Pool de Inferência Dinâmica (Dynamic Micro-Batching)

Para permitir que a inferência ocorra **na expiração de um pacote ou fluxo** sem bloquear o sniffer de rede, foi desenvolvida a classe `InferenceBatchPool`.

### 3.1 Padrão Produtor-Consumidor Assíncrono

```mermaid
flowchart TD
    subgraph Captura["Captura de Tráfego (NFStream / Extrator)"]
        F1["Fluxo 1 Expira"] -->|submit não-bloqueante| Q["Fila Concorrente (queue.Queue)"]
        F2["Fluxo 2 Expira"] -->|submit não-bloqueante| Q
        FN["Fluxo N Expira"] -->|submit não-bloqueante| Q
    end

    subgraph Pool["InferenceBatchPool (Thread Dedicada)"]
        Q -->|Drena até 128 itens OU timeout de 10ms| Batcher["Coletor de Lote Vetorizado"]
        Batcher -->|Matriz Normalizada (B, 73)| Engine["ModelInferenceEngine (GPU / VRAM < 512MB)"]
        Engine -->|model(batch_x, training=False) ~54ms| Dispatcher["Distribuidor de Predições"]
    end

    subgraph Acoes["Pós-Processamento e Mitigação"]
        Dispatcher -->|Resolve Future / Callback| Res["Resposta do Fluxo"]
        Dispatcher -->|Trilha Forense JSONL| AUD["InferenceAuditor (SIEM)"]
        Dispatcher -->|Se ameaça detectada| NIPS["ActiveDefenseAgent (nftables drop)"]
    end
```

### 3.2 Parâmetros e Regras de Disparo
* **`max_batch_size = 128`**: Limite superior do lote. Se a fila acumular 128 requisições, o lote é despachado imediatamente para a GPU, atingindo a eficiência máxima de ~0,42 ms/item.
* **`max_wait_ms = 10.0 ms`**: Limite temporal máximo de espera. Se o tráfego de rede for reduzido e a fila tiver menos de 128 itens, o coletor aguarda no máximo 10 milissegundos antes de processar os itens disponíveis. Isso impede que fluxos esparsos sofram latência artificial de espera.
* **Desacoplamento do Capturador**: O método `pool.submit()` adiciona a requisição à fila em microssegundos e retorna um `concurrent.futures.Future`. O loop do `NFStreamer` continua escutando a interface de rede sem perder pacotes nos buffers de socket do kernel.

---

## 4. Decisão Arquitetural 3: Vetorização no Pré-processamento

O pré-processamento de features tabulares foi reestruturado no método `ModelInferenceEngine.preprocess()`:
1. **Imputação Rápida com `np.tile`**: A matriz de entrada de dimensões $(N, 73)$ é pré-inicializada replicando em bloco o vetor de medianas canônicas pré-computadas (`default_vector`), substituindo loops lentos de preenchimento coluna por coluna.
2. **Normalização de Chaves em Cache**: As chaves fornecidas são normalizadas para um índice numérico direto via dicionário hash `clean_feature_map`.
3. **Transformação Logarítmica e Escalonamento em Bloco**: As 53 features de alta dispersão recebem `np.log1p(np.maximum(data[:, log1p_indices], 0.0))` de forma vetorizada, e a matriz resultante é escalonada em uma única chamada `RobustScaler.transform(data)`.
4. **Desempenho**: O pré-processamento de 128 itens leva apenas **~6,2 ms** (0,048 ms por item).

---

## 5. Tabela Comparativa: Antes vs. Depois da Refatoração

| Dimensão de Engenharia | Arquitetura Anterior | Arquitetura Refatorada | Impacto Prático |
| :--- | :--- | :--- | :--- |
| **Política de VRAM** | Alocação livre (até ~5,5 GB) | **Teto de 512 MB** via Logical Device | Elimina risco de OOM no SO e na GPU |
| **VRAM em Execução** | > 4.000 MB alocados | **~176 MB de pico** | Economia de >95% de memória gráfica |
| **Modo de Inferência** | Síncrono unitário ($N=1$) | **Micro-Batching Dinâmico** ($N \le 128$) | Fim do bloqueio na captura de rede |
| **Latência por Item** | ~100 ms / item | **~0,42 ms a 0,50 ms / item** | Ganho de velocidade de até 200x |
| **Throughput Máximo** | ~10 a 20 fluxos/s | **> 1.700 fluxos/s** | Suporta rajadas de ataques DDoS |
| **Atraso Ponta a Ponta (`e2e`)**| Acumulava até dezenas de segundos | **Estável em ~64 ms** | Reação de bloqueio em tempo real |
| **Loop do NFStreamer** | Bloqueado a cada expiração | **Não-bloqueante** via `pool.submit` | Zero pacotes descartados por saturação |
| **Fallback CPU** | Não isolado | `device="cpu"` nativo (**0 MB VRAM**) | Portabilidade para servidores sem GPU |

---

## 6. Referência dos Componentes no Código

* **Configuração de Hardware e VRAM**: `configure_hardware` em `src/inference.py`
* **Motor Otimizado**: `ModelInferenceEngine` em `src/inference.py`
* **Pool Dinâmica**: `InferenceBatchPool` em `src/inference.py`
* **Pipeline Integrado**: `InferencePipeline` em `src/inference.py`
* **Captura em Tempo Real com Pool**: `InferencePipeline.stream_capture` em `src/inference.py`
* **Defesa Ativa NIPS (nftables)**: `ActiveDefenseAgent` em `src/inference.py`
* **Trilha Forense JSONL (SIEM)**: `InferenceAuditor` em `src/inference.py`
