import train_model
import pickle
import pandas as pd
import numpy as np
import argparse
import yaml

from src.helpers.helpers import read_raw, save_dataset, fillColumnNAs, setFeatureType

def load_model(modelpath = '../models/', modelfilename = 'xgb_model.pkl'):
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
  def __init__(self, player1, player2, court):
    self.player1 = player1
    self.player2 = player2
    self.court = court

  def getRanks(self):
    rankdata = read_raw('../data', 'static_rankings.csv')
    p1rank = rankdata[rankdata['Player'] == self.player1]['Rank'].iloc[0]
    p2rank = rankdata[rankdata['Player'] == self.player2]['Rank'].iloc[0]
    return {'Rank_P1': int(p1rank), 'Rank_P2': int(p2rank)}

  def geth2h(self):
    h2hdata = read_raw('../data', 'atp_h2h.csv')
    row = h2hdata[(h2hdata['Winner']==self.player1) & (h2hdata['Loser']==self.player2)]
    tp = row['totalPlayed'].iloc[0]
    pct = row['h2h_win_pct'].iloc[0]
    return {'totalPlayed': float(tp), 'h2h_win_pct': float(pct)}

  def getRanks(self):
    rankdata = read_raw('../data', 'static_rankings.csv')
    p1rank = rankdata[rankdata['Player'] == self.player1]['Rank'].iloc[0]
    p2rank = rankdata[rankdata['Player'] == self.player2]['Rank'].iloc[0]
    return {'Rank_P1': int(p1rank), 'Rank_P2': int(p2rank)}

  def getSurface(self):
    surfdata = read_raw('../data', 'atp_winpct_surface.csv')
    surf = surfdata[surfdata['Surface'] == self.court]
    p1m= surf[surf['Player'] == self.player1]['surf_matches'].iloc[0]
    p2m = surf[surf['Player'] == self.player2]['surf_matches'].iloc[0]
    p1winp = surf[surf['Player'] == self.player1]['surf_winpct'].iloc[0]
    p2winp = surf[surf['Player'] == self.player2]['surf_winpct'].iloc[0]
    return {'mp_surface_P1': float(p1m), 'mp_surface_P2': float(p2m), 'winpct_surface_P1': float(p1winp),
        'winpct_surface_P2': float(p2winp)}    

#k = Match('Nadal R.', 'Federer R.', 'Clay')
#my_dic = {'Rank_P1': 12, 'Rank_P2': 23, 'mp_surface_P1': 0.5, 'mp_surface_P2': 0.3, 'winpct_surface_P1': 0.12,
#        'winpct_surface_P2': 0.6, 'totalPlayed': 1, 'h2h_win_pct': 0.5}
#feature_list = ['Rank_P1', 'Rank_P2', 'mp_surface_P1', 'mp_surface_P2', 'winpct_surface_P1',
# 'winpct_surface_P2', 'totalPlayed', 'h2h_win_pct']

def score_model(p1, p2, surface, args):
    """Orchestrates the generating of features from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    match = Match(p1, p2, surface)
    play_dic = match.getSurface()
    play_dic.update(match.geth2h())
    play_dic.update(match.getRanks())

    pred_df = pd.DataFrame(columns=config['score_model']['columns'])
    pred_df.loc[len(pred_df)] = play_dic
    new_model = load_model()
    preds_prob = new_model.predict_proba(np.array(pred_df))
    return preds_prob.item(0)
    