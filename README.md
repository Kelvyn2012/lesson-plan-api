# Lesson Plan API

A comprehensive RESTful API for creating, managing, and sharing educational lesson plans. Built with FastAPI, PostgreSQL, and modern Python best practices.

## Overview

This API enables educators to:
- Create and manage lesson plans with rich content
- Organize plans by subject, grade level, and difficulty
- Tag and categorize plans for easy discovery
- Search and filter through lesson plans
- Secure authentication with JWT tokens
- Version control for lesson plan updates

## Features

- **JWT Authentication**: Secure user registration and login
- **CRUD Operations**: Full create, read, update, delete for lesson plans
- **Advanced Search**: Filter by subject, grade level, difficulty, tags
- **Tagging System**: Categorize lesson plans with custom tags
- **Version Control**: Track changes to lesson plans
- **Database Relations**: Proper foreign keys and relationships
- **Input Validation**: Pydantic schemas for data validation
- **Comprehensive Testing**: 15+ test cases with pytest
- **Auto Documentation**: Interactive API docs with Swagger UI

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with passlib for password hashing
- **Validation**: Pydantic v2
- **Testing**: pytest with coverage
- **API Documentation**: OpenAPI/Swagger (auto-generated)

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or pipenv

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd lesson-plan-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create PostgreSQL database:
```bash
createdb lessonplan_db
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

7. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID

### Lesson Plans
- `POST /api/v1/lesson-plans/` - Create lesson plan
- `GET /api/v1/lesson-plans/` - List all lesson plans (with filters)
- `GET /api/v1/lesson-plans/my` - Get current user's lesson plans
- `GET /api/v1/lesson-plans/{id}` - Get specific lesson plan
- `PUT /api/v1/lesson-plans/{id}` - Update lesson plan
- `DELETE /api/v1/lesson-plans/{id}` - Delete lesson plan

### Tags
- `POST /api/v1/tags/` - Create tag
- `GET /api/v1/tags/` - List all tags
- `GET /api/v1/tags/{id}` - Get specific tag
- `DELETE /api/v1/tags/{id}` - Delete tag

## Example Usage

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@example.com",
    "username": "teacher1",
    "password": "securepass123",
    "full_name": "John Teacher"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teacher1&password=securepass123"
```

### 3. Create a Lesson Plan

```bash
curl -X POST "http://localhost:8000/api/v1/lesson-plans/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "subject": "Computer Science",
    "grade_level": "high_school",
    "duration_minutes": 60,
    "difficulty": "beginner",
    "objectives": "Learn Python basics",
    "materials": "Computer, Python 3.9+",
    "procedure": "1. Introduction\n2. Variables\n3. Data types\n4. Practice",
    "assessment": "Programming exercises"
  }'
```

### 4. Search Lesson Plans

```bash
# Search by keyword
curl "http://localhost:8000/api/v1/lesson-plans/?search=Python"

# Filter by subject and grade level
curl "http://localhost:8000/api/v1/lesson-plans/?subject=Computer&grade_level=high_school"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_lesson_plans.py
```

## Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- username (Unique)
- hashed_password
- full_name
- is_active
- is_superuser
- created_at
- updated_at

### Lesson Plans Table
- id (Primary Key)
- title
- subject
- grade_level (Enum: elementary, middle_school, high_school, college, professional)
- duration_minutes
- difficulty (Enum: beginner, intermediate, advanced)
- objectives
- materials
- procedure
- assessment
- notes
- version
- owner_id (Foreign Key to Users)
- created_at
- updated_at

### Tags Table
- id (Primary Key)
- name (Unique)
- description
- created_at

## Project Structure

```
lesson-plan-api/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── lesson_plans.py
│   │   │   ├── tags.py
│   │   │   └── users.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── lesson_plan.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── lesson_plan.py
│   │   ├── token.py
│   │   └── user.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_lesson_plans.py
│   ├── test_tags.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- Database credentials stored in environment variables
- CORS enabled for specified origins only
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM

## Contributing

This is a code sample project for the MLH Fellowship application. However, suggestions and feedback are welcome!

## License

MIT License - See LICENSE file for details

## Author

Built as a code sample demonstrating:
- RESTful API design
- Database modeling and relationships
- Authentication and authorization
- Testing best practices
- Clean code architecture

## Future Enhancements

Potential features for future development:
- File upload for lesson plan attachments
- Lesson plan sharing and collaboration
- Comments and ratings system
- Export to PDF/Word
- Email notifications
- Admin dashboard
- API rate limiting
- Caching layer

## Support

For questions or issues, please open an issue in the GitHub repository.
