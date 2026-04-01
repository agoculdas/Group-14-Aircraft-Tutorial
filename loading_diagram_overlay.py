"""
Overlay loading diagrams for CRJ1000 and CRJ-EXX.
Reads data from Adsee3Plane.xlsx and produces a single figure.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

XLSX = "Adsee3Plane.xlsx"

def extract_loading(sheet_name, xls, oew_row, fuel_row):
    df = pd.read_excel(xls, sheet_name, header=None)
    masses_fwd, xcg_fwd = [], []
    masses_aft, xcg_aft = [], []
    for idx in range(oew_row, fuel_row + 1):
        m_f, m_a = df.iloc[idx, 12], df.iloc[idx, 13]
        x_f, x_a = df.iloc[idx, 18], df.iloc[idx, 19]
        if pd.notna(m_f) and pd.notna(x_f):
            masses_fwd.append(float(m_f)); xcg_fwd.append(float(x_f))
        if pd.notna(m_a) and pd.notna(x_a):
            masses_aft.append(float(m_a)); xcg_aft.append(float(x_a))
    tags = {}
    for idx in range(oew_row, fuel_row + 1):
        tag = df.iloc[idx, 20]
        if pd.notna(tag):
            tags[idx - oew_row] = str(tag).strip()
    return (np.array(xcg_fwd), np.array(masses_fwd),
            np.array(xcg_aft), np.array(masses_aft), tags)

def plot_loading_path(ax, xcg_fwd, m_fwd, xcg_aft, m_aft, tags, color):
    ax.plot(xcg_fwd, m_fwd, "-", color=color, lw=1.6)
    ax.plot(xcg_aft, m_aft, "-", color=color, lw=1.6, alpha=0.45)
    marker_map = {"CARGO 1": "s", "CARGO 2": "D", "PAX": "^", "FUEL": "o"}
    for i, tag in tags.items():
        if tag in marker_map and i < len(m_fwd):
            ax.plot(xcg_fwd[i], m_fwd[i], marker_map[tag], color=color, ms=5.5, zorder=5)
            ax.plot(xcg_aft[i], m_aft[i], marker_map[tag], color=color, ms=5.5, zorder=5, alpha=0.45)

xls = pd.ExcelFile(XLSX)
xf1, mf1, xa1, ma1, t1 = extract_loading("Part I",  xls, 14, 67)
xf2, mf2, xa2, ma2, t2 = extract_loading("Part II", xls, 18, 71)

fig, ax = plt.subplots(figsize=(8, 9.5))

plot_loading_path(ax, xf1, mf1, xa1, ma1, t1, color="#1f77b4")
plot_loading_path(ax, xf2, mf2, xa2, ma2, t2, color="#d62728")

# OEW annotations
ax.plot(xf1[0], mf1[0], "o", color="#1f77b4", ms=7, zorder=6)
ax.annotate("OEW", (xf1[0], mf1[0]), textcoords="offset points",
            xytext=(8, -4), fontsize=8, color="#1f77b4")
ax.plot(xf2[0], mf2[0], "o", color="#d62728", ms=7, zorder=6)
ax.annotate("OEW+Batt", (xf2[0], mf2[0]), textcoords="offset points",
            xytext=(8, -4), fontsize=8, color="#d62728")

# MTOW - upper left
ax.axhline(40823, color="grey", ls="--", lw=0.8, alpha=0.6)
ax.annotate("MTOW = 40 823 kg", (0.16, 40823), textcoords="offset points",
            xytext=(0, 5), fontsize=7, color="grey")

# Legend - upper right
h_crj = mlines.Line2D([], [], color="#1f77b4", lw=1.6, label="CRJ1000")
h_exx = mlines.Line2D([], [], color="#d62728", lw=1.6, label="CRJ-EXX")
h_fwd = mlines.Line2D([], [], color="black", lw=1.6, alpha=1.0,
                       label="Fwd CG path (cargo fwd first)")
h_aft = mlines.Line2D([], [], color="black", lw=1.6, alpha=0.40,
                       label="Aft CG path (cargo aft first)")
h_oew   = mlines.Line2D([], [], color="black", marker="o", ls="None", ms=6,
                         label="OEW / MTOW (fuel loaded)")
h_cargo = mlines.Line2D([], [], color="black", marker="s", ls="None", ms=5.5,
                         label="Cargo hold 1 loaded")
h_carg2 = mlines.Line2D([], [], color="black", marker="D", ls="None", ms=5.5,
                         label="Cargo hold 2 loaded")
h_pax   = mlines.Line2D([], [], color="black", marker="^", ls="None", ms=5.5,
                         label="Pax boarding start")

ax.legend(handles=[h_crj, h_exx, h_fwd, h_aft, h_oew, h_cargo, h_carg2, h_pax],
          loc="upper right", fontsize=8, framealpha=0.92,
          handlelength=2.2, borderpad=0.8, labelspacing=0.5,
          title="Legend", title_fontsize=9)

ax.set_xlabel(r"$\bar{x}_{cg}$ / MAC", fontsize=11)
ax.set_ylabel("Aircraft mass [kg]", fontsize=11)
ax.set_title("Loading Diagram — CRJ1000 vs CRJ-EXX\n(Front cargo 30 %, Aft cargo 70 %)", fontsize=12)
ax.set_xlim(0.15, 0.70)
ax.set_ylim(23188 - 200, 41500)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("loading_diagram_overlay.pdf", dpi=300)
fig.savefig("loading_diagram_overlay.png", dpi=300)
print("Saved loading_diagram_overlay.pdf / .png")
plt.show()
