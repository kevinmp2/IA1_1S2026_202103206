# MediLogic - Sistema Experto de Diagnóstico Médico

## Descripción
Sistema experto inteligente basado en lógica computacional y automatización robótica de procesos (RPA), orientado al diagnóstico médico preliminar. Arquitectura web moderna con React + Flask.

## Tecnologías
- **Frontend**: React 18 + Vite
- **Backend**: Flask + Python 3.x (API REST)
- **Motor Lógico**: Prolog (pyswip)
- **RPA**: PyAutoGUI, TagUI
- **Generación PDF**: ReportLab

## Arquitectura
```
┌─────────────────────────┐
│   Frontend (React)      │
│   Puerto: 3000          │
└───────────┬─────────────┘
            │ HTTP/REST
            │
┌───────────▼─────────────┐
│   Backend (Flask)       │
│   Puerto: 5000          │
│   API REST              │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│   Motor Prolog          │
│   (SWI-Prolog)          │
└─────────────────────────┘
```

## Estructura del Proyecto
```
P1/
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   │   └── Navbar.jsx
│   │   ├── pages/         # Páginas principales
│   │   │   ├── Home.jsx
│   │   │   ├── Paciente.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Administrador.jsx
│   │   ├── services/      # Servicios API
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/               # API Flask
│   └── app.py            # Servidor backend
├── src/                   # Código fuente Python
│   ├── modulos/
│   │   ├── rpa.py        # Automatización RPA
│   │   └── ...
│   └── utils/
│       ├── prolog_engine.py  # Motor Prolog
│       └── pdf_generator.py  # Generación PDF
├── base_conocimiento/      # Base de conocimiento
│   └── medilogic.pl       # Archivo Prolog
├── datos/                 # Datos de ejemplo
│   └── enfermedades_ejemplo.txt
├── docs/                  # Documentación
│   ├── MANUAL_USUARIO.md
│   └── MANUAL_TECNICO.md
├── requirements.txt       # Dependencias Python
└── LICENSE
```

## Instalación

### Requisitos Previos
1. **Node.js 18+** y npm (para React)
2. **Python 3.8+** (para backend)
3. **SWI-Prolog** (motor de inferencia)

#### Instalar Node.js
- Windows/Mac: Descargar desde https://nodejs.org/
- Linux: `sudo apt install nodejs npm`

#### Instalar SWI-Prolog
**Windows:**
1. Descargar desde: https://www.swi-prolog.org/download/stable
2. Instalar en la ruta predeterminada
3. Variables de entorno se configuran automáticamente

**Linux:**
```bash
sudo apt-add-repository ppa:swi-prolog/stable
sudo apt-get update
sudo apt-get install swi-prolog
```

**macOS:**
```bash
brew install swi-prolog
```

### Instalación del Proyecto

#### 1. Clonar repositorio
```bash
git clone https://github.com/[usuario]/IA1_1S2026_[Carnet].git
cd IA1_1S2026_[Carnet]/P1
```

#### 2. Instalar Backend (Python)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 3. Instalar Frontend (React)
```bash
cd frontend
npm install
```

#### 4. Configurar Variables de Entorno (Opcional)

Para el envío de correos electrónicos por RPA sin ingresar credenciales manualmente cada vez:

**Paso 1:** Copiar el archivo de ejemplo
```bash
# Desde la carpeta P1
cp .env.example .env
```

**Paso 2:** Editar el archivo `.env` con tus credenciales:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_REMITENTE=tu-correo@gmail.com
EMAIL_PASSWORD=tu-contraseña-de-aplicacion
```

**Paso 3:** Obtener contraseña de aplicación de Gmail:
1. Ir a https://myaccount.google.com/apppasswords
2. Iniciar sesión en tu cuenta de Google
3. En "Nombre de la app", escribir: `MediLogic`
4. Click en "Generar"
5. Copiar la contraseña de 16 caracteres generada
6. Pegarla en `EMAIL_PASSWORD` del archivo `.env`

**Nota:** El archivo `.env` está en `.gitignore` y nunca se subirá al repositorio. Si no configuras estas variables, podrás ingresar las credenciales manualmente en el panel de administrador.

### Verificar Instalación
```bash
# Verificar Prolog
python -c "from pyswip import Prolog; prolog = Prolog(); print('✓ Prolog OK')"

# Verificar Node.js
node --version
npm --version
```

## Ejecutar la Aplicación


### Inicio Manual

**Terminal 1 - Backend:**
```bash
# Desde la carpeta P1
cd backend
python app.py
```
   Backend: http://localhost:5000

**Terminal 2 - Frontend:**
```bash
# Desde la carpeta P1/frontend
cd frontend
npm run dev
```
   Frontend: http://localhost:3000

### Modo Producción

**Backend:**
```bash
cd backend
python app.py
```

**Frontend:**
```bash
cd frontend
npm run build
# Archivos compilados en: frontend/dist/
```


## Uso de la Aplicación

1. **Abrir navegador** en http://localhost:3000
2. **Módulo Paciente**: 
   - Seleccionar síntomas y su severidad
   - Ingresar alergias
   - Seleccionar enfermedades crónicas
   - Click en "Realizar Diagnóstico"
   - Ver resultados y descargar PDF
   
3. **Módulo Administrador**: 
   - Click en "Login" en el menú
   - Credenciales:
     - Usuario: `admin` | Contraseña: `admin123`
     - Usuario: `medico` | Contraseña: `medico123`
   - Acceder a gestión de base de conocimiento
   - Usar módulo RPA para carga masiva

## Funcionalidades

### Módulo de Pacientes
- Ingreso de síntomas con nivel de severidad
- Registro de alergias y enfermedades crónicas
- Generación de diagnóstico con porcentaje de afinidad
- Sugerencia de medicamentos seguros
- Descarga de informe en PDF

### Módulo de Administrador
- Gestión de enfermedades (CRUD)
- Gestión de síntomas (CRUD)
- Gestión de medicamentos y contraindicaciones
- Carga/descarga de archivo .pl
- Panel de control integrado

### RPA (Automatización)
- Carga automática de enfermedades desde archivo de texto
- Clasificación por sistema del cuerpo
- Generación de informes
- Envío de notificaciones por correo

## Autor
- Nombre: Kewin Maslovy Patzan Tzun
- Carnet: 202103206
- Curso: Inteligencia Artificial 1 - 1S2026


