from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.cv import CVOut
from app.services.cv_service import CVService


router = APIRouter(
    prefix="/api/v1/cv",
    tags=["CV"],
)


@router.post(
    "/upload",
    response_model=CVOut,
)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await CVService.upload_cv(
        db=db,
        current_user=current_user,
        file=file,
    )