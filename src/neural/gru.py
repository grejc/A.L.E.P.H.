"""
Especialista GRU (Gated Recurrent Unit) para o Domínio Temporal Curto / IATs.

Processa séries temporais de intervalos entre pacotes (IATs), taxas e durações
(T_v = 8 passos temporais com d_v = 4 atributos por passo, totalizando 32 features).
"""

import keras
from keras import layers
import numpy as np
from typing import Tuple, Optional


def build_gru_expert(
    input_shape: Tuple[int, ...],
    num_classes: int,
    timesteps: int = 8,
    features_per_step: int = 4,
    gru_units: int = 64,
    dense_units: int = 128,
    dropout_rate: float = 0.1,
    bidirectional: bool = True,
    name: str = "GRU",
) -> keras.Model:
    """
    Constrói o especialista GRU para dependências temporais estatísticas de curto prazo.

    Args:
        input_shape: Formato de entrada (ex: (32,)).
        num_classes: Quantidade de classes.
        timesteps: Número de etapas temporais (padrão: 8).
        features_per_step: Features por etapa temporal (padrão: 4, 8*4=32).
        gru_units: Unidades ocultas na camada GRU.
        dense_units: Neurônios na camada densa pós-recorrência.
        dropout_rate: Taxa de dropout (padrão: 0.1).
        bidirectional: Se True, encapsula GRU em Bidirectional.
        name: Nome identificador do especialista.

    Returns:
        keras.Model: Modelo funcional do especialista GRU com saída Softmax.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    dim = input_shape[0] if len(input_shape) == 1 else np.prod(input_shape)
    target_dim = timesteps * features_per_step

    x = inputs
    if dim != target_dim:
        x = layers.Dense(target_dim, activation=None, name=f"{name.lower()}_dim_align")(x)

    x = layers.Reshape((timesteps, features_per_step), name=f"{name.lower()}_reshape_seq")(x)

    gru_layer = layers.GRU(gru_units, return_sequences=False, name=f"{name.lower()}_core")
    if bidirectional:
        x = layers.Bidirectional(gru_layer, name=f"{name.lower()}_bidirectional")(x)
    else:
        x = gru_layer(x)

    x = layers.BatchNormalization(name=f"{name.lower()}_bn")(x)
    x = layers.Dense(dense_units, activation=None, name=f"{name.lower()}_dense")(x)
    x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu")(x)
    if dropout_rate > 0.0:
        x = layers.Dropout(dropout_rate, name=f"{name.lower()}_drop")(x)

    logits = layers.Dense(num_classes, activation=None, name=f"{name.lower()}_logits")(x)
    outputs = layers.Activation("softmax", name=name)(logits)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    return model
