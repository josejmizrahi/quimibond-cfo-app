#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a Odoo y obtener algunos datos de prueba
"""

from odoo_connector import OdooConnector, OdooConfig, FinancialDataExtractor

def test_connection():
    """Prueba la conexión básica a Odoo"""
    print("🔌 Probando conexión a Odoo...")
    
    config = OdooConfig(
        url='http://quimibond.odoo.com',
        db='quimibond',
        username='jose.mizrahi@quimibond.com',
        password='1eab31ba65706701e5912ec026e40ca096d4fc99'
    )
    
    try:
        connector = OdooConnector(config)
        print(f"✅ Conexión exitosa! Usuario ID: {connector.uid}")
        
        # Probar una consulta simple
        company_count = connector.execute('res.company', 'search_count', [])
        print(f"✅ Empresas encontradas: {company_count}")
        
        # Probar el extractor
        print("\n📊 Probando extractor de datos financieros...")
        extractor = FinancialDataExtractor(connector)
        
        # Obtener KPIs
        print("📈 Obteniendo KPIs del dashboard...")
        kpis = extractor.get_kpis_dashboard()
        
        print("\n✅ KPIs obtenidos exitosamente:")
        print(f"  - Ingresos: ${kpis['financial']['revenue']:,.2f}")
        print(f"  - Margen Bruto: {kpis['financial']['gross_margin']:.2f}%")
        print(f"  - Utilidad Neta: ${kpis['financial']['net_income']:,.2f}")
        print(f"  - Ciclo de Caja: {kpis['working_capital']['cash_conversion_cycle']:.1f} días")
        print(f"  - Alertas: {len(kpis['alerts'])}")
        
        if kpis['alerts']:
            print("\n⚠️  Alertas encontradas:")
            for alert in kpis['alerts'][:3]:  # Mostrar solo las primeras 3
                print(f"  - [{alert['type']}] {alert['message']}")
        
        print("\n✅ Todas las pruebas pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()

