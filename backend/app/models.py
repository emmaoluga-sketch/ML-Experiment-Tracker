"""SQLAlchemy models for experiments."""

from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from datetime import datetime
from .database import Base


class Experiment(Base):
    """Experiment model for storing ML experiment data."""
    
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    params = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    artifacts = Column(JSON, nullable=True)  # Paths or metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Experiment(id={self.id}, name='{self.name}', created_at={self.created_at})>"
