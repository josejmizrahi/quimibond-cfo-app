# ⚡ Inicio Rápido - Quimibond CFO Dashboard

## 🚀 Inicio en 3 Pasos

### 1. Configurar Variables de Entorno

```bash
cd backend
cp env.example .env
# Edita .env con tus credenciales de Odoo
```

### 2. Ejecutar con Docker (Recomendado)

```bash
docker-compose up -d
```

### 3. Verificar

Abre en tu navegador:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📋 O Sin Docker

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔗 Endpoints Principales

- `GET /api/dashboard/kpis` - KPIs principales
- `GET /api/revenue/by-customer` - Ingresos por cliente
- `GET /api/working-capital/summary` - Capital de trabajo
- `GET /api/alerts` - Alertas activas

## 📚 Más Información

Ver `INSTALL.md` para instrucciones detalladas.

