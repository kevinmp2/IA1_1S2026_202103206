# Instrucciones para Configuración de GitHub

## Paso 1: Crear el Repositorio

1. Ve a https://github.com y haz login
2. Click en el botón "+" en la esquina superior derecha y selecciona "New repository"
3. Configura el repositorio:
   - **Repository name**: `IA1_1S2026_[TuCarnet]` (reemplaza [TuCarnet] con tu número de carnet)
   - **Description**: "Proyecto 1 - Sistema Experto MediLogic - Inteligencia Artificial 1"
   - **Visibility**: Private (por ahora, cambiar a Public después de la evaluación)
   - **Initialize repository**: NO marcar "Add a README file" (ya lo tienes)
4. Click en "Create repository"

## Paso 2: Inicializar Git Localmente

Abre una terminal en la carpeta `P1` y ejecuta:

```bash
# Inicializar repositorio
git init

# Agregar archivos al staging
git add .

# Hacer el primer commit
git commit -m "Initial commit: Estructura completa del proyecto MediLogic"

# Renombrar rama a main (si es necesario)
git branch -M main

# Agregar el repositorio remoto
git remote add origin https://github.com/[TuUsuario]/IA1_1S2026_[TuCarnet].git

# Subir cambios
git push -u origin main
```

## Paso 3: Agregar Colaboradores

1. En tu repositorio de GitHub, ve a "Settings"
2. En el menú lateral, selecciona "Collaborators"
3. Click en "Add people"
4. Agrega los usuarios:
   - `roberto1206`
   - `ixchop98`
5. Envía las invitaciones

## Paso 4: Crear la Estructura de Carpetas P1

Si aún no has creado la carpeta P1 dentro del repositorio:

```bash
# Crear carpeta P1 si no existe
mkdir P1

# Mover todos los archivos del proyecto a P1
# (o clonar directamente en la estructura correcta)

# Hacer commit
git add .
git commit -m "Organizar proyecto en carpeta P1"
git push
```

## Paso 5: Configuración para el Proyecto

### Archivo .gitignore
Ya está incluido en el proyecto con las siguientes exclusiones:
- Archivos Python compilados (*.pyc, __pycache__)
- Entornos virtuales (venv/, env/)
- Archivos del sistema operativo (.DS_Store, Thumbs.db)
- Archivos de IDEs (.vscode/, .idea/)

### Branch Protection (Opcional pero Recomendado)

Para proteger la rama main:
1. Ve a Settings > Branches
2. Agrega una regla para "main"
3. Habilita:
   - "Require a pull request before merging"
   - "Require approvals"

## Comandos Git Útiles

```bash
# Ver estado de los archivos
git status

# Ver historial de commits
git log --oneline

# Crear una nueva rama para desarrollo
git checkout -b desarrollo

# Cambiar entre ramas
git checkout main

# Ver ramas
git branch

# Actualizar desde remoto
git pull origin main

# Subir cambios
git add .
git commit -m "Descripción del cambio"
git push origin main

# Crear un tag para la entrega
git tag -a v1.0 -m "Entrega 1 - Febrero 26"
git push origin v1.0
```

## Paso 6: Preparar para la Entrega

### Entrega 1 (26 de febrero)
```bash
# Asegurarse de que todo esté actualizado
git add .
git commit -m "Entrega 1: Sistema completo con RPA"
git push

# Crear tag
git tag -a Entrega1 -m "Primera entrega - 26 febrero 2026"
git push origin Entrega1
```

### Después de la Evaluación
```bash
# Cambiar repositorio a público
# GitHub > Settings > General > Danger Zone > Change visibility > Make public
```

## Verificación Final

Asegúrate de que el repositorio contenga:
- ✅ Todo el código fuente en la carpeta P1/
- ✅ README.md con documentación completa
- ✅ LICENSE (MIT)
- ✅ requirements.txt con todas las dependencias
- ✅ .gitignore configurado correctamente
- ✅ Colaboradores agregados
- ✅ Estructura de carpetas organizada

## Estructura Final en GitHub

```
IA1_1S2026_[Carnet]/
└── P1/
    ├── src/
    ├── base_conocimiento/
    ├── datos/
    ├── docs/
    ├── README.md
    ├── requirements.txt
    ├── LICENSE
    └── .gitignore
```

## Notas Importantes

1. **NO** subir archivos grandes (videos, datasets grandes)
2. **SÍ** subir todo el código fuente
3. **SÍ** incluir documentación clara
4. Para el video de demostración del RPA:
   - Súbelo a YouTube o Google Drive
   - Agrega el enlace en el README.md
5. Mantén commits descriptivos y frecuentes
6. Haz push regularmente para no perder trabajo

## Solución de Problemas

### Error: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/[TuUsuario]/IA1_1S2026_[TuCarnet].git
```

### Error: "Updates were rejected because the remote contains work"
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Olvidaste agregar un archivo al .gitignore
```bash
git rm --cached nombre_archivo
git commit -m "Remover archivo del tracking"
git push
```
