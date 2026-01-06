from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import BackgroundTasks

from sqlalchemy.orm import Session

from app.models import ReceiptProcessing
from app.schemas.receipt_filter import ReceiptFilter
from app.services.receipts.receipt_service import get_user_receipts, upload_user_receipt
from app.auth.jwt import get_user_from_token
from app.db.db import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="verify-otp")

@router.get("/receipts")
def get_receipts(filters: ReceiptFilter = Depends(),
                 token: str = Depends(oauth2_scheme),
                 db: Session = Depends(get_db)):
    user = get_user_from_token(token, db)
    return get_user_receipts(user, filters, db)

@router.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...),
                         token: str = Depends(oauth2_scheme),
                         db: Session = Depends(get_db),
                         background_tasks: BackgroundTasks = None):
    user = get_user_from_token(token, db)
    return upload_user_receipt(user, db, file, background_tasks)

@router.get("/receipts/{receipt_id}/status")
def get_receipt_status(receipt_id: str, db: Session = Depends(get_db)):
    processing = db.query(ReceiptProcessing).filter(
        ReceiptProcessing.receipt_id == receipt_id
    ).first()

    if not processing:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return {
        "stage": processing.stage,
        "status": processing.status,
        "error_message": processing.error_message
    }