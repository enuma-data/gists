import boto3
import sys
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def download_file_from_s3(access_key, secret_key, s3_arn, local_file_name):
    # Parse the S3 ARN
    arn_parts = s3_arn.split(':')
    if len(arn_parts) < 6 or arn_parts[0] != 'arn' or arn_parts[1] != 'aws' or arn_parts[2] != 's3':
        raise ValueError(f"Invalid S3 ARN: {s3_arn}")
    
    bucket_name = arn_parts[5].split('/')[0]
    object_key = '/'.join(arn_parts[5].split('/')[1:])
    
    # Initialize the S3 client
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    try:
        # Download the file
        s3_client.download_file(bucket_name, object_key, local_file_name)
        print(f"File '{local_file_name}' downloaded successfully from bucket '{bucket_name}'.")
    except NoCredentialsError:
        print("Error: AWS credentials not available.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python download_file.py <access_key> <secret_key> <s3_arn> <local_file_name>")
        sys.exit(1)
    
    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    s3_arn = sys.argv[3]
    local_file_name = sys.argv[4]
    
    download_file_from_s3(access_key, secret_key, s3_arn, local_file_name)
