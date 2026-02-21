# Manual de Usuario - MediLogic

## Sistema Experto de Diagnóstico Médico Preliminar

---

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Inicio de la Aplicación](#inicio-de-la-aplicación)
5. [Módulo de Paciente](#módulo-de-paciente)
6. [Módulo de Administrador](#módulo-de-administrador)
7. [Preguntas Frecuentes](#preguntas-frecuentes)
8. [Soporte](#soporte)

---

## Introducción

MediLogic es un sistema experto diseñado para proporcionar diagnósticos médicos preliminares basados en síntomas reportados por el paciente. El sistema utiliza inteligencia artificial simbólica (Prolog) para analizar síntomas y sugerir posibles diagnósticos.

### ⚠️ Advertencia Importante
**Este sistema es únicamente para propósitos educativos y de apoyo diagnóstico preliminar. NO sustituye la consulta con un médico profesional. Siempre busque atención médica calificada para diagnósticos y tratamientos definitivos.**

---

## Requisitos del Sistema

### Hardware Mínimo
- Procesador: 1 GHz o superior
- RAM: 2 GB mínimo (4 GB recomendado)
- Espacio en disco: 500 MB
- Resolución de pantalla: 1024x768 o superior

### Software
- Sistema Operativo: Windows 7/8/10/11, Linux (Ubuntu 18.04+), macOS 10.12+
- Python 3.8 o superior
- SWI-Prolog 8.0 o superior
- Conexión a internet (solo para instalación y envío de correos)

---

## Instalación

### Paso 1: Instalar SWI-Prolog

#### Windows
1. Descargar desde: https://www.swi-prolog.org/download/stable
2. Ejecutar el instalador (.exe)
3. Seguir las instrucciones del asistente
4. El instalador configurará las variables de entorno automáticamente

#### Linux (Ubuntu/Debian)
```bash
sudo apt-add-repository ppa:swi-prolog/stable
sudo apt-get update
sudo apt-get install swi-prolog
```

#### macOS
```bash
brew install swi-prolog
```

### Paso 2: Instalar Python y Dependencias

1. Verificar Python instalado:
```bash
python --version
```

2. Navegar a la carpeta del proyecto:
```bash
cd P1
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Paso 3: Verificar Instalación
```bash
python test_sistema.py
```

---

## Inicio de la Aplicación

### Ejecutar MediLogic
```bash
python src/main.py
```

### Pantalla de Inicio
Al iniciar, verá la pantalla principal con dos opciones:
- **Módulo Paciente**: Para realizar consultas diagnósticas
- **Módulo Administrador**: Para gestionar la base de conocimiento (requiere autenticación)

---

## Módulo de Paciente

### 1. Acceso al Módulo
Desde la pantalla principal, click en el botón **"Módulo Paciente"**.

### 2. Ingreso de Síntomas

#### Paso 2.1: Seleccionar Síntomas
Los síntomas están organizados por sistema del cuerpo:
- ✅ **Sistema Respiratorio**: Tos, fiebre, dificultad respiratoria, etc.
- ✅ **Sistema Digestivo**: Náuseas, dolor abdominal, diarrea, etc.
- ✅ **Sistema Cardiovascular**: Palpitaciones, dolor en el pecho, etc.
- ✅ **Sistema Neurológico**: Dolor de cabeza, mareos, etc.

**Instrucciones**:
1. Marque la casilla de cada síntoma que experimenta
2. Para cada síntoma seleccionado, elija la severidad:
   - 🟢 **Leve**: Malestar tolerable
   - 🟡 **Moderado**: Malestar notable
   - 🔴 **Severo**: Malestar grave o muy intenso

#### Paso 2.2: Ingresar Alergias
En el campo "Alergias", escriba cualquier alergia conocida a medicamentos, separadas por comas.

**Ejemplo**:
```
penicilina, ibuprofeno
```

#### Paso 2.3: Seleccionar Enfermedades Crónicas
Marque cualquier enfermedad crónica preexistente:
- Diabetes
- Hipertensión
- Insuficiencia Renal
- Enfermedad Hepática
- Asma

### 3. Realizar Diagnóstico

Click en el botón **"🔍 Realizar Diagnóstico"**.

El sistema procesará los datos y mostrará:
- Lista de posibles diagnósticos ordenados por afinidad (%)
- Nivel de urgencia
- Medicamentos seguros recomendados
- Advertencias sobre contraindicaciones

### 4. Visualizar Resultados

Los resultados incluyen:
- **Fecha y hora del diagnóstico**
- **Datos ingresados**: Resumen de síntomas, alergias y enfermedades crónicas
- **Diagnósticos sugeridos**: Con porcentaje de afinidad
- **Gravedad**: Nivel de urgencia (leve/moderada/grave)
- **Advertencias**: Información importante sobre contraindicaciones

### 5. Descargar Informe PDF

Para guardar el diagnóstico:
1. Click en **"📥 Descargar PDF"**
2. Seleccionar ubicación para guardar
3. El archivo PDF se generará automáticamente

El PDF incluye:
- Encabezado profesional
- Todos los datos del paciente
- Diagnósticos detallados
- Advertencias legales

### 6. Ver Historial

Durante la sesión actual, puede ver diagnósticos anteriores:
1. Click en **"📋 Ver Historial"**
2. Se abrirá una ventana con todos los diagnósticos de la sesión
3. Puede revisar los datos de cada diagnóstico previo

### 7. Limpiar Formulario

Para iniciar una nueva consulta:
- Click en **"🗑️ Limpiar"**
- Todos los campos se resetearán

---

## Módulo de Administrador

### 1. Acceso al Módulo

#### Paso 1.1: Ingresar Credenciales
Desde la pantalla principal, click en **"Módulo Administrador"**.

**Credenciales por defecto**:
- Usuario: `admin` | Contraseña: `admin123`
- Usuario: `medico` | Contraseña: `medico123`

⚠️ **Nota de Seguridad**: Cambie estas credenciales en un entorno de producción.

### 2. Panel de Administración

El panel contiene 5 pestañas:

#### 🦠 Pestaña 1: Enfermedades
**Funciones**:
- Ver lista de todas las enfermedades en la base de conocimiento
- Agregar nueva enfermedad
- Editar información de enfermedad existente
- Eliminar enfermedad
- Filtrar por sistema del cuerpo

**Datos de una enfermedad**:
- ID único
- Nombre
- Descripción
- Sistema del cuerpo afectado
- Tipo (viral, bacterial, crónico, etc.)
- Gravedad (leve, moderada, grave)
- Síntomas asociados
- Medicamentos contraindicados

#### 🩺 Pestaña 2: Síntomas
**Funciones**:
- Ver lista de síntomas disponibles
- Agregar nuevo síntoma
- Editar síntoma existente
- Eliminar síntoma
- Asociar síntomas con enfermedades

**Datos de un síntoma**:
- ID único
- Nombre
- Descripción
- Sistema del cuerpo
- Peso diagnóstico (1-10)

#### 💊 Pestaña 3: Medicamentos
**Funciones**:
- Ver lista de medicamentos
- Agregar nuevo medicamento
- Editar información de medicamento
- Eliminar medicamento
- Gestionar contraindicaciones

**Datos de un medicamento**:
- ID único
- Nombre
- Tipo (analgésico, antibiótico, etc.)
- Dosis recomendada
- Contraindicaciones

#### 📝 Pestaña 4: Archivo Prolog
**Funciones**:
- Visualizar el contenido del archivo `.pl` de Prolog
- Editar directamente el código Prolog
- Exportar archivo `.pl`
- Recargar base de conocimiento

**Uso avanzado**:
- Permite modificación directa de reglas lógicas
- Útil para ajustar pesos de síntomas
- Requiere conocimiento de Prolog

#### 🤖 Pestaña 5: RPA (Automatización)
**Funciones**:
- Carga masiva de enfermedades desde archivo de texto
- Generación automática de informes
- Envío de notificaciones por correo electrónico

**Cómo usar**:
1. Preparar archivo de texto con formato específico (ver sección siguiente)
2. Click en **"📁 Seleccionar Archivo"**
3. Click en **"▶️ Procesar Archivo"**
4. El sistema cargará y clasificará automáticamente las enfermedades
5. Se generará un informe en texto plano
6. Opcionalmente, enviar informe por correo a administradores

### 3. Formato de Archivo para RPA

El archivo debe tener extensión `.txt` y seguir este formato:

```
ENFERMEDAD
ID: e9
Nombre: Neumonía Atípica
Descripcion: Infección pulmonar por bacterias atípicas
Sistema: respiratorio
Tipo: bacterial
Gravedad: grave
Sintomas: s1,s2,s15
Medicamentos_Contraindicados: m2
---
ENFERMEDAD
ID: e10
Nombre: Gastritis Aguda
Descripcion: Inflamación del revestimiento gástrico
Sistema: digestivo
Tipo: general
Gravedad: moderada
Sintomas: s6,s9
Medicamentos_Contraindicados: m2
---
```

**Campos obligatorios**:
- ID
- Nombre
- Sistema
- Tipo
- Gravedad

**Campos opcionales**:
- Descripcion
- Sintomas
- Medicamentos_Contraindicados

### 4. Envío de Informes por Correo

Para enviar informes automáticos:

1. **Configurar correo remitente**:
   - Usar una cuenta de Gmail
   - Generar contraseña de aplicación:
     - Ir a https://myaccount.google.com/apppasswords
     - Generar nueva contraseña para "MediLogic"
     - Usar esa contraseña (NO la contraseña normal de Gmail)

2. **Ingresar destinatarios**:
   - Separar múltiples direcciones con comas
   - Ejemplo: `admin1@correo.com, admin2@correo.com`

3. **Enviar**:
   - Click en **"📧 Enviar Informe"**
   - El sistema enviará el informe como adjunto

### 5. Cerrar Sesión

Para salir del módulo administrador:
- Click en **"← Cerrar Sesión"**
- Volverá a la pantalla de login

---

## Preguntas Frecuentes

### ¿Es necesario tener conexión a internet?
No durante el uso normal. Solo se requiere internet para:
- Instalación inicial de dependencias
- Envío de correos electrónicos desde el módulo RPA

### ¿Puedo usar el sistema sin instalar SWI-Prolog?
No. SWI-Prolog es esencial para el funcionamiento del motor de inferencia lógica.

### ¿Los diagnósticos son definitivos?
**NO**. Los diagnósticos son preliminares y educativos. Siempre consulte a un médico profesional.

### ¿Se guardan mis datos?
Los datos solo se almacenan durante la sesión actual. Al cerrar la aplicación, se eliminan. El sistema no tiene persistencia de datos de pacientes.

### ¿Cómo agrego más enfermedades o síntomas?
Use el Módulo de Administrador para agregar, editar o eliminar entidades médicas.

### ¿Puedo modificar las reglas de diagnóstico?
Sí, desde la pestaña "Archivo Prolog" en el módulo administrador. Requiere conocimientos de lógica Prolog.

### ¿Qué hago si obtengo un error al iniciar?
1. Ejecute `python test_sistema.py` para diagnóstico
2. Verifique que SWI-Prolog esté instalado correctamente
3. Confirme que todas las dependencias estén instaladas
4. Revise que la base de conocimiento no tenga errores de sintaxis

---

## Soporte

### Documentación Adicional
- **Manual Técnico**: Para información sobre arquitectura y desarrollo
- **Casos Clínicos**: Ejemplos de uso con casos reales

### Contacto
- **Curso**: Inteligencia Artificial 1 - 1S2026
- **Institución**: Universidad de San Carlos de Guatemala
- **GitHub**: Ver repositorio del proyecto

---

**Versión**: 1.0  
**Fecha**: Febrero 2026  
**Licencia**: MIT

---

© 2026 MediLogic - Sistema Experto de Diagnóstico Médico
