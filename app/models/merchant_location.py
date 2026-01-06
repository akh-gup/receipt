from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.db import Base

class MerchantLocation(Base):
    __tablename__ = "merchant_locations"

    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=True)
    pincode = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
