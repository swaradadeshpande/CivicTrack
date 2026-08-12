import enum

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class IssueStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Kept as a plain string for now — this becomes a proper foreign key
    # to a `categories` table in Phase 6 (relational design). Indexed
    # because we'll filter on it constantly once the feed grows.
    category = Column(String(50), nullable=False, index=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    status = Column(Enum(IssueStatus), default=IssueStatus.open, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
