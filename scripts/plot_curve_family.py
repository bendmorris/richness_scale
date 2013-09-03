#!/usr/bin/env python
import cPickle as pkl
import sys
try: filename = sys.argv[1]
except: filename = None
import matplotlib
if filename and filename.endswith('.svg'):
    matplotlib.use('SVG')
from mpltools import layout
from mpltools import style
style.use('ggplot')
import matplotlib.pyplot as plt
import numpy as np


xlim = 20
log = False

with open('data/group_richness.pkl', 'rb') as pickle_file:
    data = pkl.load(pickle_file)

for route, values in data.items():
    xs, ys = [v[0] for v in values], [v[1] for v in values]
    plt.plot(xs, ys)

plt.xlim(0, xlim)
plt.ylabel('group richness')
plt.xlabel('clade grouping percentile')
if log: plt.xscale('log')

layout.cross_spines(ax=plt.gca())

if filename: plt.savefig(filename)
else: plt.show()