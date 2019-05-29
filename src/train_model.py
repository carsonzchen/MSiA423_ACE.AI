import pandas as pd
import numpy as np
import random

import logging
import logging.config
from helpers.helpers import read_raw, save_dataset, fillColumnNAs, setFeatureType

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('train model')

from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBClassifier 
import pickle

def choose_features(df, features_to_use=None, target=None):
    """Reduces the dataset to the features_to_use. Will keep the target if provided.

    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features
        features_to_use (:obj:`list`): List of columnms to extract from the dataset to be features
        target (str, optional): If given, will include the target column in the output dataset as well.

    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
    """

    logger.debug("Choosing features")
    if features_to_use is not None:
        features = []
        dropped_columns = []
        for column in df.columns:
            # Identifies if this column is in the features to use or if it is a dummy of one of the features to use
            if column in features_to_use or column.split("_dummy_")[0] in features_to_use or column == target:
                features.append(column)
            else:
                dropped_columns.append(column)

        if len(dropped_columns) > 0:
            logger.info("The following columns were not used as features: %s", ",".join(dropped_columns))
        logger.debug(features)
        X = df[features]
    else:
        logger.debug("features_to_use is None, df being returned")
        X = df

    return X

def split_train_test(df, label, test_size = 0.25, random_state = 42):
    """???

    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features
        label 
        test_size (:obj:`list`): List of columnms to extract from the dataset to be features
        random_state (str, optional): If given, will include the target column in the output dataset as well.

    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
    """
    if label not in df.columns:
        logger.error("Label %s is not found in dataframe", label)
        print('a')
    else:
        flist = list(df.columns)
        flist.remove(label)
        features_raw = df[flist]
        # One-hot encode features if categorical variables exit
        features_processed = pd.get_dummies(features_raw)
        features = np.array(features_processed)
        labels = np.array(df[label])
        # Split the data into training and testing sets
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = test_size, random_state = random_state)
        return [train_features, test_features, train_labels, test_labels]

def train_xgboost(train_features, train_labels, save_path = '../models/xgb_model.pkl', **kwargs):
    """???

    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features
        label 
        test_size (:obj:`list`): List of columnms to extract from the dataset to be features
        random_state (str, optional): If given, will include the target column in the output dataset as well.

    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
    """
    # ### Best result: tree: 150 alpha: 0.1 depth: 3
    xgbmodel = xgb.XGBClassifier(objective ='binary:logistic', n_estimators=150, \
        learning_rate = 0.1, max_depth = 3).fit(train_features, train_labels)
    if save_path is not None:
        with open(save_path, "wb") as f:
            pickle.dump(xgbmodel, f)
    return xgbmodel

mypath = '..\\data'
mysavefile = 'atp_cleaned.csv'
atp_data = read_raw(mypath, mysavefile)

#atp_data = pd.read_csv('../../data/atp_cleaned.csv', encoding = "ISO-8859-1")
feature_list = ['Rank_P1', 'Rank_P2', 'mp_surface_P1', 'mp_surface_P2', 'winpct_surface_P1',
        'winpct_surface_P2', 'totalPlayed', 'h2h_win_pct']
atp_matches_p = choose_features(atp_data, features_to_use=feature_list, target='matchresult')

setFeatureType(atp_matches_p, feature_list, 'float')
atp_matches_p.axes
atp_matches_p.dtypes
#fewGamesCorrection(atp_matches_p, ['h2h_win_pct'])

data = split_train_test(atp_matches_p, 'matchresult')
train_features = data[0]
test_features = data[1]
train_labels = data[2]
test_labels = data[3]
print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

newmodel = train_xgboost(train_features, train_labels)