"""
Módulo Neural do Modelo ALF-MoE.

Exporta as camadas customizadas, os 5 especialistas e a classe central ALFMoEModel.
"""

from .extra_layers import (
    FocalLoss,
    HannFFTLayer,
    ConvolutionalAutoencoder,
    CAELoss,
    AttentionRefinementLayer,
    WeightedSumFusion,
    SliceLayer,
)
from .dnn import build_dnn_expert
from .cnn import build_cnn_expert
from .gru import build_gru_expert
from .cae import build_cae_expert
from .lstm import build_lstm_expert
from .gating import build_gating_network
from .model import ALFMoEModel

__all__ = [
    "FocalLoss",
    "HannFFTLayer",
    "ConvolutionalAutoencoder",
    "CAELoss",
    "AttentionRefinementLayer",
    "WeightedSumFusion",
    "SliceLayer",
    "build_dnn_expert",
    "build_cnn_expert",
    "build_gru_expert",
    "build_cae_expert",
    "build_lstm_expert",
    "build_gating_network",
    "ALFMoEModel",
]
