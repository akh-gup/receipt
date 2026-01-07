from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.models.user import User

def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(days=7)
    payload = {
        "sub": subject,
        "exp": expire
    }
    return jwt.encode(payload, "dev-secret-key", algorithm="HS256")

def get_user_from_token(token: str, db: Session):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, "dev-secret-key", algorithms=["HS256"])
        identifier: str = payload.get("sub")
        if identifier is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user from DB
    user = db.query(User).filter(User.identifier == identifier).first()
    if user is None:
        raise credentials_exception

    return user