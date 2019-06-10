import boto3
import requests
import yaml
import argparse
import os
import logging
import logging.config

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('upload_data')

## download file from external data source
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

## upload file to s3 project bucket
def upload_data(args):
    """
    Upload raw data downloaded  in the local current folder to a bucket of user input, erases local file
    :param args (argparse): user-input s3 bucket name for uploading the file 

    :return: None
    """
    s3 = boto3.client('s3')
    try:
        filepath = args.localfolder + '//' + args.filename
        s3.upload_file(filepath, args.bucket, 'data/{}'.format(args.file_name))
        logger.info("Uploaded %s to bucket %s", args.filename, args.bucket)
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Error: Upload unsuccessful")

def run_download_source(args):
    """Orchestrates the generating of features from commandline arguments."""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    download_data(**config["run_download_source"]['download_data'])
    f.close()