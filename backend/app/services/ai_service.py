import json

from fastapi import HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.cv_repository import CVRepository
from app.repositories.github_profile_repository import GitHubProfileRepository


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

class AIService:

    @staticmethod
    def generate_analysis(db: Session, current_user: User):
        cv = CVRepository.get_latest_by_user_id(db, current_user.id)
        github_profile = GitHubProfileRepository.get_latest_by_user_id(db, current_user.id)

        if not cv:
            raise HTTPException(status_code=400, detail="Önce CV yüklemelisiniz.")

        if not github_profile:
            raise HTTPException(status_code=400, detail="Önce GitHub analizi yapmalısınız.")

        prompt = f"""
Sen deneyimli bir yazılım kariyer danışmanısın.

Aşağıdaki CV metnini ve GitHub teknoloji listesini analiz et.

CV METNİ:
{cv.extracted_text[:6000]}

GITHUB TEKNOLOJİLERİ:
{github_profile.technologies}

Bana SADECE geçerli JSON döndür.

Format:
{{
  "summary": "...",
  "missing_skills": "...",
  "internship_email": "...",
  "linkedin_message": "...",
  "score": 75
}}

Kurallar:
- Türkçe cevap ver.
- score 0-100 arasında sayı olsun.
- missing_skills kısmında eksik teknolojileri açıkça söyle.
- internship_email profesyonel staj başvuru maili olsun.
- linkedin_message kısa ve doğal LinkedIn mesajı olsun.
"""

        response = client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        raw_text = response.choices[0].message.content

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="AI çıktısı JSON formatında dönmedi.",
            )

        analysis = AnalysisRepository.create(
            db=db,
            user_id=current_user.id,
            cv_id=cv.id,
            github_profile_id=github_profile.id,
            summary=data.get("summary", ""),
            missing_skills=data.get("missing_skills", ""),
            internship_email=data.get("internship_email", ""),
            linkedin_message=data.get("linkedin_message", ""),
            score=data.get("score", 0),
        )

        return analysis