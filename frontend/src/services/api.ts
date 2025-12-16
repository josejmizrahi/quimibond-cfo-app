import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface KPIDashboard {
  financial: {
    revenue: number;
    gross_margin: number;
    operating_margin: number;
    net_margin: number;
    net_income: number;
  };
  working_capital: {
    ar_total: number;
    ar_days: number;
    ap_total: number;
    ap_days: number;
    inventory_value: number;
    inventory_days: number;
    cash_conversion_cycle: number;
  };
  concentration: {
    top_customer_pct: number;
    top3_pct: number;
    hhi_index: number;
    concentration_risk: string;
  };
  alerts: Array<{
    type: 'CRITICAL' | 'WARNING' | 'INFO';
    category: string;
    message: string;
    impact: string;
  }>;
  last_updated: string;
}

export interface CustomerRevenue {
  customer_name: string;
  revenue: number;
  percentage: number;
  cumulative_percentage: number;
  transaction_count: number;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  getKPIs: (year?: number) => 
    api.get<KPIDashboard>('/dashboard/kpis', { params: year ? { year } : {} }),
  
  getExecutiveSummary: (year?: number) =>
    api.get('/dashboard/summary', { params: year ? { year } : {} }),
  
  getRevenueByCustomer: (year?: number, limit: number = 20) =>
    api.get('/revenue/by-customer', { params: { year, limit } }),
  
  getRevenueByPeriod: (year?: number, groupBy: 'month' | 'quarter' = 'month') =>
    api.get('/revenue/by-period', { params: { year, group_by: groupBy } }),
  
  getWorkingCapitalSummary: (year?: number) =>
    api.get('/working-capital/summary', { params: year ? { year } : {} }),
  
  getAlerts: (year?: number, severity?: 'CRITICAL' | 'WARNING' | 'INFO') =>
    api.get('/alerts', { params: { year, severity } }),
  
  getYearOverYear: (currentYear?: number) =>
    api.get('/analysis/year-over-year', { params: currentYear ? { current_year: currentYear } : {} }),
  
  healthCheck: () => api.get('/health'),
};

export default api;

