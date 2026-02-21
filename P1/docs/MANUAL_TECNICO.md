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
7. [Generación de PDF](#generación-de-pdf)
8. [Módulo RPA](#módulo-rpa)
9. [Flujo de Datos](#flujo-de-datos)
10. [Consideraciones de Diseño](#consideraciones-de-diseño)
11. [Extensión y Mantenimiento](#extensión-y-mantenimiento)
12. [Pruebas](#pruebas)

---

## Arquitectura del Sistema

### Patrón de Diseño
MediLogic implementa una arquitectura de **tres capas**:

```
┌─────────────────────────────────────────┐
│      CAPA DE PRESENTACIÓN (UI)          │
│    Tkinter - Interfaz Gráfica           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      CAPA DE LÓGICA DE NEGOCIO          │
│    Python - Controladores               │
│    - ModuloPaciente                     │
│    - ModuloAdministrador                │
│    - RPA_MediLogic                      │
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
- **Framework**: Tkinter
- **Patrón**: Page/Frame switching
- **Componentes**:
  - `PantallaInicio`: Menú principal
  - `ModuloPaciente`: Interfaz de diagnóstico
  - `ModuloAdministrador`: Panel de gestión

#### 2. Backend (Lógica de Negocio)
- **Lenguaje**: Python 3.8+
- **Componentes**:
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
**Justificación**: Lenguaje versátil con excelentes bibliotecas para IA y GUI.

**Bibliotecas principales**:
```python
pyswip==0.2.11         # Interfaz Python-Prolog
tkinter                # GUI (incluido con Python)
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

### Tkinter
**Justificación**: 
- Incluido con Python (sin dependencias extra)
- Multiplataforma
- Suficiente para aplicaciones de escritorio

### PyAutoGUI
**Justificación**: Automatización de procesos (RPA) requerida por el proyecto.

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

### 1. `main.py` - Aplicación Principal

```python
class MediLogicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MediLogic")
        self.geometry("1200x800")
        
        # Inicializar motor Prolog
        self.prolog_engine = PrologEngine()
        
        # Container para frames
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)
        
        # Diccionario de frames
        self.frames = {}
        
        # Crear frames
        self.crear_frames()
        
        # Mostrar inicio
        self.mostrar_frame("Inicio")
    
    def crear_frames(self):
        """Crear todos los frames de la aplicación"""
        frames_clases = {
            "Inicio": PantallaInicio,
            "Paciente": ModuloPaciente,
            "Administrador": ModuloAdministrador
        }
        
        for nombre, Clase in frames_clases.items():
            frame = Clase(
                parent=self.container,
                controller=self,
                prolog_engine=self.prolog_engine
            )
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def mostrar_frame(self, nombre):
        """Mostrar un frame específico"""
        frame = self.frames[nombre]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()
```

**Patrón**: Frame switching
**Responsabilidades**:
- Gestionar ventana principal
- Inicializar motor Prolog
- Coordinar navegación entre módulos
- Compartir instancia de PrologEngine

### 2. `prolog_engine.py` - Motor de Inferencia

```python
class PrologEngine:
    def __init__(self):
        self.prolog = Prolog()
        self.archivo_pl = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'base_conocimiento', 'medilogic.pl'
        )
        self.cargar_base_conocimiento()
    
    def cargar_base_conocimiento(self):
        """Cargar archivo Prolog"""
        try:
            self.prolog.consult(self.archivo_pl)
            return True
        except Exception as e:
            print(f"Error al cargar base de conocimiento: {e}")
            return False
    
    def consultar(self, consulta):
        """Ejecutar consulta genérica"""
        try:
            return list(self.prolog.query(consulta))
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
    
    def diagnosticar(self, sintomas, alergias, cronicas):
        """
        Realizar diagnóstico
        
        Args:
            sintomas: [(id, nombre, severidad), ...]
            alergias: [alergia1, alergia2, ...]
            cronicas: [id1, id2, ...]
        
        Returns:
            Lista de diagnósticos ordenados por afinidad
        """
        # Construir consulta Prolog
        sintomas_prolog = [f"({sid}, {sev})" 
                          for sid, _, sev in sintomas]
        sintomas_str = f"[{', '.join(sintomas_prolog)}]"
        
        alergias_str = f"[{', '.join(alergias)}]" if alergias else "[]"
        cronicas_str = f"[{', '.join(cronicas)}]" if cronicas else "[]"
        
        consulta = f"""
            diagnosticar(
                {sintomas_str},
                {alergias_str},
                {cronicas_str},
                Diagnosticos
            )
        """
        
        resultado = self.consultar(consulta)
        return resultado
```

**Responsabilidades**:
- Inicializar SWI-Prolog
- Cargar base de conocimiento
- Construir consultas Prolog desde Python
- Procesar resultados

**Consideraciones**:
- Manejo de excepciones robusto
- Conversión de tipos Python ↔ Prolog
- Escapado de caracteres especiales

### 3. `paciente.py` - Módulo de Paciente

**Componentes principales**:

```python
class ModuloPaciente(ttk.Frame):
    def __init__(self, parent, controller, prolog_engine):
        super().__init__(parent)
        self.controller = controller
        self.prolog_engine = prolog_engine
        
        # Variables de formulario
        self.sintomas_vars = {}       # {sintoma_id: BooleanVar}
        self.severidad_vars = {}      # {sintoma_id: StringVar}
        self.cronicas_vars = {}       # {cronica_id: BooleanVar}
        
        # Historial
        self.historial_diagnosticos = []
        
        self.crear_widgets()
```

**Flujo de diagnóstico**:
1. Usuario selecciona síntomas y severidad
2. Usuario ingresa alergias y selecciona crónicas
3. Click en "Realizar Diagnóstico"
4. `realizar_diagnostico()` recopila datos
5. Llama a `prolog_engine.diagnosticar()`
6. `mostrar_resultados()` presenta diagnósticos
7. Usuario puede descargar PDF

### 4. `admin.py` - Módulo de Administrador

**Autenticación**:
```python
USUARIOS = {
    'admin': 'admin123',
    'medico': 'medico123'
}

def autenticar(self):
    usuario = self.usuario_entry.get()
    password = self.password_entry.get()
    
    if usuario in self.USUARIOS and \
       self.USUARIOS[usuario] == password:
        self.autenticado = True
        self.usuario_actual = usuario
        self.crear_widgets()
    else:
        messagebox.showerror(
            "Error",
            "Credenciales incorrectas"
        )
```

**CRUD de Enfermedades** (ejemplo):
```python
def nueva_enfermedad(self):
    # Ventana de diálogo
    ventana = tk.Toplevel(self)
    
    # Campos de entrada
    ttk.Label(ventana, text="ID:").grid(row=0, column=0)
    id_entry = ttk.Entry(ventana)
    id_entry.grid(row=0, column=1)
    
    # ... más campos ...
    
    def guardar():
        # Recopilar datos
        id_enf = id_entry.get()
        nombre = nombre_entry.get()
        # ...
        
        # Agregar a Prolog
        self.prolog_engine.agregar_enfermedad(...)
        
        # Actualizar lista
        self.actualizar_lista_enfermedades()
        
        ventana.destroy()
    
    ttk.Button(ventana, text="Guardar", 
               command=guardar).grid(...)
```

### 5. `rpa.py` - Automatización RPA

**Carga de archivo**:
```python
def cargar_enfermedades_desde_archivo(self, archivo_txt):
    enfermedades = []
    enfermedad_actual = {}
    
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            
            if linea == '---':
                if enfermedad_actual:
                    enfermedades.append(enfermedad_actual.copy())
                    enfermedad_actual = {}
            elif ':' in linea and linea != 'ENFERMEDAD':
                clave, valor = linea.split(':', 1)
                enfermedad_actual[clave.strip()] = valor.strip()
        
        # Última enfermedad
        if enfermedad_actual:
            enfermedades.append(enfermedad_actual)
    
    return enfermedades
```

**Envío de correo**:
```python
def enviar_informe_por_correo(self, archivo_informe, 
                               destinatarios, remitente, password):
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = f"Informe MediLogic {datetime.now()}"
    
    # Cuerpo
    cuerpo = "Se adjunta informe de carga RPA..."
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    # Adjuntar archivo
    with open(archivo_informe, 'r', encoding='utf-8') as f:
        contenido = f.read()
    adjunto = MIMEText(contenido, 'plain', 'utf-8')
    adjunto.add_header('Content-Disposition', 
                       'attachment', 
                       filename='informe_carga.txt')
    msg.attach(adjunto)
    
    # Enviar
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, password)
    server.send_message(msg)
    server.quit()
```

### 6. `pdf_generator.py` - Generación de PDF

```python
class PDFGenerator:
    def generar_informe_diagnostico(self, archivo, 
                                     datos_paciente, 
                                     diagnosticos):
        doc = SimpleDocTemplate(archivo, pagesize=letter)
        story = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Título
        story.append(Paragraph("INFORME MÉDICO", title_style))
        story.append(Spacer(1, 12))
        
        # Datos del paciente
        data = [
            ['Fecha:', datos_paciente['fecha']],
            ['Hora:', datos_paciente['hora']],
            ['Síntomas:', len(datos_paciente['sintomas'])],
            ['Alergias:', ', '.join(datos_paciente['alergias'])]
        ]
        
        tabla = Table(data, colWidths=[2*inch, 4*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla)
        
        # Diagnósticos
        # ...
        
        # Construir PDF
        doc.build(story)
```

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

## Pruebas

### Pruebas Unitarias (Python)

```python
import unittest
from utils.prolog_engine import PrologEngine

class TestPrologEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PrologEngine()
    
    def test_obtener_sintomas(self):
        sintomas = self.engine.obtener_sintomas()
        self.assertIsInstance(sintomas, list)
        self.assertGreater(len(sintomas), 0)
    
    def test_diagnosticar_gripe(self):
        sintomas = [('s1', 'Tos', 'severo'), 
                    ('s2', 'Fiebre', 'moderado')]
        alergias = []
        cronicas = []
        
        diagnosticos = self.engine.diagnosticar(
            sintomas, alergias, cronicas
        )
        
        self.assertIsInstance(diagnosticos, list)
        # Gripe debería estar en top 3
        enfermedades = [d[1] for d in diagnosticos[:3]]
        self.assertIn('e1', enfermedades)

if __name__ == '__main__':
    unittest.main()
```

### Pruebas de Integración

```python
def test_flujo_completo_diagnostico():
    # 1. Inicializar sistema
    app = MediLogicApp()
    
    # 2. Navegar a módulo paciente
    app.mostrar_frame("Paciente")
    
    # 3. Simular selección de síntomas
    modulo_paciente = app.frames["Paciente"]
    modulo_paciente.sintomas_vars['s1'].set(True)
    modulo_paciente.severidad_vars['s1'].set('severo')
    
    # 4. Realizar diagnóstico
    modulo_paciente.realizar_diagnostico()
    
    # 5. Verificar resultados
    assert len(modulo_paciente.historial_diagnosticos) > 0
```

### Pruebas en Prolog

```prolog
% test_medilogic.pl

:- consult('medilogic.pl').

test_calcular_afinidad :-
    calcular_afinidad(e1, [(s1, severo), (s2, moderado)], Afinidad),
    Afinidad > 70,
    write('✓ Test calcular_afinidad pasado'), nl.

test_medicamento_seguro :-
    medic amento_seguro(m1, [], []),
    write('✓ Test medicamento_seguro pasado'), nl.

% Ejecutar todos los tests
run_tests :-
    test_calcular_afinidad,
    test_medicamento_seguro,
    write('✓ Todos los tests pasaron'), nl.
```

### Casos de Prueba Clínicos

Ver documento: `docs/casos_clinicos.pdf`

**Casos incluidos**:
1. **Gripe común**: Tos + fiebre + dolor muscular
2. **Gastroenteritis**: Náuseas + vómito + diarrea + fiebre
3. **Angina**: Dolor de garganta + fiebre + malestar
4. **Caso con alergias**: Paciente alérgico a penicilina
5. **Caso con crónicas**: Paciente con diabetes e hipertensión

---

## Apéndices

### A. Glosario

- **Afinidad**: Porcentaje de coincidencia entre síntomas del paciente y enfermedad
- **Backtracking**: Mecanismo de Prolog para explorar soluciones alternativas
- **Hecho**: Declaración verdadera en Prolog (predating sin cuerpo)
- **Predicado**: Función/relación en Prolog
- **Regla**: Predicado con condiciones (cuerpo)
- **Unificación**: Proceso de igualar términos en Prolog

### B. Referencias

- SWI-Prolog Documentation: https://www.swi-prolog.org/pldoc/
- PySwip GitHub: https://github.com/yuce/pyswip
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- ReportLab User Guide: https://www.reportlab.com/docs/reportlab-userguide.pdf

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
**Autor**: [Tu Nombre]  
**Licencia**: MIT

---

© 2026 MediLogic - Sistema Experto Médico
