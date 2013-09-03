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


smooth_radius = 1
xlim = 20
log = False

with open('richness_correlates.pkl', 'rb') as pickle_file:
    data = pkl.load(pickle_file)

xs = [x for x in sorted(data.keys()) if x <= xlim]
y1 = []
y2 = []
y3 = []
for a, b, c in [data[x] for x in xs]:
    y1.append(c-b)
    y2.append(c-a)
    y3.append(c-y1[-1]-y2[-1])
def smooth(x, y):
    ys = []
    for xi, yi in zip(x, y):
        weights = [1 if xi == xi2 else (smooth_radius*xi**0.5) - abs(xi2 - xi) if abs(xi2-xi) < smooth_radius*xi**0.5 else 0 for xi2 in x]
        total_weight = sum(weights)
        ys.append(sum([y[n] * weights[n] / total_weight for n in range(len(x))]))
    return ys

a = plt.plot(xs, smooth(xs, y2), label='var', linewidth=2)
plt.scatter(xs, y2, marker='+', s=10, color=a[0].get_markeredgecolor())
a = plt.plot(xs, smooth(xs, y1), label='mean', linewidth=2)
plt.scatter(xs, y1, marker='+', s=10, color=a[0].get_markeredgecolor())
a = plt.plot(xs, smooth(xs, y3), label='shared', linewidth=2)
plt.scatter(xs, np.maximum(y3, 0), marker='+', s=10, color=a[0].get_markeredgecolor())

plt.xlim(0, xlim)
plt.ylim(0, round(max(y1+y2+y3) + 0.05, 1))
plt.ylabel('unique rsquared')
plt.xlabel('clade grouping percentile')
plt.legend(loc='upper left')
if log: plt.xscale('log')

layout.cross_spines(ax=plt.gca())

if filename: plt.savefig(filename)
else: plt.show()