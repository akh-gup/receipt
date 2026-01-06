from sqlalchemy import Column, Integer, String, Text, Numeric, Date, ForeignKey
from app.db.db import Base

# TODO: Break-out into multiple tables e.g., metadata, merchant info etc.
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    merchant_name = Column(String)
    merchant_city = Column(String)
    amount_total = Column(Numeric(10, 2))
    currency = Column(String(3), default="INR")
    receipt_date = Column(Date)

    category = Column(String)
    category_confidence = Column(Integer)

    filename = Column(String, unique=True, nullable=False)
    s3_url = Column(String, nullable=False)
    text = Column(Text)

    created_at = Column(Date)