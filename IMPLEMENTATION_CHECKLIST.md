# 📋 Implementation Checklist & Development Notes

## ✅ Backend (COMPLETE)

### Core Features
- [x] FastAPI app setup
- [x] Pydantic models (all from PRD)
- [x] Supabase integration
- [x] Auth routes (stub)
- [x] Opportunities routes
- [x] Tests routes
- [x] Mock data (7 opportunities)
- [x] Hard rules validation
- [x] Scoring logic
- [x] Error handling
- [x] CORS middleware
- [x] API client (TypeScript)

### Testing
- [x] Health check tests
- [x] Auth tests
- [x] Opportunities tests
- [x] Tests endpoints tests
- [x] Integration tests
- [x] Edge case tests
- [x] 40+ unit tests

### Documentation
- [x] Backend README
- [x] API endpoints documented
- [x] Setup guide
- [x] Integration guide
- [x] Deployment guide

### DevOps
- [x] requirements.txt
- [x] .env.example
- [x] Dockerfile
- [x] docker-compose.yml
- [x] railway.toml
- [x] setup.sh script
- [x] .gitignore

---

## 🎯 Frontend (TO DO)

### Pages to Build

#### [1] Onboarding/Register
**Route:** `/register`

**Components:**
- [ ] Email input
- [ ] Freelance type selector (SEO only for MVP)
- [ ] Years of experience slider (1-10)
- [ ] Register button
- [ ] Error handling & validation

**Integration:**
- [ ] Use `useAuth()` hook
- [ ] Store user_id in localStorage
- [ ] Redirect to `/opportunities` on success

**UI Elements:**
- [ ] Logo/branding
- [ ] Form styling (shadcn/ui)
- [ ] Loading state
- [ ] Error toast (sonner)

---

#### [2] Opportunities List
**Route:** `/opportunities`

**Components:**
- [ ] Opportunities grid (max 10)
- [ ] Score badge with color coding:
  - 🟢 Strong (80-100)
  - 🟡 Decent (60-79)
  - 🟠 Weak (40-59)
- [ ] Problem statement
- [ ] Evidence count
- [ ] Average spend
- [ ] Click → Detail view
- [ ] Pagination (if > 10)

**Integration:**
- [ ] Use `useOpportunities()` hook
- [ ] Fetch on mount
- [ ] Display loading skeleton
- [ ] Handle empty state

**Sorting/Filtering:**
- [ ] Sort by score (default)
- [ ] Filter by level (optional Phase 2)
- [ ] Search by keyword (optional Phase 2)

---

#### [3] Opportunity Detail
**Route:** `/opportunities/{id}`

**Components (4 tabs):**

1. **Proof Tab**
   - [ ] Evidence count badge
   - [ ] Paying users count
   - [ ] Sources list (clickable links)
   - [ ] Raw quotes (testimonials)

2. **Score Tab**
   - [ ] Score breakdown (5 dimensions)
     - Frequency (0-100)
     - Time wasted (0-100)
     - Frustration (0-100)
     - Budget signal (0-100)
     - Repeatability (0-100)
   - [ ] Total score circle/gauge
   - [ ] Explanation text

3. **Market Gap Tab**
   - [ ] List of existing tools
   - [ ] Their limitations (1-2 sentences each)
   - [ ] Your angle (the differentiation)
   - [ ] Confidence % badge

4. **Blueprint Tab**
   - [ ] Product type (SaaS/Extension/CLI/etc)
   - [ ] Pricing range
   - [ ] Target customer description
   - [ ] Acquisition channels (max 2)
   - [ ] Estimated build cost (low/medium/high)
   - [ ] Copy "Validation plan" CTA

**Interactions:**
- [ ] "Start 48h test" button
- [ ] Copy scoring formula to clipboard
- [ ] Share opportunity (optional)

---

#### [4] Validation Plan Modal
**Trigger:** Click "Start 48h test"

**Components:**
- [ ] Landing page headline (copy-paste ready)
- [ ] Landing page subheading (copy-paste)
- [ ] Offer type badge (discovery call / waitlist / preorder)
- [ ] 3 Outreach variants (tabs or toggle)
- [ ] Recommended channel (existing clients > cold > paid)
- [ ] Success metrics (targets)
  - Conversion rate target
  - Positive responses target
  - Calls booked target
  - Precommits target

**Actions:**
- [ ] Copy each variant to clipboard
- [ ] Open Carrd/Framer in new tab (if setup)
- [ ] "Ready, start test" → Create test
- [ ] "Back" → Close modal

---

#### [5] Test Tracking
**Route:** `/test/{testId}` (optional, peut être modal)

**Components:**
- [ ] Test status
  - Created at
  - Time remaining (48h countdown)
  - Status: "In progress" / "Ready to submit"
- [ ] Instructions
  - Run test outside app
  - Submit results after 48h

**Interactions:**
- [ ] "I tested, here are my results" button
- [ ] Opens verdict submission form

---

#### [6] Verdict Submission Form
**Components:**
- [ ] Conversion rate slider (0-100%)
- [ ] Positive responses counter
- [ ] Total outreach counter
- [ ] Precommits counter
- [ ] Calls booked counter
- [ ] Notes textarea
- [ ] Submit button
- [ ] Auto-calculates verdict (logic in hook)

**Verdict Display:**
- [ ] 🟢 CONTINUE message
  - "Signal fort! Lance le MVP, tu as un marché."
  - Suggest next steps
- [ ] 🟡 ITERATE message
  - "Signal mitigé. Affine ton angle/prix/cible, puis reteste."
  - Show what changed
- [ ] ❌ KILL message
  - "Pas de signal. Archive cette idée, passe à la suivante."
  - Suggest browsing more opportunities

---

#### [7] Dashboard (optional Phase 2)
**Route:** `/dashboard`

**Components:**
- [ ] User profile card (email, freelance type, years)
- [ ] Tests stats
  - Total tests launched
  - CONTINUE rate
  - ITERATE rate
  - KILL rate
- [ ] Recent tests timeline
- [ ] Success stories (if any CONTINUEs)

---

### Hooks to Implement

Already created in `src/hooks/useApi.ts`:

- [x] `useAuth()` — Register/Login/Logout
- [x] `useOpportunities()` — List opportunities
- [x] `useOpportunityDetail()` — Get detail
- [x] `useValidationPlan()` — Get 48h plan
- [x] `useCreateTest()` — Create test
- [x] `useSubmitTestVerdict()` — Submit verdict
- [x] `useUserTestStats()` — Get stats
- [x] `useIdeaValidationFlow()` — Full flow orchestration

**Usage Example:**

```typescript
import { useIdeaValidationFlow } from '@/hooks/useApi';

export function OpportunitiesPage() {
  const {
    userId,
    selectedOpportunityId,
    opportunities,
    selectOpportunity,
    startTest,
    submitTestResults,
  } = useIdeaValidationFlow();

  return (
    <div>
      {opportunities.data?.items.map(opp => (
        <div key={opp.id} onClick={() => selectOpportunity(opp.id)}>
          {opp.problem_statement}
        </div>
      ))}
    </div>
  );
}
```

---

### Components to Create (shadcn/ui based)

- [ ] `OpportunityCard` — List item display
- [ ] `ScoreBreakdownViewer` — Score visualization
- [ ] `TabsComponent` — Proof/Score/Gap/Blueprint tabs
- [ ] `VerdictBadge` — CONTINUE/ITERATE/KILL badge
- [ ] `TestCountdown` — 48h timer
- [ ] `OutreachTemplateModal` — Variants display
- [ ] `ResultsForm` — Verdict submission
- [ ] `LoadingSkeletons` — Placeholders

---

### Frontend Routing

```
/                      → Landing (use existing)
/register              → Onboarding
/opportunities         → List (main app)
/opportunities/{id}    → Detail view
/test/{testId}        → Test tracking (optional)
/dashboard            → User stats (Phase 2)
```

---

## 🔧 Integration Points

### Step 1: Setup API client

```bash
cp backend/api-client.ts src/lib/api.ts
```

### Step 2: Create providers

```typescript
// src/providers/index.tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '@/context/AuthContext';

export function Providers({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        {children}
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

### Step 3: Update App routing

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Providers } from '@/providers';
import OnboardingPage from '@/pages/Onboarding';
import OpportunitiesPage from '@/pages/Opportunities';
import DetailPage from '@/pages/Detail';

function App() {
  return (
    <Providers>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/register" element={<OnboardingPage />} />
          <Route path="/opportunities" element={<OpportunitiesPage />} />
          <Route path="/opportunities/:id" element={<DetailPage />} />
        </Routes>
      </BrowserRouter>
    </Providers>
  );
}
```

### Step 4: Test integration

```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
npm run dev

# Open http://localhost:5173/register
# Should see form
```

---

## 🧪 Testing Checklist (Frontend)

- [ ] Register flow works
- [ ] Opportunities load
- [ ] Click opportunity → detail loads
- [ ] All 4 tabs display correctly
- [ ] Start test → modal appears
- [ ] Submit verdict → success message
- [ ] Error handling (network, invalid data)
- [ ] Mobile responsive
- [ ] Dark mode (if using next-themes)

---

## 🚀 Phase 2 Features (NOT MVP)

- [ ] Real G2/Capterra scraper
- [ ] Supabase Auth (JWT instead of localStorage)
- [ ] Stripe paywall
- [ ] Email magic link (production)
- [ ] Automatic test tracking (Carrd/Tally webhooks)
- [ ] Dashboard & user stats
- [ ] Extension SEO personas
- [ ] Reddit + Upwork sources
- [ ] ML scoring refinement
- [ ] Slack integration
- [ ] B2B deal flow (premium)

---

## 📝 Development Notes

### Scoring Formula (PRD)

```
Score = (Frequency × 0.25)
      + (TimeWasted × 0.20)
      + (Frustration × 0.15)
      + (BudgetSignal × 0.25)
      + (Repeatability × 0.15)
```

Each dimension: 0-100
Total: 0-100

Levels:
- 80-100: 🟢 Strong
- 60-79: 🟡 Decent
- 40-59: 🟠 Weak
- 0-39: ❌ Auto-reject

### Verdict Logic (PRD)

Auto-calculated on test submission:

```
if (precommits >= 1 OR calls_booked >= 2):
  verdict = CONTINUE
elif (positive_responses >= 3):
  verdict = ITERATE
else:
  verdict = KILL
```

---

## 🐛 Known Issues / Limitations

### MVP
- Auth is stub (localStorage only, no JWT)
- No real scraper (mock data)
- No email magic links
- No automatic test tracking
- No payment system

### Phase 2 Fixes
- Real Supabase Auth
- Full scraper pipeline
- Email verification
- Carrd/Tally webhook integration
- Stripe integration

---

## 📞 Questions?

See:
- `backend/README.md` — Backend docs
- `INTEGRATION_GUIDE.md` — Integration help
- `DEPLOYMENT_GUIDE.md` — Deployment help
- Code comments in routes + models

---

**Last updated:** April 2024  
**Status:** Ready for frontend implementation  
**Backend completeness:** 100%  
**Frontend completeness:** 0% (to be built)
