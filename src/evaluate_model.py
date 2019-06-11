from train_model import split_train_test, choose_features
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.ensemble.partial_dependence import partial_dependence, plot_partial_dependence
from helpers.helpers import read_raw, setFeatureType

import pandas as pd
import numpy as np
import yaml
import pickle
import logging

logger = logging.getLogger(__name__)

def load_model(modelpath = '../models/xgboost', modelfilename = 'xgb_model.pkl'):
    """
    Load pre-saved pickle model from a pkl file
    
    :param rawfilepath (str): relative path of the target file
    :param filename (str): name of the pickle file to load

    :return: a model file can be used for predictions
    """
    path = modelpath + '//' + modelfilename
    pickle_in = open(path, 'rb')
    model = pickle.load(pickle_in)
    return model

new_model = load_model()
train_features = np.loadtxt('../data/sample/train_features.csv', delimiter=',', usecols=range(8))
test_features = np.loadtxt('../data/sample/test_features.csv', delimiter=',', usecols=range(8))
train_labels = np.loadtxt('../data/sample/train_labels.csv', delimiter=',', usecols=range(1), dtype='str')
test_labels = np.loadtxt('../data/sample/test_labels.csv', delimiter=',', usecols=range(1), dtype='str')

# predict on train and test
preds_train = new_model.predict(train_features)
print('train misclassification rate: ', np.sum(preds_train != train_labels) / train_features.shape[0])

preds_test = new_model.predict(test_features)
print('test misclassification rate: ', np.sum(preds_test != test_labels) / test_features.shape[0])

feature_list = ['Rank_P1', 'Rank_P2', 'h2h_win_pct', 'mp_surface_P1', 'mp_surface_P2', 'totalPlayed', 'winpct_surface_P1',
'winpct_surface_P2']
feature_importance = pd.DataFrame(new_model.feature_importances_, index = feature_list, columns=['importance']).sort_values('importance',ascending=False)
print(feature_importance)
print(sum(feature_importance['importance']))

y_actu = pd.Series(test_labels, name='Actual')
y_pred = pd.Series(preds_test, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
df_confusion