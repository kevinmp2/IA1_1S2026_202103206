# 🎉 MediLogic - Migración a Arquitectura Web

## ✅ ¿Qué se ha implementado?

El proyecto MediLogic ha sido transformado de una aplicación de escritorio (Tkinter) a una **aplicación web moderna** con arquitectura cliente-servidor.

## 🏗️ Nueva Arquitectura

### Frontend (React)
- **Framework**: React 18 con Vite
- **Puerto**: 3000
- **Ubicación**: `/frontend`
- **Características**:
  - Single Page Application (SPA)
  - React Router para navegación
  - Axios para peticiones HTTP
  - React Toastify para notificaciones
  - Diseño responsive
  - Hot Module Replacement (HMR)

### Backend (Flask)
- **Framework**: Flask + Flask-CORS
- **Puerto**: 5000
- **Ubicación**: `/backend`
- **Características**:
  - API REST completa
  - Endpoints para paciente y administrador
  - Integración con Prolog (pyswip)
  - Módulo RPA funcional
  - Generación de PDF

## 📁 Estructura del Proyecto

```
P1/
├── frontend/                    # ⭐ NUEVO
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx      # Barra de navegación
│   │   │   └── Navbar.css
│   │   ├── pages/
│   │   │   ├── Home.jsx        # Página de inicio
│   │   │   ├── Paciente.jsx    # Módulo paciente
│   │   │   ├── Login.jsx       # Login administrador
│   │   │   └── Administrador.jsx  # Panel admin
│   │   ├── services/
│   │   │   └── api.js          # Cliente API
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── App.css
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .gitignore
│   ├── .env.example
│   └── README.md
│
├── backend/                     # ⭐ NUEVO
│   ├── app.py                  # Servidor Flask con API REST
│   └── README.md
│
├── src/                         # Código Python compartido
│   ├── modulos/
│   │   ├── rpa.py              # ✅ Mantenido
│   │   ├── admin.py            # 🔄 Adaptado (solo lógica)
│   │   └── paciente.py         # 🔄 Adaptado (solo lógica)
│   └── utils/
│       ├── prolog_engine.py    # ✅ Mantenido
│       └── pdf_generator.py    # ✅ Mantenido
│
├── base_conocimiento/
│   └── medilogic.pl            # ✅ Sin cambios
│
├── datos/
│   └── enfermedades_ejemplo.txt # ✅ Archivo de ejemplo RPA
│
├── docs/
│   ├── MANUAL_USUARIO.md       # ✅ Documentación
│   └── MANUAL_TECNICO.md       # ✅ Documentación técnica
│
├── start-backend.bat           # ⭐ Script Windows backend
├── start-frontend.bat          # ⭐ Script Windows frontend
├── start-backend.sh            # ⭐ Script Linux/Mac backend
├── start-frontend.sh           # ⭐ Script Linux/Mac frontend
├── INICIO_RAPIDO.md            # ⭐ Guía de inicio rápido
├── INSTRUCCIONES_GITHUB.md     # ✅ Instrucciones Git
├── README.md                   # 🔄 Actualizado para web
├── requirements.txt            # 🔄 Actualizado (Flask añadido)
├── LICENSE                     # ✅ Sin cambios
└── .gitignore                  # ✅ Sin cambios
```

## 🎨 Componentes Frontend Creados

### Páginas
1. **Home** (`/`)
   - Presentación del sistema
   - Características principales
   - Enlaces a módulos
   - Advertencia médica

2. **Paciente** (`/paciente`)
   - Formulario de síntomas con checkboxes
   - Selector de severidad (leve/moderado/severo)
   - Input de alergias
   - Selector de enfermedades crónicas
   - Panel de resultados con diagnósticos
   - Botón de descarga PDF
   - Historial de sesión

3. **Login** (`/login`)
   - Formulario de autenticación
   - Credenciales por defecto mostradas
   - Redirección a panel admin tras login exitoso

4. **Administrador** (`/admin`)
   - Tabs navegables:
     - 🦠 Enfermedades: Tabla con CRUD
     - 🩺 Síntomas: Tabla con CRUD
     - 💊 Medicamentos: Tabla con CRUD
     - 📝 Prolog: Editor de código
     - 🤖 RPA: Carga masiva y envío de correos

### Componentes
- **Navbar**: Barra de navegación con links y logout

### Servicios
- **api.js**: Cliente Axios con todos los endpoints configurados

## 🔌 API REST Endpoints

### Públicos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/sintomas` | Lista de síntomas |
| GET | `/api/enfermedades` | Lista de enfermedades |
| GET | `/api/medicamentos` | Lista de medicamentos |
| GET | `/api/enfermedades-cronicas` | Enfermedades crónicas |

### Paciente
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/diagnosticar` | Realizar diagnóstico |
| POST | `/api/generar-pdf` | Generar informe PDF |

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/login` | Login de administrador |

### Administrador
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/admin/enfermedad` | Crear enfermedad |
| PUT | `/api/admin/enfermedad/<id>` | Editar enfermedad |
| DELETE | `/api/admin/enfermedad/<id>` | Eliminar enfermedad |
| GET | `/api/admin/prolog` | Obtener archivo Prolog |
| POST | `/api/admin/prolog` | Guardar archivo Prolog |

### RPA
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/rpa/procesar` | Procesar archivo RPA |
| POST | `/api/rpa/enviar-correo` | Enviar informe |

## 🚀 Cómo Ejecutar

### Opción 1: Scripts (Recomendado)
**Windows:**
```bash
start-backend.bat    # Terminal 1
start-frontend.bat   # Terminal 2
```

**Linux/Mac:**
```bash
./start-backend.sh   # Terminal 1
./start-frontend.sh  # Terminal 2
```

### Opción 2: Manual
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm install  # Solo primera vez
npm run dev
```

### Acceder
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## ✨ Características Nuevas

### 1. **Interfaz Web Moderna**
- Diseño responsive
- Navegación fluida con React Router
- Notificaciones toast
- Loading states
- Manejo de errores

### 2. **Separación Frontend-Backend**
- API REST estandarizada
- Escalabilidad mejorada
- Posibilidad de múltiples clientes

### 3. **Autenticación**
- Login funcional
- Token storage en localStorage
- Protección de rutas admin

### 4. **Mejoras de UX**
- Feedback visual inmediato
- Estados de carga
- Validación de formularios
- Historial de diagnósticos en sesión

## 🔧 Tecnologías Agregadas

### Frontend
- React 18.2.0
- React Router DOM 6.21.0
- Axios 1.6.5
- React Icons 5.0.1
- React Toastify 10.0.4
- Vite 5.0.11

### Backend
- Flask 3.0.0
- Flask-CORS 4.0.0

## 📝 Archivos Clave

### Configuración
- `frontend/vite.config.js` - Configuración Vite con proxy
- `frontend/package.json` - Dependencias Node.js
- `requirements.txt` - Dependencias Python (actualizado)

### Documentación
- `README.md` - Documentación principal (actualizada)
- `INICIO_RAPIDO.md` - Guía de inicio rápido
- `frontend/README.md` - Documentación del frontend
- `backend/README.md` - Documentación del backend

### Scripts
- `start-backend.bat` / `.sh` - Iniciar backend
- `start-frontend.bat` / `.sh` - Iniciar frontend

## ⚠️ Archivos Deprecados

Los siguientes archivos **ya no se usan** pero se mantienen por compatibilidad:
- `src/main.py` - Aplicación Tkinter (reemplazada por backend/app.py)
- `src/modulos/inicio.py` - Pantalla inicio Tkinter (reemplazada por Home.jsx)
- UI parts de `src/modulos/paciente.py` y `admin.py` (lógica mantenida)

## 🎯 Próximos Pasos

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt  # Backend
   cd frontend && npm install       # Frontend
   ```

2. **Verificar Prolog**:
   ```bash
   python -c "from pyswip import Prolog; print('OK')"
   ```

3. **Ejecutar aplicación**:
   - Usar scripts de inicio
   - O ejecutar manualmente

4. **Acceder**:
   - Abrir http://localhost:3000
   - Probar módulo paciente
   - Login admin (admin/admin123)

## 📚 Documentación Adicional

- Ver `INICIO_RAPIDO.md` para guía paso a paso
- Ver `frontend/README.md` para detalles del frontend
- Ver `backend/README.md` para detalles del backend
- Ver `docs/MANUAL_TECNICO.md` para arquitectura completa

## 🎉 ¡Listo!

El proyecto MediLogic ahora es una **aplicación web moderna** con:
- ✅ Frontend React con componentes reutilizablesv
- ✅ Backend Flask con API REST
- ✅ Separación de responsabilidades
- ✅ Arquitectura escalable
- ✅ Interfaz profesional
- ✅ Toda la funcionalidad original mantenida

---

**¡Disfruta de tu nueva aplicación web MediLogic!** 🏥🤖✨
