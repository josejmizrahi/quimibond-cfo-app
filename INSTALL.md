# 🚀 Guía de Instalación - Quimibond CFO Dashboard

## Requisitos Previos

- Python 3.11 o superior
- Docker y Docker Compose (opcional, para ejecutar con Docker)
- Acceso a una instancia de Odoo 18/19 con credenciales válidas

## Opción 1: Instalación Local

### 1. Configurar Variables de Entorno

```bash
cd backend
cp env.example .env
```

Edita el archivo `.env` con tus credenciales de Odoo:

```env
ODOO_URL=http://localhost:8069
ODOO_DB=quimibond
ODOO_USER=admin
ODOO_PASSWORD=tu_password
```

### 2. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Servidor

**Opción A: Usando el script de inicio**
```bash
./start.sh
```

**Opción B: Manualmente**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Verificar que Funciona

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## Opción 2: Instalación con Docker

### 1. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto o configura las variables directamente en `docker-compose.yml`.

### 2. Construir y Ejecutar

```bash
docker-compose up -d
```

### 3. Ver Logs

```bash
docker-compose logs -f api
```

### 4. Detener

```bash
docker-compose down
```

## Verificación de Conexión

Para verificar que la conexión a Odoo funciona correctamente:

```bash
cd backend
python -c "from odoo_connector import OdooConnector, OdooConfig; import os; config = OdooConfig(url=os.getenv('ODOO_URL', 'http://localhost:8069'), db=os.getenv('ODOO_DB', 'quimibond'), username=os.getenv('ODOO_USER', 'admin'), password=os.getenv('ODOO_PASSWORD', 'admin')); conn = OdooConnector(config); print('✅ Conexión exitosa a Odoo')"
```

## Solución de Problemas

### Error: "Autenticación fallida con Odoo"
- Verifica que las credenciales en `.env` sean correctas
- Asegúrate de que la URL de Odoo sea accesible
- Verifica que la base de datos existe

### Error: "ModuleNotFoundError"
- Asegúrate de haber activado el entorno virtual
- Ejecuta `pip install -r requirements.txt` nuevamente

### Error: "Connection refused"
- Verifica que Odoo esté ejecutándose
- Si usas Docker, verifica que `host.docker.internal` funcione en tu sistema

### Puerto 8000 ya en uso
- Cambia el puerto en `docker-compose.yml` o en el comando uvicorn
- Ejemplo: `uvicorn main:app --port 8001`

## Próximos Pasos

1. Una vez que el backend esté funcionando, puedes crear el frontend usando Lovable
2. Usa el archivo `lovable-prompts/PROMPT_DASHBOARD_CFO.md` como guía
3. Configura la URL del API en el frontend: `http://localhost:8000/api`

## Desarrollo

Para desarrollo con hot-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Para ejecutar tests (cuando estén implementados):

```bash
pytest
```

