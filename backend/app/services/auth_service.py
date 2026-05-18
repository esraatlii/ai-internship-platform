from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password

class AuthService:

    @staticmethod
    def register(db: Session, payload: UserCreate):
        existing_user = UserRepository.get_by_email(db, payload.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu email zaten kayıtlı",
            )
        
        password_hash = hash_password(payload.password)

        user = UserRepository.create(
            db=db,
            full_name=payload.full_name,
            email=payload.email,
            password_hash=password_hash,
        )

        return user