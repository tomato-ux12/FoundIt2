from fastapi import APIRouter, HTTPException, Query
from models import OpportunityListItem, GetOpportunitiesRequest, ScoreLevel
from mock_data import get_mock_opportunities, get_mock_opportunity_by_id
from services import ValidationFilter

router = APIRouter(prefix="/api/opportunities", tags=["opportunities"])


@router.get("/list")
async def list_opportunities(limit: int = Query(10, le=10, ge=1), offset: int = Query(0, ge=0)):
    """
    Retourner la liste des opportunités validées (max 10).
    
    Filtrage appliqué:
    - Hard rule: paying_users_count >= 10
    - Hard rule: score >= 40
    - Triées par Pain-to-Money Score (décroissant)
    """
    try:
        # Récupérer les mock opportunities
        opportunities = get_mock_opportunities(limit=20, offset=0)
        
        # Appliquer les filtres
        filtered = ValidationFilter.filter_opportunities(opportunities)
        
        # Trier par score
        filtered.sort(key=lambda x: x.score.total, reverse=True)
        
        # Limiter à 10 max et appliquer offset
        paginated = filtered[offset:offset + limit]
        
        # Converter en OpportunityListItem pour la liste
        items = [
            OpportunityListItem(
                id=opp.id,
                problem_statement=opp.problem_statement,
                score_total=opp.score.total,
                score_level=opp.score.level,
                evidence_count=opp.evidence_count,
                average_spend_eur_month=opp.average_spend_eur_month,
            )
            for opp in paginated
        ]
        
        return {
            "items": items,
            "total": len(filtered),
            "limit": limit,
            "offset": offset,
            "message": f"{len(items)} opportunités trouvées"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{opportunity_id}")
async def get_opportunity_detail(opportunity_id: str):
    """
    Récupérer le détail complet d'une opportunité.
    
    Inclus:
    - Problem statement
    - Pain-to-Money Score avec explication
    - Market Gap analysis
    - Revenue Blueprint
    - Validation plan
    """
    try:
        opportunity = get_mock_opportunity_by_id(opportunity_id)
        
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        # Vérifier que ça passe les hard rules
        should_display, reason = ValidationFilter.should_display(
            opportunity.evidence_count,
            opportunity.paying_users_count,
            opportunity.score.total
        )
        
        if not should_display:
            raise HTTPException(
                status_code=403,
                detail=f"Cette opportunité a été rejetée: {reason}"
            )
        
        return {
            "id": opportunity.id,
            "problem_statement": opportunity.problem_statement,
            "evidence_count": opportunity.evidence_count,
            "paying_users_count": opportunity.paying_users_count,
            "average_spend_eur_month": opportunity.average_spend_eur_month,
            "sources": opportunity.sources,
            "raw_quotes": opportunity.raw_quotes,
            "first_seen": opportunity.first_seen,
            "last_seen": opportunity.last_seen,
            "score": {
                "frequency": opportunity.score.frequency,
                "time_wasted": opportunity.score.time_wasted,
                "frustration": opportunity.score.frustration,
                "budget_signal": opportunity.score.budget_signal,
                "repeatability": opportunity.score.repeatability,
                "total": opportunity.score.total,
                "level": opportunity.score.level,
                "explanation": opportunity.score.explanation,
            },
            "market_gap": {
                "existing_tools": opportunity.market_gap.existing_tools,
                "angle": opportunity.market_gap.angle,
                "differentiation": opportunity.market_gap.differentiation,
                "confidence": opportunity.market_gap.confidence,
            },
            "blueprint": {
                "product_type": opportunity.blueprint.product_type,
                "pricing_range": opportunity.blueprint.pricing_range,
                "target_customer": opportunity.blueprint.target_customer,
                "acquisition_channels": opportunity.blueprint.acquisition_channels,
                "outreach_template": opportunity.blueprint.outreach_template,
                "build_cost": opportunity.blueprint.build_cost,
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{opportunity_id}/validation-plan")
async def get_validation_plan(opportunity_id: str):
    """
    Récupérer le plan de test 48h pour une opportunité.
    
    Inclus:
    - Landing page template
    - Outreach variants
    - Success metrics
    """
    try:
        from mock_data import get_mock_validation_plan
        
        opportunity = get_mock_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        plan = get_mock_validation_plan(opportunity_id)
        
        return {
            "opportunity_id": opportunity_id,
            "landing_page_headline": plan.landing_page_headline,
            "landing_page_subheading": plan.landing_page_subheading,
            "offer_type": plan.offer_type,
            "outreach_variants": plan.outreach_variants,
            "recommended_channel": plan.recommended_channel,
            "success_metrics": plan.success_metrics,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
