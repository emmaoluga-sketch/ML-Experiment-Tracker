"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class ExperimentCreate(BaseModel):
    """Schema for creating an experiment."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    artifacts: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ExperimentUpdate(BaseModel):
    """Schema for updating an experiment."""
    name: Optional[str] = None
    description: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    artifacts: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ExperimentResponse(BaseModel):
    """Schema for experiment response."""
    id: int
    name: str
    description: Optional[str]
    params: Optional[Dict[str, Any]]
    metrics: Optional[Dict[str, Any]]
    tags: Optional[List[str]]
    artifacts: Optional[Dict[str, Any]]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
