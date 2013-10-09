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
import pybioclim


# set of BIOCLIM variables to use for mean/heterogeneity models
mean_vars = ['bio%s' % i for i in range(1,20)] + ['ndvi']
#mean_vars = ['bio%s' % i for i in (1,2,3,4,7,12,15)]
var_vars = mean_vars

routes = set()
mean_data, var_data = {}, {}
with open('data/%s.csv' % dataset) as data_file:
    reader = csv.reader(data_file)
    reader.next()
    for route, lat, lon, genus, species, count in reader:
        route = (round(float(lat), 3), round(float(lon), 3))
        if not route in routes:
            routes.add(route)

for route in routes:
    print len(mean_data), '/', len(routes),
    sys.stdout.write('\r')
    mean_values = [pybioclim.get_values(var, [route])[0] for var in mean_vars]
    var_values = [pybioclim.get_spatial_variance(var, [route])[0] for var in var_vars]

    mean_data[route] = mean_values
    var_data[route] = var_values

print '\n', 'done!'

data = (mean_data, var_data)
with open('data/%s_env_data.pkl' % dataset, 'wb') as pickle_file:
    pkl.dump(data, pickle_file, -1)
