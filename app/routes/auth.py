# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.auth import SendOTPRequest, VerifyOTPRequest
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.user.user_service import initiate_user_verification, verify_user

router = APIRouter()

@router.post("/send-otp")
def send_otp_endpoint(payload: SendOTPRequest, db: Session = Depends(get_db)):
    identifier = payload.identifier
    try :
        return initiate_user_verification(identifier, db)
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-otp")
def verify_otp_endpoint(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    identifier = payload.identifier
    otp = payload.otp
    try :
        return verify_user(identifier, otp, db)
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))