from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def create_issue(db: Session, issue: schemas.IssueCreate) -> models.Issue:
    db_issue = models.Issue(**issue.model_dump())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)  # pulls back DB-generated fields: id, created_at, etc.
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

    # exclude_unset=True: only fields the client actually sent get applied —
    # a field left out of the request body won't overwrite existing data with None.
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
