# 🧠 Idea Validator — Startup Validation Engine

Transform freelance problems into validated SaaS opportunities **before writing a single line of code**.

## 📚 Documentation

- **[PRD](./PRD.md)** — Complete product specification
- **[Backend README](./backend/README.md)** — Backend setup & API docs
- **[Integration Guide](./INTEGRATION_GUIDE.md)** — Frontend-backend integration
- **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** — Production deployment

---

## 🚀 Quick Start

### Backend (FastAPI + Supabase)

```bash
cd backend
bash setup.sh
# Edit .env with your Supabase credentials
python main.py
# Visit http://localhost:8000/docs
```

### Frontend (React + Vite)

```bash
npm install
npm run dev
# Visit http://localhost:5173
```

### Stack

**Backend**
- FastAPI (Python)
- Supabase (PostgreSQL + Auth)
- Pydantic (validation)
- TanStack Query (frontend)

**Frontend**
- React 18 + TypeScript
- Vite (bundler)
- shadcn/ui (components)
- Tailwind CSS (styling)

**Deployment**
- Railway (backend)
- Vercel (frontend)
- Supabase (database)

---

## 📋 Project Structure

```
idea-validator/
├── backend/              # FastAPI backend
│   ├── main.py          # App entry point
│   ├── models.py        # Pydantic models
│   ├── database.py      # Supabase client
│   ├── routes_*.py      # API endpoints
│   └── mock_data.py     # MVP data
├── src/                 # React frontend
│   ├── components/      # UI components
│   ├── hooks/           # Custom hooks
│   ├── pages/           # Page components
│   └── lib/             # Utilities
├── docker-compose.yml   # Local dev setup
├── Dockerfile           # Backend container
└── README.md           # This file
```

---

## 🎯 Core Features (MVP)

### 1. Demand Proof Engine
Extract validated problems from G2/Capterra reviews (mock for MVP)

### 2. Pain-to-Money Score
Rate opportunities 0-100 with transparent formula and explanation

### 3. Market Gap Detector
Identify differentiation angle and existing competitors

### 4. Revenue Blueprint
Pre-fill template: pricing, target customer, acquisition channels

### 5. Validation Engine
Generate 48h test plan with:
- Landing page copy
- Outreach templates (3 variants)
- Success metrics
- Auto-verdict logic (CONTINUE/ITERATE/KILL)

---

## ⚡ Key Constraints (Hard Rules)

✅ **Max 10 opportunities** displayed at any time  
✅ **Proof of payment required** (≥10 paying users)  
✅ **Transparent scoring** (always with explanation)  
✅ **No gamification** (motivation letters only)  
✅ **Disclaimer always visible** ("Validation ≠ Revenue")  

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest test_api.py -v

# Frontend tests (coming soon)
npm test
```

---

## 📡 API Endpoints

### Auth
- `POST /api/auth/register` — Register user
- `POST /api/auth/login` — Login (magic link stub)
- `GET /api/auth/user/{id}` — Get user

### Opportunities
- `GET /api/opportunities/list` — List opportunities (max 10)
- `GET /api/opportunities/{id}` — Get detail (with scoring)
- `GET /api/opportunities/{id}/validation-plan` — Get 48h test plan

### Tests
- `POST /api/tests/create` — Create new test
- `POST /api/tests/{id}/submit-verdict` — Submit verdict
- `GET /api/tests/user/{id}/stats` — Get user stats

Full docs: `http://localhost:8000/docs` (Swagger UI)

---

## 🔑 Environment Variables

### Backend (.env)

```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

---

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for:
- Railway setup (backend)
- Vercel setup (frontend)
- Supabase production config
- Monitoring & logs
- Security checklist

Quick version:

```bash
# Backend → Railway
railway init && railway deploy

# Frontend → Vercel
vercel deploy --prod

# Database → Supabase (already managed)
```

---

## 📊 Test Results

Current metrics:
- ✅ 7 mock opportunities generated
- ✅ All endpoints tested
- ✅ Hard rules enforced
- ✅ Error handling implemented

---

## 🔄 Development Workflow

### Local Development

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
npm run dev

# Terminal 3: Tests
cd backend && pytest --watch
```

### Database Changes

1. Update schema in `backend/database.py`
2. Run SQL in Supabase SQL Editor
3. Update models if needed in `backend/models.py`

### API Changes

1. Create/update route in `backend/routes_*.py`
2. Update client in `backend/api-client.ts`
3. Update hooks in `src/hooks/useApi.ts`

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
# Check Python version (3.8+)
python --version

# Check dependencies
pip install -r backend/requirements.txt

# Check Supabase connection
SUPABASE_KEY=test python -c "from supabase import create_client"
```

**CORS error?**
```bash
# Make sure CORS_ORIGINS in .env includes your frontend URL
# Restart backend after changing .env
```

**Database connection failed?**
```bash
# Verify Supabase credentials in .env
# Check that Supabase project is running
curl $SUPABASE_URL/rest/v1/
```

---

## 📚 Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Supabase Docs](https://supabase.com/docs)
- [React Hooks](https://react.dev/reference/react/hooks)
- [TanStack Query](https://tanstack.com/query/latest)

---

## 📄 License

MIT

---

## 👥 Contributors

- Ibrahim (Product + Backend)
- Frontend Team (Figma → Implementation)

---

**Made with ❤️ for freelancers validating SaaS ideas**

Last updated: April 2024 | Version 0.1.0 (MVP)
