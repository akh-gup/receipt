from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.db import Base

class MerchantNormalization(Base):
    __tablename__ = "merchant_normalization"

    id = Column(Integer, primary_key=True, index=True)
    variant = Column(String(255), unique=True, nullable=False)
    canonical = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())