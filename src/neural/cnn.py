"""
Especialista CNN 2D (Convolutional Neural Network) para o Domínio Espacial.

Modela geometria canônica de pacotes e correlações espaciais locais (matriz 4x4).
Seleciona com segurança as 16 features canônicas de geometria de pacote
(excluindo Flow Packets/s e features de taxa não escalonadas),
reformatando para (4, 4, 1), seguida de convoluções 2D (kernel 2x2, filtros 64 e 128),
Batch Normalization, LeakyReLU(0.2), Dropout(0.2) e projeção densa (128).
"""

import keras
from keras import layers
import numpy as np
from typing import Tuple, Sequence, Optional
from .extra_layers import SliceLayer


def build_cnn_expert(
    input_shape: Tuple[int, ...],
    num_classes: int,
    grid_shape: Tuple[int, int] = (4, 4),
    filters: Sequence[int] = (64, 128),
    kernel_size: Tuple[int, int] = (2, 2),
    dense_units: int = 128,
    dropout_rate: float = 0.2,
    name: str = "CNN",
) -> keras.Model:
    """
    Constrói o especialista CNN 2D para padrões espaciais e geometria canônica de pacotes (4x4).

    Args:
        input_shape: Formato de entrada 1D (ex: (20,)).
        num_classes: Quantidade de classes.
        grid_shape: Dimensões (H, W) para reformatação espacial 2D (4 x 4 = 16).
        filters: Quantidade de filtros convolucionais em cada bloco (padrão: 64, 128).
        kernel_size: Dimensões do kernel 2D (padrão: 2x2).
        dense_units: Neurônios na camada densa pós-flatten (padrão: 128).
        dropout_rate: Taxa de dropout (padrão: 0.2).
        name: Nome do especialista.

    Returns:
        keras.Model: Modelo funcional do especialista CNN 2D com saída Softmax.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    dim = input_shape[0] if len(input_shape) == 1 else int(np.prod(input_shape))
    target_dim = grid_shape[0] * grid_shape[1]  # 4 * 4 = 16

    # Seleção segura das 16 features canônicas de geometria de pacote:
    # Em CICDomainFeatures.x_s(), os primeiros 16 índices correspondem estritamente
    # às estatísticas de comprimento de pacotes (Min, Max, Mean, Std, etc.),
    # excluindo propositalmente o índice 19 ('Flow Packets/s') que possui escala desregulada.
    if dim == target_dim:
        x = inputs
    elif dim > target_dim:
        x = SliceLayer(list(range(target_dim)), name=f"{name.lower()}_canonical_slice")(inputs)
    else:
        x = layers.Dense(target_dim, activation=None, name=f"{name.lower()}_dim_align")(inputs)

    x = layers.Reshape((*grid_shape, 1), name=f"{name.lower()}_reshape_spatial")(x)

    f1 = filters[0] if len(filters) > 0 else 64
    f2 = filters[1] if len(filters) > 1 else 128

    # Bloco Convolucional 1 (Filtros: 64, Kernel: 2x2)
    x = layers.Conv2D(
        filters=f1,
        kernel_size=kernel_size,
        padding="same",
        activation=None,
        name=f"{name.lower()}_conv2d_1",
    )(x)
    x = layers.BatchNormalization(name=f"{name.lower()}_bn_1")(x)
    x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu_1")(x)

    # Bloco Convolucional 2 (Filtros: 128, Kernel: 2x2)
    x = layers.Conv2D(
        filters=f2,
        kernel_size=kernel_size,
        padding="same",
        activation=None,
        name=f"{name.lower()}_conv2d_2",
    )(x)
    x = layers.BatchNormalization(name=f"{name.lower()}_bn_2")(x)
    x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu_2")(x)

    # Flatten e Projeção Densa para Dense(128)
    x = layers.Flatten(name=f"{name.lower()}_flatten")(x)
    x = layers.Dense(dense_units, activation=None, name=f"{name.lower()}_dense")(x)
    x = layers.BatchNormalization(name=f"{name.lower()}_bn_dense")(x)
    x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu_dense")(x)
    if dropout_rate > 0.0:
        x = layers.Dropout(dropout_rate, name=f"{name.lower()}_drop")(x)

    logits = layers.Dense(num_classes, activation=None, name=f"{name.lower()}_logits")(x)
    outputs = layers.Activation("softmax", name=name)(logits)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    return model
