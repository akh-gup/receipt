from sqlalchemy.orm import Session
from app.models.merchant_normalization import MerchantNormalization


def normalize_merchant_db(raw_name: str, db: Session) -> str:
    if not raw_name:
        return "UNKNOWN"

    cleaned = raw_name.lower().strip()

    # Fetch mapping from DB
    # TODO: Cache at app load time
    mapping = db.query(MerchantNormalization).filter_by(variant=cleaned).first()
    if mapping:
        return mapping.canonical
    else:
        return raw_name.upper()  # default if not found