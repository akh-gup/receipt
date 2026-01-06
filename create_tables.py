from app.db.db import engine, Base
from app.models.user import User # noqa: F401
from app.models.receipt import Receipt # noqa: F401
from app.models.otp import OTP # noqa: F401
from app.models.receipt_processing import ReceiptProcessing # noqa: F401
from app.models.merchant_normalization import MerchantNormalization # noqa: F401
from app.models.merchant_location import MerchantLocation # noqa: F401


def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_all_tables()