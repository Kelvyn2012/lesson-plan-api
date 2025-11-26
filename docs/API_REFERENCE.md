# API Reference

Complete documentation for all API endpoints.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require authentication using JWT Bearer tokens.

### Getting a Token

1. Register or login
2. Include token in `Authorization` header:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint**: `POST /auth/register`

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe"  // Optional
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `400`: Email already registered or username taken
- `422`: Validation error (e.g., password too short)

---

### Login

Authenticate and receive an access token.

**Endpoint**: `POST /auth/login`

**Authentication**: Not required

**Request Body** (form-urlencoded):
```
username=johndoe
password=securepassword123
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- `401`: Incorrect username or password
- `400`: Inactive user

---

## User Endpoints

### Get Current User

Get information about the authenticated user.

**Endpoint**: `GET /users/me`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Current User

Update authenticated user's information.

**Endpoint**: `PUT /users/me`

**Authentication**: Required

**Request Body** (all fields optional):
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name",
  "password": "newpassword123"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Errors**:
- `400`: Username or email already taken
- `401`: Not authenticated

---

### Get User by ID

Get public information about any user.

**Endpoint**: `GET /users/{user_id}`

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `404`: User not found

---

## Lesson Plan Endpoints

### Create Lesson Plan

Create a new lesson plan.

**Endpoint**: `POST /lesson-plans/`

**Authentication**: Required

**Request Body**:
```json
{
  "title": "Introduction to Python Programming",
  "subject": "Computer Science",
  "grade_level": "high_school",  // elementary, middle_school, high_school, college, professional
  "duration_minutes": 60,  // Optional
  "difficulty": "beginner",  // Optional: beginner, intermediate, advanced
  "objectives": "Students will learn Python basics",  // Optional
  "materials": "Computer with Python 3.9+",  // Optional
  "procedure": "1. Introduction\n2. Variables\n3. Data types\n4. Practice",
  "assessment": "Programming exercises",  // Optional
  "notes": "Ensure all computers have Python installed",  // Optional
  "tag_ids": [1, 2, 3]  // Optional: array of tag IDs
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Introduction to Python Programming",
  "subject": "Computer Science",
  "grade_level": "high_school",
  "duration_minutes": 60,
  "difficulty": "beginner",
  "objectives": "Students will learn Python basics",
  "materials": "Computer with Python 3.9+",
  "procedure": "1. Introduction\n2. Variables\n3. Data types\n4. Practice",
  "assessment": "Programming exercises",
  "notes": "Ensure all computers have Python installed",
  "version": 1,
  "owner_id": 1,
  "tags": [
    {"id": 1, "name": "Programming", "description": null, "created_at": "2024-01-15T10:00:00Z"}
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

**Errors**:
- `401`: Not authenticated
- `422`: Validation error

---

### List Lesson Plans

Get all lesson plans with optional filtering.

**Endpoint**: `GET /lesson-plans/`

**Authentication**: Not required

**Query Parameters**:
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=100, max=100): Maximum records to return
- `subject` (string): Filter by subject (partial match)
- `grade_level` (enum): Filter by grade level
- `difficulty` (enum): Filter by difficulty
- `search` (string): Search in title, subject, and procedure
- `tag_ids` (string): Comma-separated tag IDs (e.g., "1,2,3")

**Examples**:
```
GET /lesson-plans/?search=Python
GET /lesson-plans/?subject=Math&grade_level=middle_school
GET /lesson-plans/?difficulty=beginner&tag_ids=1,2
GET /lesson-plans/?skip=10&limit=20
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Introduction to Python Programming",
    "subject": "Computer Science",
    ...
  },
  {
    "id": 2,
    "title": "Advanced Python Concepts",
    ...
  }
]
```

---

### Get My Lesson Plans

Get lesson plans created by the authenticated user.

**Endpoint**: `GET /lesson-plans/my`

**Authentication**: Required

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=100, max=100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "My Lesson Plan",
    ...
  }
]
```

---

### Get Lesson Plan by ID

Get a specific lesson plan.

**Endpoint**: `GET /lesson-plans/{lesson_plan_id}`

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Introduction to Python Programming",
  "subject": "Computer Science",
  "grade_level": "high_school",
  ...
}
```

**Errors**:
- `404`: Lesson plan not found

---

### Update Lesson Plan

Update a lesson plan (owner only).

**Endpoint**: `PUT /lesson-plans/{lesson_plan_id}`

**Authentication**: Required (must be owner)

**Request Body** (all fields optional):
```json
{
  "title": "Updated Title",
  "duration_minutes": 90,
  "tag_ids": [1, 3, 5]
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Updated Title",
  "duration_minutes": 90,
  "version": 2,  // Version incremented
  ...
}
```

**Errors**:
- `401`: Not authenticated
- `403`: Not authorized (not the owner)
- `404`: Lesson plan not found

---

### Delete Lesson Plan

Delete a lesson plan (owner only).

**Endpoint**: `DELETE /lesson-plans/{lesson_plan_id}`

**Authentication**: Required (must be owner)

**Response** (204 No Content)

**Errors**:
- `401`: Not authenticated
- `403`: Not authorized (not the owner)
- `404`: Lesson plan not found

---

## Tag Endpoints

### Create Tag

Create a new tag for categorizing lesson plans.

**Endpoint**: `POST /tags/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "STEM",
  "description": "Science, Technology, Engineering, and Mathematics"  // Optional
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "STEM",
  "description": "Science, Technology, Engineering, and Mathematics",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `400`: Tag with this name already exists
- `401`: Not authenticated

---

### List Tags

Get all tags.

**Endpoint**: `GET /tags/`

**Authentication**: Not required

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=100, max=100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "STEM",
    "description": "Science, Technology, Engineering, and Mathematics",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Programming",
    "description": null,
    "created_at": "2024-01-15T10:35:00Z"
  }
]
```

---

### Get Tag by ID

Get a specific tag.

**Endpoint**: `GET /tags/{tag_id}`

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "STEM",
  "description": "Science, Technology, Engineering, and Mathematics",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `404`: Tag not found

---

### Delete Tag

Delete a tag.

**Endpoint**: `DELETE /tags/{tag_id}`

**Authentication**: Required

**Response** (204 No Content)

**Errors**:
- `401`: Not authenticated
- `404`: Tag not found

---

## Data Models

### Grade Levels
- `elementary`
- `middle_school`
- `high_school`
- `college`
- `professional`

### Difficulty Levels
- `beginner`
- `intermediate`
- `advanced`

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request (validation error, duplicate data)
- `401`: Unauthorized (not authenticated)
- `403`: Forbidden (not authorized for this action)
- `404`: Not Found
- `422`: Unprocessable Entity (invalid data format)

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## Pagination

List endpoints support pagination via `skip` and `limit` parameters:

```
GET /lesson-plans/?skip=20&limit=10
```

This returns records 21-30.

---

## CORS

The API allows requests from:
- `http://localhost:3000`
- `http://localhost:8000`

Configure additional origins in `.env` file.
