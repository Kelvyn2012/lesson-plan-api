"""Tests for authentication endpoints."""

import pytest


def test_register_user(client):
    """Test user registration."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
        "full_name": "New User"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email fails."""
    user_data = {
        "email": test_user["user_data"]["email"],
        "username": "differentuser",
        "password": "password123"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username fails."""
    user_data = {
        "email": "different@example.com",
        "username": test_user["user_data"]["username"],
        "password": "password123"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Test successful login."""
    login_data = {
        "username": test_user["user_data"]["username"],
        "password": test_user["user_data"]["password"]
    }

    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password fails."""
    login_data = {
        "username": test_user["user_data"]["username"],
        "password": "wrongpassword"
    }

    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with nonexistent user fails."""
    login_data = {
        "username": "nonexistent",
        "password": "password123"
    }

    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
