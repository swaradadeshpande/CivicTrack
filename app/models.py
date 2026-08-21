import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class IssueStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class IssueCategory(str, enum.Enum):
    pothole = "pothole"
    streetlight = "streetlight"
    garbage = "garbage"
    water_leak = "water_leak"
    sewage = "sewage"
    road_damage = "road_damage"
    other = "other"


class UserRole(str, enum.Enum):
    citizen = "citizen"
    official = "official"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.citizen, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    issues = relationship("Issue", back_populates="reporter")


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(IssueCategory), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(Enum(IssueStatus), default=IssueStatus.open, nullable=False, index=True)

    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reporter = relationship("User", back_populates="issues")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
