import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

from helpers import create_connection, get_session
import argparse
import config

#logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('ace-models')

Base = declarative_base()

class Prediction(Base):
    """ Defines the data model for the table `tweet`. """

    __tablename__ = 'prediction'

    pair_id = Column(String(100), primary_key=True, unique=True, nullable=False)
    player1_name = Column(String(100), unique=False, nullable=False)
    player2_name = Column(String(100), unique=False, nullable=False)
    predictedWinner = Column(String(100), unique=False, nullable=False)
    p1_win_probability = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        prediction_repr = "<Prediction(pair_id='%s', player1_name='%s', player2_name='%s', predictedWinner='%s', p1_win_probability='%s')>"
        return prediction_repr % (self.pair_id, self.player1_name, self.player2_name, self.predictedWinner, self.p1_win_probability)


# the engine_string format
#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
#host = os.environ.get("MYSQL_HOST")
#port = os.environ.get("MYSQL_PORT")
host = config.RDS_HOST
port = config.RDS_PORT
database_name = config.DATABASE_NAME

engine_string = "{}://{}:{}@{}:{}/{}".\
format(conn_type, user, password, host, port, database_name)
#print(engine_string)
engine = sql.create_engine(engine_string)
Base.metadata.create_all(engine)

# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)