import boto3
import os

# Initialize SNS client
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
sns_client = boto3.client("sns", region_name=AWS_REGION)

def send_sns_text_message(message: str, phone: str) -> None:
    sns_client.publish(PhoneNumber=f"+91{phone}", Message=message)
