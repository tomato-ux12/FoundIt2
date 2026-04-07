/**
 * API Client Configuration
 * À utiliser côté frontend pour les appels au backend
 */

const API_BASE_URL = 
  process.env.VITE_API_URL || 
  (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://api.idea-validator.com');

export const API_ENDPOINTS = {
  // Auth
  auth: {
    register: '/api/auth/register',
    login: '/api/auth/login',
    user: (userId: string) => `/api/auth/user/${userId}`,
  },
  
  // Opportunities
  opportunities: {
    list: '/api/opportunities/list',
    detail: (opportunityId: string) => `/api/opportunities/${opportunityId}`,
    validationPlan: (opportunityId: string) => `/api/opportunities/${opportunityId}/validation-plan`,
  },
  
  // Tests
  tests: {
    create: '/api/tests/create',
    detail: (testId: string) => `/api/tests/${testId}`,
    submitVerdict: (testId: string) => `/api/tests/${testId}/submit-verdict`,
    userStats: (userId: string) => `/api/tests/user/${userId}/stats`,
    userHistory: (userId: string) => `/api/tests/user/${userId}/history`,
  },
};

/**
 * Wrapper fetch avec gestion d'erreurs
 */
export const fetchAPI = async (
  endpoint: string,
  options?: RequestInit
): Promise<any> => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
};

/**
 * Helper pour appels GET
 */
export const fetchGet = (endpoint: string) => 
  fetchAPI(endpoint, { method: 'GET' });

/**
 * Helper pour appels POST
 */
export const fetchPost = (endpoint: string, data: any) =>
  fetchAPI(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });

/**
 * Types pour le frontend
 */
export interface Opportunity {
  id: string;
  problem_statement: string;
  score_total: number;
  score_level: 'strong' | 'decent' | 'weak' | 'auto_kill';
  evidence_count: number;
  average_spend_eur_month: number;
}

export interface OpportunityDetail extends Opportunity {
  sources: string[];
  raw_quotes: string[];
  first_seen: string;
  last_seen: string;
  score: {
    frequency: number;
    time_wasted: number;
    frustration: number;
    budget_signal: number;
    repeatability: number;
    total: number;
    level: string;
    explanation: string;
  };
  market_gap: {
    existing_tools: any[];
    angle: string;
    differentiation: string[];
    confidence: number;
  };
  blueprint: {
    product_type: string;
    pricing_range: string;
    target_customer: string;
    acquisition_channels: string[];
    outreach_template: string;
    build_cost: string;
  };
}

export interface ValidationPlan {
  opportunity_id: string;
  landing_page_headline: string;
  landing_page_subheading: string;
  offer_type: string;
  outreach_variants: string[];
  recommended_channel: string;
  success_metrics: Record<string, any>;
}

export interface TestResult {
  conversion_rate?: number;
  positive_responses: number;
  total_outreach: number;
  precommits: number;
  calls_booked: number;
  notes?: string;
}

export interface Test {
  id: string;
  user_id: string;
  opportunity_id: string;
  started_at: string;
  completed_at?: string;
  verdict?: 'continue' | 'iterate' | 'kill';
  results?: TestResult;
}
