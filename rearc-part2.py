import boto3
import requests

S3_BUCKET_NAME = "vinakar-rearcbucket"
DATA_SOURCE = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"

# Initialize S3 resource and get the bucket
s3 = boto3.resource('s3', aws_access_key_id=os.getenv('AWS_ACCESS_ID'),
         aws_secret_access_key= os.getenv('AWS_ACCESS_KEY'))
bucket = s3.Bucket(S3_BUCKET_NAME)

# Request the API data and parse it
r = requests.get(DATA_SOURCE)
data = r.text

# Upload the data to S3
bucket.put_object(Key="population.json", Body=data)