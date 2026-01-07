import boto3
from app.config.config import settings


# Initialize SNS client
AWS_REGION = settings.AWS_REGION
sns_client = boto3.client("sns", region_name=AWS_REGION)

def send_sns_text_message(message: str, phone: str) -> None:
    sns_client.publish(PhoneNumber=f"+91{phone}", Message=message)
