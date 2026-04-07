from models import (
    OpportunityDetail, Evidence, ScoreBreakdown, MarketGap, 
    RevenueBlueprint, ScoreLevel, ValidationPlan
)
from datetime import datetime, timedelta
import uuid

# Mock opportunities pour freelances SEO
MOCK_OPPORTUNITIES = [
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Audit technique hebdomadaire automatisé pour freelances avec 5-20 clients",
        evidence_count=47,
        paying_users_count=38,
        average_spend_eur_month=129,
        sources=[
            "https://g2.com/products/ahrefs/reviews",
            "https://capterra.com/p/173929-Ahrefs/",
        ],
        raw_quotes=[
            "Ahrefs est trop cher pour un solo SEO, je paye 200€/mois juste pour audits hebdo",
            "Screaming Frog ne fait pas du monitoring continu, j'aurais besoin d'une solution qui tourne chaque semaine",
            "Je fais manuellement les audits pour 8 clients, ça me prend 15h/semaine",
        ],
        first_seen=datetime.now() - timedelta(days=90),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=92,
            time_wasted=88,
            frustration=85,
            budget_signal=95,
            repeatability=89,
            total=87,
            level=ScoreLevel.STRONG,
            explanation="Forte demande: 47 plaintes, 38 users payants. Temps perdu: 12-15h/semaine mentionnés. Budget: dépensent 100-300€/mois en alternatives. Très répétitif (toutes les semaines)."
        ),
        market_gap=MarketGap(
            existing_tools=[
                {
                    "name": "Ahrefs",
                    "limitation": "Coûte 200€/mois minimum, trop cher pour solo",
                    "evidence": "Reviews 1-2 stars: 'way overpriced for freelancers'"
                },
                {
                    "name": "Screaming Frog",
                    "limitation": "Pas de monitoring automatique continu",
                    "evidence": "Nécessite lancement manuel chaque semaine"
                },
                {
                    "name": "SEMrush",
                    "limitation": "Interface complexe, overkill pour audits simples",
                    "evidence": "Reviews: 'too many features, I only need basic audits'"
                },
            ],
            angle="Outil automatisé pour audits hebdomadaires, pricing solo-friendly (29€/mois), rapport blanc-label",
            differentiation=[
                "Pricing adapté freelances (29€ vs 200€ alternatives)",
                "Multi-client dashboard simple",
                "Rapports blanc-label PDF",
                "Intégration GSC/Ahrefs API existantes",
            ],
            confidence=0.85
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS web app + Chrome extension",
            pricing_range="29-49€/mois (solo), 79€/mois (pro 20+ clients)",
            target_customer="Freelance SEO avec 5-20 clients, <5k€/mois revenu",
            acquisition_channels=["Outreach clients existants", "Communities SEO (r/bigseo, Malt)"],
            outreach_template="""Salut [CLIENT],

Tu fais les audits techniques pour tes clients comment? 

Je test un outil automatisé qui fait les audits hebdo en 5min (vs les 2h que tu fais à la main).

Intéressé pour tester 7 jours gratuit?

[LINK]""",
            build_cost="medium"
        ),
    ),
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Monitoring multi-clients Google Search Console (positions, impressions, CTR)",
        evidence_count=38,
        paying_users_count=32,
        average_spend_eur_month=89,
        sources=[
            "https://g2.com/products/ahrefs/reviews",
            "https://capterra.com/p/211234-Semrush/",
        ],
        raw_quotes=[
            "Je check GSC manuellement chaque matin pour 6 clients, c'est 30min/jour de perdu",
            "Besoin d'une dashboard centralisée pour toutes mes positions clients, pas de truc gratuit vraiment utilisable",
            "Ahrefs coûte 200€ rien que pour tracker 6 sites",
        ],
        first_seen=datetime.now() - timedelta(days=60),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=82,
            time_wasted=79,
            frustration=78,
            budget_signal=85,
            repeatability=86,
            total=82,
            level=ScoreLevel.STRONG,
            explanation="Douleur quotidienne: 30min/jour pour 6 clients. 32 users payants cherchent solution. Budget: prêts à payer 89€/mois en moyenne."
        ),
        market_gap=MarketGap(
            existing_tools=[
                {
                    "name": "Ahrefs",
                    "limitation": "Trop cher (200€+)",
                    "evidence": "Reviews: 'way too expensive for tracking only'"
                },
                {
                    "name": "Google Search Console",
                    "limitation": "Pas de multi-account dashboard",
                    "evidence": "Limitation produit Google officielle"
                },
            ],
            angle="Dashboard centralisée GSC pour freelances, alertes positions, rapports PDF",
            differentiation=[
                "Multi-account en 1 clic",
                "Alertes drops de position",
                "Rapports PDF automatisés",
                "Pricing: 39€/mois pour 10 clients",
            ],
            confidence=0.78
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS web app",
            pricing_range="39-99€/mois selon clients trackés",
            target_customer="Freelance SEO avec 3-15 clients",
            acquisition_channels=["Direct à clients existants", "Slack communities SEO"],
            outreach_template="Salut, tu trackues combien de positions clients par jour? Je teste une dashboard GSC unifiée...",
            build_cost="medium"
        ),
    ),
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Rapports SEO white-label rapides (générer en 5min au lieu de 2h)",
        evidence_count=29,
        paying_users_count=24,
        average_spend_eur_month=64,
        sources=[
            "https://g2.com/products/semrush/reviews",
        ],
        raw_quotes=[
            "Je passe 2h à formatter des rapports Ahrefs/GSC en PDF custom pour chaque client",
            "Besoin d'outil qui génère rapport blanc-label automatiquement",
            "Je reporte à 5-6 clients par mois, 2h chacun = 10h perdues",
        ],
        first_seen=datetime.now() - timedelta(days=45),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=71,
            time_wasted=75,
            frustration=68,
            budget_signal=72,
            repeatability=79,
            total=73,
            level=ScoreLevel.DECENT,
            explanation="Douleur hebdomadaire mais moins universelle. 24 users payants. Temps: 2h/rapport × 5-6 rapports/mois."
        ),
        market_gap=MarketGap(
            existing_tools=[
                {
                    "name": "Ahrefs Reports",
                    "limitation": "Pas blanc-label, format fixe",
                    "evidence": "Pas de customisation visuelle"
                },
            ],
            angle="Générateur rapport blanc-label 5min, templates customisables",
            differentiation=[
                "Template builder drag-drop",
                "Export PDF + email auto-envoi",
                "Branding client intégré",
            ],
            confidence=0.68
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS web app",
            pricing_range="19-49€/mois",
            target_customer="Freelance SEO avec 5+ clients récurrents",
            acquisition_channels=["Direct clients", "Facebook groups SEO FR"],
            outreach_template="Combien de temps tu passes à formatter rapports pour tes clients?",
            build_cost="low"
        ),
    ),
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Checklist SEO technique automatisée pour audit initial (pas d'outil gratuit vraiment utilisable)",
        evidence_count=22,
        paying_users_count=18,
        average_spend_eur_month=54,
        sources=[
            "https://g2.com/products/screaming-frog/reviews",
        ],
        raw_quotes=[
            "Screaming Frog crawle et c'est tout, je dois formatter la checklist manuellement",
            "J'utilise un Notion template que j'ai créé, mais j'aimerais un outil dédié",
        ],
        first_seen=datetime.now() - timedelta(days=30),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=62,
            time_wasted=68,
            frustration=61,
            budget_signal=58,
            repeatability=72,
            total=64,
            level=ScoreLevel.DECENT,
            explanation="Signal modéré. Moins d'urgence (utilisent Notion workarounds). Mais 18 users payants potentiels."
        ),
        market_gap=MarketGap(
            existing_tools=[
                {
                    "name": "Screaming Frog",
                    "limitation": "Crawl seulement, pas de checklist",
                    "evidence": "Nécessite travail manuel post-crawl"
                },
            ],
            angle="Crawleur + checklist SEO auto-évaluation, rapport JSON/PDF",
            differentiation=[
                "Checklist intégrée pré-remplie",
                "Notation auto (bon/mauvais)",
            ],
            confidence=0.62
        ),
        blueprint=RevenueBlueprint(
            product_type="Python CLI + web app",
            pricing_range="9-29€/mois",
            target_customer="Freelance SEO débutant/junior",
            acquisition_channels=["YouTube tutos", "Communautés SEO"],
            outreach_template="Outil crawl + checklist en 5min, intéressé?",
            build_cost="low"
        ),
    ),
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Suivi automatique backlinks (alertes nouvelles/perdues) pour multi-clients",
        evidence_count=19,
        paying_users_count=15,
        average_spend_eur_month=76,
        sources=[
            "https://g2.com/products/moz/reviews",
        ],
        raw_quotes=[
            "J'ai besoin d'alertes si un client perd des backlinks, Ahrefs c'est trop pour juste ça",
            "Monitoring manuelle c'est 30min par semaine",
        ],
        first_seen=datetime.now() - timedelta(days=20),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=58,
            time_wasted=62,
            frustration=55,
            budget_signal=72,
            repeatability=68,
            total=63,
            level=ScoreLevel.DECENT,
            explanation="Signal décroissant mais segment clair (15 payants). Moins universel que audit/positions."
        ),
        market_gap=MarketGap(
            existing_tools=[
                {
                    "name": "Ahrefs",
                    "limitation": "Trop cher pour juste alertes backlinks",
                    "evidence": "Overkill pour ce usecase"
                },
            ],
            angle="Alertes backlinks minimalistes, slack/email intégré",
            differentiation=[
                "Pricing ultra-basique (19€/mois)",
                "Alertes Slack en temps réel",
            ],
            confidence=0.64
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS web app",
            pricing_range="19-39€/mois",
            target_customer="Freelance SEO avec 3-10 clients",
            acquisition_channels=["Direct clients", "Reddit r/SEO"],
            outreach_template="Besoin d'alertes backlinks pour tes clients?",
            build_cost="medium"
        ),
    ),
]

# Générer plus d'opportunités pour avoir 10 (mockées rapidement)
MOCK_OPPORTUNITIES.extend([
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Analyse compétiteur SEO (structure, keywords, backlinks) en bulk",
        evidence_count=16,
        paying_users_count=13,
        average_spend_eur_month=98,
        sources=["https://g2.com/products/semrush/reviews"],
        raw_quotes=["Trop long d'analyser chaque compétiteur manuellement"],
        first_seen=datetime.now() - timedelta(days=15),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=55, time_wasted=58, frustration=52,
            budget_signal=68, repeatability=61, total=59,
            level=ScoreLevel.WEAK,
            explanation="Signal faible. Cas d'usage moins fréquent. 13 payants seulement."
        ),
        market_gap=MarketGap(
            angle="Outil analyse compétiteurs en batch",
            confidence=0.58
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS app",
            pricing_range="29€/mois",
            target_customer="SEO avancé",
            acquisition_channels=["Communities"],
            outreach_template="Analyse compétiteurs rapide?",
            build_cost="high"
        ),
    ),
    OpportunityDetail(
        id=str(uuid.uuid4()),
        problem_statement="Gestion calendrier editorial contenu (publication, tracking)",
        evidence_count=12,
        paying_users_count=10,
        average_spend_eur_month=42,
        sources=["https://capterra.com/p/123456-Airtable/"],
        raw_quotes=["Notion c'est lent pour gérer 20 articles/mois"],
        first_seen=datetime.now() - timedelta(days=10),
        last_seen=datetime.now(),
        score=ScoreBreakdown(
            frequency=48, time_wasted=52, frustration=45,
            budget_signal=55, repeatability=58, total=52,
            level=ScoreLevel.WEAK,
            explanation="Signal très faible. Alternatives gratuites suffisent (Notion, Trello)."
        ),
        market_gap=MarketGap(
            angle="Editorial calendar simple SEO-focused",
            confidence=0.48
        ),
        blueprint=RevenueBlueprint(
            product_type="SaaS app",
            pricing_range="9€/mois",
            target_customer="SEO junior",
            acquisition_channels=["Twitter"],
            outreach_template="Editorial calendar?",
            build_cost="low"
        ),
    ),
])


def get_mock_opportunities(limit: int = 10, offset: int = 0):
    """Retourner les 10 meilleures opportunités triées par score"""
    sorted_opps = sorted(MOCK_OPPORTUNITIES, key=lambda x: x.score.total, reverse=True)
    return sorted_opps[offset:offset + limit]


def get_mock_opportunity_by_id(opportunity_id: str):
    """Récupérer une opportunité par ID"""
    for opp in MOCK_OPPORTUNITIES:
        if opp.id == opportunity_id:
            return opp
    return None


def get_mock_validation_plan(opportunity_id: str) -> ValidationPlan:
    """Générer un plan de test 48h pour une opportunité"""
    opp = get_mock_opportunity_by_id(opportunity_id)
    if not opp:
        return None
    
    return ValidationPlan(
        landing_page_headline=f"Automatisez: {opp.problem_statement.split('(')[0]}",
        landing_page_subheading=f"Économisez 10h/semaine. Test gratuit 7j.",
        offer_type="discovery_call",
        outreach_variants=[
            opp.blueprint.outreach_template,
            f"Salut, tu as 5min? Une question rapide sur ton workflow {opp.blueprint.target_customer.split('with')[1] if 'with' in opp.blueprint.target_customer else ''}...",
            f"Salut, {opp.problem_statement}. Intéressé tester une solution? (7j gratuit)",
        ],
        recommended_channel="existing_clients",
        success_metrics={
            "conversion_rate_target": 0.15,
            "positive_responses_target": 3,
            "calls_booked_target": 1,
            "precommits_target": 1,
        }
    )
