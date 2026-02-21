#!/bin/bash

echo "================================"
echo "MediLogic - Frontend React"
echo "================================"
echo ""

cd frontend

echo "Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js no está instalado"
    exit 1
fi

node --version

echo ""
echo "Verificando dependencias..."
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias..."
    npm install
fi

echo ""
echo "Iniciando frontend React..."
echo "Frontend estará disponible en: http://localhost:3000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

npm run dev
