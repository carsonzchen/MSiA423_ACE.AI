import os
import sys
import argparse
import yaml

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

from src.helpers.helpers import read_raw, setFeatureType
import config.flask_config as conf

import logging
logger = logging.getLogger(__name__)

Base = declarative_base()

class ranking_db(Base):
    """ Defines the data model for the table `Rankings`. """

    __tablename__ = 'Ranking'

    player = Column(String(100), primary_key=True, unique=True, nullable=False)
    rank = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        rankings_repr = "<Rankings(player='%s', rank='%s')>"
        return rankings_repr % (self.player, self.rank)

class h2h_db(Base):
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

class surfacewinpct_db(Base):
    """ Defines the data model for the table `Rankings`. """

    __tablename__ = 'SurfaceWinPct'

    player = Column(String(100), primary_key=True, unique=True, nullable=False)
    surface = Column(String(100), unique=False, nullable=False)
    surf_matches = Column(sql.Float, unique=False, nullable=False)
    surf_winpct = Column(sql.Float, unique=False, nullable=False)  

    def __repr__(self):
        h2h_repr = "<H2H(player='%s', surface='%s', surf_matches='%s', surf_winpct='%s')>"
        return h2h_repr % (self.player, self.surface, self.surf_matches, self.surf_winpct)

def df_to_db(args):
    """Orchestrates the writing of csv files to database from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    if args.rds == 'True': # Setting up the database in RDS
        engine_string = conf.rds_engine_string

    else: # Setting up the database in local using sqlite
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