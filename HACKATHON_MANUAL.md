# 🚀 90-Minute 2-Person Hackathon with Claude Code
## Complete Instruction Manual

---

## 📋 TABLE OF CONTENTS
1. [Pre-Hackathon Setup (Do This NOW)](#pre-hackathon-setup)
2. [Claude Code Plugins & Skills Installation](#installation)
3. [Folder Structure](#folder-structure)
4. [Task Division for 2 People](#task-division)
5. [90-Minute Timeline](#timeline)
6. [Claude Code Commands Cheatsheet](#cheatsheet)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 PRE-HACKATHON SETUP {#pre-hackathon-setup}

### ✅ Do This RIGHT NOW (Before Hackathon Starts)

**1. Install Required Claude Code Plugins**
```bash
# Plugin 1: Superpowers (Planning & Structured Workflows)
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# Plugin 2: Get Shit Done (Context Management & Atomic Commits)
npx get-shit-done-cc --claude --global

# Plugin 3 (OPTIONAL - Only if UI-heavy): UI/UX Pro Max Skill
# /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
# /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

**2. Verify Installations**
```bash
# Restart Claude Code
# You should see in your session start:
# ✓ You have Superpowers
# ✓ GSD system loaded
```

**3. Bookmark These Resources**
- Awesome Claude Code: https://github.com/hesreallyhim/awesome-claude-code
- Superpowers Repo: https://github.com/obra/superpowers
- GSD Repo: https://github.com/gsd-build/get-shit-done

**4. Prepare Your Git Repository** (Clone or Create)
```bash
mkdir hackathon-project
cd hackathon-project
git init
git remote add origin https://github.com/YOUR-TEAM/hackathon.git
```

**5. Set Up GitHub/Deployment**
- Create GitHub repo (public or private)
- Have Vercel/Railway account ready
- Set up environment variables (.env.example)

---

## 📦 INSTALLATION GUIDE {#installation}

### What Each Plugin Does

#### **Plugin 1: Superpowers (Structured Planning)**
- **Purpose**: Guides you through brainstorm → design → plan → execute workflow
- **Activates**: Automatically when you start coding
- **Key Commands**:
  - `/superpowers:brainstorm` — Refine your idea before coding
  - `/superpowers:write-plan` — Break work into tasks
  - `/superpowers:code-reviewer` — Review implementation against spec

#### **Plugin 2: Get Shit Done (Context Engineering)**
- **Purpose**: Prevents context rot by splitting work into atomic tasks
- **How it works**: Each task runs in fresh context with git commits
- **Requires**: Run with `claude --dangerously-skip-permissions` (no approval prompts)
- **Key Benefit**: No hallucination drift, clean git history for debugging

#### **Plugin 3: UI/UX Pro Max (Design Intelligence) - OPTIONAL**
- **Purpose**: Auto-generates design systems for UI-heavy projects
- **When to use**: If your hackathon problem involves UI/dashboard/landing page
- **Command**: `python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system`

---

## 📁 FOLDER STRUCTURE {#folder-structure}

### Minimal 2-Person Setup
Create this structure BEFORE the hackathon starts:

```
hackathon-project/
├── README.md                    # Project overview (fill during hackathon)
├── package.json                 # Node.js dependencies
├── .gitignore                   # Git ignore file
├── .env.example                 # Environment variables template
│
├── server.js                    # Backend entry point (Person A)
├── database.js                  # Database setup (Person A)
│
├── public/                      # Frontend files (Person B)
│   ├── index.html              # HTML structure
│   ├── styles.css              # CSS styling
│   └── app.js                  # Frontend JavaScript
│
├── docs/                        # Documentation (updated during)
│   ├── API.md                  # API endpoints spec
│   ├── ARCHITECTURE.md         # System architecture
│   └── SETUP.md                # Setup instructions
│
├── .claude/                     # Claude Code configuration
│   └── claude.json             # Project context
│
└── .github/
    └── workflows/
        └── deploy.yml          # CI/CD (optional)
```

### Initialize package.json NOW
```json
{
  "name": "hackathon-2person",
  "version": "1.0.0",
  "scripts": {
    "dev": "node server.js",
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "sqlite3": "^5.1.6"
  }
}
```

### Create .claude/claude.json NOW
```json
{
  "name": "hackathon-2person",
  "instructions": "You are building a hackathon project with 2 developers. Use Superpowers for planning and GSD for execution. Keep work split: Person A = backend/database, Person B = frontend/UI. No file conflicts. Fresh context per task. Atomic commits.",
  "rules": [
    "Person A ONLY touches: server.js, database.js, docs/API.md",
    "Person B ONLY touches: public/*, docs/ARCHITECTURE.md",
    "All API endpoints documented in docs/API.md before coding",
    "Every git commit includes task completion verification",
    "Deploy to production at minute 70 (15 min before demo)"
  ]
}
```

---

## 👥 TASK DIVISION FOR 2 PEOPLE {#task-division}

### Person A: Full-Stack Backend + Deployment
**Owns:** `server.js`, `database.js`, `docs/API.md`, `.env`

**Responsibilities:**
1. **API Endpoints** — Build all REST endpoints (or GraphQL if preferred)
2. **Database** — Schema design, migrations, data models
3. **Authentication** (if needed) — Sessions, JWT, OAuth
4. **Deployment** — Push to Railway/Render, manage environment variables
5. **Integration** — Verify frontend can call your APIs

**Skill Required:** Backend logic, database design, DevOps

---

### Person B: Frontend + Integration + Demo
**Owns:** `public/`, `docs/ARCHITECTURE.md`, demo script

**Responsibilities:**
1. **HTML Structure** — Build forms, pages, components
2. **Styling** — CSS (Tailwind recommended) for clean design
3. **API Integration** — Call Person A's endpoints with fetch()
4. **Error Handling** — User-friendly error messages
5. **Demo Polish** — Make it look good, prepare 1-2 min pitch

**Skill Required:** Frontend, CSS, UX basics

---

## ⏱️ 90-MINUTE TIMELINE {#timeline}

### Minutes 0-5: Problem Understanding & Brainstorming
```bash
# Person A + B together (5 min max)
# Read the problem statement carefully

# THEN → Person A runs in Claude Code:
/superpowers:brainstorm
# Claude walks you through: What are we building? MVP? Core features?
# Saves DESIGN.md automatically

# Outcome: Clear 1-page design spec everyone agrees on
```

### Minutes 5-10: Architecture & Task Breakdown
```bash
# Person A + B together (5 min max)

# In Claude Code, ask:
"Read DESIGN.md and break this into 5-8 atomic tasks (2-5 min each).
Person A gets backend tasks, Person B gets frontend tasks.
Format:
- Task 1: [Description] (Person A/B)
- Task 2: [Description] (Person A/B)
..."

# Claude generates task list
# Copy this to docs/TASKS.md

# Outcome: Clear task ownership, no ambiguity
```

### Minutes 10-50: Parallel Core Development (40 min)

#### Person A's Workflow (Backend)
```bash
# Start Claude Code with GSD enabled
claude --dangerously-skip-permissions

# For each backend task:
# Task 1: Set up Express server + database
# Task 2: Create /api/users endpoint
# Task 3: Create /api/data endpoint
# Task 4: Add error handling

# After EACH task:
git add .
git commit -m "feat: completed [task name]"

# GSD automatically: runs tests, verifies output, fresh context for next task
```

#### Person B's Workflow (Frontend)
```bash
# In a separate Claude Code terminal/window
claude --dangerously-skip-permissions

# For each frontend task:
# Task 1: Build HTML structure (forms, layout)
# Task 2: Add CSS styling (Tailwind)
# Task 3: Implement API calls to Person A's endpoints
# Task 4: Add error messages + loading states

# After EACH task:
git add .
git commit -m "feat: completed [task name]"

# GSD keeps context fresh, prevents hallucination
```

**Key Rules During This Phase:**
- ✅ Person A commits to `server.js`, `database.js`
- ✅ Person B commits to `public/index.html`, `public/styles.css`, `public/app.js`
- ✅ ZERO merge conflicts (different files)
- ✅ Person A's done? Help Person B debug or deploy early

---

### Minutes 50-70: Integration & Testing (20 min)

#### Person A (5 min)
```bash
# Verify all endpoints work:
curl -X GET http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/data

# Push backend to production (Railway/Render):
git push origin main
# Railway auto-deploys (or manual deploy)
# Copy production URL: https://your-app-railway.app

# Verify production endpoints:
curl -X GET https://your-app-railway.app/api/health
```

#### Person B (10 min)
```bash
# Update API URLs in public/app.js to production URL
const API_URL = 'https://your-app-railway.app';  // Not localhost!

# Test frontend against live backend:
# Open browser → localhost:5000/public/index.html
# Try forms, verify data saves

# Fix any integration bugs (usually CORS, missing fields)
```

#### Both (5 min)
```bash
# Do a full end-to-end test:
# 1. Open frontend
# 2. Submit form / trigger API call
# 3. Verify data saved in database
# 4. Verify response displayed in UI

# If broken, debug together:
# - Check browser console (F12) for errors
# - Check server logs for API errors
# - Use `curl` to test endpoints directly
```

---

### Minutes 70-85: Final Deployment & Polish (15 min)

#### Person A (5 min)
```bash
# Deploy to production (if not already done)
git push origin main

# Verify all endpoints live:
curl -X GET https://your-app-production.app/api/health

# Share production URL with Person B
```

#### Person B (10 min)
```bash
# Update all hardcoded localhost URLs to production

# Final UI polish (2 min):
# - Fix any layout issues
# - Ensure buttons are clickable
# - Test on mobile if time (one person's phone)

# Take a screenshot for fallback demo:
# If live demo breaks, show this screenshot
```

---

### Minutes 85-90: Demo Prep (5 min)

#### Person A + B Together
```bash
# Write 1-2 minute demo script:

"Hi! We built [project name] in 90 minutes.
 Here's what it does:
 
 1. [Show the UI]
 2. [Click form, submit data]
 3. [Data appears in [location]]
 4. [Show architecture: Frontend → API → Database]
 
 Built with: Express, SQLite, Vanilla JS
 Deployed to: Railway + Vercel
"

# Practice demo ONCE (2 min)

# Have fallback ready:
# - Screenshot of working app
# - GitHub repo link
# - Be ready to show code in IDE if live breaks
```

---

## ⌨️ CLAUDE CODE COMMANDS CHEATSHEET {#cheatsheet}

### Superpowers Commands (Start of Hackathon)
```bash
/superpowers:brainstorm
# Walks you through: What are you building? MVP? Requirements?
# Saves DESIGN.md with spec

/superpowers:write-plan
# Breaks work into granular tasks (2-5 min each)
# Saves PLAN.md

/superpowers:code-reviewer
# After implementation: reviews code against spec
# Catches bugs before demo
```

### Get Shit Done Commands (Throughout Hackathon)
```bash
# NOT slash commands — GSD is activated by running:
claude --dangerously-skip-permissions

# Then just code normally. GSD automatically:
# - Splits work into small tasks
# - Runs each in fresh context
# - Commits after each task
# - Prevents context rot
```

### Git Commands (After Each Task)
```bash
# Stage changes
git add .

# Atomic commit (important for GSD + debugging)
git commit -m "feat: [task name] — [what was accomplished]"

# Push to GitHub
git push origin main

# Check status
git status
git log --oneline | head -10
```

### Testing & Debugging Commands
```bash
# Start local server
npm run dev
# Should print: "Server running on port 5000"

# Test API endpoint
curl -X GET http://localhost:5000/api/health

# Test with data
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'

# Check server logs
# Should print request info + any errors

# Browser console (F12)
# Check for JavaScript errors in frontend
```

### Deployment Commands
```bash
# Push to production (Railway/Render auto-deploys)
git push origin main

# Verify production endpoint
curl -X GET https://your-app-production.app/api/health

# Check logs (Railway/Render dashboard)
# Should see: "Server running on port 5000"
```

---

## 🐛 TROUBLESHOOTING {#troubleshooting}

### Problem: CORS Errors
**Symptom:** Frontend can't call backend API
```
Access to XMLHttpRequest at 'https://...' from origin 'http://...'
has been blocked by CORS policy
```

**Fix (Add to server.js):**
```javascript
app.use(cors());  // Add this before routes
```

**Or more restrictive:**
```javascript
app.use(cors({
  origin: 'https://your-frontend-domain.app'
}));
```

---

### Problem: 404 on Endpoint
**Symptom:** `curl` returns 404 on `/api/data`

**Debug:**
```bash
# Check if endpoint is defined in server.js
grep -n "app.get('/api/data'" server.js

# Check if server is running
curl -X GET http://localhost:5000/api/health

# Check logs — should show request
```

**Fix:** Ensure endpoint is defined BEFORE app.listen()
```javascript
app.get('/api/data', (req, res) => {
  res.json({ data: [] });
});

app.listen(5000, () => console.log('Server running'));
```

---

### Problem: Frontend Can't Find Server
**Symptom:** `fetch()` fails silently or "Can't reach server"

**Debug:**
```javascript
// In public/app.js, add logging:
fetch(API_URL + '/api/health')
  .then(res => {
    console.log('✅ Connected to API');
    return res.json();
  })
  .catch(err => console.error('❌ API error:', err));
```

**Fix:** Verify API_URL is correct
```javascript
// Development
const API_URL = 'http://localhost:5000';

// Production
const API_URL = 'https://your-app-railway.app';
```

---

### Problem: Deployment Fails
**Symptom:** Railway/Render build fails

**Debug:**
```bash
# Check logs in Railway/Render dashboard
# Look for: syntax errors, missing dependencies

# Verify locally first
npm install
npm run dev

# Check package.json has all dependencies
npm list
```

**Fix:** Ensure all used packages are in package.json
```bash
npm install express cors sqlite3
```

---

### Problem: Claude Code Running Out of Context
**Symptom:** Claude forgets previous tasks or repeats work

**This is why GSD exists!**
```bash
# Solution: You're already using it
claude --dangerously-skip-permissions

# GSD automatically: fresh context per task, atomic commits
# If still having issues, simplify the current task
```

---

### Problem: Merge Conflicts
**Symptom:** `git pull` shows conflicts

**Prevention (BEST):**
- Person A ONLY edits: `server.js`, `database.js`
- Person B ONLY edits: `public/`
- Never both edit same file

**If conflict happens:**
```bash
# Show conflicts
git status

# Fix conflicts manually (pick Person A or B's version)
# Then:
git add .
git commit -m "fix: merge conflict resolved"
```

---

## 🎯 FINAL CHECKLIST (Minute 85)

- [ ] `git log --oneline` shows 8+ clean commits (tasks completed)
- [ ] `npm run dev` starts without errors
- [ ] `curl http://localhost:5000/api/health` returns 200
- [ ] Frontend loads at `http://localhost:5000/public/index.html`
- [ ] Form submission works end-to-end (data saves + displays)
- [ ] Production deployment shows green ✅ (Railway/Render)
- [ ] Production URL is tested and working
- [ ] README.md filled out (what you built, how to run it)
- [ ] Demo script written (1-2 min pitch)
- [ ] Screenshot saved (fallback if live demo breaks)

---

## 💡 PRO TIPS FOR WINNING

1. **Ship fast, polish later** — Working MVP beats half-built perfect app
2. **Test early** — Don't wait until minute 80 to discover API doesn't work
3. **Use Claude's design system skill** — If UI matters, use ui-ux-pro-max for instant style guide
4. **Commit frequently** — Every 5-10 min, even if incomplete
5. **Have a fallback demo** — Screenshot + GitHub repo link + be ready to show code
6. **Sleep-deprived brains fail on debugging** — Better to have 3 simple features that work than 1 complex broken feature
7. **Document as you go** — Update docs/API.md and README.md while coding (not after)

---

## 📚 REFERENCE LINKS

- **Superpowers**: https://github.com/obra/superpowers
- **Get Shit Done**: https://github.com/gsd-build/get-shit-done
- **Awesome Claude Code**: https://github.com/hesreallyhim/awesome-claude-code
- **Claude Code Docs**: https://docs.anthropic.com/claude-code
- **Express.js Quick Start**: https://expressjs.com/starter/hello-world.html
- **MDN Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **Railway Deployment**: https://railway.app (create account now)
- **Vercel Deployment**: https://vercel.com (for frontend if separate)

---

## 🚀 YOU'RE READY

**Timeline for next 5 minutes:**

1. ✅ Install Superpowers + GSD (run the commands above)
2. ✅ Create folder structure locally
3. ✅ Create GitHub repo + push empty folder structure
4. ✅ Bookmark awesome-claude-code
5. ✅ Share this manual with your teammate

**When problem drops at hackathon:**

1. Read problem (2 min)
2. Both run `/superpowers:brainstorm` (3 min)
3. Break into tasks (5 min)
4. Person A: `claude --dangerously-skip-permissions` in Terminal 1
5. Person B: `claude --dangerously-skip-permissions` in Terminal 2
6. Go.

---

**Good luck! 🎉**
