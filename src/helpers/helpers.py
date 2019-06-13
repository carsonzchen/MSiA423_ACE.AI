import datetime
import numpy as np
import pandas as pd
import os
import logging
logger = logging.getLogger(__name__)

#import sqlalchemy
#from sqlalchemy.orm import sessionmaker

def read_raw(rawfilepath, filename, **kwargs):
    """
    Reads data from a csv file from a specified path
    
    :param rawfilepath (str): relative path of the target file
    :param filename (str): name of the file to load
    :param **kwargs: read data types. Default: encoding = "ISO-8859-1", dtype=object

    :return: a pandas dataframe of the raw file
    """
    path = rawfilepath + '//' + filename
    try:
        rawfile = pd.read_csv(path, encoding = "ISO-8859-1", dtype=object)
        logger.info("Load file from %s", path)
        return rawfile
    except:
        raise logger.error("Error: Unable to load file %s", filename)

def save_dataset(df, rawfilepath, filename):
    """
    Saves data from a pandas dataframe to a csv file in a specified path
    
    :param rawfilepath (str): relative path of the target file to save
    :param filename (str): name of the file to save

    :return: none
    """
    path = rawfilepath + '//' + filename
    df.to_csv(path, index=False)
    
def setFeatureType(df, columns, input_type):
    """
    Bulk-setting columns to a specific data type specified
    
    :param df (dataFrame): dataframe object to work with
    :param columns (list): list of columns to re-set data type
    :param input_type (str): specify data type such as 'int', 'str'

    :return: none
    """
    for column in columns:
        try:
            df[column] = df[column].astype(input_type)
        except:
            logger.error("Variable %s cannot be set to data type %s", column, input_type)


def fillColumnNAs(df, columns, value = 0):
    """
    Bulk-replacing NANs in specific columns to defined values
    
    :param df (dataFrame): dataframe object to work with
    :param columns (list): list of columns to re-set data type
    :param input_type (str): value to be replaced to, default is 0

    :return: none
    """
    for column in columns:
        df[column] = df[column].fillna(value)