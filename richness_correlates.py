import Bio.Phylo as bp
import csv
import numpy as np
from geophy.cluster import color_clusters
import statsmodels.api as sm
import cPickle as pkl
import sys


#tree = bp.read('passeriformes.new', 'newick')
tree = bp.read('bbs.new', 'newick')
#tree = bp.read('jetz_birds.new', 'newick')
tips = tree.get_terminals()
all_species = {t.name: t for t in tips}

mean_data = {}
var_data = {}
with open('env_data.csv') as data_file:
    reader = csv.reader(data_file)
    var_names = reader.next()
    for line in reader:
        route = line[0]
        mean_data[route] = [float(value) 
                            for var_name, value in zip(var_names, line) 
                            if '.mean' in var_name]
        var_data[route] =  [float(value) 
                            for var_name, value in zip(var_names, line) 
                            if '.var' in var_name]
                

routes = {}
count_data_spp = set()
with open('bbs.csv') as data_file:
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
thresholds = [0] + sorted(set([clade._med_distance for clade in tree.find_elements()
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
        try:
            x1.append(mean_data[route])
            x2.append(var_data[route])
        except KeyError: continue
        for sp in spp:
            if sp in all_species and hasattr(all_species[sp], 'group'):
                richness.add(all_species[sp].group)
        y.append(len(richness))

    x1 = [[1] + x for x in x1]
    x2 = [[1] + x for x in x2]
    x3 = [[1]+a+b for (a,b) in zip(x1, x2)]

    results = [sm.OLS(y, x).fit().rsquared 
               for x in (x1, x2, x3)]
    print results
    if all([0 <= result <= 1 for result in results]):
        data[threshold] = results
    else: continue

with open('richness_correlates.pkl', 'wb') as pickle_file:
    pkl.dump(data, pickle_file, -1)

