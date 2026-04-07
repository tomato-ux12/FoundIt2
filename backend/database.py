from typing import Optional, Dict, List
import uuid
from datetime import datetime

# In-memory database for MVP (no Supabase)
USERS_DB: Dict[str, Dict] = {}
TESTS_DB: Dict[str, Dict] = {}

class Database:
    """In-memory database for MVP testing"""
    
    def __init__(self):
        """Initialize in-memory database"""
        pass
    
    # ===== USER OPERATIONS =====
    
    async def create_user(self, email: str, freelance_type: str, years_experience: int):
        """Create or get user"""
        try:
            # Check if exists
            for user in USERS_DB.values():
                if user["email"] == email:
                    return user
            
            # Create new
            user_id = str(uuid.uuid4())
            user = {
                "id": user_id,
                "email": email,
                "freelance_type": freelance_type,
                "years_experience": years_experience,
                "created_at": datetime.now().isoformat(),
            }
            USERS_DB[user_id] = user
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    async def get_user(self, user_id: str):
        """Get user by ID"""
        try:
            return USERS_DB.get(user_id)
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    # ===== TEST OPERATIONS =====
    
    async def create_test(self, user_id: str, opportunity_id: str):
        """Create a new test"""
        try:
            test_id = str(uuid.uuid4())
            test = {
                "id": test_id,
                "user_id": user_id,
                "opportunity_id": opportunity_id,
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "verdict": None,
            }
            TESTS_DB[test_id] = test
            return test
        except Exception as e:
            print(f"Error creating test: {e}")
            return None
    
    async def get_test(self, test_id: str):
        """Get test by ID"""
        try:
            return TESTS_DB.get(test_id)
        except Exception as e:
            print(f"Error getting test: {e}")
            return None
    
    async def update_test_verdict(self, test_id: str, verdict: str, results: dict):
        """Update test with verdict"""
        try:
            if test_id in TESTS_DB:
                TESTS_DB[test_id].update({
                    "verdict": verdict,
                    "completed_at": datetime.now().isoformat(),
                    "positive_responses": results.get("positive_responses"),
                    "total_outreach": results.get("total_outreach"),
                    "precommits": results.get("precommits"),
                    "calls_booked": results.get("calls_booked"),
                    "conversion_rate": results.get("conversion_rate"),
                    "notes": results.get("notes"),
                })
                return TESTS_DB[test_id]
            return None
        except Exception as e:
            print(f"Error updating test: {e}")
            return None
    
    async def get_user_tests(self, user_id: str):
        """Get all tests for a user"""
        try:
            return [t for t in TESTS_DB.values() if t.get("user_id") == user_id]
        except Exception as e:
            print(f"Error getting user tests: {e}")
            return []
    
    async def get_test_stats(self, user_id: str):
        """Get test statistics for user"""
        try:
            tests = await self.get_user_tests(user_id)
            
            total = len(tests)
            continue_count = len([t for t in tests if t.get("verdict") == "continue"])
            iterate_count = len([t for t in tests if t.get("verdict") == "iterate"])
            kill_count = len([t for t in tests if t.get("verdict") == "kill"])
            
            return {
                "total_tests": total,
                "continue": continue_count,
                "iterate": iterate_count,
                "kill": kill_count,
                "continue_rate": continue_count / total if total > 0 else 0,
            }
        except Exception as e:
            print(f"Error getting test stats: {e}")
            return {}

# Initialize database
db = Database()