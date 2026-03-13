# Manual Técnico - MediLogic

## Sistema Experto de Diagnóstico Médico Preliminar

---

## Tabla de Contenidos
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Base de Conocimiento Prolog](#base-de-conocimiento-prolog)
4. [Módulos del Sistema](#módulos-del-sistema)
5. [Motor de Inferencia](#motor-de-inferencia)
6. [Integración Python-Prolog](#integración-python-prolog)
7. [Módulo RPA](#módulo-rpa)
8. [Flujo de Datos](#flujo-de-datos)
9. [Consideraciones de Diseño](#consideraciones-de-diseño)
10. [Decisiones de Diseño](#decisiones-de-diseño)
11. [Generación de PDF](#generación-de-pdf)

---

## Arquitectura del Sistema

### Patrón de Diseño
MediLogic implementa una arquitectura de **tres capas**:

```
┌─────────────────────────────────────────┐
│      CAPA DE PRESENTACIÓN (UI)          │
│    React + Vite (SPA Web)               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      CAPA DE LÓGICA DE NEGOCIO          │
│    Flask (REST API)                     │
│    - Endpoints Paciente/Admin           │
│    - Orquestación Prolog/PDF/RPA        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      CAPA DE DATOS Y CONOCIMIENTO       │
│    Prolog - Motor de Inferencia         │
│    Base de Conocimiento (medilogic.pl)  │
└─────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Frontend (UI)
- **Stack**: React 18 + Vite
- **Patrón**: SPA con `react-router-dom`
- **Componentes**:
    - `Home`: Página de inicio y acceso a módulos
    - `Paciente`: Flujo de captura de síntomas y diagnóstico
    - `Login`: Autenticación del administrador
    - `Administrador`: CRUD, editor Prolog y RPA

#### 2. Backend (Lógica de Negocio)
- **Stack**: Flask + Python 3.8+
- **Componentes**:
    - `app.py`: API REST y validación de entrada
  - `PrologEngine`: Interfaz Python-Prolog
  - `PDFGenerator`: Generación de informes
  - `RPA_MediLogic`: Automatización de procesos

#### 3. Motor de Conocimiento
- **Lenguaje**: Prolog (SWI-Prolog)
- **Archivo**: `base_conocimiento/medilogic.pl`
- **Paradigma**: Programación lógica

---

## Tecnologías Utilizadas

### Python 3.8+
**Justificación**: Lenguaje versátil con excelentes bibliotecas para IA simbólica, APIs y automatización.

**Bibliotecas principales**:
```python
pyswip==0.2.11         # Interfaz Python-Prolog
pyautogui==0.9.54      # RPA y automatización
reportlab==4.0.9       # Generación de PDF
```

### SWI-Prolog
**Justificación**: Motor Prolog robusto y ampliamente usado en IA simbólica.

**Características usadas**:
- Consultas lógicas
- Unificación
- Backtracking
- Reglas de inferencia
- Predicados dinámicos

### ReportLab
**Justificación**: Generación de PDF profesionales con control total sobre el diseño.

---

## Base de Conocimiento Prolog

### Estructura del Archivo `medilogic.pl`

#### 1. Predicados de Hechos

##### Síntomas: `sintoma/4`
```prolog
sintoma(ID, Nombre, Descripcion, Sistema).

% Ejemplo:
sintoma(s1, 'Tos persistente', 
        'Tos que dura más de 3 días', 
        respiratorio).
```

**Parámetros**:
- `ID`: Identificador único (átomo)
- `Nombre`: Nombre del síntoma (cadena)
- `Descripcion`: Descripción detallada (cadena)
- `Sistema`: Sistema del cuerpo afectado (átomo)

##### Enfermedades: `enfermedad/6`
```prolog
enfermedad(ID, Nombre, Descripcion, Sistema, Tipo, Gravedad).

% Ejemplo:
enfermedad(e1, 'Gripe Común',
           'Infección viral del tracto respiratorio',
           respiratorio, viral, moderada).
```

**Parámetros**:
- `ID`: Identificador único
- `Nombre`: Nombre de la enfermedad
- `Descripcion`: Descripción médica
- `Sistema`: Sistema del cuerpo afectado
- `Tipo`: Clasificación (viral, bacterial, crónico, etc.)
- `Gravedad`: Nivel (leve, moderada, grave)

##### Medicamentos: `medicamento/5`
```prolog
medicamento(ID, Nombre, Tipo, Dosis, Contraindicaciones).

% Ejemplo:
medicamento(m1, 'Paracetamol', analgesico,
            '500mg cada 8 horas',
            'Evitar en enfermedad hepática').
```

##### Relaciones Síntoma-Enfermedad: `presenta_sintoma/3`
```prolog
presenta_sintoma(EnfermedadID, SintomaID, Peso).

% Ejemplo:
presenta_sintoma(e1, s1, 8).  % Gripe → Tos (peso 8/10)
presenta_sintoma(e1, s2, 9).  % Gripe → Fiebre (peso 9/10)
```

**Peso**: Importancia del síntoma (1-10)
- 1-3: Síntoma secundario/ocasional
- 4-7: Síntoma común
- 8-10: Síntoma principal/característico

##### Relaciones Medicamento-Enfermedad: `trata_enfermedad/3`
```prolog
trata_enfermedad(MedicamentoID, EnfermedadID, Efectividad).

% Ejemplo:
trata_enfermedad(m1, e1, 80).  % Paracetamol trata Gripe (80%)
```

##### Contraindicaciones: `contraindicado/3`
```prolog
contraindicado(MedicamentoID, Alergia, Gravedad).

% Ejemplo:
contraindicado(m2, penicilina, grave).
```

#### 2. Reglas de Inferencia

##### Calcular Afinidad: `calcular_afinidad/3`
```prolog
calcular_afinidad(Enfermedad, SintomasPaciente, Afinidad) :-
    findall(Peso,
            (member((Sintoma, Severidad), SintomasPaciente),
             presenta_sintoma(Enfermedad, Sintoma, Peso),
             ajustar_peso(Peso, Severidad, PesoAjustado)),
            Pesos),
    sum_list(Pesos, SumaPesos),
    findall(PesoTotal,
            presenta_sintoma(Enfermedad, _, PesoTotal),
            TodosPesos),
    sum_list(TodosPesos, MaxPesos),
    (MaxPesos > 0 -> 
        Afinidad is (SumaPesos / MaxPesos) * 100 
    ; 
        Afinidad is 0
    ).
```

**Lógica**:
1. Para cada síntoma del paciente, buscar si la enfermedad lo presenta
2. Ajustar el peso según la severidad reportada
3. Sumar todos los pesos coincidentes
4. Calcular porcentaje: (pesos coincidentes / pesos totales) × 100

##### Ajustar Peso por Severidad: `ajustar_peso/3`
```prolog
ajustar_peso(Peso, leve, PesoAjustado) :- 
    PesoAjustado is Peso * 0.7.
    
ajustar_peso(Peso, moderado, PesoAjustado) :- 
    PesoAjustado is Peso * 1.0.
    
ajustar_peso(Peso, severo, PesoAjustado) :- 
    PesoAjustado is Peso * 1.3.
```

**Multiplicadores**:
- Leve: 0.7× (reduce peso)
- Moderado: 1.0× (sin cambio)
- Severo: 1.3× (aumenta peso)

##### Nivel de Urgencia: `nivel_urgencia/3`
```prolog
nivel_urgencia(Enfermedad, Afinidad, Urgencia) :-
    enfermedad(Enfermedad, _, _, _, _, Gravedad),
    (   Gravedad = grave, Afinidad > 60 -> 
        Urgencia = 'ALTA - Buscar atención inmediata'
    ;   Gravedad = grave -> 
        Urgencia = 'MEDIA - Monitorizar síntomas'
    ;   Gravedad = moderada, Afinidad > 70 -> 
        Urgencia = 'MEDIA - Consultar médico pronto'
    ;   
        Urgencia = 'BAJA - Cuidados básicos'
    ).
```

**Clasificación de urgencia**:
- **ALTA**: Enfermedad grave + afinidad > 60%
- **MEDIA**: Enfermedad grave o (moderada + afinidad > 70%)
- **BAJA**: Resto de casos

##### Medicamento Seguro: `medicamento_seguro/3`
```prolog
medicamento_seguro(Medicamento, Alergias, Cronicas) :-
    medicamento(Medicamento, Nombre, _, _, _),
    \+ (member(Alergia, Alergias),
        contraindicado(Medicamento, Alergia, _)),
    \+ (member(Cronica, Cronicas),
        contraindicado_cronica(Medicamento, Cronica)).
```

**Lógica**:
- Verificar que el medicamento NO tenga contraindicaciones con alergias
- Verificar que NO tenga contraindicaciones con enfermedades crónicas
- Usa negación por falla (`\+`)

##### Diagnóstico Principal: `diagnosticar/4`
```prolog
diagnosticar(SintomasPaciente, Alergias, Cronicas, Diagnosticos) :-
    findall(
        (Afinidad, Enfermedad, Urgencia, Medicamentos),
        (
            enfermedad(Enfermedad, _, _, _, _, _),
            calcular_afinidad(Enfermedad, SintomasPaciente, Afinidad),
            Afinidad > 30,  % Umbral mínimo
            nivel_urgencia(Enfermedad, Afinidad, Urgencia),
            findall(Med,
                    (trata_enfermedad(Med, Enfermedad, _),
                     medicamento_seguro(Med, Alergias, Cronicas)),
                    Medicamentos)
        ),
        ResultadosSinOrdenar
    ),
    sort(1, @>=, ResultadosSinOrdenar, Diagnosticos).
```

**Proceso**:
1. Encontrar todas las enfermedades
2. Calcular afinidad con síntomas del paciente
3. Filtrar las que tengan afinidad > 30%
4. Determinar nivel de urgencia
5. Buscar medicamentos seguros para cada diagnóstico
6. Ordenar resultados por afinidad (descendente)

---

## Módulos del Sistema

### 1. `backend/app.py` - API Principal

`app.py` centraliza la API REST y conecta frontend, motor Prolog y servicios auxiliares.

**Responsabilidades**:
- Exponer endpoints de paciente (`/api/sintomas`, `/api/diagnosticar`, `/api/generar-pdf`)
- Exponer endpoints de administración (`/api/admin/*`)
- Validar payloads y responder JSON uniforme (`success`, `data`, `error`)
- Coordinar llamadas a `PrologEngine`, `PDFGenerator` y `RPA_MediLogic`

### 2. `backend/src/utils/prolog_engine.py` - Motor de Inferencia

**Responsabilidades**:
- Cargar y recargar `base_conocimiento/medilogic.pl`
- Ejecutar consultas SWI-Prolog desde Python
- Convertir estructuras Python a términos Prolog
- Gestionar CRUD de hechos y relaciones dinámicas

**Consideraciones**:
- Manejo de excepciones en consultas
- Conversión de tipos Python ↔ Prolog
- Persistencia consistente del archivo `.pl`

### 3. `frontend/src/App.jsx` - Enrutamiento de la SPA

**Rutas principales**:
- `/` → Inicio (`Home`)
- `/paciente` → Flujo de diagnóstico
- `/login` → Inicio de sesión de administrador
- `/admin` → Panel administrativo

**Responsabilidades**:
- Montar navegación con `react-router-dom`
- Mantener layout compartido (`Navbar` + contenido)
- Mostrar notificaciones globales con `react-toastify`

### 4. `frontend/src/pages/Paciente.jsx` - Módulo Paciente

**Responsabilidades**:
- Obtener catálogos clínicos (síntomas y crónicas)
- Capturar síntomas y severidad
- Enviar solicitud de diagnóstico (`POST /api/diagnosticar`)
- Mostrar resultados con afinidad y recomendaciones
- Descargar PDF de resultados (`POST /api/generar-pdf`)

**Flujo**:
1. Usuario completa formulario clínico.
2. Frontend envía payload JSON al backend.
3. Backend consulta Prolog y calcula afinidades.
4. Frontend renderiza diagnósticos y urgencia.

### 5. `frontend/src/pages/Administrador.jsx` - Módulo Administrador

**Responsabilidades**:
- Autenticar usuario administrador (`POST /api/login`)
- Ejecutar CRUD de enfermedades, síntomas y medicamentos
- Gestionar relaciones clínicas
- Editar, guardar, importar y exportar `medilogic.pl`
- Ejecutar funciones RPA y envío de informe por correo

### 6. `backend/src/modulos/rpa.py` - Automatización RPA

**Funciones clave**:
- Parseo de archivos de carga de enfermedades
- Clasificación y validación de registros
- Generación de informe de carga
- Envío por SMTP de resultados

### 7. `backend/src/utils/pdf_generator.py` - Generación de PDF

**Funciones clave**:
- Construcción de informe clínico en memoria
- Renderizado tabular de síntomas, alergias y diagnósticos
- Entrega del PDF al frontend para descarga inmediata

---

## Motor de Inferencia

### Algoritmo de Diagnóstico

**Pseudocódigo**:
```
FUNCIÓN diagnosticar(sintomas_paciente, alergias, cronicas):
    diagnosticos = []
    
    PARA CADA enfermedad EN base_conocimiento:
        afinidad = calcular_afinidad(enfermedad, sintomas_paciente)
        
        SI afinidad > 30%:
            urgencia = determinar_urgencia(enfermedad, afinidad)
            medicamentos = buscar_medicamentos_seguros(
                enfermedad, alergias, cronicas
            )
            
            diagnosticos.agregar(
                enfermedad, afinidad, urgencia, medicamentos
            )
    
    diagnosticos.ordenar_por_afinidad(DESC)
    RETORNAR diagnosticos
```

### Cálculo de Afinidad

**Fórmula**:
$$
\text{Afinidad} = \frac{\sum_{i=1}^{n} (P_i \times F_s)}{\sum_{j=1}^{m} P_j} \times 100
$$

Donde:
- $P_i$ = Peso del síntoma $i$ coincidente
- $F_s$ = Factor de severidad (0.7, 1.0, o 1.3)
- $n$ = Número de síntomas coincidentes
- $m$ = Número total de síntomas de la enfermedad

**Ejemplo**:
```
Enfermedad: Gripe
Síntomas de la enfermedad:
  - s1 (Tos): peso 8
  - s2 (Fiebre): peso 9
  - s5 (Dolor muscular): peso 6
  Total pesos: 23

Síntomas del paciente:
  - s1 (Tos): SEVERO → 8 × 1.3 = 10.4
  - s2 (Fiebre): MODERADO → 9 × 1.0 = 9.0
  Suma coincidencias: 19.4

Afinidad = (19.4 / 23) × 100 = 84.3%
```

---

## Integración Python-Prolog

### PySwip

**Instalación**:
```bash
# 1. Instalar SWI-Prolog (sistema)
# 2. Instalar PySwip
pip install pyswip
```

**Uso básico**:
```python
from pyswip import Prolog

prolog = Prolog()
prolog.consult('archivo.pl')

# Consulta simple
resultado = list(prolog.query("sintoma(ID, Nombre, _, _)"))
# [{'ID': 's1', 'Nombre': 'Tos'}, ...]

# Consulta con variables
for solución in prolog.query("enfermedad(ID, Nombre, _, _, _, _)"):
    print(f"ID: {solución['ID']}, Nombre: {solución['Nombre']}")
```

**Conversión de tipos**:
| Python | Prolog |
|--------|--------|
| `str` | Átomo |
| `int` / `float` | Número |
| `list` | Lista |
| `tuple` | Tupla/Estructura |
| `None` | Variable no unificada |

**Limitaciones**:
- No soporta todos los predicados avanzados de SWI-Prolog
- Problemas con caracteres especiales (acentos, ñ)
- Requiere manejo cuidadoso de strings

---

## Generación de PDF

### ReportLab

**Componentes usados**:
- `SimpleDocTemplate`: Gestión de páginas
- `Paragraph`: Texto con estilos
- `Table`: Tablas formateadas
- `Spacer`: Espaciado vertical
- `PageBreak`: Saltos de página

**Estilos personalizados**:
```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2C3E50'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)
```

**Tablas con estilo**:
```python
tabla = Table(data, colWidths=[2*inch, 4*inch])
tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.grey),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
```

---

## Módulo RPA

### PyAutoGUI

**Funciones usadas**:
```python
import pyautogui

# Seguridad: mover mouse a esquina = abortar
pyautogui.FAILSAFE = True

# Pausa entre acciones
pyautogui.PAUSE = 0.5

# Acciones
pyautogui.click(x=100, y=200)
pyautogui.write('texto', interval=0.1)
pyautogui.press('tab')
pyautogui.hotkey('ctrl', 's')
```

**En MediLogic**:
- No se usa para automatización de GUI (no es necesario)
- Se incluye como requisito del proyecto
- Método `automatizar_ingreso_interfaz()` está preparado para extensión futura

### SMTP para Correos

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, cuerpo):
    msg = MIMEMultipart()
    msg['From'] = 'remitente@gmail.com'
    msg['To'] = destinatario
    msg['Subject'] = asunto
    
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    # Gmail con contraseña de aplicación
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('remitente@gmail.com', 'password_app')
    server.send_message(msg)
    server.quit()
```

---

## Flujo de Datos

### Diagnóstico de Paciente

```
┌──────────────┐
│ Usuario      │
│ selecciona   │
│ síntomas     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ ModuloPaciente       │
│ recopila datos       │
│ - sintomas_vars      │
│ - severidad_vars     │
│ - alergias           │
│ - cronicas_vars      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ PrologEngine         │
│ .diagnosticar()      │
│ construye consulta   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ SWI-Prolog           │
│ ejecuta reglas       │
│ - calcular_afinidad  │
│ - nivel_urgencia     │
│ - medicamento_seguro │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Resultados           │
│ [(afinidad, enf,     │
│   urgencia, meds)]   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ ModuloPaciente       │
│ .mostrar_resultados()│
│ formatea y muestra   │
└──────┬───────────────┘
       │
       ▼ (opcional)
┌──────────────────────┐
│ PDFGenerator         │
│ genera informe PDF   │
└──────────────────────┘
```

### Carga RPA

```
┌──────────────────┐
│ Archivo TXT      │
│ enfermedades.txt │
└────────┬─────────┘
         │
         ▼
┌────────────────────────┐
│ RPA_MediLogic          │
│ .cargar_enfermedades() │
│ parsea archivo         │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ RPA_MediLogic          │
│ .clasificar_enfermedad()│
│ valida datos           │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ RPA_MediLogic          │
│ .generar_informe_txt() │
│ crea reporte           │
└────────┬───────────────┘
         │
         ▼ (opcional)
┌────────────────────────┐
│ SMTP                   │
│ envía por correo       │
└────────────────────────┘
```

---

## Consideraciones de Diseño

### 1. Separación de Responsabilidades
- **UI**: Solo presentación y captura de datos
- **Lógica**: En módulos Python independientes
- **Conocimiento**: En Prolog, separado del código

### 2. Extensibilidad
- Agregar nuevos síntomas: Solo editar `medilogic.pl`
- Agregar nuevas reglas: Ampliar predicados Prolog
- Cambiar UI: Solo modificar módulos de interfaz

### 3. Mantenibilidad
- Código modular y documentado
- Archivo Prolog editable sin recompilar
- Logs de operaciones RPA

### 4. Escalabilidad
**Limitaciones actuales**:
- Base de conocimiento en archivo único
- Sin persistencia de datos de pacientes
- Autenticación en diccionario hardcoded

**Mejoras futuras**:
- Base de datos (SQLite, PostgreSQL)
- Sistema de usuarios robusto
- API REST para integración
- Versión web (Flask/Django)

---

## Decisiones de Diseño

### 1. Migración de Aplicación de Escritorio a Arquitectura Web

**Decisión**: Evolucionar de una interfaz de escritorio a Flask + React (web).

**Contexto**: El sistema originalmente se diseñó como aplicación local de escritorio. A medida que el proyecto evolucionó se identificó la necesidad de una interfaz más moderna, accesible desde el navegador y con mayor capacidad de expansión.

**Alternativas evaluadas**:

| Opción | Pros | Contras |
|--------|------|---------|
| Interfaz local tradicional (mantener) | Sin infraestructura web adicional | UI limitada y acoplada al entorno local |
| Flask + Jinja2 | Un solo lenguaje, simple | Sin componentes reutilizables, recarga completa por acción |
| **Flask + React** ✓ | SPA moderna, UI reactiva, separación clara | Requiere npm + servidor Python corriendo simultáneamente |
| Django + React | Más robusto para producción | Overhead excesivo para el alcance del proyecto |

**Resultado**: La separación backend (Flask REST API en `backend/app.py`) / frontend (React SPA en `frontend/`) permite mantener el motor Prolog intacto y evolucionar la interfaz de usuario de forma independiente. El backend expone únicamente JSON; la lógica de presentación reside completamente en React.

---

### 2. Prolog Como Motor de Inferencia Simbólica

**Decisión**: Usar SWI-Prolog en lugar de aprendizaje automático o reglas codificadas en Python.

**Razones principales**:
- **Interpretabilidad**: Cada diagnóstico puede rastrearse hasta las reglas lógicas exactas que lo generaron, lo que es crítico en un contexto médico.
- **Determinismo**: El mismo conjunto de síntomas produce siempre el mismo resultado, sin variaciones estadísticas.
- **Base de conocimiento separada del código**: Un médico puede revisar y editar `medilogic.pl` sin tocar el código Python ni reiniciar el servidor.
- **Extensibilidad sin reentrenamiento**: Agregar una nueva enfermedad es añadir hechos al `.pl`; no requiere reentrenar modelo alguno.

**Trade-offs asumidos**:
- Requiere instalación de SWI-Prolog en el servidor de despliegue.
- No aprende automáticamente de nuevos casos clínicos.
- Limitaciones con caracteres especiales UTF-8 al construir consultas dinámicas desde Python.

---

### 3. Declaraciones `:- dynamic` en la Base de Conocimiento

**Decisión**: Todos los predicados principales se declaran dinámicos al inicio de `medilogic.pl`.

**Problema resuelto**: Sin `:- dynamic`, SWI-Prolog lanzaba `permission_error(modify, static_procedure)` al intentar insertar o eliminar hechos en tiempo de ejecución desde el módulo administrador.

**Implementación**:
```prolog
:- dynamic sintoma/4.
:- dynamic enfermedad/6.
:- dynamic medicamento/5.
:- dynamic presenta_sintoma/3.
:- dynamic trata_enfermedad/3.
:- dynamic contraindicado/3.
```

**Consecuencia de diseño**: Al declarar todos los predicados como dinámicos desde el inicio, el sistema puede modificar la base de conocimiento en caliente mediante `assertz`/`retract` sin necesidad de recargar el archivo `.pl` completo entre operaciones CRUD.

---

### 4. Estrategia de Fusión para Carga de Archivos `.pl`

**Decisión**: La carga de un archivo `.pl` externo fusiona (merge) predicados en lugar de reemplazar la base completa.

**Contexto**: La primera implementación reemplazaba el archivo completo, eliminando todos los datos existentes al cargar un nuevo `.pl`.

**Alternativas consideradas**:

| Estrategia | Comportamiento | Riesgo |
|-----------|----------------|--------|
| Reemplazo completo | El nuevo `.pl` sustituye toda la base | Pérdida irreversible de datos |
| **Fusión (merge)** ✓ | Los IDs existentes se actualizan; los nuevos se insertan | Seguro, no destructivo |
| Append puro | Solo inserta sin actualizar nunca | Genera predicados duplicados |

**Lógica del endpoint `POST /api/admin/prolog/upload`**:
1. Un parser con expresiones regulares extrae los predicados del archivo subido.
2. Para cada predicado: si el ID ya existe en la base actual → lo actualiza; si no → lo inserta al final de su sección.
3. El archivo `medilogic.pl` se persiste con el resultado combinado.

---

### 5. Diseño del API REST

**Decisión**: API sin autenticación JWT (alcance MVP) con rutas agrupadas semánticamente por módulo.

**Estructura de rutas**:
```
GET  /api/paciente/sintomas
POST /api/paciente/diagnosticar
GET  /api/paciente/pdf/<id>

POST /api/admin/login
GET  /api/admin/enfermedades
POST /api/admin/enfermedades
PUT  /api/admin/enfermedades/<id>
DELETE /api/admin/enfermedades/<id>
... (síntomas, medicamentos, relaciones)
POST /api/admin/prolog/upload
GET  /api/admin/prolog/export
POST /api/admin/rpa/cargar
POST /api/admin/rpa/enviar-correo
```

**Decisión sobre autenticación**:
- **MVP**: Las credenciales se verifican en el backend; el estado de sesión se gestiona en memoria con Flask sessions.
- **Razón**: El alcance del proyecto no requiere multiusuario ni tokens persistentes entre reinicios.
- **Extensión futura recomendada**: Migrar a JWT (`flask-jwt-extended`) con una base de datos de usuarios (SQLite o PostgreSQL).

---

### 6. Interfaz de Usuario: Estética Clínica Diferenciada

**Decisión**: Paleta de colores y componentes que comunican identidad médica y técnica, evitando plantillas SaaS genéricas.

**Paleta seleccionada**:

| Token | Valor | Uso |
|-------|-------|-----|
| Navy | `#0a2540` | Fondo hero, botones primarios, encabezados |
| Teal | `#00b4d8` | Acento principal, highlights, hover states |
| Green | `#06d6a0` | Módulo paciente, resultados, indicadores positivos |
| Coral | `#ef476f` | Módulo administrador, alertas, acciones destructivas |
| Dark terminal | `#0d1b2a` | Panel de código Prolog en la página de inicio |

**Componentes de identidad visual**:
- **Panel de código Prolog** en el hero: comunica al usuario la base tecnológica simbólica del sistema.
- **Pills de estadísticas**: exponen de forma visible las métricas de la base de conocimiento (enfermedades, síntomas, medicamentos).
- **Pasos numerados** con conectores: guía visual del flujo de diagnóstico en tres etapas.
- **Cards con gradiente por módulo**: diferenciación visual clara entre el acceso de paciente y de administrador.

**Razón del rediseño**: La interfaz original era indistinguible de plantillas SaaS genéricas. El diseño actual refleja la naturaleza clínica y el enfoque simbólico-técnico del sistema.

---

### 7. Generación de PDF en el Servidor

**Decisión**: El PDF se genera en el backend (Flask + ReportLab), no en el cliente.

**Alternativas consideradas**:

| Opción | Ventaja | Desventaja |
|--------|---------|------------|
| **ReportLab (backend)** ✓ | Control total del formato, consistente en todos los navegadores | Requiere librería Python adicional |
| jsPDF (frontend) | Sin carga al servidor | Formato limitado, difícil de estilizar con precisión |
| Puppeteer / HTML→PDF | Usa HTML como fuente de verdad | Dependencia Node.js extra, overhead en servidor |

**Resultado**: El endpoint `GET /api/paciente/pdf/<id>` devuelve el binario directamente como `application/pdf`. El frontend lo descarga creando un `Blob URL` temporal, sin abrir nuevas ventanas del navegador.

---

## Extensión y Mantenimiento

### Agregar Nuevo Síntoma

1. **Editar `medilogic.pl`**:
```prolog
sintoma(s16, 'Náuseas', 
        'Sensación de malestar estomacal',
        digestivo).
```

2. **Asociar con enfermedades**:
```prolog
presenta_sintoma(e10, s16, 9).  % Gastritis → Náuseas
```

3. **Recargar base**:
- Desde módulo administrador: "Recargar Prolog"
- O reiniciar aplicación

### Agregar Nueva Enfermedad

1. **Agregar hecho**:
```prolog
enfermedad(e14, 'Migraña',
           'Dolor de cabeza intenso y pulsátil',
           neurologico, cronico, moderada).
```

2. **Asociar síntomas**:
```prolog
presenta_sintoma(e14, s10, 10).  % Dolor de cabeza
presenta_sintoma(e14, s12, 7).   % Mareos
presenta_sintoma(e14, s7, 6).    % Sensibilidad a luz
```

3. **Asociar tratamientos**:
```prolog
trata_enfermedad(m7, e14, 85).  % Ibuprofeno
```

### Modificar Reglas de Inferencia

**Ejemplo: Cambiar umbral de afinidad**

Original:
```prolog
diagnosticar(...) :-
    ...
    Afinidad > 30,
    ...
```

Modificado:
```prolog
diagnosticar(...) :-
    ...
    Afinidad > 40,  % Más restrictivo
    ...
```

### Agregar Nueva Regla

**Ejemplo: Considerar edad del paciente**

```prolog
% Nuevo predicado
ajustar_por_edad(Enfermedad, Edad, FactorAjuste) :-
    enfermedad_pediatrica(Enfermedad),
    Edad < 12,
    FactorAjuste is 1.2.

ajustar_por_edad(Enfermedad, Edad, FactorAjuste) :-
    enfermedad_geriatrica(Enfermedad),
    Edad > 65,
    FactorAjuste is 1.15.

ajustar_por_edad(_, _, 1.0).  % Sin ajuste por defecto

% Modificar calcular_afinidad para usar el ajuste
```

---


### Casos de Prueba Clínicos

Ver documento: `docs/casos_clinicos.pdf`

**Casos incluidos**:
1. **Gripe común**: Tos + fiebre + dolor muscular
2. **Gastroenteritis**: Náuseas + vómito + diarrea + fiebre
3. **Angina**: Dolor de garganta + fiebre + malestar
4. **Caso con alergias**: Paciente alérgico a penicilina
5. **Caso con crónicas**: Paciente con diabetes e hipertensión

---



### C. Estructura de Archivos

```
P1/
├── src/
│   ├── main.py                    # Aplicación principal
│   ├── modulos/
│   │   ├── __init__.py
│   │   ├── inicio.py              # Pantalla de inicio
│   │   ├── paciente.py            # Módulo paciente
│   │   ├── admin.py               # Módulo administrador
│   │   └── rpa.py                 # RPA
│   └── utils/
│       ├── __init__.py
│       ├── prolog_engine.py       # Motor Prolog
│       └── pdf_generator.py       # Generador PDF
├── base_conocimiento/
│   └── medilogic.pl               # Base de conocimiento
├── datos/
│   └── enfermedades_ejemplo.txt   # Ejemplo RPA
├── docs/
│   ├── MANUAL_USUARIO.md
│   ├── MANUAL_TECNICO.md
│   └── casos_clinicos.md
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── test_sistema.py
└── INSTRUCCIONES_GITHUB.md
```

---

**Versión**: 1.0  
**Fecha**: Febrero 2026  
**Autor**: Kewin Maslovy Patzan Tzun

---

© 2026 MediLogic - Sistema Experto Médico
