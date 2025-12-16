/**
 * Servicio de API para Quimibond CFO Dashboard
 * Conecta con el backend FastAPI en http://localhost:8000/api
 */

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

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  private async fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  // Dashboard KPIs
  async getKPIs(year?: number): Promise<KPIDashboard> {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI<KPIDashboard>(`/dashboard/kpis${params}`);
  }

  async getExecutiveSummary(year?: number) {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI(`/dashboard/summary${params}`);
  }

  // Revenue
  async getRevenueByCustomer(year?: number, limit: number = 20) {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    params.append('limit', limit.toString());
    return this.fetchAPI(`/revenue/by-customer?${params}`);
  }

  async getRevenueByPeriod(year?: number, groupBy: 'month' | 'quarter' = 'month') {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    params.append('group_by', groupBy);
    return this.fetchAPI(`/revenue/by-period?${params}`);
  }

  async getRevenueByCategory(year?: number) {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI(`/revenue/by-category${params}`);
  }

  // Costs
  async getCostsSummary(year?: number) {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI(`/costs/summary${params}`);
  }

  async getCostsMonthly(year?: number) {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI(`/costs/monthly${params}`);
  }

  // Working Capital
  async getWorkingCapitalSummary(year?: number) {
    const params = year ? `?year=${year}` : '';
    return this.fetchAPI(`/working-capital/summary${params}`);
  }

  async getReceivables() {
    return this.fetchAPI('/working-capital/receivables');
  }

  async getPayables() {
    return this.fetchAPI('/working-capital/payables');
  }

  async getInventory() {
    return this.fetchAPI('/working-capital/inventory');
  }

  // Alerts
  async getAlerts(year?: number, severity?: 'CRITICAL' | 'WARNING' | 'INFO') {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    if (severity) params.append('severity', severity);
    return this.fetchAPI(`/alerts?${params}`);
  }

  // Analysis
  async getYearOverYear(currentYear?: number) {
    const params = currentYear ? `?current_year=${currentYear}` : '';
    return this.fetchAPI(`/analysis/year-over-year${params}`);
  }

  // Health Check
  async healthCheck() {
    return this.fetchAPI('/health');
  }
}

export const apiService = new ApiService();
export default apiService;

