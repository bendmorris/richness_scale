#!/usr/bin/env python
import Bio.Phylo as bp
import csv
import numpy as np
import scipy.stats as s
from geophy.cluster import color_clusters
import statsmodels.api as sm
import cPickle as pkl
import sys
dataset = sys.argv[1]


tree = bp.read('data/%s.new' % dataset, 'newick')
tips = tree.get_terminals()
all_species = {t.name: t for t in tips}

with open('data/%s_env_data.pkl' % dataset, 'r') as pickle_file:
    mean_data, var_data = pkl.load(pickle_file)

routes = {}
#count_data_spp = set()
with open('data/%s.csv' % dataset) as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for route, lat, lon, genus, species, count in reader:
        route = (round(float(lat), 3), round(float(lon), 3))
        spname = '%s %s' % (genus, species)
        if not spname in all_species: continue
        #count_data_spp.add(spname)
        #count = int(count)
        if not route in routes: routes[route] = set()
        routes[route].add(spname)


data = {}
color_clusters(tree, threshold=0, draw=False, 
               all_colors=xrange(len(tips)),
               color_attr='group', min_clade_size=1)
thresholds = [0] + sorted(set([s.percentileofscore(tree._distances, clade._med_distance) 
                               for clade in tree.find_elements()
                               if hasattr(clade, '_med_distance')]))
print thresholds
for threshold in thresholds:
    if threshold > 50: break
    sys.stdout.write(str(threshold) + '...')
    sys.stdout.flush()
    color_clusters(tree, threshold=threshold, draw=False, 
                   all_colors=xrange(len(tips)),
                   color_attr='group', min_clade_size=1)
    print 'done'
    x1 = []
    x2 = []
    y = []
    for route, spp in routes.iteritems():
        richness = set()
        if None in mean_data[route] or None in var_data[route]: continue
        try:
            x1.append(mean_data[route])
            x2.append(var_data[route])
        except KeyError: continue
        for sp in spp:
            if sp in all_species and hasattr(all_species[sp], 'group'):
                richness.add(all_species[sp].group)
        y.append(float(len(richness)))

    x3 = [[1]+a+b for (a,b) in zip(x1, x2)]
    x1 = [[1] + x for x in x1]
    x2 = [[1] + x for x in x2]

    results = [sm.OLS(y, x).fit().rsquared 
               for x in (x1, x2, x3)]
    print results
    if all([0 <= result <= 1 for result in results]):
        data[threshold] = results
    else: continue

with open('data/%s_richness_correlates.pkl' % dataset, 'wb') as pickle_file:
    pkl.dump(data, pickle_file, -1)

