# Frontend Integration Guide

Guide pour connecter ton frontend React au backend FastAPI.

## 📌 Setup rapide

### 1. Copier le client API

```bash
# Copier api-client.ts vers ton frontend
cp backend/api-client.ts src/lib/api.ts
```

### 2. Installer dans ton .env frontend

```env
VITE_API_URL=http://localhost:8000
```

### 3. Utiliser l'API dans tes composants

```typescript
import { fetchGet, fetchPost, API_ENDPOINTS } from '@/lib/api';

// Enregistrer un utilisateur
const handleRegister = async (email: string, type: string, years: number) => {
  const response = await fetchPost(API_ENDPOINTS.auth.register, {
    email,
    freelance_type: type,
    years_experience: years,
  });
  
  // Stocker user_id (localStorage ou state)
  localStorage.setItem('user_id', response.user_id);
};

// Récupérer les opportunités
const loadOpportunities = async () => {
  const response = await fetchGet(
    API_ENDPOINTS.opportunities.list + '?limit=10&offset=0'
  );
  
  setOpportunities(response.items);
};

// Récupérer détail opportunité
const loadDetail = async (opportunityId: string) => {
  const detail = await fetchGet(
    API_ENDPOINTS.opportunities.detail(opportunityId)
  );
  
  setSelectedOpportunity(detail);
};

// Créer un test
const startTest = async (opportunityId: string) => {
  const response = await fetchPost(
    API_ENDPOINTS.tests.create,
    { opportunity_id: opportunityId }
  );
  
  return response.test_id;
};

// Soumettre verdict
const submitVerdict = async (testId: string, results: any) => {
  const response = await fetchPost(
    API_ENDPOINTS.tests.submitVerdict(testId),
    { results }
  );
  
  return response.verdict;
};
```

---

## 🗂️ Flows Frontend à implémenter

### Flow 1: Onboarding → Liste

```
[1] Onboarding (Register)
    ↓
    POST /api/auth/register
    ↓
    Store user_id → localStorage
    ↓
[2] Liste Opportunités
    ↓
    GET /api/opportunities/list?limit=10&offset=0
    ↓
    Display top 10 opportunities
```

### Flow 2: Détail Opportunité → Blueprint

```
[1] Click une opportunité
    ↓
    GET /api/opportunities/{id}
    ↓
    Display: Problem | Score | Market Gap | Blueprint
    ↓
    [Button] "Lancer test 48h"
    ↓
[2] Get Validation Plan
    ↓
    GET /api/opportunities/{id}/validation-plan
    ↓
    Display: Landing page + Outreach templates
```

### Flow 3: Test 48h → Verdict

```
[1] Create Test
    ↓
    POST /api/tests/create { opportunity_id }
    ↓
    Store test_id → localStorage
    ↓
    Display: "Exécute ton test en dehors!"
    ↓
[2] Utilisateur lance son test réel (48h)
    ↓
[3] Saisir Résultats
    ↓
    POST /api/tests/{test_id}/submit-verdict
    ↓
    body: { results: { positive_responses: N, ...} }
    ↓
    Display Verdict: CONTINUE | ITERATE | KILL
```

---

## 💾 State Management (React)

### Option 1: useContext + localStorage

```typescript
// AuthContext.tsx
import { createContext, useState } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(() => 
    localStorage.getItem('user_id') || null
  );
  
  const login = (newUserId: string) => {
    setUserId(newUserId);
    localStorage.setItem('user_id', newUserId);
  };
  
  const logout = () => {
    setUserId(null);
    localStorage.removeItem('user_id');
  };
  
  return (
    <AuthContext.Provider value={{ userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Option 2: TanStack Query (recommandé)

```typescript
// hooks/useOpportunities.ts
import { useQuery } from '@tanstack/react-query';
import { fetchGet, API_ENDPOINTS } from '@/lib/api';

export const useOpportunities = () => {
  return useQuery({
    queryKey: ['opportunities'],
    queryFn: () => fetchGet(
      API_ENDPOINTS.opportunities.list + '?limit=10&offset=0'
    ),
  });
};

export const useOpportunityDetail = (opportunityId: string | null) => {
  return useQuery({
    queryKey: ['opportunity', opportunityId],
    queryFn: () => fetchGet(
      API_ENDPOINTS.opportunities.detail(opportunityId!)
    ),
    enabled: !!opportunityId,
  });
};
```

---

## 🔑 Auth Flow (MVP)

Pour MVP, utiliser localStorage:

```typescript
// hooks/useAuth.ts
export const useAuth = () => {
  const [userId, setUserId] = useState(() => 
    localStorage.getItem('user_id')
  );
  
  const register = async (email: string, type: string, years: number) => {
    const { user_id } = await fetchPost(
      API_ENDPOINTS.auth.register,
      { email, freelance_type: type, years_experience: years }
    );
    
    setUserId(user_id);
    localStorage.setItem('user_id', user_id);
    return user_id;
  };
  
  return { userId, register };
};
```

**Production**: Intégrer Supabase Auth directement côté frontend.

---

## 🧪 Test Local

### Terminal 1: Backend

```bash
cd backend
python main.py
# Devrait écouter http://localhost:8000
```

### Terminal 2: Frontend

```bash
npm run dev
# Devrait écouter http://localhost:5173
```

### Terminal 3: Test API (curl)

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","freelance_type":"seo","years_experience":2}'

# List opportunities
curl http://localhost:8000/api/opportunities/list

# Get detail
curl http://localhost:8000/api/opportunities/{opportunity_id}
```

---

## 🔗 Routes à implémenter côté Frontend

| Page | Endpoint | Méthode |
|---|---|---|
| Onboarding | `/api/auth/register` | POST |
| Liste | `/api/opportunities/list` | GET |
| Détail | `/api/opportunities/{id}` | GET |
| Blueprint | `/api/opportunities/{id}/validation-plan` | GET |
| Test Create | `/api/tests/create` | POST |
| Test Submit | `/api/tests/{id}/submit-verdict` | POST |
| Dashboard | `/api/tests/user/{id}/stats` | GET |

---

## ⚙️ Configuration CORS

Backend CORS est déjà config pour:
- `http://localhost:5173` (Vite dev)
- `http://localhost:3000` (Next.js fallback)

Si tu ajoutes d'autres origins, édite `backend/.env`:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://app.example.com
```

---

## 🚀 Deployment

### Frontend (Vercel)

```bash
# Set env var
VITE_API_URL=https://api.idea-validator.com
```

### Backend (Railway/Heroku)

```bash
# Set env vars
SUPABASE_URL=...
SUPABASE_KEY=...
CORS_ORIGINS=https://app.idea-validator.com
```

---

## 📝 Checklist Intégration

- [ ] Copier `api-client.ts` → `src/lib/api.ts`
- [ ] Setup `.env` avec `VITE_API_URL`
- [ ] Créer `AuthContext` ou custom hooks
- [ ] Implémenter Onboarding page
- [ ] Implémenter Liste page
- [ ] Implémenter Détail page
- [ ] Implémenter Blueprint modal
- [ ] Implémenter Test create flow
- [ ] Implémenter Verdict submit
- [ ] Tester avec backend local
- [ ] CORS configuré
- [ ] Error handling (toasts)

---

## 🐛 Troubleshooting

**CORS Error?**
- Vérifier `CORS_ORIGINS` dans `backend/.env`
- Backend sur 8000, frontend sur 5173
- Redémarrer le backend après changement .env

**API returns 404?**
- Vérifier que `VITE_API_URL` est correct
- Tester avec `curl` d'abord
- Vérifier console browser (Network tab)

**Auth not persisting?**
- Vérifier localStorage: `localStorage.getItem('user_id')`
- Assurer que register retourne `user_id`
- Vérifier que c'est stocké avant de naviguer

---

**Need help?** Voir les exemples React dans `src/` ou ouvrir issue.
