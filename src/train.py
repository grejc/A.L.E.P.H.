"""
Script Executável de Treinamento Direto para o Modelo ALF-MoE.

Permite execução imediata:
    python train.py

Estrutura de Artefatos em 3 Subpastas exatamente como no padrão canônico:
    artifacts/{dataset}/{timestamp}/
        preprocess/
            {dataset}_artifacts.pkl
            {dataset}_metadata.json
        model/
            model_architecture.json
            weights.weights.h5 (e alf_moe.weights.h5)
            model.keras (e alf_moe.keras)
            model_summary.txt
        reports/
            training_curves.png
            training_history.csv e training_history.json
            training_report.txt e training_report.json
            test_report.txt e test_report.json
            classification_report.csv
            confusion_matrix.csv, confusion_matrix.png, confusion_matrix_normalized.csv, confusion_matrix_normalized.png
            expert_comparison_heatmap.csv e .png (F1-Score para 5 especialistas + ALF)
            expert_comparison_accuracy_heatmap.csv e .png (Acurácia OvR para 5 especialistas + ALF)
            expert_comparison_precision_heatmap.csv e .png (Precisão para 5 especialistas + ALF)
            expert_comparison_recall_heatmap.csv e .png (Recall para 5 especialistas + ALF)
            alf_moe_metrics_heatmap.csv e .png (Precision, Recall, F1 do ALF)
            gating_attention_heatmap.csv e .png (Média de pesos do Gating)
            gating_weights_boxplot.png (Boxplot dos pesos do Gating por classe)
            expert_radar_chart.png (Radar Chart comparativo dos 5 especialistas + ALF)
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Silenciar logs excessivos do TensorFlow para treinamento limpo
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "0")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import pandas as pd
import keras

from config import CONFIG
from domain_features import CICDomainFeatures
from preprocessing import Preprocessor
from neural.model import ALFMoEModel
from reports import (
    plot_training_curves,
    plot_confusion_matrix,
    plot_gating_attention_heatmap,
    plot_gating_weights_boxplot,
    plot_expert_comparison_heatmap,
    plot_alf_metrics_heatmap,
    plot_expert_radar_chart,
    generate_training_report,
    generate_test_report,
)


def run_training(
    dataset_name: str = CONFIG.preprocessing.dataset_name,
    epochs: int = CONFIG.training.epochs,
    batch_size: int = CONFIG.training.batch_size,
    learning_rate: float = CONFIG.training.learning_rate,
    threat_level: int = CONFIG.preprocessing.threat_level,
    load_sampled: bool = CONFIG.preprocessing.load_sampled,
    auxiliary_weight: float = CONFIG.training.auxiliary_weight,
    focal_gamma: float = CONFIG.training.focal_gamma,
    artifacts_root: Path = CONFIG.artifacts_dir,
) -> Path:
    """
    Executa o pipeline completo de ponta a ponta:
    Pré-processamento -> Compilação -> Treino -> Avaliação -> Geração Completa de Artefatos.
    """
    start_total_time = time.perf_counter()
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    experiment_dir = artifacts_root / dataset_name / timestamp_str

    # 1. Estrutura de Artefatos em 3 Subpastas
    preprocess_dir = experiment_dir / "preprocess"
    models_dir = experiment_dir / "model"
    reports_dir = experiment_dir / "reports"

    experiment_dir.mkdir(parents=True, exist_ok=True)
    preprocess_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print(f"             INICIANDO TREINAMENTO ALF-MoE [{dataset_name}]")
    print(f"  Diretório Raiz de Artefatos: {experiment_dir}")
    print(f"  Subpastas: preprocess/, model/, reports/")
    print(f"  Épocas: {epochs} | Batch Size: {batch_size} | LR: {learning_rate}")
    print(f"  Threat Level: {threat_level} | Sampled: {load_sampled}")
    print("=" * 80)

    # 2. Carregamento e Pré-processamento
    print("\n[Etapa 1/5] Executando pré-processamento robusto sem vazamento de dados...")
    prep = Preprocessor(
        dataset=dataset_name,
        load_sampled=load_sampled,
        train_val_size=CONFIG.preprocessing.train_val_size,
        val_size=CONFIG.preprocessing.val_size,
        test_size=CONFIG.preprocessing.test_size,
        random_state=CONFIG.preprocessing.random_state,
        skew_threshold=CONFIG.preprocessing.skew_threshold,
        threat_level=threat_level,
        artifacts_dir=preprocess_dir,
        auto_load=True,
    )

    (X_train, y_train), (X_val, y_val), (X_test, y_test) = prep.generate_train_val_test(
        stratify=True,
        threat_level=threat_level,
        deduplicate=CONFIG.preprocessing.deduplicate,
    )

    # Persiste artefatos em preprocess/ ({dataset}_artifacts.pkl e {dataset}_metadata.json)
    pkl_art, json_meta = prep.save_artifacts()
    print(f"[Pré-processamento] Artefatos salvos em: {preprocess_dir}")

    # 3. Mapeamento de Domínios dos Especialistas
    print("\n[Etapa 2/5] Mapeando subespaços estatísticos dos 5 especialistas...")
    domain_indices = prep.get_domain_indices()

    # 4. Construção e Compilação da Arquitetura ALF-MoE
    print("\n[Etapa 3/5] Instanciando e compilando arquitetura ALF-MoE multi-task...")
    model_wrapper = ALFMoEModel(
        feature_names=prep.feature_names,
        classes=prep.classes,
        domain_indices=domain_indices,
        dnn_units=CONFIG.model.dnn_units,
        dnn_dropout=CONFIG.model.dnn_dropout,
        cnn_filters=CONFIG.model.cnn_filters,
        cnn_kernel_size=CONFIG.model.cnn_kernel_size,
        cnn_dense_units=CONFIG.model.cnn_dense_units,
        cnn_dropout=CONFIG.model.cnn_dropout,
        gru_units=CONFIG.model.gru_units,
        gru_dense_units=CONFIG.model.gru_dense_units,
        gru_dropout=CONFIG.model.gru_dropout,
        cae_filters=CONFIG.model.cae_filters,
        cae_kernel_size=CONFIG.model.cae_kernel_size,
        cae_lambda_rec=CONFIG.model.cae_lambda_rec,
        cae_lambda_reg=CONFIG.model.cae_lambda_reg,
        cae_dense_units=CONFIG.model.cae_dense_units,
        cae_dropout=CONFIG.model.cae_dropout,
        lstm_units=CONFIG.model.lstm_units,
        lstm_dense_units=CONFIG.model.lstm_dense_units,
        lstm_dropout=CONFIG.model.lstm_dropout,
        gating_units=CONFIG.model.gating_units,
        gating_dropout=CONFIG.model.gating_dropout,
        gating_temperature_init=CONFIG.model.gating_temperature_init,
        alf_units=CONFIG.model.alf_units,
        alf_dropout=CONFIG.model.alf_dropout,
    )

    # Class weights aplicados exclusivamente na Focal Loss (sem dupla ponderação!)
    model_wrapper.compile(
        learning_rate=learning_rate,
        beta_1=CONFIG.training.beta_1,
        beta_2=CONFIG.training.beta_2,
        epsilon=CONFIG.training.epsilon,
        auxiliary_weight=auxiliary_weight,
        focal_gamma=focal_gamma,
        class_weights=prep.class_weights if CONFIG.training.class_weight_strategy != "none" else None,
    )

    print("\nSumário da Arquitetura Unificada:")
    model_wrapper.summary()

    # Callbacks (salva CSVLogger em reports/training_history.csv)
    history_csv = reports_dir / "training_history.csv"
    callbacks = [
        keras.callbacks.ReduceLROnPlateau(
            monitor=CONFIG.training.monitor_metric,
            mode=CONFIG.training.monitor_mode,
            factor=CONFIG.training.reduce_lr_factor,
            patience=CONFIG.training.reduce_lr_patience,
            min_lr=CONFIG.training.min_lr,
            verbose=1,
        ),
        keras.callbacks.EarlyStopping(
            monitor=CONFIG.training.monitor_metric,
            mode=CONFIG.training.monitor_mode,
            patience=CONFIG.training.early_stopping_patience,
            restore_best_weights=True,
            verbose=1,
        ),
        keras.callbacks.CSVLogger(str(history_csv)),
    ]

    # 5. Execução do Treinamento
    print("\n[Etapa 4/5] Executando treinamento...")
    train_start_time = time.perf_counter()
    history = model_wrapper.fit(
        x_train=X_train,
        y_train=y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1,
    )
    train_time_sec = time.perf_counter() - train_start_time

    # Persistência de Modelos em model/
    # (model_architecture.json, weights.weights.h5, model.keras, model_summary.txt)
    model_wrapper.save(models_dir)
    print(f"\n[Modelo] Artefatos do modelo salvos em: {models_dir}")

    # 6. Avaliação e Geração Completa de Relatórios em reports/
    print("\n[Etapa 5/5] Gerando heatmaps analíticos, boxplot, radar chart e relatórios de desempenho...")
    history_dict = history.history

    # Curvas de treino 2x2
    plot_training_curves(
        history_dict=history_dict,
        output_path=reports_dir / "training_curves.png",
        dataset_name=dataset_name,
    )

    # Relatório de Treinamento (salva training_report.json, training_report.txt, training_history.json)
    generate_training_report(
        history_dict=history_dict,
        train_time_sec=train_time_sec,
        num_samples=len(X_train),
        output_dir=reports_dir,
    )

    # Inferência no conjunto de teste
    test_start_time = time.perf_counter()
    preds_test = model_wrapper.predict(X_test, batch_size=256)
    test_time_sec = time.perf_counter() - test_start_time

    y_pred_alf = np.argmax(preds_test["ALF"], axis=-1)

    # Matrizes de Confusão (Absoluta e Normalizada: .csv e .png)
    plot_confusion_matrix(
        y_true=y_test,
        y_pred=y_pred_alf,
        classes=prep.classes,
        output_dir=reports_dir,
    )

    # Heatmaps Comparativos dos Especialistas vs ALF-MoE por Classe
    # 1. F1-Score
    plot_expert_comparison_heatmap(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        output_path=reports_dir / "expert_comparison_heatmap.png",
        metric="f1",
    )
    # 2. Acurácia Balanceada
    plot_expert_comparison_heatmap(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        output_path=reports_dir / "expert_comparison_balanced_accuracy_heatmap.png",
        metric="balanced_accuracy",
    )
    # 3. Precisão
    plot_expert_comparison_heatmap(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        output_path=reports_dir / "expert_comparison_precision_heatmap.png",
        metric="precision",
    )
    # 4. Recall
    plot_expert_comparison_heatmap(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        output_path=reports_dir / "expert_comparison_recall_heatmap.png",
        metric="recall",
    )

    # Heatmap de Métricas do ALF-MoE (Precision, Recall, F1)
    plot_alf_metrics_heatmap(
        y_true=y_test,
        y_pred_alf=preds_test["ALF"],
        classes=prep.classes,
        output_path=reports_dir / "alf_moe_metrics_heatmap.png",
    )

    # Heatmap e Boxplot de Atenção da Gating Network
    plot_gating_attention_heatmap(
        y_true=y_test,
        gn_weights=preds_test["GN"],
        classes=prep.classes,
        output_path=reports_dir / "gating_attention_heatmap.png",
    )
    plot_gating_weights_boxplot(
        y_true=y_test,
        gn_weights=preds_test["GN"],
        classes=prep.classes,
        output_path=reports_dir / "gating_weights_boxplot.png",
    )

    # Radar Chart Comparativo Global dos 5 Especialistas + ALF-MoE
    plot_expert_radar_chart(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        output_path=reports_dir / "expert_radar_chart.png",
    )

    # Relatório Estruturado de Teste e classification_report.csv
    test_rep = generate_test_report(
        y_true=y_test,
        preds_dict=preds_test,
        classes=prep.classes,
        inference_time_sec=test_time_sec,
        num_samples=len(X_test),
        output_dir=reports_dir,
    )

    total_pipeline_time = time.perf_counter() - start_total_time

    print("\n" + "=" * 80)
    print("                 TREINAMENTO FINALIZADO COM SUCESSO!")
    print(f"  Diretório Final de Artefatos: {experiment_dir}")
    print(f"  Subpastas Preenchidas:")
    print(f"    - {preprocess_dir}")
    print(f"    - {models_dir}")
    print(f"    - {reports_dir}")
    print(f"  Acurácia Teste:              {test_rep['alf_moe_metrics']['accuracy'] * 100:.2f}%")
    print(f"  Macro F1-Score Teste:        {test_rep['alf_moe_metrics']['macro_f1']:.4f}")
    print(f"  Latência de Inferência:      {test_rep['latency_ms_per_sample']:.4f} ms/fluxo")
    print(f"  Vazão de Inferência:         {test_rep['throughput_samples_per_sec']:,.2f} fluxos/s")
    print(f"  Tempo Total de Execução:     {total_pipeline_time:.2f} s")
    print("=" * 80)

    return experiment_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Treinamento direto do modelo ALF-MoE")
    parser.add_argument("--dataset", type=str, default=CONFIG.preprocessing.dataset_name, choices=['CSE-CIC-IDS2018', 'CIC-UNSW-NB15', 'CIC-BCCC-NRC-2024'], help="Nome do dataset")
    parser.add_argument("--epochs", type=int, default=CONFIG.training.epochs, help="Quantidade de épocas")
    parser.add_argument("--batch-size", type=int, default=CONFIG.training.batch_size, help="Tamanho do lote")
    parser.add_argument("--lr", type=float, default=CONFIG.training.learning_rate, help="Taxa de aprendizado")
    parser.add_argument("--threat-level", type=int, default=CONFIG.preprocessing.threat_level, choices=[0, 1, 2], help="Nível de ameaça (0, 1 ou 2)")
    parser.add_argument("--full-dataset", action="store_true", help="Carrega dataset completo em vez de amostrado")

    args = parser.parse_args()

    run_training(
        dataset_name=args.dataset,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        threat_level=args.threat_level,
        load_sampled=not args.full_dataset,
    )


if __name__ == "__main__":
    main()
