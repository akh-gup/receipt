import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
S3_BUCKET = os.environ.get("S3_BUCKET", "slipsafe-app-poc")

# Initialize Textract client (credentials are read from env)
textract_client = boto3.client("textract", region_name=AWS_REGION)

# For POC: mock Textract to avoid hitting Free Tier limit
def extract_mock_text(filename: str) -> str:
    """
    Mock OCR output for development.
    """
    return f"Mock receipt text for {filename}:\nDate: 04/01/2026\nTotal: ₹500\nMerchant: ABC Store"

def extract_text(filename):
    """
    Calls AWS Textract to detect text from a file in S3.
    """
    try:
        response = textract_client.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": S3_BUCKET,
                    "Name": filename
                }
            }
        )
        # Extract plain text from Textract response
        text = ""
        for item in response.get("Blocks", []):
            if item.get("BlockType") == "LINE":
                text += item.get("Text", "") + "\n"
        return text

    except NoCredentialsError:
        raise Exception("AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as environment variables.")
    except ClientError as e:
        raise Exception(f"Error calling Textract: {e}")