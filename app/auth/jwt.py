from datetime import datetime, timedelta
from app.config.config import settings
from fastapi import HTTPException
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.models.user import User

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_TOKEN_EXPIRE_DAYS = settings.JWT_TOKEN_EXPIRE_DAYS

def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(days=JWT_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "exp": expire
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_user_from_token(token: str, db: Session):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
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