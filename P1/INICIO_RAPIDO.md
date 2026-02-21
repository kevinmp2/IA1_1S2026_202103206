# MediLogic - Inicio Rápido

## 🚀 Ejecutar en 3 Pasos

### 1️⃣ Instalar Dependencias

**Backend:**
```bash
cd P1
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Frontend:**
```bash
cd P1/frontend
npm install
```

### 2️⃣ Iniciar Servidores

**Terminal 1 - Backend:**
```bash
cd P1/backend
python app.py
```
✅ Backend: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd P1/frontend
npm run dev
```
✅ Frontend: http://localhost:3000

### 3️⃣ Usar la Aplicación

Abrir navegador en: **http://localhost:3000**

#### Credenciales de Administrador:
- Usuario: `admin` | Contraseña: `admin123`
- Usuario: `medico` | Contraseña: `medico123`

## 📋 Requisitos Previos

- ✅ Python 3.8+
- ✅ Node.js 18+
- ✅ SWI-Prolog (descargar de https://www.swi-prolog.org/download/stable)

## 🔧 Solución de Problemas

### Error: "pyswip not found"
```bash
pip install pyswip
```

### Error: "SWI-Prolog not installed"
Instalar SWI-Prolog desde el sitio oficial y reiniciar terminal.

### Error al conectar frontend con backend
Verificar que ambos servidores estén corriendo:
- Backend: http://localhost:5000/api/health
- Frontend: http://localhost:3000

## 📚 Documentación Completa

Ver [README.md](README.md) para instrucciones detalladas.

## 🎯 Endpoints API

- `GET /api/health` - Estado del servidor
- `GET /api/sintomas` - Lista de síntomas
- `POST /api/diagnosticar` - Realizar diagnóstico
- `POST /api/login` - Autenticación
- Ver `backend/app.py` para todos los endpoints

## 🏗️ Estructura de Carpetas

```
P1/
├── frontend/          # React app (puerto 3000)
├── backend/           # Flask API (puerto 5000)
├── src/               # Código Python compartido
├── base_conocimiento/ # Prolog knowledge base
└── docs/              # Documentación
```

## 📞 Soporte

Si encuentras problemas:
1. Verificar que Python, Node.js y SWI-Prolog estén instalados
2. Revisar que ambos servidores estén corriendo
3. Verificar la consola del navegador (F12) para errores

---

**¡Listo para usar MediLogic! 🏥🤖**
