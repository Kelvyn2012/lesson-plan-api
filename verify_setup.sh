#!/bin/bash

# Lesson Plan API Setup Verification Script
# This script helps verify your development environment is correctly set up

set -e

echo "🔍 Verifying Lesson Plan API Setup..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "1️⃣  Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -ge 3 ] && [ "$python_minor" -ge 9 ]; then
    echo -e "${GREEN}✓ Python $python_version found${NC}"
else
    echo -e "${RED}✗ Python 3.9+ required (found $python_version)${NC}"
    exit 1
fi
echo ""

# Check PostgreSQL
echo "2️⃣  Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    pg_version=$(psql --version | awk '{print $3}')
    echo -e "${GREEN}✓ PostgreSQL $pg_version found${NC}"
else
    echo -e "${YELLOW}⚠ PostgreSQL not found or not in PATH${NC}"
    echo "  Install PostgreSQL 12+ to continue"
fi
echo ""

# Check virtual environment
echo "3️⃣  Checking virtual environment..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment found${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment not found${NC}"
    echo "  Run: python -m venv venv"
fi
echo ""

# Check if venv is activated
echo "4️⃣  Checking if virtual environment is activated..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}✓ Virtual environment activated: $VIRTUAL_ENV${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment not activated${NC}"
    echo "  Run: source venv/bin/activate"
fi
echo ""

# Check requirements installed
echo "5️⃣  Checking dependencies..."
if python -c "import fastapi" 2>/dev/null; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Dependencies not installed${NC}"
    echo "  Run: pip install -r requirements.txt"
fi
echo ""

# Check .env file
echo "6️⃣  Checking environment configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo "  Run: cp .env.example .env"
    echo "  Then edit .env with your database credentials"
fi
echo ""

# Check database connection
echo "7️⃣  Checking database..."
if [ -f ".env" ]; then
    db_url=$(grep DATABASE_URL .env | cut -d '=' -f2)
    if [ -n "$db_url" ]; then
        echo -e "${GREEN}✓ Database URL configured${NC}"

        # Try to connect to database
        db_name=$(echo $db_url | awk -F'/' '{print $NF}')
        if psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$db_name"; then
            echo -e "${GREEN}✓ Database '$db_name' exists${NC}"
        else
            echo -e "${YELLOW}⚠ Database '$db_name' not found${NC}"
            echo "  Run: createdb $db_name"
        fi
    else
        echo -e "${YELLOW}⚠ DATABASE_URL not configured in .env${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Cannot check database (no .env file)${NC}"
fi
echo ""

# Check project structure
echo "8️⃣  Checking project structure..."
required_dirs=("app" "tests" "docs")
all_dirs_exist=true

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ $dir/ directory exists${NC}"
    else
        echo -e "${RED}✗ $dir/ directory missing${NC}"
        all_dirs_exist=false
    fi
done
echo ""

# Summary
echo "📊 Setup Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$python_major" -ge 3 ] && [ "$python_minor" -ge 9 ] && \
   [ -d "venv" ] && [ -f ".env" ] && [ "$all_dirs_exist" = true ]; then
    echo -e "${GREEN}✓ Your environment is ready!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Make sure PostgreSQL is running"
    echo "  2. Activate virtual environment: source venv/bin/activate"
    echo "  3. Run the application: uvicorn app.main:app --reload"
    echo "  4. Visit: http://localhost:8000/docs"
else
    echo -e "${YELLOW}⚠ Some setup steps are incomplete${NC}"
    echo ""
    echo "Please complete the steps marked with ⚠ above"
    echo "See QUICKSTART.md for detailed instructions"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
