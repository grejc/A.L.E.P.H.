"""
Especialista DNN (Deep Neural Network) para o Domínio Estatístico Geral.

Processa características estatísticas globais do fluxo de rede (F_g).
Arquitetura corrigida:
- Capacidade adequada: 256 -> 128 neurônios
- Batch Normalization e LeakyReLU para evitar saturação e neurônios mortos
- Dropout moderado (0.1) para evitar sobre-regularização e colapso de classes raras
"""

import keras
from keras import layers
from typing import Tuple, Sequence, Optional


def build_dnn_expert(
    input_shape: Tuple[int, ...],
    num_classes: int,
    hidden_units: Sequence[int] = (256, 128),
    dropout_rate: float = 0.1,
    name: str = "DNN",
) -> keras.Model:
    """
    Constrói o especialista DNN robusto com capacidade balanceada.

    Args:
        input_shape: Formato de entrada estatística geral (ex: (29,)).
        num_classes: Quantidade de classes do problema.
        hidden_units: Neurônios nas camadas densas ocultas (padrão: 256, 128).
        dropout_rate: Taxa de dropout moderada (padrão: 0.1).
        name: Nome identificador do modelo especialista.

    Returns:
        keras.Model: Modelo funcional do especialista DNN com saída Softmax.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation=None, name=f"{name.lower()}_dense_{i+1}")(x)
        x = layers.BatchNormalization(name=f"{name.lower()}_bn_{i+1}")(x)
        x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu_{i+1}")(x)
        if dropout_rate > 0.0 and i == 0:
            x = layers.Dropout(dropout_rate, name=f"{name.lower()}_drop_{i+1}")(x)

    logits = layers.Dense(num_classes, activation=None, name=f"{name.lower()}_logits")(x)
    outputs = layers.Activation("softmax", name=name)(logits)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    return model
