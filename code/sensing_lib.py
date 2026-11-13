"""Loader for the cleaned sensing CSV files."""
import csv, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CLEAN = os.path.join(ROOT, 'data', 'sensing', 'clean_csv')
DERIVED = os.path.join(ROOT, 'data', 'sensing', 'derived')
FIGS = os.path.join(ROOT, 'figures')
# main sensing element used for each gas in the manuscript
MAIN_CHANNEL = {'CO': 'RED', 'VOC': 'RED', 'NO2': 'OX', 'NH3': 'OX'}

def load(name):
    """Read one clean CSV (e.g. 'VOC_COATED_Elsevier_Clean.csv') into a list of dicts."""
    rows = list(csv.DictReader(open(os.path.join(CLEAN, name))))
    for r in rows:
        for k in r:
            if k not in ('sensor', 'gas'):
                try:
                    r[k] = float(r[k])
                except ValueError:
                    pass
    return rows
