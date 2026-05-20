from datetime import datetime

from pydantic import BaseModel


class CVOut(BaseModel):
    id: int
    file_name: str
    extracted_text: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }