# Quimibond CFO Dashboard - Documentación de Arquitectura

## 📋 Resumen

Sistema de dashboard financiero en tiempo real que extrae datos de Odoo ERP y los presenta en una interfaz web moderna para el equipo de CFO.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USUARIO (CFO)                                │
│                              │                                       │
│                              ▼                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    LOVABLE FRONTEND                             │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │ │
│  │  │Dashboard │ │ Revenue  │ │  Costs   │ │   KPIs   │          │ │
│  │  │  Main    │ │ Analysis │ │ Analysis │ │ & Alerts │          │ │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │ │
│  │       │            │            │            │                 │ │
│  │       └────────────┴────────────┴────────────┘                 │ │
│  │                         │                                       │ │
│  │                    React Query                                  │ │
│  │                    (caching)                                    │ │
│  └─────────────────────────┬──────────────────────────────────────┘ │
│                            │ HTTPS                                   │
│                            ▼                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    FASTAPI BACKEND                              │ │
│  │  ┌──────────────────────────────────────────────────────────┐  │ │
│  │  │                     API Endpoints                         │  │ │
│  │  │  /dashboard/kpis  /revenue/*  /costs/*  /working-capital  │  │ │
│  │  └──────────────────────────┬───────────────────────────────┘  │ │
│  │                             │                                   │ │
│  │  ┌──────────────────────────▼───────────────────────────────┐  │ │
│  │  │              FinancialDataExtractor                       │  │ │
│  │  │   • get_revenue_by_customer()                            │  │ │
│  │  │   • get_profit_and_loss_summary()                        │  │ │
│  │  │   • get_accounts_receivable_aging()                      │  │ │
│  │  │   • get_kpis_dashboard()                                 │  │ │
│  │  └──────────────────────────┬───────────────────────────────┘  │ │
│  │                             │                                   │ │
│  │  ┌──────────────────────────▼───────────────────────────────┐  │ │
│  │  │                  OdooConnector                            │  │ │
│  │  │   • XML-RPC Connection                                   │  │ │
│  │  │   • Authentication                                       │  │ │
│  │  │   • Query execution                                      │  │ │
│  │  └──────────────────────────┬───────────────────────────────┘  │ │
│  └─────────────────────────────┬──────────────────────────────────┘ │
│                                │ XML-RPC                             │
│                                ▼                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                      ODOO 18/19                                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │ │
│  │  │   account   │ │    stock    │ │     sale    │              │ │
│  │  │  .move.line │ │   .quant    │ │   .order    │              │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘              │ │
│  │                                                                 │ │
│  │  ┌───────────────────────────────────────────────────────────┐ │ │
│  │  │                    PostgreSQL                              │ │ │
│  │  └───────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

```
quimibond-cfo-app/
├── backend/
│   ├── odoo_connector.py      # Conexión y extracción de Odoo
│   ├── main.py                # API FastAPI
│   ├── requirements.txt       # Dependencias Python
│   ├── Dockerfile            # Container para deploy
│   └── .env.example          # Variables de entorno
├── lovable-prompts/
│   └── PROMPT_DASHBOARD_CFO.md  # Prompt para generar frontend
├── docs/
│   └── ARCHITECTURE.md       # Este documento
└── docker-compose.yml        # Orquestación local
```

## 🔌 Endpoints de API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/dashboard/kpis` | KPIs principales |
| GET | `/api/dashboard/summary` | Resumen ejecutivo completo |
| GET | `/api/revenue/by-period` | Ingresos por período |
| GET | `/api/revenue/by-customer` | Ingresos por cliente |
| GET | `/api/revenue/by-category` | Ingresos por categoría |
| GET | `/api/costs/summary` | Resumen de costos |
| GET | `/api/costs/monthly` | Costos mensuales |
| GET | `/api/expenses/operating` | Gastos operativos |
| GET | `/api/working-capital/summary` | Capital de trabajo |
| GET | `/api/working-capital/receivables` | CxC con antigüedad |
| GET | `/api/working-capital/payables` | CxP |
| GET | `/api/working-capital/inventory` | Inventarios |
| GET | `/api/alerts` | Alertas activas |
| GET | `/api/analysis/year-over-year` | Comparativo YoY |

## 🗃️ Modelos de Odoo Utilizados

| Modelo | Uso |
|--------|-----|
| `account.move.line` | Movimientos contables |
| `account.move` | Facturas y asientos |
| `account.account` | Catálogo de cuentas |
| `res.partner` | Clientes y proveedores |
| `product.product` | Productos |
| `product.category` | Categorías |
| `stock.quant` | Inventarios |

## 🔐 Seguridad

### Recomendaciones para Producción:

1. **API Key**: Agregar autenticación por API key
2. **JWT**: Implementar tokens JWT para sesiones
3. **Rate Limiting**: Limitar requests por IP
4. **HTTPS**: Usar certificados SSL
5. **Odoo User**: Crear usuario con permisos mínimos necesarios

### Ejemplo de usuario Odoo recomendado:
```python
# Crear grupo de permisos en Odoo
# Acceso de solo lectura a:
# - account.move.line (read)
# - account.move (read)
# - res.partner (read)
# - product.product (read)
# - stock.quant (read)
```

## 🚀 Despliegue

### Opción 1: Docker Local
```bash
cd quimibond-cfo-app
docker-compose up -d
```

### Opción 2: Railway/Render
1. Crear servicio desde repositorio Git
2. Configurar variables de entorno
3. Deploy automático

### Opción 3: VPS
```bash
# En el servidor
pip install -r requirements.txt
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📊 Métricas Calculadas

### KPIs Financieros
- **Margen Bruto**: (Ingresos - CV) / Ingresos × 100
- **Margen Operativo**: (UB - GO) / Ingresos × 100
- **Margen Neto**: UN / Ingresos × 100

### KPIs de Capital de Trabajo
- **Días CxC**: CxC Total / (Ingresos / 365)
- **Días CxP**: CxP Total / (Costo / 365)
- **Días Inventario**: Inventario / (Costo / 365)
- **Ciclo de Caja**: Días CxC + Días Inv - Días CxP

### KPIs de Concentración
- **HHI**: Σ(participación%)²
- **Top N%**: Suma de top N clientes / Total

## ⚠️ Alertas Automáticas

| Condición | Tipo | Umbral |
|-----------|------|--------|
| Margen Bruto bajo | CRITICAL | < 25% |
| CxC vencidas | CRITICAL | > 30% del total |
| HHI alto | WARNING | > 2500 |
| CxP vencidas +60d | WARNING | > 0 |

## 🔄 Flujo de Datos

1. **Frontend** solicita datos via API
2. **Backend** valida request y parámetros
3. **OdooConnector** ejecuta queries XML-RPC
4. **Odoo** procesa y retorna datos
5. **FinancialDataExtractor** calcula métricas
6. **Backend** formatea respuesta JSON
7. **Frontend** renderiza visualizaciones

## 📈 Roadmap

### Fase 1 (MVP) ✅
- Dashboard principal
- KPIs básicos
- Concentración de clientes
- Alertas simples

### Fase 2
- Proyecciones y presupuestos
- Comparativos multi-período
- Export a Excel

### Fase 3
- Integración con presupuestos de Odoo
- Machine Learning para predicciones
- Notificaciones push
- App móvil

## 🐛 Troubleshooting

### Error de conexión a Odoo
```python
# Verificar:
# 1. URL correcta (incluir puerto)
# 2. Base de datos existe
# 3. Usuario y contraseña válidos
# 4. Firewall permite conexión
```

### Datos no actualizados
```python
# El caché tiene TTL de 5 minutos
# Forzar refresh: agregar ?force_refresh=true
```

### Performance lento
```python
# Opciones:
# 1. Aumentar cache TTL
# 2. Limitar períodos consultados
# 3. Agregar índices en PostgreSQL/Odoo
```

## 📞 Soporte

- **Documentación Odoo**: https://www.odoo.com/documentation
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Lovable Docs**: https://docs.lovable.dev
