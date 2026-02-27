import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Configurar Axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ==================== ENDPOINTS PÚBLICOS ====================

export const healthCheck = () => api.get('/health');

export const obtenerSintomas = () => api.get('/sintomas');

export const obtenerEnfermedades = () => api.get('/enfermedades');

export const obtenerMedicamentos = () => api.get('/medicamentos');

export const obtenerEnfermedadesCronicas = () => api.get('/enfermedades-cronicas');

// ==================== MÓDULO PACIENTE ====================

export const diagnosticar = (data) => api.post('/diagnosticar', data);

export const generarPDF = (data) => api.post('/generar-pdf', data, {
  responseType: 'blob' // Recibir PDF como blob directamente
});

// ==================== AUTENTICACIÓN ====================

export const login = (credentials) => api.post('/login', credentials);

export const logout = () => {
  // Limpiar toda la información del usuario
  localStorage.removeItem('token');
  localStorage.removeItem('usuario');
  localStorage.removeItem('rol');
  localStorage.removeItem('nombre_completo');
  localStorage.removeItem('permisos');
};

// ==================== MÓDULO ADMINISTRADOR ====================

export const crearEnfermedad = (data) => api.post('/admin/enfermedad', data);

export const editarEnfermedad = (id, data) => api.put(`/admin/enfermedad/${id}`, data);

export const eliminarEnfermedad = (id) => api.delete(`/admin/enfermedad/${id}`);

export const obtenerArchivoProlog = () => api.get('/admin/prolog');

export const guardarArchivoProlog = (data) => api.post('/admin/prolog', data);

// ==================== MÓDULO RPA ====================

export const procesarRPA = (data) => api.post('/rpa/procesar', data);

export const enviarCorreoRPA = (data) => api.post('/rpa/enviar-correo', data);

export default api;
