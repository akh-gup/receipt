from time import sleep

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.mapper.category_mapper import categorize_receipt
from app.models import Receipt, ReceiptProcessing
from app.parser.amount_parser import extract_total_amount
from app.parser.date_parser import extract_transaction_date
from app.parser.merchant_parser import extract_merchant_name
from app.services.aws import ocr_service
from app.utils.merchant_city import infer_city_from_merchant
from app.utils.normalize import normalize_merchant_db


# TODO: Implement using Celery / SQS worker when production ready
def process_receipt_ocr(receipt_id: int):
    db: Session = next(get_db())

    # Fetch processing record
    processing = db.query(ReceiptProcessing).filter(
        ReceiptProcessing.receipt_id == receipt_id
    ).first()

    if not processing:
        print(f"No processing record found for {receipt_id}")
        return

    processing.status = "IN_PROGRESS"
    db.commit()

    try:
        # Mock OCR delay
        sleep(5)

        # Call OCR service (or mock)
        receipt = db.query(Receipt).get(receipt_id)
        extracted_text = ocr_service.extract_mock_text(receipt.filename)

        # Parse amount, date, merchant, category
        amount = extract_total_amount(extracted_text)
        date = extract_transaction_date(extracted_text)
        merchant = normalize_merchant_db(extract_merchant_name(extracted_text), db)
        category, confidence = categorize_receipt(merchant, extracted_text)

        print("merchant: ",merchant)
        print("city: ", infer_city_from_merchant(merchant, db))

        # Update receipt
        receipt.text = extracted_text
        receipt.amount_total = amount
        receipt.receipt_date = date
        receipt.merchant_name = merchant
        receipt.category = category
        receipt.category_confidence = confidence
        receipt.merchant_city = infer_city_from_merchant(merchant, db)
        db.commit()

        # Update processing record
        processing.status = "COMPLETED"
        processing.completed_at = func.now()
        db.commit()

    except Exception as e:
        processing.status = "FAILED"
        processing.error_message = str(e)
        processing.completed_at = func.now()
        db.commit()
