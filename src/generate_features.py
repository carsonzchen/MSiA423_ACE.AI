import numpy as np
import pandas as pd
import random
import argparse
import yaml

import logging
import logging.config
from helpers.helpers import read_raw, save_dataset, fillColumnNAs, setFeatureType
from preprocess import trim_columns, gen_rankings_static

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('generate features')

def fewGamesCorrection(df, columns_to_correct, criterion_column = 'totalPlayed', threshold = 2.0, replace_value = 0.5):
    """
    Correct win percentages if two few games are played, with a default value of 0.5 
    Primarily used for calculate_h2h function

    :param df (pd.dataFrame): dataframe containing main match records data
    :param columns_to_correct (`obj`:list): list of the columns describing win percentages
    :param criterion_column (str): Column indicating number of matches played, default is 'totalPlayed'
    :param threshold (float): Lowest number of games played to be considered not replacing, default is 2
    :param replace_value (float): The correction value for win percentage, default is 0.5

    :return: df (pd.dataFrame): dataframe with corrections on win percentages performed
    """
    if set(columns_to_correct).issubset(set(df.columns)) == False:
        logger.error("target column(s): %s not in dataset", str(columns_to_correct))
        return df
    elif criterion_column not in df.columns:
        logger.error("Criterion column: %s not in dataset", str(criterion_column))
        return df
    else:
        setFeatureType(df, [criterion_column], 'float')
        for column in columns_to_correct:
            index = df[criterion_column] < threshold
            df.loc[index, column] = replace_value
        return df

def add_h2h(df, h2htable):
    """
    Merge all 4 features from head-to-head records to the dataframe
    
    :param df (pd.dataFrame): pandas dataframe containing input data
    :param h2htable (pd.dataFrame): pandas dataframe containing h2h records data

    :return: df (pd.dataFrame): pandas dataframe containing processed data
    """
    feature_to_create = ['h2h_win', 'h2h_lost', 'totalPlayed', 'h2h_win_pct']
    columns_needed = ['Winner', 'Loser']
    if set(feature_to_create).issubset(set(df.columns)): # Check if features already exist
        logger.info("features %s already exists", str(feature_to_create))
        return df
    elif set(columns_needed).issubset(set(df.columns)) == False: # Check if required columns exist
        logger.error("%s not in dataset", str(columns_needed))
        return df
    else: 
        h2h_adjusted = fewGamesCorrection(h2htable, ['h2h_win_pct'])
        merged = df.merge(h2h_adjusted, how='left', on=['Winner', 'Loser'])
        return merged

def add_surface_winpct(df, surfacedf):
    """
    Add 4 surface competency features to the main data: 
    'surf_matches_x': Total number of matches played on the specific surface for 'Winner'
    'surf_matches_y': Total number of matches played on the specific surface for 'Loser'
    'surf_winpct_x': Historical percentage of winning on the specific surface for 'Winner'
    'surf_winpct_y': Historical percentage of winning on the specific surface for 'Loser'
    Output the same exact table if the features already exist or required input columns are missing
    
    :param df (pd.dataFrame): dataframe containing main match records data
    :param surfacedf (pd.dataFrame): dataframe containing summarized surface winning % data

    :return: df (pd.dataFrame): dataframe with surface competency features added
    """
    feature_to_create = ['surf_matches_x', 'surf_matches_y', 'surf_winpct_x', 'surf_winpct_y']
    df_columns_needed = ['Winner', 'Loser', 'Surface']
    sr_columns_needed = ['Player', 'Surface', 'surf_matches', 'surf_winpct']
    if set(feature_to_create).issubset(set(df.columns)):
        logger.info("features %s already exists", str(feature_to_create))
        return df
    elif set(df_columns_needed).issubset(set(df.columns)) == False:
        logger.error("%s not in main dataset", str(df_columns_needed))
        return df
    elif set(sr_columns_needed).issubset(set(surfacedf.columns)) == False:
        logger.error("%s not in to merge dataset", str(sr_columns_needed))
        return df
    else:
        df_new = df.merge(surfacedf, how='left',\
                          left_on=['Winner', 'Surface'], right_on=['Player', 'Surface'])\
                   .merge(surfacedf, how='left',\
                          left_on=['Loser', 'Surface'], right_on=['Player', 'Surface'])
        df_new.drop(['Player_x', 'Player_y'], axis=1, inplace=True)
        return df_new

def flip_records(df, seednumber):
    """
    # The original dataset has 'winner' and 'loser' columns, this function mixes winners and losers 
    # to be Player 1 and Player 2, with a target that about 50% of all records have Player 1 as the
    # winner, so that it appears as a balanced dataset for model building.
    # 
    # Algorithm for the flip:
    # 1. Copy a dataset populated by winners, rename corresponding columns
    # 2. Paste a exact same dataset populated by losers, swap corresponding columns
    # 3. Append two datasets so that for every match there are 2 records. 
    # 4. Select 1 record at random from each paired matches using generated seed
    
    :param df (pd.dataFrame): dataframe containing main match records and features
    :param seednumber (int): a random seed for random number generator to choose the row

    :return: df (pd.dataFrame): dataframe in the format of player 1 and player 2
    """
    setFeatureType(df, ['h2h_win_pct'], 'float') 
    atp_winner_half = df
    atp_loser_half = df.copy()
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
    atp_loser_half['h2h_win_pct'] = 1 - atp_loser_half['h2h_win_pct'] # Need to take win% complement

    atp_matches_twice = pd.concat([atp_winner_half, atp_loser_half], sort=True)
    atp_matches_twice.sort_values(by = ['index'])
    random.seed(seednumber)
    atp_matches = atp_matches_twice.groupby('index').apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    ds_balance = sum(atp_matches['matchresult'] == 'W') / atp_matches['matchresult'].count()
    logger.info("%s percent of rows are designated as 'W'", str(ds_balance*100))
    return atp_matches

#def run_features(args):
def run_features(args.config = 'config = yaml.load(f)'):
    """Orchestrates the generating of features from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f)

    if 'load_data' in config:
        df = read_raw(config["load_data"]["datafolderpath"], config["load_data"]["rawfilename"])
    else:
        raise ValueError("Path to CSV for input data must be provided through --csv or "
                         "load_data configuration must exist in config file")
    
    trimmed_data = trim_columns(df, config["generate_features"]["trimlist"])
    data = select_columns(trimmed_data, config["generate_features"]["clist"])
    surface_record = read_raw(config["load_data"]["datafolderpath"], config["load_data"]["atp_winpct_surface.csv"])
    h2h_record = read_raw(config["load_data"]["datafolderpath"], config["load_data"]["static_rankings.csv"])
    data = add_h2h(data, h2h_record)
    data = add_surface_winpct(data, surface_record)
    matches = flip_records(data, config["generate_features"]["seednumber"])
    save_dataset(matches, config["load_data"]["datafolderpath"], config["load_data"]["rawfilename"])

    return matches

# mypath = '..\\data'
# myfile = 'atp_data.csv'
# clist = ['ATP', 'Location', 'Tournament', 'Date', 'Series', 'Court', 'Surface',
#        'Round', 'Best of', 'Winner', 'Loser', 'WRank', 'LRank', 'Wsets',
#        'Lsets']
# trimlist = ['Winner', 'Loser']
# mysavefile = 'atp_cleaned.csv'
# surfacefile = 'atp_winpct_surface.csv'
# rankingssavefile = 'static_rankings.csv'
# h2hfile = 'atp_h2h.csv'
# fewMatchAdj_column = ['h2h_win_pct']

# atp_raw = read_raw(mypath, myfile)
# trimmed_data = trim_columns(atp_raw, trimlist)
# srank = gen_rankings_static(trimmed_data)
# save_dataset(srank, mypath, rankingssavefile)

# data = select_columns(trimmed_data, clist)
# h2h_record = calculate_h2h(data)
# save_dataset(h2h_record, mypath, h2hfile)

# surface_record = calculate_surface_winpct(data)
# save_dataset(surface_record, mypath, surfacefile)

# surface_record = read_raw(mypath, surfacefile, dtype = None)
# h2h_record = read_raw(mypath, h2hfile, dtype = None)
# df_h2h = add_h2h(data, h2h_record)
# df_allfeatures = add_surface_winpct(df_h2h, surface_record)
# matches = flip_records(df_allfeatures, 8008)
# save_dataset(matches, mypath, mysavefile)