from sqlalchemy.orm import Session

from app.models.cv import CV


class CVRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        file_name: str,
        file_path: str,
        extracted_text: str,
    ) -> CV:

        cv = CV(
            user_id=user_id,
            file_name=file_name,
            file_path=file_path,
            extracted_text=extracted_text,
        )

        db.add(cv)
        db.commit()
        db.refresh(cv)

        return cv