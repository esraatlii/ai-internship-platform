from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, TokenOut, UserLogin
from app.services.auth_service import AuthService

from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register(db, payload)

@router.post(
    "/login",
    response_model=TokenOut,
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login(db,payload)


@router.get(
    "/me",
    response_model=UserOut,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
