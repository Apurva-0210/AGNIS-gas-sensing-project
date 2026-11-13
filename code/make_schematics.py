"""Draws the two schematic figures (synthesis route and proposed sensing mechanism) as vector graphics.

Run:  python code/make_schematics.py
Writes figures/schematic_synthesis.pdf/.png and figures/schematic_mechanism.pdf/.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle, Ellipse, FancyArrowPatch, Wedge, Arc

OUT = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'figures')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42, 'mathtext.default': 'regular'})

def box(ax, x, y, w, h, fc, ec='none', lw=0.8, r=1.2, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw, zorder=z))

def fit_text(ax, x, y, s, fs, maxw, floor=5.0, **kw):
    """Draw text and shrink the font until it fits within maxw data units."""
    tx = ax.text(x, y, s, fontsize=fs, **kw)
    r = ax.figure.canvas.get_renderer(); inv = ax.transData.inverted()
    while fs > floor:
        bb = tx.get_window_extent(r)
        if inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0] <= maxw: break
        fs -= 0.2; tx.set_fontsize(fs)
    return tx

# ------------------------------------------------------------------ synthesis
def beaker(ax, cx, cy, s=1.0, liquid='#cfe3f5', liq_h=0.55, stirrer=False, liq_edge='#7aa6cf'):
    w, h = 9 * s, 12 * s
    ax.add_patch(Polygon([[cx - w / 2, cy + h], [cx - w / 2, cy], [cx + w / 2, cy], [cx + w / 2, cy + h]], closed=False, fc='#f4f9fd', ec='#5b6f82', lw=0.8, zorder=4))
    ax.add_patch(Rectangle((cx - w / 2 + 0.2, cy + 0.2), w - 0.4, h * liq_h, fc=liquid, ec=liq_edge, lw=0.4, zorder=3))
    ax.plot([cx - w / 2 - 0.8 * s, cx - w / 2], [cy + h + 0.5 * s, cy + h], color='#5b6f82', lw=0.8, zorder=4)
    if stirrer:
        ax.plot([cx + 0.5 * s, cx + 3.5 * s], [cy + h * liq_h * 0.6, cy + h + 5 * s], color='#6b6b6b', lw=1.6, zorder=5)
        ax.add_patch(Rectangle((cx + 3.0 * s, cy + h + 3.5 * s), 1.6 * s, 3.5 * s, angle=-15, fc='#9aa0a6', ec='#555', lw=0.5, zorder=5))

def step1(ax, x0, w):
    cx = x0 + w / 2
    ax.add_patch(Polygon([[cx - 6, 15.2], [cx + 6, 15.2], [cx + 7.5, 17.2], [cx - 7.5, 17.2]], fc='#d5dbe1', ec='#5b6f82', lw=0.6, zorder=2))
    ax.add_patch(Rectangle((cx - 7.5, 15.0), 15, 2.2, fc='#c3cbd3', ec='#5b6f82', lw=0.6, zorder=2))
    beaker(ax, cx, 17.2, s=1.0, liq_h=0.5)

def step2(ax, x0, w):
    cx = x0 + w / 2 - 1.5
    for i, (yy, hh) in enumerate([(15.5, 3.2), (19.0, 3.2), (22.5, 3.2)]):
        ax.add_patch(FancyBboxPatch((cx - 5.2, yy), 10.4, hh, boxstyle='round,pad=0,rounding_size=0.8', fc='#aeb4ba', ec='#4d555c', lw=0.7, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - 6.2, 26.0), 12.4, 3.0, boxstyle='round,pad=0,rounding_size=0.8', fc='#c4c9ce', ec='#4d555c', lw=0.7, zorder=3))
    for dx in (-4.6, -1.6, 1.6, 4.6):
        ax.add_patch(Rectangle((cx + dx - 0.8, 29.0), 1.6, 1.2, fc='#8a9096', ec='#4d555c', lw=0.5, zorder=3))
    ax.add_patch(Rectangle((cx - 1.2, 29.0), 2.4, 2.4, fc='#9aa0a6', ec='#4d555c', lw=0.5, zorder=3))
    ax.add_patch(Circle((cx + 6.8, 17.5), 4.2, fc='#eeeeee', ec='#555', lw=0.9, zorder=5))
    ax.add_patch(FancyBboxPatch((cx + 4.6, 15.4), 4.4, 4.6, boxstyle='round,pad=0,rounding_size=0.6', fc='#fafafa', ec='#777', lw=0.6, zorder=6))

def step3(ax, x0, w):
    cx = x0 + w / 2
    ax.add_patch(FancyBboxPatch((cx - 9.2, 15.2), 18.4, 10.5, boxstyle='round,pad=0,rounding_size=2', fc='#d7ebfa', ec='#4f7fb0', lw=0.9, zorder=2))
    rng = np.random.default_rng(3)
    for _ in range(18):
        xx = cx - 8.2 + rng.random() * 16.4; yy = 15.8 + rng.random() * 3.0
        ax.add_patch(Rectangle((xx, yy), 1.4, 1.4, angle=rng.random() * 40, fc='white', ec='#8fb5d6', lw=0.4, zorder=3))
    ax.add_patch(Rectangle((cx - 4.3, 17.5), 8.6, 11.5, fc='#e9f2f9', ec='#5b6f82', lw=0.7, zorder=4))
    ax.add_patch(Rectangle((cx - 4.1, 17.7), 8.2, 6.0, fc='#2f5d3a', ec='none', zorder=4))
    ax.plot([cx + 0.2, cx + 2.6], [20.0, 33.2], color='#6b6b6b', lw=1.6, zorder=5)
    ax.add_patch(Rectangle((cx + 1.9, 31.4), 1.8, 3.6, angle=-12, fc='#9aa0a6', ec='#555', lw=0.5, zorder=5))

def step4(ax, x0, w):
    cx = x0 + w / 2
    ax.add_patch(Polygon([[cx - 7.4, 16.5], [cx + 7.4, 16.5], [cx + 8.2, 25.5], [cx - 8.2, 25.5]], fc='#c9ced3', ec='#59626b', lw=0.8, zorder=2))
    ax.add_patch(Polygon([[cx - 6.8, 22.0], [cx + 6.8, 22.0], [cx + 7.4, 24.6], [cx - 7.4, 24.6]], fc='#cfe3f5', ec='#7aa6cf', lw=0.5, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - 2.4, 20.2), 4.8, 9.0, boxstyle='round,pad=0,rounding_size=0.7', fc='#eef5fb', ec='#59626b', lw=0.7, zorder=4))
    ax.add_patch(Rectangle((cx - 2.2, 20.4), 4.4, 4.0, fc='#2f5d3a', ec='none', zorder=4))
    ax.add_patch(Rectangle((cx - 2.6, 29.2), 5.2, 2.2, fc='#222', ec='none', zorder=4))
    ax.add_patch(Rectangle((cx - 5.5, 17.6), 5.0, 2.4, fc='#7e8e9e', ec='none', zorder=4))
    for k in (1, 2, 3):
        ax.add_patch(Arc((cx + 4.6, 19.0), 1.6 * k, 1.6 * k, theta1=-50, theta2=50, color='#3a6ea5', lw=0.7, zorder=5))

def step5(ax, x0, w):
    cx = x0 + w / 2
    ax.add_patch(Polygon([[cx - 7, 15.0], [cx + 5, 15.0], [cx + 8, 19.0], [cx - 4, 19.0]], fc='#3f7d4d', ec='#27472f', lw=0.8, zorder=2))
    ax.add_patch(Polygon([[cx - 3.6, 15.9], [cx + 2.6, 15.9], [cx + 4.2, 18.1], [cx - 2.0, 18.1]], fc='#d7b84a', ec='#8a7421', lw=0.5, zorder=3))
    ax.add_patch(Circle((cx + 0.0, 17.0), 1.1, fc='#2f5d3a', ec='none', zorder=4))
    ax.add_patch(Polygon([[cx + 0.9, 18.0], [cx + 0.1, 18.0], [cx + 3.8, 30.0], [cx + 5.4, 30.0]], fc='#dfe3e8', ec='#59626b', lw=0.6, zorder=4))
    ax.add_patch(Polygon([[cx + 3.5, 30.0], [cx + 6.1, 30.0], [cx + 6.9, 34.5], [cx + 4.3, 34.5]], fc='#6f8fbf', ec='#3e5a85', lw=0.6, zorder=4))

def synthesis():
    fig, ax = plt.subplots(figsize=(6.0, 3.54)); ax.set_xlim(0, 100); ax.set_ylim(-5, 54); ax.axis('off')
    W, G = 18.4, 2.0
    cols = [
        ('Step 1:\nPrecursors', '#dbe8f6', '#3f6fa8', ['NH$_4$VO$_3$ + AgNO$_3$', 'in water', 'pH ≈ 4.5 (HNO$_3$)'], ['sonicate 10 min'], 'precursor\nsuspension', step1),
        ('Step 2:\nHydrothermal', '#dbe8f6', '#3f6fa8', ['autoclave', '140 °C, 12–18 h'], ['centrifuge,', 'wash, dry 60 °C'], 'precursor powder\n(target β-AgVO$_3$)', step2),
        ('Step 3:\nPolymerisation', '#f7dcdc', '#b04a4a', ['1 M HCl, 0–5 °C', '+ powder, aniline', '+ APS'], ['3–4 h, stirring', 'wash, dry 50 °C'], 'dark-green PANI\ncomposite', step3),
        ('Step 4:\nCoating ink', '#dcefd9', '#3d7a43', ['composite, 5 mg', 'ethanol / water', '+ 1 % chitosan'], ['sonicate 20 min'], 'chitosan-\nstabilised ink', step4),
        ('Step 5:\nIntegration', '#e7f1cf', '#6b8e23', ['1 µL drop-cast', 'on MiCS-4514'], ['dry 50–60 °C', 'burn-in 24–28 h', 'at 5 V DC'], 'coated\nMiCS-4514', step5),
    ]
    fig.canvas.draw()
    for i, (title, fc, ec, top, bot, res, icon) in enumerate(cols):
        x0 = i * (W + G); cx = x0 + W / 2; mw = W - 1.6
        box(ax, x0, -4.0, W, 49.0, fc, r=1.6, z=0)
        box(ax, x0, 46.0, W, 7.6, fc, ec=ec, lw=1.0, r=1.4, z=1)
        fit_text(ax, cx, 49.8, title, 7.0, mw, ha='center', va='center', fontweight='bold', linespacing=1.1, zorder=3)
        for j, s in enumerate(top):
            fit_text(ax, cx, 42.0 - j * 2.6, s, 6.6, mw, ha='center', va='center', zorder=3)
        icon(ax, x0, W)
        for j, s in enumerate(bot):
            fit_text(ax, cx, 12.4 - j * 2.6, s, 6.6, mw, ha='center', va='center', zorder=3)
        ax.annotate('', xy=(cx, 1.6), xytext=(cx, 3.0), arrowprops=dict(arrowstyle='-|>', lw=0.8, color='k', mutation_scale=6), zorder=3)
        fit_text(ax, cx, -1.1, res, 6.4, mw, ha='center', va='center', fontweight='bold', linespacing=1.05, zorder=3)
        if i < 4:
            ax.annotate('', xy=(x0 + W + G + 0.3, 25), xytext=(x0 + W - 0.3, 25), arrowprops=dict(arrowstyle='-|>', lw=1.2, color='k', mutation_scale=8), zorder=5)
    fig.savefig(os.path.join(OUT, 'schematic_synthesis.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(OUT, 'schematic_synthesis.png'), bbox_inches='tight', pad_inches=0.03, dpi=600); plt.close(fig)

# ------------------------------------------------------------------ mechanism
def slab(ax, x, y, w, h, dx, dy, front, top, side, ec='#37424d', z=2, lw=0.7):
    ax.add_patch(Polygon([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], fc=front, ec=ec, lw=lw, zorder=z))
    ax.add_patch(Polygon([[x, y + h], [x + w, y + h], [x + w + dx, y + h + dy], [x + dx, y + h + dy]], fc=top, ec=ec, lw=lw, zorder=z))
    ax.add_patch(Polygon([[x + w, y], [x + w + dx, y + dy], [x + w + dx, y + h + dy], [x + w, y + h]], fc=side, ec=ec, lw=lw, zorder=z))

def molecule(ax, x, y, kind):
    def atom(px, py, r, c): ax.add_patch(Circle((px, py), r, fc=c, ec='#333', lw=0.4, zorder=6))
    if kind == 'CO':
        atom(x - 1.3, y, 1.3, '#8a8a8a'); atom(x + 1.1, y, 1.2, '#d02b2b')
    elif kind == 'NH3':
        atom(x, y + 0.3, 1.5, '#2f55c4')
        for dx in (-1.8, 1.8): atom(x + dx, y - 1.0, 0.8, 'white')
        atom(x, y - 1.8, 0.8, 'white')
    elif kind == 'NO2':
        atom(x, y + 0.5, 1.4, '#2f55c4'); atom(x - 2.0, y - 0.9, 1.2, '#d02b2b'); atom(x + 2.0, y - 0.9, 1.2, '#d02b2b')
    else:
        atom(x - 1.6, y - 0.4, 1.2, '#8a8a8a'); atom(x + 0.2, y + 0.6, 1.2, '#8a8a8a'); atom(x + 1.9, y - 0.3, 1.0, '#d02b2b'); atom(x + 0.2, y - 1.5, 0.7, 'white')

def mechanism():
    fig, ax = plt.subplots(figsize=(5.6, 3.5)); ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis('off')
    X, W, DX, DY = 22, 52, 9, 5
    # substrate with electrodes
    slab(ax, X, 2, W, 6, DX, DY, '#8e969d', '#c3c8cd', '#6f767c')
    for k in range(4):
        x1 = X + 4 + k * 12
        ax.add_patch(Polygon([[x1, 8], [x1 + 6, 8], [x1 + 6 + DX, 8 + DY], [x1 + DX, 8 + DY]], fc='#f1f1f1', ec='#8a8a8a', lw=0.4, zorder=3))
    ax.text(X + W / 2, 4.9, 'MiCS-4514 sensing element', ha='center', va='center', fontsize=6.0, color='white', fontweight='bold', zorder=5)
    # PANI layer with particles
    slab(ax, X, 17, W, 12, DX, DY, '#8fb6dc', '#b9d3ec', '#6f9cc7', z=2)
    rng = np.random.default_rng(7)
    pts = [(X + 8, 22.5), (X + 21, 25.0), (X + 33, 21.5), (X + 45, 24.8), (X + 14, 19.5), (X + 39, 19.2)]
    for px, py in pts:
        ax.add_patch(Circle((px, py), 1.9, fc='#d9bc5b', ec='#8a7421', lw=0.6, zorder=4))
        ax.add_patch(Circle((px - 0.5, py + 0.6), 0.5, fc='#f6e7a8', ec='none', zorder=5))
    # carriers in PANI
    for (px, py, t, c) in [(X + 4, 26.2, 'e$^-$', '#1b3c8a'), (X + 27, 18.8, 'h$^+$', '#a31d1d'), (X + 36, 26.3, 'e$^-$', '#1b3c8a'), (X + 48, 19.8, 'h$^+$', '#a31d1d'), (X + 17, 27.0, 'h$^+$', '#a31d1d')]:
        ax.text(px, py, t, fontsize=6.3, color=c, fontweight='bold', ha='center', va='center', zorder=6)
    # chitosan porous overlayer
    slab(ax, X, 36, W, 8, DX, DY, '#e3e6a8', '#f0f2c6', '#c9cd86', z=2)
    rng = np.random.default_rng(11)
    for _ in range(46):
        px = X + 1.2 + rng.random() * (W - 2.4); py = 36.8 + rng.random() * 6.4
        ax.add_patch(Ellipse((px, py), 1.5 * (0.6 + rng.random() * 0.8), 1.2 * (0.6 + rng.random() * 0.8), fc='#8f9549', ec='none', alpha=0.85, zorder=3))
    for _ in range(40):
        px = X + DX * 0.1 + rng.random() * (W + DX * 0.7); py = 44.4 + rng.random() * (DY - 1.2)
        ax.add_patch(Ellipse((px, py), 1.4, 0.9, fc='#a8ae5a', ec='none', alpha=0.8, zorder=3))
    # gas arrows and molecules
    gases = [('CO', X + 6, '#555555'), ('NH3', X + 21, '#2f55c4'), ('NO2', X + 36, '#c02b2b'), ('VOC', X + 51, '#2e7d4f')]
    for g, gx, c in gases:
        molecule(ax, gx + 4, 54.0, g)
        lab = {'CO': 'CO', 'NH3': 'NH$_3$', 'NO2': 'NO$_2$', 'VOC': 'VOC vapour'}[g]
        ax.text(gx + 4, 58.6, lab, ha='center', va='center', fontsize=7, color=c, fontweight='bold', zorder=6)
        ax.add_patch(FancyArrowPatch((gx + 4, 51.0), (gx + 4, 46.4), arrowstyle='-|>', mutation_scale=7, lw=1.4, color=c, zorder=6))
    # labels
    ax.text(1.0, 40.4, 'Chitosan binder /\nporous overlayer', ha='left', va='center', fontsize=6.6, linespacing=1.15)
    ax.plot([19.5, X - 0.3], [40.0, 40.0], color='k', lw=0.6)
    ax.text(1.0, 23.0, 'PANI matrix', ha='left', va='center', fontsize=6.6)
    ax.plot([13.5, X - 0.3], [23.0, 23.0], color='k', lw=0.6)
    ax.text(99.5, 31.0, 'Embedded\ninorganic\n(AgVO$_3$/AgCl)', ha='right', va='center', fontsize=6.3, linespacing=1.15)
    ax.plot([X + 45 + 1.9, 87.5], [24.8, 28.0], color='k', lw=0.6)
    ax.text(50, 0.4, 'Proposed reading: gas exposure shifts charge carriers in the PANI film, and the embedded inorganic phase modifies the interface.',
            ha='center', va='bottom', fontsize=0.1, alpha=0)
    fig.savefig(os.path.join(OUT, 'schematic_mechanism.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(OUT, 'schematic_mechanism.png'), bbox_inches='tight', pad_inches=0.03, dpi=600); plt.close(fig)

if __name__ == '__main__':
    synthesis(); mechanism(); print('schematics written')
