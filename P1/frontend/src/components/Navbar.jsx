import { Link, useNavigate } from 'react-router-dom';
import { FaHospital, FaSignOutAlt, FaUserMd } from 'react-icons/fa';
import { logout } from '../services/api';
import './Navbar.css';

function Navbar() {
  const navigate = useNavigate();
  const usuario = localStorage.getItem('usuario');

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <FaHospital className="logo-icon" />
          <span>MediLogic</span>
        </Link>
        
        <ul className="navbar-menu">
          <li><Link to="/">Inicio</Link></li>
          <li><Link to="/paciente">Módulo Paciente</Link></li>
          {usuario ? (
            <>
              <li><Link to="/admin">Administrador</Link></li>
              <li className="user-info">
                <FaUserMd className="user-icon" />
                <span className="user-name">{usuario}</span>
              </li>
              <li>
                <button onClick={handleLogout} className="btn-logout">
                  <FaSignOutAlt /> Cerrar Sesión
                </button>
              </li>
            </>
          ) : (
            <li><Link to="/login">Login</Link></li>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
