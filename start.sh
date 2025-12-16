#!/bin/bash
# Script para iniciar Backend y Frontend de Quimibond CFO Dashboard

echo "🚀 Iniciando Quimibond CFO Dashboard..."
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar si un puerto está en uso
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Verificar puertos
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Puerto 8000 ya está en uso (Backend)${NC}"
else
    echo -e "${BLUE}📦 Iniciando Backend...${NC}"
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt
    echo -e "${GREEN}✅ Backend iniciado en http://localhost:8000${NC}"
    echo -e "${GREEN}   📚 Documentación: http://localhost:8000/docs${NC}"
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /tmp/quimibond-backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    sleep 2
fi

if check_port 5173; then
    echo -e "${YELLOW}⚠️  Puerto 5173 ya está en uso (Frontend)${NC}"
else
    echo -e "${BLUE}🎨 Iniciando Frontend...${NC}"
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "Instalando dependencias del frontend..."
        npm install
    fi
    echo -e "${GREEN}✅ Frontend iniciado en http://localhost:5173${NC}"
    npm run dev > /tmp/quimibond-frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    sleep 2
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Quimibond CFO Dashboard está corriendo!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📍 URLs:${NC}"
echo -e "   Frontend: ${GREEN}http://localhost:5173${NC}"
echo -e "   Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "   API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}💡 Para detener los servidores, presiona Ctrl+C${NC}"
echo ""

# Esperar a que el usuario presione Ctrl+C
trap "echo ''; echo '🛑 Deteniendo servidores...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Mantener el script corriendo
wait

