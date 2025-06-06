from typing import List

from pydantic import BaseModel

from app.schemas.detection import DetectionOut  # ✅ Required import


class AssetQuestionCreate(BaseModel):
    question_text: str


class AssetDefinitionCreate(BaseModel):
    label: str
    questions: List[AssetQuestionCreate]


class AssetWithDetectionsOut(BaseModel):
    id: int
    label: str
    detections: List[DetectionOut]
