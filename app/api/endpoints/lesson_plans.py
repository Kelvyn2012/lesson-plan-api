"""Lesson plan management endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.lesson_plan import LessonPlan, Tag, GradeLevel, DifficultyLevel
from app.schemas.lesson_plan import (
    LessonPlan as LessonPlanSchema,
    LessonPlanCreate,
    LessonPlanUpdate
)

router = APIRouter()


@router.post("/", response_model=LessonPlanSchema, status_code=status.HTTP_201_CREATED)
def create_lesson_plan(
    lesson_plan_in: LessonPlanCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new lesson plan."""
    # Create lesson plan
    lesson_plan_data = lesson_plan_in.model_dump(exclude={"tag_ids"})
    db_lesson_plan = LessonPlan(**lesson_plan_data, owner_id=current_user.id)

    # Add tags if provided
    if lesson_plan_in.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(lesson_plan_in.tag_ids)).all()
        db_lesson_plan.tags = tags

    db.add(db_lesson_plan)
    db.commit()
    db.refresh(db_lesson_plan)

    return db_lesson_plan


@router.get("/", response_model=List[LessonPlanSchema])
def get_lesson_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    subject: Optional[str] = None,
    grade_level: Optional[GradeLevel] = None,
    difficulty: Optional[DifficultyLevel] = None,
    search: Optional[str] = None,
    tag_ids: Optional[str] = Query(None, description="Comma-separated tag IDs"),
    db: Session = Depends(get_db)
):
    """
    Get lesson plans with filtering and search.

    - **subject**: Filter by subject
    - **grade_level**: Filter by grade level
    - **difficulty**: Filter by difficulty level
    - **search**: Search in title, subject, and procedure
    - **tag_ids**: Filter by tag IDs (comma-separated, e.g., "1,2,3")
    """
    query = db.query(LessonPlan)

    # Apply filters
    if subject:
        query = query.filter(LessonPlan.subject.ilike(f"%{subject}%"))

    if grade_level:
        query = query.filter(LessonPlan.grade_level == grade_level)

    if difficulty:
        query = query.filter(LessonPlan.difficulty == difficulty)

    # Search
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (LessonPlan.title.ilike(search_filter)) |
            (LessonPlan.subject.ilike(search_filter)) |
            (LessonPlan.procedure.ilike(search_filter))
        )

    # Filter by tags
    if tag_ids:
        try:
            tag_id_list = [int(tid.strip()) for tid in tag_ids.split(",")]
            query = query.join(LessonPlan.tags).filter(Tag.id.in_(tag_id_list))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid tag_ids format"
            )

    # Order by most recent
    query = query.order_by(LessonPlan.created_at.desc())

    lesson_plans = query.offset(skip).limit(limit).all()
    return lesson_plans


@router.get("/my", response_model=List[LessonPlanSchema])
def get_my_lesson_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's lesson plans."""
    lesson_plans = (
        db.query(LessonPlan)
        .filter(LessonPlan.owner_id == current_user.id)
        .order_by(LessonPlan.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return lesson_plans


@router.get("/{lesson_plan_id}", response_model=LessonPlanSchema)
def get_lesson_plan(lesson_plan_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson plan by ID."""
    lesson_plan = db.query(LessonPlan).filter(LessonPlan.id == lesson_plan_id).first()
    if not lesson_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson plan not found"
        )
    return lesson_plan


@router.put("/{lesson_plan_id}", response_model=LessonPlanSchema)
def update_lesson_plan(
    lesson_plan_id: int,
    lesson_plan_update: LessonPlanUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a lesson plan (only owner can update)."""
    lesson_plan = db.query(LessonPlan).filter(LessonPlan.id == lesson_plan_id).first()

    if not lesson_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson plan not found"
        )

    if lesson_plan.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this lesson plan"
        )

    # Update fields
    update_data = lesson_plan_update.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for field, value in update_data.items():
        setattr(lesson_plan, field, value)

    # Update tags if provided
    if lesson_plan_update.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(lesson_plan_update.tag_ids)).all()
        lesson_plan.tags = tags

    # Increment version
    lesson_plan.version += 1

    db.commit()
    db.refresh(lesson_plan)

    return lesson_plan


@router.delete("/{lesson_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson_plan(
    lesson_plan_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a lesson plan (only owner can delete)."""
    lesson_plan = db.query(LessonPlan).filter(LessonPlan.id == lesson_plan_id).first()

    if not lesson_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson plan not found"
        )

    if lesson_plan.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this lesson plan"
        )

    db.delete(lesson_plan)
    db.commit()

    return None
