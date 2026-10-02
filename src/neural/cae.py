"""
Especialista CAE (Convolutional Autoencoder) para o Domínio da Frequência.

Processa o subconjunto de features no domínio espectral (L_f = 27 features).
Aplica janelamento de Hann, RFFT e autoencoder convolucional 1D com
perda de reconstrução composta (MSE) e cabeça de classificação supervisionada.
"""

import keras
from keras import layers
from typing import Tuple, Sequence, Optional
from .extra_layers import ConvolutionalAutoencoder


def build_cae_expert(
    input_shape: Tuple[int, ...],
    num_classes: int,
    signal_length: int = 27,
    filters: Sequence[int] = (16, 32, 64),
    kernel_size: int = 5,
    strides: int = 1,
    lambda_rec: float = 1.0,
    lambda_reg: float = 1e-4,
    name: str = "CAE",
) -> keras.Model:
    """
    Constrói o especialista Convolutional Autoencoder (CAE) com perda espectral MSE.

    Args:
        input_shape: Formato de entrada estatística de frequência (ex: (27,)).
        num_classes: Quantidade de classes.
        signal_length: Comprimento do sinal para janelamento Hann e RFFT (padrão: 27).
        filters: Filtros convolucionais 1D do codificador.
        kernel_size: Tamanho do kernel convolucional 1D.
        lambda_rec: Peso da perda de reconstrução MSE adicionada via add_loss().
        lambda_reg: Peso de regularização L2 dos pesos convolucionais.
        dense_units: Neurônios na camada densa pós-autoencoder.
        dropout_rate: Taxa de dropout (padrão: 0.1).
        name: Nome identificador do especialista.

    Returns:
        keras.Model: Modelo funcional do especialista CAE com saída Softmax.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    # Camada customizada auto-suficiente: Hann + RFFT + Conv1D + Transpose + add_loss(MSE)
    cae_layer = ConvolutionalAutoencoder(
        signal_length=signal_length,
        filters=tuple(filters),
        kernel_size=kernel_size,
        strides=strides,
        lambda_rec=lambda_rec,
        lambda_4=lambda_reg,
        flatten_output=True,
        name=f"{name.lower()}_autoencoder",
    )
    latent_repr = cae_layer(inputs)

    outputs = layers.Dense(num_classes, activation="softmax", name=name)(latent_repr)

    model = keras.Model(inputs=inputs, outputs=outputs, name=name)
    return model
