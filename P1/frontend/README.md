# Frontend React - MediLogic

## Aplicación web moderna con React 18 + Vite

### Ejecutar Frontend

```bash
cd frontend
npm install
npm run dev
```

Aplicación en: http://localhost:3000

### Estructura

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── Navbar.jsx
│   │   └── Navbar.css
│   ├── pages/              # Páginas principales
│   │   ├── Home.jsx        # Página de inicio
│   │   ├── Paciente.jsx    # Módulo de paciente
│   │   ├── Login.jsx       # Login de administrador
│   │   └── Administrador.jsx  # Panel de administración
│   ├── services/           # Servicios API
│   │   └── api.js          # Cliente Axios
│   ├── App.jsx             # Componente principal
│   ├── main.jsx            # Entry point
│   └── index.css           # Estilos globales
├── index.html              # HTML principal
├── vite.config.js          # Configuración Vite
└── package.json
```

### Scripts Disponibles

```bash
npm run dev      # Modo desarrollo
npm run build    # Compilar para producción
npm run preview  # Vista previa de build
npm run lint     # Linter ESLint
```

### Tecnologías

- **React 18** - UI Library
- **React Router DOM** - Navegación
- **Axios** - Cliente HTTP
- **React Icons** - Iconos
- **React Toastify** - Notificaciones
- **Vite** - Build tool

### Páginas

#### Home (`/`)
Página de bienvenida con descripción del sistema.

#### Paciente (`/paciente`)
- Formulario de síntomas
- Selección de severidad
- Alergias y enfermedades crónicas
- Resultados de diagnóstico
- Descarga de PDF

#### Login (`/login`)
Autenticación para administradores.

#### Administrador (`/admin`)
- Gestión de enfermedades
- Gestión de síntomas
- Gestión de medicamentos
- Editor de archivo Prolog
- Módulo RPA

### API Service

El archivo `services/api.js` maneja todas las peticiones HTTP al backend:

```javascript
import { diagnosticar, login, obtenerSintomas } from './services/api';

// Ejemplo de uso
const resultado = await diagnosticar({
  sintomas: [...],
  alergias: [...],
  cronicas: [...]
});
```

### Configuración API

Por defecto, el frontend se conecta a:
```
http://localhost:5000/api
```

Para cambiar, editar `vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://tu-backend:puerto',
    changeOrigin: true,
  }
}
```

### Estilos

- CSS modular por componente
- Variables CSS globales en `index.css`
- Sistema de colores definido en `:root`
- Responsive design

### Build para Producción

```bash
npm run build
```

Los archivos compilados estarán en `dist/` y pueden servirse con cualquier servidor web:

```bash
npm run preview  # Ver build localmente
```

O con servidor estático:
```bash
npx serve -s dist
```

### Notas de Desarrollo

- Hot Module Replacement (HMR) habilitado
- Proxy configurado para desarrollo
- React DevTools recomendado
- Token JWT guardado en localStorage
- CORS debe estar habilitado en el backend

### Solución de Problemas

**Error de conexión con API:**
- Verificar que el backend esté corriendo en puerto 5000
- Verificar configuración de proxy en `vite.config.js`

**Dependencias no encontradas:**
```bash
rm -rf node_modules
npm install
```

**Build falla:**
Verificar que no haya errores de lint:
```bash
npm run lint
```
