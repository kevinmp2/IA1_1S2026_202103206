@echo off
echo ================================
echo MediLogic - Backend Flask
echo ================================
echo.

cd backend

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo.
echo Iniciando backend Flask...
echo Backend estara disponible en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py

pause
