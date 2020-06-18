# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# #!usr/bin/bash/python3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib_venn import venn3_circles, venn3_unweighted
from matplotlib_venn import _common, _venn3

datafile = '../../data/cleanBib_citations.csv'
df = pd.read_csv(datafile)
df.head()
# -

list(df.columns)


def venn_of_df(df):
    subsets = []
    for col in df.columns:
        s = set(df.index[df[col] > 0].tolist())
        subsets.append(s)

    labels = [label.replace('_', ' ').capitalize() for label in df.columns]

    v = venn3_unweighted(subsets, set_labels=labels)
    areas = (1, 1, 1, 1, 1, 1, 1)
    centers, radii = _venn3.solve_venn3_circles(areas)
    ax = plt.gca()
    _common.prepare_venn_axes(ax, centers, radii)


cols = ['paper_citation', 'code_citation', 'diversity_statement']   
venn_of_df(df[cols])
plt.title('Counts of whether papers contain \n' +\
          'a diversity statement, a citation of the paper, \n' +\
          'and/or a citation of the preprint', fontsize=14)
plt.tight_layout()
plt.savefig('../../reports/figures/venn_diagram_content.png')

plt.figure()
cols = ['paper_opencitations',
 'paper_googlescholar',
 'code_googlescholar']
venn_of_df(df[cols])
plt.title('Where did we find the papers? \n', fontsize=14)
plt.tight_layout()
plt.savefig('../../reports/figures/venn_diagram_sources.png')

n_preprints = df['preprint'].sum()
n_articles = len(df) - df['preprint'].sum()
print(f'{n_preprints} preprints, {n_articles} journal articles')

n_by_bassett = df['bassett_author'].sum()
n_not_by_bassett = len(df) - n_by_bassett
print(f'{n_by_bassett} including Dani Bassett as an author, {n_not_by_bassett} not')
