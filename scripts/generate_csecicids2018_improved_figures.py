#!/usr/bin/env python3
"""
Gera os gráficos de alta qualidade para o CSE-CIC-IDS2018 Corrigido (Improved)
tanto em PDF vetorial quanto em PNG (300 DPI) para UndergraduateThesis/figures,
para /run/media/null/VM_s/DATASETS/eda_plots e para os artefatos da sessão.

Figuras geradas:
1. Dataset_CSECICIDS2018_Corrigido_Classes (Painel Duplo: Distribuição Completa L0 + Zoom Ataques)
2. Dataset_CSECICIDS2018_Corrigido_Classes_Single (Painel Único: 15 Classes)
3. Dataset_CSECICIDS2018_Corrigido_L2 (Macro-Categorias L2: Barras + Rosca Donut)
4. Dataset_CSECICIDS2018_Corrigido_Amostragem_Fidelidade (População 63.2M vs Amostra 878k)
5. Dataset_CSECICIDS2018_Corrigido_Rerotulamento (Impacto da reclassificação de "Attempted" -> BENIGN)
6. csecicids2018_improved_distribution (Distribuição Canônica no eda_plots)
7. Dataset_CSECICIDS2018_Corrigido_Features_Boxplots (Boxplots de 4 Atributos Chave de Rede)
8. Dataset_CSECICIDS2018_Corrigido_TCP_Flags (Perfil Médio de Flags TCP por Classe)
"""

import os
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

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
    "figure.titlesize": 16,
    "figure.titleweight": "bold",
})

PARQUET_PATH = Path("/run/media/null/VM_s/DATASETS/CSECICIDS2018_improved.parquet")
THESIS_FIG_DIR = Path("/home/null/ALF-MoE/UndergraduateThesis/figures")
EDA_PLOTS_DIR = Path("/run/media/null/VM_s/DATASETS/eda_plots")
ARTIFACT_PLOTS_DIR = Path("/home/null/.gemini/antigravity-cli/brain/8d12e56c-f7d5-4acc-b926-04692619d30d/plots")

THESIS_FIG_DIR.mkdir(parents=True, exist_ok=True)
EDA_PLOTS_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def fmt_pct(pct: float) -> str:
    if pct >= 0.01:
        return f"{pct:.2f}%"
    elif pct >= 0.001:
        return f"{pct:.3f}%"
    return f"{pct:.4f}%"

def save_fig(fig, base_name):
    pdf_thesis = THESIS_FIG_DIR / f"{base_name}.pdf"
    png_thesis = THESIS_FIG_DIR / f"{base_name}.png"
    pdf_eda = EDA_PLOTS_DIR / f"{base_name}.pdf"
    png_eda = EDA_PLOTS_DIR / f"{base_name}.png"
    png_art = ARTIFACT_PLOTS_DIR / f"{base_name}.png"
    
    fig.tight_layout()
    fig.savefig(pdf_thesis, bbox_inches="tight")
    fig.savefig(png_thesis, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_eda, bbox_inches="tight")
    fig.savefig(png_eda, dpi=300, bbox_inches="tight")
    fig.savefig(png_art, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Salvo: {base_name} (PDF/PNG em Thesis, EDA e Artefatos)")

# =============================================================================
# 0. CARREGAMENTO DOS RÓTULOS REAIS DO PARQUET
# =============================================================================
print(f"Lendo rótulos diretamente de {PARQUET_PATH}...")
t0 = time.time()
tbl_label = pq.read_table(str(PARQUET_PATH), columns=["Label"])
s_corr = tbl_label["Label"].to_pandas().value_counts()
sample_classes = s_corr.to_dict()
total_corr = int(s_corr.sum())
pct_corr = (s_corr / total_corr) * 100.0

print(f"-> Carregados {total_corr:,} registros em {time.time()-t0:.2f}s.")
print(f"-> BENIGN: {sample_classes.get('BENIGN', 0):,} ({pct_corr.get('BENIGN', 0):.2f}%)")
print(f"-> Ataques: {total_corr - sample_classes.get('BENIGN', 0):,} ({100 - pct_corr.get('BENIGN', 0):.2f}%)")

# Atualizar json de distribuições se existir
json_path = EDA_PLOTS_DIR / "dataset_class_distributions.json"
if json_path.exists():
    try:
        with open(json_path, "r") as f:
            all_stats = json.load(f)
        all_stats["CSECICIDS2018_improved"] = {
            "total": total_corr,
            "classes": sample_classes
        }
        with open(json_path, "w") as f:
            json.dump(all_stats, f, indent=2)
        print(f"[OK] Atualizado {json_path}")
    except Exception as e:
        print(f"Aviso ao atualizar json: {e}")

# =============================================================================
# FIGURA 1: Painel Duplo (L0: Distribuição Completa + Zoom nos Ataques)
# =============================================================================
print("\nGerando Figura 1: Painel Duplo (L0)...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 8.5), gridspec_kw={'width_ratios': [1.2, 1]})

# Painel 1: Todas as classes (log scale)
y_pos1 = np.arange(len(s_corr))
colors_corr1 = ['#27ae60' if c == 'BENIGN' else '#c0392b' for c in s_corr.index]
bars1 = ax1.barh(y_pos1, s_corr.values, color=colors_corr1, edgecolor='black', linewidth=0.7, alpha=0.86, height=0.65)
ax1.set_yticks(y_pos1)
ax1.set_yticklabels(s_corr.index, fontweight='semibold')
ax1.invert_yaxis()
ax1.set_xscale('log')
ax1.set_xlabel('Contagem de Fluxos (Escala Logarítmica)')
ax1.set_title(f'Distribuição Completa de Classes na Amostra\n(Total: {total_corr:,} fluxos | 15 classes)')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count, pct in zip(bars1, s_corr.values, pct_corr.values):
    w = bar.get_width()
    ax1.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0,
             f"{count:,} ({fmt_pct(pct)})",
             va='center', ha='left', fontsize=9.2, fontweight='bold')
ax1.set_xlim(right=ax1.get_xlim()[1] * 9.5)

# Painel 2: Apenas Ataques (Zoom nos Tráfegos Maliciosos)
s_att = s_corr[s_corr.index != 'BENIGN']
total_att = int(s_att.sum())
pct_att = (s_att / total_att) * 100.0

y_pos2 = np.arange(len(s_att))
palette_att = sns.color_palette("flare", len(s_att))
bars2 = ax2.barh(y_pos2, s_att.values, color=palette_att, edgecolor='black', linewidth=0.7, alpha=0.86, height=0.65)
ax2.set_yticks(y_pos2)
ax2.set_yticklabels(s_att.index, fontweight='semibold')
ax2.invert_yaxis()
ax2.set_xscale('log')
ax2.set_xlabel('Contagem de Fluxos de Ataque (Escala Logarítmica)')
ax2.set_title(f'Zoom nos Tráfegos Maliciosos da Amostra\n(Subtotal de Ataques: {total_att:,} fluxos | 14 famílias)')
ax2.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count, pct in zip(bars2, s_att.values, pct_att.values):
    w = bar.get_width()
    ax2.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0,
             f"{count:,} ({fmt_pct(pct)})",
             va='center', ha='left', fontsize=9.2, fontweight='bold')
ax2.set_xlim(right=ax2.get_xlim()[1] * 9.5)

plt.suptitle('CSE-CIC-IDS2018 (Corrigido / Improved): Perfil de Classes e Tráfego Malicioso na Amostra',
             fontsize=16, fontweight='bold', y=1.02)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_Classes")

# =============================================================================
# FIGURA 2: Painel Único (L0 Compacto)
# =============================================================================
print("Gerando Figura 2: Painel Único (L0)...")
fig, ax = plt.subplots(figsize=(14, 8.5))
bars = ax.barh(y_pos1, s_corr.values, color=colors_corr1, edgecolor='black', linewidth=0.7, alpha=0.86, height=0.65)
ax.set_yticks(y_pos1)
ax.set_yticklabels(s_corr.index, fontweight='semibold')
ax.invert_yaxis()
ax.set_xscale('log')
ax.set_xlabel('Contagem de Fluxos (Escala Logarítmica)')
ax.set_title(f'CSE-CIC-IDS2018 (Corrigido / Improved)\nDistribuição de Classes da Amostra (Total: {total_corr:,} fluxos | 15 classes)')
ax.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count, pct in zip(bars, s_corr.values, pct_corr.values):
    w = bar.get_width()
    ax.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0,
            f"{count:,} ({fmt_pct(pct)})",
            va='center', ha='left', fontsize=9.5, fontweight='bold')
ax.set_xlim(right=ax.get_xlim()[1] * 9.5)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_Classes_Single")

# =============================================================================
# FIGURA 3: Macro-Categorias L2 (9 Classes: Barras + Rosca Donut)
# =============================================================================
print("Gerando Figura 3: Macro-Categorias L2...")
mapping_l2 = {
    "BENIGN": "BENIGN",
    "DoS Hulk": "DoS",
    "DoS GoldenEye": "DoS",
    "DoS Slowloris": "DoS",
    "Botnet Ares": "Botnet",
    "DDoS-HOIC": "DDoS",
    "DDoS-LOIC-HTTP": "DDoS",
    "DDoS-LOIC-UDP": "DDoS",
    "SSH-BruteForce": "SSH-BruteForce",
    "Infiltration - NMAP Portscan": "Infiltration - NMAP Portscan",
    "Infiltration - Communication Victim Attacker": "Infiltration - Communication Victim Attacker",
    "Infiltration - Dropbox Download": "Infiltration - Dropbox Download",
    "Web Attack - Brute Force": "Web Attack",
    "Web Attack - XSS": "Web Attack",
    "Web Attack - SQL": "Web Attack"
}

df_l2 = pd.DataFrame({"Class": s_corr.index, "Count": s_corr.values})
df_l2["Macro"] = df_l2["Class"].map(mapping_l2)
s_macro = df_l2.groupby("Macro")["Count"].sum().sort_values(ascending=False)
pct_macro = (s_macro / total_corr) * 100.0

colors_macro_map = {
    "BENIGN": "#27ae60",
    "DoS": "#e67e22",
    "Botnet": "#8e44ad",
    "DDoS": "#c0392b",
    "SSH-BruteForce": "#d35400",
    "Infiltration - NMAP Portscan": "#2980b9",
    "Web Attack": "#f39c12",
    "Infiltration - Communication Victim Attacker": "#16a085",
    "Infiltration - Dropbox Download": "#7f8c8d"
}
colors_macro = [colors_macro_map[c] for c in s_macro.index]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 8.5), gridspec_kw={'width_ratios': [1.2, 1]})

y_pos_m = np.arange(len(s_macro))
bars_m = ax1.barh(y_pos_m, s_macro.values, color=colors_macro, edgecolor='black', linewidth=0.7, alpha=0.88, height=0.65)
ax1.set_yticks(y_pos_m)
ax1.set_yticklabels(s_macro.index, fontweight='bold', fontsize=11)
ax1.invert_yaxis()
ax1.set_xscale('log')
ax1.set_xlabel('Contagem de Fluxos (Escala Logarítmica)', fontsize=12)
ax1.set_title(f'Contagem e Proporção por Macro-Categoria (L2)\n(Total: {total_corr:,} fluxos | 9 macro-famílias)', fontsize=13.5)
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count, pct in zip(bars_m, s_macro.values, pct_macro.values):
    w = bar.get_width()
    ax1.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0,
             f"{count:,} ({fmt_pct(pct)})",
             va='center', ha='left', fontsize=9.5, fontweight='bold')
ax1.set_xlim(right=ax1.get_xlim()[1] * 9.5)

# Rosca Donut
explode_m = [0.03 if p < 4.0 else 0.0 for p in pct_macro]
wedges, texts, autotexts = ax2.pie(
    s_macro.values,
    labels=None,
    autopct=lambda p: f"{p:.1f}%" if p >= 2.0 else "",
    pctdistance=0.78,
    colors=colors_macro,
    startangle=140,
    explode=explode_m,
    wedgeprops=dict(width=0.45, edgecolor='black', linewidth=1)
)
for at in autotexts:
    at.set_fontsize(9.5)
    at.set_fontweight('bold')
    at.set_color('white')

ax2.set_title('Proporção Relativa das Macro-Categorias (L2)', fontsize=13.5, pad=10)
legend_labels = [f"{cat}: {cnt:,} ({fmt_pct(pct)})" for cat, cnt, pct in zip(s_macro.index, s_macro.values, pct_macro.values)]
ax2.legend(wedges, legend_labels, title="Macro-Categorias", loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=10, frameon=True)

plt.suptitle('CSE-CIC-IDS2018 (Corrigido): Agrupamento em 9 Macro-Famílias (L2)', fontsize=16, y=1.02)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_L2")

# =============================================================================
# FIGURA 4: Fidelidade da Amostragem (População 63.2M vs Amostra Otimizada)
# =============================================================================
print("Gerando Figura 4: Fidelidade da Amostragem (População vs Amostra)...")
pop_classes_relabeled = {
    "BENIGN": 59659723,
    "DoS Hulk": 1803160,
    "DDoS-HOIC": 1082293,
    "DDoS-LOIC-HTTP": 289328,
    "Botnet Ares": 142921,
    "SSH-BruteForce": 94197,
    "Infiltration - NMAP Portscan": 89374,
    "DoS GoldenEye": 22560,
    "DoS Slowloris": 8490,
    "DDoS-LOIC-UDP": 2527,
    "Infiltration - Communication Victim Attacker": 204,
    "Web Attack - Brute Force": 131,
    "Web Attack - XSS": 113,
    "Infiltration - Dropbox Download": 85,
    "Web Attack - SQL": 39
}

df_comp = []
for c, pop_cnt in pop_classes_relabeled.items():
    s_cnt = sample_classes.get(c, 0)
    ret_pct = (s_cnt / pop_cnt) * 100.0
    df_comp.append({
        "Class": c,
        "Pop": pop_cnt,
        "Sample": s_cnt,
        "Retention": ret_pct
    })
df_comp = pd.DataFrame(df_comp).iloc[::-1]

fig, ax = plt.subplots(figsize=(16, 9))
y_c = np.arange(len(df_comp))
w_bar = 0.38

bars_pop = ax.barh(y_c - w_bar/2, df_comp["Pop"], w_bar, label="População Total no CSV (63.195.145 fluxos)", color="#34495e", alpha=0.9, log=True, edgecolor="black", linewidth=0.6)
bars_smp = ax.barh(y_c + w_bar/2, df_comp["Sample"], w_bar, label=f"Amostra Otimizada no Parquet ({total_corr:,} fluxos)", color="#27ae60", alpha=0.9, log=True, edgecolor="black", linewidth=0.6)

for i, row in df_comp.reset_index(drop=True).iterrows():
    ret = row["Retention"]
    s_val = row["Sample"]
    if ret >= 99.9:
        lbl_text = "100% retido (Minoria Preservada)"
        col_text = "#1e8449"
    elif abs(ret - 10.0) < 0.2:
        lbl_text = "10,0% retido (Ataque Volumétrico)"
        col_text = "#b9770e"
    else:
        lbl_text = f"{ret:.2f}% retido (Subamostrado para 200k)"
        col_text = "#2e4053"
    
    ax.text(s_val * 1.45, i + w_bar/2, lbl_text, va="center", ha="left", fontsize=9, fontweight="bold", color=col_text)

ax.set_yticks(y_c)
ax.set_yticklabels(df_comp["Class"], fontweight="semibold")
ax.set_xlabel("Contagem de Fluxos (Escala Logarítmica)", fontsize=12)
ax.set_title(f"Representatividade e Preservação de Minorias: População Completa (.csv) vs. Amostra Otimizada (.parquet)\n(Estratégia Híbrida: 100% em 11 minorias, 10% nos ataques volumétricos e 0,34% em BENIGN — {total_corr:,} fluxos)", fontsize=13)
ax.legend(loc="lower right", frameon=True, fontsize=11)
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.set_xlim(right=ax.get_xlim()[1] * 35)

plt.suptitle("CSE-CIC-IDS2018 (Corrigido): Validação da Amostragem e Balanceamento", fontsize=16, fontweight="bold", y=0.99)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_Amostragem_Fidelidade")

# =============================================================================
# FIGURA 5: Auditoria de Re-rotulamento ("Attempted" -> BENIGN)
# =============================================================================
print("Gerando Figura 5: Auditoria de Re-rotulamento...")
original_25_classes = {
    "BENIGN": 59353486,
    "FTP-BruteForce - Attempted": 298874,
    "DoS Hulk": 1803160,
    "DDoS-HOIC": 1082293,
    "DDoS-LOIC-HTTP": 289328,
    "Botnet Ares": 142921,
    "SSH-BruteForce": 94197,
    "Infiltration - NMAP Portscan": 89374,
    "DoS GoldenEye": 22560,
    "DoS Slowloris": 8490,
    "DoS GoldenEye - Attempted": 4301,
    "DDoS-LOIC-UDP": 2527,
    "DoS Slowloris - Attempted": 2280,
    "Botnet Ares - Attempted": 262,
    "DDoS-LOIC-UDP - Attempted": 251,
    "Infiltration - Communication Victim Attacker": 204,
    "Web Attack - Brute Force - Attempted": 137,
    "Web Attack - Brute Force": 131,
    "Web Attack - XSS": 113,
    "DoS Hulk - Attempted": 86,
    "Infiltration - Dropbox Download": 85,
    "Web Attack - SQL": 39,
    "Infiltration - Dropbox Download - Attempted": 28,
    "Web Attack - SQL - Attempted": 14,
    "Web Attack - XSS - Attempted": 4
}
s_orig25 = pd.Series(original_25_classes).sort_values(ascending=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10), gridspec_kw={'width_ratios': [1.1, 1]})

colors_25 = ['#e67e22' if 'Attempted' in c else ('#27ae60' if c == 'BENIGN' else '#c0392b') for c in s_orig25.index]
bars_25 = ax1.barh(np.arange(len(s_orig25)), s_orig25.values, color=colors_25, edgecolor='black', linewidth=0.6, alpha=0.88, height=0.68)
ax1.set_yticks(np.arange(len(s_orig25)))
ax1.set_yticklabels(s_orig25.index, fontweight='semibold', fontsize=9.5)
ax1.set_xscale('log')
ax1.set_xlabel('Contagem de Fluxos (Escala Logarítmica)')
ax1.set_title('Configuração Bruta no CSV (25 Classes)\n[Laranja: 10 Categorias "Attempted" (306.237 fluxos) | Vermelho: Ataques | Verde: Benign]', fontsize=12)
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count in zip(bars_25, s_orig25.values):
    w = bar.get_width()
    ax1.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0, f"{count:,}", va='center', ha='left', fontsize=8.5, fontweight='bold')
ax1.set_xlim(right=ax1.get_xlim()[1] * 8)

# Painel Direito: Pós-Re-rotulamento (15 Classes)
s_relab = pd.Series(pop_classes_relabeled).sort_values(ascending=True)
colors_relab = ['#27ae60' if c == 'BENIGN' else '#c0392b' for c in s_relab.index]
bars_relab = ax2.barh(np.arange(len(s_relab)), s_relab.values, color=colors_relab, edgecolor='black', linewidth=0.6, alpha=0.88, height=0.68)
ax2.set_yticks(np.arange(len(s_relab)))
ax2.set_yticklabels(s_relab.index, fontweight='semibold', fontsize=9.5)
ax2.set_xscale('log')
ax2.set_xlabel('Contagem de Fluxos (Escala Logarítmica)')
ax2.set_title('Configuração Saneada na População (15 Classes Efetivas)\n[Todas as tentativas "Attempted" reclassificadas como BENIGN — Liu et al., 2022]', fontsize=12)
ax2.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count in zip(bars_relab, s_relab.values):
    w = bar.get_width()
    ax2.text(w * 1.15, bar.get_y() + bar.get_height() / 2.0, f"{count:,}", va='center', ha='left', fontsize=8.5, fontweight='bold')
ax2.set_xlim(right=ax2.get_xlim()[1] * 8)

plt.suptitle('CSE-CIC-IDS2018 (Corrigido): Efeito da Reclassificação de Tentativas ("Attempted") para BENIGN', fontsize=16, fontweight='bold', y=0.99)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_Rerotulamento")

# =============================================================================
# FIGURA 6: csecicids2018_improved_distribution (EDA Plots Standard)
# =============================================================================
print("Gerando Figura 6: csecicids2018_improved_distribution...")
fig, ax = plt.subplots(figsize=(14, 8))
y_pos = np.arange(len(s_corr))
colors_imp = ['#27ae60' if c.upper() == 'BENIGN' else '#e74c3c' for c in s_corr.index]
bars = ax.barh(y_pos, s_corr.values, color=colors_imp, edgecolor='black', alpha=0.85, height=0.65)
ax.set_yticks(y_pos)
ax.set_yticklabels(s_corr.index, fontweight='semibold')
ax.invert_yaxis()
ax.set_xscale('log')
ax.set_xlabel('Contagem de Fluxos (Escala Logarítmica)')
ax.set_title(f'CSE-CIC-IDS2018 (Corrigido)\nDistribuição de Classes (Total: {total_corr:,} fluxos | 15 classes)')
ax.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, count, pct in zip(bars, s_corr.values, pct_corr.values):
    w = bar.get_width()
    pct_str = f"{pct:.2f}%" if pct >= 0.01 else f"{pct:.4f}%"
    ax.text(w * 1.15, bar.get_y() + bar.get_height()/2,
            f"{count:,} ({pct_str})",
            va='center', ha='left', fontsize=9.5, fontweight='bold')
ax.set_xlim(right=ax.get_xlim()[1] * 8)
save_fig(fig, "csecicids2018_improved_distribution")

# =============================================================================
# FIGURA 7: Boxplots de Features Principais de Rede
# =============================================================================
print("Gerando Figura 7: Boxplots de Features Principais de Rede...")
cols_to_load = [
    'Label', 'Flow Duration', 'Packet Length Mean', 'FWD Init Win Bytes', 'Total Fwd Packet'
]
tbl_feat = pq.read_table(str(PARQUET_PATH), columns=cols_to_load)
df_feat = tbl_feat.to_pandas()

# Subamostra equilibrada de até 10.000 por classe para plotagem ultra nítida e rápida
sub_dfs = [grp.sample(min(len(grp), 10000), random_state=42) for _, grp in df_feat.groupby('Label')]
df_box = pd.concat(sub_dfs, ignore_index=True)
class_order = s_corr.index.tolist()

fig, axes = plt.subplots(2, 2, figsize=(18, 12))

df_box['Flow Duration Log'] = np.log10(np.maximum(df_box['Flow Duration'], 1.0))
sns.boxplot(data=df_box, x='Flow Duration Log', y='Label', order=class_order, ax=axes[0, 0], palette='turbo', showfliers=False)
axes[0, 0].set_title('Duração do Fluxo [log10(microsegundos)]', fontweight='bold')
axes[0, 0].set_xlabel('log10(Flow Duration + 1)')
axes[0, 0].set_ylabel('')

sns.boxplot(data=df_box, x='Packet Length Mean', y='Label', order=class_order, ax=axes[0, 1], palette='turbo', showfliers=False)
axes[0, 1].set_title('Tamanho Médio de Pacote (Bytes)', fontweight='bold')
axes[0, 1].set_xlabel('Packet Length Mean')
axes[0, 1].set_ylabel('')

sns.boxplot(data=df_box, x='FWD Init Win Bytes', y='Label', order=class_order, ax=axes[1, 0], palette='turbo', showfliers=False)
axes[1, 0].set_title('Tamanho da Janela TCP Inicial (FWD Init Win Bytes)', fontweight='bold')
axes[1, 0].set_xlabel('FWD Init Win Bytes')
axes[1, 0].set_ylabel('')

df_box['Total Fwd Packet Log'] = np.log10(np.maximum(df_box['Total Fwd Packet'], 1.0))
sns.boxplot(data=df_box, x='Total Fwd Packet Log', y='Label', order=class_order, ax=axes[1, 1], palette='turbo', showfliers=False)
axes[1, 1].set_title('Volume de Pacotes Enviados [log10(Fwd Packets)]', fontweight='bold')
axes[1, 1].set_xlabel('log10(Total Fwd Packet)')
axes[1, 1].set_ylabel('')

for ax in axes.flat:
    ax.grid(True, linestyle='--', alpha=0.5)

plt.suptitle('CSE-CIC-IDS2018 (Corrigido): Dispersão de Métricas de Fluxo por Classe', fontsize=16, fontweight='bold', y=1.01)
save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_Features_Boxplots")
del df_box, df_feat, tbl_feat

# =============================================================================
# FIGURA 8: Perfil Médio de Flags TCP por Classe
# =============================================================================
print("Gerando Figura 8: Perfil Médio de Flags TCP por Classe...")
flag_cols = ['FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'ECE Flag Count']
tbl_flags = pq.read_table(str(PARQUET_PATH), columns=['Label'] + flag_cols)
df_flags = tbl_flags.to_pandas()
flag_means = df_flags.groupby('Label')[flag_cols].mean().loc[class_order]

fig, ax = plt.subplots(figsize=(15, 7.5))
flag_means.plot(kind='bar', stacked=True, ax=ax, colormap='tab10', alpha=0.9, edgecolor='black', linewidth=0.5)
ax.set_title('CSE-CIC-IDS2018 (Corrigido): Perfil Médio de Flags TCP por Classe de Ataque e BENIGN', fontsize=13.5, fontweight='bold')
ax.set_ylabel('Média de Ocorrência de Flags por Fluxo', fontsize=11.5)
ax.set_xlabel('Classe', fontsize=11.5)
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right', fontweight='semibold')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(title='Flags TCP', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)

save_fig(fig, "Dataset_CSECICIDS2018_Corrigido_TCP_Flags")
del df_flags, tbl_flags

print("\n" + "=" * 70)
print("Todas as figuras foram geradas e salvas com sucesso em:")
print(f"  - Tese:      {THESIS_FIG_DIR}")
print(f"  - EDA Plots: {EDA_PLOTS_DIR}")
print(f"  - Artefatos: {ARTIFACT_PLOTS_DIR}")
print("=" * 70)
