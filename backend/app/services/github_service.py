import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.github_profile_repository import GitHubProfileRepository
from app.schemas.github_profile import GitHubProfileCreate


class GitHubService:

    @staticmethod
    def extract_username(github_url: str) -> str:
        url = str(github_url).rstrip("/")
        parts = url.split("/")

        username = parts[-1]

        if not username:
            raise HTTPException(
                status_code=400,
                detail="Geçerli bir GitHub kullanıcı linki giriniz.",
            )

        return username

    @staticmethod
    def analyze_profile(
        db: Session,
        current_user: User,
        payload: GitHubProfileCreate,
    ):
        username = GitHubService.extract_username(payload.github_url)

        response = requests.get(
            f"https://api.github.com/users/{username}/repos",
            timeout=10,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="GitHub profili bulunamadı veya repolar alınamadı.",
            )

        repos = response.json()

        technologies_set = set()

        for repo in repos:
            language = repo.get("language")

            if language:
                technologies_set.add(language)

        technologies = ", ".join(sorted(technologies_set))

        profile = GitHubProfileRepository.create(
            db=db,
            user_id=current_user.id,
            github_url=str(payload.github_url),
            username=username,
            technologies=technologies,
        )

        return profile