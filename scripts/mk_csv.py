#!/usr/bin/env python
''' 
This script requires the bbs.sqlite database, which can be generated
by the EcoData Retriever:

retriever install bbs -e s -f bbs.sqlite
''' 
import sqlite3 as dbapi
import csv
import sys

con = dbapi.connect('data/bbs.sqlite')
query = open('data/bbs_query.sql').read()
cur = con.cursor()
cur.execute(query)

with sys.stdout as output_file:
    writer = csv.writer(output_file)
    writer.writerow(('stateroute', 'lat','lon','genus','species','count'))
    for row in cur:
        #lat = round(row[0], 3)
        #lon = round(row[1], 3)
        writer.writerow(row)