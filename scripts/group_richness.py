#!/usr/bin/env python
import Bio.Phylo as bp
import csv
import numpy as np
import scipy.stats as s
from geophy.cluster import color_clusters
import statsmodels.api as sm
import cPickle as pkl
import sys


tree = bp.read('data/bbs.new', 'newick')
tips = tree.get_terminals()
all_species = {t.name: t for t in tips}

routes = {}
count_data_spp = set()
with open('data/bbs.csv') as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for route, lat, lon, genus, species, count in reader:
        spname = '%s %s' % (genus, species)
        if not spname in all_species: continue
        count_data_spp.add(spname)
        count = int(count)
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
data = {}
for threshold in thresholds:
    if threshold > 50: break
    sys.stdout.write(str(threshold) + '...')
    sys.stdout.flush()
    color_clusters(tree, threshold=threshold, draw=False, 
                   all_colors=xrange(len(tips)),
                   color_attr='group', min_clade_size=1)
    print 'done'
    for route, spp in routes.iteritems():
        if not route in data: data[route] = []
        richness = set()
        for sp in spp:
            if sp in all_species and hasattr(all_species[sp], 'group'):
                richness.add(all_species[sp].group)
        data[route].append((threshold, len(richness)))


with open('data/group_richness.pkl', 'wb') as pickle_file:
    pkl.dump(data, pickle_file, -1)

