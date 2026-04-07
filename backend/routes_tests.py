from fastapi import APIRouter, HTTPException
from models import CreateTestRequest, SubmitTestResultRequest, TestVerdict
from database import Database
from datetime import datetime

router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.post("/create")
async def create_test(request: CreateTestRequest):
    """
    Créer un nouveau test 48h pour une opportunité.
    
    Nécessite:
    - user_id (header Authorization)
    - opportunity_id
    """
    try:
        # TODO: Vérifier le user_id depuis le JWT/session
        # Pour MVP, on le prend du body ou on le fakerise
        
        # Créer le test dans la DB
        test = Database.create_test(
            user_id="test-user-123",  # TODO: remplacer par user_id du JWT
            opportunity_id=request.opportunity_id
        )
        
        if not test:
            raise HTTPException(status_code=500, detail="Failed to create test")
        
        return {
            "test_id": test["id"],
            "opportunity_id": request.opportunity_id,
            "started_at": test["started_at"],
            "message": "Test créé, tu as 48h pour tester!"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{test_id}")
async def get_test(test_id: str):
    """Récupérer le détail d'un test"""
    try:
        test = Database.get_test(test_id)
        
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        
        return {
            "id": test["id"],
            "user_id": test["user_id"],
            "opportunity_id": test["opportunity_id"],
            "started_at": test["started_at"],
            "completed_at": test.get("completed_at"),
            "verdict": test.get("verdict"),
            "results": {
                "conversion_rate": test.get("conversion_rate"),
                "positive_responses": test.get("positive_responses"),
                "total_outreach": test.get("total_outreach"),
                "precommits": test.get("precommits"),
                "calls_booked": test.get("calls_booked"),
                "notes": test.get("notes"),
            } if test.get("verdict") else None,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{test_id}/submit-verdict")
async def submit_test_verdict(test_id: str, request: SubmitTestResultRequest):
    """
    Soumettre le verdict d'un test après 48h.
    
    Verdict options: CONTINUE | ITERATE | KILL
    """
    try:
        # Vérifier que le test existe
        test = Database.get_test(test_id)
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        
        # Calculer le verdict automatiquement ou le prendre du body
        # Pour MVP, on force l'utilisateur à saisir les résultats
        
        results = request.results.dict()
        
        # Auto-verdict basé sur les metrics
        conversion_rate = results.get("conversion_rate", 0)
        positive_responses = results.get("positive_responses", 0)
        precommits = results.get("precommits", 0)
        calls_booked = results.get("calls_booked", 0)
        
        # Logique simple:
        # - Si ≥1 precommit ou ≥2 appels: CONTINUE
        # - Si ≥3 réponses positives: ITERATE
        # - Sinon: KILL
        
        if precommits >= 1 or calls_booked >= 2:
            verdict = TestVerdict.CONTINUE
        elif positive_responses >= 3:
            verdict = TestVerdict.ITERATE
        else:
            verdict = TestVerdict.KILL
        
        # Enregistrer le verdict en DB
        updated_test = Database.update_test_verdict(
            test_id,
            verdict.value,
            results
        )
        
        if not updated_test:
            raise HTTPException(status_code=500, detail="Failed to submit verdict")
        
        return {
            "test_id": test_id,
            "verdict": verdict.value,
            "message": get_verdict_message(verdict),
            "results": results,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}/stats")
async def get_user_test_stats(user_id: str):
    """
    Récupérer les stats de l'utilisateur:
    - Nombre de tests lancés
    - Nombre de verdicts CONTINUE / ITERATE / KILL
    - Taux de succès
    """
    try:
        stats = Database.get_test_stats(user_id)
        
        return {
            "user_id": user_id,
            "stats": stats,
            "message": f"{stats.get('total_tests', 0)} tests lancés"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}/history")
async def get_user_test_history(user_id: str, limit: int = 10):
    """Récupérer l'historique des tests d'un utilisateur"""
    try:
        tests = Database.get_user_tests(user_id, limit=limit)
        
        return {
            "user_id": user_id,
            "tests": tests,
            "total": len(tests),
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_verdict_message(verdict: TestVerdict) -> str:
    """Retourner un message motivant selon le verdict"""
    messages = {
        TestVerdict.CONTINUE: "🟢 Signal fort! Lance le MVP, tu as un marché.",
        TestVerdict.ITERATE: "🟡 Signal mitigé. Affine ton angle/prix/cible, puis reteste.",
        TestVerdict.KILL: "❌ Pas de signal. Archive cette idée, passe à la suivante."
    }
    return messages.get(verdict, "Test enregistré")
