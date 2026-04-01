"""
Plot CRJ1000 and CRJ-EXX scissor plots — individual, faceted, and combined.
"""

import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_data
from scissor import make_params, plot_single

data = load_data()
MAC = data["mac_calc"]["MAC"]
S_h = data["HT"]["S_h"]
S   = data["wing"]["S"]

params_1000 = make_params(data["aero"], data, MAC, S_h, S)
params_exx  = make_params(data["aero_exx"], data, MAC, S_h, S,
                          cg_extremes_key='cg_extremes_exx')

# Shared x range
all_fwd = min(params_1000['xcg_fwd'], params_exx['xcg_fwd'])
all_aft = max(params_1000['xcg_aft'], params_exx['xcg_aft'])
margin = 0.15
xcg_range = (all_fwd - margin, all_aft + margin)
xcg = np.linspace(xcg_range[0], xcg_range[1], 200)

# --- CRJ1000 standalone ---
fig1, ax1 = plt.subplots(figsize=(10, 7))
plot_single(ax1, xcg, params_1000)
ax1.set_xlabel('$\\bar{x}_{cg}$ / MAC')
ax1.set_ylabel('$S_h / S$')
ax1.set_title('Scissor Plot \u2014 CRJ1000')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(bottom=0)
plt.tight_layout()
fig1.savefig('scissor_plot_1000.png', dpi=200)

# --- CRJ-EXX standalone ---
fig2, ax2 = plt.subplots(figsize=(10, 7))
plot_single(ax2, xcg, params_exx)
ax2.set_xlabel('$\\bar{x}_{cg}$ / MAC')
ax2.set_ylabel('$S_h / S$')
ax2.set_title('Scissor Plot \u2014 CRJ-EXX')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(bottom=0)
plt.tight_layout()
fig2.savefig('scissor_plot_exx.png', dpi=200)

# --- Faceted side by side ---
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

plot_single(ax3a, xcg, params_1000)
ax3a.set_xlabel('$\\bar{x}_{cg}$ / MAC')
ax3a.set_ylabel('$S_h / S$')
ax3a.set_title('CRJ1000')
ax3a.legend(loc='best', fontsize=8)
ax3a.grid(True, alpha=0.3)
ax3a.set_ylim(bottom=0)

plot_single(ax3b, xcg, params_exx)
ax3b.set_xlabel('$\\bar{x}_{cg}$ / MAC')
ax3b.set_title('CRJ-EXX')
ax3b.legend(loc='best', fontsize=8)
ax3b.grid(True, alpha=0.3)

plt.tight_layout()
fig3.savefig('scissor_plot_faceted.png', dpi=200)

# --- Combined overlay ---
fig4, ax4 = plt.subplots(figsize=(12, 8))
plot_single(ax4, xcg, params_1000, label_prefix="CRJ1000",
            colors=('blue', 'red', 'gray'), linestyle='-')
plot_single(ax4, xcg, params_exx, label_prefix="CRJ-EXX",
            colors=('cyan', 'magenta', 'silver'), linestyle='--')
ax4.set_xlabel('$\\bar{x}_{cg}$ / MAC')
ax4.set_ylabel('$S_h / S$')
ax4.set_title('Scissor Plot Comparison \u2014 CRJ1000 vs CRJ-EXX')
ax4.legend(loc='best', fontsize=7, ncol=2)
ax4.grid(True, alpha=0.3)
ax4.set_ylim(bottom=0)
plt.tight_layout()
fig4.savefig('scissor_plot_comparison.png', dpi=200)

plt.show()
