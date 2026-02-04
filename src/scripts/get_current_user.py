


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.db.base import get_db
from src.schemas.user import User
from config import SECRET_KEY, ALGORITHM
from src.main import logger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("payload", payload)
        user_id: str | None = payload.get("sub")
    except Exception as e:
        raise e

 
    user = db.query(User).filter(User.id == int(user_id)).first()
 
    return user
