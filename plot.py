import cPickle as pkl
import matplotlib.pyplot as plt
import sys
try: filename = sys.argv[1]
except: filename = None

smooth_radius = 2
xlim = 10
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
plt.scatter(xs, y1, color="blue", marker='+', s=10)
plt.scatter(xs, y2, color="red", marker='+', s=10)
plt.scatter(xs, y3, color="purple", marker='+', s=10)
plt.plot(xs, smooth(xs, y1), color="blue", label='mean', linewidth=2)
plt.plot(xs, smooth(xs, y2), color="red", label='var', linewidth=2)
plt.plot(xs, smooth(xs, y3), color="purple", label='shared', linewidth=2)

plt.xlim(0, xlim)
plt.ylabel('unique rsquared')
plt.xlabel('clade grouping percentile')
plt.legend(loc='upper left')
if log: plt.xscale('log')

if filename: plt.savefig(filename)
else: plt.show()