# MLH Fellowship Submission Checklist

Use this checklist before submitting your code sample to ensure everything is ready.

## Pre-Submission Checklist

### ✅ Code Quality

- [ ] All code files are properly formatted
- [ ] No debugging print statements or commented-out code
- [ ] No hardcoded passwords or secrets in code
- [ ] Consistent naming conventions throughout
- [ ] All imports are used (no unused imports)
- [ ] Type hints used where appropriate

### ✅ Testing

- [ ] All tests pass: `pytest`
- [ ] Test coverage is adequate: `pytest --cov=app`
- [ ] No failing or skipped tests
- [ ] Test database is cleaned up properly

### ✅ Documentation

- [ ] README.md is complete and accurate
- [ ] API_REFERENCE.md covers all endpoints
- [ ] QUICKSTART.md has working setup instructions
- [ ] ARCHITECTURE.md explains design decisions
- [ ] All documentation links work
- [ ] Code comments explain "why" not "what"

### ✅ Configuration

- [ ] .env.example file includes all required variables
- [ ] .gitignore prevents secrets from being committed
- [ ] requirements.txt has all dependencies with versions
- [ ] No absolute paths in code (use relative or env vars)

### ✅ Repository

- [ ] All files are committed to Git
- [ ] .env file is NOT in repository (check .gitignore)
- [ ] Virtual environment (venv/) is NOT in repository
- [ ] Database files (.db, *.sqlite) are NOT in repository
- [ ] Meaningful commit messages
- [ ] No sensitive data in commit history

### ✅ Functionality

- [ ] Server starts without errors: `uvicorn app.main:app --reload`
- [ ] API docs load: http://localhost:8000/docs
- [ ] Can register a new user
- [ ] Can login and get token
- [ ] Can create a lesson plan with authentication
- [ ] Can search and filter lesson plans
- [ ] Can create and use tags
- [ ] All CRUD operations work

### ✅ Personal Touches

- [ ] README has your name and contact info
- [ ] PROJECT_SUMMARY has your personal story
- [ ] Code demonstrates your unique skills
- [ ] Documentation reflects your voice

---

## Verification Steps

### 1. Fresh Environment Test

Test that a new user can set up your project:

```bash
# In a new terminal/directory
git clone <your-repo>
cd lesson-plan-api

# Follow QUICKSTART.md exactly
# Did it work without issues?
```

### 2. Run All Tests

```bash
source venv/bin/activate
pytest -v
```

Expected: All tests pass, no errors.

### 3. Test API Manually

```bash
# Start server
uvicorn app.main:app --reload

# In another terminal, test endpoints:
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Try registration, login, creating lesson plan
# (See QUICKSTART.md for examples)
```

### 4. Check Documentation Links

Open each doc file and verify:
- All internal links work
- Code examples are accurate
- File paths are correct
- No broken references

### 5. Security Review

```bash
# Check for secrets in code
grep -r "password" app/  # Should only find hashing logic
grep -r "SECRET_KEY" app/  # Should only be in config.py reading from env

# Check .env is gitignored
cat .gitignore | grep .env  # Should be listed

# Verify .env not in repo
git ls-files | grep .env  # Should only show .env.example
```

---

## GitHub Repository Checklist

### Repository Setup

- [ ] Repository is public (or accessible to MLH reviewers)
- [ ] Repository name is descriptive (e.g., "lesson-plan-api")
- [ ] Repository has a description
- [ ] Repository has a README.md that renders properly
- [ ] Repository has appropriate license (MIT recommended)

### Repository Content

- [ ] All project files are in the repository
- [ ] .gitignore is working (no secrets, venv, or db files)
- [ ] README.md renders with proper markdown formatting
- [ ] Documentation is in docs/ folder
- [ ] Tests are in tests/ folder

### GitHub Presentation

- [ ] Repository README has badges (optional but nice):
  - Python version
  - License
  - Test status (if using CI/CD)
- [ ] Repository has topics/tags (e.g., "fastapi", "postgresql", "rest-api")
- [ ] Repository has a clear file structure
- [ ] Commit history is clean and professional

---

## Application Form Checklist

### Code Sample URL

- [ ] GitHub repository URL is correct
- [ ] Repository is accessible (public or shared)
- [ ] URL goes directly to repository (not your profile)

### Project Description

Draft your description (keep it under 500 words):

**Template**:
```
Lesson Plan API - A RESTful API for managing educational lesson plans

This project demonstrates:
- Backend development with FastAPI and PostgreSQL
- JWT authentication and authorization
- Database design with SQLAlchemy ORM
- Comprehensive testing with pytest
- Professional documentation

As a teacher trainer, I built this to solve a real problem educators face:
managing and sharing lesson plans efficiently. The API provides:
- User authentication and registration
- Full CRUD operations for lesson plans
- Search and filtering capabilities
- Tag-based categorization
- Version control for updates

Tech stack: Python 3.9+, FastAPI, PostgreSQL, SQLAlchemy, JWT, pytest

The codebase includes 23 test cases, comprehensive API documentation,
and detailed architecture explanations. It's production-ready and
demonstrates best practices in security, testing, and code organization.

Repository includes:
- Complete source code (31 files)
- Full test suite with fixtures
- 5 documentation guides
- Setup instructions
- API reference

This project showcases my ability to design scalable systems, implement
security best practices, and create maintainable, well-documented code.
```

- [ ] Description written
- [ ] Under 500 words
- [ ] Mentions key technologies
- [ ] Explains your unique angle (educator background)
- [ ] Highlights technical achievements

### Why MLH Fellowship?

Connect your project to MLH:

- [ ] Explain how this project prepares you for SRE work
- [ ] Mention specific skills (APIs, databases, testing, security)
- [ ] Show your passion for education + tech
- [ ] Demonstrate readiness to learn and grow

---

## Final Pre-Submission Steps

### 1. Fresh Clone Test

```bash
# Clone your repo in a new location
cd /tmp
git clone <your-github-repo-url>
cd lesson-plan-api

# Follow your own QUICKSTART.md
# Can you set it up without any external knowledge?
```

If you encounter any issues, update the documentation!

### 2. Get a Friend to Test

Ask a developer friend to:
- Clone your repo
- Follow QUICKSTART.md
- Try creating a lesson plan
- Give feedback on clarity

### 3. Final Code Review

Review your own code:
- Would you be proud to explain any file to an interviewer?
- Is every function clear and purposeful?
- Are there any "TODO" or "FIXME" comments?
- Is the code consistent in style?

### 4. Documentation Proofread

- Check for typos and grammar
- Verify all code examples work
- Ensure file paths are correct
- Test all command examples

### 5. Personal Touch

- Add your name to README
- Include your background in PROJECT_SUMMARY
- Make sure your contact info is correct
- Add a personal note about why you built this

---

## Submission

### Before You Submit

1. Push all changes to GitHub
2. Verify GitHub repo looks good (check on github.com)
3. Test the repository URL in an incognito browser
4. Make sure all documentation renders properly on GitHub

### When You're Ready

1. Copy your GitHub repository URL
2. Fill out the MLH Fellowship application
3. Paste your repository URL
4. Submit your project description
5. Answer all application questions
6. Double-check everything before final submit

---

## Post-Submission

### If You Find Issues

Don't panic! You can:
1. Fix the issues
2. Push to GitHub
3. Send an updated link to MLH (if possible)

Small typos are okay—focus on:
- Code functionality
- Working setup instructions
- Clear documentation

### Prepare for Follow-Up

Be ready to discuss:
- Design decisions (why FastAPI, why PostgreSQL)
- Challenges you faced (database schema, authentication)
- What you'd improve (async, service layer)
- How it relates to SRE work (APIs, databases, monitoring)

---

## Common Mistakes to Avoid

❌ **Don't**:
- Include .env file in repository
- Hardcode passwords or secrets
- Submit with failing tests
- Forget to update README with your info
- Use absolute file paths
- Include TODO comments for incomplete features
- Submit with debugging code

✅ **Do**:
- Test setup from scratch
- Include comprehensive documentation
- Show your personality in docs
- Demonstrate best practices
- Explain your decisions
- Make it easy for reviewers

---

## Confidence Check

Before submitting, you should be able to confidently say "yes" to:

- [ ] I can explain every design decision in this project
- [ ] A new developer could set this up using my docs
- [ ] All tests pass and demonstrate key functionality
- [ ] The code is production-quality
- [ ] I'm proud to show this to potential employers
- [ ] This demonstrates skills relevant to SRE work
- [ ] The documentation is clear and helpful
- [ ] There are no secrets or sensitive data in the repo

---

## You're Ready! 🚀

If you've completed this checklist, you have a strong, professional code sample that demonstrates:

✅ Technical skills (Python, FastAPI, PostgreSQL, JWT)
✅ Best practices (testing, security, documentation)
✅ Professional development (Git, docs, clean code)
✅ Problem-solving (real-world educator problem)
✅ Communication (clear documentation)

**Good luck with your MLH Fellowship application!**

---

## Questions?

If you're unsure about anything:
1. Review the relevant documentation file
2. Test it manually to verify it works
3. If still unsure, it's better to over-document than under-document

**Remember**: The goal is to show your skills clearly. A well-documented, working project beats a complex, confusing one every time.

---

**Last Updated**: Before submission
**Next Step**: Submit your application!
