# Sanitizing the MDC dataset
# Please read through before executing
# Jeffrey Murray Jr
"""
* Input of Raw Set
* Removes extra spaces and Nulls
* Converts Unix to Date, Time respectively
* Saves to csv
"""

import lib.preprocess as pre
import pandas as pd
import numpy as np

## Paths : TO CHANGE FOR LOCAL SETUP ## TODO
rawGPS = '/media/jeffmur/School/data/mdcd/raw/gpswlan.csv'
cleanGPS= '/media/jeffmur/School/data/mdcd/cleaned-gpswlan.csv' 

gpsRecords = '/media/jeffmur/School/data/mdcd/gpswlan-cleanrecords.csv'
# cleanRecords = '/home/jeffmur/dev/mdcd/gpswlan-clean.csv'
# gpsRecords = '/media/jeffmur/School/data/mdcd/gpswlan-clean.csv'

## ------------------------------

# Drop spaces and save as gps.csv
# pre.removeSpaces(rawGPS, cleanGPS)

# # Create Pandas Dataset
# headers = ['UID', 'Latitude', 'Longitude', 'MAC']
# gpsLong = pre.toPandas(cleanGPS, headers, ' ')

# # Drop extra headers 
# newGPS = gpsLong[['UID', 'Latitude', 'Longitude']]
# # Convert Unix to Date, Time respectively
# # gps = pre.unixToTimeStamp(newGPS)
# # # Then save
# newGPS.to_csv('gpswlan-formatted.csv')

"""
With the data cleaned, we can now decode Database keys for User IDs
To do this, we must use records.csv (which also must be cleaned)
"""
# pre.removeSpaces(rawRecords, gpsRecords)
# $ cat records.csv | grep -w 'gps' > gpsrecords.csv

gps = pd.read_csv('gpswlan-formatted.csv')

headers = ['DB', 'UID', 'tz', 'time', 'type']
records = pre.toPandas(gpsRecords, headers, ' ')

print(f" There are {records['UID'].nunique()} unique users")

## Create a dictionary for O(1) reading, O(N) for intialization
dictOfRecords = {}
for row in records.itertuples():
    KEY = row.DB
    VAL = row.UID
    
    dictOfRecords[KEY] = VAL

replaceUID = gps['UID'].to_numpy()

# O(N) to replace each key (Database) w/ value (UID)
for i in range(0, len(replaceUID)):
    replaceUID[i] = dictOfRecords.get(replaceUID[i], 000)

# final_gps = gps[['UID', 'Date', 'Time' ,'Latitude', 'Longitude']]
gps['UID'] = replaceUID

gps.to_csv('gpswlan-sanitized.csv')