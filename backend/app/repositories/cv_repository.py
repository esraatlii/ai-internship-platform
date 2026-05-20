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
    
    @staticmethod
    def get_latest_by_user_id(db: Session, user_id: int):
        return (
            db.query(CV)
            .filter(CV.user_id == user_id)
            .order_by(CV.created_at.desc())
            .first()
        )