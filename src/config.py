"""
Configurações Globais Centralizadas para o ALF-MoE.

Define todos os caminhos padrão, hiperparâmetros ótimos para o dataset
CSE-CIC-IDS2018 (e datasets correlatos da família CIC), dimensões dos
especialistas neurais, parâmetros de treinamento e defesa ativa.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Literal


# =============================================================================
# DIRETÓRIOS E CAMINHOS BASE
# =============================================================================
BASE_DIR: Path = Path("/home/null/ALF-MoE").resolve()
DATASETS_DIR: Path = Path(os.getenv("DATASETS_DIR", "/run/media/null/VM_s/DATASETS")).resolve()

# Dataset canônico padrão
DEFAULT_DATASET: str = "CSECICIDS2018_improved"

# Subdiretórios do projeto
ARTIFACTS_DIR: Path = BASE_DIR / "artifacts"
LOGS_DIR: Path = BASE_DIR / "logs"

# Criação automática dos diretórios essenciais
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# DATASET & PRÉ-PROCESSAMENTO
# =============================================================================
@dataclass
class PreprocessingConfig:
    dataset_name: str = DEFAULT_DATASET
    load_sampled: bool = True
    train_val_size: float = 0.8
    val_size: float = 0.2
    test_size: float = 0.2
    random_state: int = 42
    skew_threshold: float = 3.0
    threat_level: Literal[0, 1, 2] = 2  # 2: Meta-categorias consolidadas
    deduplicate: bool = False

    @property
    def dataset_path(self) -> Path:
        clean_name = self.dataset_name[:-8] if self.dataset_name.endswith(".parquet") else (
            self.dataset_name[:-4] if self.dataset_name.endswith(".csv") else self.dataset_name
        )
        cand_paths: List[Path] = []
        if self.load_sampled:
            cand_paths.extend([
                DATASETS_DIR / f"{clean_name}_sampled.parquet",
                DATASETS_DIR / f"{clean_name}_sampled.csv",
            ])
        if self.dataset_name.endswith(".parquet") or self.dataset_name.endswith(".csv"):
            cand_paths.append(DATASETS_DIR / self.dataset_name)
        cand_paths.extend([
            DATASETS_DIR / f"{clean_name}.parquet",
            DATASETS_DIR / f"{clean_name}.csv",
        ])
        for p in cand_paths:
            if p.exists():
                return p
        suffix = "_sampled.csv" if self.load_sampled else ".csv"
        return DATASETS_DIR / f"{clean_name}{suffix}"


# =============================================================================
# ARQUITETURA NEURAL ALF-MoE
# =============================================================================
@dataclass
class ModelConfig:
    # Dimensão de entrada tabular canônica CIC (73 features após remoção de colunas URG sem variância)
    num_features: int = 73
    num_experts: int = 5

    # DNN Expert (General Statistical Domain)
    dnn_units: Tuple[int, ...] = (256, 128)
    dnn_dropout: float = 0.1

    # CNN Expert (Spatial Packet Geometry Domain - 16 canonical features -> 4x4)
    cnn_filters: Tuple[int, ...] = (64, 128)
    cnn_kernel_size: Tuple[int, int] = (2, 2)
    cnn_dense_units: int = 128
    cnn_dropout: float = 0.2

    # GRU Expert (Short-term Temporal Domain - 32 features -> 8x4)
    gru_units: int = 64
    gru_dense_units: int = 128
    gru_dropout: float = 0.1

    # CAE Expert (Frequency Domain - 27 features -> Hann + RFFT)
    cae_filters: Tuple[int, ...] = (16, 32, 64)
    cae_kernel_size: int = 5
    cae_lambda_rec: float = 1.0
    cae_lambda_reg: float = 1e-4
    cae_dense_units: int = 128
    cae_dropout: float = 0.1

    # LSTM Expert (Long-term Temporal State Domain - 18 features -> 6x3)
    lstm_units: int = 64
    lstm_dense_units: int = 128
    lstm_dropout: float = 0.1

    # Gating Network (Dynamic Router com Refinamento Atencional)
    gating_units: Tuple[int, ...] = (128, 64)
    gating_dropout: float = 0.1
    gating_temperature_init: float = 1.0

    # ALF Module (Attention-based Learnable Fusion Module)
    alf_units: int = 128
    alf_dropout: float = 0.1


# =============================================================================
# TREINAMENTO & OTIMIZAÇÃO
# =============================================================================
@dataclass
class TrainingConfig:
    epochs: int = 10
    batch_size: int = 128
    learning_rate: float = 1e-3
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-8

    # Supervisão multi-task equilibrada (ALF=1.0, cada especialista=0.2, Gating=0.0)
    alf_weight: float = 1.0
    auxiliary_weight: float = 0.2

    # Focal Loss (sem dupla ponderação!)
    focal_gamma: float = 2.0
    class_weight_strategy: Literal["none", "sqrt", "balanced"] = "sqrt"

    # Callbacks de convergência
    reduce_lr_patience: int = 2
    reduce_lr_factor: float = 0.5
    min_lr: float = 1e-6
    early_stopping_patience: int = 4
    monitor_metric: str = "val_ALF_F1-Score"
    monitor_mode: str = "max"


# =============================================================================
# AUDITORIA SIEM & DEFESA ATIVA (PRODUÇÃO)
# =============================================================================
@dataclass
class InferenceConfig:
    threat_threshold: float = 0.70
    enable_active_defense: bool = True
    active_defense_duration: int = 300  # 5 minutos de bloqueio automático via nftables
    active_response_text: str = "I SEE YOU!"
    active_responder_port: int = 9999
    enable_audit: bool = True
    audit_jsonl: bool = True
    audit_to_file: bool = True
    audit_to_console: bool = False
    protected_ips: List[str] = field(default_factory=lambda: [
        "127.0.0.1", "::1", "0.0.0.0", "localhost"
    ])


# =============================================================================
# INSTÂNCIA DE CONFIGURAÇÃO UNIFICADA
# =============================================================================
@dataclass
class ALFConfig:
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    inference: InferenceConfig = field(default_factory=InferenceConfig)
    base_dir: Path = BASE_DIR
    artifacts_dir: Path = ARTIFACTS_DIR
    logs_dir: Path = LOGS_DIR


# Instância global singleton padrão para importação direta
CONFIG = ALFConfig()
