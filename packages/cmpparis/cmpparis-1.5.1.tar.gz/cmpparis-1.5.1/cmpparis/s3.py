import boto3
import os
import sys

from botocore.exceptions import ClientError

from cmpparis.parameters_utils import *
from cmpparis.ses_utils import *

class S3:
    def __init__(self, aws_region_name, aws_bucket_name):
        self.aws_region_name = aws_region_name
        self.aws_bucket_name = aws_bucket_name
        self.s3 = boto3.client('s3', region_name=aws_region_name)

    # Function to download file from S3 bucket
    def download_file_from_s3(self, s3_key, local_filename):
        try:
            self.s3.download_file(self.aws_bucket_name, s3_key, local_filename)
            print("The file has been successfully downloaded from the S3 bucket")
            return True
        except ClientError as e:
            error_message = f"Error while downloading the CSV file from the S3 bucket : {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    # Function to get file from S3 bucket
    def get_file_from_s3(self, s3_key):
        try:
            response = self.s3.get_object(Bucket=self.aws_bucket_name, Key=s3_key)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            error_message = f"Error while getting the file from S3 : {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    # Function to get all files from S3 bucket location
    def get_files_from_s3(self, s3_key):
        try:
            response = self.s3.list_objects_v2(Bucket=self.aws_bucket_name, Prefix=s3_key)
            files = []
            for obj in response.get('Contents', []):
                files.append(obj['Key'])
            return files
        except ClientError as e:
            error_message = f"Error while getting the files from S3 : {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    # Function to upload a file to S3
    def upload_file_to_s3(self, local_filename, s3_key = None):
        try:
            if (s3_key is None):
                s3_key = os.path.basename(local_filename)

            self.s3.upload_file(local_filename, self.aws_bucket_name, s3_key)
            print("File uploaded and archived to S3")
            return True
        except ClientError as e:
            error_message = f"Error while uploading file to S3 : {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)

    # Function to delete file from S3 bucket
    def delete_file_from_s3(self, s3_key):
        try:
            self.s3.delete_object(Bucket=self.aws_bucket_name, Key=s3_key)
            print("File deleted from S3")
            return True
        except ClientError as e:
            error_message = f"Error while deleting file from S3 : {e}"
            print(error_message)
            send_email_to_support(error_message)

            sys.exit(1)