import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import random
import os
import logging
import logging.config

import config
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('upload_data')
cwd = os.getcwd()

def read_raw(rawfilepath, filename):
    path = rawfilepath + '\\' + filename
    try:
        rawfile = pd.read_csv(path, encoding = "ISO-8859-1", dtype=object)
        logger.info("Load file from %s", path)
        return rawfile
    except:
        logger.error("Error: Unable to load file %s", filename)

def select_columns(df, columnlist):
    if set(columnlist).issubset(df.columns):
        atp_short = df[columnlist]
        atp_short = atp_short.reset_index()
        logger.info(atp_short.head(2))
        return atp_short
    else:
        logger.error("Error: columns not entirely found in the dataset")
     
# ### Code to calculate H2
def add_h2h(df):
    #feature_to_create = ['h2h_win', 'h2h_lost']
    feature_to_create = ['h2h_win', 'h2h_lost', 'totalPlayed', 'h2h_win_pct']
    columns_needed = ['Winner', 'Loser', 'index']
    if set(feature_to_create).issubset(set(df.columns)):
        logger.info("features %s already exists", str(feature_to_create))
        return df
    elif set(columns_needed).issubset(set(df.columns)) == False:
        logger.debug("%s not in dataset", str(columns_needed))
    else:
        h2hwin = df.groupby(['Winner', 'Loser']).aggregate('count').reset_index()[['Winner', 'Loser', 'index']]
        h2hwin.rename(columns={'index':'h2h_win'}, inplace=True)
        h2hwin['h2h_win'] = h2hwin['h2h_win'].astype(float)
        h2hlost = h2hwin.copy()
        h2hlost.rename(columns={'h2h_win':'h2h_lost', 'Winner':'Loser', 'Loser':'Winner'}, inplace=True)
        merged = df.merge(h2hwin, how='left', on=['Winner', 'Loser']) \
                   .merge(h2hlost, how='left', on=['Winner', 'Loser'])
        merged['h2h_win'] = merged['h2h_win'].fillna(0)
        merged['h2h_lost'] = merged['h2h_lost'].fillna(0)
        merged['totalPlayed'] = merged['h2h_win'] + merged['h2h_lost']
        merged['h2h_win_pct'] = merged['h2h_win']/merged['totalPlayed']
        merged['h2h_win_pct'] = merged['h2h_win_pct'].fillna(value = 0.5)
        return merged

# ### Feature Generation
# 1. total matches between
# 2. winning %
# atp_matches['TotalMatchesBetween'] = atp_matches['h2hwin_P1'].astype('float') + atp_matches['h2hwin_P2'].astype('float') 
# atp_matches['WinPct_P1'] = atp_matches['h2hwin_P1']/atp_matches['TotalMatchesBetween']
# atp_matches['WinPct_P1'] = atp_matches['WinPct_P1'].fillna(value = 0.5)

# # Win % on Surface
# ### Code to calculate H2
def calculate_surface_winpct(df):
    surf_win = df.groupby(['Winner', 'Surface']).aggregate('count')\
                 .reset_index()[['Winner', 'Surface', 'index']]\
                 .rename(columns={'index':'totalWin'})
    surf_lost = df.groupby(['Loser', 'Surface']).aggregate('count')\
                  .reset_index()[['Loser', 'Surface', 'index']]\
                  .rename(columns={'index':'totalLost'})
    surface = surf_win.merge(surf_lost, how='outer', \
                left_on=['Winner', 'Surface'], right_on=['Loser', 'Surface'])
    surface.loc[(pd.isnull(surface.Winner), 'Winner')] = surface.Loser
    surface.loc[(pd.isnull(surface.Loser), 'Loser')] = surface.Winner
    surface = surface.fillna(0)
    surface['surf_matches'] = surface['totalWin'] + surface['totalLost']
    surface['surf_winpct'] = surface['totalWin']/surface['surf_matches']
    return surface[['Winner', 'Loser', 'Surface', 'surf_matches', 'surf_winpct']]

def add_surface_winpct(df):
    feature_to_create = ['surf_matches_x', 'surf_matches_y', 'surf_winpct_x', 'surf_winpct_y']
    columns_needed = ['Winner', 'Loser', 'Surface', 'index']
    if set(feature_to_create).issubset(set(df.columns)):
        logger.info("features %s already exists", str(feature_to_create))
        return df
    elif set(columns_needed).issubset(set(df.columns)) == False:
        logger.debug("%s not in dataset", str(columns_needed))
    else:
        surfacedf = calculate_surface_winpct(df)     
        df_new = df.merge(surfacedf[['Winner', 'Surface', 'surf_matches', 'surf_winpct']],\
                          how='left', on=['Winner', 'Surface'])\
                   .merge(surfacedf[['Loser', 'Surface', 'surf_matches', 'surf_winpct']],\
                          how='left', on=['Loser', 'Surface'])
        return df_new

# ### Dataset Flip - to mix winners and losers to make it a true prediction dataset
# 
# 1. Copy a dataset populated by winners, rename corresponding columns
# 2. Paste a exact same dataset populated by losers, swap corresponding columns
# 3. Append two datasets, select 1 record at random from the combined dataset for each match

def flip_records(df, seednumber):
    atp_winner_half = df
    atp_loser_half = atp_winner_half.copy()
    atp_winner_half = atp_winner_half.assign(matchresult='W')
    atp_winner_half.rename(columns={'Winner':'Player1', 'Loser':'Player2',
                               'WRank':'Rank_P1', 'LRank':'Rank_P2',
                               'Wsets':'Sets_P1', 'Lsets':'Sets_P2',
                               'h2h_win':'h2hwin_P1', 'h2h_lost': 'h2hwin_P2',
                               'surf_matches_x': 'mp_surface_P1', 'surf_matches_y': 'mp_surface_P2',
                               'surf_winpct_x': 'winpct_surface_P1', 'surf_winpct_y': 'winpct_surface_P2'},  
                 inplace=True)

    atp_loser_half = atp_loser_half.assign(matchresult='L')
    atp_loser_half.rename(columns={'Winner':'Player2', 'Loser':'Player1',
                               'WRank':'Rank_P2', 'LRank':'Rank_P1',
                               'Wsets':'Sets_P2', 'Lsets':'Sets_P1',
                               'h2h_win':'h2hwin_P2', 'h2h_lost': 'h2hwin_P1',
                               'surf_matches_x': 'mp_surface_P2', 'surf_matches_y': 'mp_surface_P1',
                               'surf_winpct_x': 'winpct_surface_P2', 'surf_winpct_y': 'winpct_surface_P1'},  
                 inplace=True)
    atp_loser_half['h2h_win_pct'] = 1 - atp_loser_half['h2h_win_pct']
    atp_matches_twice = pd.concat([atp_winner_half, atp_loser_half], sort=True)
    atp_matches_twice.sort_values(by = ['index'])
    random.seed(seednumber)
    atp_matches = atp_matches_twice.groupby('index').apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    print(sum(atp_matches['matchresult'] == 'W') / atp_matches['matchresult'].count())
    return atp_matches

def setFeatureType(df, columns, input_type):
    for column in columns:
        df[column] = df[column].astype(input_type)

def fillColumnNAs(df, columns, value = 0):
    for column in columns:
        df[column] = df[column].fillna(value)

def save_dataset(df, rawfilepath, filename):
    path = rawfilepath + '\\' + filename
    df.to_csv(path, index=False)

mypath = '..\\data'
myfile = 'atp_data.csv'
clist = ['ATP', 'Location', 'Tournament', 'Date', 'Series', 'Court', 'Surface',
        'Round', 'Best of', 'Winner', 'Loser', 'WRank', 'LRank', 'Wsets',
        'Lsets']
mysavefile = 'atp_cleaned.csv'

atp_raw = read_raw(mypath, myfile)
data = select_columns(atp_raw, clist)
df_h2h= add_h2h(data)
df_allfeatures = add_surface_winpct(df_h2h)
matches = flip_records(df_allfeatures, 8008)
setFeatureType(matches, ['Rank_P1', 'Rank_P2'], 'int')
save_dataset(matches, mypath, mysavefile)