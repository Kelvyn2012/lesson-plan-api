"""Tests for user endpoints."""

import pytest


def test_get_current_user(client, test_user):
    """Test getting current user information."""
    response = client.get("/api/v1/users/me", headers=test_user["headers"])
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_user["user_data"]["email"]
    assert data["username"] == test_user["user_data"]["username"]


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication fails."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_update_current_user(client, test_user):
    """Test updating current user information."""
    update_data = {
        "full_name": "Updated Name"
    }

    response = client.put(
        "/api/v1/users/me",
        json=update_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 200

    data = response.json()
    assert data["full_name"] == update_data["full_name"]


def test_update_user_password(client, test_user):
    """Test updating user password."""
    update_data = {
        "password": "newpassword123"
    }

    response = client.put(
        "/api/v1/users/me",
        json=update_data,
        headers=test_user["headers"]
    )
    assert response.status_code == 200

    # Try logging in with new password
    login_data = {
        "username": test_user["user_data"]["username"],
        "password": update_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
