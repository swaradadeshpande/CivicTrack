from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas
from .security import hash_password


def create_issue(db: Session, issue: schemas.IssueCreate, reported_by_id: int) -> models.Issue:
    db_issue = models.Issue(**issue.model_dump(), reported_by_id=reported_by_id)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue(db: Session, issue_id: int) -> Optional[models.Issue]:
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def get_issues(db: Session, skip: int = 0, limit: int = 20) -> List[models.Issue]:
    return (
        db.query(models.Issue)
        .order_by(models.Issue.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_issue(
    db: Session, issue_id: int, issue_update: schemas.IssueUpdate
) -> Optional[models.Issue]:
    db_issue = get_issue(db, issue_id)
    if not db_issue:
        return None

    update_data = issue_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_issue, field, value)

    db.commit()
    db.refresh(db_issue)
    return db_issue


def delete_issue(db: Session, issue_id: int) -> bool:
    db_issue = get_issue(db, issue_id)
    if not db_issue:
        return False
    db.delete(db_issue)
    db.commit()
    return True


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
