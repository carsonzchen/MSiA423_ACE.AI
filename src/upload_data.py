import boto3
import requests
import argparse
import os

cwd = os.getcwd()

data_permanent_url = 'http://s3.us-east-2.amazonaws.com/nw-carsonchen-acedata/atp_data.csv'
file_name = "atp_data.csv"

## upload file to s3 project bucket 
def upload_data(args):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, args.bucket, 'data/{}'.format(file_name))

if __name__ == "__main__":
    r = requests.get(data_permanent_url)
    open(file_name, 'wb').write(r.content) # Temporarily save the data
    parser = argparse.ArgumentParser(description='Data downloaded as ' + cwd + '\\' + file_name)
    parser.add_argument("--bucket", help="input s3 bucket name")
    args = parser.parse_args()
    upload_data(args)
    os.remove(file_name) # Delete data temporarily saved
