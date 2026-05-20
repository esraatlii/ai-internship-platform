from sqlalchemy.orm import Session

from app.models.analysis import Analysis


class AnalysisRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        cv_id: int,
        github_profile_id: int,
        summary: str,
        missing_skills: str,
        internship_email: str,
        linkedin_message: str,
        score: int,
    ) -> Analysis:
        analysis = Analysis(
            user_id=user_id,
            cv_id=cv_id,
            github_profile_id=github_profile_id,
            summary=summary,
            missing_skills=missing_skills,
            internship_email=internship_email,
            linkedin_message=linkedin_message,
            score=score,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis