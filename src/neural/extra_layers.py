"""
Camadas Neurais Customizadas e Funções de Perda do Modelo ALF-MoE.

Implementa componentes essenciais para Keras 3 / TensorFlow 2.x com
serialização completa (@keras.saving.register_keras_serializable):
- FocalLoss: Perda focal multiclasse com estabilidade numérica e suporte a pesos de classe
- HannFFTLayer: Janelamento temporal de Hann e magnitude espectral via RFFT
- ConvolutionalAutoencoder: Autoencoder convolucional 1D com perda composta MSE
- CAELoss: Camada auxiliar de perda de reconstrução do especialista de frequência
- WeightedSumFusion: Fusão estrita por soma ponderada dos 5 especialistas (Eq. 27)
- AttentionRefinementLayer: Refinamento atencional calibrado sem saturação rígida de tanh
- SliceLayer: Fatiamento funcional serializável para particionamento de domínios
"""

from __future__ import annotations
import keras
from keras import ops
import tensorflow as tf
import numpy as np
from typing import Dict, Optional, Union, List, Any, Tuple, Sequence


# =============================================================================
# PERDA FOCAL MULTICLASSE (Focal Loss)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class FocalLoss(keras.losses.Loss):
    """
    Focal Loss multiclasse para desbalanceamento de classes em tráfego de rede:
    FL(p_t) = -α_t * (1 - p_t)^γ * log(p_t)

    Evita dupla ponderação (utiliza alpha apenas aqui ou via sample_weight, nunca ambos).
    """

    def __init__(
        self,
        gamma: float = 2.0,
        alpha: Optional[Union[float, List[float], np.ndarray, Dict[int, float]]] = None,
        from_logits: bool = False,
        name: str = "focal_loss",
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.gamma = float(gamma)
        self.from_logits = from_logits
        self._alpha_raw = alpha

        if alpha is not None:
            if isinstance(alpha, dict):
                max_k = max(int(k) for k in alpha.keys()) if alpha else 0
                alpha_list = [float(alpha.get(i, 1.0)) for i in range(max_k + 1)]
                self.alpha = tf.constant(alpha_list, dtype=tf.float32)
            elif isinstance(alpha, (list, tuple, np.ndarray)):
                self.alpha = tf.constant([float(x) for x in alpha], dtype=tf.float32)
            elif isinstance(alpha, (int, float)):
                self.alpha = tf.constant([float(alpha)], dtype=tf.float32)
            elif isinstance(alpha, tf.Tensor):
                self.alpha = tf.cast(alpha, tf.float32)
            else:
                self.alpha = None
        else:
            self.alpha = None

    def call(self, y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        y_true = tf.cast(y_true, tf.float32)
        num_classes = tf.shape(y_pred)[-1]

        # Converte inteiros 1D para representação one-hot se necessário
        y_true = tf.cond(
            tf.logical_or(tf.equal(tf.rank(y_true), 1), tf.not_equal(tf.shape(y_true)[-1], num_classes)),
            lambda: tf.one_hot(tf.cast(tf.reshape(y_true, [-1]), tf.int32), depth=num_classes),
            lambda: y_true,
        )

        if self.from_logits:
            y_pred = tf.nn.softmax(y_pred)

        y_pred = tf.clip_by_value(y_pred, 1e-8, 1.0 - 1e-8)
        cross_entropy = -y_true * tf.math.log(y_pred)
        p_t = tf.reduce_sum(y_true * y_pred, axis=-1, keepdims=True)
        focal_weight = tf.pow(1.0 - p_t, self.gamma)

        if self.alpha is not None:
            alpha_tensor = self.alpha
            alpha_len = tf.shape(alpha_tensor)[0]
            alpha_t = tf.cond(
                tf.equal(alpha_len, num_classes),
                lambda: tf.reduce_sum(y_true * alpha_tensor, axis=-1, keepdims=True),
                lambda: tf.ones_like(p_t),
            )
            focal_weight *= alpha_t

        loss = tf.reduce_sum(cross_entropy * focal_weight, axis=-1)
        return loss

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        if isinstance(self._alpha_raw, np.ndarray):
            alpha_val = self._alpha_raw.tolist()
        elif isinstance(self._alpha_raw, dict):
            alpha_val = {int(k): float(v) for k, v in self._alpha_raw.items()}
        else:
            alpha_val = self._alpha_raw
        cfg.update({
            "gamma": self.gamma,
            "alpha": alpha_val,
            "from_logits": self.from_logits,
        })
        return cfg


# =============================================================================
# JANELAMENTO DE HANN E RFFT (Domínio da Frequência)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class HannFFTLayer(keras.layers.Layer):
    """
    Aplica janela periódica de Hann e extrai a magnitude do espectro RFFT:
    w(n) = 0.5 - 0.5 * cos(2*pi*n / (L - 1))
    x_f = |RFFT(x * w)|
    """

    def __init__(self, signal_length: int, name: str = "hann_fft", **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)
        self.signal_length = int(signal_length)
        if self.signal_length <= 1:
            raise ValueError(f"signal_length deve ser > 1, obtido {signal_length}")

    def build(self, input_shape: Tuple[Optional[int], ...]) -> None:
        n = np.arange(self.signal_length, dtype=np.float32)
        denom = float(self.signal_length - 1)
        window = 0.5 - 0.5 * np.cos(2.0 * np.pi * n / denom)
        self.hann_window = self.add_weight(
            name="hann_window",
            shape=(self.signal_length,),
            initializer=keras.initializers.Constant(window),
            trainable=False,
            dtype="float32",
        )
        super().build(input_shape)

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        x = tf.cast(inputs, tf.float32)
        x = tf.reshape(x, [-1, self.signal_length])
        windowed = x * self.hann_window
        spectrum = tf.signal.rfft(windowed)
        return tf.abs(spectrum)

    def compute_output_shape(self, input_shape: Tuple[Optional[int], ...]) -> Tuple[Optional[int], int]:
        batch_size = input_shape[0]
        spectrum_len = (self.signal_length // 2) + 1
        return (batch_size, spectrum_len)

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        cfg.update({"signal_length": self.signal_length})
        return cfg


# =============================================================================
# AUTOENCODER CONVOLUCIONAL 1D (CAE) COM PERDA COMPOSTA MSE (RESTAURADO)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class ConvolutionalAutoencoder(keras.layers.Layer):
    """
    1D Convolutional Autoencoder with Hann-windowed one-sided FFT preprocessing.

    Pipeline:
        x ∈ R^F
          ↓
        feature selection
          ↓
        Hann window
          ↓
        rFFT magnitude
          ↓
        Conv1D encoder
          ↓
        latent representation z
          ↓
        Conv1DTranspose decoder
          ↓
        reconstructed spectrum

    The layer returns the latent representation and adds the reconstruction
    loss and L2 regularization terms through `self.add_loss()`.

    Parameters
    ----------
    signal_length:
        Number of selected input features used as the signal length L.

    filters:
        Number of filters for each encoder Conv1D layer.

    kernel_size:
        Convolution kernel size.

    strides:
        Encoder/decoder stride.

    feature_indices:
        Explicit indices of the input features used to construct the signal.
        If None, the first `signal_length` features are used.

    lambda_rec:
        Weight applied to the reconstruction MSE.

    lambda_4:
        L2 regularization coefficient.

    flatten_output:
        If True, returns z as [batch, latent_features].
        Otherwise returns z as [batch, time, channels].

    decoder_output_activation:
        Activation used by the last decoder layer. "relu" preserves the
        original implementation and is appropriate for non-negative
        magnitude spectra.
    """

    def __init__(
        self,
        signal_length: int,
        filters: Sequence[int] = (16, 32, 64),
        kernel_size: int = 5,
        strides: int = 2,
        feature_indices: Sequence[int] | None = None,
        lambda_rec: float = 1.0,
        lambda_4: float = 1e-4,
        flatten_output: bool = True,
        decoder_output_activation: str | None = "relu",
        name: str | None = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)

        if signal_length <= 0:
            raise ValueError(
                f"signal_length must be > 0, got {signal_length}"
            )

        if not filters:
            raise ValueError("filters cannot be empty.")

        if any(int(f) <= 0 for f in filters):
            raise ValueError(
                f"All filter sizes must be > 0, got {filters}"
            )

        if kernel_size <= 0:
            raise ValueError(
                f"kernel_size must be > 0, got {kernel_size}"
            )

        if strides <= 0:
            raise ValueError(
                f"strides must be > 0, got {strides}"
            )

        if lambda_rec < 0:
            raise ValueError(
                f"lambda_rec must be >= 0, got {lambda_rec}"
            )

        if lambda_4 < 0:
            raise ValueError(
                f"lambda_4 must be >= 0, got {lambda_4}"
            )

        if feature_indices is not None:
            feature_indices = tuple(int(i) for i in feature_indices)

            if len(feature_indices) != signal_length:
                raise ValueError(
                    "feature_indices length must match signal_length: "
                    f"{len(feature_indices)} != {signal_length}"
                )

            if any(i < 0 for i in feature_indices):
                raise ValueError(
                    "feature_indices cannot contain negative indices."
                )

        self.signal_length = int(signal_length)
        self.filters = tuple(int(f) for f in filters)
        self.kernel_size = int(kernel_size)
        self.strides = int(strides)
        self.feature_indices = feature_indices
        self.lambda_rec = float(lambda_rec)
        self.lambda_4 = float(lambda_4)
        self.flatten_output = bool(flatten_output)
        self.decoder_output_activation = decoder_output_activation

        self.spectrum_length = (self.signal_length // 2) + 1

        self.hann_window: tf.Tensor | None = None

        self.enc_convs: list[keras.layers.Conv1D] = []
        self.dec_convs: list[keras.layers.Conv1DTranspose] = []

        self.flatten_layer: keras.layers.Flatten | None = None

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, input_shape: tf.TensorShape) -> None:
        input_dim = input_shape[-1]

        if input_dim is None:
            raise ValueError(
                "The input feature dimension must be statically known."
            )

        input_dim = int(input_dim)

        # --------------------------------------------------------------
        # Validate feature selection
        # --------------------------------------------------------------

        if self.feature_indices is None:
            if input_dim < self.signal_length:
                raise ValueError(
                    "Input feature dimension is smaller than signal_length: "
                    f"{input_dim} < {self.signal_length}"
                )
        else:
            max_index = max(self.feature_indices)

            if max_index >= input_dim:
                raise ValueError(
                    f"feature_indices contains index {max_index}, but "
                    f"input has only {input_dim} features."
                )

        # --------------------------------------------------------------
        # Hann window
        # --------------------------------------------------------------

        self.hann_window = tf.signal.hann_window(
            self.signal_length,
            periodic=True,
            dtype=tf.float32,
        )

        # --------------------------------------------------------------
        # L2 regularization
        # --------------------------------------------------------------

        kernel_regularizer = (
            keras.regularizers.L2(self.lambda_4)
            if self.lambda_4 > 0
            else None
        )

        # --------------------------------------------------------------
        # Encoder
        # --------------------------------------------------------------

        self.enc_convs = []

        for i, n_filters in enumerate(self.filters):
            self.enc_convs.append(
                keras.layers.Conv1D(
                    filters=n_filters,
                    kernel_size=self.kernel_size,
                    strides=self.strides,
                    padding="same",
                    activation="relu",
                    kernel_regularizer=kernel_regularizer,
                    name=f"enc_conv_{i}",
                )
            )

        # --------------------------------------------------------------
        # Decoder
        #
        # Example:
        #     encoder: 16 → 32 → 64
        #     decoder: 32 → 16 → 1
        # --------------------------------------------------------------

        decoder_filters = tuple(reversed(self.filters[:-1])) + (1,)

        self.dec_convs = []

        for i, n_filters in enumerate(decoder_filters):
            is_last = i == len(decoder_filters) - 1

            activation = (
                self.decoder_output_activation
                if is_last
                else "relu"
            )

            self.dec_convs.append(
                keras.layers.Conv1DTranspose(
                    filters=n_filters,
                    kernel_size=self.kernel_size,
                    strides=self.strides,
                    padding="same",
                    activation=activation,
                    kernel_regularizer=kernel_regularizer,
                    name=f"dec_conv_transpose_{i}",
                )
            )

        # --------------------------------------------------------------
        # Latent flattening
        # --------------------------------------------------------------

        if self.flatten_output:
            self.flatten_layer = keras.layers.Flatten(
                name="latent_flatten"
            )

        super().build(input_shape)

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------

    def _select_features(self, x: tf.Tensor) -> tf.Tensor:
        """Selects the L-dimensional signal from the original F features."""

        if self.feature_indices is not None:
            return tf.gather(
                x,
                indices=self.feature_indices,
                axis=-1,
            )

        return x[..., : self.signal_length]

    def _extract_and_transform(self, x: tf.Tensor) -> tf.Tensor:
        """
        Converts selected tabular features into a one-sided FFT magnitude
        representation.

        x:
            [B, F]

        Returns:
            [B, L//2 + 1]
        """

        x = tf.cast(x, tf.float32)

        # R^F → R^L
        signal = self._select_features(x)

        # Hann window
        windowed = signal * self.hann_window

        # One-sided FFT for real-valued input
        spectrum = tf.signal.rfft(windowed)

        # Magnitude spectrum
        return tf.abs(spectrum)

    # ------------------------------------------------------------------
    # Encoder
    # ------------------------------------------------------------------

    def encode(
        self,
        spectrum: tf.Tensor,
        training: bool | None = None,
    ) -> tf.Tensor:
        """
        Encodes the FFT magnitude into the latent representation.

        Input:
            [B, spectrum_length]

        Output:
            [B, reduced_length, latent_channels]
        """

        z = tf.expand_dims(spectrum, axis=-1)

        for conv in self.enc_convs:
            z = conv(z, training=training)

        return z

    # ------------------------------------------------------------------
    # Decoder
    # ------------------------------------------------------------------

    def decode(
        self,
        z: tf.Tensor,
        training: bool | None = None,
    ) -> tf.Tensor:
        """
        Reconstructs the FFT magnitude spectrum.

        Output shape is forced to:
            [B, spectrum_length]
        """

        reconstruction = z

        for deconv in self.dec_convs:
            reconstruction = deconv(
                reconstruction,
                training=training,
            )

        # [B, L_out, 1] → [B, L_out]
        reconstruction = tf.squeeze(
            reconstruction,
            axis=-1,
        )

        # --------------------------------------------------------------
        # Length alignment
        # --------------------------------------------------------------

        current_length = tf.shape(reconstruction)[-1]
        target_length = self.spectrum_length

        def crop() -> tf.Tensor:
            return reconstruction[:, :target_length]

        def pad() -> tf.Tensor:
            padding = target_length - current_length

            return tf.pad(
                reconstruction,
                paddings=[
                    [0, 0],
                    [0, padding],
                ],
            )

        reconstruction = tf.cond(
            current_length >= target_length,
            crop,
            pad,
        )

        reconstruction.set_shape(
            [None, self.spectrum_length]
        )

        return reconstruction

    # ------------------------------------------------------------------
    # Forward pass
    # ------------------------------------------------------------------

    def call(
        self,
        inputs: tf.Tensor,
        training: bool | None = None,
    ) -> tf.Tensor:

        # --------------------------------------------------------------
        # 1. Feature selection + Hann + rFFT
        # --------------------------------------------------------------

        spectrum = self._extract_and_transform(inputs)

        # --------------------------------------------------------------
        # 2. Encoder
        # --------------------------------------------------------------

        z = self.encode(
            spectrum,
            training=training,
        )

        # --------------------------------------------------------------
        # 3. Decoder
        # --------------------------------------------------------------

        reconstructed = self.decode(
            z,
            training=training,
        )

        # --------------------------------------------------------------
        # 4. Reconstruction loss
        #
        # True MSE:
        #
        #   1/NL * Σ (x_f - x̂_f)^2
        # --------------------------------------------------------------

        if self.lambda_rec > 0:
            reconstruction_loss = tf.reduce_mean(
                tf.square(
                    spectrum - reconstructed
                )
            )

            self.add_loss(
                self.lambda_rec * reconstruction_loss
            )

        # --------------------------------------------------------------
        # 5. Return latent representation
        # --------------------------------------------------------------

        if self.flatten_output:
            return self.flatten_layer(z)

        return z

    # ------------------------------------------------------------------
    # Shape inference
    # ------------------------------------------------------------------

    def compute_output_shape(
        self,
        input_shape: tf.TensorShape,
    ) -> tf.TensorShape:

        batch_size = input_shape[0]

        latent_length = self.spectrum_length

        # Conv1D(..., padding="same", stride=s)
        # gives ceil(length / stride).
        for _ in self.filters:
            latent_length = (
                latent_length + self.strides - 1
            ) // self.strides

        latent_channels = self.filters[-1]

        if self.flatten_output:
            return tf.TensorShape(
                [
                    batch_size,
                    latent_length * latent_channels,
                ]
            )

        return tf.TensorShape(
            [
                batch_size,
                latent_length,
                latent_channels,
            ]
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def get_config(self) -> dict:
        config = super().get_config()

        config.update(
            {
                "signal_length": self.signal_length,
                "filters": list(self.filters),
                "kernel_size": self.kernel_size,
                "strides": self.strides,
                "feature_indices": (
                    list(self.feature_indices)
                    if self.feature_indices is not None
                    else None
                ),
                "lambda_rec": self.lambda_rec,
                "lambda_4": self.lambda_4,
                "flatten_output": self.flatten_output,
                "decoder_output_activation": (
                    self.decoder_output_activation
                ),
            }
        )

        return config


@keras.saving.register_keras_serializable(package="alf_moe")
class CAELoss(keras.layers.Layer):
    """
    Camada auxiliar opcional que adiciona a perda MSE entre espectro original e reconstruído.
    """

    def __init__(self, lambda_rec: float = 1.0, name: str = "cae_loss", **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)
        self.lambda_rec = float(lambda_rec)

    def call(self, inputs: Tuple[tf.Tensor, tf.Tensor]) -> tf.Tensor:
        x_orig, x_recon = inputs
        mse = tf.reduce_mean(tf.square(x_orig - x_recon))
        self.add_loss(self.lambda_rec * mse)
        return x_recon

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        cfg.update({"lambda_rec": self.lambda_rec})
        return cfg


# =============================================================================
# REFINAMENTO ATENCIONAL DA GATING NETWORK (Attention Refinement Layer)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class AttentionRefinementLayer(keras.layers.Layer):
    """
    Camada personalizada de refinamento atencional da Gating Network (Equação 26):
    refined_logits = W_g * log(alpha + eps) + b_g
    refined_logits = tanh(refined_logits)
    a = softmax(refined_logits)

    CORREÇÃO TÉCNICA ESSENCIAL (Equação 26 original):
    A compressão via tf.nn.tanh limita simetricamente os logits em [-1, 1],
    impedindo que biases negativos empurrem os logits para valores extremos (ex: -17),
    o que causaria a extinção catastrófica de especialistas (como o CAE)
    com pesos caindo para 10^-8 na soma ponderada Z.
    """

    def __init__(
        self,
        num_experts: int = 5,
        use_tanh: bool = True,
        temperature_init: float = 1.0,
        learnable_temp: bool = False,
        eps: float = 1e-7,
        name: str = "attention_refinement",
        **kwargs: Any,
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.num_experts = int(num_experts)
        self.use_tanh = bool(use_tanh)
        self.temperature_init = float(temperature_init)
        self.learnable_temp = bool(learnable_temp)
        self.eps = float(eps)

    def build(self, input_shape: Tuple[Optional[int], ...]) -> None:
        experts_in = input_shape[-1] or self.num_experts
        self.W_g = self.add_weight(
            name="W_g",
            shape=(experts_in, self.num_experts),
            initializer=keras.initializers.GlorotUniform(),
            trainable=True,
        )
        self.b_g = self.add_weight(
            name="b_g",
            shape=(self.num_experts,),
            initializer=keras.initializers.Zeros(),
            trainable=True,
        )
        super().build(input_shape)

    def call(self, alpha: tf.Tensor) -> tf.Tensor:
        alpha_clipped = tf.clip_by_value(alpha, self.eps, 1.0)
        log_alpha = tf.math.log(alpha_clipped)
        refined_logits = tf.matmul(log_alpha, self.W_g) + self.b_g
        if self.use_tanh:
            refined_logits = tf.nn.tanh(refined_logits)
        return tf.nn.softmax(refined_logits, axis=-1)

    def compute_output_shape(self, input_shape: Tuple[Optional[int], ...]) -> Tuple[Optional[int], int]:
        return (input_shape[0], self.num_experts)

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        cfg.update({
            "num_experts": self.num_experts,
            "use_tanh": self.use_tanh,
            "temperature_init": self.temperature_init,
            "learnable_temp": self.learnable_temp,
            "eps": self.eps,
        })
        return cfg


# =============================================================================
# FUSÃO POR SOMA PONDERADA ALF (Weighted Sum Fusion - Eq. 27)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class WeightedSumFusion(keras.layers.Layer):
    """
    Camada de fusão por soma ponderada estrita do módulo ALF (Equação 27):
    Z = sum_{k=1}^K a_k * y^{(k)}

    CORREÇÃO TÉCNICA ESSENCIAL:
    Não inclui conexões residuais paralelas (sem concatenar os especialistas
    diretamente na cabeça final). Todo o fluxo de gradiente passa estritamente
    pelo produto atencional Z, forçando o Gating a especializar cada especialista.
    """

    def __init__(self, name: str = "weighted_sum_fusion", **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)

    def call(self, inputs: Tuple[Union[List[tf.Tensor], tf.Tensor], tf.Tensor]) -> tf.Tensor:
        if not isinstance(inputs, (list, tuple)) or len(inputs) != 2:
            raise ValueError(
                "WeightedSumFusion requer inputs=[experts_predictions, attention_weights]"
            )

        experts_preds, attention_weights = inputs

        # Empilha predições dos K especialistas -> Shape: (batch, K, num_classes)
        if isinstance(experts_preds, (list, tuple)):
            stacked_experts = tf.stack(experts_preds, axis=1)
        else:
            stacked_experts = experts_preds

        # Expande pesos de atenção para multiplicação matricial -> Shape: (batch, K, 1)
        attention_expanded = tf.expand_dims(attention_weights, axis=-1)

        # Multiplicação ponderada element-wise e soma sobre o eixo dos especialistas
        weighted = stacked_experts * attention_expanded
        fused_vector = tf.reduce_sum(weighted, axis=1)
        return fused_vector

    def compute_output_shape(self, input_shape: Any) -> Tuple[Optional[int], int]:
        preds_shape = input_shape[0]
        if isinstance(preds_shape, list):
            return (preds_shape[0][0], preds_shape[0][-1])
        elif len(preds_shape) == 3:
            return (preds_shape[0], preds_shape[2])
        return (preds_shape[0], preds_shape[-1])

    def get_config(self) -> Dict[str, Any]:
        return super().get_config()


# =============================================================================
# FATIAMENTO FUNCIONAL SERIALIZÁVEL (SliceLayer)
# =============================================================================
@keras.saving.register_keras_serializable(package="alf_moe")
class SliceLayer(keras.layers.Layer):
    """
    Fatiamento determinístico de colunas tabulares para particionar a entrada única (D,)
    nos 5 subespaços de domínio dos especialistas.
    Totalmente serializável em Keras 3 sem dependência de Lambdas.
    """

    def __init__(self, indices: List[int], name: str = "slice_domain", **kwargs: Any) -> None:
        super().__init__(name=name, **kwargs)
        self.indices = [int(i) for i in indices]

    def build(self, input_shape: Tuple[Optional[int], ...]) -> None:
        self._indices_tensor = self.add_weight(
            name="slice_indices",
            shape=(len(self.indices),),
            initializer=keras.initializers.Constant(self.indices),
            trainable=False,
            dtype=tf.int32,
        )
        super().build(input_shape)

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        return tf.gather(inputs, self._indices_tensor, axis=-1)

    def compute_output_shape(self, input_shape: Tuple[Optional[int], ...]) -> Tuple[Optional[int], int]:
        return (input_shape[0], len(self.indices))

    def get_config(self) -> Dict[str, Any]:
        cfg = super().get_config()
        cfg.update({"indices": self.indices})
        return cfg
