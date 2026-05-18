from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from app.models.user import User


bearer = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    token = creds.credentials

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))

    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token geçersiz veya süresi dolmuş.",
        )

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı bulunamadı.",
        )

    return user