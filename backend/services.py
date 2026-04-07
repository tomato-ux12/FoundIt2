from models import ScoreBreakdown, ScoreLevel


class ScoringService:
    """Service pour calculer et expliquer les scores"""

    @staticmethod
    def calculate_score(breakdown: ScoreBreakdown) -> ScoreBreakdown:
        """
        Calculer le score total basé sur la formule du PRD:
        Score = (Frequency × 0.25)
              + (TimeWasted × 0.20)
              + (Frustration × 0.15)
              + (BudgetSignal × 0.25)
              + (Repeatability × 0.15)
        """
        total = int(
            (breakdown.frequency * 0.25)
            + (breakdown.time_wasted * 0.20)
            + (breakdown.frustration * 0.15)
            + (breakdown.budget_signal * 0.25)
            + (breakdown.repeatability * 0.15)
        )
        
        # Déterminer le level
        if total >= 80:
            level = ScoreLevel.STRONG
        elif total >= 60:
            level = ScoreLevel.DECENT
        elif total >= 40:
            level = ScoreLevel.WEAK
        else:
            level = ScoreLevel.AUTO_KILL
        
        breakdown.total = total
        breakdown.level = level
        return breakdown

    @staticmethod
    def generate_explanation(breakdown: ScoreBreakdown) -> str:
        """Générer une explication lisible du score"""
        
        if breakdown.level == ScoreLevel.STRONG:
            template = "Signal très fort: {frequency}% de fréquence, {time_wasted}% de temps perdu, budget signal {budget_signal}%."
        elif breakdown.level == ScoreLevel.DECENT:
            template = "Signal décent: {frequency}% de fréquence, {budget_signal}% de budget signal."
        elif breakdown.level == ScoreLevel.WEAK:
            template = "Signal faible: {frequency}% fréquence seulement, alternatives gratuites disponibles."
        else:
            template = "Pas assez de signal. Score auto-rejeté."
        
        return template.format(
            frequency=breakdown.frequency,
            time_wasted=breakdown.time_wasted,
            frustration=breakdown.frustration,
            budget_signal=breakdown.budget_signal,
            repeatability=breakdown.repeatability,
        )


class ValidationFilter:
    """Filtres de validation stricte (hard rules du PRD)"""

    @staticmethod
    def should_display(evidence_count: int, paying_users_count: int, score_total: int) -> tuple[bool, str]:
        """
        Déterminer si une opportunité doit être affichée.
        Hard rule: paying_users_count < 10 → rejet automatique
        """
        
        if paying_users_count < 10:
            return False, "Pas assez de preuves de paiement (< 10 utilisateurs payants)"
        
        if score_total < 40:
            return False, "Score trop faible (auto-kill)"
        
        if evidence_count < 5:
            return False, "Pas assez d'évidences"
        
        return True, "Passe les filtres"

    @staticmethod
    def filter_opportunities(opportunities: list) -> list:
        """Filtrer une liste d'opportunités selon les hard rules"""
        filtered = []
        for opp in opportunities:
            should_display, reason = ValidationFilter.should_display(
                opp.evidence_count,
                opp.paying_users_count,
                opp.score.total
            )
            if should_display:
                filtered.append(opp)
        
        return filtered
