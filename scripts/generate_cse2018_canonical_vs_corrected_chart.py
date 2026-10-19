#!/usr/bin/env python3
"""
Gera o gráfico comparativo lado a lado (1x2) da distribuição amostral de classes
do dataset CSE-CIC-IDS2018: Versão Canônica vs. Versão Corrigida (Liu et al., 2022).

Extrai os dados diretamente dos datasets de trabalho na fonte (/run/media/null/VM_s/DATASETS):
- CSE-CIC-IDS2018_sampled.csv (Versão Canônica amostrada: 3.712.942 fluxos | 15 classes)
- CSECICIDS2018_improved.parquet (Versão Corrigida amostrada: 6.319.514 fluxos | 15 classes)

Salva em PDF vetorial e PNG (300 DPI) em UndergraduateThesis/figures/.
"""

import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.csv as pcsv
import pyarrow.parquet as pq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Estilo acadêmico padronizado com as demais figuras de distribuição da tese
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.labelweight": "semibold",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10.5,
    "legend.fontsize": 10.5,
    "figure.titlesize": 15.5,
    "figure.titleweight": "bold",
})

DATASETS_DIR = Path("/run/media/null/VM_s/DATASETS")
CANONICAL_PATH = DATASETS_DIR / "CSE-CIC-IDS2018_sampled.csv"
CORRECTED_PATH = DATASETS_DIR / "CSECICIDS2018_improved.parquet"

THESIS_FIG_DIR = Path("/home/null/ALF-MoE/UndergraduateThesis/figures")
EDA_PLOTS_DIR = DATASETS_DIR / "eda_plots"


def format_pct(pct: float) -> str:
    if pct >= 0.01:
        return f"{pct:.2f}%"
    elif pct >= 0.001:
        return f"{pct:.3f}%"
    return f"{pct:.4f}%"


def main() -> None:
    THESIS_FIG_DIR.mkdir(parents=True, exist_ok=True)
    EDA_PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print(f"1. Lendo coluna 'Label' direto da fonte: {CANONICAL_PATH} ...")
    t0 = time.time()
    ro = pcsv.ReadOptions(use_threads=True)
    co = pcsv.ConvertOptions(include_columns=["Label"])
    table_canon = pcsv.read_csv(str(CANONICAL_PATH), read_options=ro, convert_options=co)
    s_canon = pd.Series(table_canon["Label"].to_pylist()).value_counts()
    total_canon = int(len(table_canon))
    del table_canon
    print(f"   Concluído em {time.time() - t0:.2f}s | Total: {total_canon:,} fluxos | {len(s_canon)} classes")

    print("=" * 72)
    print(f"2. Lendo coluna 'Label' direto da fonte: {CORRECTED_PATH} ...")
    t0 = time.time()
    table_corr = pq.read_table(str(CORRECTED_PATH), columns=["Label"])
    s_corr = pd.Series(table_corr["Label"].to_pylist()).value_counts()
    total_corr = int(len(table_corr))
    del table_corr
    print(f"   Concluído em {time.time() - t0:.2f}s | Total: {total_corr:,} fluxos | {len(s_corr)} classes")

    # Salvar manifesto JSON de auditoria dos dados lidos direto da fonte
    audit_stats = {
        "CSE-CIC-IDS2018_sampled": {
            "source_file": str(CANONICAL_PATH),
            "total": total_canon,
            "n_classes": int(len(s_canon)),
            "classes": {str(k): int(v) for k, v in s_canon.items()},
        },
        "CSECICIDS2018_improved": {
            "source_file": str(CORRECTED_PATH),
            "total": total_corr,
            "n_classes": int(len(s_corr)),
            "classes": {str(k): int(v) for k, v in s_corr.items()},
        },
    }
    json_out = EDA_PLOTS_DIR / "cse_cic_ids2018_canonical_vs_corrected_sampled.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(audit_stats, f, indent=2, ensure_ascii=False)
    print(f"   JSON de auditoria salvo em: {json_out}")

    # Cálculo de proporções
    pct_canon = (s_canon / total_canon) * 100.0
    pct_corr = (s_corr / total_corr) * 100.0

    # Criação do painel 1x2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 8.2), gridspec_kw={"width_ratios": [1, 1]})

    # -------------------------------------------------------------------------
    # Painel Esquerdo: Versão Canônica (Amostrada)
    # -------------------------------------------------------------------------
    y_pos1 = np.arange(len(s_canon))
    colors_canon = ["#27ae60" if c.lower() == "benign" else "#c0392b" for c in s_canon.index]
    bars1 = ax1.barh(
        y_pos1,
        s_canon.values,
        color=colors_canon,
        edgecolor="black",
        linewidth=0.7,
        alpha=0.86,
        height=0.65,
    )
    ax1.set_yticks(y_pos1)
    ax1.set_yticklabels(s_canon.index, fontweight="semibold")
    ax1.invert_yaxis()
    ax1.set_xscale("log")
    ax1.set_xlabel("Contagem de Fluxos (Escala Logarítmica)")
    ax1.set_title(
        f"Versão Canônica Amostrada (Original)\n"
        f"(Total: {total_canon:,} fluxos | {len(s_canon)} classes)"
    )
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    for bar, count, pct in zip(bars1, s_canon.values, pct_canon.values):
        w = bar.get_width()
        ax1.text(
            w * 1.15,
            bar.get_y() + bar.get_height() / 2.0,
            f"{count:,} ({format_pct(pct)})",
            va="center",
            ha="left",
            fontsize=9.2,
            fontweight="bold",
        )
    ax1.set_xlim(right=ax1.get_xlim()[1] * 9.5)

    # -------------------------------------------------------------------------
    # Painel Direito: Versão Corrigida (Amostrada — Liu et al., 2022)
    # -------------------------------------------------------------------------
    y_pos2 = np.arange(len(s_corr))
    colors_corr = ["#27ae60" if c.upper() == "BENIGN" else "#2980b9" for c in s_corr.index]
    bars2 = ax2.barh(
        y_pos2,
        s_corr.values,
        color=colors_corr,
        edgecolor="black",
        linewidth=0.7,
        alpha=0.86,
        height=0.65,
    )
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(s_corr.index, fontweight="semibold")
    ax2.invert_yaxis()
    ax2.set_xscale("log")
    ax2.set_xlabel("Contagem de Fluxos (Escala Logarítmica)")
    ax2.set_title(
        f"Versão Corrigida Amostrada (Liu et al., 2022)\n"
        f"(Total: {total_corr:,} fluxos | {len(s_corr)} classes pós-reclassificação)"
    )
    ax2.grid(True, which="both", linestyle="--", alpha=0.5)

    for bar, count, pct in zip(bars2, s_corr.values, pct_corr.values):
        w = bar.get_width()
        ax2.text(
            w * 1.15,
            bar.get_y() + bar.get_height() / 2.0,
            f"{count:,} ({format_pct(pct)})",
            va="center",
            ha="left",
            fontsize=9.2,
            fontweight="bold",
        )
    ax2.set_xlim(right=ax2.get_xlim()[1] * 10.5)

    plt.suptitle(
        "CSE-CIC-IDS2018: Distribuição Amostral de Classes — Versão Canônica vs. Versão Corrigida",
        fontsize=16,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout()

    # Salvar arquivos em PDF e PNG
    out_stem = "Dataset_CSECICIDS2018_Canonico_vs_Corrigido"
    pdf_thesis = THESIS_FIG_DIR / f"{out_stem}.pdf"
    png_thesis = THESIS_FIG_DIR / f"{out_stem}.png"
    png_eda = EDA_PLOTS_DIR / f"{out_stem}.png"

    fig.savefig(pdf_thesis, bbox_inches="tight")
    fig.savefig(png_thesis, dpi=300, bbox_inches="tight")
    fig.savefig(png_eda, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("=" * 72)
    print(f"[OK] PDF salvo em: {pdf_thesis}")
    print(f"[OK] PNG salvo em: {png_thesis}")
    print(f"[OK] PNG salvo em: {png_eda}")


if __name__ == "__main__":
    main()
