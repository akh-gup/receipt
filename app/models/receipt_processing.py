import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.db import Base


class ReceiptProcessing(Base):
    __tablename__ = "receipt_processing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    receipt_id = Column(
        Integer,
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    stage = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False)

    error_message = Column(Text, nullable=True)
    attempt_count = Column(Integer, default=0, nullable=False)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )