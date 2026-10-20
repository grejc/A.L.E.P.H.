#!/usr/bin/env python3
"""
Gera dois gráficos de barras em PDF vetorial (e PNG 300 DPI) com o desempenho
do modelo ALF-MoE na partição de teste dos 4 datasets de benchmark:
1. Cenário Granular (TL0 - Classes brutas / Assinaturas estritas)
2. Cenário Consolidado (TL1 - Macro-categorias / Famílias funcionais)

Métricas exibidas:
- Acurácia Global
- Macro F1-Score
- F1-Score Ponderada (Weighted F1)
- Macro Precisão
- Macro Recall

Fonte dos dados: Relatórios de avaliação de teste (test_report.json) em artifacts/.
Salva em:
- UndergraduateThesis/figures/benchmarks/
- artifacts/reports/
"""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Configurações visuais elegantes para publicação acadêmica
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 13.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 11.5,
    "axes.labelweight": "bold",
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "legend.fontsize": 10,
    "figure.titlesize": 14.5,
    "figure.titleweight": "bold",
})

# Paleta harmônica para as 5 métricas
METRIC_COLORS = {
    "Acurácia Global": "#1f77b4",       # Azul institucional
    "Macro F1-Score": "#d62728",        # Vermelho carmim
    "F1-Score Ponderada": "#9467bd",    # Roxo suave
    "Macro Precisão": "#2ca02c",        # Verde esmeralda
    "Macro Recall": "#ff7f0e",          # Laranja âmbar
}

METRIC_KEYS = [
    ("Acurácia Global", "accuracy"),
    ("Macro F1-Score", "macro_f1"),
    ("F1-Score Ponderada", "weighted_f1"),
    ("Macro Precisão", "macro_precision"),
    ("Macro Recall", "macro_recall"),
]

# Configurações dos 4 Datasets para cada gráfico
CONFIG_TL0 = [
    {
        "id": "unsw_tl0",
        "name": "CIC-UNSW-NB15\n(TL0 - 10 cls)",
        "report_path": "artifacts/CIC-UNSW-NB15/2026-10-19_03:50:51/reports/test_report.json",
    },
    {
        "id": "bccc_tl0",
        "name": "CIC-BCCC-NRC-2024\n(TL0 - 49 cls)",
        "report_path": "artifacts/CIC-BCCC-NRC-2024/2026-10-19_04:04:13/reports/test_report.json",
    },
    {
        "id": "cse_orig_tl0",
        "name": "CSE-CIC-IDS2018 Canônico\n(TL0 - 15 cls)",
        "report_path": "artifacts/CSE-CIC-IDS2018/2026-10-19_10:31:58/reports/test_report.json",
    },
    {
        "id": "cse_imp_tl0",
        "name": "CSE-CIC-IDS2018 Corrigido\n(TL0 - 15 cls)",
        "report_path": "artifacts/CSECICIDS2018_improved/2026-10-19_03:44:14/reports/test_report.json",
    },
]

CONFIG_TL1 = [
    {
        "id": "unsw_tl1_ref",
        "name": "CIC-UNSW-NB15\n(Ref. 10 cls)",
        "report_path": "artifacts/CIC-UNSW-NB15/2026-10-19_03:50:51/reports/test_report.json",
    },
    {
        "id": "bccc_tl1",
        "name": "CIC-BCCC-NRC-2024\n(TL1 - 9 cls)",
        "report_path": "artifacts/CIC-BCCC-NRC-2024/2026-10-19_04:57:09/reports/test_report.json",
    },
    {
        "id": "cse_orig_tl1",
        "name": "CSE-CIC-IDS2018 Canônico\n(TL1 - 7 cls)",
        "report_path": "artifacts/CSE-CIC-IDS2018/2026-10-19_11:34:08/reports/test_report.json",
    },
    {
        "id": "cse_imp_tl1",
        "name": "CSE-CIC-IDS2018 Corrigido\n(TL1 - 9 cls)",
        "report_path": "artifacts/CSECICIDS2018_improved/2026-10-19_03:28:34/reports/test_report.json",
    },
]


def load_dataset_metrics(base_dir: Path, config_list: list) -> list:
    results = []
    for item in config_list:
        file_path = base_dir / item["report_path"]
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        metrics = data.get("alf_moe_metrics", {})
        results.append({
            "name": item["name"],
            "metrics": {
                label: float(metrics.get(k, 0.0)) * 100.0
                for label, k in METRIC_KEYS
            }
        })
    return results


def plot_grouped_bar_chart(data: list, title: str, output_paths: list):
    n_datasets = len(data)
    n_metrics = len(METRIC_KEYS)

    x = np.arange(n_datasets)
    total_cluster_width = 0.78
    bar_width = total_cluster_width / n_metrics
    offsets = np.linspace(
        -(total_cluster_width - bar_width) / 2,
        (total_cluster_width - bar_width) / 2,
        n_metrics
    )

    fig, ax = plt.subplots(figsize=(13.5, 7.2))

    for i, (label, _) in enumerate(METRIC_KEYS):
        values = [d["metrics"][label] for d in data]
        color = METRIC_COLORS[label]
        rects = ax.bar(
            x + offsets[i],
            values,
            bar_width,
            label=label,
            color=color,
            edgecolor="#222222",
            linewidth=0.7,
            alpha=0.92,
            zorder=3
        )

        for rect in rects:
            height = rect.get_height()
            label_text = f"{height:.1f}%".replace(".", ",")
            ax.annotate(
                label_text,
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.2,
                rotation=90,
                fontweight="bold",
                color="#111111",
            )

    ax.set_ylabel("Desempenho na Avaliação de Teste (%)", labelpad=10)
    ax.set_title(title, pad=18)
    ax.set_xticks(x)
    ax.set_xticklabels([d["name"] for d in data], fontweight="bold")
    ax.set_ylim(0.0, 118.0)
    ax.set_yticks(np.arange(0, 101, 10))
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())
    
    # Grid sutil
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=0)
    ax.set_axisbelow(True)

    # Linha de 100% de referência
    ax.axhline(100.0, color="#777777", linestyle=":", linewidth=1.0, alpha=0.75, zorder=1)

    # Legenda em 1 linha no topo
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=5,
        framealpha=0.95,
        edgecolor="#cccccc",
        facecolor="#ffffff"
    )

    plt.tight_layout()

    for p in output_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".pdf":
            plt.savefig(p, bbox_inches="tight")
        else:
            plt.savefig(p, dpi=300, bbox_inches="tight")
        print(f"[OK] Gráfico salvo em: {p}")

    plt.close(fig)


def main():
    base_dir = Path(__file__).resolve().parent.parent
    thesis_dir = base_dir / "UndergraduateThesis" / "figures" / "benchmarks"
    artifacts_dir = base_dir / "artifacts" / "reports"

    # Carregar dados
    data_tl0 = load_dataset_metrics(base_dir, CONFIG_TL0)
    data_tl1 = load_dataset_metrics(base_dir, CONFIG_TL1)

    # 1. Gráfico TL0
    plot_grouped_bar_chart(
        data=data_tl0,
        title="Desempenho do Modelo ALF-MoE nos 4 Datasets de Benchmark\nCenário Granular (TL0 - Classes Brutas / Assinaturas Estritas)",
        output_paths=[
            thesis_dir / "comparativo_metricas_4datasets_tl0.pdf",
            thesis_dir / "comparativo_metricas_4datasets_tl0.png",
            artifacts_dir / "comparativo_metricas_4datasets_tl0.pdf",
            artifacts_dir / "comparativo_metricas_4datasets_tl0.png",
        ]
    )

    # 2. Gráfico TL1
    plot_grouped_bar_chart(
        data=data_tl1,
        title="Desempenho do Modelo ALF-MoE nos 4 Datasets de Benchmark\nCenário Consolidado (TL1 - Macro-Categorias / Famílias Funcionais)",
        output_paths=[
            thesis_dir / "comparativo_metricas_4datasets_tl1.pdf",
            thesis_dir / "comparativo_metricas_4datasets_tl1.png",
            artifacts_dir / "comparativo_metricas_4datasets_tl1.pdf",
            artifacts_dir / "comparativo_metricas_4datasets_tl1.png",
        ]
    )


if __name__ == "__main__":
    main()
