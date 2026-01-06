from app.db.db import get_db
from app.models.merchant_normalization import MerchantNormalization
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

MERCHANTS = [
    {"variant": "DMart", "canonical": "DMART"},
    {"variant": "D-Mart", "canonical": "DMART"},
    {"variant": "Big Bazaar", "canonical": "BIG BAZAAR"},
    {"variant": "merchant abc store", "canonical": "ABC STORE"},
]

def insert_merchants(db: Session):
    for m in MERCHANTS:
        stmt = insert(MerchantNormalization).values(**m).on_conflict_do_nothing(index_elements=['variant'])
        db.execute(stmt)
    db.commit()
    print("Merchants inserted!")

if __name__ == "__main__":
    db = next(get_db())
    insert_merchants(db)