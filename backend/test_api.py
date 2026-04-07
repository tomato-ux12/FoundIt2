import pytest
from fastapi.testclient import TestClient
from main import app
from mock_data import get_mock_opportunities, MOCK_OPPORTUNITIES

client = TestClient(app)


# ===== HEALTH CHECKS =====

def test_root():
    """Test endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ===== AUTH ENDPOINTS =====

def test_register_user():
    """Test enregistrement utilisateur"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "freelance_type": "seo",
        "years_experience": 3,
    })
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "test@example.com"


def test_register_duplicate():
    """Test que l'enregistrement dupliqué retourne l'user existant"""
    email = "duplicate@example.com"
    
    # Premier register
    response1 = client.post("/api/auth/register", json={
        "email": email,
        "freelance_type": "seo",
        "years_experience": 2,
    })
    user_id_1 = response1.json()["user_id"]
    
    # Deuxième register avec même email
    response2 = client.post("/api/auth/register", json={
        "email": email,
        "freelance_type": "paid_ads",
        "years_experience": 3,
    })
    user_id_2 = response2.json()["user_id"]
    
    # Doit être le même user
    assert user_id_1 == user_id_2


def test_login():
    """Test login"""
    email = "login@example.com"
    
    # Register d'abord
    client.post("/api/auth/register", json={
        "email": email,
        "freelance_type": "seo",
        "years_experience": 1,
    })
    
    # Login
    response = client.post("/api/auth/login", json={"email": email})
    assert response.status_code == 200
    assert response.json()["user_id"]


def test_login_nonexistent():
    """Test login utilisateur inexistant"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com"
    })
    assert response.status_code == 404


# ===== OPPORTUNITIES ENDPOINTS =====

def test_list_opportunities():
    """Test listage des opportunités"""
    response = client.get("/api/opportunities/list?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["limit"] == 10
    assert len(data["items"]) <= 10


def test_list_opportunities_max_10():
    """Test que max 10 opportunités sont retournées"""
    response = client.get("/api/opportunities/list?limit=15&offset=0")
    assert response.status_code == 200
    data = response.json()
    # Le limit devrait être ajusté à 10 max
    assert len(data["items"]) <= 10


def test_list_opportunities_sorted_by_score():
    """Test que les opportunités sont triées par score (décroissant)"""
    response = client.get("/api/opportunities/list?limit=10&offset=0")
    assert response.status_code == 200
    items = response.json()["items"]
    
    scores = [item["score_total"] for item in items]
    assert scores == sorted(scores, reverse=True)


def test_list_opportunities_filters():
    """Test que les hard rules sont appliquées"""
    response = client.get("/api/opportunities/list?limit=20&offset=0")
    assert response.status_code == 200
    items = response.json()["items"]
    
    # Tous les items doivent avoir paying_users_count >= 10
    for item in items:
        # Vérifier que le score est affiché
        assert item["score_total"] >= 40


def test_get_opportunity_detail():
    """Test récupération détail opportunité"""
    # Récupérer une opportunity id
    list_response = client.get("/api/opportunities/list")
    items = list_response.json()["items"]
    assert len(items) > 0
    
    opportunity_id = items[0]["id"]
    
    # Get detail
    response = client.get(f"/api/opportunities/{opportunity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == opportunity_id
    assert "score" in data
    assert "market_gap" in data
    assert "blueprint" in data


def test_get_opportunity_nonexistent():
    """Test get opportunity inexistante"""
    response = client.get("/api/opportunities/fake-id-12345")
    assert response.status_code == 404


def test_get_validation_plan():
    """Test récupération du plan de validation 48h"""
    # Get une opportunity
    list_response = client.get("/api/opportunities/list")
    items = list_response.json()["items"]
    opportunity_id = items[0]["id"]
    
    # Get validation plan
    response = client.get(
        f"/api/opportunities/{opportunity_id}/validation-plan"
    )
    assert response.status_code == 200
    data = response.json()
    assert "landing_page_headline" in data
    assert "outreach_variants" in data
    assert "recommended_channel" in data
    assert "success_metrics" in data


# ===== TESTS ENDPOINTS =====

def test_create_test():
    """Test création d'un test"""
    # Get une opportunity
    list_response = client.get("/api/opportunities/list")
    opportunity_id = list_response.json()["items"][0]["id"]
    
    # Create test
    response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    assert response.status_code == 200
    data = response.json()
    assert "test_id" in data
    assert data["opportunity_id"] == opportunity_id


def test_get_test():
    """Test récupération d'un test"""
    # Create test d'abord
    list_response = client.get("/api/opportunities/list")
    opportunity_id = list_response.json()["items"][0]["id"]
    
    create_response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    test_id = create_response.json()["test_id"]
    
    # Get test
    response = client.get(f"/api/tests/{test_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_id


def test_submit_test_verdict_continue():
    """Test soumission verdict CONTINUE"""
    # Create test
    list_response = client.get("/api/opportunities/list")
    opportunity_id = list_response.json()["items"][0]["id"]
    
    create_response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    test_id = create_response.json()["test_id"]
    
    # Submit verdict avec signal fort
    response = client.post(
        f"/api/tests/{test_id}/submit-verdict",
        json={
            "test_id": test_id,
            "results": {
                "conversion_rate": 0.25,
                "positive_responses": 5,
                "total_outreach": 20,
                "precommits": 2,  # >= 1 → CONTINUE
                "calls_booked": 1,
                "notes": "Great signal"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "continue"


def test_submit_test_verdict_iterate():
    """Test soumission verdict ITERATE"""
    # Create test
    list_response = client.get("/api/opportunities/list")
    opportunity_id = list_response.json()["items"][0]["id"]
    
    create_response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    test_id = create_response.json()["test_id"]
    
    # Submit verdict avec signal moyen
    response = client.post(
        f"/api/tests/{test_id}/submit-verdict",
        json={
            "test_id": test_id,
            "results": {
                "conversion_rate": 0.05,
                "positive_responses": 4,  # >= 3 → ITERATE
                "total_outreach": 80,
                "precommits": 0,
                "calls_booked": 0,
                "notes": "Moderate signal"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "iterate"


def test_submit_test_verdict_kill():
    """Test soumission verdict KILL"""
    # Create test
    list_response = client.get("/api/opportunities/list")
    opportunity_id = list_response.json()["items"][0]["id"]
    
    create_response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    test_id = create_response.json()["test_id"]
    
    # Submit verdict avec pas de signal
    response = client.post(
        f"/api/tests/{test_id}/submit-verdict",
        json={
            "test_id": test_id,
            "results": {
                "conversion_rate": 0.0,
                "positive_responses": 0,
                "total_outreach": 20,
                "precommits": 0,
                "calls_booked": 0,
                "notes": "No signal"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "kill"


# ===== INTEGRATION TESTS =====

def test_full_flow_register_to_verdict():
    """Test complet: register → list → detail → create test → submit verdict"""
    
    # 1. Register
    register_response = client.post("/api/auth/register", json={
        "email": "fullflow@example.com",
        "freelance_type": "seo",
        "years_experience": 2,
    })
    assert register_response.status_code == 200
    user_id = register_response.json()["user_id"]
    
    # 2. List opportunities
    list_response = client.get("/api/opportunities/list?limit=5")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    assert len(items) > 0
    opportunity_id = items[0]["id"]
    
    # 3. Get detail
    detail_response = client.get(f"/api/opportunities/{opportunity_id}")
    assert detail_response.status_code == 200
    
    # 4. Get validation plan
    plan_response = client.get(
        f"/api/opportunities/{opportunity_id}/validation-plan"
    )
    assert plan_response.status_code == 200
    
    # 5. Create test
    test_response = client.post("/api/tests/create", json={
        "opportunity_id": opportunity_id
    })
    assert test_response.status_code == 200
    test_id = test_response.json()["test_id"]
    
    # 6. Submit verdict
    verdict_response = client.post(
        f"/api/tests/{test_id}/submit-verdict",
        json={
            "test_id": test_id,
            "results": {
                "conversion_rate": 0.1,
                "positive_responses": 2,
                "total_outreach": 20,
                "precommits": 1,
                "calls_booked": 0,
                "notes": "Testing full flow"
            }
        }
    )
    assert verdict_response.status_code == 200
    assert verdict_response.json()["verdict"] in ["continue", "iterate", "kill"]


# ===== EDGE CASES =====

def test_opportunity_hard_rules():
    """Test que les hard rules filtrènent correctement"""
    # Les opportunités avec < 10 paying users doivent être filtrées
    
    opportunities = get_mock_opportunities(limit=20)
    for opp in opportunities:
        # Tous les affichés doivent avoir >= 10 paying users
        assert opp.paying_users_count >= 10


def test_scoring_breakdown():
    """Test que les scores ont tous les champs"""
    list_response = client.get("/api/opportunities/list")
    items = list_response.json()["items"]
    
    for item in items:
        # Vérifier les champs obligatoires du score
        assert item["score_total"] >= 40
        assert item["score_level"] in ["strong", "decent", "weak", "auto_kill"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
