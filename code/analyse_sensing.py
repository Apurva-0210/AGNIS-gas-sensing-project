"""Step means, fits and enhancement for every gas.

Run:  python code/analyse_sensing.py
Writes data/sensing/derived/results.json and step_means_all_gases.csv
Definitions: S_RED = R0/Rs ; S_OX = Rs/R0 ; R0 = clean-air baseline of the same run.
"""
import json, os, csv, collections
import numpy as np
from scipy.optimize import curve_fit
from sensing_lib import load, DERIVED, MAIN_CHANNEL

def segments(rows):
    seg, cur = [], None
    for x in rows:
        if cur is None or x['cert_ppm'] != cur[0]:
            cur = [x['cert_ppm'], []]; seg.append(cur)
        cur[1].append(x)
    return seg

res = {}
for g in ['NO2', 'VOC', 'NH3', 'CO']:
    c = MAIN_CHANNEL[g]; res[g] = {'ch': c}
    for sn in ['COATED', 'UNCOATED']:
        rows = load(f'{g}_{sn}_Elsevier_Clean.csv'); t0 = rows[0]['time_s']
        d = collections.defaultdict(lambda: {'S': [], 'Rs': []})
        for p, xs in segments(rows):
            if p == 0: continue
            for x in xs:
                d[p]['S'].append(x['Sensitivity_%s_SGX' % c]); d[p]['Rs'].append(x['Rs_%s_ohm' % c])
        res[g][sn] = {
            'steps': {str(p): {'S': float(np.mean(v['S'])), 'sd': float(np.std(v['S'], ddof=1)),
                               'Rs': float(np.mean(v['Rs'])), 'n': len(v['S'])} for p, v in sorted(d.items())},
            'R0_RED': rows[0]['R0_RED_clean_air_ohm'], 'R0_OX': rows[0]['R0_OX_clean_air_ohm'],
            't': [x['time_s'] - t0 for x in rows], 'y': [x['Rs_R0_%s' % c] for x in rows],
            'ppm': [x['cert_ppm'] for x in rows], 'temp': [x['temp_C'] for x in rows]}
        s = res[g][sn]['steps']; C = np.array([float(k) for k in s]); S = np.array([s[k]['S'] for k in s])
        out = {'n': len(C)}
        pw = lambda C, A, B: A * C ** B
        try:
            p, _ = curve_fit(pw, C, S, p0=[1, 0.5], maxfev=20000); pred = pw(C, *p)
            out['pow'] = (p.tolist(), 1 - np.sum((S - pred) ** 2) / np.sum((S - S.mean()) ** 2), float(np.sqrt(np.mean((S - pred) ** 2))))
        except Exception:
            out['pow'] = None
        q = np.polyfit(C, S, 2); pred = np.polyval(q, C)
        out['poly'] = (q.tolist(), 1 - np.sum((S - pred) ** 2) / np.sum((S - S.mean()) ** 2), float(np.sqrt(np.mean((S - pred) ** 2))))
        res[g][sn]['fit'] = out

json.dump(res, open(os.path.join(DERIVED, 'results.json'), 'w'))
with open(os.path.join(DERIVED, 'step_means_all_gases.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['gas', 'element', 'concentration_ppm', 'S_coated', 'S_uncoated', 'enhancement_pct', 'enhancement_factor',
                'Rs_coated_ohm', 'Rs_uncoated_ohm', 'SD_S_coated', 'SD_S_uncoated', 'n_coated', 'n_uncoated'])
    for g in ['NO2', 'VOC', 'NH3', 'CO']:
        c = res[g]['COATED']['steps']; b = res[g]['UNCOATED']['steps']
        for k in sorted(set(c) | set(b), key=float):
            e = ef = ''
            if k in c and k in b:
                e = (c[k]['S'] - b[k]['S']) / b[k]['S'] * 100; ef = c[k]['S'] / b[k]['S']
            w.writerow([g, res[g]['ch'], k, c[k]['S'] if k in c else '', b[k]['S'] if k in b else '', e, ef,
                        c[k]['Rs'] if k in c else '', b[k]['Rs'] if k in b else '', c[k]['sd'] if k in c else '',
                        b[k]['sd'] if k in b else '', c[k]['n'] if k in c else '', b[k]['n'] if k in b else ''])
print('written results.json and step_means_all_gases.csv')
