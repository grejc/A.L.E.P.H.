"""
Modelo Completo ALF-MoE (Attention-based Learnable Fusion of Experts).

Integra os 5 especialistas heterogêneos, a Gating Network com refinamento atencional
e o módulo ALF sob uma única entrada tabular canônica (D=76).

Correções Essenciais Incorporadas:
1. Entrada tabular única com fatiamento funcional via SliceLayer (sem descontinuidades).
2. Fusão ALF mediada ESTRITAMENTE pela soma ponderada Z (sem bypass residual ou
   concatenação espúria direta de especialistas na cabeça final).
3. Compilação multi-task balanceada (ALF=1.0, Especialistas=0.2, Gating=0.0).
4. Focal Loss sem dupla ponderação de classes (utiliza alpha apenas na perda,
   eliminando pesos ao quadrado ~325.000).
"""

import keras
from keras import layers
import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union, Sequence

from .extra_layers import (
    FocalLoss,
    WeightedSumFusion,
    SliceLayer,
)
from .dnn import build_dnn_expert
from .cnn import build_cnn_expert
from .gru import build_gru_expert
from .cae import build_cae_expert
from .lstm import build_lstm_expert
from .gating import build_gating_network


class ALFMoEModel:
    """
    Controlador e encapsulador da arquitetura neural ALF-MoE completa.

    Attributes:
        feature_names (List[str]): Nomes das 76 features tabulares canônicas.
        classes (List[str]): Rótulos das classes do problema.
        num_classes (int): Quantidade de classes.
        domain_indices (Dict[str, List[int]]): Índices das colunas para cada especialista.
        model (keras.Model): Grafo funcional unificado Keras.
    """

    def __init__(
        self,
        feature_names: List[str],
        classes: List[str],
        domain_indices: Dict[str, List[int]],
        dnn_units: Tuple[int, ...] = (256, 128),
        dnn_dropout: float = 0.1,
        cnn_filters: Tuple[int, ...] = (64, 128),
        cnn_kernel_size: Tuple[int, int] = (2, 2),
        cnn_dense_units: int = 128,
        cnn_dropout: float = 0.2,
        gru_units: int = 64,
        gru_dense_units: int = 128,
        gru_dropout: float = 0.1,
        cae_filters: Tuple[int, ...] = (16, 32, 64),
        cae_kernel_size: int = 5,
        cae_lambda_rec: float = 1.0,
        cae_lambda_reg: float = 1e-4,
        cae_dense_units: int = 128,
        cae_dropout: float = 0.1,
        lstm_units: int = 64,
        lstm_dense_units: int = 128,
        lstm_dropout: float = 0.1,
        gating_units: Tuple[int, ...] = (128, 64),
        gating_dropout: float = 0.1,
        gating_temperature_init: float = 1.0,
        alf_units: int = 128,
        alf_dropout: float = 0.1,
        name: str = "ALF_MoE",
    ) -> None:
        self.feature_names = list(feature_names)
        self.classes = list(classes)
        self.num_classes = len(self.classes)
        self.domain_indices = domain_indices
        self.name = name

        # Construção da arquitetura funcional
        self.model = self._build_architecture(
            dnn_units=dnn_units,
            dnn_dropout=dnn_dropout,
            cnn_filters=cnn_filters,
            cnn_kernel_size=cnn_kernel_size,
            cnn_dense_units=cnn_dense_units,
            cnn_dropout=cnn_dropout,
            gru_units=gru_units,
            gru_dense_units=gru_dense_units,
            gru_dropout=gru_dropout,
            cae_filters=cae_filters,
            cae_kernel_size=cae_kernel_size,
            cae_lambda_rec=cae_lambda_rec,
            cae_lambda_reg=cae_lambda_reg,
            cae_dense_units=cae_dense_units,
            cae_dropout=cae_dropout,
            lstm_units=lstm_units,
            lstm_dense_units=lstm_dense_units,
            lstm_dropout=lstm_dropout,
            gating_units=gating_units,
            gating_dropout=gating_dropout,
            gating_temperature_init=gating_temperature_init,
            alf_units=alf_units,
            alf_dropout=alf_dropout,
        )

    def _build_architecture(
        self,
        dnn_units: Tuple[int, ...],
        dnn_dropout: float,
        cnn_filters: Tuple[int, ...],
        cnn_kernel_size: Tuple[int, int],
        cnn_dense_units: int,
        cnn_dropout: float,
        gru_units: int,
        gru_dense_units: int,
        gru_dropout: float,
        cae_filters: Tuple[int, ...],
        cae_kernel_size: int,
        cae_lambda_rec: float,
        cae_lambda_reg: float,
        cae_dense_units: int,
        cae_dropout: float,
        lstm_units: int,
        lstm_dense_units: int,
        lstm_dropout: float,
        gating_units: Tuple[int, ...],
        gating_dropout: float,
        gating_temperature_init: float,
        alf_units: int,
        alf_dropout: float,
    ) -> keras.Model:
        # 1. Entrada tabular única (shape: (D,))
        num_features = len(self.feature_names)
        tabular_input = layers.Input(shape=(num_features,), name="input_tabular")

        # 2. Fatiamento funcional serializável via SliceLayer
        slice_dnn = SliceLayer(self.domain_indices["dnn"], name="slice_dnn")(tabular_input)
        slice_cnn = SliceLayer(self.domain_indices["cnn"], name="slice_cnn")(tabular_input)
        slice_gru = SliceLayer(self.domain_indices["gru"], name="slice_gru")(tabular_input)
        slice_cae = SliceLayer(self.domain_indices["cae"], name="slice_cae")(tabular_input)
        slice_lstm = SliceLayer(self.domain_indices["lstm"], name="slice_lstm")(tabular_input)

        # 3. Construção dos 5 Especialistas Neurais Heterogêneos
        dnn_expert = build_dnn_expert(
            input_shape=(len(self.domain_indices["dnn"]),),
            num_classes=self.num_classes,
            hidden_units=dnn_units,
            dropout_rate=dnn_dropout,
            name="DNN",
        )

        cnn_expert = build_cnn_expert(
            input_shape=(len(self.domain_indices["cnn"]),),
            num_classes=self.num_classes,
            grid_shape=(4, 4),
            filters=cnn_filters,
            kernel_size=cnn_kernel_size,
            dense_units=cnn_dense_units,
            dropout_rate=cnn_dropout,
            name="CNN",
        )

        gru_expert = build_gru_expert(
            input_shape=(len(self.domain_indices["gru"]),),
            num_classes=self.num_classes,
            timesteps=8 if len(self.domain_indices["gru"]) == 32 else max(1, len(self.domain_indices["gru"]) // 4),
            features_per_step=4,
            gru_units=gru_units,
            dense_units=gru_dense_units,
            dropout_rate=gru_dropout,
            name="GRU",
        )

        cae_expert = build_cae_expert(
            input_shape=(len(self.domain_indices["cae"]),),
            num_classes=self.num_classes,
            signal_length=len(self.domain_indices["cae"]),
            filters=cae_filters,
            kernel_size=cae_kernel_size,
            strides=1,
            lambda_rec=cae_lambda_rec,
            lambda_reg=cae_lambda_reg,
            dense_units=cae_dense_units,
            dropout_rate=cae_dropout,
            name="CAE",
        )

        lstm_expert = build_lstm_expert(
            input_shape=(len(self.domain_indices["lstm"]),),
            num_classes=self.num_classes,
            timesteps=6 if len(self.domain_indices["lstm"]) == 18 else max(1, len(self.domain_indices["lstm"]) // 3),
            features_per_step=3,
            lstm_units=lstm_units,
            dense_units=lstm_dense_units,
            dropout_rate=lstm_dropout,
            name="LSTM",
        )

        # 4. Gating Network (avalia o vetor global tabular completo de 76 features)
        gating_network = build_gating_network(
            input_shape=(num_features,),
            num_experts=5,
            hidden_units=gating_units,
            dropout_rate=gating_dropout,
            temperature_init=gating_temperature_init,
            learnable_temp=True,
            name="GN",
        )

        # Execução das predições de probabilidade
        pred_dnn = dnn_expert(slice_dnn)
        pred_cnn = cnn_expert(slice_cnn)
        pred_gru = gru_expert(slice_gru)
        pred_cae = cae_expert(slice_cae)
        pred_lstm = lstm_expert(slice_lstm)
        attention_weights = gating_network(tabular_input)

        # 5. Módulo ALF (Fusão por Soma Ponderada Z estrita)
        fused_vector = WeightedSumFusion(name="alf_weighted_fusion")(
            [[pred_dnn, pred_cnn, pred_gru, pred_cae, pred_lstm], attention_weights]
        )

        # Cabeça densa do ALF: opera ESTRITAMENTE sobre o vetor fundido Z
        x = layers.Dense(alf_units, activation=None, name="alf_dense_1")(fused_vector)
        x = layers.BatchNormalization(name="alf_bn_1")(x)
        x = layers.LeakyReLU(negative_slope=0.2, name="alf_lrelu_1")(x)
        if alf_dropout > 0.0:
            x = layers.Dropout(alf_dropout, name="alf_drop_1")(x)

        x = layers.Dense(alf_units // 2, activation=None, name="alf_dense_2")(x)
        x = layers.BatchNormalization(name="alf_bn_2")(x)
        x = layers.LeakyReLU(negative_slope=0.2, name="alf_lrelu_2")(x)

        alf_logits = layers.Dense(self.num_classes, activation=None, name="alf_logits")(x)
        final_alf = layers.Activation("softmax", name="ALF")(alf_logits)

        # 6. Grafo unificado multi-output
        full_model = keras.Model(
            inputs=tabular_input,
            outputs=[pred_dnn, pred_cnn, pred_gru, pred_cae, pred_lstm, attention_weights, final_alf],
            name=self.name,
        )
        return full_model

    def compile(
        self,
        learning_rate: float = 1e-3,
        beta_1: float = 0.9,
        beta_2: float = 0.999,
        epsilon: float = 1e-8,
        auxiliary_weight: float = 0.2,
        focal_gamma: float = 2.0,
        class_weights: Optional[Union[Dict[int, float], List[float], np.ndarray]] = None,
        optimizer: Optional[keras.optimizers.Optimizer] = None,
    ) -> None:
        """
        Compila o modelo com supervisão profunda multi-task e Focal Loss.
        Garante que class_weights seja aplicado exclusivamente na perda (sem dupla ponderação).
        """
        opt = optimizer or keras.optimizers.Adam(
            learning_rate=learning_rate,
            beta_1=beta_1,
            beta_2=beta_2,
            epsilon=epsilon,
        )

        # Instancia FocalLoss garantindo proteção e serialização Keras 3
        criterion = FocalLoss(gamma=focal_gamma, alpha=class_weights)

        losses = {
            "DNN": criterion,
            "CNN": criterion,
            "GRU": criterion,
            "CAE": criterion,
            "LSTM": criterion,
            "GN": None,
            "ALF": criterion,
        }

        loss_weights = {
            "DNN": float(auxiliary_weight),
            "CNN": float(auxiliary_weight),
            "GRU": float(auxiliary_weight),
            "CAE": float(auxiliary_weight),
            "LSTM": float(auxiliary_weight),
            "GN": 0.0,
            "ALF": 1.0,
        }

        metrics = {
            "ALF": [
                keras.metrics.CategoricalAccuracy(name="Accuracy"),
                keras.metrics.Precision(name="Precision"),
                keras.metrics.Recall(name="Recall"),
                keras.metrics.F1Score(average="macro", name="F1-Score"),
            ]
        }

        self.model.compile(
            optimizer=opt,
            loss=losses,
            loss_weights=loss_weights,
            metrics=metrics,
            jit_compile=False,
        )

    def summary(self, print_fn: Any = None) -> None:
        """Exibe ou salva o sumário da arquitetura."""
        self.model.summary(print_fn=print_fn)

    def fit(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        epochs: int = 10,
        batch_size: int = 128,
        callbacks: Optional[List[keras.callbacks.Callback]] = None,
        verbose: int = 1,
    ) -> keras.callbacks.History:
        """
        Treina o modelo com alinhamento multi-output para todos os especialistas e ALF.
        """
        def _to_cat(y_arr: np.ndarray) -> np.ndarray:
            if y_arr.ndim == 1 or y_arr.shape[-1] != self.num_classes:
                return keras.utils.to_categorical(y_arr, num_classes=self.num_classes)
            return y_arr

        y_train_cat = _to_cat(y_train)
        num_samples = len(x_train)

        # Dicionário de alvos multi-output (cada especialista e ALF recebem y_cat)
        train_targets = {
            "DNN": y_train_cat,
            "CNN": y_train_cat,
            "GRU": y_train_cat,
            "CAE": y_train_cat,
            "LSTM": y_train_cat,
            "GN": np.zeros((num_samples, 5), dtype=np.float32),  # Saída GN tem peso 0.0
            "ALF": y_train_cat,
        }

        val_tuple = None
        if validation_data is not None:
            x_val, y_val = validation_data
            y_val_cat = _to_cat(y_val)
            val_samples = len(x_val)
            val_targets = {
                "DNN": y_val_cat,
                "CNN": y_val_cat,
                "GRU": y_val_cat,
                "CAE": y_val_cat,
                "LSTM": y_val_cat,
                "GN": np.zeros((val_samples, 5), dtype=np.float32),
                "ALF": y_val_cat,
            }
            val_tuple = (x_val, val_targets)

        return self.model.fit(
            x=x_train,
            y=train_targets,
            validation_data=val_tuple,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose,
        )

    def predict(
        self,
        x: np.ndarray,
        batch_size: int = 256,
        verbose: int = 0,
    ) -> Dict[str, np.ndarray]:
        """
        Executa inferência e retorna dicionário com saídas dos especialistas e ALF.
        """
        raw_preds = self.model.predict(x, batch_size=batch_size, verbose=verbose)
        return {
            "DNN": raw_preds[0],
            "CNN": raw_preds[1],
            "GRU": raw_preds[2],
            "CAE": raw_preds[3],
            "LSTM": raw_preds[4],
            "GN": raw_preds[5],
            "ALF": raw_preds[6],
        }

    def save_weights(self, filepath: str) -> None:
        """Salva os pesos do modelo."""
        self.model.save_weights(filepath)

    def load_weights(self, filepath: str) -> None:
        """Restaura os pesos do modelo garantindo que todas as variáveis estejam instanciadas."""
        dummy_in = np.zeros((1, len(self.feature_names)), dtype=np.float32)
        try:
            _ = self.model(dummy_in, training=False)
        except Exception:
            pass
        self.model.load_weights(filepath)

    def save(self, filepath: Union[str, Path]) -> None:
        """Salva o modelo serializado no formato Keras 3 ou diretório com artefatos."""
        path = Path(filepath)
        if path.suffix in (".keras", ".h5"):
            self.model.save(str(path))
            return

        path.mkdir(parents=True, exist_ok=True)
        # 1. model.keras & alf_moe.keras
        try:
            self.model.save(str(path / "model.keras"))
        except Exception as exc:
            print(f"[Aviso] Falha ao salvar model.keras: {exc}")
        try:
            self.model.save(str(path / "alf_moe.keras"))
        except Exception:
            pass

        # 2. weights.weights.h5 & alf_moe.weights.h5
        self.model.save_weights(str(path / "weights.weights.h5"))
        try:
            self.model.save_weights(str(path / "alf_moe.weights.h5"))
            self.model.save_weights(str(path / "alf_moe_weights.weights.h5"))
        except Exception:
            pass

        # 3. model_architecture.json
        try:
            with open(path / "model_architecture.json", "w", encoding="utf-8") as f:
                f.write(self.model.to_json())
        except Exception as exc:
            print(f"[Aviso] Falha ao salvar model_architecture.json: {exc}")

        # 4. model_summary.txt
        try:
            with open(path / "model_summary.txt", "w", encoding="utf-8") as f:
                self.model.summary(print_fn=lambda x: f.write(x + "\n"))
        except Exception as exc:
            print(f"[Aviso] Falha ao salvar model_summary.txt: {exc}")

    @classmethod
    def load(cls, filepath: str) -> keras.Model:
        """Carrega modelo serializado Keras 3."""
        return keras.models.load_model(filepath)
