import uuid

from fastapi import BackgroundTasks
from fastapi import UploadFile, File
from sqlalchemy.orm import Session

from app.models import ReceiptProcessing
from app.models.receipt import Receipt
from app.models.user import User
from app.schemas.receipt_filter import ReceiptFilter
from app.services.aws import s3_service
from app.services.receipts.background_ocr import process_receipt_ocr
from app.utils.sorting import SORT_FIELD_MAP


def get_user_receipts(user: User, filters: ReceiptFilter, db: Session):
    query = db.query(Receipt).filter(Receipt.user_id == user.id)
    if filters.start_date:
        query = query.filter(Receipt.receipt_date >= filters.start_date)

    if filters.end_date:
        query = query.filter(Receipt.receipt_date <= filters.end_date)

    if filters.category:
        query = query.filter(Receipt.category.ilike(f"%{filters.category}%"))

    if filters.merchant:
        query = query.filter(Receipt.merchant_name.ilike(f"%{filters.merchant}%"))

    if filters.min_amount:
        query = query.filter(Receipt.amount_total >= filters.min_amount)

    if filters.max_amount:
        query = query.filter(Receipt.amount_total <= filters.max_amount)

    if filters.q:
        query = query.filter(Receipt.raw_text.ilike(f"%{filters.q}%"))

    sort_column = SORT_FIELD_MAP[filters.sort_by]

    if filters.order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = query.count()
    receipts = (
        query
        .order_by(Receipt.receipt_date.desc())
        .offset(filters.offset)
        .limit(filters.limit)
        .all()
    )
    return {
        "total": total,
        "limit": filters.limit,
        "offset": filters.offset,
        "sort_by": filters.sort_by,
        "order": filters.order,
        "receipts": receipts
    }

def upload_user_receipt(user: User,
                        db: Session,
                        file: UploadFile = File(...),
                        background_tasks: BackgroundTasks = None):
    filename = f"{uuid.uuid4()}_{file.filename}"

    # Upload to S3
    file_url = s3_service.upload_file_to_s3(file.file, filename)

    # Save to Postgres
    receipt = Receipt(
        user_id=user.id,
        filename=filename,
        s3_url=file_url
    )
    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    processing = ReceiptProcessing(
        receipt_id=receipt.id,
        stage="OCR",
        status="PENDING"
    )
    db.add(processing)
    db.commit()

    # Queue background OCR task
    background_tasks.add_task(process_receipt_ocr, receipt.id)

    return {
        "id": receipt.id,
        "filename": receipt.filename,
        "s3_url": receipt.s3_url
    }