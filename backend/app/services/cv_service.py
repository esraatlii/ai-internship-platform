import os
import uuid

import pdfplumber
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.cv_repository import CVRepository


UPLOAD_DIR = "uploads"


class CVService:

    @staticmethod
    async def upload_cv(
        db: Session,
        current_user: User,
        file: UploadFile,
    ):
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Sadece PDF dosyası yüklenebilir.",
            )

        unique_name = f"{uuid.uuid4()}.pdf"

        file_path = os.path.join(UPLOAD_DIR, unique_name)

        content = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        extracted_text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    cleaned_text = (
                        text.replace("\x00", "")
                        .strip()
                    )

                    extracted_text += cleaned_text + "\n"

        cv = CVRepository.create(
            db=db,
            user_id=current_user.id,
            file_name=file.filename,
            file_path=file_path,
            extracted_text=extracted_text,
        )

        return cv