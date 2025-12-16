#!/bin/bash
# Script de inicio para Quimibond CFO Dashboard Backend

echo "🚀 Iniciando Quimibond CFO Dashboard API..."

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Creando desde env.example..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Archivo .env creado. Por favor, edítalo con tus credenciales de Odoo."
    else
        echo "❌ Archivo env.example no encontrado."
        exit 1
    fi
fi

# Verificar dependencias
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
else
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
fi

# Iniciar servidor
echo "🌐 Iniciando servidor FastAPI..."
echo "📍 API disponible en: http://localhost:8000"
echo "📚 Documentación en: http://localhost:8000/docs"
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

