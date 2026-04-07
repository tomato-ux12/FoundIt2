import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchAPI, fetchGet, fetchPost, API_ENDPOINTS } from '@/lib/api';

// ===== AUTH HOOKS =====

export const useAuth = () => {
  const [userId, setUserId] = useState<string | null>(() => 
    typeof window !== 'undefined' ? localStorage.getItem('user_id') : null
  );

  const register = useMutation({
    mutationFn: (data: { email: string; freelance_type: string; years_experience: number }) =>
      fetchPost(API_ENDPOINTS.auth.register, data),
    onSuccess: (data) => {
      setUserId(data.user_id);
      localStorage.setItem('user_id', data.user_id);
    },
  });

  const login = useMutation({
    mutationFn: (email: string) =>
      fetchPost(API_ENDPOINTS.auth.login, { email }),
    onSuccess: (data) => {
      setUserId(data.user_id);
      localStorage.setItem('user_id', data.user_id);
    },
  });

  const logout = useCallback(() => {
    setUserId(null);
    localStorage.removeItem('user_id');
  }, []);

  return { userId, register, login, logout };
};

// ===== OPPORTUNITIES HOOKS =====

export const useOpportunities = (limit: number = 10, offset: number = 0) => {
  return useQuery({
    queryKey: ['opportunities', limit, offset],
    queryFn: () => fetchGet(
      `${API_ENDPOINTS.opportunities.list}?limit=${limit}&offset=${offset}`
    ),
  });
};

export const useOpportunityDetail = (opportunityId: string | null) => {
  return useQuery({
    queryKey: ['opportunity', opportunityId],
    queryFn: () => fetchGet(API_ENDPOINTS.opportunities.detail(opportunityId!)),
    enabled: !!opportunityId,
  });
};

export const useValidationPlan = (opportunityId: string | null) => {
  return useQuery({
    queryKey: ['validationPlan', opportunityId],
    queryFn: () => fetchGet(
      API_ENDPOINTS.opportunities.validationPlan(opportunityId!)
    ),
    enabled: !!opportunityId,
  });
};

// ===== TESTS HOOKS =====

export const useCreateTest = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (opportunityId: string) =>
      fetchPost(API_ENDPOINTS.tests.create, { opportunity_id: opportunityId }),
    onSuccess: () => {
      // Invalidate user tests
      queryClient.invalidateQueries({ queryKey: ['userTests'] });
    },
  });
};

export const useTest = (testId: string | null) => {
  return useQuery({
    queryKey: ['test', testId],
    queryFn: () => fetchGet(API_ENDPOINTS.tests.detail(testId!)),
    enabled: !!testId,
    refetchInterval: 10000, // Refresh every 10s while in progress
  });
};

export const useSubmitTestVerdict = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: {
      test_id: string;
      results: {
        conversion_rate?: number;
        positive_responses: number;
        total_outreach: number;
        precommits: number;
        calls_booked: number;
        notes?: string;
      };
    }) => fetchPost(API_ENDPOINTS.tests.submitVerdict(data.test_id), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userTests'] });
      queryClient.invalidateQueries({ queryKey: ['userStats'] });
    },
  });
};

export const useUserTestStats = (userId: string | null) => {
  return useQuery({
    queryKey: ['userStats', userId],
    queryFn: () => fetchGet(API_ENDPOINTS.tests.userStats(userId!)),
    enabled: !!userId,
  });
};

export const useUserTestHistory = (userId: string | null, limit: number = 10) => {
  return useQuery({
    queryKey: ['userTests', userId],
    queryFn: () => fetchGet(
      `${API_ENDPOINTS.tests.userHistory(userId!)}?limit=${limit}`
    ),
    enabled: !!userId,
  });
};

// ===== CUSTOM LOGIC HOOKS =====

/**
 * Hook pour gérer le flow complet: register → list → select → detail → test
 */
export const useIdeaValidationFlow = () => {
  const { userId, register } = useAuth();
  const [selectedOpportunityId, setSelectedOpportunityId] = useState<string | null>(null);
  const [testId, setTestId] = useState<string | null>(null);
  const [testVerdict, setTestVerdict] = useState<'continue' | 'iterate' | 'kill' | null>(null);

  const opportunities = useOpportunities();
  const selectedDetail = useOpportunityDetail(selectedOpportunityId);
  const validationPlan = useValidationPlan(selectedOpportunityId);
  const createTest = useCreateTest();
  const submitVerdict = useSubmitTestVerdict();

  const selectOpportunity = useCallback((id: string) => {
    setSelectedOpportunityId(id);
    setTestId(null);
    setTestVerdict(null);
  }, []);

  const startTest = useCallback(async () => {
    if (!selectedOpportunityId) return;
    
    try {
      const response = await createTest.mutateAsync(selectedOpportunityId);
      setTestId(response.test_id);
      // Store test_id in localStorage for reference
      localStorage.setItem('current_test_id', response.test_id);
    } catch (error) {
      console.error('Failed to create test:', error);
    }
  }, [selectedOpportunityId, createTest]);

  const submitTestResults = useCallback(async (results: any) => {
    if (!testId) return;
    
    try {
      const response = await submitVerdict.mutateAsync({
        test_id: testId,
        results,
      });
      setTestVerdict(response.verdict);
      localStorage.removeItem('current_test_id');
    } catch (error) {
      console.error('Failed to submit verdict:', error);
    }
  }, [testId, submitVerdict]);

  const resetFlow = useCallback(() => {
    setSelectedOpportunityId(null);
    setTestId(null);
    setTestVerdict(null);
  }, []);

  return {
    // State
    userId,
    selectedOpportunityId,
    testId,
    testVerdict,
    
    // Data
    opportunities,
    selectedDetail,
    validationPlan,
    
    // Mutations
    register,
    selectOpportunity,
    startTest,
    submitTestResults,
    resetFlow,
    
    // Loading states
    isLoadingOpportunities: opportunities.isLoading,
    isLoadingDetail: selectedDetail.isLoading,
    isCreatingTest: createTest.isPending,
    isSubmittingVerdict: submitVerdict.isPending,
  };
};

/**
 * Hook pour error handling global
 */
export const useApiError = (error: Error | null) => {
  if (!error) return null;

  // Parse error message
  const message = error.message || 'An error occurred';
  
  // Determine error type
  let type: 'error' | 'warning' | 'info' = 'error';
  
  if (message.includes('404')) {
    type = 'warning';
  } else if (message.includes('Network') || message.includes('Failed to fetch')) {
    type = 'error';
  }

  return { message, type };
};

/**
 * Hook pour caching et offline support (optional)
 */
export const useCachedQuery = <T,>(
  queryKey: string[],
  queryFn: () => Promise<T>,
  options?: any
) => {
  return useQuery({
    queryKey,
    queryFn,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    ...options,
  });
};
