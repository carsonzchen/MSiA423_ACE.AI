import boto3
import requests
import argparse
import os
import logging
import logging.config

import config
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='pipeline_log.log', level=logging.DEBUG)
logger = logging.getLogger('upload_data')
cwd = os.getcwd()

## download file from external data source
def download_data(sourceurl, filename):
    """
    Downloads raw data from source public bucket (defined in config) to the local current folder
    
    :param sourceurl (str): url of the public data
    :param filename (str): name of the saved file

    :return: None
    """
    try:
        r = requests.get(sourceurl)
        logger.info("Download %s from bucket %s", filename, sourceurl)
        open(filename, 'wb').write(r.content)
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
        s3.upload_file(config.file_name, args.bucket, 'data/{}'.format(config.file_name))
        logger.info("Uploaded %s to bucket %s", config.file_name, args.bucket)
        os.remove(config.file_name) # Delete data temporarily saved
    except boto3.exceptions.S3UploadFailedError:
        logger.error("Error: Upload unsuccessful")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload data to specific S3 bucket')
    parser.add_argument("--bucket", help="input s3 bucket name")
    args = parser.parse_args()
    download_data(config.data_permanent_url, config.file_name)
    upload_data(args)