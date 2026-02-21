#!/bin/bash

echo "================================"
echo "MediLogic - Backend Flask"
echo "================================"
echo ""

cd backend

echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python no está instalado"
    exit 1
fi

python3 --version

echo ""
echo "Iniciando backend Flask..."
echo "Backend estará disponible en: http://localhost:5000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python3 app.py
