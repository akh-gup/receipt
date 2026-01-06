from app.services.aws.sns_service import send_sns_text_message

def send_phone_otp(phone: str,
                   otp_code: str):
    # Send SMS
    message = f"Your SlipSafe OTP is {otp_code}. It will expire in 5 minutes."
    print("Mobile ", phone, " OTP: ", message)
    return {"message": "OTP sent successfully"}

def send_phone_otp_sns(phone: str,
                       otp_code: str):

    # Send SMS
    message = f"Your SlipSafe OTP is {otp_code}. It will expire in 5 minutes."
    send_sns_text_message(phone, message)
    return {"message": "OTP sent successfully"}