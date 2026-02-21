import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { FaVirus, FaFileMedical, FaPills, FaCode, FaRobot, FaSync } from 'react-icons/fa';
import {
  obtenerEnfermedades,
  obtenerSintomas,
  obtenerMedicamentos,
  obtenerArchivoProlog,
  guardarArchivoProlog,
  procesarRPA,
  enviarCorreoRPA
} from '../services/api';
import './Administrador.css';

function Administrador() {
  const navigate = useNavigate();
  const [tabActiva, setTabActiva] = useState('enfermedades');
  const [enfermedades, setEnfermedades] = useState([]);
  const [sintomas, setSintomas] = useState([]);
  const [medicamentos, setMedicamentos] = useState([]);
  const [codigoProlog, setCodigoProlog] = useState('');
  const [loading, setLoading] = useState(false);

  // RPA States
  const [archivoRPA, setArchivoRPA] = useState('');
  const [informeRPA, setInformeRPA] = useState('');
  const [logRPA, setLogRPA] = useState([]);
  const [emailRemitente, setEmailRemitente] = useState('');
  const [emailPassword, setEmailPassword] = useState('');
  const [emailDestinatarios, setEmailDestinatarios] = useState('');

  // Modal states
  const [mostrarModal, setMostrarModal] = useState(false);
  const [enfermedadEditando, setEnfermedadEditando] = useState(null);

  useEffect(() => {
    // Verificar autenticación
    const usuario = localStorage.getItem('usuario');
    if (!usuario) {
      toast.warning('Debe iniciar sesión');
      navigate('/login');
      return;
    }

    // Cargar datos al montar el componente
    cargarDatos();
    
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Solo ejecutar una vez al montar

  const cargarDatos = async () => {
    setLoading(true);
    try {
      const [resEnf, resSint, resMed, resProlog] = await Promise.all([
        obtenerEnfermedades(),
        obtenerSintomas(),
        obtenerMedicamentos(),
        obtenerArchivoProlog()
      ]);

      console.log('Datos cargados:', { 
        enfermedades: resEnf.data.data?.length || 0,
        sintomas: resSint.data.data?.length || 0,
        medicamentos: resMed.data.data?.length || 0
      });

      if (resEnf.data.success) {
        const enf = resEnf.data.data || [];
        setEnfermedades(enf);
        console.log('✓ Enfermedades recibidas:', enf.length);
      } else {
        console.warn('No se pudieron cargar enfermedades');
        setEnfermedades([]);
      }
      
      if (resSint.data.success) {
        const sint = resSint.data.data || [];
        setSintomas(sint);
        console.log('✓ Síntomas recibidos:', sint.length);
      } else {
        console.warn('No se pudieron cargar síntomas');
        setSintomas([]);
      }
      
      if (resMed.data.success) {
        const med = resMed.data.data || [];
        setMedicamentos(med);
        console.log('✓ Medicamentos recibidos:', med.length);
      } else {
        console.warn('No se pudieron cargar medicamentos');
        setMedicamentos([]);
      }
      
      if (resProlog.data.success) {
        setCodigoProlog(resProlog.data.data.contenido || '');
        console.log('✓ Código Prolog cargado');
      }
      
      console.log('✓ Carga completa');
    } catch (error) {
      console.error('✗ Error al cargar datos:', error);
      toast.error('Error al cargar algunos datos. Verifique que el backend esté funcionando.');
      // Inicializar estados vacíos en caso de error
      setEnfermedades([]);
      setSintomas([]);
      setMedicamentos([]);
    } finally {
      setLoading(false);
    }
  };

  const handleGuardarProlog = async () => {
    setLoading(true);
    try {
      const response = await guardarArchivoProlog({ contenido: codigoProlog });
      if (response.data.success) {
        toast.success('Archivo Prolog guardado y recargado');
      }
    } catch (error) {
      toast.error('Error al guardar: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleProcesarRPA = async () => {
    if (!archivoRPA.trim()) {
      toast.warning('Ingrese el contenido del archivo');
      return;
    }

    setLoading(true);
    try {
      const response = await procesarRPA({ archivo_contenido: archivoRPA });
      
      if (response.data.success) {
        setInformeRPA(response.data.data.informe);
        setLogRPA(response.data.data.log);
        toast.success(`${response.data.data.enfermedades_procesadas} enfermedades procesadas`);
      }
    } catch (error) {
      toast.error('Error al procesar: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleEnviarCorreo = async () => {
    if (!informeRPA) {
      toast.warning('Primero procese un archivo para generar el informe');
      return;
    }

    if (!emailRemitente || !emailPassword || !emailDestinatarios) {
      toast.warning('Complete todos los campos de correo');
      return;
    }

    setLoading(true);
    try {
      const destinatarios = emailDestinatarios.split(',').map(e => e.trim());
      
      const response = await enviarCorreoRPA({
        informe: informeRPA,
        destinatarios,
        remitente: emailRemitente,
        password: emailPassword
      });

      if (response.data.success) {
        toast.success('Correo enviado exitosamente');
      }
    } catch (error) {
      toast.error('Error al enviar correo: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleNuevaEnfermedad = () => {
    toast.info('Funcionalidad en desarrollo. Por ahora puede editar el archivo Prolog directamente en la pestaña "Prolog"');
  };

  const handleEditarEnfermedad = (enf) => {
    toast.info('Funcionalidad en desarrollo. Por ahora puede editar el archivo Prolog directamente en la pestaña "Prolog"');
  };

  const handleEliminarEnfermedad = (enf) => {
    toast.info('Funcionalidad en desarrollo. Por ahora puede editar el archivo Prolog directamente en la pestaña "Prolog"');
  };

  const renderEnfermedades = () => (
    <div className="tab-content">
      <div className="tab-header">
        <h2>Gestión de Enfermedades</h2>
        <span className="count-badge">{enfermedades.length} registros</span>
      </div>
      <button className="btn btn-primary mb-20" onClick={handleNuevaEnfermedad}>+ Nueva Enfermedad</button>
      
      {loading ? (
        <div className="text-center">
          <p>Cargando datos...</p>
        </div>
      ) : enfermedades.length === 0 ? (
        <div className="alert alert-info">
          <p>No hay enfermedades registradas. El backend debe estar corriendo para mostrar los datos.</p>
          <p>Ejecuta: <code>python backend/app.py</code></p>
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Sistema</th>
                <th>Tipo</th>
                <th>Gravedad</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {enfermedades.map(enf => (
                <tr key={enf.id}>
                  <td>{enf.id}</td>
                  <td>{enf.nombre}</td>
                  <td>{enf.sistema}</td>
                  <td>{enf.tipo}</td>
                  <td>{enf.gravedad}</td>
                  <td>
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEditarEnfermedad(enf)}>Editar</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleEliminarEnfermedad(enf)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );

  const renderSintomas = () => (
    <div className="tab-content">
      <div className="tab-header">
        <h2>Gestión de Síntomas</h2>
        <span className="count-badge">{sintomas.length} registros</span>
      </div>
      <button className="btn btn-primary mb-20" onClick={() => toast.info('Funcionalidad en desarrollo')}>+ Nuevo Síntoma</button>
      
      {sintomas.length === 0 ? (
        <div className="alert alert-info">
          <p>No hay síntomas registrados. Asegúrate de que el backend esté corriendo.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Sistema</th>
                <th>Descripción</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {sintomas.map(sint => (
                <tr key={sint.id}>
                  <td>{sint.id}</td>
                  <td>{sint.nombre}</td>
                  <td>{sint.sistema}</td>
                  <td>{sint.descripcion}</td>
                  <td>
                    <button className="btn btn-sm btn-secondary" onClick={() => toast.info('Funcionalidad en desarrollo')}>Editar</button>
                    <button className="btn btn-sm btn-danger" onClick={() => toast.info('Funcionalidad en desarrollo')}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );

  const renderMedicamentos = () => (
    <div className="tab-content">
      <div className="tab-header">
        <h2>Gestión de Medicamentos</h2>
        <span className="count-badge">{medicamentos.length} registros</span>
      </div>
      <button className="btn btn-primary mb-20" onClick={() => toast.info('Funcionalidad en desarrollo')}>+ Nuevo Medicamento</button>
      
      {medicamentos.length === 0 ? (
        <div className="alert alert-info">
          <p>No hay medicamentos registrados. Asegúrate de que el backend esté corriendo.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Principio</th>
                <th>Tipo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {medicamentos.map(med => (
                <tr key={med.id}>
                  <td>{med.id}</td>
                  <td>{med.nombre}</td>
                  <td>{med.principio}</td>
                  <td>{med.tipo}</td>
                  <td>
                    <button className="btn btn-sm btn-secondary" onClick={() => toast.info('Funcionalidad en desarrollo')}>Editar</button>
                    <button className="btn btn-sm btn-danger" onClick={() => toast.info('Funcionalidad en desarrollo')}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );

  const renderProlog = () => (
    <div className="tab-content">
      <h2>Editor de Archivo Prolog</h2>
      <p className="subtitle">Edite directamente el archivo de base de conocimiento</p>
      
      <textarea
        className="prolog-editor"
        value={codigoProlog}
        onChange={(e) => setCodigoProlog(e.target.value)}
        spellCheck={false}
      />
      
      <div className="flex gap-10 mt-20">
        <button
          className="btn btn-success"
          onClick={handleGuardarProlog}
          disabled={loading}
        >
          💾 Guardar y Recargar
        </button>
        <button className="btn btn-secondary" onClick={cargarDatos}>
          🔄 Descartar Cambios
        </button>
      </div>
    </div>
  );

  const renderRPA = () => (
    <div className="tab-content">
      <h2>Automatización RPA</h2>
      
      <div className="card mb-20">
        <h3>Carga Masiva de Enfermedades</h3>
        <p>Pegue el contenido del archivo de texto con el formato especificado:</p>
        
        <textarea
          className="form-textarea"
          rows="10"
          value={archivoRPA}
          onChange={(e) => setArchivoRPA(e.target.value)}
          placeholder="ENFERMEDAD&#10;ID: e9&#10;Nombre: ...&#10;---"
        />
        
        <button
          className="btn btn-primary mt-20"
          onClick={handleProcesarRPA}
          disabled={loading}
        >
          ▶️ Procesar Archivo
        </button>
      </div>

      {informeRPA && (
        <div className="card mb-20">
          <h3>Informe Generado</h3>
          <pre className="informe-output">{informeRPA}</pre>
        </div>
      )}

      {logRPA.length > 0 && (
        <div className="card mb-20">
          <h3>Log de Operaciones</h3>
          <div className="log-output">
            {logRPA.map((log, i) => (
              <div key={i} className="log-line">{log}</div>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <h3>Enviar Informe por Correo</h3>
        
        <div className="form-group">
          <label className="form-label">Correo Remitente (Gmail):</label>
          <input
            type="email"
            className="form-input"
            value={emailRemitente}
            onChange={(e) => setEmailRemitente(e.target.value)}
            placeholder="tu-correo@gmail.com"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Contraseña de Aplicación:</label>
          <input
            type="password"
            className="form-input"
            value={emailPassword}
            onChange={(e) => setEmailPassword(e.target.value)}
            placeholder="Contraseña de aplicación de Gmail"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Destinatarios (separados por coma):</label>
          <input
            type="text"
            className="form-input"
            value={emailDestinatarios}
            onChange={(e) => setEmailDestinatarios(e.target.value)}
            placeholder="admin1@correo.com, admin2@correo.com"
          />
        </div>

        <button
          className="btn btn-success"
          onClick={handleEnviarCorreo}
          disabled={loading || !informeRPA}
        >
          📧 Enviar Correo
        </button>
      </div>
    </div>
  );

  if (loading && !enfermedades.length) {
    return (
      <div className="container text-center" style={{ paddingTop: '100px' }}>
        <div className="spinner"></div>
        <p>Cargando datos...</p>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <div className="container">
        <div className="admin-header">
          <div>
            <h1>Panel de Administración</h1>
            <p className="subtitle">Gestione la base de conocimiento del sistema MediLogic</p>
          </div>
          <div className="admin-header-actions">
            <button 
              className="btn btn-secondary btn-reload" 
              onClick={cargarDatos}
              disabled={loading}
              title="Recargar datos"
            >
              <FaSync className={loading ? 'spinning' : ''} /> 
              {loading ? 'Cargando...' : 'Recargar'}
            </button>
            <div className="admin-user-badge">
              <div className="admin-user-avatar">
                {localStorage.getItem('usuario')?.charAt(0).toUpperCase() || 'A'}
              </div>
              <div className="admin-user-info">
                <span className="admin-user-role">
                  {localStorage.getItem('rol') || 'Administrador'}
                </span>
                <span className="admin-user-name">
                  {localStorage.getItem('nombre_completo') || localStorage.getItem('usuario') || 'Usuario'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab ${tabActiva === 'enfermedades' ? 'active' : ''}`}
            onClick={() => setTabActiva('enfermedades')}
          >
            <FaVirus /> Enfermedades
          </button>
          <button
            className={`tab ${tabActiva === 'sintomas' ? 'active' : ''}`}
            onClick={() => setTabActiva('sintomas')}
          >
            <FaFileMedical /> Síntomas
          </button>
          <button
            className={`tab ${tabActiva === 'medicamentos' ? 'active' : ''}`}
            onClick={() => setTabActiva('medicamentos')}
          >
            <FaPills /> Medicamentos
          </button>
          <button
            className={`tab ${tabActiva === 'prolog' ? 'active' : ''}`}
            onClick={() => setTabActiva('prolog')}
          >
            <FaCode /> Prolog
          </button>
          <button
            className={`tab ${tabActiva === 'rpa' ? 'active' : ''}`}
            onClick={() => setTabActiva('rpa')}
          >
            <FaRobot /> RPA
          </button>
        </div>

        <div className="card">
          {tabActiva === 'enfermedades' && renderEnfermedades()}
          {tabActiva === 'sintomas' && renderSintomas()}
          {tabActiva === 'medicamentos' && renderMedicamentos()}
          {tabActiva === 'prolog' && renderProlog()}
          {tabActiva === 'rpa' && renderRPA()}
        </div>
      </div>
    </div>
  );
}

export default Administrador;
