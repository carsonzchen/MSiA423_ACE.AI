import boto3
import requests
import argparse
import os
cwd = os.getcwd()

#ACCESS_KEY = "My Key"
#SECRET_KEY = "SK"

data_permanent_url = 'http://s3.us-east-2.amazonaws.com/nw-carsonchen-acedata/atp_data.csv'
file_name = "atp_data.csv"

## upload file to s3 project bucket 
def upload_data(args, filename, output = ''):
    s3 = boto.client('s3')
    s3.upload_file(args.bucket, filename, output)

if __name__ == "__main__":
	r = requests.get(data_permanent_url)
	open(file_name, 'wb').write(r.content)
    parser = argparse.ArgumentParser(description='Data downloaded as ' + cwd + '\\' + file_name)
    parser.add_argument("--bucket", help="input s3 bucket name")
    args = parser.parse_args()
    upload_data(args, file_name)