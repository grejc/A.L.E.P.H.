"""
Script Executável de Avaliação do Modelo ALF-MoE.

Permite execução imediata:
    python evaluate.py

Localiza automaticamente o artefato treinado mais recente (ou diretório especificado
via `--artifacts-dir`), restaura o preprocessor (em preprocess/) e pesos do modelo (em model/),
avalia no conjunto de teste com medição de latência/vazão e atualiza todos os heatmaps analíticos,
boxplot, radar chart e relatórios em reports/.
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

import numpy as np
import pandas as pd
import keras

from config import CONFIG
from domain_features import CICDomainFeatures
from preprocessing import Preprocessor
from neural.model import ALFMoEModel
from reports import (
    plot_confusion_matrix,
    plot_gating_attention_heatmap,
    plot_gating_weights_boxplot,
    plot_expert_comparison_heatmap,
    plot_alf_metrics_heatmap,
    plot_expert_radar_chart,
    generate_test_report,
)


def find_latest_experiment_dir(base_artifacts: Path, dataset_name: str) -> Path:
    """Localiza o subdiretório de experimento mais recente."""
    target_dir = base_artifacts / dataset_name
    if not target_dir.exists():
        # Fallback para busca recursiva
        candidates = list(base_artifacts.glob(f"**/*{dataset_name}*"))
        if not candidates:
            raise FileNotFoundError(f"Nenhum diretório de artefatos encontrado em: {base_artifacts}")
        target_dir = candidates[0]

    subdirs = [p for p in target_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if not subdirs:
        if (target_dir / "model").exists() or (target_dir / "preprocess").exists():
            return target_dir
        raise FileNotFoundError(f"Nenhum subdiretório de execução encontrado em: {target_dir}")

    # Ordena pelo nome do diretório timestamp (ISO)
    subdirs.sort(key=lambda p: p.name, reverse=True)
    return subdirs[0]


def run_evaluation(
    artifacts_dir: Optional[Union[str, Path]] = None,
    dataset_name: str = CONFIG.preprocessing.dataset_name,
    load_sampled: bool = CONFIG.preprocessing.load_sampled,
    batch_size: int = 256,
    threat_level: Optional[int] = None,
) -> Dict[str, Any]:
    """Executa a avaliação do modelo no conjunto de teste gerando todos os artefatos de relatório."""
    if artifacts_dir is None:
        exp_dir = find_latest_experiment_dir(CONFIG.artifacts_dir, dataset_name)
    else:
        exp_dir = Path(artifacts_dir)

    print("=" * 80)
    print(f"             AVALIAÇÃO DO MODELO ALF-MoE [{dataset_name}]")
    print(f"  Diretório do Experimento: {exp_dir}")
    print("=" * 80)

    # 1. Carregar artefatos de pré-processamento (busca em preprocess/ ou raiz do experimento)
    prep_dir = exp_dir / "preprocess"
    pkl_files = (
        list(prep_dir.glob("*_artifacts.pkl"))
        + list(exp_dir.glob("*_artifacts.pkl"))
        + list(exp_dir.glob("**/*_artifacts.pkl"))
        + list(exp_dir.parent.glob("*_artifacts.pkl"))
    )
    if not pkl_files:
        raise FileNotFoundError(f"Arquivo *_artifacts.pkl não encontrado em {exp_dir}")

    pkl_path = pkl_files[0]
    print(f"Carregando preprocessor de: {pkl_path}")
    prep = Preprocessor(dataset=dataset_name, auto_load=False).load_artifacts(pkl_path)

    # 2. Carregar partição de teste
    print("\n[Etapa 1/4] Carregando partição de teste...")
    prep.dataset = prep.load_dataset()
    threat_lvl = threat_level if threat_level is not None else (
        prep._threat_level_used if prep._threat_level_used is not None else prep.threat_level
    )
    if threat_lvl is None:
        threat_lvl = CONFIG.preprocessing.threat_level

    _, _, (X_test, y_test) = prep.generate_train_val_test(
        stratify=True,
        threat_level=threat_lvl,
        deduplicate=CONFIG.preprocessing.deduplicate,
        refit=False,
    )

    # 3. Localizar e carregar pesos do modelo
    print("\n[Etapa 2/4] Instanciando e restaurando pesos do modelo...")
    domain_indices = prep.get_domain_indices()

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

    model_dir = exp_dir / "model"
    weights_candidates = (
        list(model_dir.glob("weights.weights.h5"))
        + list(model_dir.glob("*.weights.h5"))
        + list(exp_dir.glob("*.weights.h5"))
        + list(exp_dir.glob("**/*.weights.h5"))
    )

    if not weights_candidates:
        raise FileNotFoundError(f"Pesos .weights.h5 não localizados em {exp_dir}")

    target_weights = weights_candidates[0]
    print(f"Carregando pesos de: {target_weights}")
    model_wrapper.load_weights(str(target_weights))

    # 4. Inferência e Medição de Performance
    print("\n[Etapa 3/4] Executando inferência sobre o conjunto de teste...")
    test_start_time = time.perf_counter()
    preds_test = model_wrapper.predict(X_test, batch_size=batch_size)
    inference_time = time.perf_counter() - test_start_time

    y_pred_alf = np.argmax(preds_test["ALF"], axis=-1)

    # 5. Geração de Relatórios e Heatmaps em reports/
    print("\n[Etapa 4/4] Gerando relatórios, matrizes, heatmaps, boxplot e radar chart...")
    reports_dir = exp_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

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
        inference_time_sec=inference_time,
        num_samples=len(X_test),
        output_dir=reports_dir,
    )

    print("\n" + "=" * 80)
    print("                  RESULTADOS DA AVALIAÇÃO DE TESTE")
    print(f"  Amostras de Teste:           {len(X_test):,}")
    print(f"  Acurácia Global:             {test_rep['alf_moe_metrics']['accuracy'] * 100:.2f}%")
    print(f"  Macro F1-Score:              {test_rep['alf_moe_metrics']['macro_f1']:.4f}")
    print(f"  Macro Precisão:              {test_rep['alf_moe_metrics']['macro_precision']:.4f}")
    print(f"  Macro Recall:                {test_rep['alf_moe_metrics']['macro_recall']:.4f}")
    print(f"  Latência por Fluxo:          {test_rep['latency_ms_per_sample']:.4f} ms")
    print(f"  Vazão de Processamento:      {test_rep['throughput_samples_per_sec']:,.2f} fluxos/s")
    print(f"  Relatório completo salvo em: {reports_dir / 'test_report.txt'}")
    print("=" * 80)

    return test_rep


def main() -> None:
    parser = argparse.ArgumentParser(description="Avaliação do modelo ALF-MoE no conjunto de teste")
    parser.add_argument("--artifacts-dir", type=str, default=None, help="Caminho do experimento específico")
    parser.add_argument("--dataset", type=str, default=CONFIG.preprocessing.dataset_name, help="Nome do dataset")
    parser.add_argument("--batch-size", type=int, default=256, help="Tamanho do lote para inferência")
    parser.add_argument("--full-dataset", action="store_true", help="Utiliza dataset completo")
    parser.add_argument("--threat-level", type=int, default=None, choices=[0, 1, 2], help="Nível de ameaça (sobrescreve o do artefato se fornecido)")

    args = parser.parse_args()
    run_evaluation(
        artifacts_dir=args.artifacts_dir,
        dataset_name=args.dataset,
        load_sampled=not args.full_dataset,
        batch_size=args.batch_size,
        threat_level=args.threat_level,
    )


if __name__ == "__main__":
    main()
