from app.db.db import get_db
from app.models.merchant_location import MerchantLocation
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

MERCHANTS = [
    {"merchant": "ABC STORE", "city": "Gurgaon", "state": "Haryana", "pincode": "122001"},
]

def insert_merchants_location(db: Session):
    for loc in MERCHANTS:
        exists = db.query(MerchantLocation).filter_by(merchant=loc['merchant'],city=loc['city']).first()
        if not exists:
            db.add(MerchantLocation(**loc))
    db.commit()
    print("Merchants Location inserted!")

if __name__ == "__main__":
    db = next(get_db())
    insert_merchants_location(db)