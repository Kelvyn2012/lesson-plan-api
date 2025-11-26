"""Tests for lesson plan endpoints."""

import pytest


def test_create_lesson_plan(client, test_user, test_lesson_plan_data):
    """Test creating a lesson plan."""
    response = client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == test_lesson_plan_data["title"]
    assert data["subject"] == test_lesson_plan_data["subject"]
    assert data["version"] == 1


def test_create_lesson_plan_unauthorized(client, test_lesson_plan_data):
    """Test creating lesson plan without authentication fails."""
    response = client.post("/api/v1/lesson-plans/", json=test_lesson_plan_data)
    assert response.status_code == 401


def test_get_lesson_plans(client, test_user, test_lesson_plan_data):
    """Test getting all lesson plans."""
    # Create a lesson plan first
    client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )

    response = client.get("/api/v1/lesson-plans/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == test_lesson_plan_data["title"]


def test_get_lesson_plan_by_id(client, test_user, test_lesson_plan_data):
    """Test getting a specific lesson plan by ID."""
    # Create a lesson plan
    create_response = client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )
    lesson_plan_id = create_response.json()["id"]

    response = client.get(f"/api/v1/lesson-plans/{lesson_plan_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == lesson_plan_id
    assert data["title"] == test_lesson_plan_data["title"]


def test_get_my_lesson_plans(client, test_user, test_lesson_plan_data):
    """Test getting current user's lesson plans."""
    # Create a lesson plan
    client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )

    response = client.get("/api/v1/lesson-plans/my", headers=test_user["headers"])
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0


def test_update_lesson_plan(client, test_user, test_lesson_plan_data):
    """Test updating a lesson plan."""
    # Create a lesson plan
    create_response = client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )
    lesson_plan_id = create_response.json()["id"]

    # Update it
    update_data = {
        "title": "Updated Title",
        "duration_minutes": 90
    }

    response = client.put(
        f"/api/v1/lesson-plans/{lesson_plan_id}",
        json=update_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["duration_minutes"] == update_data["duration_minutes"]
    assert data["version"] == 2


def test_update_lesson_plan_unauthorized(client, test_user, test_lesson_plan_data):
    """Test updating lesson plan by non-owner fails."""
    # Create a lesson plan
    create_response = client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )
    lesson_plan_id = create_response.json()["id"]

    # Try to update without authentication
    update_data = {"title": "Hacked Title"}
    response = client.put(f"/api/v1/lesson-plans/{lesson_plan_id}", json=update_data)
    assert response.status_code == 401


def test_delete_lesson_plan(client, test_user, test_lesson_plan_data):
    """Test deleting a lesson plan."""
    # Create a lesson plan
    create_response = client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )
    lesson_plan_id = create_response.json()["id"]

    # Delete it
    response = client.delete(
        f"/api/v1/lesson-plans/{lesson_plan_id}",
        headers=test_user["headers"]
    )
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/v1/lesson-plans/{lesson_plan_id}")
    assert response.status_code == 404


def test_search_lesson_plans(client, test_user, test_lesson_plan_data):
    """Test searching lesson plans."""
    # Create a lesson plan
    client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )

    # Search by keyword
    response = client.get("/api/v1/lesson-plans/?search=Python")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0


def test_filter_lesson_plans_by_subject(client, test_user, test_lesson_plan_data):
    """Test filtering lesson plans by subject."""
    # Create a lesson plan
    client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )

    # Filter by subject
    response = client.get("/api/v1/lesson-plans/?subject=Computer")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert "Computer" in data[0]["subject"]


def test_filter_lesson_plans_by_grade_level(client, test_user, test_lesson_plan_data):
    """Test filtering lesson plans by grade level."""
    # Create a lesson plan
    client.post(
        "/api/v1/lesson-plans/",
        json=test_lesson_plan_data,
        headers=test_user["headers"]
    )

    # Filter by grade level
    response = client.get("/api/v1/lesson-plans/?grade_level=high_school")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert data[0]["grade_level"] == "high_school"
