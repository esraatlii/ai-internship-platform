from datetime import datetime
from pydantic import BaseModel, HttpUrl


class GitHubProfileCreate(BaseModel):
    github_url: HttpUrl


class GitHubProfileOut(BaseModel):
    id: int
    github_url: str
    username: str
    technologies: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }