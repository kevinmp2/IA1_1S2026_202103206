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

### Advertencia Importante
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
![PantallaInicio](/P1/img/pantalla_inicio.png)

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

![Paciente](/P1/img/paciente_1.png)
![Paciente](/P1/img/paciente_2.png)


### 3. Realizar Diagnóstico

Click en el botón **"🔍 Realizar Diagnóstico"**.

El sistema procesará los datos y mostrará:
- Lista de posibles diagnósticos ordenados por afinidad (%)
- Nivel de urgencia
- Medicamentos seguros recomendados

![Resultados](/P1/img/diagnostico_1.png)


### 4. Descargar Informe PDF

Para guardar el diagnóstico:
1. Click en **"📥 Descargar PDF"**
2. Seleccionar ubicación para guardar
3. El archivo PDF se generará automáticamente

El PDF incluye:
- Encabezado profesional
- Diagnósticos detallados
- Advertencias legales

![PDF](/P1/img/informe.png)

### 6. Limpiar Formulario

Para iniciar una nueva consulta:
- Click en **"🗑️ Limpiar"**
- Todos los campos se resetearán

![Limpiar](/P1/img/limpiar.png)

---

## Módulo de Administrador

### 1. Acceso al Módulo

#### Paso 1.1: Ingresar Credenciales
Desde la pantalla principal, click en **"Módulo Administrador"**.



![Login](/P1/img/login_admin.png)

### 2. Panel de Administración

El panel contiene 5 pestañas:

![Admin](/P1/img/panel_admin.png)

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

![Enfermedades](/P1/img/enfermedades.png)


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

![Síntomas](/P1/img/sintomas.png)

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

![Medicamentos](/P1/img/medicamentos.png)

#### 📝 Pestaña 4: Archivo Prolog
**Funciones**:
- Visualizar el contenido del archivo `.pl` de Prolog
- Editar directamente el código Prolog
- Exportar archivo `.pl`
- Recargar base de conocimiento
- Cargar archivo Prolog `.pl`

**Uso avanzado**:
- Permite modificación directa de reglas lógicas
- Útil para ajustar pesos de síntomas
- Requiere conocimiento de Prolog

![Prolog](/P1/img/prolog.png)

#### 🤖 Pestaña 5: RPA (Automatización)
**Funciones**:
- Carga masiva de enfermedades desde archivo de texto
- Generación automática de informes
- Envío de notificaciones por correo electrónico

**Cómo usar**:
1. Preparar archivo de texto con formato específico
2. Click en **"📁 Seleccionar Archivo"**
3. Click en **"▶️ Procesar Archivo"**
4. El sistema cargará y clasificará automáticamente las enfermedades
5. Se generará un informe en texto plano
6. Enviar informe por correo a administradores

![RPA](/P1/img/rpa.png)
![RPA](/P1/img/procesar_1.png)

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

1. **Ingresar destinatarios**:
   - Separar múltiples direcciones con comas
   - Ejemplo: `admin1@correo.com, admin2@correo.com`

2. **Enviar**:
   - Click en **"📧 Enviar Informe"**
   - El sistema enviará el informe como adjunto


![Correo](/P1/img/procesar_2.png)

### 5. Cerrar Sesión

Para salir del módulo administrador:
- Click en **"← Cerrar Sesión"**
- Volverá a la pantalla de login

![Logout](/P1/img/cerrar_sesion.png)


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

---

© 2026 MediLogic - Sistema Experto de Diagnóstico Médico
