from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    external_id = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    artist = Column(String(500), nullable=True)
    image_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    visited = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="places")

    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_project_place"),
    )
