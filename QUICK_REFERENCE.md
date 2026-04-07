# ⚡ Quick Reference — Common Commands

## 🚀 Getting Started (First Time)

```bash
# 1. Clone repo
git clone https://github.com/tomato-ux12/idea-validator.git
cd idea-validator

# 2. Setup backend
cd backend
bash setup.sh
# Edit .env with Supabase credentials
python main.py

# 3. In new terminal, setup frontend
npm install
npm run dev

# 4. Test
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

---

## 📚 Development (Daily)

### Start services

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Frontend
npm run dev

# Terminal 3: Tests (optional)
cd backend
pytest -v --watch

# Terminal 4: Git
git status
```

---

## 🧪 Testing

### Backend tests

```bash
cd backend

# All tests
pytest test_api.py -v

# Specific test
pytest test_api.py::test_register_user -v

# With coverage
pytest test_api.py --cov=. --cov-report=html

# Watch mode (requires pytest-watch)
ptw test_api.py
```

### Frontend tests (Phase 2)

```bash
npm test
npm run test:watch
```

---

## 🐛 Debugging

### Backend debug

```bash
# Print SQL being executed
SQLALCHEMY_ECHO=1 python main.py

# Verbose logging
python main.py --log-level DEBUG

# Test single endpoint
curl -X GET http://localhost:8000/api/opportunities/list
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","freelance_type":"seo","years_experience":2}'
```

### Frontend debug

```bash
# React DevTools Chrome extension
# Redux DevTools (install extension)
# Console: localStorage.getItem('user_id')
```

---

## 📦 Docker (Local)

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Logs
docker-compose logs -f backend

# Stop
docker-compose down

# Clean
docker-compose down -v  # Also remove volumes
```

---

## 📤 Deployment

### Push to GitHub

```bash
git add .
git commit -m "feat: add backend MVP"
git push origin main
```

### Deploy Backend (Railway)

```bash
# First time setup
railway init
railway link  # Select your repo

# Deploy
git push origin main  # Auto-deploys
# OR manual
railway deploy

# Check status
railway logs -f
railway open
```

### Deploy Frontend (Vercel)

```bash
# First time
vercel login
vercel

# Redeploy
git push origin main  # Auto-deploys
# OR manual
vercel deploy --prod
```

### Update Environment Variables

**Railway Dashboard:**
```
Settings → Environment Variables
Add: SUPABASE_URL, SUPABASE_KEY, etc.
```

**Vercel Dashboard:**
```
Settings → Environment Variables
Add: VITE_API_URL
```

**Redeploy after changing vars:**
```bash
# Railway
railway redeploy

# Vercel
vercel redeploy --prod
```

---

## 🔧 Database Management

### Local (Supabase Cloud)

```bash
# View schema
# → Supabase Dashboard → SQL Editor

# Run migrations
# Paste SQL in Supabase SQL Editor

# Backup
# → Supabase Dashboard → Backups → Download
```

### Reset database

```sql
-- Drop tables
DROP TABLE tests;
DROP TABLE users;

-- Recreate (paste full schema)
-- From database.py init_schema()
```

---

## 📝 Code Commands

### Generate boilerplate

```bash
# API client types (auto from backend)
# → Already done in backend/api-client.ts

# Component template (shadcn/ui)
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add tabs
```

### Code formatting

```bash
# Backend
cd backend
black *.py
flake8 .

# Frontend
npm run lint
npm run format
```

### Type checking

```bash
# Frontend
npx tsc --noEmit

# Backend
mypy backend/
```

---

## 🚨 Troubleshooting Commands

### Check Python setup

```bash
python --version  # Should be 3.8+
pip --version
which python
which pip
```

### Check Node setup

```bash
node --version   # Should be 16+
npm --version
which npm
```

### Check dependencies

```bash
# Backend
cd backend
pip list
pip install -r requirements.txt --upgrade

# Frontend
npm outdated
npm audit
npm update
```

### Network troubleshooting

```bash
# Test backend
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Test Supabase connection
curl https://your-project.supabase.co/rest/v1/
# Should return 404 (OK, means server is responding)

# Test frontend build
npm run build
npm run preview
```

### Reset everything

```bash
# Backend
cd backend
rm -rf venv/
bash setup.sh

# Frontend
rm -rf node_modules/
npm install

# Git
git clean -fd
git reset --hard HEAD
```

---

## 📊 Monitoring

### Backend logs

```bash
# Local
tail -f backend.log

# Railway
railway logs -f

# Supabase
# → Dashboard → Logs → Database
```

### Performance profiling

```bash
# Backend timing
python -m cProfile -o profile_stats.prof main.py

# View
python -m pstats profile_stats.prof
> sort cumtime
> stats 10
```

---

## 🔑 Environment Variables Management

### List all required vars

```bash
cd backend
grep "settings\." main.py routes_*.py
# Tells you which vars are used
```

### Rotate secrets

```bash
# Generate new JWT_SECRET
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in:
# - .env (local)
# - Railway Environment Variables
# - Vercel Environment Variables (if needed)
```

---

## 📚 Documentation Commands

```bash
# Generate backend docs
# Already at http://localhost:8000/docs (Swagger)
# And http://localhost:8000/redoc (ReDoc)

# Generate frontend component docs
# (Phase 2: Storybook integration)
npm run storybook
```

---

## 🎯 Common Git Workflows

### Feature branch

```bash
git checkout -b feature/add-scoring
# Make changes
git add .
git commit -m "feat: implement scoring logic"
git push origin feature/add-scoring
# → Create PR on GitHub
```

### Update from main

```bash
git fetch origin
git rebase origin/main
# OR
git merge origin/main
```

### See what changed

```bash
git diff
git log --oneline -10
git status
```

---

## 📞 Getting Help

**Backend issues?**
```bash
cd backend
# Check logs
python main.py  # Look for errors
# Check .env
cat .env  # Verify Supabase creds
# Test API
curl http://localhost:8000/health
```

**Frontend issues?**
```bash
npm run dev  # Check terminal output
# Check console in browser DevTools
# Verify .env VITE_API_URL
cat .env
```

**Database issues?**
```bash
# Try connecting directly
psql postgresql://user:password@host:port/postgres
# Or use Supabase dashboard
```

---

## 🎯 Workflow Example (Daily)

```bash
# 1. Start of day
git pull origin main

# 2. Start services
# Terminal 1
cd backend && python main.py
# Terminal 2
npm run dev

# 3. Make changes
# Edit files as needed

# 4. Test
pytest backend/test_api.py -v

# 5. Commit
git add .
git commit -m "feat: clear message"
git push origin feature/my-feature

# 6. End of day
# (Auto-deploy on PR merge)
```

---

**Last updated:** April 2024  
**Questions?** See README.md or individual module docs.
