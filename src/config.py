from os import path

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "aceScorePredictor"
DEBUG = True

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/logging.conf')

# Source data
data_permanent_url = 'http://s3.us-east-2.amazonaws.com/nw-carsonchen-acedata/atp_data.csv'
file_name = "atp_data.csv"

# Database connection config
DATABASE_PATH = path.join(PROJECT_HOME, 'data/acePredictor.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
DATABASE_NAME = 'msia423'
RDS_HOST = 'mysql-nw-carsonchen.cvtyax3otjph.us-east-2.rds.amazonaws.com'
RDS_PORT = '3306'