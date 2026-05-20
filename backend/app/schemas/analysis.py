from datetime import datetime
from pydantic import BaseModel


class AnalysisOut(BaseModel):
    id: int
    summary: str
    missing_skills: str
    internship_email: str
    linkedin_message: str
    score: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }