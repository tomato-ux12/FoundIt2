# 🚀 Deployment Guide

Guide complet pour déployer l'app en production.

---

## 📋 Table des matières

1. [Backend (Railway)](#backend-railway)
2. [Frontend (Vercel)](#frontend-vercel)
3. [Database (Supabase)](#database-supabase)
4. [Variables d'environnement](#variables-denvironnement)
5. [Monitoring & Logs](#monitoring--logs)

---

## Backend (Railway)

### Prérequis

- Compte [Railway.app](https://railway.app)
- Code pusté sur GitHub (public ou private)

### Étapes

#### 1. Créer un nouveau projet Railway

```bash
# Installer CLI Railway
npm i -g @railway/cli

# Login
railway login

# Initialiser depuis le repo
railway init
```

#### 2. Configurer le service

```bash
# Dans le dashboard Railway
# New → GitHub repo → Select your repo
```

#### 3. Configurer les variables d'environnement

Dans Railway Dashboard → Environment:

```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxx...
ANTHROPIC_API_KEY=sk-ant-xxx (optionnel)
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
```

#### 4. Setup database

Railway peut se connecter à Supabase. Dans Settings:
- Database: External PostgreSQL
- Host: Supabase URL
- Database: postgres
- User: postgres
- Password: votre mot de passe

#### 5. Deploy

```bash
# Automatic on git push to main
# Ou manuel:
railway deploy
```

### Vérifier le deploy

```bash
# Récupérer l'URL Railway
railway open

# Tester l'endpoint
curl https://your-railway-app.up.railway.app/health
```

---

## Frontend (Vercel)

### Prérequis

- Compte [Vercel](https://vercel.com)
- Code sur GitHub

### Étapes

#### 1. Importer le projet

```bash
# Dans Vercel dashboard
# New Project → Import Git Repo → Select your repo
```

#### 2. Configurer les variables d'environnement

Settings → Environment Variables:

```
VITE_API_URL=https://your-railway-app.up.railway.app
```

#### 3. Build settings

- Framework: Vite
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

#### 4. Deploy

```bash
# Automatique on git push
# Ou via Vercel CLI
vercel deploy --prod
```

### Custom domain

Settings → Domains:
- Ajouter votre domaine custom
- Configurer DNS records selon les instructions Vercel

---

## Database (Supabase)

### Créer un projet Supabase

1. [supabase.com](https://supabase.com) → New Project
2. Choisir region (EU recommandé pour RGPD)
3. Définir mot de passe admin
4. Attendre ~2 minutes pour l'initialisation

### Initialiser le schema

#### Option 1: Via SQL Editor (plus simple)

Supabase Dashboard → SQL Editor → New Query

Copier-coller le SQL:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  freelance_type TEXT NOT NULL,
  years_experience INT NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Tests table
CREATE TABLE IF NOT EXISTS tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  opportunity_id TEXT NOT NULL,
  started_at TIMESTAMP DEFAULT now(),
  completed_at TIMESTAMP,
  conversion_rate DECIMAL,
  positive_responses INT,
  total_outreach INT,
  precommits INT,
  calls_booked INT,
  notes TEXT,
  verdict TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- Indexes
CREATE INDEX idx_tests_user_id ON tests(user_id);
CREATE INDEX idx_tests_opportunity_id ON tests(opportunity_id);
```

Run → Done!

#### Option 2: Via Python script

```bash
cd backend
python -c "from database import Database; print(Database.init_schema())"
```

Copier le SQL output et paster dans Supabase.

### Récupérer les clés API

Supabase Dashboard → Settings → API:

- **SUPABASE_URL** : Project URL
- **SUPABASE_KEY** : anon public key
- **SUPABASE_SERVICE_ROLE_KEY** : service_role (garder secret!)

Sauvegarder dans:
- `backend/.env` (local)
- Railway Environment (production)
- Vercel Environment (optional, juste pour seed data)

### Row Level Security (RLS)

**MVP**: RLS désactivée (plus simple)

Production (Phase 2):

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE tests ENABLE ROW LEVEL SECURITY;

-- User can only see their own data
CREATE POLICY "Users can only see themselves"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can only see their tests"
  ON tests FOR SELECT
  USING (auth.uid() = user_id);
```

---

## Variables d'Environnement

### Backend (.env production)

```env
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Anthropic (Phase 2)
ANTHROPIC_API_KEY=sk-ant-...

# App
CORS_ORIGINS=https://app.idea-validator.com,https://www.idea-validator.com
JWT_SECRET=generate-strong-random-key-here
ENVIRONMENT=production
```

### Frontend (.env.production)

```env
VITE_API_URL=https://api.your-domain.com
```

### Générer JWT_SECRET

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Node
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

## Monitoring & Logs

### Railway

Dashboard → Logs:

```bash
# Voir les logs en direct
railway logs -f

# Filtrer par service
railway logs backend -f
```

### Supabase

Dashboard → Logs:
- Database logs
- Auth logs
- API requests

### Sentry (optional)

Intégrer Sentry pour error tracking:

```python
# backend/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
    environment="production"
)
```

### Health checks

```bash
# Vérifier que l'API est up
curl https://your-api.com/health

# Supabase connection
curl https://your-api.com/api/opportunities/list
```

---

## 🔐 Checklist Sécurité

- [ ] `.env` files ajoutés à `.gitignore`
- [ ] CORS_ORIGINS restreint à votre domaine
- [ ] JWT_SECRET généré aléatoirement (32+ bytes)
- [ ] SUPABASE_SERVICE_ROLE_KEY jamais dans les logs ou frontend
- [ ] Database backups activés (Supabase auto)
- [ ] HTTPS activé (Vercel/Railway auto)
- [ ] Rate limiting configuré (Phase 2)
- [ ] CORS_ORIGINS en prod ≠ CORS_ORIGINS en dev

---

## 🚨 Troubleshooting

### API returns 403 CORS error

```
❌ Access-Control-Allow-Origin missing
```

Solution:

1. Vérifier `CORS_ORIGINS` dans backend `.env`
2. Redémarrer le service (Railway redeploy)
3. Vérifier que le frontend URL est dans la liste

### Database connection failed

```
❌ could not connect to server: Connection refused
```

Solution:

1. Vérifier que Supabase project est running
2. Vérifier `SUPABASE_URL` et `SUPABASE_KEY`
3. Vérifier la région (pas de changement après creation)

### Frontend shows API 404

```
GET https://api.xxx/api/opportunities/list → 404
```

Solution:

1. Vérifier que `VITE_API_URL` ne finit pas par `/`
2. Vérifier que le backend est déployé et running
3. Tester via curl: `curl $VITE_API_URL/health`

### Build fails on Vercel

```
npm ERR! code E404
npm ERR! 404 Not Found
```

Solution:

1. Vérifier que `package.json` existe à la racine
2. Vérifier que `.gitignore` n'exclut pas `package-lock.json`
3. Redéployer depuis Vercel dashboard

---

## 📈 Performance Tips

### Backend

- [ ] Enable gzip compression (déjà activé)
- [ ] Use connection pooling (Supabase inclus)
- [ ] Cache opportunities en mémoire ou Redis (Phase 2)
- [ ] Rate limiting par IP/user (Phase 2)

### Frontend

- [ ] Code splitting (Vite auto)
- [ ] Image optimization (Vercel auto)
- [ ] Lazy load components
- [ ] Use React.memo pour pures components

### Database

- [ ] Indexes sur `user_id` et `opportunity_id` (créés)
- [ ] Enable database query cache (Supabase)
- [ ] Optimize JWT tokens (Phase 2)

---

## 🚀 Post-Deploy Checklist

- [ ] Health checks passing
- [ ] Frontend loads without errors
- [ ] API responds to requests
- [ ] Database queries working
- [ ] User can register
- [ ] User can view opportunities
- [ ] Logs are clean (no errors)
- [ ] Custom domain working (if setup)

---

## 📞 Support

- Railway docs: https://docs.railway.app
- Vercel docs: https://vercel.com/docs
- Supabase docs: https://supabase.com/docs
- FastAPI docs: https://fastapi.tiangolo.com/

---

**Version**: 0.1.0  
**Last updated**: April 2024
