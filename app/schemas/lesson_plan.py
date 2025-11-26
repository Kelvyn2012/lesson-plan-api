"""Lesson plan schemas for API validation."""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.lesson_plan import GradeLevel, DifficultyLevel


class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None


class TagCreate(TagBase):
    """Schema for creating a tag."""
    pass


class Tag(TagBase):
    """Public tag schema."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LessonPlanBase(BaseModel):
    """Base lesson plan schema."""
    title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=1, max_length=100)
    grade_level: GradeLevel
    duration_minutes: Optional[int] = Field(None, gt=0, le=480)
    difficulty: Optional[DifficultyLevel] = None
    objectives: Optional[str] = None
    materials: Optional[str] = None
    procedure: str = Field(..., min_length=10)
    assessment: Optional[str] = None
    notes: Optional[str] = None


class LessonPlanCreate(LessonPlanBase):
    """Schema for creating a lesson plan."""
    tag_ids: Optional[List[int]] = []


class LessonPlanUpdate(BaseModel):
    """Schema for updating a lesson plan."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    grade_level: Optional[GradeLevel] = None
    duration_minutes: Optional[int] = Field(None, gt=0, le=480)
    difficulty: Optional[DifficultyLevel] = None
    objectives: Optional[str] = None
    materials: Optional[str] = None
    procedure: Optional[str] = Field(None, min_length=10)
    assessment: Optional[str] = None
    notes: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class LessonPlanInDB(LessonPlanBase):
    """Schema for lesson plan in database."""
    id: int
    version: int
    owner_id: int
    tags: List[Tag] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LessonPlan(LessonPlanInDB):
    """Public lesson plan schema."""
    pass
