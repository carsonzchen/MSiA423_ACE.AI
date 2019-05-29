import train_model
import pickle
import pandas as pd
import numpy as np

def load_model(modelpath = '../models/', modelfilename = 'xgb_model.pkl'):
    """
    ???
    
    :param rawfilepath (str): relative path of the target file
    :param filename (str): name of the file to load

    :return: a pandas dataframe of the raw file
    """
    path = modelpath + '\\' + modelfilename
    pickle_in = open(path, 'rb')
    model = pickle.load(pickle_in)
    return model

new_model = load_model()

preds_test_prob = new_model.predict_proba(train_model.test_features)