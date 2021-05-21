# Sanitizing the geoLife dataset
# Please read through before executing
# Jeffrey Murray Jr
"""
* Input of user_by_month
* Concats UID to each record for each month file
* Can be called for N-Resolution
* Outputs DataFrame
"""

import lib.preprocess as pre
import pandas as pd
import numpy as np
import glob as glob
import os
import datetime as dt
from dateutil import parser, relativedelta
import ntpath

## Paths : TO CHANGE FOR LOCAL SETUP ## TODO
dataDir = '/media/jeffmur/School/dev/490-demo/data'
geoUsers = dataDir+'/geoLife/user_by_month'
rawHeaders = [ "Latitude", "Longitude", "Zero", "Altitude", "Num of Days", "Date", "Time"]

def getAllUID():
    """
    return path to each user as list[str]
    """
    return [x[-3:] for x in glob.glob(geoUsers+"/*")]

def userDataFrame(UID):
    """
    returns all {UID} csv files into one dataframe
    """
    # Easy to read
    pathToUser = geoUsers+f"/{UID}/"

    # Glob all users (os.path is universal)
    months = glob.glob(os.path.join(pathToUser + "/*.csv"))

    # Concat all month files for user
    df = pd.concat((pd.read_csv(f, names=rawHeaders)) for f in months)

    # Add UID column and fill
    df.insert(0, 'UID', [UID for x in range(0, df.shape[0])])
    return df[['UID', 'Latitude', 'Longitude', 'Date', 'Time']]

def allUsersDF(listofUID):
    """
    Single DataFrame for a given list of users
    """
    return pd.concat([userDataFrame(uid) for uid in listofUID])


## make a function to get a certain time range of given user!! ##TODO

def filterUserMonthRange(UID, fromDate, toDate):
    """
    returns all {UID} csv files into one dataframe
    """
    # Easy to read
    pathToUser = geoUsers+f"/{UID}/"

    # Glob all users (os.path is universal)
    months = glob.glob(os.path.join(pathToUser + "/*.csv"))

    # Filter by year-month
    filtered = []
    fromDate = parser.parse(fromDate)
    fromDate = fromDate - relativedelta.relativedelta(months=1)
    toDate = parser.parse(toDate)


    # Create datetime object from Path/To/filename.csv
    for m in months: 
        # list of string data
        b = ntpath.basename(m)[:-4].split('_')
        fileDate = dt.datetime(int(b[0]), int(b[1]), 1)
        if(fromDate <= fileDate <= toDate):
            filtered.append(m)

    if(not filtered): return pd.DataFrame() # return empty DF :)

    # Concat all month files for user
    df = pd.concat((pd.read_csv(f, names=rawHeaders)) for f in filtered)

    # Add UID column and fill
    df.insert(0, 'UID', [UID for x in range(0, df.shape[0])])
    return df[['UID', 'Latitude', 'Longitude', 'Date', 'Time']]

def filterbyMonthRange(uidList=[], fromDate='2008-10', toDate='2008-11'):
    """
    filter Choice/ALL users by date range
    """
    # All users if none entered
    if(not uidList): return pd.concat(filterUserMonthRange(uid, fromDate, toDate) for uid in getAllUID())
    # else choice
    return pd.concat(filterUserMonthRange(uid, fromDate, toDate) for uid in uidList)