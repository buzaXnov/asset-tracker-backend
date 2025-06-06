from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base


class DetectionAnswer(Base):
    __tablename__ = "detection_answers"
    id = Column(Integer, primary_key=True)
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=False)
    answer_text = Column(Text, nullable=False)

    detection = relationship("Detection", back_populates="answers")
