"""
Gating Network (Rede de Roteamento Dinâmico e Refinamento Atencional).

Avalia o vetor tabular global completo (76 features canônicas) e determina a
distribuição adaptativa de pesos de atenção para os 5 especialistas neurais:
a = [a_1, a_2, a_3, a_4, a_5], onde sum(a_k) = 1.

Inclui a camada corrigida AttentionRefinementLayer com temperatura aprendível
e sem saturação rígida de tanh, viabilizando especialização real.
"""

import keras
from keras import layers
from typing import Tuple, Sequence, Optional
from .extra_layers import AttentionRefinementLayer


def build_gating_network(
    input_shape: Tuple[int, ...],
    num_experts: int = 5,
    hidden_units: Sequence[int] = (128, 64),
    dropout_rate: float = 0.1,
    temperature_init: float = 1.0,
    learnable_temp: bool = True,
    name: str = "GN",
) -> keras.Model:
    """
    Constrói a Gating Network dinâmica com refinamento atencional afiado.

    Args:
        input_shape: Formato do vetor global de entrada (ex: (76,)).
        num_experts: Quantidade de especialistas (padrão: 5).
        hidden_units: Neurônios nas camadas densas intermediárias (padrão: 128, 64).
        dropout_rate: Taxa de dropout (padrão: 0.1).
        temperature_init: Temperatura inicial de calibração atencional.
        learnable_temp: Se True, aprende o fator de escala de temperatura.
        name: Nome identificador do modelo da Gating Network.

    Returns:
        keras.Model: Modelo funcional emitindo pesos atencionais normalizados a_1..a_5.
    """
    inputs = layers.Input(shape=input_shape, name=f"{name.lower()}_input")

    x = inputs
    for i, units in enumerate(hidden_units):
        x = layers.Dense(units, activation=None, name=f"{name.lower()}_dense_{i+1}")(x)
        x = layers.BatchNormalization(name=f"{name.lower()}_bn_{i+1}")(x)
        x = layers.LeakyReLU(negative_slope=0.2, name=f"{name.lower()}_lrelu_{i+1}")(x)
        if dropout_rate > 0.0:
            x = layers.Dropout(dropout_rate, name=f"{name.lower()}_drop_{i+1}")(x)

    # Logits iniciais e distribuição de confiança preliminar alpha
    raw_logits = layers.Dense(num_experts, activation=None, name=f"{name.lower()}_raw_logits")(x)
    alpha_softmax = layers.Activation("softmax", name=f"{name.lower()}_alpha_softmax")(raw_logits)

    # Refinamento atencional calibrado (sem compressão tanh limitante)
    attention_weights = AttentionRefinementLayer(
        num_experts=num_experts,
        temperature_init=temperature_init,
        learnable_temp=learnable_temp,
        name=name,
    )(alpha_softmax)

    model = keras.Model(inputs=inputs, outputs=attention_weights, name=name)
    return model
