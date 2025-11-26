"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.core.security import create_access_token

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """Create a test user and return user data with token."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }

    # Register user
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    # Login to get token
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "user_data": user_data,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }


@pytest.fixture
def test_lesson_plan_data():
    """Sample lesson plan data for testing."""
    return {
        "title": "Introduction to Python Programming",
        "subject": "Computer Science",
        "grade_level": "high_school",
        "duration_minutes": 60,
        "difficulty": "beginner",
        "objectives": "Students will learn basic Python syntax and write their first program.",
        "materials": "Computer with Python installed, text editor",
        "procedure": "1. Introduction to Python\n2. Variables and data types\n3. Hello World program\n4. Practice exercises",
        "assessment": "Students will complete a simple programming exercise.",
        "notes": "Make sure all computers have Python 3.8+ installed."
    }
