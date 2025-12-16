# 🔗 Configuración de GitHub

## ✅ Repositorio Git Inicializado

El proyecto ya está configurado con Git. Para subirlo a GitHub:

## 📤 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Crea un nuevo repositorio llamado `quimibond-cfo-app`
3. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)

### 2. Conectar el Repositorio Local con GitHub

```bash
cd /Users/jj/Desktop/quimibond-cfo-app

# Agregar el remote de GitHub
git remote add origin https://github.com/TU_USUARIO/quimibond-cfo-app.git

# O si prefieres SSH:
# git remote add origin git@github.com:TU_USUARIO/quimibond-cfo-app.git
```

### 3. Hacer el Primer Commit

```bash
git add .
git commit -m "Initial commit: Quimibond CFO Dashboard

- Backend FastAPI con conexión a Odoo
- Frontend React + TypeScript + shadcn/ui
- Dashboard con KPIs en tiempo real
- Sistema de alertas automáticas
- Análisis de capital de trabajo
- Componentes reutilizables"
```

### 4. Subir a GitHub

```bash
git push -u origin main
```

## 🔐 Configuración de Seguridad

### ⚠️ IMPORTANTE: Credenciales

Las credenciales de Odoo están en `backend/main.py`. Antes de hacer push:

**Opción 1: Usar Variables de Entorno (Recomendado)**

1. Mueve las credenciales a un archivo `.env` (ya está en .gitignore)
2. Actualiza `backend/main.py` para leer de variables de entorno
3. Crea `backend/.env.example` con valores de ejemplo

**Opción 2: Usar GitHub Secrets (Para CI/CD)**

1. Ve a Settings > Secrets en tu repositorio
2. Agrega:
   - `ODOO_URL`
   - `ODOO_DB`
   - `ODOO_USER`
   - `ODOO_PASSWORD`

## 📝 Comandos Útiles

### Ver estado
```bash
git status
```

### Agregar cambios
```bash
git add .
git commit -m "Descripción del cambio"
git push
```

### Ver historial
```bash
git log --oneline
```

### Crear una rama nueva
```bash
git checkout -b feature/nueva-funcionalidad
```

## 🚀 GitHub Actions

Ya está configurado un workflow básico en `.github/workflows/ci.yml` que:
- Verifica el backend (instala dependencias)
- Verifica el frontend (build)

Para activarlo, solo haz push a la rama `main` o `develop`.

## 📋 Checklist Antes de Push

- [ ] Verificar que `.env` esté en `.gitignore`
- [ ] Verificar que `venv/` esté en `.gitignore`
- [ ] Verificar que `node_modules/` esté en `.gitignore`
- [ ] Revisar que no haya credenciales hardcodeadas (excepto en .env)
- [ ] README.md actualizado
- [ ] Todos los archivos importantes agregados

## 🔄 Flujo de Trabajo Recomendado

1. **Desarrollo local**
   ```bash
   git checkout -b feature/mi-feature
   # Hacer cambios
   git add .
   git commit -m "Agregar feature X"
   ```

2. **Push a GitHub**
   ```bash
   git push origin feature/mi-feature
   ```

3. **Crear Pull Request en GitHub**
   - Ve a tu repositorio en GitHub
   - Crea un Pull Request desde tu rama
   - Revisa y mergea cuando esté listo

## 📚 Recursos

- [GitHub Docs](https://docs.github.com)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)

