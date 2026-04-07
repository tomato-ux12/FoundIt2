# Idea Validator Backend

FastAPI backend pour le moteur de validation d'opportunités SaaS.

## 🚀 Quick Start

### 1. Setup Python & dépendances

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurer Supabase

1. Créer un compte sur [supabase.io](https://supabase.io)
2. Créer un nouveau projet
3. Récupérer les clés:
   - `SUPABASE_URL`
   - `SUPABASE_KEY` (anon key)
   - `SUPABASE_SERVICE_ROLE_KEY`

### 3. Créer les tables (SQL Supabase)

Copier-coller le SQL du fichier `database.py` → `Database.init_schema()` dans l'éditeur SQL Supabase.

**Ou** exécuter depuis Python (une fois):

```python
from database import Database
print(Database.init_schema())
# Copy-paste le SQL output dans Supabase SQL editor
```

### 4. Variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec tes clés Supabase
```

### 5. Lancer le serveur

```bash
python main.py
# Ou avec uvicorn directement:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Vérifier: `http://localhost:8000/docs` (Swagger UI)

---

## 📚 API Endpoints

### Auth
- `POST /api/auth/register` — Enregistrer utilisateur
- `GET /api/auth/user/{user_id}` — Récupérer infos utilisateur
- `POST /api/auth/login` — Login (magic link stub)

### Opportunities
- `GET /api/opportunities/list` — Lister les opportunités (max 10, filtrées)
- `GET /api/opportunities/{opportunity_id}` — Détail d'une opportunité
- `GET /api/opportunities/{opportunity_id}/validation-plan` — Plan de test 48h

### Tests
- `POST /api/tests/create` — Créer un test 48h
- `GET /api/tests/{test_id}` — Détail d'un test
- `POST /api/tests/{test_id}/submit-verdict` — Soumettre verdict (CONTINUE/ITERATE/KILL)
- `GET /api/tests/user/{user_id}/stats` — Stats des tests utilisateur
- `GET /api/tests/user/{user_id}/history` — Historique des tests

---

## 🗂️ Structure

```
backend/
├── main.py                 # FastAPI app + routes principales
├── config.py              # Settings/configuration
├── models.py              # Pydantic models
├── database.py            # Supabase client + queries
├── services.py            # Business logic (scoring, filtering)
├── mock_data.py           # Mock opportunities (MVP data)
├── routes_auth.py         # Auth endpoints
├── routes_opportunities.py # Opportunities endpoints
├── routes_tests.py        # Tests endpoints
├── requirements.txt       # Python dependencies
├── .env.example           # Template variables d'environnement
└── README.md              # This file
```

---

## 🔑 Key Features

### Hard Rules (PRD)
- **Max 10 opportunités affichées** — toujours
- **Preuve de paiement** — minimum 10 utilisateurs payants
- **Auto-reject** — score < 40
- **Scoring transparent** — formule explicite, toujours accompagnée d'explication

### Mock Data (MVP)
- **7 opportunités** pour SEO freelance avec scores heuristiques
- Données cohérentes avec PRD (quotes, sources, budgets)
- Testable sans scraper réel

### Supabase Integration
- Users table (enregistrement)
- Tests table (tracking 48h tests)
- Auth (magic link stub, prêt pour expansion)

---

## 🔧 Todo Before Production

1. **Auth réelle** : remplacer stub magic link par Supabase Auth (JWT)
2. **Scraper réel** : implémenter G2/Capterra scraper + clustering LLM
3. **Stripe intégration** : checkout payant
4. **Anthropic API** : intégrer Claude pour extraction/scoring LLM
5. **Monitoring** : Sentry pour erreurs
6. **Tests** : pytest pour coverage

---

## 📝 Environment Variables

```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxxx...
ANTHROPIC_API_KEY=sk-ant-xxx (optionnel MVP)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
JWT_SECRET=votre-secret
ENVIRONMENT=development
```

---

## 🧪 Testing

```bash
# Tester les endpoints (curl)
curl http://localhost:8000/

# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc
```

---

## 🚨 Known Limitations (MVP)

- **Auth**: Stub simple (pas de JWT réel)
- **Data**: Mock hardcoded (pas de scraper)
- **Tests**: Verdict auto-calculé (pas de tracking utilisateur réel en 48h)
- **Anthropic**: Pas intégré (prêt pour Phase 2)

---

## 📦 Dépendances principales

- **FastAPI** : framework web
- **Uvicorn** : ASGI server
- **Pydantic** : validation données
- **Supabase** : BDD + auth
- **Python-dotenv** : env vars

---

## 📞 Support

Pour questions: voir PRD ou ouvrir issue GitHub.

---

**Version**: 0.1.0 MVP  
**Last updated**: Avril 2024
