import pandas as pd
import numpy as np
import random
import argparse
import yaml

from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBClassifier
import pickle
from src.helpers.helpers import read_raw, save_dataset, fillColumnNAs, setFeatureType

import logging
logger = logging.getLogger(__name__)

def choose_features(df, features_to_use=None, target=None):
    """Reduces the dataset to the features_to_use. Will keep the target (label) if provided.

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
            if column in features_to_use or column.split("_dummy_")[0] in features_to_use: #or column == target:
                features.append(column)
            else:
                dropped_columns.append(column)
        
        if target is not None:
                features.append(target)

        if len(dropped_columns) > 0:
            logger.info("The following columns were not used as features: %s", ",".join(dropped_columns))
        logger.debug(features)
        X = df[features]
    else:
        logger.debug("features_to_use is None, df being returned")
        X = df

    return X

def split_train_test(df, label, test_size = 0.25, random_state = 42, **kwargs):
    """
    Split dataframe into 4 parts - training features and labels, and test features and labels. It
    is a wrapper for sklearn function train_test_split

    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features and target
        label (str): Column name of the label (target) for prediction
        test_size (float, optional): percentage of the data to hold out as test set for evaluation
        random_state (int, optional): a seed number for random number generator used for identifying test rows

    Returns:
        X (`obj`: list): List of length 4 containing 4 numpy arrays, respectively at each position:
        0 - train_features 
        1 - test_features
        2 - train_labels 
        3 - test_labels
    """
    if label not in df.columns:
        logger.error("Label %s is not found in dataframe", label)
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

def fit_xgboost(train_features, train_labels, save_path = 'models/xgboost', **kwargs):
    """
    Fit the dataset using a xgboost model, with options to save the model as a pickle file. Use outputs
    from split_train_test, and this is a wrapper for XGBClassifier.

    Args:
        train_features: (:obj:`numpy array`) array of the training set features
        train_labels: (:obj:`numpy array`) array of the training set label
        save_path (str, optional): path to save the model as a pickle file
        **kwargs: Tuning parameters to put into xgboost model, such as n_estimators, learning_rate, max_depth etc.

    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
    """
    # Best result: tree: 150 alpha: 0.1 depth: 3
    xgbmodel = xgb.XGBClassifier(objective ='binary:logistic', **kwargs).fit(train_features, train_labels)
    if save_path is not None:
        save_string = save_path + "//" + "xgb_model.pkl"
        with open(save_string, "wb") as f:
            pickle.dump(xgbmodel, f)
    return xgbmodel

def train_model(args):
    """Orchestrates the training of model from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    
    atp_data = read_raw(**config['train_model']['read_features'])
    atp_matches_p = choose_features(atp_data, **config['train_model']['choose_features'])
    setFeatureType(atp_matches_p, **config['train_model']['setFeatureType'])
    data = split_train_test(atp_matches_p, **config['train_model']['split_train_test'])
    train_features = data[0]
    test_features = data[1]
    train_labels = data[2]
    test_labels = data[3]
    np.savetxt(args.savedatapath + "//train_features.csv", train_features, fmt='%5s', delimiter=",")
    np.savetxt(args.savedatapath + "//test_features.csv", test_features, fmt='%5s', delimiter=",")
    np.savetxt(args.savedatapath + "//train_labels.csv", train_labels, fmt='%s', delimiter=",")
    np.savetxt(args.savedatapath + "//test_labels.csv", test_labels, fmt='%s', delimiter=",")
    newmodel = fit_xgboost(train_features, train_labels, **config['train_model']['fit_xgboost'])
    f.close()
    return newmodel