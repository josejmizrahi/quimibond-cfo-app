# 🚀 Instrucciones para Ejecutar Quimibond CFO Dashboard

## ⚡ Inicio Rápido (Recomendado)

### Opción 1: Script Automático

```bash
./start.sh
```

Este script iniciará automáticamente:
- ✅ Backend en http://localhost:8000
- ✅ Frontend en http://localhost:5173

**Para detener:** Presiona `Ctrl+C`

---

## 📋 Inicio Manual

### 1. Iniciar el Backend

**Terminal 1:**
```bash
cd backend
source venv/bin/activate  # O: . venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

El backend estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 2. Iniciar el Frontend

**Terminal 2:**
```bash
cd frontend
npm run dev
```

El frontend estará disponible en:
- **Aplicación**: http://localhost:5173

---

## 🔧 Si es la Primera Vez

### Backend (Primera vez)

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Primera vez)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

---

## ✅ Verificar que Todo Funciona

1. **Backend**: Abre http://localhost:8000/docs
   - Deberías ver la documentación interactiva de la API
   - Prueba el endpoint `/api/health`

2. **Frontend**: Abre http://localhost:5173
   - Deberías ver el Dashboard CFO
   - Los datos se cargarán automáticamente desde Odoo

---

## 🐛 Solución de Problemas

### Error: Puerto 8000 ya en uso
```bash
# Encontrar proceso
lsof -ti:8000

# Detener proceso
kill -9 $(lsof -ti:8000)
```

### Error: Puerto 5173 ya en uso
```bash
# Encontrar proceso
lsof -ti:5173

# Detener proceso
kill -9 $(lsof -ti:5173)
```

### Error: Módulo no encontrado (Backend)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Error: Dependencias no instaladas (Frontend)
```bash
cd frontend
npm install
```

### Error de Conexión a Odoo
- Verifica que las credenciales en `backend/main.py` sean correctas
- Verifica que Odoo esté accesible en `http://quimibond.odoo.com`

---

## 📊 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:5173 | Aplicación principal |
| Backend API | http://localhost:8000 | API REST |
| API Docs | http://localhost:8000/docs | Documentación interactiva |
| Health Check | http://localhost:8000/api/health | Verificar conexión |

---

## 🎯 Flujo de Trabajo

1. **Inicia el Backend primero** (necesario para que el frontend funcione)
2. **Luego inicia el Frontend**
3. **Abre el navegador** en http://localhost:5173
4. **¡Listo!** El dashboard se conectará automáticamente al backend

---

## 💡 Tips

- El backend tiene **hot-reload** activado (se actualiza automáticamente)
- El frontend tiene **hot-reload** activado (cambios se reflejan al instante)
- Los logs del backend aparecen en la terminal
- Los logs del frontend aparecen en la terminal

---

## 🛑 Detener los Servidores

### Si usaste el script automático:
- Presiona `Ctrl+C` en la terminal donde ejecutaste `./start.sh`

### Si iniciaste manualmente:
- En cada terminal, presiona `Ctrl+C`
- O usa: `pkill -f uvicorn` y `pkill -f vite`

---

## ✅ Checklist de Verificación

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 5173
- [ ] Health check responde: http://localhost:8000/api/health
- [ ] Dashboard carga datos: http://localhost:5173
- [ ] Sin errores en las consolas

¡Listo para usar! 🎉

