import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

from src.helpers.helpers import create_connection, get_session
from src.helpers.helpers import read_raw, setFeatureType
import config.flask_config as conf
import argparse
import yaml

#logging.config.fileConfig(config.LOGGING_CONFIG)
#logger = logging.getLogger('ace-models')
# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

Base = declarative_base()

class rankings_db(Base):
    """ Defines the data model for the table `Rankings`. """

    __tablename__ = 'Rankings'

    player = Column(String(100), primary_key=True, unique=True, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        rankings_repr = "<Rankings(player='%s', rank='%s')>"
        return rankings_repr % (self.player, self.rank)

class rankings_h2h(Base):
    """ Defines the data model for the table `Rankings`. """

    __tablename__ = 'H2H'

    Winner = Column(String(100), primary_key=True, unique=True, nullable=False)
    Loser = Column(String(100), primary_key=True, unique=True, nullable=False)
    h2h_win	= Column(sql.Float, unique=False, nullable=False)
    h2h_lost = Column(sql.Float, unique=False, nullable=False)	
    totalPlayed	= Column(sql.Float, unique=False, nullable=False)
    h2h_win_pct = Column(sql.Float, unique=False, nullable=False)

    def __repr__(self):
        h2h_repr = "<H2H(Winner='%s', Loser='%s', h2h_win='%s', h2h_lost='%s', totalPlayed='%s', h2h_win_pct='%s')>"
        return h2h_repr % (self.Winner, self.Loser, self.h2h_win, self.h2h_lost, self.totalPlayed, self.h2h_win_pct)

def df_to_db(args):
    """Orchestrates the generating of features from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    if args.rds == 'True':
        engine_string = conf.rds_engine_string

    else:
        engine_string = conf.local_engine_string
    
    if args.option in ['Ranking', 'H2H', 'SurfaceWinPct']:
        engine = sql.create_engine(engine_string, echo = True)
        Base.metadata.create_all(engine)
        df = read_raw(**config['create_db_local'][args.option]['read_main'])
        setFeatureType(df, **config['create_db_local'][args.option]['setFeatureType'])
        df.to_sql(args.option, con=engine, if_exists='replace', index=False)
        logger.info("Database created for %s", args.option)

    else:
        raise logger.error("%s is not a valid table option", args.option)

    


    

    
# engine_string = 'sqlite:///../data/db/rankings.db'
# engine = sql.create_engine(engine_string, echo = True)
# Base.metadata.create_all(engine)

# rk = read_raw('../data', 'static_rankings.csv')
# setFeatureType(rk, ['Rank'], 'int')
# rk.to_sql('Ranking', con=engine, if_exists='replace')
# #session.commit()
# logger.info("Database created for player rankings")


# engine.execute("SELECT * FROM Ranking LIMIT 5").fetchall()

# the engine_string format
#conn_type = "mysql+pymysql"
#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
# user = os.environ.get("MYSQL_USER")
# password = os.environ.get("MYSQL_PASSWORD")
# host = os.environ.get("MYSQL_HOST")
# port = os.environ.get("MYSQL_PORT")
#host = config.RDS_HOST
#port = config.RDS_PORT
# database_name = config.DATABASE_NAME
# user = 'root'
# password = '1234asdf'
# host = '127.0.0.1'
# port = 3306
# database_name = 'msia423'



#engine_string = "{}://{}:{}@{}:{}/{}".\
#format(conn_type, user, password, host, port, database_name)
#print(engine_string)

#Session = sessionmaker(bind=engine)
#session = Session()


#session.close()
#test = rankings_db(pair_id = '11', player1_name = 'abs', player2_name = 'ace',
#    predictedWinner = 'abs', p1_win_probability = 80)
#session.add(test)

