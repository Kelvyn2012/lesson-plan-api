"""Lesson plan and tag database models."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class GradeLevel(str, enum.Enum):
    """Grade level enumeration."""
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    PROFESSIONAL = "professional"


class DifficultyLevel(str, enum.Enum):
    """Difficulty level enumeration."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# Association table for many-to-many relationship between lesson plans and tags
lesson_plan_tags = Table(
    "lesson_plan_tags",
    Base.metadata,
    Column("lesson_plan_id", Integer, ForeignKey("lesson_plans.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)


class LessonPlan(Base):
    """Lesson plan model."""

    __tablename__ = "lesson_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False, index=True)
    grade_level = Column(Enum(GradeLevel), nullable=False)
    duration_minutes = Column(Integer)
    difficulty = Column(Enum(DifficultyLevel))

    # Content fields
    objectives = Column(Text)
    materials = Column(Text)
    procedure = Column(Text, nullable=False)
    assessment = Column(Text)
    notes = Column(Text)

    # Version control
    version = Column(Integer, default=1)

    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="lesson_plans")

    tags = relationship("Tag", secondary=lesson_plan_tags, back_populates="lesson_plans")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Tag(Base):
    """Tag model for categorizing lesson plans."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)

    # Relationships
    lesson_plans = relationship("LessonPlan", secondary=lesson_plan_tags, back_populates="tags")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
