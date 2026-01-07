from app.config.config import settings
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Read credentials from environment variables
AWS_REGION = settings.AWS_REGION
S3_BUCKET = settings.S3_BUCKET

# Initialize S3 client (credentials are automatically read from env)
s3_client = boto3.client("s3",region_name=AWS_REGION)

def upload_file_to_s3(file, filename):
    """
    Uploads a file object to S3 and returns the public URL.
    """
    try:
        s3_client.upload_fileobj(file, S3_BUCKET, filename)
        file_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return file_url
    except NoCredentialsError:
        raise Exception("AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as environment variables.")
    except ClientError as e:
        raise Exception(f"Error uploading to S3: {e}")
