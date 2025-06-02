from typing import List

from pydantic import BaseModel


class DetectionAnswerOut(BaseModel):
    answer_text: str


class DetectionOut(BaseModel):
    id: int
    bbox: List[float]
    coordinate_top: List[float]
    coordinate_bottom: List[float]
    answers: List[DetectionAnswerOut]
