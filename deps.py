from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole, AccountStatus

DbSession = Annotated[Session, Depends(get_db)]
bearer = HTTPBearer(auto_error=False)

def get_current_user(db: DbSession, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> User:
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="د ننوتلو معتبر ټوکن اړین دی")
    if credentials is None:
        raise error
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        raise error
    user = db.get(User, user_id)
    if not user or user.status != AccountStatus.active:
        raise HTTPException(status_code=403, detail="اکوانټ فعال نه دی")
    return user

def require_roles(*roles: UserRole):
    def checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="تاسو دې برخې ته اجازه نه لرئ")
        return user
    return checker
