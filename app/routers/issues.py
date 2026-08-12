from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("/", response_model=schemas.IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    return crud.create_issue(db, issue)


@router.get("/", response_model=List[schemas.IssueOut])
def list_issues(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_issues(db, skip=skip, limit=limit)


@router.get("/{issue_id}", response_model=schemas.IssueOut)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = crud.get_issue(db, issue_id)
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue


@router.put("/{issue_id}", response_model=schemas.IssueOut)
def update_issue(issue_id: int, issue_update: schemas.IssueUpdate, db: Session = Depends(get_db)):
    db_issue = crud.update_issue(db, issue_id, issue_update)
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_issue(db, issue_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Issue not found")
