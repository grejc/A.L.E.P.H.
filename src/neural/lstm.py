"""
Especialista LSTM (Long Short-Term Memory) para o Domínio Temporal Longo / Estados.

Processa sequências temporais de longa duração do ciclo de vida da conexão
(T_t = 6 passos temporais com d_t = 3 atributos por passo, totalizando 18 features).
"""

import keras
from keras import layers
import numpy as np
from typing import Tuple, Optional


def build_lstm_expert(
    input_shape: Tuple[int, ...],
    num_classes: int,
    timesteps: int = 6,
    features_per_step: int = 3,
    lstm_units: int = 64,
    dense_units: int = 128,
    dropout_rate: float = 0.1,
    bidirectional: bool = True,
    name: str = "LSTM",
) -> keras.Model:
    """
    Constrói o especialista LSTM para dinâmica temporal de longo prazo e estados de protocolo.

    Args:
        input_shape: Formato de entrada (ex: (18,)).
        num_classes: Quantidade de classes.
        timesteps: Número de etapas temporais (padrão: 6).
        features_per_step: Features por etapa temporal (padrão: 3, 6*3=18).
        lstm_units: Unidades ocultas na camada LSTM.
        dense_units: Neurônios na camada densa pós-recorrência.
        dropout_rate: Taxa de dropout (padrão: 0.1).
        bidirectional: Se True, encapsula LSTM em Bidirectional.
        name: Nome identificador do especialista.

    Returns:
        keras.Model: Modelo funcional do especialista LSTM com saída Softmax.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    dim = input_shape[0] if len(input_shape) == 1 else np.prod(input_shape)
    target_dim = timesteps * features_per_step

    x = inputs
    if dim != target_dim:
        x = layers.Dense(target_dim, activation=None, name=f"{name.lower()}_dim_align")(x)

    x = layers.Reshape((timesteps, features_per_step), name=f"{name.lower()}_reshape_seq")(x)

    lstm_layer = layers.LSTM(lstm_units, return_sequences=False, name=f"{name.lower()}_core")
    if bidirectional:
        x = layers.Bidirectional(lstm_layer, name=f"{name.lower()}_bidirectional")(x)
    else:
        x = lstm_layer(x)

    x = layers.BatchNormalization(name=f"{name.lower()}_bn")(x)
    x = layers.Dense(dense_units, activation=None, name=f"{name.lower()}_dense")(x)
    x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu")(x)
    if dropout_rate > 0.0:
        x = layers.Dropout(dropout_rate, name=f"{name.lower()}_drop")(x)

    logits = layers.Dense(num_classes, activation=None, name=f"{name.lower()}_logits")(x)
    outputs = layers.Activation("softmax", name=name)(logits)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    return model
