from boto3.session import Session
import requests

#ACCESS_KEY = "My Key"
#SECRET_KEY = "SK"

data_permanent_url = 'http://s3.us-east-2.amazonaws.com/nw-carsonchen-acedata/atp_data.csv'
newbucketname = "nw-carsonchen-423ace"
data_path = "atp_data.csv"
folder_name = "data"

## upload file to s3 project bucket 
def upload_data(ACCESS_KEY,SECRET_KEY, bucket_name, data_path, folder_name):
    session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3 = session.resource('s3')
    s3.meta.client.upload_file(data_path, bucket_name,'%s/%s' % (folder_name,'atp_data.csv'))

if __name__ == "__main__":
	r = requests.get(data_permanent_url)
	open('atp_data.csv', 'wb').write(r.content)
	upload_data(ACCESS_KEY,SECRET_KEY, newbucketname, data_path, folder_name)