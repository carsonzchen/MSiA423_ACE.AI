import numpy as np
import pandas as pd
import logging
import logging.config
from helpers.helpers import read_raw, save_dataset

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('generate features')

def trim_columns(df, columnlist):
    """
    Return dataframe that has selected columns with leading or trailing spaces removed
    
    :param df (pandas dataframe): input pandas dataframe
    :param columnlist (list): list of column names of the pandas dataframe to trim

    :return: a pandas dataframe with selected columns trimmed
    """
    for column in columnlist:
        df[column] = df[column].str.strip()
    return df

def gen_rankings_static(df):
    """
    Generate static ranking of ATP players based on their ranking of the last game they played.
    This is different from the gynamic ranking published by ATP each week.
    
    :param df (pandas dataframe): input pandas dataframe

    :return: a pandas dataframe with player name and their static rank
    """
    df_columns_needed = ['Winner', 'Loser', 'Date', 'WRank', 'LRank']
    if set(df_columns_needed).issubset(set(df.columns)) == False:
        logger.error("%s not in main dataset", str(df_columns_needed))
    
    else:
        # Last available rank when players are match winners
        rank1 = df.groupby(['Winner']).agg({'Date':'max'})\
            .merge(df[['Winner', 'Date', 'WRank']], on = ['Winner', 'Date'], how = 'inner')\
            .rename(columns={"Winner": "Player", "WRank": "Rank"})
        
        # Last availale rank when players are match losers
        rank2 = df.groupby(['Loser']).agg({'Date':'max'})\
            .merge(df[['Loser', 'Date', 'LRank']], on = ['Loser', 'Date'], how = 'inner')\
            .rename(columns={"Loser": "Player", "LRank": "Rank"})
        
        allranks = pd.concat([rank1, rank2]).reset_index(drop = True).sort_values(by=['Player','Date']).reset_index(drop = True)
        allranks = allranks.reset_index()
        allranks["date_rank"] = allranks.groupby("Player")["index"].rank(ascending=0,method='first')
        # Preserve the rank of the latest date
        ranktable = allranks[allranks["date_rank"] == 1][['Player', 'Rank']]
        return ranktable