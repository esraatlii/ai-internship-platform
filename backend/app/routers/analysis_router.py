from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.analysis import AnalysisOut
from app.services.ai_service import AIService


router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["Analysis"],
)


@router.post(
    "/generate",
    response_model=AnalysisOut,
)
def generate_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AIService.generate_analysis(db, current_user)