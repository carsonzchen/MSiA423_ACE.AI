import train_model
import pickle
import pandas as pd
import numpy as np

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

pred_df = pd.DataFrame(columns=train_model.feature_list)
my_dic = {'Rank_P1': 12, 'Rank_P2': 23, 'mp_surface_P1': 0.5, 'mp_surface_P2': 0.3, 'winpct_surface_P1': 0.12,
        'winpct_surface_P2': 0.6, 'totalPlayed': 1, 'h2h_win_pct': 0.5}
pred_df.loc[len(pred_df)] = my_dic

new_model = load_model()

preds_prob = new_model.predict_proba(np.array(pred_df))