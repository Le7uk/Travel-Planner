from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectStatus(str):
    ACTIVE = "active"
    COMPLETED = "completed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    places = relationship(
        "Place", back_populates="project", cascade="all, delete-orphan"
    )
