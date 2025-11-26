"""Tag management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.lesson_plan import Tag
from app.schemas.lesson_plan import Tag as TagSchema, TagCreate

router = APIRouter()


@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: TagCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new tag."""
    # Check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )

    db_tag = Tag(**tag_in.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag


@router.get("/", response_model=List[TagSchema])
def get_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all tags."""
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags


@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a specific tag by ID."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a tag."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )

    db.delete(tag)
    db.commit()

    return None
