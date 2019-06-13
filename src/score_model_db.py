import pickle
import pandas as pd
import numpy as np
import argparse
import yaml

from xgboost import XGBClassifier
import sqlalchemy as sql

import logging
logger = logging.getLogger(__name__)

def load_model(modelpath = '../models/xgboost', modelfilename = 'xgb_model.pkl'):
    """
    Load pre-saved pickle model from a pkl file
    
    :param modelpath (str): relative path of the target file
    :param modelfilename (str): name of the pickle file to load

    :return: a model file can be used for predictions
    """
    try: 
        path = modelpath + '//' + modelfilename
        pickle_in = open(path, 'rb')
        model = pickle.load(pickle_in)
        logger.info("Load file from %s", modelpath)
        return model
    except:
        raise logger.error("Error: Unable to load file %s", modelfilename)

class Match:
  """
  Create a match class to gather all required prediction variables for a pair of players and court type input

  """
  def __init__(self, player1, player2, court, engine_string):
    self.player1 = player1
    self.player2 = player2
    self.court = court
    self.engine_string = engine_string
    engine = sql.create_engine(engine_string, echo = True)
    self.engine = engine

  def getRanks(self):
    """
    Query the database rank table to get ranks for both players
    """
    query1 = "SELECT * FROM Ranking WHERE player = '" + self.player1 + "'"
    query2 = "SELECT * FROM Ranking WHERE player = '" + self.player2 + "'"
    df1 = pd.read_sql(query1, con=self.engine)
    df2 = pd.read_sql(query2, con=self.engine)
    p1rank = df1['Rank'].iloc[0]
    p2rank = df2['Rank'].iloc[0]
    return {'Rank_P1': int(p1rank), 'Rank_P2': int(p2rank)}

  def geth2h(self):
    """
    Query the database H2H table to get head-to-head records between the pair of players
    
    """
    queryh2h = "SELECT * FROM H2H WHERE Winner = '" + self.player1 + "' AND Loser = '" + self.player2 + "'"
    row = pd.read_sql(queryh2h, con=self.engine)
    tp = row['totalPlayed'].iloc[0]
    pct = row['h2h_win_pct'].iloc[0]
    return {'totalPlayed': float(tp), 'h2h_win_pct': float(pct)}

  def getSurface(self):
    """
    Query the database SurfaceWinPct table to get winning percentages on the corresponding type of surface for both players
    
    """
    querysurf1 = "SELECT * FROM SurfaceWinPct WHERE Player = '" + self.player1 + "' AND Surface = '" + self.court + "'"
    querysurf2 = "SELECT * FROM SurfaceWinPct WHERE Player = '" + self.player2 + "' AND Surface = '" + self.court + "'"
    surf1 = pd.read_sql(querysurf1, con=self.engine)
    surf2 = pd.read_sql(querysurf2, con=self.engine)
    p1m = surf1['surf_matches'].iloc[0]
    p2m = surf2['surf_matches'].iloc[0]
    p1winp = surf1['surf_winpct'].iloc[0]
    p2winp = surf2['surf_winpct'].iloc[0]
    return {'mp_surface_P1': float(p1m), 'mp_surface_P2': float(p2m), 'winpct_surface_P1': float(p1winp),
        'winpct_surface_P2': float(p2winp)}    

def assemble_data(p1, p2, surface, engine_string = 'sqlite:///../data/db/playerstats.db', args = None):
    """
    Query all necessary tables to gather required values for making a prediction
    
    :param p1 (str): name of player 1
    :param p2 (str): name of player 2
    :param surface (str): type of surface the match is on
    :param engine_string (str): engine string of the database to be queried
    :param args: potential input for congifuration file that specifies features to be selected

    :return: a pandas dataframe of 1 line containing data needed for making the prediction
    """
    if args != None:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.BaseLoader)
        feature_list = config['score_model']['columns']
    else:
        feature_list = ['Rank_P1', 'Rank_P2', 'h2h_win_pct', 'mp_surface_P1', 'mp_surface_P2', 'totalPlayed', 'winpct_surface_P1',
        'winpct_surface_P2']

    match = Match(p1, p2, surface, engine_string)
    play_dic = match.getSurface()
    play_dic.update(match.geth2h())
    play_dic.update(match.getRanks())

    pred_df = pd.DataFrame(columns=feature_list)
    pred_df.loc[len(pred_df)] = play_dic
    return pred_df

def score_model(pred_df, modelpath = '../models/xgboost', modelfilename = 'xgb_model.pkl'):
    """
    Query all necessary tables to gather required values for making a prediction
    
    :param pred_df (`object` pd dataframe): dataframe containing the prediction data with all features
    :param modelpath (str): relative path of the target pickle file
    :param modelfilename (str): name of the pickle file to load

    :return: (float) predicted probability of player 1 is winning
    """
    new_model = load_model(modelpath, modelfilename)
    preds_prob = new_model.predict_proba(np.array(pred_df))
    return preds_prob.item(1)