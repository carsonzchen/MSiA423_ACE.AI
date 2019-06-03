"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`
"""
import argparse
import logging.config
#from app.app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
#logger = logging.getLogger("run-penny-lane")
#logger.debug('Test log')

from src.upload_data import run_download_source
from src.preprocess import run_trimdata, run_rankingstable, run_h2h_record, run_surface_record
from src.generate_features import run_features
from src.train_model import train_model

#def run_app(args):
#    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    sb_download = subparsers.add_parser("run_download_source", description="Load data into a dataframe")
    sb_download.add_argument('--config', help='path to yaml file with configurations')
    sb_download.set_defaults(func=run_download_source)

    sb_trim = subparsers.add_parser("run_trimdata", description="Load data into a dataframe")
    sb_trim.add_argument('--config', help='path to yaml file with configurations')
    sb_trim.set_defaults(func=run_trimdata)

    sb_rankings = subparsers.add_parser("run_rankingstable", description="Load data into a dataframe")
    sb_rankings.add_argument('--config', help='path to yaml file with configurations')
    sb_rankings.set_defaults(func=run_rankingstable)

    sb_h2h = subparsers.add_parser("run_h2h_record", description="Load data into a dataframe")
    sb_h2h.add_argument('--config', help='path to yaml file with configurations')
    sb_h2h.set_defaults(func=run_h2h_record)

    sb_surface = subparsers.add_parser("run_surface_record", description="Load data into a dataframe")
    sb_surface.add_argument('--config', help='path to yaml file with configurations')
    sb_surface.set_defaults(func=run_surface_record)

    sb_feature = subparsers.add_parser("run_features", description="Load data into a dataframe")
    sb_feature.add_argument('--config', help='path to yaml file with configurations')
    sb_feature.set_defaults(func=run_features)

    sb_model = subparsers.add_parser("train_model", description="Load data into a dataframe")
    sb_model.add_argument('--config', help='path to yaml file with configurations')
    sb_model.set_defaults(func=train_model)

    args = parser.parse_args()
    args.func(args)