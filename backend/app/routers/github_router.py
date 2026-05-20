from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.github_profile import GitHubProfileCreate, GitHubProfileOut
from app.services.github_service import GitHubService


router = APIRouter(
    prefix="/api/v1/github",
    tags=["GitHub"],
)


@router.post(
    "/analyze",
    response_model=GitHubProfileOut,
)
def analyze_github_profile(
    payload: GitHubProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GitHubService.analyze_profile(
        db=db,
        current_user=current_user,
        payload=payload,
    )