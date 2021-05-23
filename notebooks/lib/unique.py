import numpy as np 
import pandas as pd
import random
from collections import defaultdict

def locationPrecision(df_dataset, decimals):
    """[summary]
    Rounding for location (lat/lon) decimal places. 
    
    Allows for more coarse or fine grain location points. 
    
    [Args]:
        df_dataset (DataFrame): headers must contain at least 'Latitude', 'Longitude'
        decimals (int): length of values after decimal to keep
    """
    # Make deep copy, to avoid pass by reference (mem)
    roundedDF = df_dataset.copy(True)
    
    # Round each float in column to decimal preference
    roundedDF['Latitude'] = roundedDF['Latitude'].apply(lambda x: round(x, decimals))
    roundedDF['Longitude'] = roundedDF['Longitude'].apply(lambda x: round(x, decimals))
    
    return roundedDF

def generateLocationID(df_dataset):
    """[summary] 
    Generate unique location identifier (int) for new lat/lon combinations
    
    [Args]:
        df_dataset (DataFrame): headers must contain at least 'Latitude', 'Longitude'

    [Returns]:
        (list): of equal row length mapping locations (lat/lon) to a loc key 
    """
    # Create Numpy Array of [Locations]
    locations = df_dataset[['Latitude', 'Longitude']].to_numpy()
    
    # Map to tuple array
    loc = tuple(map(tuple, locations))
    # using list comprehension + defaultdict + lambda
    # assigning ids to tuple locations
    # allows for unique lat, lon unique ids
    temp = defaultdict(lambda: len(temp))

    uniqueIDs = [temp[ele] for ele in loc]

    ## Analytics
    print(f"{len(np.unique(uniqueIDs))} unique location ids of ")
    print(f"{ len(np.unique( df_dataset[['UID']] )) } total number of users. \n")

    return uniqueIDs

def inTheCrowd(NUM_POINTS, df_dataset, T_list):
    """[summary]
    Ref: de Montjoye et al. 2013 - Unique In The Crowd, The privacy bounds of human mobility patterns
    DOI: 10.1038/srep01376
    
    Calculate uniqueness rate for random user's similarity until reaching NUM_POINTS threshold. 

    [Args]:
        NUM_POINTS (int): Threshold for the number of similar traces for re-identification
        df_dataset (df): headers = ['UID', 'Unique Location ID']
        T_list (df.groupby['UID']): location list for each user

    [Returns]:
        (float): Uniqueness rate of randomly chosen users within dataset
    """
    idlist = df_dataset['UID'].to_numpy()
    RANDOM_TRACES = 2500
    BOOL_LIST = [True for i in range(NUM_POINTS)]
    n = 0
    # The uniqueness of traces is estimated as the percentage of 2500 random traces 
    # that are unique given p spatio-temporal points. 
    
    for i in range(RANDOM_TRACES):
        id_int = random.choice(idlist)  # randomly choose a user from the id list.
        step_one = df_dataset.loc[df_dataset["UID"] == id_int]
        list_one = step_one["loc_id"].unique().tolist()
        
        # random choice of N points
        sub_trace = [random.choice(list_one) for i in range(NUM_POINTS)]
        
        # For each user in dataframe (groupby "UID")
        for x in T_list.groups:  
            # For every other user, but current uid
            if x != id_int:
                # emulate each user trajectory and check if the random subtrajectory is part of them
                Tra = T_list.get_group(x).loc_id.tolist()
                
                # if all sub_trace elements are contained within random user's full trace
                bool_array = np.isin(sub_trace, Tra, assume_unique=True)  
                
                # when all elements are TRUE, we noted it as duplicate trajectory.
                if (np.array_equal(BOOL_LIST, bool_array) == True):  
                    n += 1
                    print(f"i:{i} \t rate = {1 - n/RANDOM_TRACES}")
                    break

    uniqueness_rate = 1 - n / RANDOM_TRACES
    print(f"---\n Final Uniqueness Rate: {uniqueness_rate} \n---")
    return uniqueness_rate

def splitByTime(df, timeRes):
    """
    timeRes (str): {NUM}Min 
    It must be in minutes!!!
    """
    return [g[['UID','loc_id']] for n, g in df.groupby(pd.Grouper(key='Time',freq=timeRes)) if not g.empty]

def inTheTraces(NUM_POINTS, df_dataset, T_list, TraceSplit):
    """[summary]
    Ref: de Montjoye et al. 2013 - Unique In The Crowd, The privacy bounds of human mobility patterns
    DOI: 10.1038/srep01376
    
    Calculate uniqueness rate for random user's similarity until reaching NUM_POINTS threshold. 

    [Args]:
        NUM_POINTS (int): Threshold for the number of similar traces for re-identification
        df_dataset (df): headers = ['UID', 'Unique Location ID']
        T_list (df.groupby['UID']): location list for each user
        MinuteSplit ([['UID','loc_id']]): Matrix of traces split by time resolution

    [Returns]:
        (float): Uniqueness rate of randomly chosen users within dataset
    """
    idlist = df_dataset['UID'].to_numpy()
    RANDOM_TRACES = 2500
    BOOL_LIST = [True for i in range(NUM_POINTS)]
    n = 0
    # The uniqueness of traces is estimated as the percentage of 2500 random traces 
    # that are unique given p spatio-temporal points. 
    
    for i in range(RANDOM_TRACES):
        id_int = random.choice(idlist)  # randomly choose a user from the id list.
        step_one = df_dataset.loc[df_dataset["UID"] == id_int]
        list_one = step_one["loc_id"].unique().tolist()
        
        # random choice of trace from dataset
        sub_trace = TraceSplit[random.randint(0, len(TraceSplit)-1)]
        print(sub_trace)

        # For each user in dataframe (groupby "UID")
        for x in T_list.groups:  
            # For every other user, but current uid
            if x != id_int:
                # emulate each user trajectory and check if the random subtrajectory is part of them
                Tra = T_list.get_group(x).loc_id.tolist()
                
                # if all sub_trace elements are contained within random user's full trace
                bool_array = np.isin(sub_trace, Tra, assume_unique=True)  
                
                # when all elements are TRUE, we noted it as duplicate trajectory.
                if (np.array_equal(BOOL_LIST, bool_array) == True):  
                    n += 1
                    print(f"i:{i} \t rate = {1 - n/RANDOM_TRACES}")
                    break

    uniqueness_rate = 1 - n / RANDOM_TRACES
    print(f"---\n Final Uniqueness Rate: {uniqueness_rate} \n---")
    return uniqueness_rate