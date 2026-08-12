from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .models import IssueStatus


class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class IssueCreate(IssueBase):
    """Shape required to create a new issue — no id/status/timestamps yet."""

    pass


class IssueUpdate(BaseModel):
    """
    Every field optional — this is used for partial updates (PUT here,
    though a stricter API might reserve PATCH for this and require
    every field on PUT; we're keeping PUT flexible for now).
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    status: Optional[IssueStatus] = None


class IssueOut(IssueBase):
    id: int
    status: IssueStatus
    created_at: datetime
    updated_at: datetime

    # Lets Pydantic read data straight off a SQLAlchemy model instance
    # (attribute access) instead of requiring a dict.
    model_config = ConfigDict(from_attributes=True)
