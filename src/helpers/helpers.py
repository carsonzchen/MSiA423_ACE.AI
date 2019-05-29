import datetime
import numpy as np
import pandas as pd
import os
import logging
logger = logging.getLogger(__name__)

#import sqlalchemy
#from sqlalchemy.orm import sessionmaker

def read_raw(rawfilepath, filename):
    """
    Reads data from a csv file from a specified path
    
    :param rawfilepath (str): relative path of the target file
    :param filename (str): name of the file to load

    :return: a pandas dataframe of the raw file
    """
    path = rawfilepath + '\\' + filename
    try:
        rawfile = pd.read_csv(path, encoding = "ISO-8859-1", dtype=object)
        logger.info("Load file from %s", path)
        return rawfile
    except:
        logger.error("Error: Unable to load file %s", filename)

def save_dataset(df, rawfilepath, filename):
    """
    Saves data from a pandas dataframe to a csv file in a specified path
    
    :param rawfilepath (str): relative path of the target file to save
    :param filename (str): name of the file to save

    :return: none
    """
    path = rawfilepath + '\\' + filename
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

class Timer:
    """Times the code within the with statement and logs the elapsed time when it closes.

           Args:
               function_name(string): Name of function being timed
               logger (obj:`logging.logger`): Logger to have elapsed time logged to
   """
    def __init__(self, function_name, logger):
        self.logger = logger
        self.function = function_name

    def __enter__(self):
        self.start = datetime.datetime.now()

        return self

    def __exit__(self, *args):
        self.end = datetime.datetime.now()
        self.interval = self.end - self.start
        self.logger.info("%s took %0.2f seconds", self.function, self.interval.total_seconds())


def format_sql(sql, replace_sqlvar=None, replace_var=None, python=True):
    """Formats SQL query string for Python interpretation and with variables replaced.

    Args:
        sql (string): String with SQL query
        replace_sqlvar (dict, optional): If given, replaces variables of the format ${var:dict-key} with the value
            in the dictionary corresponding to that dict-key.
        replace_var (dict, optional): If given, replaces variables of the format {dict-key} with the value
            in the dictionary corresponding to that dict-key.
        python: If True, formats the query to be passed into a Python SQL querying function by replacing "%" with
            "%%" since % is a special character in Python

    Returns: string of SQL query with variables replaced and optionally formatted for Python

    """
    if replace_sqlvar is not None:
        for var in replace_sqlvar:
            sql = sql.replace("${var:%s}" % var, replace_sqlvar[var])

    if replace_var is not None:
        sql = sql.format(**replace_var)

    if python:
        sql = sql.replace("%", "%%")

    return sql


def ifin(param, dictionary, alt=None):

    assert type(dictionary) == dict
    if param in dictionary:
        return dictionary[param]
    else:
        return alt


def create_connection(host='127.0.0.1', database="", sqltype="", port=10000,
                      user_env="", password_env="",
                      username=None, password=None, dbconfig=None, engine_string=None):

    if engine_string is None:
        if dbconfig is not None:
            with open(dbconfig, "r") as f:
                db = yaml.load(f)

            host = db["host"]
            database = ifin("dbname", db, "")
            sqltype = ifin("type", db, sqltype)
            port = db["port"]
            user_env = db["user_env"]
            password_env = db["password_env"]

        username = os.environ.get(user_env) if username is None else username
        password = os.environ.get(password_env) if password is None else password

        engine_string = "{sqltype}://{username}:{password}@{host}:{port}/{database}"
        engine_string = engine_string.format(sqltype=sqltype, username=username,
                                             password=password, host=host, port=port, database=database)

    conn = sqlalchemy.create_engine(engine_string)

    return conn


def get_session(engine=None, engine_string=None):
    """

    Args:
        engine_string: SQLAlchemy connection string in the form of:

            "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """

    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
