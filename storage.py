import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()

bucket_name = os.getenv('BUCKET_NAME')
region = os.getenv('AWS_REGION')

s3 = boto3.client('s3')

def addFile(subfolder, file_path):
    try:
        s3.upload_file(file_path, bucket_name, subfolder)
        file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{subfolder}"
        return file_url

    except FileNotFoundError:
        print(f"The file was not found")
        return FileNotFoundError
    except NoCredentialsError:
        print("Credentials not available")
        return NoCredentialsError
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return PartialCredentialsError
    except Exception as e:
        print(f"An error occurred: {e}")
        return e

