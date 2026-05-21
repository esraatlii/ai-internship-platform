from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token

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

    @staticmethod
    def login(db: Session, payload: UserLogin):
        user = UserRepository.get_by_email(db, payload.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email veya şifre hatalı",
            )
        
        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email veya şifre hatalı.",
            )
        
        access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "current_user": user,
        }