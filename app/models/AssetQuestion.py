from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

from app.models.base import Base


class AssetQuestion(Base):
    __tablename__ = "asset_questions"
    id = Column(Integer, primary_key=True)
    asset_definition_id = Column(
        Integer, ForeignKey("asset_definitions.id"), nullable=False
    )
    question_text = Column(Text, nullable=False)

    asset = relationship("AssetDefinition", back_populates="questions")
