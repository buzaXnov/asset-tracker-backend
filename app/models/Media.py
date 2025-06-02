from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "image" or "video"

    user = relationship("User", back_populates="media")
    detections = relationship("Detection", back_populates="media")
