# -*- coding: utf-8 -*-
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

# # get the percentages from the diversity statement texts

# possible labels depending on how many percentages are given
possible_labels = {
    4: ['mm', 'mf', 'fm', 'ff'],
    5: ['mm', 'mf', 'fm', 'ff', 'unknown'],
    6: ['mm', 'mf', 'fm', 'ff', 'nonbinary','unknown'],
    8: ['mm', 'mf', 'fm', 'ff', 
        'rel_mm', 'rel_mf', 'rel_fm', 'rel_ff'],
    9: ['mm', 'mf', 'fm', 'ff', 
        'rel_mm', 'rel_mf', 'rel_fm', 'rel_ff'],
    10: ['mm', 'mf', 'fm', 'ff', 'unknown',
        'rel_mm', 'rel_mf', 'rel_fm', 'rel_ff', 'relunknown'],
    11: ['mm', 'mf', 'fm', 'ff', 'nonbinary', 'unknown',
        'rel_mm', 'rel_mf', 'rel_fm', 'rel_ff', 'relunknown'],
}

# +
import pprint
import re

pattern = '\−*\s*\d*.\d*\s*\%'
for n, text in enumerate(df['ds_text']):    
    strs = re.findall(pattern, text)
    strs = [s.replace("−", "-") for s in strs]
    strs = [re.sub('[A-Za-z,]', '', s) for s in strs]
    
    ints = [float(s[:-1]) for s in strs]
    
    if len(ints) > 0:
        labels = possible_labels[len(ints)]    
        d = dict(zip(labels, ints))
    else: 
        d = {}
    df.loc[n, ('percentages')] = [d]
            

# +
lists_percents = {'mm': [],
                 'mf': [],
                 'fm': [],
                 'ff': [],
}

for d in df['percentages']:
    if len(d) > 0:
        for key in lists_percents.keys():
            lists_percents[key].append(d[key])

# +
dataset = lists_percents.values()



# +
# %matplotlib inline
import matplotlib
matplotlib.rc('font', **{'size': 14})

fig, axes = plt.subplots(figsize=(5,5))
dataset = list(lists_percents.values())
axes.violinplot(dataset=dataset)
axes.set_ylabel('% of citations in paper')
axes.set_xticks(range(len(lists_percents) + 1))
ticks = ['', 'male\nmale', 'male\nfemale', 'female\nmale', 'female\nfemale']
axes.set_xticklabels(ticks)
plt.title('Citations in papers that\n' +\
          'cite the paper on citation bias')
plt.tight_layout()
plt.savefig('../../reports/figures/violinplot_percentages.png')
