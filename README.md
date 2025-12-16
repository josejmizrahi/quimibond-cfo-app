# 📊 Quimibond CFO Dashboard

Dashboard financiero en tiempo real para el equipo de CFO de Quimibond, conectado directamente a Odoo ERP.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue)
![Odoo](https://img.shields.io/badge/Odoo-18%2F19-purple)

## 🎯 Características

- ✅ **KPIs en Tiempo Real** - Métricas financieras actualizadas desde Odoo
- ✅ **Análisis de Concentración** - Riesgo de cartera de clientes (HHI)
- ✅ **Capital de Trabajo** - CxC, CxP, Inventarios con antigüedad
- ✅ **Alertas Automáticas** - Notificaciones basadas en umbrales
- ✅ **Estado de Resultados** - P&L comparativo multi-año
- ✅ **API REST** - Consumible desde cualquier frontend
- ✅ **Frontend Moderno** - React + TypeScript + shadcn/ui

## 🚀 Quick Start

### Opción 1: Script Automático (Recomendado)

```bash
./start.sh
```

Esto iniciará automáticamente el backend y frontend.

### Opción 2: Manual

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📁 Estructura del Proyecto

```
quimibond-cfo-app/
├── backend/                    # API FastAPI
│   ├── main.py                # Endpoints REST
│   ├── odoo_connector.py      # Conexión a Odoo
│   ├── requirements.txt       # Dependencias Python
│   └── Dockerfile             # Container para deploy
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/        # Componentes reutilizables
│   │   ├── pages/             # Páginas
│   │   └── services/          # Servicios API
│   └── package.json
├── docs/                      # Documentación
│   └── ARCHITECTURE.md
├── docker-compose.yml         # Orquestación Docker
└── start.sh                   # Script de inicio
```

## 🔌 API Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/dashboard/kpis` | KPIs principales del dashboard |
| `GET /api/revenue/by-customer` | Ingresos por cliente |
| `GET /api/costs/summary` | Resumen de costos |
| `GET /api/working-capital/summary` | Capital de trabajo |
| `GET /api/alerts` | Alertas activas |

Ver documentación completa en `/docs` o `http://localhost:8000/docs`

## ⚙️ Configuración

### Backend

Las credenciales de Odoo están configuradas en `backend/main.py`:

```python
odo_url: str = 'http://quimibond.odoo.com'
odo_db: str = 'quimibond'
odo_user: str = 'jose.mizrahi@quimibond.com'
odo_password: str = '...'
```

### Frontend

El frontend se conecta automáticamente al backend en `http://localhost:8000/api`.

Para cambiar la URL, crea `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

## 📊 Métricas Incluidas

### Financieras
- Ingresos y márgenes (Bruto, Operativo, Neto)
- Estado de Resultados comparativo
- Análisis año contra año

### Capital de Trabajo
- Días de CxC, CxP, Inventario
- Ciclo de conversión de efectivo
- Antigüedad de cartera

### Concentración
- Top clientes por ingresos
- Índice HHI
- Análisis de riesgo

## 🛠️ Tecnologías

### Backend
- Python 3.11+
- FastAPI
- XML-RPC (Odoo)
- Pydantic

### Frontend
- React 19
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Recharts

## 📝 Desarrollo

### Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm run dev
```

## 🐳 Docker

```bash
docker-compose up -d
```

## 🔐 Seguridad

Para producción:
- [ ] Implementar autenticación JWT
- [ ] Usar HTTPS
- [ ] Crear usuario Odoo con permisos mínimos
- [ ] Configurar rate limiting
- [ ] Habilitar CORS específico

## 📄 Licencia

Propietario - Quimibond © 2025

## 👥 Equipo

- **Backend**: API FastAPI + Odoo Connector
- **Frontend**: React + TypeScript + shadcn/ui
- **Infraestructura**: Docker + Railway/Render

## 📚 Documentación Adicional

- [Instrucciones Detalladas](./INSTRUCCIONES.md)
- [Arquitectura](./docs/ARCHITECTURE.md)
- [Frontend Setup](./FRONTEND_SETUP.md)
