import numpy as np
import pandas as pd
import argparse
import yaml
from src.helpers.helpers import read_raw, save_dataset, setFeatureType, fillColumnNAs

import logging
logger = logging.getLogger(__name__)

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

def select_columns(df, columnlist):
    """
    Return only selected columns for the dataframe
    
    :param df (pandas dataframe): input pandas dataframe
    :param columnlist (list): list of column names of the pandas dataframe to include

    :return: a pandas dataframe with only selected columns
    """
    if set(columnlist).issubset(df.columns):
        df_part = df[columnlist]
        df_part = df_part.reset_index()
        logger.info(df_part.head(2))
        return df_part
    else:
        logger.error("Error: columns not entirely found in the dataset")

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

def calculate_h2h(df):
    """
    Create 4 head-to-head features for the main data: 
    'h2h_win': total number of wins in head-to-head records between 2 players
    'h2h_lost': total number of losts in head-to-head records between 2 players
    'totalPlayed': total number of matches between 2 players
    'h2h_win_pct': percentage of winning in the head-to-head record between 2 players
    Output the same exact table if the features already exist or required input columns are missing
    
    :param df (pd.dataFrame): pandas dataframe containing input data

    :return: df (pd.dataFrame): pandas dataframe containing processed features
    """
    columns_needed = ['Winner', 'Loser']
    if set(columns_needed).issubset(set(df.columns)): 
        h2hdf = df[columns_needed].assign(index = 1)
        h2hwin = h2hdf.groupby(['Winner', 'Loser']).aggregate('count').reset_index()[['Winner', 'Loser', 'index']]
        h2hwin.rename(columns={'index':'h2h_win'}, inplace=True)
        h2hwin['h2h_win'] = h2hwin['h2h_win'].astype(float)
        h2hlost = h2hwin.copy()
        # Swap "winner" and "loser" to calculate head-to-head lost records
        h2hlost.rename(columns={'h2h_win':'h2h_lost', 'Winner':'Loser', 'Loser':'Winner'}, inplace=True)
        merged = h2hwin.merge(h2hlost, how='outer', on=['Winner', 'Loser'])
        fillColumnNAs(merged, ['h2h_win', 'h2h_lost'])
        merged['totalPlayed'] = merged['h2h_win'] + merged['h2h_lost']
        merged['h2h_win_pct'] = merged['h2h_win']/merged['totalPlayed']
        return merged
    else:
        logger.error("Error: required columns not entirely found in the dataset")

def calculate_surface_winpct(df):
    """
    Summarize each player's winning percentage and total matches played by surface
    'surf_matches': Total number of matches played on the specific surface
    'surf_winpct': Historical percentage of winning on the specific surface
    
    :param df (pd.dataFrame): pandas dataframe containing input data

    :return: df (pd.dataFrame): pandas dataframe containing generated features, grouped by player
                                and surface
    """
    columns_needed = ['Winner', 'Loser', 'Surface']
    if set(columns_needed).issubset(set(df.columns)) == False:
        logger.error("%s not in dataset", str(columns_needed))
        return None
    else:
        df = df[columns_needed].assign(index = 1)
        surf_win = df.groupby(['Winner', 'Surface']).aggregate('count')\
                 .reset_index()[['Winner', 'Surface', 'index']]\
                 .rename(columns={'index':'totalWin'})
        surf_lost = df.groupby(['Loser', 'Surface']).aggregate('count')\
                  .reset_index()[['Loser', 'Surface', 'index']]\
                  .rename(columns={'index':'totalLost'})
        surface = surf_win.merge(surf_lost, how='outer', \
                left_on=['Winner', 'Surface'], right_on=['Loser', 'Surface'])
        surface.loc[(pd.isnull(surface.Winner), 'Winner')] = surface.Loser
        fillColumnNAs(surface, ['totalWin','totalLost'])
        surface['surf_matches'] = surface['totalWin'] + surface['totalLost']
        surface['surf_winpct'] = surface['totalWin']/surface['surf_matches']
        surface['Player'] = surface['Winner'].copy()
        return surface[['Player', 'Surface', 'surf_matches', 'surf_winpct']]

def run_trimdata(args):
    """Orchestrates the trim data functionalities from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    
    df = read_raw(**config["run_trimdata"]['read_raw'])
    df_trim = trim_columns(df, **config["run_trimdata"]['trim_columns'])
    save_dataset(df_trim, **config["run_trimdata"]['save_dataset'])
    f.close()
    return df_trim

def run_rankingstable(args):
    """Orchestrates the generation of rankings table from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    
    df = read_raw(**config["run_rankingstable"]['read_raw'])
    srank = gen_rankings_static(df)
    save_dataset(srank, **config["run_rankingstable"]['save_dataset'])
    f.close()
    return srank

def run_h2h_record(args):
    """Orchestrates the generating of h2h records table from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    
    df = read_raw(**config["run_h2h_record"]['read_raw'])
    h2h_record = calculate_h2h(df)
    save_dataset(h2h_record, **config["run_h2h_record"]['save_dataset'])
    f.close()
    return h2h_record 

def run_surface_record(args):
    """Orchestrates the generating of surface win records table from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    
    df = read_raw(**config["run_surface_record"]['read_raw'])
    surface_record = calculate_surface_winpct(df)
    save_dataset(surface_record, **config["run_surface_record"]['save_dataset'])
    f.close()
    return surface_record