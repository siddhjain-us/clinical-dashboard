# ⚡ HACKATHON COMMAND CHEATSHEET
## Print This & Keep It Open During Hackathon

---

## 🎬 START HERE (Minute 0-5)

### Installation Check
```bash
# Verify plugins installed
/plugin list

# Should see: superpowers, get-shit-done
# If missing: refer to HACKATHON_MANUAL.md Installation section
```

### Brainstorm (Everyone Together)
```bash
/superpowers:brainstorm
# Claude guides you through: What? Why? MVP? How?
# Saves DESIGN.md automatically
```

---

## 📋 PLANNING (Minute 5-10)

### Generate Task Breakdown
```bash
# In Claude Code, ask:
"Read DESIGN.md. Break this into 6-8 atomic tasks (2-5 min each).
Person A gets backend, Person B gets frontend.
List format: Task # | Description | Owner (A/B)"
```

### Document API Contract
```bash
# Create docs/API.md with:
GET /api/health
POST /api/data
etc.
# This BEFORE either person writes code
```

---

## 💻 PERSON A: BACKEND WORKFLOW

### Start Session (Minute 10)
```bash
# Terminal 1: Backend development
claude --dangerously-skip-permissions

# This enables GSD: atomic tasks, fresh context, clean commits
```

### Common Backend Tasks
```bash
# Task 1: Server Setup
npm install
# server.js: basic Express server on port 5000

# Task 2: Database
# database.js: SQLite schema + queries

# Task 3: API Endpoint 1
# server.js: POST /api/data

# Task 4: API Endpoint 2
# server.js: GET /api/data

# After EACH task:
git add .
git commit -m "feat: [task name]"
git status  # Should be clean
```

### Test Commands
```bash
# Is server running?
curl http://localhost:5000/api/health

# Test endpoint with data
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}'

# Check database
sqlite3 database.db ".tables"
sqlite3 database.db "SELECT * FROM users LIMIT 5;"
```

### Deployment (Minute 70)
```bash
# Push to production
git push origin main

# Railway auto-deploys (or manual trigger in dashboard)

# Verify production endpoint
curl https://your-app-railroad.app/api/health

# Share URL with Person B:
# https://your-app-railroad.app
```

---

## 🎨 PERSON B: FRONTEND WORKFLOW

### Start Session (Minute 10)
```bash
# Terminal 2: Frontend development
# Separate from Person A so no file conflicts
claude --dangerously-skip-permissions
```

### Common Frontend Tasks
```bash
# Task 1: HTML Structure
# public/index.html: form, buttons, display area

# Task 2: Styling
# public/styles.css: make it look clean (Tailwind classes or vanilla CSS)

# Task 3: API Integration
# public/app.js: fetch() calls to Person A's endpoints

# Task 4: Error Handling
# public/app.js: show errors, loading states

# After EACH task:
git add .
git commit -m "feat: [task name]"
git status  # Should be clean
```

### Test Commands
```bash
# Does frontend load?
# Browser: http://localhost:5000/public/index.html

# Check for JavaScript errors (F12)
# Console tab: should be clean

# Test API call
# In browser console: fetch('/api/health').then(r => r.json()).then(console.log)
```

### Wait for Backend
```bash
# Person A says: "API endpoint /api/data is ready"
# Person B: Update public/app.js with correct API_URL

# If Person A is slow:
# Use mock data in public/app.js temporarily
const mockData = { name: "John", email: "john@example.com" };

# Later, replace with real API call
```

---

## 🔗 INTEGRATION (Minute 50-70)

### Person B Updates API URL
```javascript
// public/app.js - BEFORE:
const API_URL = 'http://localhost:5000';

// AFTER (when deploying):
const API_URL = 'https://your-app-railroad.app';
```

### Both: End-to-End Test
```bash
# Person A: Start local server
npm run dev

# Person B: Open browser
http://localhost:5000/public/index.html

# Test flow:
# 1. Fill form
# 2. Click submit
# 3. Data appears on page
# 4. Check Person A's terminal: see log message
# 5. Check database: sqlite3 database.db "SELECT * FROM ..."
```

### Debug Checklist
```bash
# ❌ Form doesn't submit?
# → Check browser F12 console for JS errors
# → Check network tab: is request being sent?

# ❌ API returns 404?
# → Check server.js: is endpoint defined?
# → Check logs: "GET /api/data" should appear

# ❌ CORS error?
# → server.js needs: app.use(cors());

# ❌ Database not saving?
# → Check database.js: is INSERT query correct?
# → Check server logs for SQL errors
```

---

## 🚀 DEPLOYMENT (Minute 70-85)

### Person A: Deploy Backend
```bash
# Already did this? Good.
# If not, NOW:
git push origin main

# Check Railway/Render dashboard
# Build should say: ✅ Success

# Get production URL:
# Railway dashboard → Settings → Deployment URL

# Copy: https://your-app-railroad.app
```

### Person B: Update URLs
```javascript
// public/app.js
const API_URL = 'https://your-app-railroad.app';  // Update!
```

### Person B: Test Production
```bash
# Browser console:
fetch('https://your-app-railroad.app/api/health').then(r => r.json()).then(console.log)

# Should print: { status: 'ok' } or similar
```

### Final Git Push
```bash
# Person B: commit updated API URLs
git add public/app.js
git commit -m "feat: update API URL to production"
git push origin main
```

---

## 📝 DEMO PREP (Minute 85-90)

### Write Script (1 min read time)
```
"Hi! We built [Project Name] in 90 minutes with 2 people.

Here's what it does:
1. I click here [click button]
2. Data gets saved [show form submission]
3. Results appear here [point to screen]

We used:
- Express (backend)
- SQLite (database)
- Vanilla JavaScript (frontend)
- Deployed to Railway

Questions?"
```

### Practice (1 min)
```bash
# Actually run through demo once
# Don't wing it
```

### Fallback Plan (1 min prepare)
```bash
# Screenshot working app:
# Command+Shift+4 (Mac) or PrintScreen (Windows)

# Be ready to:
# - Show GitHub repo (judges see your code)
# - Explain technical decisions
# - Show server logs if live is down
# - Describe API endpoints from memory
```

---

## 🆘 EMERGENCY COMMANDS

### Context Getting Stale?
```bash
# Start fresh task
# Explicitly: "Previous context: I've completed tasks 1-5.
# Current state: [git log -5]
# Next task: Complete task 6 - [description]"

# This tells Claude: fresh context, don't repeat work
```

### Merge Conflict?
```bash
# Prevent: Person A and B NEVER edit same file

# If happens:
git status  # Shows conflicted files
# Edit file manually: pick version (remove conflict markers)
git add .
git commit -m "fix: resolved merge conflict"
```

### Deployment Failed?
```bash
# Check Railway/Render logs
# Usually: missing environment variable or dependency

# Fix locally first:
npm install  # Missing package?
npm run dev  # Does it start?

# Then push again:
git push origin main
```

### API Not Working?
```bash
# Test directly:
curl -X GET http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/data -d '{}' -H "Content-Type: application/json"

# Check server logs for error messages
# Fix in server.js, restart, test again
```

---

## ✅ 1-MINUTE PRE-DEMO CHECKLIST

```bash
# [ ] git log --oneline shows 8+ commits
# [ ] npm run dev starts without errors
# [ ] curl http://localhost:5000/api/health returns 200
# [ ] Browser: http://localhost:5000/public/index.html loads
# [ ] Form submission works (data saves + displays)
# [ ] Production URL tested: curl https://... works
# [ ] Demo script written & practiced
# [ ] Fallback screenshot saved
# [ ] GitHub repo is public
# [ ] README.md explains what you built
```

---

## 📊 GIT LOG OUTPUT GOAL

```bash
$ git log --oneline
a7f8e2c feat: update API URL to production
5e6d4c1 feat: add error handling to frontend
3b2a1f8 feat: implement fetch to /api/data
2d8e7a9 feat: add styling with Tailwind
1c5f3e2 feat: create HTML form
6a9b7d8 feat: deploy backend to production
4e8f5c1 feat: add database schema
3d7c2b9 feat: set up Express server
2b1a8e5 Initial commit
```

**What this shows judges:**
- ✅ Regular commits (you were working throughout)
- ✅ Clear commit messages (professional workflow)
- ✅ 8+ features completed (productive 90 min)
- ✅ No huge mega-commits (sign of scattered work)

---

## 🎯 FINAL WISDOM

- **Commit after EVERY task** (even if incomplete, better to revert 1 task than 5)
- **Test early** (don't discover broken API at minute 80)
- **Deploy at minute 70** (not 85 — gives buffer to fix things)
- **Simple beats complex** (1 working feature > 3 broken features)
- **Have fallback** (live demo crashes? Show screenshot + code)

**You've got this! 🚀**
