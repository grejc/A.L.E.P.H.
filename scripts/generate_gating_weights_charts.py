#!/usr/bin/env python3
"""
Geração de gráficos da média de pesos dos especialistas atribuídos pela Gating Network:
1. CIC-BCCC-NRC-2024
2. CSE-CIC-IDS2018 (Canônico)
3. CSE-CIC-IDS2018 (Corrigido)
4. CIC-UNSW-NB15

Gera para cada dataset:
- Gráfico detalhado por classe de tráfego com média global (estilo Figura 12 do artigo original ALF-MoE).
- Gráfico da média global consolidada atribuída a cada especialista.
- Painel consolidado comparando os 4 datasets em um único layout editorial.

Formatos gerados: PNG em alta resolução (300 DPI) e PDF vetorial para teses e artigos LaTeX.
"""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Configurações visuais elegantes para gráficos acadêmicos
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

# Cores canônicas dos 5 especialistas (idênticas ao artigo ALF-MoE e reports.py)
EXPERT_COLORS = {
    "DNN": "#1f77b4",   # Azul clássico
    "CNN": "#ff7f0e",   # Laranja
    "GRU": "#2ca02c",   # Verde
    "CAE": "#d62728",   # Vermelho carmim
    "LSTM": "#9467bd",  # Roxo
}

EXPERT_LABELS = {
    "DNN": r"$\mathcal{E}_{\mathrm{DNN}}$ (Métricas Globais)",
    "CNN": r"$\mathcal{E}_{\mathrm{CNN}}$ (Espacial / Pacotes)",
    "GRU": r"$\mathcal{E}_{\mathrm{GRU}}$ (Sequencial / IAT)",
    "CAE": r"$\mathcal{E}_{\mathrm{CAE}}$ (Espectral / Frequência)",
    "LSTM": r"$\mathcal{E}_{\mathrm{LSTM}}$ (Temporal Longo Prazo)",
}

DATASET_CONFIGS = [
    {
        "id": "bccc_2024",
        "dataset_name": "CIC-BCCC-NRC-2024",
        "dataset_dir": "CIC-BCCC-NRC-2024",
        "run_id": "2026-09-27_22:14:39",
        "threat_level": "Nível 2 (9 classes)",
        "file_suffix": "cic_bccc_nrc_2024",
        "title": "CIC-BCCC-NRC-2024",
    },
    {
        "id": "cse_2018_orig",
        "dataset_name": "CSE-CIC-IDS2018 (Canônico)",
        "dataset_dir": "CSE-CIC-IDS2018",
        "run_id": "2026-09-27_21:09:15",
        "threat_level": "Nível 2 (7 classes)",
        "file_suffix": "cse_cic_ids2018_canonico",
        "title": "CSE-CIC-IDS2018 (Canônico)",
    },
    {
        "id": "cse_2018_imp",
        "dataset_name": "CSE-CIC-IDS2018 (Corrigido)",
        "dataset_dir": "CSECICIDS2018_improved",
        "run_id": "2026-09-28_00:19:51",
        "threat_level": "Nível 2 (9 classes)",
        "file_suffix": "cse_cic_ids2018_corrigido",
        "title": "CSE-CIC-IDS2018 (Corrigido)",
    },
    {
        "id": "unsw_nb15",
        "dataset_name": "CIC-UNSW-NB15",
        "dataset_dir": "CIC-UNSW-NB15",
        "run_id": "2026-09-27_20:19:01",
        "threat_level": "Nível 0 (10 classes)",
        "file_suffix": "cic_unsw_nb15",
        "title": "CIC-UNSW-NB15",
    },
]


def load_dataset_gating_data(base_path: Path, config: dict):
    """Carrega matriz de pesos por classe e dados de suporte do test_report.json."""
    artifacts_dir = base_path / "artifacts" / config["dataset_dir"] / config["run_id"] / "reports"
    csv_file = artifacts_dir / "gating_attention_heatmap.csv"
    json_file = artifacts_dir / "test_report.json"

    if not csv_file.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_file}")
    if not json_file.exists():
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {json_file}")

    df_attn = pd.read_csv(csv_file, index_col=0)
    with open(json_file, "r", encoding="utf-8") as f:
        rep = json.load(f)

    breakdown = rep.get("alf_per_class_breakdown", {})
    supports = {k: v.get("support", 0) for k, v in breakdown.items()}

    # Alinhar suporte com classes do DataFrame
    class_supports = [supports.get(c, 0) for c in df_attn.index]
    counts = np.array(class_supports)
    weights = df_attn.values

    # Média não ponderada (macro média entre as classes)
    unweighted_mean = np.mean(weights, axis=0)

    # Média ponderada pelo número de amostras reais do conjunto de teste (global)
    total_samples = np.sum(counts)
    if total_samples > 0:
        weighted_mean = np.sum(weights * counts[:, None], axis=0) / total_samples
    else:
        weighted_mean = unweighted_mean

    return {
        "df_attn": df_attn,
        "classes": list(df_attn.index),
        "supports": class_supports,
        "total_samples": total_samples,
        "experts": list(df_attn.columns),
        "unweighted_mean": unweighted_mean,
        "weighted_mean": weighted_mean,
    }


def plot_classwise_gating_chart(data: dict, config: dict, output_dirs: list[Path]):
    """
    Gera gráfico de barras agrupadas demonstrando a média dos pesos atribuídos
    a cada especialista para cada classe de tráfego, acrescido da coluna de Média Geral
    (estilo Figura 12 do artigo original ALF-MoE).
    """
    df = data["df_attn"]
    classes = list(df.index)
    experts = data["experts"]
    n_classes = len(classes)
    n_experts = len(experts)

    # Adicionar categoria de Média Geral ao final
    all_categories = classes + ["MÉDIA GERAL"]
    n_total_cats = len(all_categories)

    # Matriz estendida com os pesos por classe + média geral ponderada
    extended_matrix = np.zeros((n_total_cats, n_experts))
    extended_matrix[:n_classes, :] = df.values
    extended_matrix[n_classes, :] = data["weighted_mean"]

    # Larguras e posições das barras agrupadas
    bar_width = 0.15
    x = np.arange(n_total_cats)
    offsets = np.linspace(-(n_experts - 1) / 2 * bar_width, (n_experts - 1) / 2 * bar_width, n_experts)

    fig, ax = plt.subplots(figsize=(max(11, n_total_cats * 1.35), 6.5))

    for j, exp in enumerate(experts):
        values = extended_matrix[:, j]
        color = EXPERT_COLORS[exp]
        label = EXPERT_LABELS[exp]
        rects = ax.bar(
            x + offsets[j],
            values,
            bar_width,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.6,
            alpha=0.9,
        )

        # Rótulo de valores sobre as barras principais
        for i, rect in enumerate(rects):
            h = rect.get_height()
            if h >= 0.04:  # Apenas exibe se for visível para não sobrepor
                ax.annotate(
                    f"{h:.2f}",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=7.5,
                    rotation=90 if n_total_cats > 8 else 0,
                    fontweight="bold" if i == n_classes else "normal",
                )

    # Linha divisória antes da Média Geral
    ax.axvline(n_classes - 0.5, color="#555555", linestyle="--", linewidth=1.2, alpha=0.7)
    
    # Destacar a área da Média Geral com fundo leve
    ax.axvspan(n_classes - 0.5, n_total_cats - 0.5, color="#f5f5f5", alpha=0.6, zorder=0)

    ax.set_ylabel("Peso Médio da Gating Network ($a_k$)", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Média de Pesos dos Especialistas Atribuídos pela Gating Network por Classe\n"
        f"Dataset: {config['title']} [{config['threat_level']}] — $N = {data['total_samples']:,}$ amostras de teste",
        pad=18,
        fontsize=12.5,
        fontweight="bold",
    )

    ax.set_xticks(x)
    # Formatar rótulos do eixo X (classes)
    formatted_labels = [c.replace(" - ", "\n").replace(" / ", "\n") for c in classes] + ["MÉDIA\nGERAL"]
    ax.set_xticklabels(formatted_labels, rotation=35, ha="right", fontweight="bold", fontsize=9.5)

    # Destacar visualmente o rótulo MÉDIA GERAL
    ax.get_xticklabels()[-1].set_color("#8b0000")
    ax.get_xticklabels()[-1].set_fontweight("bold")

    y_max = min(1.0, max(0.65, float(extended_matrix.max()) * 1.35))
    ax.set_ylim(0.0, y_max)
    ax.set_yticks(np.arange(0.0, y_max + 0.01, 0.1))
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    
    # Legenda à esquerda para não sobrepor com a Média Geral à direita
    ax.legend(loc="upper left", framealpha=0.95, edgecolor="gray", fontsize=9.5)

    plt.tight_layout()

    # Salva nos diretórios informados
    for out_dir in output_dirs:
        png_path = out_dir / f"gating_pesos_classes_{config['file_suffix']}.png"
        pdf_path = out_dir / f"gating_pesos_classes_{config['file_suffix']}.pdf"
        plt.savefig(png_path, dpi=300, bbox_inches="tight")
        plt.savefig(pdf_path, bbox_inches="tight")

    plt.close(fig)
    print(f"[OK] Gráfico por classes salvo: gating_pesos_classes_{config['file_suffix']}.png/.pdf")


def plot_global_mean_gating_chart(data: dict, config: dict, output_dirs: list[Path]):
    """
    Gera gráfico de barras vertical focado na média global atribuída a cada um dos
    5 especialistas em todo o conjunto de dados.
    """
    experts = data["experts"]
    weighted_mean = data["weighted_mean"]
    unweighted_mean = data["unweighted_mean"]

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    x = np.arange(len(experts))
    colors = [EXPERT_COLORS[exp] for exp in experts]

    bars = ax.bar(
        x,
        weighted_mean,
        width=0.55,
        color=colors,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.9,
    )

    # Anotação com porcentagem e valor absoluto sobre as barras
    for rect, wm, um in zip(bars, weighted_mean, unweighted_mean):
        h = rect.get_height()
        ax.annotate(
            f"{wm * 100:.2f}%\n({wm:.4f})",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
        )

    ax.set_ylabel("Peso Médio Global ($a_k$)", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Média Global de Pesos da Gating Network por Especialista\n"
        f"Dataset: {config['title']} ({config['threat_level']})",
        pad=16,
        fontsize=12,
        fontweight="bold",
    )

    x_labels = [
        f"DNN\n(Métricas Globais)",
        f"CNN\n(Espacial / Pacotes)",
        f"GRU\n(Sequencial / IAT)",
        f"CAE\n(Espectral / Freq.)",
        f"LSTM\n(Temporal Longo)",
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontweight="bold", fontsize=10)

    y_max = min(1.0, max(0.5, float(weighted_mean.max()) * 1.25))
    ax.set_ylim(0.0, y_max)
    ax.set_yticks(np.arange(0.0, y_max + 0.01, 0.1))
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Linha de referência da média uniforme (1/5 = 0.20)
    ax.axhline(0.20, color="gray", linestyle="--", linewidth=1.1, alpha=0.8, label="Alocação Uniforme ($a_k = 0{,}20$)")
    ax.legend(loc="upper right", framealpha=0.95, edgecolor="gray")

    plt.tight_layout()

    for out_dir in output_dirs:
        png_path = out_dir / f"gating_pesos_media_global_{config['file_suffix']}.png"
        pdf_path = out_dir / f"gating_pesos_media_global_{config['file_suffix']}.pdf"
        plt.savefig(png_path, dpi=300, bbox_inches="tight")
        plt.savefig(pdf_path, bbox_inches="tight")

    plt.close(fig)
    print(f"[OK] Gráfico média global salvo: gating_pesos_media_global_{config['file_suffix']}.png/.pdf")


def plot_consolidated_4datasets_panel(all_data: dict, output_dirs: list[Path]):
    """
    Gera um painel com os 4 datasets lado a lado em grade 2x2,
    ideal para inserção consolidada no corpo da dissertação.
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 13))
    axes = axes.flatten()

    sub_letters = ["(a)", "(b)", "(c)", "(d)"]

    for idx, cfg in enumerate(DATASET_CONFIGS):
        ax = axes[idx]
        data = all_data[cfg["id"]]
        df = data["df_attn"]
        classes = list(df.index)
        experts = data["experts"]
        n_classes = len(classes)
        n_experts = len(experts)

        all_cats = classes + ["MÉDIA"]
        extended_mat = np.zeros((len(all_cats), n_experts))
        extended_mat[:n_classes, :] = df.values
        extended_mat[n_classes, :] = data["weighted_mean"]

        bar_width = 0.15
        x = np.arange(len(all_cats))
        offsets = np.linspace(-(n_experts - 1) / 2 * bar_width, (n_experts - 1) / 2 * bar_width, n_experts)

        for j, exp in enumerate(experts):
            values = extended_mat[:, j]
            color = EXPERT_COLORS[exp]
            label = EXPERT_LABELS[exp] if idx == 0 else ""
            ax.bar(
                x + offsets[j],
                values,
                bar_width,
                label=label,
                color=color,
                edgecolor="black",
                linewidth=0.5,
                alpha=0.9,
            )

        ax.axvline(n_classes - 0.5, color="gray", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.set_title(
            f"{sub_letters[idx]} {cfg['title']} [{cfg['threat_level']}]",
            loc="left",
            fontsize=12,
            fontweight="bold",
            pad=10,
        )
        ax.set_ylabel("Peso Médio ($a_k$)", fontsize=10.5, fontweight="bold")
        ax.set_xticks(x)
        clean_labels = [c.replace(" - ", "\n").replace(" / ", "\n") for c in classes] + ["MÉDIA"]
        ax.set_xticklabels(clean_labels, rotation=35, ha="right", fontsize=8.5, fontweight="bold")
        ax.get_xticklabels()[-1].set_color("#8b0000")
        ax.get_xticklabels()[-1].set_fontweight("bold")

        y_max = min(1.0, max(0.55, float(extended_mat.max()) * 1.15))
        ax.set_ylim(0.0, y_max)
        ax.set_yticks(np.arange(0.0, y_max + 0.01, 0.1))
        ax.grid(axis="y", linestyle=":", alpha=0.5)

    # Legenda global compartilhada no topo
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=5,
        framealpha=0.95,
        edgecolor="gray",
        fontsize=11,
        bbox_to_anchor=(0.5, 0.995),
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    for out_dir in output_dirs:
        png_path = out_dir / "painel_gating_pesos_4datasets.png"
        pdf_path = out_dir / "painel_gating_pesos_4datasets.pdf"
        plt.savefig(png_path, dpi=300, bbox_inches="tight")
        plt.savefig(pdf_path, bbox_inches="tight")

    plt.close(fig)
    print(f"[OK] Painel consolidado salvo: painel_gating_pesos_4datasets.png/.pdf")


def plot_global_comparison_chart(all_data: dict, output_dirs: list[Path]):
    """
    Gera gráfico comparando diretamente a média global dos especialistas
    entre os 4 datasets.
    """
    experts = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
    dataset_titles = [cfg["title"] for cfg in DATASET_CONFIGS]
    n_datasets = len(DATASET_CONFIGS)
    n_experts = len(experts)

    x = np.arange(n_datasets)
    bar_width = 0.15
    offsets = np.linspace(-(n_experts - 1) / 2 * bar_width, (n_experts - 1) / 2 * bar_width, n_experts)

    fig, ax = plt.subplots(figsize=(13, 6.5))

    for j, exp in enumerate(experts):
        vals = [all_data[cfg["id"]]["weighted_mean"][j] for cfg in DATASET_CONFIGS]
        color = EXPERT_COLORS[exp]
        rects = ax.bar(
            x + offsets[j],
            vals,
            bar_width,
            label=EXPERT_LABELS[exp],
            color=color,
            edgecolor="black",
            linewidth=0.6,
            alpha=0.9,
        )

        for rect in rects:
            h = rect.get_height()
            ax.annotate(
                f"{h*100:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 2),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
                fontweight="bold",
            )

    ax.set_ylabel("Peso Médio Global Ponderado ($a_k$)", fontsize=11, fontweight="bold")
    ax.set_title(
        "Comparativo Inter-Dataset: Média de Pesos Atribuídos pela Gating Network aos 5 Especialistas",
        pad=18,
        fontsize=12.5,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(dataset_titles, fontweight="bold", fontsize=10.5)
    ax.set_ylim(0.0, 0.55)
    ax.set_yticks(np.arange(0.0, 0.51, 0.05))
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.axhline(0.20, color="gray", linestyle="--", linewidth=1.0, alpha=0.7, label="Alocação Uniforme ($a_k = 0{,}20$)")
    ax.legend(loc="upper right", framealpha=0.95, edgecolor="gray", ncol=2, fontsize=9.5)

    plt.tight_layout()

    for out_dir in output_dirs:
        png_path = out_dir / "comparativo_gating_pesos_4datasets.png"
        pdf_path = out_dir / "comparativo_gating_pesos_4datasets.pdf"
        plt.savefig(png_path, dpi=300, bbox_inches="tight")
        plt.savefig(pdf_path, bbox_inches="tight")

    plt.close(fig)
    print(f"[OK] Gráfico comparativo global salvo: comparativo_gating_pesos_4datasets.png/.pdf")


def main():
    root_dir = Path(__file__).resolve().parent.parent
    thesis_figures_dir = root_dir / "UndergraduateThesis" / "figures" / "benchmarks"
    thesis_figures_dir.mkdir(parents=True, exist_ok=True)

    artifacts_gating_dir = root_dir / "artifacts" / "gating_weights"
    artifacts_gating_dir.mkdir(parents=True, exist_ok=True)

    output_dirs = [thesis_figures_dir, artifacts_gating_dir]

    print("=== Carregando dados da Gating Network para os 4 datasets ===")
    all_data = {}
    for cfg in DATASET_CONFIGS:
        print(f"-> Carregando {cfg['dataset_name']} ({cfg['run_id']})...")
        data = load_dataset_gating_data(root_dir, cfg)
        all_data[cfg["id"]] = data

        # Salva também diretamente no diretório do experimento correspondente
        run_reports_dir = root_dir / "artifacts" / cfg["dataset_dir"] / cfg["run_id"] / "reports"
        ds_output_dirs = output_dirs + [run_reports_dir]

        print(f"\n[Gerando Gráficos para {cfg['dataset_name']}]")
        plot_classwise_gating_chart(data, cfg, ds_output_dirs)
        plot_global_mean_gating_chart(data, cfg, ds_output_dirs)

    print("\n[Gerando Painel Consolidado 2x2 para a Tese]")
    plot_consolidated_4datasets_panel(all_data, output_dirs)

    print("\n[Gerando Comparativo Inter-Dataset dos 4 Datasets]")
    plot_global_comparison_chart(all_data, output_dirs)

    print("\n=== Todos os gráficos foram gerados e salvos com sucesso! ===")


if __name__ == "__main__":
    main()
