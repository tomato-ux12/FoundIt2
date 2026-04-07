from supabase import create_client
from config import settings
from models import UserBase, TestRecord, TestVerdict
from datetime import datetime
import uuid

# Initialiser client Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


class Database:
    """Wrapper pour interactions Supabase"""

    @staticmethod
    def init_schema():
        """
        Créer les tables nécessaires. À appeler une fois.
        Pour MVP, on peut le faire manuellement dans Supabase dashboard.
        """
        # SQL à exécuter dans Supabase SQL editor:
        sql = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  freelance_type TEXT NOT NULL,
  years_experience INT NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- Tests table (tracking des tests 48h)
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

-- Index pour queries rapides
CREATE INDEX idx_tests_user_id ON tests(user_id);
CREATE INDEX idx_tests_opportunity_id ON tests(opportunity_id);
"""
        # Vous pouvez copier-coller ça dans Supabase SQL editor
        return sql

    @staticmethod
    def create_user(email: str, freelance_type: str, years_experience: int) -> dict:
        """Créer un nouvel utilisateur"""
        try:
            response = supabase.table("users").insert({
                "email": email,
                "freelance_type": freelance_type,
                "years_experience": years_experience,
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_user_by_email(email: str) -> dict:
        """Récupérer un utilisateur par email"""
        try:
            response = supabase.table("users").select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        """Récupérer un utilisateur par ID"""
        try:
            response = supabase.table("users").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    @staticmethod
    def create_test(user_id: str, opportunity_id: str) -> dict:
        """Créer un nouveau test 48h"""
        try:
            response = supabase.table("tests").insert({
                "user_id": user_id,
                "opportunity_id": opportunity_id,
                "started_at": datetime.now().isoformat(),
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating test: {e}")
            return None

    @staticmethod
    def get_test(test_id: str) -> dict:
        """Récupérer un test"""
        try:
            response = supabase.table("tests").select("*").eq("id", test_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching test: {e}")
            return None

    @staticmethod
    def update_test_verdict(test_id: str, verdict: str, results: dict) -> dict:
        """Enregistrer le verdict d'un test"""
        try:
            response = supabase.table("tests").update({
                "verdict": verdict,
                "conversion_rate": results.get("conversion_rate"),
                "positive_responses": results.get("positive_responses"),
                "total_outreach": results.get("total_outreach"),
                "precommits": results.get("precommits"),
                "calls_booked": results.get("calls_booked"),
                "notes": results.get("notes"),
                "completed_at": datetime.now().isoformat(),
            }).eq("id", test_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating test: {e}")
            return None

    @staticmethod
    def get_user_tests(user_id: str, limit: int = 10) -> list:
        """Récupérer les tests d'un utilisateur"""
        try:
            response = supabase.table("tests").select("*").eq("user_id", user_id).order(
                "started_at", desc=True
            ).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching user tests: {e}")
            return []

    @staticmethod
    def get_test_stats(user_id: str) -> dict:
        """Récupérer les stats des tests d'un utilisateur"""
        try:
            tests = Database.get_user_tests(user_id, limit=100)
            
            total_tests = len(tests)
            completed_tests = len([t for t in tests if t.get("verdict")])
            continue_verdicts = len([t for t in tests if t.get("verdict") == "continue"])
            iterate_verdicts = len([t for t in tests if t.get("verdict") == "iterate"])
            kill_verdicts = len([t for t in tests if t.get("verdict") == "kill"])
            
            return {
                "total_tests": total_tests,
                "completed_tests": completed_tests,
                "continue_count": continue_verdicts,
                "iterate_count": iterate_verdicts,
                "kill_count": kill_verdicts,
                "continue_rate": continue_verdicts / completed_tests if completed_tests > 0 else 0,
            }
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {}
