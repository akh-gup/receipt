from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_DAYS, ALGORITHM
from jose import jwt, JWTError

from app.models.user import User

def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str, db: Session):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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