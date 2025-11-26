# Architecture & Design Decisions

This document explains the technical architecture and key design decisions made in the Lesson Plan API.

## Overview

The Lesson Plan API follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │  ← HTTP routing, request/response
├─────────────────────────────────────┤
│       Business Logic Layer          │  ← Authentication, validation
├─────────────────────────────────────┤
│       Data Access Layer (ORM)       │  ← Database operations
├─────────────────────────────────────┤
│         Database (PostgreSQL)        │  ← Data persistence
└─────────────────────────────────────┘
```

## Technology Stack

### Why FastAPI?

**Chosen**: FastAPI 0.104+

**Alternatives Considered**: Flask, Django REST Framework

**Reasons**:
1. **Modern async support**: Built on ASGI (Starlette) for high performance
2. **Automatic documentation**: OpenAPI/Swagger docs generated automatically
3. **Type hints**: Leverages Python 3.9+ type hints for better IDE support
4. **Pydantic integration**: Built-in request/response validation
5. **Developer experience**: Clean syntax, minimal boilerplate

**Trade-offs**:
- Newer framework (less mature than Flask/Django)
- Smaller ecosystem compared to Django
- ✅ Benefits outweigh drawbacks for a modern API

### Why PostgreSQL?

**Chosen**: PostgreSQL 12+

**Alternatives Considered**: SQLite, MySQL, MongoDB

**Reasons**:
1. **Robust relational model**: Perfect for structured data with relationships
2. **ACID compliance**: Data integrity for educational content
3. **Advanced features**: Full-text search, JSON support, constraints
4. **Production-ready**: Industry standard for web applications
5. **Open source**: No licensing costs

**Trade-offs**:
- Requires separate installation (vs SQLite's embedded approach)
- ✅ Worth it for production-quality features

### Why SQLAlchemy?

**Chosen**: SQLAlchemy 2.0 ORM

**Alternatives Considered**: Raw SQL, Django ORM, Tortoise ORM

**Reasons**:
1. **Database abstraction**: Switch databases without code changes
2. **SQL injection protection**: Parameterized queries by default
3. **Relationship handling**: Easy foreign keys and joins
4. **Migration support**: Works with Alembic for schema changes
5. **Mature and stable**: Battle-tested in production

### Why JWT for Authentication?

**Chosen**: JWT (JSON Web Tokens) with python-jose

**Alternatives Considered**: Session-based auth, OAuth2

**Reasons**:
1. **Stateless**: No server-side session storage needed
2. **Scalable**: Works across multiple servers/microservices
3. **Mobile-friendly**: Perfect for mobile apps and SPAs
4. **Industry standard**: Widely supported and understood
5. **Self-contained**: Token includes user identity

**Implementation**:
- HS256 algorithm (symmetric signing)
- 30-minute expiration (configurable)
- bcrypt for password hashing (industry standard)

## Project Structure

```
app/
├── api/                    # API layer
│   ├── endpoints/          # Route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── users.py        # User management
│   │   ├── lesson_plans.py # Lesson plan CRUD
│   │   └── tags.py         # Tag management
│   └── dependencies.py     # Shared dependencies (auth, db)
│
├── core/                   # Core configuration
│   ├── config.py           # Settings (from env vars)
│   └── security.py         # Password hashing, JWT
│
├── db/                     # Database layer
│   └── database.py         # SQLAlchemy setup, session
│
├── models/                 # ORM models (database schema)
│   ├── user.py             # User table
│   └── lesson_plan.py      # LessonPlan, Tag tables
│
├── schemas/                # Pydantic schemas (validation)
│   ├── user.py             # User request/response models
│   ├── lesson_plan.py      # LessonPlan schemas
│   └── token.py            # JWT token schemas
│
└── main.py                 # Application entry point
```

### Layer Responsibilities

**API Layer** ([app/api/](../app/api/)):
- HTTP routing and request handling
- Response formatting
- Authentication checks (via dependencies)
- Calls data layer for business logic

**Core Layer** ([app/core/](../app/core/)):
- Configuration management (environment variables)
- Security utilities (password hashing, JWT)
- Shared utilities and constants

**Database Layer** ([app/db/](../app/db/)):
- Database connection and session management
- Transaction handling
- Connection pooling

**Models Layer** ([app/models/](../app/models/)):
- ORM models (SQLAlchemy)
- Database schema definition
- Relationships and constraints

**Schemas Layer** ([app/schemas/](../app/schemas/)):
- Request validation (Pydantic)
- Response serialization
- Type checking and conversion

## Database Design

### Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ username (UNQ)  │
│ hashed_password │
│ full_name       │
│ is_active       │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐       ┌──────────────────┐
│  Lesson Plans   │  N:M  │      Tags        │
├─────────────────┤◄─────►├──────────────────┤
│ id (PK)         │       │ id (PK)          │
│ title           │       │ name (UNIQUE)    │
│ subject         │       │ description      │
│ grade_level     │       │ created_at       │
│ duration_mins   │       └──────────────────┘
│ difficulty      │
│ objectives      │
│ materials       │
│ procedure       │
│ assessment      │
│ notes           │
│ version         │
│ owner_id (FK)   │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Key Design Decisions

**1. Separate Users from Lesson Plans**
- **Why**: Users can create multiple lesson plans
- **Benefit**: Track ownership, enable user-specific queries
- **Relationship**: One-to-Many (User → Lesson Plans)

**2. Many-to-Many Tags**
- **Why**: Lesson plans can have multiple tags, tags apply to multiple plans
- **Implementation**: Junction table `lesson_plan_tags`
- **Benefit**: Flexible categorization without duplication

**3. Version Field**
- **Why**: Track lesson plan changes over time
- **Benefit**: See revision history, enable rollback (future)
- **Alternative**: Could use separate versions table (more complex)

**4. Enum Types for Grade Level & Difficulty**
- **Why**: Constrain values, prevent invalid data
- **Benefit**: Database-level validation, easier querying
- **Values**: Predefined lists (e.g., elementary, middle_school, high_school)

**5. Timestamps (created_at, updated_at)**
- **Why**: Audit trail, sorting by recency
- **Implementation**: SQLAlchemy `func.now()` for automatic timestamps
- **Benefit**: No manual timestamp management needed

## Authentication Flow

```
┌──────────┐                           ┌──────────┐
│  Client  │                           │   API    │
└────┬─────┘                           └────┬─────┘
     │                                      │
     │  POST /auth/register                 │
     │  {email, username, password}         │
     ├─────────────────────────────────────►│
     │                                      │
     │       Hash password (bcrypt)         │
     │       Create user in DB              │
     │                                      │
     │◄─────────────────────────────────────┤
     │  201 Created {user data}             │
     │                                      │
     │  POST /auth/login                    │
     │  {username, password}                │
     ├─────────────────────────────────────►│
     │                                      │
     │       Verify password hash           │
     │       Generate JWT token             │
     │                                      │
     │◄─────────────────────────────────────┤
     │  200 OK {access_token}               │
     │                                      │
     │  GET /lesson-plans/my                │
     │  Authorization: Bearer TOKEN         │
     ├─────────────────────────────────────►│
     │                                      │
     │       Decode & validate JWT          │
     │       Extract user from token        │
     │       Query user's lesson plans      │
     │                                      │
     │◄─────────────────────────────────────┤
     │  200 OK [lesson plans...]            │
     │                                      │
```

### Security Measures

1. **Password Hashing**: bcrypt with automatic salt
2. **JWT Expiration**: 30-minute default (configurable)
3. **Token Validation**: Signature verification on every request
4. **HTTPS Only**: (Production deployment requirement)
5. **CORS Protection**: Whitelist allowed origins
6. **SQL Injection**: Prevented by SQLAlchemy parameterization
7. **Input Validation**: Pydantic schemas validate all inputs

## API Design Principles

### RESTful Design

- **Resources**: Users, Lesson Plans, Tags
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: Proper use of 200, 201, 204, 400, 401, 403, 404
- **JSON**: All requests/responses use JSON

### Endpoint Patterns

```
/api/v1/                        # Version prefix
  /auth/register                # Noun + action
  /auth/login
  /users/me                     # Current user resource
  /users/{id}                   # Specific user
  /lesson-plans/                # Plural resource names
  /lesson-plans/{id}            # Specific resource
  /lesson-plans/my              # User-specific collection
  /tags/                        # Separate resource
```

### Filtering & Search

**Query Parameters for GET /lesson-plans/**:
- `subject`: Partial match on subject field
- `grade_level`: Exact match on enum
- `difficulty`: Exact match on enum
- `search`: Full-text search across title, subject, procedure
- `tag_ids`: Filter by tags (comma-separated)
- `skip`, `limit`: Pagination

**Why Query Parameters?**
- RESTful convention for filtering
- Easy to use and understand
- Works with browser URLs and curl
- Allows multiple filters simultaneously

## Validation Strategy

### Two-Layer Validation

**1. Pydantic Schemas** (Request validation):
- Type checking (email, int, string)
- Field requirements (required vs optional)
- String length limits
- Number ranges
- Custom validators

**2. Database Constraints** (Data integrity):
- Unique constraints (email, username)
- Foreign keys
- NOT NULL constraints
- Enum types

**Why Both?**
- Pydantic: Fast feedback, clear error messages
- Database: Last line of defense, data integrity

## Error Handling

### HTTP Status Code Strategy

- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation errors, duplicate data
- `401 Unauthorized`: Missing/invalid authentication
- `403 Forbidden`: Valid auth, but not allowed (ownership)
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Invalid data format

### Error Response Format

```json
{
  "detail": "Human-readable error message"
}
```

**Consistent Format**: All errors follow same structure

## Testing Strategy

### Test Pyramid

```
        ┌────────┐
        │  E2E   │  ← Few (future)
        ├────────┤
        │  API   │  ← Most tests here
        │  Tests │
        ├────────┤
        │  Unit  │  ← Some (security, utilities)
        └────────┘
```

### Current Test Coverage

- **Authentication**: 6 tests (register, login, errors)
- **Users**: 3 tests (get, update, password change)
- **Lesson Plans**: 9 tests (CRUD, search, filter, permissions)
- **Tags**: 5 tests (CRUD, relationships)

**Total**: 23 test cases

### Testing Tools

- **pytest**: Test framework
- **TestClient**: FastAPI's test client (simulates HTTP)
- **SQLite**: In-memory test database (fast)
- **Fixtures**: Reusable test data (conftest.py)

## Performance Considerations

### Database Optimization

1. **Indexes**: On email, username, subject, grade_level
2. **Connection Pooling**: SQLAlchemy's built-in pooling
3. **Lazy Loading**: Relationships loaded on demand
4. **Query Optimization**: Use `.filter()` instead of loading all

### Future Optimizations

- **Caching**: Redis for frequently accessed data
- **Pagination**: Already implemented (skip/limit)
- **Database Read Replicas**: For high read traffic
- **CDN**: For static assets

## Scalability

### Current Architecture Supports

- **Horizontal Scaling**: Stateless (JWT), can run multiple instances
- **Load Balancing**: No session affinity needed
- **Microservices**: Clear layer separation enables splitting
- **Database Scaling**: PostgreSQL supports replication

### Limitations

- **File Storage**: Not implemented (use S3/cloud storage)
- **Background Jobs**: No task queue (use Celery if needed)
- **Real-time**: No WebSockets (add if needed)

## Deployment Considerations

### Environment Variables

All configuration via `.env`:
- Database URL
- Secret key
- Token expiration
- CORS origins

**Why?**
- 12-factor app principle
- Easy per-environment config
- Secrets not in code

### Production Checklist

- [ ] Use strong SECRET_KEY (32+ random bytes)
- [ ] Enable HTTPS only
- [ ] Set restrictive CORS origins
- [ ] Use production database (not SQLite)
- [ ] Enable database backups
- [ ] Set up monitoring/logging
- [ ] Use environment variables for all secrets
- [ ] Enable database connection pooling
- [ ] Set up reverse proxy (nginx)

## Future Enhancements

### Potential Additions

1. **File Uploads**: S3 integration for lesson plan attachments
2. **Search**: Elasticsearch for advanced full-text search
3. **Caching**: Redis for performance
4. **Rate Limiting**: Prevent abuse
5. **Email**: User notifications, password reset
6. **WebSockets**: Real-time collaboration
7. **Admin Panel**: Moderation tools
8. **Export**: PDF/Word generation

### Why Not Included Now?

- **Scope**: Keep code sample focused and understandable
- **Complexity**: Additional dependencies and setup
- **Demonstrate Core**: Show fundamental skills first

## Lessons Learned

### What Worked Well

1. **FastAPI**: Excellent developer experience
2. **Pydantic**: Validation with minimal code
3. **SQLAlchemy**: Powerful and flexible ORM
4. **JWT**: Simple stateless authentication
5. **Testing**: Comprehensive tests gave confidence

### What Could Be Improved

1. **Async**: Could use async SQLAlchemy for better performance
2. **Service Layer**: Could add explicit service classes (currently logic in endpoints)
3. **Repository Pattern**: Could abstract database access further
4. **Error Handling**: Could use custom exception classes

**Trade-off**: Current approach prioritizes clarity and simplicity for a code sample.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [RESTful API Design](https://restfulapi.net/)
- [12-Factor App](https://12factor.net/)
