from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ===== CUSTOM EXCEPTIONS =====

class IdeaValidatorError(Exception):
    """Base exception pour l'app"""
    pass


class ValidationError(IdeaValidatorError):
    """Erreur de validation"""
    pass


class OpportunityNotFoundError(IdeaValidatorError):
    """Opportunité non trouvée"""
    pass


class HardRuleViolationError(IdeaValidatorError):
    """Violation des hard rules du PRD"""
    pass


# ===== ERROR RESPONSES =====

class ErrorResponse:
    """Format standardisé des erreurs API"""
    
    def __init__(
        self,
        error: str,
        detail: str,
        code: Optional[str] = None,
        status_code: int = 400,
    ):
        self.error = error
        self.detail = detail
        self.code = code or error.lower().replace(" ", "_")
        self.status_code = status_code
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "detail": self.detail,
            "code": self.code,
        }
    
    def to_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail=self.to_dict()
        )


# ===== VALIDATORS =====

class OpportunityValidator:
    """Validateurs pour les opportunités"""
    
    @staticmethod
    def validate_hard_rules(
        evidence_count: int,
        paying_users_count: int,
        score_total: int,
    ) -> tuple[bool, Optional[str]]:
        """
        Vérifier les hard rules du PRD.
        
        Rules:
        - paying_users_count >= 10
        - score_total >= 40
        - evidence_count >= 5
        """
        
        if paying_users_count < 10:
            return False, "Pas assez de preuves de paiement (minimum 10 utilisateurs payants requis)"
        
        if score_total < 40:
            return False, "Score trop faible (minimum 40 requis)"
        
        if evidence_count < 5:
            return False, "Pas assez d'évidences (minimum 5 requis)"
        
        return True, None
    
    @staticmethod
    def validate_opportunity_exists(opportunity_id: str) -> bool:
        """Vérifier qu'une opportunité existe"""
        from mock_data import get_mock_opportunity_by_id
        return get_mock_opportunity_by_id(opportunity_id) is not None
    
    @staticmethod
    def validate_user_can_access_opportunity(
        user_id: str,
        opportunity_id: str,
    ) -> bool:
        """Vérifier que l'utilisateur peut accéder à cette opportunité"""
        # Pour MVP, tous les utilisateurs peuvent accéder
        # En production, implémenter des restrictions par persona
        return True


class TestValidator:
    """Validateurs pour les tests"""
    
    @staticmethod
    def validate_test_results(results: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Valider les résultats d'un test.
        
        Champs requis:
        - positive_responses (int >= 0)
        - total_outreach (int >= positive_responses)
        - precommits (int >= 0)
        - calls_booked (int >= 0)
        - conversion_rate (float 0-1, optional)
        """
        
        required_fields = ["positive_responses", "total_outreach", "precommits", "calls_booked"]
        
        for field in required_fields:
            if field not in results:
                return False, f"Champ requis manquant: {field}"
        
        positive_responses = results.get("positive_responses", 0)
        total_outreach = results.get("total_outreach", 0)
        
        if not isinstance(positive_responses, int) or positive_responses < 0:
            return False, "positive_responses doit être un entier >= 0"
        
        if not isinstance(total_outreach, int) or total_outreach < 0:
            return False, "total_outreach doit être un entier >= 0"
        
        if positive_responses > total_outreach:
            return False, "positive_responses ne peut pas être > total_outreach"
        
        conversion_rate = results.get("conversion_rate")
        if conversion_rate is not None:
            if not isinstance(conversion_rate, (int, float)) or not (0 <= conversion_rate <= 1):
                return False, "conversion_rate doit être entre 0 et 1"
        
        return True, None
    
    @staticmethod
    def auto_verdict(results: Dict[str, Any]) -> str:
        """
        Calculer le verdict automatiquement basé sur les résultats.
        
        Logique:
        - precommits >= 1 OR calls_booked >= 2 → CONTINUE
        - positive_responses >= 3 → ITERATE
        - Sinon → KILL
        """
        
        precommits = results.get("precommits", 0)
        calls_booked = results.get("calls_booked", 0)
        positive_responses = results.get("positive_responses", 0)
        
        if precommits >= 1 or calls_booked >= 2:
            return "continue"
        elif positive_responses >= 3:
            return "iterate"
        else:
            return "kill"


# ===== ERROR HANDLERS =====

def handle_validation_error(field: str, reason: str) -> HTTPException:
    """Handler pour erreurs de validation"""
    error = ErrorResponse(
        error="Validation Error",
        detail=f"{field}: {reason}",
        code="validation_error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    logger.warning(f"Validation error: {error.to_dict()}")
    return error.to_exception()


def handle_not_found_error(resource: str, resource_id: str) -> HTTPException:
    """Handler pour ressources non trouvées"""
    error = ErrorResponse(
        error="Not Found",
        detail=f"{resource} '{resource_id}' not found",
        code="not_found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    logger.warning(f"Not found: {error.to_dict()}")
    return error.to_exception()


def handle_hard_rule_violation(reason: str) -> HTTPException:
    """Handler pour violations des hard rules"""
    error = ErrorResponse(
        error="Hard Rule Violation",
        detail=reason,
        code="hard_rule_violation",
        status_code=status.HTTP_403_FORBIDDEN,
    )
    logger.warning(f"Hard rule violation: {error.to_dict()}")
    return error.to_exception()


def handle_unauthorized_error(reason: str = "Unauthorized") -> HTTPException:
    """Handler pour erreurs d'auth"""
    error = ErrorResponse(
        error="Unauthorized",
        detail=reason,
        code="unauthorized",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    logger.warning(f"Unauthorized: {error.to_dict()}")
    return error.to_exception()


def handle_server_error(error: Exception, context: str = "") -> HTTPException:
    """Handler pour erreurs serveur"""
    logger.error(f"Server error [{context}]: {str(error)}", exc_info=True)
    error_resp = ErrorResponse(
        error="Internal Server Error",
        detail="An unexpected error occurred. Please try again later.",
        code="server_error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    return error_resp.to_exception()


# ===== LOGGING HELPERS =====

def log_api_call(method: str, endpoint: str, user_id: Optional[str] = None):
    """Logger un appel API"""
    logger.info(f"API call: {method} {endpoint}" + (f" [user: {user_id}]" if user_id else ""))


def log_validation_failure(field: str, value: Any, reason: str):
    """Logger un échec de validation"""
    logger.warning(f"Validation failed: {field}={value} ({reason})")
