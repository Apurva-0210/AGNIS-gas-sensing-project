"""Rebuilds the XRD, FTIR and FESEM figures from the raw instrument files.

Run:  python code/make_characterisation_figures.py
Writes figures/xrd.pdf, figures/ftir.pdf, figures/fesem.png (and .tif).
XRD and FTIR are vector PDFs. FESEM panels are the unprocessed 768 x 768 pixel image areas
(linear 16-bit to 8-bit scaling only), with scale bars and labels drawn on top.
"""
import os, re, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
D = os.path.join(ROOT, 'data'); OUT = os.path.join(ROOT, 'figures')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.linewidth': 0.8, 'pdf.fonttype': 42})
BLUE, RED = '#1f5f8b', '#b5441f'

def read_xrd(name):
    th, it = [], []
    started = False
    for line in open(os.path.join(D, 'xrd', name)):
        if line.startswith('Angle'): started = True; continue
        if started:
            p = line.strip().split(',')
            if len(p) >= 3: th.append(float(p[0])); it.append(float(p[2]))
    return np.array(th), np.array(it)

def xrd():
    a, ia = read_xrd('AgVO3.csv'); b, ib = read_xrd('PA-HCl.csv')
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={'wspace': 0.25})
    m = a <= 60
    ax[0].plot(a[m], ia[m], color='0.75', lw=0.4)
    ax[0].plot(a[m], savgol_filter(ia[m], 7, 2), color=BLUE, lw=0.8)
    ax[0].set_xlim(5, 60); ax[0].set_ylim(0, 600)
    lab = {12.3: (12.3, 395), 17.1: (17.1, 440), 27.4: (21.5, 470), 28.2: (25.0, 540),
           31.4: (28.8, 470), 32.0: (33.0, 540), 32.8: (36.5, 470)}
    for x, (tx, ty) in lab.items():
        i = np.argmin(abs(a - x)); y = ia[max(0, i - 6):i + 7].max()
        ax[0].plot([x, tx], [y + 8, ty - 4], color='0.4', lw=0.4)
        ax[0].text(tx, ty, f'{x}', ha='center', va='bottom', fontsize=6.5)
    ax[0].set_xlabel(r'2$\theta$ (°), Cu K$\alpha$'); ax[0].set_ylabel('Intensity (counts)')
    ax[0].set_title('(a) Hydrothermal precursor', loc='left', fontsize=9)
    ax[1].plot(b, ib, color='0.75', lw=0.4); ax[1].plot(b, savgol_filter(ib, 5, 2), color=RED, lw=0.8)
    ax[1].set_xlim(5, 80); ax[1].set_ylim(0, 2150)
    for x in (12.3, 17.1, 24.9): ax[1].axvline(x, color=BLUE, lw=0.7, ls=':')
    hk = {27.9: '(111)', 32.3: '(200)', 46.3: '(220)', 55.0: '(311)', 57.6: '(222)', 67.6: '(400)', 76.7: '(420)'}
    for x, t in hk.items():
        i = np.argmin(abs(b - x)); y = ib[max(0, i - 5):i + 6].max()
        ax[1].text(x, y + 40, t, rotation=90, ha='center', va='bottom', fontsize=6.5)
    ax[1].text(36, 1900, 'dotted: strongest\nprecursor lines\n(12.3, 17.1, 24.9°),\nabsent here', color=BLUE, fontsize=6.5, va='top')
    ax[1].set_xlabel(r'2$\theta$ (°), Cu K$\alpha$')
    ax[1].set_title('(b) PANI–silver vanadate composite', loc='left', fontsize=9)
    for x in ax: x.spines[['top', 'right']].set_visible(False)
    fig.savefig(os.path.join(OUT, 'xrd.pdf'), bbox_inches='tight'); plt.close(fig)

def read_ir(name):
    x, y = [], []
    for line in open(os.path.join(D, 'ftir', name)):
        p = line.split()
        if len(p) == 2:
            try: x.append(float(p[0])); y.append(float(p[1]))
            except ValueError: pass
    return np.array(x), np.array(y)

def ftir():
    xa, ya = read_ir('PA-HCl.txt'); xb, yb = read_ir('AgVO3.txt')
    fig, ax = plt.subplots(2, 1, figsize=(3.6, 4.2), gridspec_kw={'hspace': 0.28})
    ax[0].plot(xa, ya, color=BLUE, lw=0.5); ax[0].set_xlim(4000, 400); ax[0].set_ylim(70, 96)
    for x, t, dy in [(1571, '1571', 3), (1472, '1472', -4), (1292, '1292', 3), (1236, '~1236', -4.5), (1135, '~1135', 3), (798, '~798', 3)]:
        i = np.argmin(abs(xa - x)); ax[0].text(x, ya[i] + dy, t, rotation=90, ha='center', va='bottom' if dy > 0 else 'top', fontsize=6.5)
    ax[0].set_ylabel('Transmittance (%)'); ax[0].text(0.03, 0.94, '(a) PA-HCl composite', transform=ax[0].transAxes, ha='left', va='top', fontsize=8, weight='bold')
    m = (xb <= 1100)
    ax[1].plot(xb[m], yb[m], color='#8b3a10', lw=0.6); ax[1].set_xlim(1100, 400); ax[1].set_ylim(20, 108)
    for x, t, dy in [(926, '926', -6), (908, '908', 5), (761, '761', 5), (625, '625', -6)]:
        i = np.argmin(abs(xb - x)); ax[1].text(x, yb[i] + dy, t, rotation=90, ha='center', va='bottom' if dy > 0 else 'top', fontsize=6.5)
    ax[1].text(470, 24.5, '~490', ha='center', va='bottom', fontsize=6.5)
    ax[1].set_ylabel('Transmittance (%)'); ax[1].set_xlabel(r'Wavenumber (cm$^{-1}$)')
    ax[1].text(0.03, 0.94, r'(b) AgVO$_3$ precursor', transform=ax[1].transAxes, ha='left', va='top', fontsize=8, weight='bold')
    for x in ax: x.grid(alpha=0.2, lw=0.4)
    fig.savefig(os.path.join(OUT, 'ftir.pdf'), bbox_inches='tight'); plt.close(fig)

def fesem():
    spec = [('AgVO3', '10.png', '(a)', 5), ('AgVO3', '8.png', '(b)', 2), ('PA-HCl', '4.png', '(c)', 10), ('PA-HCl', '11.png', '(d)', 2)]
    tiles = []
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44)
    for d, f, lab, um in spec:
        p = os.path.join(D, 'fesem', d, f)
        hdr = open(p.replace('.png', '-png.hdr')).read()
        px_nm = float(re.search(r'PixelSizeX=([\d.eE+-]+)', hdr).group(1)) * 1e9
        a = np.asarray(Image.open(p), float)[:768, :768] / 65535.0
        im = Image.fromarray((a * 255).round().astype(np.uint8)).convert('RGB')
        dr = ImageDraw.Draw(im)
        dr.text((16, 8), lab, fill=(255, 235, 0), font=font)
        L = int(round(um * 1000 / px_nm)); x1 = 768 - 24; x0 = x1 - L; y = 768 - 30
        dr.rectangle([x0, y, x1, y + 8], fill='white')
        t = f'{um} µm'; w = dr.textlength(t, font=font); dr.text((x1 - L / 2 - w / 2, y - 54), t, fill='white', font=font)
        tiles.append(im)
    g = 24
    sheet = Image.new('RGB', (768 * 2 + g, 768 * 2 + g), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % 2) * (768 + g), (i // 2) * (768 + g)))
    sheet.save(os.path.join(OUT, 'fesem.png'), dpi=(300, 300)); sheet.save(os.path.join(OUT, 'fesem.tif'), dpi=(300, 300), compression='tiff_lzw')

if __name__ == '__main__':
    xrd(); ftir(); fesem(); print('characterisation figures written')
