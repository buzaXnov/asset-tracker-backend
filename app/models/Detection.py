from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base


class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    asset_definition_id = Column(
        Integer, ForeignKey("asset_definitions.id"), nullable=False
    )
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    coord_top_lat = Column(Float)
    coord_top_lng = Column(Float)
    coord_bot_lat = Column(Float)
    coord_bot_lng = Column(Float)

    media = relationship("Media", back_populates="detections")
    asset_definition = relationship("AssetDefinition", back_populates="detections")
    answers = relationship("DetectionAnswer", back_populates="detection")
