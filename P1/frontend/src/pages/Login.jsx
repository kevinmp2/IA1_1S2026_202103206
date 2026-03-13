import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { FaUserLock } from 'react-icons/fa';
import { login } from '../services/api';
import './Login.css';

function Login() {
  const [usuario, setUsuario] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!usuario || !password) {
      toast.warning('Complete todos los campos');
      return;
    }

    setLoading(true);

    try {
      const response = await login({ usuario, password });

      if (response.data.success) {
        // Guardar token y usuario en localStorage
        const userData = response.data.data;
        localStorage.setItem('token', userData.token);
        localStorage.setItem('usuario', userData.usuario);
        localStorage.setItem('rol', userData.rol || 'administrador');
        localStorage.setItem('nombre_completo', userData.nombre_completo || userData.usuario);
        if (userData.permisos) {
          localStorage.setItem('permisos', JSON.stringify(userData.permisos));
        }

        toast.success(`¡Bienvenido, ${userData.nombre_completo || userData.usuario}! Iniciando sesión...`, {
          autoClose: 2000
        });
        
        // Redirigir al panel de administrador después de un breve delay
        setTimeout(() => {
          navigate('/admin');
        }, 1000);
      }
    } catch (error) {
      if (error.response?.status === 401) {
        toast.error('Credenciales incorrectas');
      } else {
        toast.error('Error al iniciar sesión: ' + (error.response?.data?.error || error.message));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <FaUserLock className="login-icon" />
            <h1>Acceso Administrador</h1>
            <p>MediLogic Sistema Experto</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label className="form-label">Usuario</label>
              <input
                type="text"
                className="form-input"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value)}
                placeholder="Ingrese su usuario"
                autoFocus
              />
            </div>

            <div className="form-group">
              <label className="form-label">Contraseña</label>
              <input
                type="password"
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ingrese su contraseña"
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={loading}
            >
              {loading ? 'Ingresando...' : 'Ingresar'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
