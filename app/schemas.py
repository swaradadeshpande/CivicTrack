from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .models import IssueCategory, IssueStatus, UserRole


def _clean_title(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    v = v.strip()
    if not v:
        raise ValueError("title cannot be blank or just whitespace")
    return v


def _clean_description(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    v = v.strip()
    return v or None


class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    category: IssueCategory
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        return _clean_title(v)

    @field_validator("description")
    @classmethod
    def description_cleaned(cls, v: Optional[str]) -> Optional[str]:
        return _clean_description(v)


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    category: Optional[IssueCategory] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    status: Optional[IssueStatus] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        return _clean_title(v)

    @field_validator("description")
    @classmethod
    def description_cleaned(cls, v: Optional[str]) -> Optional[str]:
        return _clean_description(v)


class IssueOut(IssueBase):
    id: int
    status: IssueStatus
    reported_by_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.citizen


class UserOut(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
