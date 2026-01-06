from sqlalchemy import Column, Integer, String, DateTime
from app.db.db import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)  # email or phone
    otp = Column(String)
    otp_type = Column(String)  # email or phone
    expires_at = Column(DateTime)