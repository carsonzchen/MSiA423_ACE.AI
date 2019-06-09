import pickle
import pandas as pd
import numpy as np
import argparse
import yaml

from xgboost import XGBClassifier
import sqlalchemy as sql

def load_model(modelpath = '../models/xgboost', modelfilename = 'xgb_model.pkl'):
    """
    Load pre-saved pickle model from a pkl file
    
    :param rawfilepath (str): relative path of the target file
    :param filename (str): name of the pickle file to load

    :return: a model file can be used for predictions
    """
    path = modelpath + '\\' + modelfilename
    pickle_in = open(path, 'rb')
    model = pickle.load(pickle_in)
    return model

class Match:
  def __init__(self, player1, player2, court, engine_string):
    self.player1 = player1
    self.player2 = player2
    self.court = court
    self.engine_string = engine_string
    engine = sql.create_engine(engine_string, echo = True)
    self.engine = engine

  def getRanks(self):
    #engine_string = 'sqlite:///../data/db/rankings.db'
    query1 = "SELECT * FROM ranking WHERE player = '" + self.player1 + "'"
    query2 = "SELECT * FROM ranking WHERE player = '" + self.player2 + "'"
    df1 = pd.read_sql(query1, con=self.engine)
    df2 = pd.read_sql(query2, con=self.engine)
    p1rank = df1['Rank'].iloc[0]
    p2rank = df2['Rank'].iloc[0]
    return {'Rank_P1': int(p1rank), 'Rank_P2': int(p2rank)}

  def geth2h(self):
    queryh2h = "SELECT * FROM h2h WHERE Winner = '" + self.player1 + "' AND Loser = '" + self.player2 + "'"
    row = pd.read_sql(queryh2h, con=self.engine)
    tp = row['totalPlayed'].iloc[0]
    pct = row['h2h_win_pct'].iloc[0]
    return {'totalPlayed': float(tp), 'h2h_win_pct': float(pct)}

  def getSurface(self):
    querysurf1 = "SELECT * FROM surfacewinpct WHERE Player = '" + self.player1 + "' AND Surface = '" + self.court + "'"
    querysurf2 = "SELECT * FROM surfacewinpct WHERE Player = '" + self.player2 + "' AND Surface = '" + self.court + "'"
    surf1 = pd.read_sql(querysurf1, con=self.engine)
    surf2 = pd.read_sql(querysurf2, con=self.engine)
    p1m = surf1['surf_matches'].iloc[0]
    p2m = surf2['surf_matches'].iloc[0]
    p1winp = surf1['surf_winpct'].iloc[0]
    p2winp = surf2['surf_winpct'].iloc[0]
    return {'mp_surface_P1': float(p1m), 'mp_surface_P2': float(p2m), 'winpct_surface_P1': float(p1winp),
        'winpct_surface_P2': float(p2winp)}    

def assemble_data(p1, p2, surface, engine_string = 'sqlite:///../data/db/playerstats.db', args = None):
    """Orchestrates the generating of features from commandline arguments."""
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

def score_model(p1, p2, surface, engine_string = 'sqlite:///../data/db/playerstats.db', args = None):
    """Orchestrates the generating of features from commandline arguments."""
    pred_df = assemble_data(p1, p2, surface, engine_string, args)
    new_model = load_model('../models/xgboost', 'xgb_model.pkl')
    preds_prob = new_model.predict_proba(np.array(pred_df))
    print(preds_prob)
    return preds_prob.item(1)

# engine_string = 'sqlite:///../data/db/playerstats.db'
# #engine_string = config['create_db_local'][args.option]['engine_string']
# engine = sql.create_engine(engine_string, echo = True)
# #Session = sessionmaker(bind=engine)
# #session = Session()
# query = "SELECT * FROM ranking WHERE player = 'Nadal R.'"
# df = pd.read_sql(query, con=engine)


# query2 = "SELECT * FROM h2h WHERE Winner = 'Nadal R.' AND Loser = 'Federer R.'"
# df2 = pd.read_sql(query2, con=engine)

# p1 = 'Nadal R.'
# p2 = 'Federer R.'
# s1 = 'Grass'
# nm = Match(p1, p2, s1, 'sqlite:///../data/db/playerstats.db')
# query3 = "SELECT * FROM surfacewinpct WHERE Player = '" + p1 + "' AND Surface = '" + s1 + "'"
# df3 = pd.read_sql(query3, con=engine)