"""
Módulo de Relatórios e Visualização Analítica para ALF-MoE.

Gera todos os artefatos de avaliação estruturados em relatórios e figuras de alta resolução:
- plot_training_curves: Curvas 2x2 (Loss, F1, Acurácia, Precision/Recall)
- plot_confusion_matrix: Matrizes de confusão absoluta e normalizada (.csv e .png)
- plot_expert_comparison_heatmap: Comparativo dos 5 especialistas + ALF por classe para F1, Accuracy (OvR), Precision e Recall (.csv e .png)
- plot_alf_metrics_heatmap: Precisão, Recall e F1 por classe para o ALF-MoE (.csv e .png)
- plot_gating_attention_heatmap: Distribuição de pesos médios da Gating Network por classe (.csv e .png)
- plot_gating_weights_boxplot: Boxplot da distribuição dos pesos da Gating Network por classe (.png)
- plot_expert_radar_chart: Radar Chart comparativo global dos 5 especialistas + ALF-MoE (.png)
- generate_training_report: Relatório estruturado de treino (.json e .txt)
- generate_test_report: Relatório estruturado de teste com latência, vazão e métricas completas por especialista e ALF (.json, .txt e classification_report.csv)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Union, Literal

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Backend não-interativo para geração headless de figuras
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    accuracy_score,
    balanced_accuracy_score,
)


# =============================================================================
# 1. CURVAS DE TREINAMENTO 2x2
# =============================================================================
def plot_training_curves(
    history_dict: Dict[str, List[float]],
    output_path: Union[str, Path],
    dataset_name: str = "CSE-CIC-IDS2018",
) -> None:
    """
    Plota em grade 2x2 as curvas de Loss, Macro F1-Score, Acurácia e Precisão/Recall
    ao longo das épocas para os conjuntos de treino e validação.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not history_dict:
        return

    first_val = list(history_dict.values())[0]
    total_epochs = len(first_val) if isinstance(first_val, list) else 0
    if total_epochs == 0:
        return

    epochs_range = range(1, total_epochs + 1)
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    def _find_metric_key(name: str, prefix: str = "") -> str:
        clean_target = name.lower().replace("-", "").replace("_", "")
        candidates = []
        for k in history_dict.keys():
            k_clean = k.lower()
            if prefix:
                if not k_clean.startswith(prefix.lower()):
                    continue
                rest = k_clean[len(prefix):].replace("-", "").replace("_", "")
            else:
                if k_clean.startswith("val"):
                    continue
                rest = k_clean.replace("-", "").replace("_", "")

            if clean_target in rest:
                candidates.append(k)

        # Prioriza métricas com 'alf' no nome
        for c in candidates:
            if "alf" in c.lower():
                return c
        return candidates[0] if candidates else ""

    # 1. Curva de Perda (Loss)
    tr_loss = _find_metric_key("loss")
    val_loss = _find_metric_key("loss", prefix="val_")
    if tr_loss and val_loss:
        axs[0, 0].plot(epochs_range, history_dict[tr_loss], label="Treino", color="#1f77b4", linewidth=2)
        axs[0, 0].plot(epochs_range, history_dict[val_loss], label="Validação", color="#ff7f0e", linewidth=2, linestyle="--")
        axs[0, 0].set_title(f"Curva de Perda ({dataset_name})", fontsize=12, fontweight="bold")
        axs[0, 0].set_xlabel("Época")
        axs[0, 0].set_ylabel("Loss")
        axs[0, 0].grid(True, linestyle=":", alpha=0.6)
        axs[0, 0].legend()

    # 2. Curva de F1-Score (Macro)
    tr_f1 = _find_metric_key("f1")
    val_f1 = _find_metric_key("f1", prefix="val_")
    if tr_f1 and val_f1:
        axs[0, 1].plot(epochs_range, history_dict[tr_f1], label="Treino", color="#2ca02c", linewidth=2)
        axs[0, 1].plot(epochs_range, history_dict[val_f1], label="Validação", color="#d62728", linewidth=2, linestyle="--")
        axs[0, 1].set_title("F1-Score Macro (ALF)", fontsize=12, fontweight="bold")
        axs[0, 1].set_xlabel("Época")
        axs[0, 1].set_ylabel("F1-Score")
        axs[0, 1].grid(True, linestyle=":", alpha=0.6)
        axs[0, 1].legend()

    # 3. Curva de Acurácia
    tr_acc = _find_metric_key("acc")
    val_acc = _find_metric_key("acc", prefix="val_")
    if tr_acc and val_acc:
        axs[1, 0].plot(epochs_range, history_dict[tr_acc], label="Treino", color="#9467bd", linewidth=2)
        axs[1, 0].plot(epochs_range, history_dict[val_acc], label="Validação", color="#8c564b", linewidth=2, linestyle="--")
        axs[1, 0].set_title("Acurácia (ALF)", fontsize=12, fontweight="bold")
        axs[1, 0].set_xlabel("Época")
        axs[1, 0].set_ylabel("Acurácia")
        axs[1, 0].grid(True, linestyle=":", alpha=0.6)
        axs[1, 0].legend()

    # 4. Precisão e Recall de Validação
    val_prec = _find_metric_key("precision", prefix="val_")
    val_rec = _find_metric_key("recall", prefix="val_")
    if val_prec and val_rec:
        axs[1, 1].plot(epochs_range, history_dict[val_prec], label="Val Precisão", color="#8c564b", linewidth=2)
        axs[1, 1].plot(epochs_range, history_dict[val_rec], label="Val Recall", color="#e377c2", linewidth=2, linestyle="--")
        axs[1, 1].set_title("Precisão e Recall de Validação (ALF)", fontsize=12, fontweight="bold")
        axs[1, 1].set_xlabel("Época")
        axs[1, 1].set_ylabel("Score")
        axs[1, 1].grid(True, linestyle=":", alpha=0.6)
        axs[1, 1].legend()

    plt.tight_layout()
    plt.savefig(str(out_path), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[Reports] Curvas de treino salvas em: {out_path}")


# =============================================================================
# 2. MATRIZ DE CONFUSÃO (ABSOLUTA E NORMALIZADA - CSV & PNG)
# =============================================================================
def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    classes: List[str],
    output_dir: Union[str, Path],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Gera as matrizes de confusão absoluta e normalizada, salvando:
    - confusion_matrix.csv
    - confusion_matrix.png
    - confusion_matrix_normalized.csv
    - confusion_matrix_normalized.png
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(classes))))
    with np.errstate(divide="ignore", invalid="ignore"):
        row_sums = cm.sum(axis=1, keepdims=True)
        cm_norm = np.where(row_sums > 0, cm.astype(np.float64) / row_sums, 0.0)

    df_cm = pd.DataFrame(cm, index=classes, columns=classes)
    df_cm_norm = pd.DataFrame(np.round(cm_norm, 4), index=classes, columns=classes)

    df_cm.to_csv(out_dir / "confusion_matrix.csv")
    df_cm_norm.to_csv(out_dir / "confusion_matrix_normalized.csv")

    # 1. Plot com contagens absolutas (confusion_matrix.png)
    fig_raw, ax_raw = plt.subplots(figsize=(max(7, len(classes) * 1.1), max(6, len(classes) * 0.9)))
    im_raw = ax_raw.imshow(cm, cmap="Blues", interpolation="nearest")
    cbar_raw = ax_raw.figure.colorbar(im_raw, ax=ax_raw)
    cbar_raw.ax.set_ylabel("Contagem de Amostras", rotation=-90, va="bottom")

    ax_raw.set_xticks(np.arange(len(classes)))
    ax_raw.set_yticks(np.arange(len(classes)))
    ax_raw.set_xticklabels(classes, rotation=45, ha="right", fontsize=9, fontweight="bold")
    ax_raw.set_yticklabels(classes, fontsize=9, fontweight="bold")

    thresh_raw = cm.max() / 2.0 if cm.max() > 0 else 0.5
    for i in range(len(classes)):
        for j in range(len(classes)):
            val_c = cm[i, j]
            color_c = "white" if val_c > thresh_raw else "black"
            ax_raw.text(j, i, f"{val_c:,}", ha="center", va="center", color=color_c, fontsize=8)

    ax_raw.set_title("Matriz de Confusão Absoluta (ALF-MoE)", fontsize=12, fontweight="bold", pad=12)
    ax_raw.set_ylabel("Classe Verdadeira", fontsize=10, fontweight="bold")
    ax_raw.set_xlabel("Classe Predita", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_dir / "confusion_matrix.png", dpi=300, bbox_inches="tight")
    plt.close(fig_raw)

    # 2. Plot normalizado (confusion_matrix_normalized.png)
    fig_norm, ax_norm = plt.subplots(figsize=(max(7, len(classes) * 1.1), max(6, len(classes) * 0.9)))
    im_norm = ax_norm.imshow(cm_norm, cmap="Blues", interpolation="nearest", vmin=0.0, vmax=1.0)
    cbar_norm = ax_norm.figure.colorbar(im_norm, ax=ax_norm)
    cbar_norm.ax.set_ylabel("Fração Normalizada", rotation=-90, va="bottom")

    ax_norm.set_xticks(np.arange(len(classes)))
    ax_norm.set_yticks(np.arange(len(classes)))
    ax_norm.set_xticklabels(classes, rotation=45, ha="right", fontsize=9, fontweight="bold")
    ax_norm.set_yticklabels(classes, fontsize=9, fontweight="bold")

    thresh_norm = 0.5
    for i in range(len(classes)):
        for j in range(len(classes)):
            val = cm_norm[i, j]
            count = cm[i, j]
            txt = f"{val:.2f}\n({count:,})" if count > 0 else "0.00"
            color = "white" if val > thresh_norm else "black"
            ax_norm.text(j, i, txt, ha="center", va="center", color=color, fontsize=8)

    ax_norm.set_title("Matriz de Confusão Normalizada (ALF-MoE)", fontsize=12, fontweight="bold", pad=12)
    ax_norm.set_ylabel("Classe Verdadeira", fontsize=10, fontweight="bold")
    ax_norm.set_xlabel("Classe Predita", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(out_dir / "confusion_matrix_normalized.png", dpi=300, bbox_inches="tight")
    plt.close(fig_norm)

    print(f"[Reports] Matrizes de confusão salvas em: {out_dir}")
    return df_cm, df_cm_norm


# =============================================================================
# 3. HEATMAP DE ATENÇÃO DA GATING NETWORK (CSV & PNG)
# =============================================================================
def plot_gating_attention_heatmap(
    y_true: np.ndarray,
    gn_weights: np.ndarray,
    classes: List[str],
    output_path: Union[str, Path],
) -> pd.DataFrame:
    """
    Gera o heatmap de atenção demonstrando a distribuição dos pesos a_1..a_5
    para cada classe de tráfego, evidenciando analiticamente a especialização dos especialistas.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
    num_classes = len(classes)
    avg_weights = np.zeros((num_classes, 5), dtype=np.float32)

    for c in range(num_classes):
        mask = (y_true == c)
        if np.any(mask):
            avg_weights[c, :] = np.mean(gn_weights[mask], axis=0)
        else:
            avg_weights[c, :] = 0.2

    df_attn = pd.DataFrame(avg_weights, index=classes, columns=expert_names)
    csv_path = out_path.with_suffix(".csv")
    df_attn.to_csv(csv_path)

    fig, ax = plt.subplots(figsize=(8, max(5, num_classes * 0.6)))
    im = ax.imshow(avg_weights, cmap="Purples", aspect="auto", vmin=0.0, vmax=max(0.4, float(avg_weights.max())))
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Peso Médio de Atenção", rotation=-90, va="bottom")

    ax.set_xticks(np.arange(5))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(expert_names, fontsize=11, fontweight="bold")
    ax.set_yticklabels(classes, fontsize=10, fontweight="bold")

    thresh = avg_weights.max() / 2.0
    for i in range(num_classes):
        for j in range(5):
            val = avg_weights[i, j]
            color = "white" if val > thresh else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=10, fontweight="bold")

    ax.set_title("Gating Network: Distribuição de Atenção por Classe de Ataque", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Classe de Tráfego / Ameaça", fontsize=10, fontweight="bold")
    ax.set_xlabel("Especialista Neural", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(str(out_path.with_suffix(".png")), dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"[Reports] Heatmap de atenção da Gating Network salvo em: {out_path.with_suffix('.png')}")
    return df_attn


# =============================================================================
# 4. BOXPLOT DA GATING NETWORK POR CLASSE (PNG)
# =============================================================================
def plot_gating_weights_boxplot(
    y_true: np.ndarray,
    gn_weights: np.ndarray,
    classes: List[str],
    output_path: Union[str, Path],
) -> None:
    """
    Gera o boxplot da distribuição de pesos atencionais da Gating Network
    (DNN, CNN, GRU, CAE, LSTM) por classe de tráfego, demonstrando dispersão e quartis.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
    num_classes = len(classes)
    cols = min(4, num_classes)
    rows = int(np.ceil(num_classes / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.8, rows * 3.5), sharey=True)
    if num_classes == 1:
        axes = np.array([axes])
    axes = np.ravel(axes)

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for c in range(num_classes):
        ax = axes[c]
        mask = (y_true == c)
        if np.any(mask):
            data_c = [gn_weights[mask, j] for j in range(5)]
        else:
            data_c = [np.array([0.2]) for _ in range(5)]

        bp = ax.boxplot(
            data_c,
            patch_artist=True,
            tick_labels=expert_names,
            medianprops=dict(color="black", linewidth=1.5),
            widths=0.6,
        )
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        n_samples = int(np.sum(mask))
        ax.set_title(f"{classes[c]}\n(N={n_samples:,})", fontsize=10, fontweight="bold")
        ax.set_ylim(-0.02, 1.02)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.tick_params(axis="x", labelsize=8)

    # Oculta eixos vazios excedentes se houver
    for k in range(num_classes, len(axes)):
        axes[k].axis("off")

    fig.suptitle(
        "Distribuição dos Pesos da Gating Network por Classe de Tráfego",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(str(out_path.with_suffix(".png")), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[Reports] Boxplot de pesos do Gating salvo em: {out_path.with_suffix('.png')}")


# =============================================================================
# 5. HEATMAP COMPARATIVO: ESPECIALISTAS VS ALF-MoE (F1, ACCURACY, PRECISION, RECALL)
# =============================================================================
def plot_expert_comparison_heatmap(
    y_true: np.ndarray,
    preds_dict: Dict[str, np.ndarray],
    classes: List[str],
    output_path: Union[str, Path],
    metric: Literal["f1", "balanced_accuracy", "accuracy", "precision", "recall"] = "f1",
) -> pd.DataFrame:
    """
    Compara o desempenho individual de cada um dos 5 especialistas contra a fusão ALF-MoE.
    Suporta métricas: 'f1', 'balanced_accuracy', 'precision', 'recall'.
    Salva tanto o arquivo .csv quanto .png.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    models_order = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF"]
    display_names = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF-MoE"]
    num_classes = len(classes)
    scores = np.zeros((num_classes, len(models_order)), dtype=np.float32)

    metric_clean = str(metric).lower().strip()
    metric_labels = {
        "f1": "F1-Score",
        "balanced_accuracy": "Acurácia Balanceada",
        "balanced_acc": "Acurácia Balanceada",
        "accuracy": "Acurácia Balanceada",
        "acc": "Acurácia Balanceada",
        "precision": "Precisão",
        "recall": "Recall",
    }
    metric_label = metric_labels.get(metric_clean, metric_clean.capitalize())

    for j, m in enumerate(models_order):
        if m in preds_dict:
            raw_p = preds_dict[m]
            y_pred_m = np.argmax(raw_p, axis=-1) if raw_p.ndim > 1 else raw_p
            p, r, f1, _ = precision_recall_fscore_support(
                y_true, y_pred_m, labels=list(range(num_classes)), zero_division=0
            )
            if metric_clean == "f1":
                scores[:, j] = f1
            elif metric_clean == "precision":
                scores[:, j] = p
            elif metric_clean == "recall":
                scores[:, j] = r
            elif metric_clean in ("balanced_accuracy", "balanced_acc", "accuracy", "acc"):
                for c in range(num_classes):
                    scores[c, j] = balanced_accuracy_score(y_true == c, y_pred_m == c) if len(y_true) > 0 else 0.0

    df_comp = pd.DataFrame(scores, index=classes, columns=display_names)
    df_comp.to_csv(out_path.with_suffix(".csv"))

    fig, ax = plt.subplots(figsize=(9, max(5, num_classes * 0.6)))
    im = ax.imshow(scores, cmap="YlGnBu", aspect="auto", vmin=0.0, vmax=1.0)
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(f"Escore {metric_label}", rotation=-90, va="bottom")

    ax.set_xticks(np.arange(len(display_names)))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(display_names, fontsize=10, fontweight="bold")
    ax.set_yticklabels(classes, fontsize=10, fontweight="bold")

    thresh = 0.5
    for i in range(num_classes):
        for j in range(len(display_names)):
            val = scores[i, j]
            color = "white" if val > thresh else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=9, fontweight="bold")

    ax.set_title(f"Comparativo por Classe: Especialistas vs ALF-MoE ({metric_label})", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Classe de Tráfego / Ameaça", fontsize=10, fontweight="bold")
    ax.set_xlabel("Modelo Neural", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(str(out_path.with_suffix(".png")), dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"[Reports] Heatmap comparativo ({metric_label}) salvo em: {out_path.with_suffix('.png')}")
    return df_comp


# =============================================================================
# 6. HEATMAP DE MÉTRICAS EXCLUSIVAS DO ALF-MoE (CSV & PNG)
# =============================================================================
def plot_alf_metrics_heatmap(
    y_true: np.ndarray,
    y_pred_alf: np.ndarray,
    classes: List[str],
    output_path: Union[str, Path],
) -> pd.DataFrame:
    """
    Plota as 3 métricas cardinais de classificação (Precisão, Recall e F1-Score)
    por classe para o modelo consolidado ALF-MoE.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    y_pred = np.argmax(y_pred_alf, axis=-1) if y_pred_alf.ndim > 1 else y_pred_alf
    num_classes = len(classes)

    p, r, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=list(range(num_classes)), zero_division=0
    )
    scores = np.column_stack([p, r, f1]).astype(np.float32)
    cols = ["Precisão", "Recall", "F1-Score"]

    df_alf = pd.DataFrame(scores, index=classes, columns=cols)
    df_alf.to_csv(out_path.with_suffix(".csv"))

    fig, ax = plt.subplots(figsize=(7, max(5, num_classes * 0.6)))
    im = ax.imshow(scores, cmap="YlGnBu", aspect="auto", vmin=0.0, vmax=1.0)
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Score", rotation=-90, va="bottom")

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(cols, fontsize=11, fontweight="bold")
    ax.set_yticklabels(classes, fontsize=10, fontweight="bold")

    thresh = 0.5
    for i in range(num_classes):
        for j in range(3):
            val = scores[i, j]
            color = "white" if val > thresh else "black"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=color, fontsize=10, fontweight="bold")

    ax.set_title("Métricas de Classificação do ALF-MoE por Classe", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Classe de Tráfego / Ameaça", fontsize=10, fontweight="bold")
    ax.set_xlabel("Métrica", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(str(out_path.with_suffix(".png")), dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"[Reports] Heatmap de métricas do ALF salvo em: {out_path.with_suffix('.png')}")
    return df_alf


# =============================================================================
# 7. RADAR CHART COMPARATIVO GLOBAL (PNG)
# =============================================================================
def plot_expert_radar_chart(
    y_true: np.ndarray,
    preds_dict: Dict[str, np.ndarray],
    classes: List[str],
    output_path: Union[str, Path],
) -> None:
    """
    Gera o Radar Chart comparativo global dos 5 especialistas + fusão ALF-MoE.
    Utiliza o F1-Score por classe como eixos polares radiais.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    models_order = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF"]
    display_names = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF-MoE"]
    model_colors = {
        "DNN": "#1f77b4",
        "CNN": "#ff7f0e",
        "GRU": "#2ca02c",
        "CAE": "#9467bd",
        "LSTM": "#8c564b",
        "ALF-MoE": "#d62728",
    }
    num_classes = len(classes)

    # Computa F1 por classe para cada modelo
    scores = {}
    for m, disp in zip(models_order, display_names):
        if m in preds_dict:
            raw_p = preds_dict[m]
            y_pred_m = np.argmax(raw_p, axis=-1) if raw_p.ndim > 1 else raw_p
            _, _, f1, _ = precision_recall_fscore_support(
                y_true, y_pred_m, labels=list(range(num_classes)), zero_division=0
            )
            scores[disp] = f1
        else:
            scores[disp] = np.zeros(num_classes, dtype=np.float32)

    angles = np.linspace(0, 2 * np.pi, num_classes, endpoint=False).tolist()
    angles += angles[:1]  # Fecha o círculo

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plota os 5 especialistas com linhas secundárias
    for disp in display_names[:-1]:
        vals = scores[disp].tolist()
        vals += vals[:1]
        ax.plot(
            angles,
            vals,
            label=disp,
            color=model_colors[disp],
            linewidth=1.5,
            linestyle="--",
            alpha=0.75,
        )

    # Plota ALF-MoE com linha destacada e preenchimento
    alf_vals = scores["ALF-MoE"].tolist()
    alf_vals += alf_vals[:1]
    ax.plot(
        angles,
        alf_vals,
        label="ALF-MoE",
        color=model_colors["ALF-MoE"],
        linewidth=2.8,
        linestyle="-",
        marker="o",
        markersize=5,
    )
    ax.fill(angles, alf_vals, color=model_colors["ALF-MoE"], alpha=0.15)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(classes, fontsize=9, fontweight="bold")
    ax.set_ylim(0.0, 1.05)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8, color="gray")
    ax.grid(True, linestyle=":", alpha=0.7)

    ax.set_title(
        "Comparativo Global: 5 Especialistas vs ALF-MoE\n(F1-Score por Classe)",
        fontsize=12,
        fontweight="bold",
        pad=20,
    )
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.1),
        fontsize=9,
        frameon=True,
    )

    plt.tight_layout()
    plt.savefig(str(out_path.with_suffix(".png")), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[Reports] Radar Chart de especialistas salvo em: {out_path.with_suffix('.png')}")


# =============================================================================
# 8. RELATÓRIOS ESTRUTURADOS (JSON e TXT)
# =============================================================================
def generate_training_report(
    history_dict: Dict[str, List[float]],
    train_time_sec: float,
    num_samples: int,
    output_dir: Union[str, Path],
) -> Dict[str, Any]:
    """Gera resumo de treinamento em JSON e TXT e persiste histórico JSON."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    val_f1_key = [k for k in history_dict if "val" in k and "f1" in k.lower()]
    val_loss_key = [k for k in history_dict if "val" in k and "loss" in k.lower()]

    best_val_f1 = float(max(history_dict[val_f1_key[0]])) if val_f1_key else 0.0
    best_epoch = int(np.argmax(history_dict[val_f1_key[0]])) + 1 if val_f1_key else 0
    final_loss = float(history_dict[val_loss_key[0]][-1]) if val_loss_key else 0.0

    # Persiste training_history.json
    try:
        clean_hist = {k: [float(v) for v in vals] for k, vals in history_dict.items()}
        with open(out_dir / "training_history.json", "w", encoding="utf-8") as f:
            json.dump(clean_hist, f, indent=2)
    except Exception as exc:
        print(f"[Aviso] Falha ao salvar training_history.json: {exc}")

    report = {
        "timestamp": datetime.now().isoformat() + "Z",
        "train_time_sec": round(train_time_sec, 2),
        "num_train_samples": int(num_samples),
        "throughput_samples_per_sec": round(num_samples / max(train_time_sec, 1e-4), 2),
        "total_epochs": len(list(history_dict.values())[0]) if history_dict else 0,
        "best_epoch": best_epoch,
        "best_val_f1_macro": round(best_val_f1, 4),
        "final_val_loss": round(final_loss, 4),
    }

    # Salva training_report.json
    with open(out_dir / "training_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Salva training_report.txt
    txt_lines = [
        "=" * 60,
        "       RELATÓRIO DE TREINAMENTO - MODELO ALF-MoE",
        "=" * 60,
        f"Data/Hora:                     {report['timestamp']}",
        f"Amostras de Treino:            {report['num_train_samples']:,}",
        f"Tempo Total de Treino:         {report['train_time_sec']} segundos",
        f"Vazão de Processamento:        {report['throughput_samples_per_sec']:,} amostras/s",
        f"Épocas Executadas:             {report['total_epochs']}",
        f"Melhor Época:                  {report['best_epoch']}",
        f"Melhor Val F1-Score (Macro):   {report['best_val_f1_macro']:.4f}",
        f"Final Val Loss:                {report['final_val_loss']:.4f}",
        "=" * 60,
    ]
    with open(out_dir / "training_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines) + "\n")

    return report


def generate_test_report(
    y_true: np.ndarray,
    preds_dict: Dict[str, np.ndarray],
    classes: List[str],
    inference_time_sec: float,
    num_samples: int,
    output_dir: Union[str, Path],
) -> Dict[str, Any]:
    """
    Gera avaliação abrangente de teste:
    - Salva classification_report.csv
    - Coleta métricas de Acurácia, F1, Precisão e Recall por classe para CADA especialista e ALF
    - Salva test_report.json e test_report.txt
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    y_pred_alf = np.argmax(preds_dict["ALF"], axis=-1) if preds_dict["ALF"].ndim > 1 else preds_dict["ALF"]

    acc = float(accuracy_score(y_true, y_pred_alf))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred_alf, average="macro", zero_division=0)
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(y_true, y_pred_alf, average="weighted", zero_division=0)

    latency_ms = (inference_time_sec / max(num_samples, 1)) * 1000.0
    throughput = float(num_samples) / max(inference_time_sec, 1e-4)

    # Classification Report completo exportado para CSV
    clf_dict = classification_report(y_true, y_pred_alf, target_names=classes, output_dict=True, zero_division=0)
    df_clf = pd.DataFrame(clf_dict).transpose()
    df_clf.to_csv(out_dir / "classification_report.csv")

    # Avaliação individual de cada especialista (DNN, CNN, GRU, CAE, LSTM)
    experts_eval: Dict[str, Any] = {}
    for m in ["DNN", "CNN", "GRU", "CAE", "LSTM"]:
        if m in preds_dict:
            y_m = np.argmax(preds_dict[m], axis=-1) if preds_dict[m].ndim > 1 else preds_dict[m]
            p_m, r_m, f1_m, _ = precision_recall_fscore_support(y_true, y_m, average="macro", zero_division=0)
            acc_m = accuracy_score(y_true, y_m)
            p_cls, r_cls, f1_cls, supp_cls = precision_recall_fscore_support(
                y_true, y_m, labels=list(range(len(classes))), zero_division=0
            )
            experts_eval[m] = {
                "accuracy": round(float(acc_m), 4),
                "macro_f1": round(float(f1_m), 4),
                "macro_precision": round(float(p_m), 4),
                "macro_recall": round(float(r_m), 4),
                "per_class": {
                    cls_name: {
                        "balanced_accuracy": round(float(balanced_accuracy_score(y_true == idx, y_m == idx)), 4),
                        "precision": round(float(p_cls[idx]), 4),
                        "recall": round(float(r_cls[idx]), 4),
                        "f1_score": round(float(f1_cls[idx]), 4),
                        "support": int(supp_cls[idx]),
                    }
                    for idx, cls_name in enumerate(classes)
                },
            }

    # Desmembramento por classe do modelo ALF-MoE
    alf_per_class = {
        cls_name: {
            "balanced_accuracy": round(float(balanced_accuracy_score(y_true == idx, y_pred_alf == idx)), 4),
            "precision": round(float(clf_dict[cls_name]["precision"]), 4),
            "recall": round(float(clf_dict[cls_name]["recall"]), 4),
            "f1_score": round(float(clf_dict[cls_name]["f1-score"]), 4),
            "support": int(clf_dict[cls_name]["support"]),
        }
        for idx, cls_name in enumerate(classes) if cls_name in clf_dict
    }

    report = {
        "timestamp": datetime.now().isoformat() + "Z",
        "num_test_samples": int(num_samples),
        "inference_time_sec": round(inference_time_sec, 4),
        "latency_ms_per_sample": round(latency_ms, 4),
        "throughput_samples_per_sec": round(throughput, 2),
        "alf_moe_metrics": {
            "accuracy": round(acc, 4),
            "macro_f1": round(float(f1_macro), 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "weighted_precision": round(float(p_weighted), 4),
            "weighted_recall": round(float(r_weighted), 4),
        },
        "alf_per_class_breakdown": alf_per_class,
        "experts_metrics": experts_eval,
    }

    # Salva test_report.json
    with open(out_dir / "test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Salva test_report.txt legível
    txt_lines = [
        "=" * 75,
        "           RELATÓRIO DE AVALIAÇÃO DE TESTE - MODELO ALF-MoE",
        "=" * 75,
        f"Data/Hora:                     {report['timestamp']}",
        f"Total de Amostras de Teste:    {report['num_test_samples']:,}",
        f"Tempo de Inferência:           {report['inference_time_sec']:.4f} s",
        f"Latência por Amostra:          {report['latency_ms_per_sample']:.4f} ms/fluxo",
        f"Vazão de Inferência:           {report['throughput_samples_per_sec']:,.2f} fluxos/s",
        "-" * 75,
        "DESEMPENHO GLOBAL DO MODELO ALF-MoE:",
        f"  Acurácia:                    {acc * 100:.2f}%",
        f"  Macro F1-Score:              {f1_macro:.4f}",
        f"  Macro Precisão:              {p_macro:.4f}",
        f"  Macro Recall:                {r_macro:.4f}",
        f"  Weighted F1-Score:           {f1_weighted:.4f}",
        "-" * 75,
        "DESEMPENHO INDIVIDUAL DOS ESPECIALISTAS VS ALF-MoE:",
    ]
    for m in ["DNN", "CNN", "GRU", "CAE", "LSTM"]:
        if m in experts_eval:
            e_m = experts_eval[m]
            txt_lines.append(
                f"  {m:<8} F1: {e_m['macro_f1']:.4f} | Acc: {e_m['accuracy'] * 100:.2f}% | Prec: {e_m['macro_precision']:.4f} | Rec: {e_m['macro_recall']:.4f}"
            )
    txt_lines.append(
        f"  {'ALF-MoE':<8} F1: {f1_macro:.4f} | Acc: {acc * 100:.2f}% | Prec: {p_macro:.4f} | Rec: {r_macro:.4f}"
    )

    txt_lines.extend([
        "-" * 79,
        f"{'Classe de Ameaça':<22} {'Acurácia Bal.':<14} {'Precisão':<10} {'Recall':<10} {'F1-Score':<10} {'Suporte':<10}",
        "-" * 79,
    ])
    for cls_name, vals in alf_per_class.items():
        txt_lines.append(
            f"{cls_name:<22} {vals['balanced_accuracy']:<14.4f} {vals['precision']:<10.4f} {vals['recall']:<10.4f} {vals['f1_score']:<10.4f} {vals['support']:<10,}"
        )
    txt_lines.append("=" * 79)

    with open(out_dir / "test_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines) + "\n")

    return report
