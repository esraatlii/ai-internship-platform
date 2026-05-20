from sqlalchemy.orm import Session

from app.models.github_profile import GitHubProfile


class GitHubProfileRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        github_url: str,
        username: str,
        technologies: str,
    ) -> GitHubProfile:
        profile = GitHubProfile(
            user_id=user_id,
            github_url=github_url,
            username=username,
            technologies=technologies,
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile