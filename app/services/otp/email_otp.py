from app.services.aws.ses_service import send_ses_text_message

def send_email_otp(recipient_email: str,
                   otp_code: str):
    print("Email OTP: ", otp_code)
    return {"message": f"OTP sent to {recipient_email}"}

def send_email_otp_ses(recipient_email: str,
                       otp_code: str):
    send_ses_text_message(otp_code, recipient_email)
    return {"message": f"OTP sent to {recipient_email}"}
