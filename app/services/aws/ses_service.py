import boto3
from app.config.config import settings

# Initialize SES client
AWS_REGION = settings.AWS_REGION
ses_client = boto3.client("ses", region_name=AWS_REGION)

def send_ses_text_message(otp_code: str, recipient_email: str) -> None:
    # SES send email
    try:
        ses_client.send_email(
            Source="slipsafe0000@gmail.com",  # Verified sender email
            Destination={"ToAddresses": [recipient_email]},
            Message={
                "Subject": {"Data": "SlipSafe OTP"},
                "Body": {"Text": {"Data": f"Your SlipSafe OTP is {otp_code}. It expires in 5 minutes."}}
            },
        )
    except Exception as e:
        raise Exception(f"Error sending OTP via SES: {str(e)}")


