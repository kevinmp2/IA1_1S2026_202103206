import { Link } from 'react-router-dom';
import { FaUserMd, FaUserCog, FaBrain } from 'react-icons/fa';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <h1>MediLogic</h1>
        <p className="tagline">Sistema Experto de Diagnóstico Médico Preliminar</p>
        <p className="description">
          Utilizando inteligencia artificial simbólica y lógica computacional para 
          proporcionar diagnósticos preliminares basados en síntomas.
        </p>
      </div>

      <div className="features">
        <div className="feature-card">
          <FaBrain className="feature-icon" />
          <h3>Motor de Inferencia Prolog</h3>
          <p>Sistema experto basado en reglas lógicas que analiza síntomas y sugiere diagnósticos.</p>
        </div>
        <div className="feature-card">
          <FaUserMd className="feature-icon" />
          <h3>Análisis Inteligente</h3>
          <p>Considera severidad de síntomas, alergias y enfermedades crónicas del paciente.</p>
        </div>
        <div className="feature-card">
          <FaUserCog className="feature-icon" />
          <h3>Gestión Completa</h3>
          <p>Panel administrativo para gestionar base de conocimiento y automatización RPA.</p>
        </div>
      </div>

      <div className="modules-section">
        <h2>Módulos del Sistema</h2>
        <div className="modules-grid">
          <Link to="/paciente" className="module-card module-paciente">
            <FaUserMd className="module-icon" />
            <h3>Módulo Paciente</h3>
            <p>Ingrese sus síntomas y obtenga un diagnóstico preliminar</p>
            <button className="btn btn-primary">Acceder →</button>
          </Link>

          <Link to="/login" className="module-card module-admin">
            <FaUserCog className="module-icon" />
            <h3>Módulo Administrador</h3>
            <p>Gestione la base de conocimiento médico</p>
            <button className="btn btn-secondary">Login →</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
