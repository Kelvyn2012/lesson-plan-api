"""Tests for tag endpoints."""

import pytest


def test_create_tag(client, test_user):
    """Test creating a tag."""
    tag_data = {
        "name": "STEM",
        "description": "Science, Technology, Engineering, and Mathematics"
    }

    response = client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == tag_data["name"]
    assert data["description"] == tag_data["description"]


def test_create_duplicate_tag(client, test_user):
    """Test creating duplicate tag fails."""
    tag_data = {
        "name": "STEM",
        "description": "Science, Technology, Engineering, and Mathematics"
    }

    # Create first tag
    client.post("/api/v1/tags/", json=tag_data, headers=test_user["headers"])

    # Try to create duplicate
    response = client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 400


def test_get_tags(client, test_user):
    """Test getting all tags."""
    tag_data = {"name": "STEM"}
    client.post("/api/v1/tags/", json=tag_data, headers=test_user["headers"])

    response = client.get("/api/v1/tags/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0


def test_get_tag_by_id(client, test_user):
    """Test getting a specific tag by ID."""
    tag_data = {"name": "STEM"}
    create_response = client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=test_user["headers"]
    )
    tag_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == tag_id
    assert data["name"] == tag_data["name"]


def test_lesson_plan_with_tags(client, test_user, test_lesson_plan_data):
    """Test creating lesson plan with tags."""
    # Create tags
    tag1 = client.post(
        "/api/v1/tags/",
        json={"name": "Programming"},
        headers=test_user["headers"]
    ).json()

    tag2 = client.post(
        "/api/v1/tags/",
        json={"name": "Beginner"},
        headers=test_user["headers"]
    ).json()

    # Create lesson plan with tags
    lesson_data = {**test_lesson_plan_data, "tag_ids": [tag1["id"], tag2["id"]]}

    response = client.post(
        "/api/v1/lesson-plans/",
        json=lesson_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 201

    data = response.json()
    assert len(data["tags"]) == 2
    tag_names = [tag["name"] for tag in data["tags"]]
    assert "Programming" in tag_names
    assert "Beginner" in tag_names


def test_delete_tag(client, test_user):
    """Test deleting a tag."""
    tag_data = {"name": "STEM"}
    create_response = client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=test_user["headers"]
    )
    tag_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/tags/{tag_id}", headers=test_user["headers"])
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 404
