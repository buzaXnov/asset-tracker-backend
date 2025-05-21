from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base


class AssetDefinition(Base):
    __tablename__ = "asset_definitions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String, nullable=False)

    user = relationship("User", back_populates="assets")
    questions = relationship(
        "AssetQuestion", back_populates="asset", cascade="all, delete-orphan"
    )
    detections = relationship(
        "Detection", back_populates="asset_definition", cascade="all, delete-orphan"
    )
