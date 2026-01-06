from sqlalchemy.orm import Session
from app.models import MerchantLocation

def infer_city_from_merchant(canonical_merchant: str, db: Session):
    """
    Returns city (or None) for a given canonical merchant name
    """
    if not canonical_merchant:
        return None

    # TODO: Cache at app load time
    loc = db.query(MerchantLocation).filter_by(merchant=canonical_merchant).first()
    if loc:
        return loc.city
    return None