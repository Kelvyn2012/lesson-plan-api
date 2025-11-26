# Quick Start Guide

This guide will get you up and running with the Lesson Plan API in under 10 minutes.

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9 or higher (`python --version`)
- [ ] PostgreSQL 12+ installed (`psql --version`)
- [ ] pip package manager (`pip --version`)
- [ ] Git (optional, for cloning)

## Step 1: Database Setup (2 minutes)

### Create Database

```bash
# Using psql command
createdb lessonplan_db

# Or using psql shell
psql postgres
CREATE DATABASE lessonplan_db;
\q
```

### Verify Database

```bash
psql -l | grep lessonplan_db
```

You should see your database in the list.

## Step 2: Project Setup (3 minutes)

### Clone/Extract Project

```bash
# If using git
git clone <your-repo-url>
cd lesson-plan-api

# Or extract the ZIP file and navigate to the directory
```

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Install Dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, SQLAlchemy, PostgreSQL driver, and all dependencies.

## Step 3: Configuration (1 minute)

### Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file
# Update these values:
```

Edit `.env` with your settings:

```env
# If using default PostgreSQL setup:
DATABASE_URL=postgresql://postgres:yourpassword@localhost/lessonplan_db

# Generate a secure secret key (use this command):
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-generated-secret-key-here

# Keep these defaults:
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Generate Secret Key

```bash
# Run this command to generate a secure secret key:
python -c "import secrets; print(secrets.token_hex(32))"

# Copy the output and paste it as SECRET_KEY in .env
```

## Step 4: Run the Application (1 minute)

### Start the Server

```bash
uvicorn app.main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify It's Running

Open your browser and visit:
- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 5: Test the API (3 minutes)

### Option A: Using the Interactive Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on "POST /api/v1/auth/register"
3. Click "Try it out"
4. Enter this JSON:

```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "testpass123",
  "full_name": "Test User"
}
```

5. Click "Execute"
6. You should get a 201 response with your user data!

### Option B: Using cURL

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Login and Get Token

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

Copy the `access_token` from the response.

### Create a Lesson Plan

```bash
# Replace YOUR_TOKEN with the token from login
curl -X POST "http://localhost:8000/api/v1/lesson-plans/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "subject": "Computer Science",
    "grade_level": "high_school",
    "duration_minutes": 60,
    "difficulty": "beginner",
    "procedure": "1. Intro to Python\n2. Variables\n3. Data types\n4. Practice"
  }'
```

## Step 6: Run Tests (Optional)

```bash
# Run all tests
pytest

# Run with output
pytest -v

# Run with coverage
pytest --cov=app
```

## Common Issues

### Issue: "createdb: command not found"

**Solution**: PostgreSQL bin directory not in PATH.

```bash
# On macOS with Homebrew:
export PATH="/usr/local/opt/postgresql/bin:$PATH"

# Or use full path:
/usr/local/bin/createdb lessonplan_db
```

### Issue: "FATAL: database does not exist"

**Solution**: Create the database first (see Step 1).

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Make sure virtual environment is activated and dependencies installed:

```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Install dependencies
```

### Issue: "Connection refused" when starting server

**Solution**: Make sure PostgreSQL is running:

```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL
# On macOS with Homebrew:
brew services start postgresql

# On Linux with systemd:
sudo systemctl start postgresql
```

### Issue: "Secret key not found" or authentication errors

**Solution**: Make sure `.env` file exists and has valid SECRET_KEY:

```bash
# Generate new secret
python -c "import secrets; print(secrets.token_hex(32))"

# Add to .env file
echo "SECRET_KEY=your-generated-key" >> .env
```

## Next Steps

Now that your API is running:

1. **Explore the API**: Visit http://localhost:8000/docs and try all endpoints
2. **Read the docs**: Check out [API_REFERENCE.md](API_REFERENCE.md) for detailed endpoint documentation
3. **Understand the code**: Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. **Customize**: Modify the code to add your own features

## Need Help?

- Check the [README.md](../README.md) for detailed documentation
- Review test files in `tests/` for usage examples
- Open an issue if you encounter problems

## Summary

You now have:
- ✅ Database running
- ✅ API server running
- ✅ User registered
- ✅ Authentication working
- ✅ Lesson plan created

**Total time**: ~10 minutes

Congratulations! Your Lesson Plan API is fully operational.
