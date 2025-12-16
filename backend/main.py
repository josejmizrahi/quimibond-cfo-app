"""
Quimibond CFO Dashboard - FastAPI Backend
API REST para consumo desde Lovable/React
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import os
from functools import lru_cache

from odoo_connector import OdooConnector, OdooConfig, FinancialDataExtractor

# ==================== CONFIGURACIÓN ====================

class Settings(BaseSettings):
    odoo_url: str = 'http://quimibond.odoo.com'
    odoo_db: str = 'quimibond'
    odoo_user: str = 'jose.mizrahi@quimibond.com'
    odoo_password: str = '1eab31ba65706701e5912ec026e40ca096d4fc99'
    cache_ttl: int = 300  # 5 minutos
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

# ==================== APP ====================

app = FastAPI(
    title="Quimibond CFO Dashboard API",
    description="API para análisis financiero en tiempo real desde Odoo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS para Lovable
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.lovable.app",
        "https://*.lovableproject.com",
        "*"  # En producción, especificar dominios exactos
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DEPENDENCIAS ====================

def get_odoo_extractor(settings: Settings = Depends(get_settings)) -> FinancialDataExtractor:
    """Dependency injection para el extractor de Odoo"""
    config = OdooConfig(
        url=settings.odoo_url,
        db=settings.odoo_db,
        username=settings.odoo_user,
        password=settings.odoo_password
    )
    connector = OdooConnector(config)
    return FinancialDataExtractor(connector)

# ==================== MODELOS ====================

class PeriodEnum(str, Enum):
    month = "month"
    quarter = "quarter"
    year = "year"

class AlertType(str, Enum):
    critical = "CRITICAL"
    warning = "WARNING"
    info = "INFO"

class FinancialSummary(BaseModel):
    revenue: float
    cost_of_sales: float
    gross_profit: float
    gross_margin: float
    operating_expenses: float
    operating_profit: float
    operating_margin: float
    financial_costs: float
    net_income: float
    net_margin: float

class CustomerConcentration(BaseModel):
    customer_name: str
    revenue: float
    percentage: float
    cumulative_percentage: float

class Alert(BaseModel):
    type: AlertType
    category: str
    message: str
    impact: str
    timestamp: datetime = None

class KPIDashboard(BaseModel):
    financial: Dict[str, float]
    working_capital: Dict[str, float]
    concentration: Dict[str, Any]
    alerts: List[Dict]
    last_updated: datetime

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Quimibond CFO Dashboard API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check(extractor: FinancialDataExtractor = Depends(get_odoo_extractor)):
    """Verifica conexión con Odoo"""
    try:
        # Intenta una consulta simple
        extractor.odoo.execute('res.company', 'search_count', [])
        return {"status": "connected", "odoo": "ok"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Odoo connection failed: {str(e)}")

# ==================== DASHBOARD PRINCIPAL ====================

@app.get("/api/dashboard/kpis", response_model=KPIDashboard)
async def get_dashboard_kpis(
    year: int = Query(default=None, description="Año fiscal"),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """
    Obtiene todos los KPIs principales para el dashboard CFO
    """
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        kpis = extractor.get_kpis_dashboard()
        kpis['last_updated'] = datetime.now()
        
        return kpis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/summary")
async def get_executive_summary(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """
    Resumen ejecutivo completo para CFO
    """
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        pnl = extractor.get_profit_and_loss_summary()
        customers = extractor.get_revenue_by_customer(limit=10)
        ar = extractor.get_accounts_receivable_aging()
        ap = extractor.get_accounts_payable_summary()
        inventory = extractor.get_inventory_valuation()
        
        # Calcular métricas adicionales
        total_revenue = pnl['revenue']
        
        return {
            "profit_and_loss": pnl,
            "top_customers": customers,
            "accounts_receivable": {
                "total": ar['total'],
                "aging": {k: v for k, v in ar.items() if k != 'details' and k != 'total'},
                "overdue_percentage": ((ar['1_30'] + ar['31_60'] + ar['61_90'] + ar['over_90']) / ar['total'] * 100) if ar['total'] else 0
            },
            "accounts_payable": ap,
            "inventory": {
                "total_value": inventory['total_value'],
                "item_count": inventory['item_count']
            },
            "concentration_metrics": {
                "top_customer_pct": (customers[0]['revenue'] / total_revenue * 100) if customers and total_revenue else 0,
                "top5_pct": (sum(c['revenue'] for c in customers[:5]) / total_revenue * 100) if customers and total_revenue else 0
            },
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== INGRESOS ====================

@app.get("/api/revenue/summary")
async def get_revenue_summary(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Resumen de ingresos"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        pnl = extractor.get_profit_and_loss_summary()
        return {
            "total_revenue": pnl['revenue'],
            "year": year or datetime.now().year
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/revenue/by-period")
async def get_revenue_by_period(
    year: int = Query(default=None),
    group_by: PeriodEnum = Query(default=PeriodEnum.month),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Ingresos agrupados por período"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        data = extractor.get_revenue_by_period(group_by=group_by.value)
        return {"data": data, "group_by": group_by.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/revenue/by-customer")
async def get_revenue_by_customer(
    year: int = Query(default=None),
    limit: int = Query(default=20, le=100),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Top clientes por ingresos con análisis de concentración"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        customers = extractor.get_revenue_by_customer(limit=limit)
        total = sum(c['revenue'] for c in customers)
        
        # Agregar porcentajes y acumulados
        cumulative = 0
        for c in customers:
            c['percentage'] = (c['revenue'] / total * 100) if total else 0
            cumulative += c['percentage']
            c['cumulative_percentage'] = cumulative
        
        # Calcular HHI
        hhi = sum((c['percentage'])**2 for c in customers)
        
        return {
            "customers": customers,
            "total_revenue": total,
            "concentration": {
                "hhi": hhi,
                "risk_level": "ALTO" if hhi > 2500 else "MEDIO" if hhi > 1500 else "BAJO",
                "top1_pct": customers[0]['percentage'] if customers else 0,
                "top3_pct": sum(c['percentage'] for c in customers[:3]),
                "top5_pct": sum(c['percentage'] for c in customers[:5])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/revenue/by-category")
async def get_revenue_by_category(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Ingresos por categoría de producto"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        data = extractor.get_revenue_by_product_category()
        total = sum(c['revenue'] for c in data)
        
        for c in data:
            c['percentage'] = (c['revenue'] / total * 100) if total else 0
        
        return {"categories": sorted(data, key=lambda x: x['revenue'], reverse=True), "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== COSTOS ====================

@app.get("/api/costs/summary")
async def get_costs_summary(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Resumen de costo de ventas"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        costs = extractor.get_cost_of_sales()
        pnl = extractor.get_profit_and_loss_summary()
        
        # Agregar porcentajes sobre ventas
        revenue = pnl['revenue']
        for key in costs:
            if key != 'total':
                costs[f'{key}_pct'] = (costs[key] / revenue * 100) if revenue else 0
        
        costs['cost_ratio'] = (costs['total'] / revenue * 100) if revenue else 0
        
        return costs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/costs/monthly")
async def get_costs_monthly(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Costos por mes"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        data = extractor.get_cost_breakdown_monthly()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== GASTOS OPERATIVOS ====================

@app.get("/api/expenses/operating")
async def get_operating_expenses(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Gastos operativos desglosados"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        expenses = extractor.get_operating_expenses()
        pnl = extractor.get_profit_and_loss_summary()
        
        revenue = pnl['revenue']
        for key in expenses:
            if key != 'total':
                expenses[f'{key}_pct'] = (expenses[key] / revenue * 100) if revenue else 0
        
        expenses['opex_ratio'] = (expenses['total'] / revenue * 100) if revenue else 0
        
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CAPITAL DE TRABAJO ====================

@app.get("/api/working-capital/receivables")
async def get_receivables(
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Cuentas por cobrar con antigüedad"""
    try:
        ar = extractor.get_accounts_receivable_aging()
        return ar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/working-capital/payables")
async def get_payables(
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Cuentas por pagar"""
    try:
        ap = extractor.get_accounts_payable_summary()
        return ap
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/working-capital/inventory")
async def get_inventory(
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Inventarios"""
    try:
        inv = extractor.get_inventory_valuation()
        return inv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/working-capital/summary")
async def get_working_capital_summary(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Resumen completo de capital de trabajo"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        ar = extractor.get_accounts_receivable_aging()
        ap = extractor.get_accounts_payable_summary()
        inv = extractor.get_inventory_valuation()
        pnl = extractor.get_profit_and_loss_summary()
        
        # Calcular días de rotación
        daily_revenue = pnl['revenue'] / 365 if pnl['revenue'] else 1
        daily_cost = pnl['cost_of_sales'] / 365 if pnl['cost_of_sales'] else 1
        
        ar_days = ar['total'] / daily_revenue
        ap_days = ap['total'] / daily_cost
        inv_days = inv['total_value'] / daily_cost
        
        cash_cycle = ar_days + inv_days - ap_days
        
        working_capital = ar['total'] + inv['total_value'] - ap['total']
        
        return {
            "accounts_receivable": {
                "total": ar['total'],
                "days": ar_days,
                "aging": {k: v for k, v in ar.items() if k not in ['details', 'total']}
            },
            "accounts_payable": {
                "total": ap['total'],
                "days": ap_days
            },
            "inventory": {
                "total": inv['total_value'],
                "days": inv_days,
                "items": inv['item_count']
            },
            "metrics": {
                "working_capital": working_capital,
                "cash_conversion_cycle": cash_cycle,
                "health": "BUENO" if cash_cycle < 45 else "REGULAR" if cash_cycle < 60 else "CRÍTICO"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ALERTAS ====================

@app.get("/api/alerts")
async def get_alerts(
    year: int = Query(default=None),
    severity: Optional[AlertType] = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Obtiene alertas activas del sistema"""
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        kpis = extractor.get_kpis_dashboard()
        alerts = kpis.get('alerts', [])
        
        # Filtrar por severidad si se especifica
        if severity:
            alerts = [a for a in alerts if a['type'] == severity.value]
        
        # Agregar timestamp
        for alert in alerts:
            alert['timestamp'] = datetime.now().isoformat()
        
        return {
            "alerts": alerts,
            "count": len(alerts),
            "critical_count": len([a for a in alerts if a['type'] == 'CRITICAL']),
            "warning_count": len([a for a in alerts if a['type'] == 'WARNING'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ANÁLISIS COMPARATIVO ====================

@app.get("/api/analysis/year-over-year")
async def get_yoy_analysis(
    current_year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Análisis año contra año"""
    try:
        current = current_year or datetime.now().year
        previous = current - 1
        
        # Datos año actual
        extractor.set_fiscal_period(current)
        current_pnl = extractor.get_profit_and_loss_summary()
        
        # Datos año anterior
        extractor.set_fiscal_period(previous)
        previous_pnl = extractor.get_profit_and_loss_summary()
        
        # Calcular variaciones
        def calc_variation(current_val, previous_val):
            if previous_val == 0:
                return None
            return ((current_val - previous_val) / abs(previous_val)) * 100
        
        comparison = {}
        for key in current_pnl:
            comparison[key] = {
                'current': current_pnl[key],
                'previous': previous_pnl[key],
                'variation': calc_variation(current_pnl[key], previous_pnl[key]),
                'absolute_change': current_pnl[key] - previous_pnl[key]
            }
        
        return {
            'current_year': current,
            'previous_year': previous,
            'comparison': comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== EXPORTACIÓN ====================

@app.get("/api/export/excel")
async def export_to_excel(
    year: int = Query(default=None),
    extractor: FinancialDataExtractor = Depends(get_odoo_extractor)
):
    """Exporta datos a Excel (retorna URL de descarga)"""
    # En producción, generar archivo y retornar URL
    # Por ahora retornamos los datos en JSON
    try:
        if year:
            extractor.set_fiscal_period(year)
        
        return {
            "message": "Función de exportación - implementar generación de Excel",
            "format": "xlsx",
            "year": year or datetime.now().year
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
