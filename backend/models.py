from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ===== ENUMS =====
class FreelanceType(str, Enum):
    SEO = "seo"
    PAID_ADS = "paid_ads"
    COPYWRITING = "copywriting"
    EMAIL = "email"
    CRM = "crm"


class TestVerdict(str, Enum):
    CONTINUE = "continue"
    ITERATE = "iterate"
    KILL = "kill"


class ScoreLevel(str, Enum):
    STRONG = "strong"  # 80-100
    DECENT = "decent"  # 60-79
    WEAK = "weak"  # 40-59
    AUTO_KILL = "auto_kill"  # 0-39


# ===== AUTH =====
class UserRegister(BaseModel):
    email: str
    freelance_type: FreelanceType
    years_experience: int = Field(ge=1)


class UserBase(BaseModel):
    id: str
    email: str
    freelance_type: FreelanceType
    years_experience: int
    created_at: datetime
    updated_at: datetime


class UserResponse(UserBase):
    pass


# ===== OPPORTUNITIES =====
class Evidence(BaseModel):
    id: str
    opportunity_id: str
    source_url: str
    quote: str
    paying_user: bool
    scraped_at: datetime


class ScoreBreakdown(BaseModel):
    frequency: int = Field(ge=0, le=100)
    time_wasted: int = Field(ge=0, le=100)
    frustration: int = Field(ge=0, le=100)
    budget_signal: int = Field(ge=0, le=100)
    repeatability: int = Field(ge=0, le=100)
    total: int = Field(ge=0, le=100)
    level: ScoreLevel
    explanation: str


class MarketGap(BaseModel):
    existing_tools: List[dict] = Field(default_factory=list)
    angle: str
    differentiation: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class RevenueBlueprint(BaseModel):
    product_type: str
    pricing_range: str
    target_customer: str
    acquisition_channels: List[str] = Field(default_factory=list)
    outreach_template: str
    build_cost: str  # low, medium, high


class OpportunityBase(BaseModel):
    problem_statement: str
    evidence_count: int
    paying_users_count: int
    average_spend_eur_month: float
    sources: List[str] = Field(default_factory=list)


class OpportunityDetail(OpportunityBase):
    id: str
    score: ScoreBreakdown
    market_gap: MarketGap
    blueprint: RevenueBlueprint
    first_seen: datetime
    last_seen: datetime
    raw_quotes: List[str] = Field(default_factory=list)


class OpportunityListItem(BaseModel):
    id: str
    problem_statement: str
    score_total: int
    score_level: ScoreLevel
    evidence_count: int
    average_spend_eur_month: float


# ===== VALIDATION ENGINE =====
class ValidationPlan(BaseModel):
    landing_page_headline: str
    landing_page_subheading: str
    offer_type: str  # pre-order, waitlist, discovery_call
    outreach_variants: List[str] = Field(default_factory=list)
    recommended_channel: str
    success_metrics: dict


class TestResult(BaseModel):
    conversion_rate: Optional[float] = None
    positive_responses: int
    total_outreach: int
    precommits: int
    calls_booked: int
    notes: str = ""


class TestRecord(BaseModel):
    id: str
    user_id: str
    opportunity_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[TestResult] = None
    verdict: Optional[TestVerdict] = None


# ===== API REQUESTS =====
class GetOpportunitiesRequest(BaseModel):
    limit: int = Field(default=10, le=10, ge=1)
    offset: int = Field(default=0, ge=0)


class CreateTestRequest(BaseModel):
    opportunity_id: str


class SubmitTestResultRequest(BaseModel):
    test_id: str
    results: TestResult
