"""
Quimibond CFO Dashboard - Odoo Connector
Conexión a Odoo 18/19 via XML-RPC para extracción de datos financieros
"""

import xmlrpc.client
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from functools import lru_cache
import os

@dataclass
class OdooConfig:
    url: str
    db: str
    username: str
    password: str

class OdooConnector:
    """Conector robusto para Odoo con manejo de sesiones y cache"""
    
    def __init__(self, config: OdooConfig):
        self.config = config
        self.uid: Optional[int] = None
        self.common = None
        self.models = None
        self._connect()
    
    def _connect(self):
        """Establece conexión con Odoo"""
        self.common = xmlrpc.client.ServerProxy(f'{self.config.url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(
            self.config.db, 
            self.config.username, 
            self.config.password, 
            {}
        )
        if not self.uid:
            raise ConnectionError("Autenticación fallida con Odoo")
        self.models = xmlrpc.client.ServerProxy(f'{self.config.url}/xmlrpc/2/object')
    
    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """Ejecuta método en modelo de Odoo"""
        return self.models.execute_kw(
            self.config.db,
            self.uid,
            self.config.password,
            model,
            method,
            args,
            kwargs
        )
    
    def search_read(self, model: str, domain: List, fields: List[str], 
                    limit: int = None, order: str = None) -> List[Dict]:
        """Búsqueda optimizada con lectura"""
        kwargs = {'fields': fields}
        if limit:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order
        return self.execute(model, 'search_read', domain, **kwargs)
    
    def read_group(self, model: str, domain: List, fields: List[str], 
                   groupby: List[str], lazy: bool = False) -> List[Dict]:
        """Agrupación para reportes agregados"""
        return self.execute(model, 'read_group', domain, fields, groupby, lazy=lazy)


class FinancialDataExtractor:
    """Extractor de datos financieros específico para CFO Dashboard"""
    
    def __init__(self, connector: OdooConnector):
        self.odoo = connector
        self.current_year = datetime.now().year
        self.fiscal_year_start = f"{self.current_year}-01-01"
        self.fiscal_year_end = f"{self.current_year}-12-31"
    
    def set_fiscal_period(self, year: int, start_month: int = 1, end_month: int = 12):
        """Configura el período fiscal a analizar"""
        self.current_year = year
        self.fiscal_year_start = f"{year}-{start_month:02d}-01"
        last_day = 31 if end_month in [1,3,5,7,8,10,12] else 30 if end_month != 2 else 28
        self.fiscal_year_end = f"{year}-{end_month:02d}-{last_day}"
    
    # ==================== INGRESOS ====================
    
    def get_revenue_by_period(self, group_by: str = 'month') -> List[Dict]:
        """Obtiene ingresos agrupados por período"""
        domain = [
            ('date', '>=', self.fiscal_year_start),
            ('date', '<=', self.fiscal_year_end),
            ('account_id.code', '=like', '401%'),  # Cuentas de ingreso
            ('parent_state', '=', 'posted')
        ]
        
        groupby_field = 'date:month' if group_by == 'month' else 'date:quarter'
        
        result = self.odoo.read_group(
            'account.move.line',
            domain,
            ['credit:sum', 'debit:sum'],
            [groupby_field]
        )
        
        return [{
            'period': r[groupby_field],
            'revenue': r['credit'] - r['debit']
        } for r in result]
    
    def get_revenue_by_customer(self, limit: int = 20) -> List[Dict]:
        """Top clientes por ingresos"""
        domain = [
            ('date', '>=', self.fiscal_year_start),
            ('date', '<=', self.fiscal_year_end),
            ('account_id.code', '=like', '401%'),
            ('parent_state', '=', 'posted'),
            ('partner_id', '!=', False)
        ]
        
        result = self.odoo.read_group(
            'account.move.line',
            domain,
            ['partner_id', 'credit:sum', 'debit:sum'],
            ['partner_id'],
            lazy=False
        )
        
        customers = [{
            'customer_id': r['partner_id'][0] if r['partner_id'] else None,
            'customer_name': r['partner_id'][1] if r['partner_id'] else 'Sin cliente',
            'revenue': r['credit'] - r['debit'],
            'transaction_count': r['__count']
        } for r in result]
        
        # Ordenar y limitar
        customers.sort(key=lambda x: x['revenue'], reverse=True)
        return customers[:limit]
    
    def get_revenue_by_product_category(self) -> List[Dict]:
        """Ingresos por categoría de producto"""
        # Primero obtener las líneas de factura con productos
        invoices = self.odoo.search_read(
            'account.move',
            [
                ('invoice_date', '>=', self.fiscal_year_start),
                ('invoice_date', '<=', self.fiscal_year_end),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('state', '=', 'posted')
            ],
            ['id', 'partner_id', 'amount_total_signed']
        )
        
        invoice_ids = [inv['id'] for inv in invoices]
        
        if not invoice_ids:
            return []
        
        # Obtener líneas con categorías
        lines = self.odoo.search_read(
            'account.move.line',
            [
                ('move_id', 'in', invoice_ids),
                ('product_id', '!=', False),
                ('exclude_from_invoice_tab', '=', False)
            ],
            ['product_id', 'price_subtotal', 'quantity']
        )
        
        # Obtener categorías de productos
        product_ids = list(set(l['product_id'][0] for l in lines if l['product_id']))
        
        if not product_ids:
            return []
        
        products = self.odoo.search_read(
            'product.product',
            [('id', 'in', product_ids)],
            ['id', 'categ_id']
        )
        
        product_category = {p['id']: p['categ_id'][1] if p['categ_id'] else 'Sin categoría' 
                          for p in products}
        
        # Agregar por categoría
        category_revenue = {}
        for line in lines:
            if line['product_id']:
                cat = product_category.get(line['product_id'][0], 'Sin categoría')
                if cat not in category_revenue:
                    category_revenue[cat] = {'revenue': 0, 'quantity': 0}
                category_revenue[cat]['revenue'] += line['price_subtotal']
                category_revenue[cat]['quantity'] += line['quantity']
        
        return [{'category': k, **v} for k, v in category_revenue.items()]
    
    # ==================== COSTOS ====================
    
    def get_cost_of_sales(self) -> Dict:
        """Obtiene costo de ventas desglosado"""
        accounts_config = {
            'materia_prima': '501.01%',
            'mano_obra_directa': '501.06%',
            'gif': '504%',
            'depreciacion': '504.08%'
        }
        
        result = {}
        for name, account_pattern in accounts_config.items():
            domain = [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', account_pattern),
                ('parent_state', '=', 'posted')
            ]
            
            data = self.odoo.read_group(
                'account.move.line',
                domain,
                ['debit:sum', 'credit:sum'],
                []
            )
            
            if data:
                result[name] = data[0]['debit'] - data[0]['credit']
            else:
                result[name] = 0
        
        result['total'] = sum(result.values())
        return result
    
    def get_cost_breakdown_monthly(self) -> List[Dict]:
        """Desglose de costos por mes"""
        domain = [
            ('date', '>=', self.fiscal_year_start),
            ('date', '<=', self.fiscal_year_end),
            ('account_id.code', '=like', '5%'),  # Cuentas de costo
            ('parent_state', '=', 'posted')
        ]
        
        result = self.odoo.read_group(
            'account.move.line',
            domain,
            ['debit:sum', 'credit:sum'],
            ['date:month']
        )
        
        return [{
            'month': r['date:month'],
            'cost': r['debit'] - r['credit']
        } for r in result]
    
    # ==================== GASTOS OPERATIVOS ====================
    
    def get_operating_expenses(self) -> Dict:
        """Gastos operativos por categoría"""
        accounts_config = {
            'gastos_generales': '601%',
            'gastos_admin': '602%',
            'gastos_corporativos': '603%'
        }
        
        result = {}
        for name, account_pattern in accounts_config.items():
            domain = [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', account_pattern),
                ('parent_state', '=', 'posted')
            ]
            
            data = self.odoo.read_group(
                'account.move.line',
                domain,
                ['debit:sum', 'credit:sum'],
                []
            )
            
            if data:
                result[name] = data[0]['debit'] - data[0]['credit']
            else:
                result[name] = 0
        
        result['total'] = sum(result.values())
        return result
    
    # ==================== CUENTAS POR COBRAR ====================
    
    def get_accounts_receivable_aging(self) -> Dict:
        """Antigüedad de cuentas por cobrar"""
        today = datetime.now().date()
        
        # Obtener facturas pendientes
        invoices = self.odoo.search_read(
            'account.move',
            [
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial'])
            ],
            ['partner_id', 'amount_residual', 'invoice_date_due', 'invoice_date']
        )
        
        aging = {
            'current': 0,      # No vencido
            '1_30': 0,         # 1-30 días
            '31_60': 0,        # 31-60 días
            '61_90': 0,        # 61-90 días
            'over_90': 0       # Más de 90 días
        }
        
        details = []
        
        for inv in invoices:
            due_date = datetime.strptime(inv['invoice_date_due'], '%Y-%m-%d').date() if inv['invoice_date_due'] else today
            days_overdue = (today - due_date).days
            amount = inv['amount_residual']
            
            if days_overdue <= 0:
                aging['current'] += amount
            elif days_overdue <= 30:
                aging['1_30'] += amount
            elif days_overdue <= 60:
                aging['31_60'] += amount
            elif days_overdue <= 90:
                aging['61_90'] += amount
            else:
                aging['over_90'] += amount
            
            details.append({
                'partner': inv['partner_id'][1] if inv['partner_id'] else 'N/A',
                'amount': amount,
                'days_overdue': max(0, days_overdue)
            })
        
        aging['total'] = sum(aging.values())
        aging['details'] = sorted(details, key=lambda x: x['days_overdue'], reverse=True)[:20]
        
        return aging
    
    # ==================== CUENTAS POR PAGAR ====================
    
    def get_accounts_payable_summary(self) -> Dict:
        """Resumen de cuentas por pagar"""
        today = datetime.now().date()
        
        bills = self.odoo.search_read(
            'account.move',
            [
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial'])
            ],
            ['partner_id', 'amount_residual', 'invoice_date_due']
        )
        
        aging = {
            'current': 0,
            '1_30': 0,
            '31_60': 0,
            'over_60': 0
        }
        
        for bill in bills:
            due_date = datetime.strptime(bill['invoice_date_due'], '%Y-%m-%d').date() if bill['invoice_date_due'] else today
            days = (today - due_date).days
            amount = bill['amount_residual']
            
            if days <= 0:
                aging['current'] += amount
            elif days <= 30:
                aging['1_30'] += amount
            elif days <= 60:
                aging['31_60'] += amount
            else:
                aging['over_60'] += amount
        
        aging['total'] = sum(aging.values())
        return aging
    
    # ==================== INVENTARIOS ====================
    
    def get_inventory_valuation(self) -> Dict:
        """Valuación de inventarios"""
        try:
            # Obtener productos con stock (sin el campo 'value' que causa MemoryError)
            quants = self.odoo.search_read(
                'stock.quant',
                [
                    ('location_id.usage', '=', 'internal'),
                    ('quantity', '>', 0)
                ],
                ['product_id', 'quantity'],
                limit=10000  # Limitar para evitar problemas de memoria
            )
            
            total_qty = sum(q['quantity'] for q in quants)
            
            # Obtener productos para calcular valor usando costo estándar
            product_ids = list(set(q['product_id'][0] for q in quants if q['product_id']))
            
            total_value = 0
            by_category = {}
            
            if product_ids:
                # Obtener productos con costo estándar
                products = self.odoo.search_read(
                    'product.product',
                    [('id', 'in', product_ids)],
                    ['id', 'categ_id', 'standard_price']
                )
                
                product_data = {p['id']: {
                    'categ': p['categ_id'][1] if p['categ_id'] else 'Sin categoría',
                    'cost': p.get('standard_price', 0) or 0
                } for p in products}
                
                # Calcular valor total y por categoría
                for q in quants:
                    if q['product_id']:
                        product_id = q['product_id'][0]
                        prod_info = product_data.get(product_id, {'categ': 'Sin categoría', 'cost': 0})
                        quantity = q['quantity']
                        value = quantity * prod_info['cost']
                        
                        total_value += value
                        cat = prod_info['categ']
                        
                        if cat not in by_category:
                            by_category[cat] = {'value': 0, 'quantity': 0}
                        by_category[cat]['value'] += value
                        by_category[cat]['quantity'] += quantity
            
            return {
                'total_value': total_value,
                'total_quantity': total_qty,
                'by_category': by_category,
                'item_count': len(quants)
            }
        except Exception as e:
            # Si hay error, retornar valores por defecto
            print(f"Advertencia: Error al obtener inventario: {e}")
            return {
                'total_value': 0,
                'total_quantity': 0,
                'by_category': {},
                'item_count': 0
            }
    
    # ==================== MÉTRICAS CALCULADAS ====================
    
    def get_profit_and_loss_summary(self) -> Dict:
        """Estado de resultados resumido"""
        # Ingresos
        revenue_data = self.odoo.read_group(
            'account.move.line',
            [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', '4%'),
                ('parent_state', '=', 'posted')
            ],
            ['credit:sum', 'debit:sum'],
            []
        )
        revenue = revenue_data[0]['credit'] - revenue_data[0]['debit'] if revenue_data else 0
        
        # Costos
        cost_data = self.odoo.read_group(
            'account.move.line',
            [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', '5%'),
                ('parent_state', '=', 'posted')
            ],
            ['debit:sum', 'credit:sum'],
            []
        )
        cost = cost_data[0]['debit'] - cost_data[0]['credit'] if cost_data else 0
        
        # Gastos operativos
        opex_data = self.odoo.read_group(
            'account.move.line',
            [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', '6%'),
                ('parent_state', '=', 'posted')
            ],
            ['debit:sum', 'credit:sum'],
            []
        )
        opex = opex_data[0]['debit'] - opex_data[0]['credit'] if opex_data else 0
        
        # CIF
        cif_data = self.odoo.read_group(
            'account.move.line',
            [
                ('date', '>=', self.fiscal_year_start),
                ('date', '<=', self.fiscal_year_end),
                ('account_id.code', '=like', '7%'),
                ('parent_state', '=', 'posted')
            ],
            ['debit:sum', 'credit:sum'],
            []
        )
        cif = cif_data[0]['debit'] - cif_data[0]['credit'] if cif_data else 0
        
        gross_profit = revenue - cost
        operating_profit = gross_profit - opex
        net_income = operating_profit - cif
        
        return {
            'revenue': revenue,
            'cost_of_sales': cost,
            'gross_profit': gross_profit,
            'gross_margin': (gross_profit / revenue * 100) if revenue else 0,
            'operating_expenses': opex,
            'operating_profit': operating_profit,
            'operating_margin': (operating_profit / revenue * 100) if revenue else 0,
            'financial_costs': cif,
            'net_income': net_income,
            'net_margin': (net_income / revenue * 100) if revenue else 0
        }
    
    def get_kpis_dashboard(self) -> Dict:
        """KPIs principales para dashboard"""
        pnl = self.get_profit_and_loss_summary()
        ar = self.get_accounts_receivable_aging()
        ap = self.get_accounts_payable_summary()
        inventory = self.get_inventory_valuation()
        customers = self.get_revenue_by_customer(limit=10)
        
        # Calcular concentración
        total_revenue = pnl['revenue']
        top_customer_revenue = customers[0]['revenue'] if customers else 0
        top3_revenue = sum(c['revenue'] for c in customers[:3])
        
        # Calcular HHI
        hhi = sum((c['revenue']/total_revenue * 100)**2 for c in customers) if total_revenue else 0
        
        # Días de rotación (aproximados)
        daily_revenue = total_revenue / 365 if total_revenue else 1
        daily_cost = pnl['cost_of_sales'] / 365 if pnl['cost_of_sales'] else 1
        
        ar_days = ar['total'] / daily_revenue if daily_revenue else 0
        ap_days = ap['total'] / daily_cost if daily_cost else 0
        inventory_days = inventory['total_value'] / daily_cost if daily_cost else 0
        
        cash_cycle = ar_days + inventory_days - ap_days
        
        return {
            'financial': {
                'revenue': pnl['revenue'],
                'gross_margin': pnl['gross_margin'],
                'operating_margin': pnl['operating_margin'],
                'net_margin': pnl['net_margin'],
                'net_income': pnl['net_income']
            },
            'working_capital': {
                'ar_total': ar['total'],
                'ar_days': ar_days,
                'ap_total': ap['total'],
                'ap_days': ap_days,
                'inventory_value': inventory['total_value'],
                'inventory_days': inventory_days,
                'cash_conversion_cycle': cash_cycle
            },
            'concentration': {
                'top_customer_pct': (top_customer_revenue / total_revenue * 100) if total_revenue else 0,
                'top3_pct': (top3_revenue / total_revenue * 100) if total_revenue else 0,
                'hhi_index': hhi,
                'concentration_risk': 'ALTO' if hhi > 2500 else 'MEDIO' if hhi > 1500 else 'BAJO'
            },
            'alerts': self._generate_alerts(pnl, ar, ap, inventory, hhi)
        }
    
    def _generate_alerts(self, pnl, ar, ap, inventory, hhi) -> List[Dict]:
        """Genera alertas automáticas basadas en umbrales"""
        alerts = []
        
        # Margen bruto bajo
        if pnl['gross_margin'] < 25:
            alerts.append({
                'type': 'CRITICAL',
                'category': 'Rentabilidad',
                'message': f"Margen bruto crítico: {pnl['gross_margin']:.1f}% (umbral: 25%)",
                'impact': 'Revisar costos de producción urgente'
            })
        elif pnl['gross_margin'] < 30:
            alerts.append({
                'type': 'WARNING',
                'category': 'Rentabilidad',
                'message': f"Margen bruto bajo: {pnl['gross_margin']:.1f}% (objetivo: 30%)",
                'impact': 'Monitorear evolución de costos'
            })
        
        # CxC vencidas
        ar_overdue = ar['1_30'] + ar['31_60'] + ar['61_90'] + ar['over_90']
        if ar_overdue > ar['total'] * 0.3:
            alerts.append({
                'type': 'CRITICAL',
                'category': 'Cobranza',
                'message': f"CxC vencidas: ${ar_overdue:,.0f} ({ar_overdue/ar['total']*100:.0f}% del total)",
                'impact': 'Riesgo de liquidez - acelerar cobranza'
            })
        
        # Concentración de clientes
        if hhi > 2500:
            alerts.append({
                'type': 'WARNING',
                'category': 'Comercial',
                'message': f"Alta concentración de clientes (HHI: {hhi:.0f})",
                'impact': 'Diversificar cartera de clientes'
            })
        
        # CxP vencidas
        if ap['over_60'] > 0:
            alerts.append({
                'type': 'WARNING',
                'category': 'Tesorería',
                'message': f"CxP vencidas +60 días: ${ap['over_60']:,.0f}",
                'impact': 'Riesgo de relación con proveedores'
            })
        
        return alerts


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración (usar variables de entorno en producción)
    config = OdooConfig(
        url=os.getenv('ODOO_URL', 'http://localhost:8069'),
        db=os.getenv('ODOO_DB', 'quimibond'),
        username=os.getenv('ODOO_USER', 'admin'),
        password=os.getenv('ODOO_PASSWORD', 'admin')
    )
    
    try:
        connector = OdooConnector(config)
        extractor = FinancialDataExtractor(connector)
        
        # Obtener KPIs
        kpis = extractor.get_kpis_dashboard()
        print("KPIs obtenidos exitosamente")
        print(kpis)
        
    except Exception as e:
        print(f"Error: {e}")
