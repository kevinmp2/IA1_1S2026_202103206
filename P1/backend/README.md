# Backend Flask - MediLogic

## API REST para el sistema experto

### Ejecutar Backend

```bash
cd backend
python app.py
```

Servidor en: http://localhost:5000

### Endpoints Disponibles

#### Públicos
- `GET /api/health` - Health check
- `GET /api/sintomas` - Obtener síntomas
- `GET /api/enfermedades` - Obtener enfermedades
- `GET /api/medicamentos` - Obtener medicamentos
- `GET /api/enfermedades-cronicas` - Obtener enfermedades crónicas

#### Paciente
- `POST /api/diagnosticar` - Realizar diagnóstico
- `POST /api/generar-pdf` - Generar informe PDF

#### Autenticación
- `POST /api/login` - Login de administrador

#### Administrador (requiere autenticación)
- `POST /api/admin/enfermedad` - Crear enfermedad
- `PUT /api/admin/enfermedad/<id>` - Editar enfermedad
- `DELETE /api/admin/enfermedad/<id>` - Eliminar enfermedad
- `GET /api/admin/prolog` - Obtener archivo Prolog
- `POST /api/admin/prolog` - Guardar archivo Prolog

#### RPA
- `POST /api/rpa/procesar` - Procesar archivo RPA
- `POST /api/rpa/enviar-correo` - Enviar informe por correo

### Configuración

El servidor usa:
- **Puerto**: 5000
- **CORS**: Habilitado para desarrollo
- **Debug**: True (solo desarrollo)

### Dependencias

Ver `requirements.txt` en la raíz del proyecto.

### Estructura

```
backend/
└── app.py  # Servidor Flask con todos los endpoints
```

### Probar API

#### Con curl:
```bash
curl http://localhost:5000/api/health
```

#### Con navegador:
```
http://localhost:5000/api/sintomas
```

### Notas

- El backend requiere que SWI-Prolog esté instalado
- Usa la carpeta `src/` para módulos compartidos
- La base de conocimiento está en `base_conocimiento/medilogic.pl`
