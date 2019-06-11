import boto3
import requests
import yaml
import argparse
import os

import logging
logger = logging.getLogger(__name__)

def download_data(sourceurl, rawfilepath, filename):
    """
    Downloads raw data from source public bucket (defined in config) to the local current folder
    
    :param sourceurl (str): url of the public data
    :param rawfilepath (str): path of the saved file
    :param filename (str): name of the saved file

    :return: None
    """
    path = rawfilepath + '//' + filename
    try:
        r = requests.get(sourceurl)
        logger.info("Download %s from bucket %s", path, sourceurl)
        open(path, 'wb').write(r.content)
    except requests.exceptions.RequestException:
        logger.error("Error: Unable to download file %s", filename)

def upload_data(args):
    """
    Upload raw data downloaded  in the local current folder to a bucket of user input, erases local file
    :param args (argparse): user-input s3 bucket name for uploading the file 

    :return: None
    """
    s3 = boto3.client('s3')
    try:
        filepath = args.localfolder + '//' + args.filename
        s3.upload_file(filepath, args.bucket, 'data/{}'.format(args.filename))
        logger.info("Uploaded %s to bucket %s", args.filename, args.bucket)
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Error: Upload unsuccessful")

def run_download_source(args):
    """Orchestrates the downloading of source data from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    download_data(**config["run_download_source"]['download_data'])
    f.close()