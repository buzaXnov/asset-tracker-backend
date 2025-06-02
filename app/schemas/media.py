from datetime import datetime

from pydantic import BaseModel


class MediaOut(BaseModel):
    id: int
    filename: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
