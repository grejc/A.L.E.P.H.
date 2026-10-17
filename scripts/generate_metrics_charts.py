#!/usr/bin/env python3
"""
Geração de gráficos comparativos das métricas:
- Acurácia Global
- Macro Precisão
- Macro Sensibilidade (Recall)
- Macro F1-Score

Extrai dados diretamente dos relatórios de teste (test_report.json) disponíveis em artifacts/.
Gera figuras em PNG (300 DPI) e PDF vetorial para teses/artigos.
"""

import json
import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configuração de estilo visual refinado
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.titleweight": "bold",
})

# Paleta harmônica para as 4 métricas
METRIC_COLORS = {
    "Acurácia Global": "#1f77b4",       # Azul corporativo
    "Macro Precisão": "#2ca02c",        # Verde
    "Macro Sensibilidade": "#ff7f0e",   # Laranja
    "Macro F1-Score": "#d62728",        # Vermelho carmim
}

# Mapeamento canônico dos 7 cenários experimentais
SCENARIOS = [
    {
        "id": "unsw_l0",
        "dataset_dir": "CIC-UNSW-NB15",
        "run_id": "2026-09-27_20:19:01",
        "name": "CIC-UNSW-NB15\n(L0 - 10 cls)",
        "short_name": "UNSW-NB15 (L0)",
    },
    {
        "id": "bccc_l0",
        "dataset_dir": "CIC-BCCC-NRC-2024",
        "run_id": "2026-09-27_21:38:11",
        "name": "CIC-BCCC-NRC-2024\n(L0 - 49 cls)",
        "short_name": "BCCC-NRC (L0)",
    },
    {
        "id": "bccc_l2",
        "dataset_dir": "CIC-BCCC-NRC-2024",
        "run_id": "2026-09-27_22:14:39",
        "name": "CIC-BCCC-NRC-2024\n(L2 - 9 cls)",
        "short_name": "BCCC-NRC (L2)",
    },
    {
        "id": "cse_orig_l0",
        "dataset_dir": "CSE-CIC-IDS2018",
        "run_id": "2026-09-27_20:21:21",
        "name": "CSE-CIC-IDS2018 Orig.\n(L0 - 15 cls)",
        "short_name": "CSE-2018 Orig. (L0)",
    },
    {
        "id": "cse_orig_l2",
        "dataset_dir": "CSE-CIC-IDS2018",
        "run_id": "2026-09-27_21:09:15",
        "name": "CSE-CIC-IDS2018 Orig.\n(L2 - 7 cls)",
        "short_name": "CSE-2018 Orig. (L2)",
    },
    {
        "id": "cse_imp_l0",
        "dataset_dir": "CSECICIDS2018_improved",
        "run_id": "2026-09-27_22:58:17",
        "name": "CSE-CIC-IDS2018 Corr.\n(L0 - 15 cls)",
        "short_name": "CSE-2018 Corr. (L0)",
    },
    {
        "id": "cse_imp_l2",
        "dataset_dir": "CSECICIDS2018_improved",
        "run_id": "2026-09-28_00:19:51",
        "name": "CSE-CIC-IDS2018 Corr.\n(L2 - 9 cls)",
        "short_name": "CSE-2018 Corr. (L2)",
    },
]


def load_scenario_data(base_path: Path):
    """Carrega dados dos 7 cenários a partir dos arquivos test_report.json."""
    records = []
    experts_data = {}

    for sc in SCENARIOS:
        report_file = base_path / "artifacts" / sc["dataset_dir"] / sc["run_id"] / "reports" / "test_report.json"
        if not report_file.exists():
            print(f"[Aviso] Arquivo não encontrado: {report_file}")
            continue

        with open(report_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        m = data.get("alf_moe_metrics", {})
        records.append({
            "id": sc["id"],
            "name": sc["name"],
            "short_name": sc["short_name"],
            "Acurácia Global": float(m.get("accuracy", 0.0)),
            "Macro Precisão": float(m.get("macro_precision", 0.0)),
            "Macro Sensibilidade": float(m.get("macro_recall", 0.0)),
            "Macro F1-Score": float(m.get("macro_f1", 0.0)),
        })

        experts_data[sc["id"]] = {
            "alf": m,
            "experts": data.get("experts_metrics", {}),
        }

    return pd.DataFrame(records), experts_data


def plot_alf_moe_scenarios_chart(df: pd.DataFrame, output_dir: Path):
    """Gera gráfico de barras agrupadas comparando os 7 cenários para o ALF-MoE."""
    metrics = ["Acurácia Global", "Macro Precisão", "Macro Sensibilidade", "Macro F1-Score"]
    n_scenarios = len(df)
    n_metrics = len(metrics)

    # Configuração de barras agrupadas
    x = np.arange(n_scenarios)
    bar_width = 0.18
    offsets = np.linspace(-(n_metrics - 1) / 2 * bar_width, (n_metrics - 1) / 2 * bar_width, n_metrics)

    fig, ax = plt.subplots(figsize=(15, 7.5))

    for i, metric in enumerate(metrics):
        values = df[metric].values
        color = METRIC_COLORS[metric]
        rects = ax.bar(
            x + offsets[i],
            values,
            bar_width,
            label=metric,
            color=color,
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9,
        )

        # Rótulos de porcentagem/valor sobre as barras
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:.2f}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
                fontweight="semibold",
            )

    ax.set_ylabel("Escore / Taxa (0.0 a 1.0)")
    ax.set_title("Desempenho Global do ALF-MoE nos 7 Cenários de Benchmark\n(Acurácia Global, Macro Precisão, Macro Sensibilidade e Macro F1-Score)", pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(df["name"].values, fontweight="bold")
    ax.set_ylim(0.0, 1.15)
    ax.set_yticks(np.arange(0.0, 1.01, 0.1))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", ncol=4, framealpha=0.95, edgecolor="gray")

    # Linha de referência em 1.0
    ax.axhline(1.0, color="gray", linestyle=":", linewidth=0.8, alpha=0.7)

    plt.tight_layout()

    png_path = output_dir / "grafico_metricas_cenarios_alf_moe.png"
    pdf_path = output_dir / "grafico_metricas_cenarios_alf_moe.pdf"
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Gráfico salvo em:\n  - {png_path}\n  - {pdf_path}")
    return png_path, pdf_path


def plot_experts_vs_alf_chart(experts_data: dict, output_dir: Path, target_scenario_id="cse_imp_l2"):
    """Gera gráfico comparativo entre os 5 especialistas e o ALF-MoE no cenário corrigido."""
    sc_data = experts_data.get(target_scenario_id, {})
    experts = sc_data.get("experts", {})
    alf = sc_data.get("alf", {})

    models = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF-MoE (Proposto)"]
    metrics = ["Acurácia Global", "Macro Precisão", "Macro Sensibilidade", "Macro F1-Score"]

    records = []
    for m in ["DNN", "CNN", "GRU", "CAE", "LSTM"]:
        exp_m = experts.get(m, {})
        records.append({
            "Modelo": m,
            "Acurácia Global": exp_m.get("accuracy", 0.0),
            "Macro Precisão": exp_m.get("macro_precision", 0.0),
            "Macro Sensibilidade": exp_m.get("macro_recall", 0.0),
            "Macro F1-Score": exp_m.get("macro_f1", 0.0),
        })

    records.append({
        "Modelo": "ALF-MoE (Proposto)",
        "Acurácia Global": alf.get("accuracy", 0.0),
        "Macro Precisão": alf.get("macro_precision", 0.0),
        "Macro Sensibilidade": alf.get("macro_recall", 0.0),
        "Macro F1-Score": alf.get("macro_f1", 0.0),
    })

    df_models = pd.DataFrame(records)

    n_models = len(models)
    n_metrics = len(metrics)
    x = np.arange(n_models)
    bar_width = 0.18
    offsets = np.linspace(-(n_metrics - 1) / 2 * bar_width, (n_metrics - 1) / 2 * bar_width, n_metrics)

    fig, ax = plt.subplots(figsize=(13, 7))

    for i, metric in enumerate(metrics):
        values = df_models[metric].values
        color = METRIC_COLORS[metric]
        rects = ax.bar(
            x + offsets[i],
            values,
            bar_width,
            label=metric,
            color=color,
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9,
        )

        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:.2f}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
                fontweight="semibold",
            )

    ax.set_ylabel("Escore / Taxa (0.0 a 1.0)")
    ax.set_title("Estudo de Ablação: Especialistas Neurais Individuais vs. ALF-MoE\nCenário de Referência: CSE-CIC-IDS2018 Corrigido (Nível 2 - 9 classes)", pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight="bold")
    ax.set_ylim(0.0, 1.15)
    ax.set_yticks(np.arange(0.0, 1.01, 0.1))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", ncol=4, framealpha=0.95, edgecolor="gray")

    # Destaque visual no modelo proposto
    ax.get_xticklabels()[-1].set_color("#d62728")
    ax.get_xticklabels()[-1].set_fontweight("extra bold")

    plt.tight_layout()

    png_path = output_dir / "grafico_metricas_especialistas_vs_alf.png"
    pdf_path = output_dir / "grafico_metricas_especialistas_vs_alf.pdf"
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Gráfico salvo em:\n  - {png_path}\n  - {pdf_path}")
    return png_path, pdf_path


def plot_integrated_dashboard(df: pd.DataFrame, experts_data: dict, output_dir: Path):
    """Gera um painel com 2 subgráficos consolidando os 2 ângulos de análise."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 13))

    metrics = ["Acurácia Global", "Macro Precisão", "Macro Sensibilidade", "Macro F1-Score"]
    bar_width = 0.18
    n_metrics = len(metrics)
    offsets = np.linspace(-(n_metrics - 1) / 2 * bar_width, (n_metrics - 1) / 2 * bar_width, n_metrics)

    # Painel 1: Cenários
    x1 = np.arange(len(df))
    for i, metric in enumerate(metrics):
        values = df[metric].values
        color = METRIC_COLORS[metric]
        rects = ax1.bar(x1 + offsets[i], values, bar_width, label=metric, color=color, edgecolor="black", linewidth=0.7, alpha=0.9)
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height), xytext=(0, 2),
                         textcoords="offset points", ha="center", va="bottom", fontsize=7.5, rotation=90)

    ax1.set_ylabel("Escore (0.0 a 1.0)")
    ax1.set_title("(A) Desempenho do ALF-MoE nos 7 Cenários de Benchmark", loc="left", pad=12)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(df["short_name"].values, fontweight="bold")
    ax1.set_ylim(0.0, 1.15)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left", ncol=4, framealpha=0.95)

    # Painel 2: Especialistas vs ALF (CSE-CIC-IDS2018 Corr L2)
    sc_data = experts_data.get("cse_imp_l2", {})
    experts = sc_data.get("experts", {})
    alf = sc_data.get("alf", {})
    models = ["DNN", "CNN", "GRU", "CAE", "LSTM", "ALF-MoE (Proposto)"]
    records = []
    for m in ["DNN", "CNN", "GRU", "CAE", "LSTM"]:
        exp_m = experts.get(m, {})
        records.append({
            "Modelo": m,
            "Acurácia Global": exp_m.get("accuracy", 0.0),
            "Macro Precisão": exp_m.get("macro_precision", 0.0),
            "Macro Sensibilidade": exp_m.get("macro_recall", 0.0),
            "Macro F1-Score": exp_m.get("macro_f1", 0.0),
        })
    records.append({
        "Modelo": "ALF-MoE (Proposto)",
        "Acurácia Global": alf.get("accuracy", 0.0),
        "Macro Precisão": alf.get("macro_precision", 0.0),
        "Macro Sensibilidade": alf.get("macro_recall", 0.0),
        "Macro F1-Score": alf.get("macro_f1", 0.0),
    })
    df_models = pd.DataFrame(records)

    x2 = np.arange(len(models))
    for i, metric in enumerate(metrics):
        values = df_models[metric].values
        color = METRIC_COLORS[metric]
        rects = ax2.bar(x2 + offsets[i], values, bar_width, label=metric, color=color, edgecolor="black", linewidth=0.7, alpha=0.9)
        for rect in rects:
            height = rect.get_height()
            ax2.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height), xytext=(0, 2),
                         textcoords="offset points", ha="center", va="bottom", fontsize=7.5, rotation=90)

    ax2.set_ylabel("Escore (0.0 a 1.0)")
    ax2.set_title("(B) Comparativo de Ablação: Especialistas Individuais vs. Fusão ALF-MoE [CSE-2018 Corr. L2]", loc="left", pad=12)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(models, fontweight="bold")
    ax2.get_xticklabels()[-1].set_color("#d62728")
    ax2.get_xticklabels()[-1].set_fontweight("extra bold")
    ax2.set_ylim(0.0, 1.15)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.legend(loc="upper left", ncol=4, framealpha=0.95)

    plt.tight_layout()
    png_path = output_dir / "painel_metricas_global_completo.png"
    pdf_path = output_dir / "painel_metricas_global_completo.pdf"
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Painel salvo em:\n  - {png_path}\n  - {pdf_path}")
    return png_path, pdf_path


def main():
    root_dir = Path(__file__).resolve().parent.parent
    output_dir = root_dir / "UndergraduateThesis" / "figures" / "benchmarks"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=== Carregando métricas dos relatórios de teste ===")
    df_scenarios, experts_data = load_scenario_data(root_dir)

    print("\n--- Tabela Consolidada ALF-MoE nos 7 Cenários ---")
    print(df_scenarios[["name", "Acurácia Global", "Macro Precisão", "Macro Sensibilidade", "Macro F1-Score"]].to_string(index=False))

    print("\n=== Gerando Gráfico 1: Cenários ALF-MoE ===")
    plot_alf_moe_scenarios_chart(df_scenarios, output_dir)

    print("\n=== Gerando Gráfico 2: Especialistas vs. ALF-MoE ===")
    plot_experts_vs_alf_chart(experts_data, output_dir, target_scenario_id="cse_imp_l2")

    print("\n=== Gerando Gráfico 3: Painel Consolidado Completo ===")
    plot_integrated_dashboard(df_scenarios, experts_data, output_dir)

    print("\n[Concluído com sucesso!]")


if __name__ == "__main__":
    main()
