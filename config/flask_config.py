#from os import path
import os
import sys

# Getting the parent directory of this file. That will function as the project home.
# PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "ACE.AI"
DEBUG = True

# Logging
# Logging
# LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/logging.conf')
# LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/logging.conf')

# Local Database connection config
local_engine_string = 'sqlite:///data/db/playerstats.db'
HOST = "127.0.0.1"
PORT = "3000"

# Database connection config
CONN_TYPE = "mysql+pymysql"
# USER = "Enter mysql Username"
# PASSWORD = "Enter mysql Password"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
DATABASE_NAME = 'playerstats'
#HOST = 'mysql-nw-carsonchen.cvtyax3otjph.us-east-2.rds.amazonaws.com'
#PORT = '3306'
rds_engine_string = "{}://{}:{}@{}:{}/{}".\
format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Final engine string used:
ENGINE_STRING = 'sqlite:///../data/db/playerstats.db'
#ENGINE_STRING = rds_engine_string