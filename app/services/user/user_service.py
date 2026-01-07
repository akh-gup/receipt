from app.auth.jwt import create_access_token
from app.models.otp import OTP
from app.models.user import User
from sqlalchemy.orm import Session
import random
from app.services.otp.email_otp import send_email_otp
from app.services.otp.phone_otp import send_phone_otp
import re
from datetime import datetime, timedelta

def create_user(identifier: str, db: Session):
    # 1️⃣ Check if user exists, create if not
    user = db.query(User).filter(User.identifier == identifier).first()
    if not user:
        user = User(identifier=identifier)
        db.add(user)
        db.commit()
        db.refresh(user)

def is_otp_matches(identifier: str,
                   otp_code: str,
                   db: Session):
    record = (db.query(OTP)
              .filter(OTP.identifier == identifier, OTP.otp == otp_code)
              .first()
              )
    if not record:
        raise Exception(f"No matching otp found.")

    if record.expires_at < datetime.utcnow():
        raise Exception(f"OTP expired")

    # OTP valid → remove or mark used
    db.delete(record)
    db.commit()
    return True


def is_email(identifier: str) -> bool:
    # Simple regex for email
    return re.match(r"[^@]+@[^@]+\.[^@]+", identifier) is not None

def is_phone(identifier: str) -> bool:
    # Simple check: 10 digits (India)
    return re.match(r"^\d{10}$", identifier) is not None

def save_otp(identifier: str,
             otp_code: str,
             otp_type:str,
             expiry_time:datetime,
             db: Session):
    otp_record = OTP(identifier=identifier,
                     otp=otp_code,
                     otp_type=otp_type,
                     expires_at=expiry_time)
    db.add(otp_record)
    db.commit()

def initiate_user_verification(identifier: str, db: Session):
    try:
        otp = str(random.randint(100000, 999999))
        expiry_time = datetime.utcnow() + timedelta(minutes=5)

        if is_email(identifier):
            save_otp(identifier, otp, "email", expiry_time, db)
            return send_email_otp(identifier, otp)
        elif is_phone(identifier):
            save_otp(identifier, otp, "phone", expiry_time, db)
            return send_phone_otp(identifier, otp)
        else:
            raise Exception("Identifier must be a valid email or 10-digit phone number")
    except Exception as e:
        raise Exception(str(e))

def verify_user(identifier: str, otp: str, db: Session):
    try:
        # ✅ Is OTP valid
        is_otp_matches(identifier, otp, db)

        # ✅ OTP valid → create user if not already
        create_user(identifier, db)

        # ✅ Issue JWT
        access_token = create_access_token(subject=identifier)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise Exception(str(e))
