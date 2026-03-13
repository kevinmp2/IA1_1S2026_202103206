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
  cargarArchivoProlog,
  procesarRPA,
  enviarCorreoRPA,
  verificarCredencialesConfiguradas,
  crearEnfermedad,
  editarEnfermedad,
  eliminarEnfermedad,
  crearSintoma,
  editarSintoma,
  eliminarSintoma,
  crearMedicamento,
  editarMedicamento,
  eliminarMedicamento
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
  const [credencialesConfiguradas, setCredencialesConfiguradas] = useState({
    remitente: false,
    password: false
  });
  const [nombreArchivoSeleccionado, setNombreArchivoSeleccionado] = useState('');
  const [archivoPrologSeleccionado, setArchivoPrologSeleccionado] = useState(null);
  const [nombreArchivoPrologSeleccionado, setNombreArchivoPrologSeleccionado] = useState('');

  // Modal states
  const [mostrarModal, setMostrarModal] = useState(false);
  const [tipoModal, setTipoModal] = useState(''); // 'enfermedad', 'sintoma', 'medicamento'
  const [modoModal, setModoModal] = useState('crear'); // 'crear' o 'editar'
  const [itemEditando, setItemEditando] = useState(null);
  
  // Form states
  const [formData, setFormData] = useState({
    id: '',
    nombre: '',
    descripcion: '',
    sistema: '',
    tipo: '',
    gravedad: '',
    principio: ''
  });

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
    verificarCredenciales();
    
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Solo ejecutar una vez al montar

  const verificarCredenciales = async () => {
    try {
      const response = await verificarCredencialesConfiguradas();
      if (response.data) {
        setCredencialesConfiguradas({
          remitente: response.data.remitente_configurado,
          password: response.data.password_configurado
        });
        
        // Pre-llenar el remitente si está configurado
        if (response.data.remitente) {
          setEmailRemitente(response.data.remitente);
        }
      }
    } catch (error) {
      console.error('Error al verificar credenciales:', error);
    }
  };

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

  const handleExportarProlog = () => {
    if (!codigoProlog) {
      toast.warning('No hay contenido para exportar');
      return;
    }
    const blob = new Blob([codigoProlog], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'medilogic.pl';
    link.click();
    URL.revokeObjectURL(url);
    toast.success('Archivo medilogic.pl exportado correctamente');
  };

  const handleSeleccionarArchivoProlog = (event) => {
    const archivo = event.target.files[0];

    if (!archivo) {
      setArchivoPrologSeleccionado(null);
      setNombreArchivoPrologSeleccionado('');
      return;
    }

    if (!archivo.name.toLowerCase().endsWith('.pl')) {
      toast.warning('Por favor seleccione un archivo Prolog (.pl)');
      event.target.value = '';
      setArchivoPrologSeleccionado(null);
      setNombreArchivoPrologSeleccionado('');
      return;
    }

    setArchivoPrologSeleccionado(archivo);
    setNombreArchivoPrologSeleccionado(archivo.name);
  };

  const handleCargarArchivoProlog = async () => {
    if (!archivoPrologSeleccionado) {
      toast.warning('Seleccione un archivo .pl primero');
      return;
    }

    const confirmar = window.confirm(
      'Esta acción fusionará el archivo cargado con la base actual. ¿Desea continuar?'
    );

    if (!confirmar) {
      return;
    }

    setLoading(true);
    try {
      const response = await cargarArchivoProlog(archivoPrologSeleccionado);
      if (response.data.success) {
        setCodigoProlog(response.data.data?.contenido || '');
        await cargarDatos();
        const insertados = response.data.data?.insertados ?? 0;
        const actualizados = response.data.data?.actualizados ?? 0;
        toast.success(`Fusión completada: ${insertados} insertados, ${actualizados} actualizados`);

        setArchivoPrologSeleccionado(null);
        setNombreArchivoPrologSeleccionado('');
        const input = document.getElementById('file-upload-prolog');
        if (input) {
          input.value = '';
        }
      }
    } catch (error) {
      toast.error('Error al cargar archivo .pl: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCargarArchivo = (event) => {
    const archivo = event.target.files[0];
    
    if (!archivo) {
      setNombreArchivoSeleccionado('');
      return;
    }

    // Verificar que sea un archivo de texto
    if (!archivo.name.endsWith('.txt')) {
      toast.warning('Por favor seleccione un archivo de texto (.txt)');
      event.target.value = '';
      setNombreArchivoSeleccionado('');
      return;
    }

    // Guardar nombre del archivo
    setNombreArchivoSeleccionado(archivo.name);

    // Leer el contenido del archivo
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const contenido = e.target.result;
      setArchivoRPA(contenido);
      toast.success(`Archivo "${archivo.name}" cargado exitosamente`);
    };
    
    reader.onerror = () => {
      toast.error('Error al leer el archivo');
      setNombreArchivoSeleccionado('');
    };
    
    reader.readAsText(archivo, 'UTF-8');
  };

  const handleLimpiarRPA = () => {
    setArchivoRPA('');
    setNombreArchivoSeleccionado('');
    setInformeRPA('');
    setLogRPA([]);
    
    // Resetear el input de archivo
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
      fileInput.value = '';
    }
    
    toast.info('Formulario limpiado');
  };

  const handleProcesarRPA = async () => {
    if (!archivoRPA.trim()) {
      toast.warning('Ingrese el contenido del archivo');
      return;
    }

    setLoading(true);
    try {
      const response = await procesarRPA({ 
        archivo_contenido: archivoRPA,
        guardar_en_prolog: true 
      });
      
      if (response.data.success) {
        setInformeRPA(response.data.data.informe);
        setLogRPA(response.data.data.log);
        
        const { enfermedades_procesadas, prolog_actualizado, error_prolog } = response.data.data;
        
        if (prolog_actualizado) {
          toast.success(`✓ ${enfermedades_procesadas} enfermedad(es) procesada(s) y guardada(s) en la base de conocimiento`);
          // Recargar enfermedades para reflejar los cambios
          setTimeout(() => cargarDatos(), 500);
        } else if (error_prolog) {
          toast.warning(`${enfermedades_procesadas} enfermedad(es) procesada(s), pero hubo un error al actualizar Prolog: ${error_prolog}`);
        } else {
          toast.success(`${enfermedades_procesadas} enfermedad(es) procesada(s) (informe generado)`);
        }
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

    if (!emailDestinatarios) {
      toast.warning('Ingrese al menos un destinatario');
      return;
    }

    // Solo validar credenciales si no están configuradas en el servidor
    if (!credencialesConfiguradas.remitente && !emailRemitente) {
      toast.warning('Ingrese el correo remitente o configúrelo en el archivo .env del servidor');
      return;
    }

    if (!credencialesConfiguradas.password && !emailPassword) {
      toast.warning('Ingrese la contraseña de aplicación o configúrela en el archivo .env del servidor');
      return;
    }

    setLoading(true);
    try {
      const destinatarios = emailDestinatarios.split(',').map(e => e.trim());
      
      // Construir el objeto de datos dinámicamente
      const datosCorreo = {
        informe: informeRPA,
        destinatarios
      };
      
      // Solo incluir credenciales si no están vacías (si están vacías, el backend usará .env)
      if (emailRemitente) {
        datosCorreo.remitente = emailRemitente;
      }
      if (emailPassword) {
        datosCorreo.password = emailPassword;
      }
      
      const response = await enviarCorreoRPA(datosCorreo);

      if (response.data.success) {
        toast.success('Correo enviado exitosamente');
      }
    } catch (error) {
      toast.error('Error al enviar correo: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  // ==================== FUNCIONES MODALES ====================
  
  const abrirModal = (tipo, modo, item = null) => {
    setTipoModal(tipo);
    setModoModal(modo);
    setItemEditando(item);
    
    if (modo === 'editar' && item) {
      setFormData({
        id: item.id || '',
        nombre: item.nombre || '',
        descripcion: item.descripcion || '',
        sistema: item.sistema || '',
        tipo: item.tipo || '',
        gravedad: item.gravedad || '',
        principio: item.principio || ''
      });
    } else {
      setFormData({
        id: '',
        nombre: '',
        descripcion: '',
        sistema: '',
        tipo: '',
        gravedad: '',
        principio: ''
      });
    }
    
    setMostrarModal(true);
  };
  
  const cerrarModal = () => {
    setMostrarModal(false);
    setTipoModal('');
    setModoModal('crear');
    setItemEditando(null);
    setFormData({
      id: '',
      nombre: '',
      descripcion: '',
      sistema: '',
      tipo: '',
      gravedad: '',
      principio: ''
    });
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSubmitModal = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      let resultado;
      
      if (tipoModal === 'enfermedad') {
        if (modoModal === 'crear') {
          resultado = await crearEnfermedad(formData);
        } else {
          resultado = await editarEnfermedad(itemEditando.id, formData);
        }
        await cargarEnfermedades();
      } else if (tipoModal === 'sintoma') {
        if (modoModal === 'crear') {
          resultado = await crearSintoma(formData);
        } else {
          resultado = await editarSintoma(itemEditando.id, formData);
        }
        await cargarSintomas();
      } else if (tipoModal === 'medicamento') {
        if (modoModal === 'crear') {
          resultado = await crearMedicamento(formData);
        } else {
          resultado = await editarMedicamento(itemEditando.id, formData);
        }
        await cargarMedicamentos();
      }
      
      if (resultado?.data?.success) {
        toast.success(resultado.data.message || 'Operación exitosa');
        cerrarModal();
      } else {
        toast.error(resultado?.data?.error || 'Error en la operación');
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error(error.response?.data?.error || 'Error al procesar la solicitud');
    } finally {
      setLoading(false);
    }
  };

  // ==================== FUNCIONES ENFERMEDADES ====================

  const handleNuevaEnfermedad = () => {
    abrirModal('enfermedad', 'crear');
  };

  const handleEditarEnfermedad = (enf) => {
    abrirModal('enfermedad', 'editar', enf);
  };

  const handleEliminarEnfermedad = async (enf) => {
    if (window.confirm(`¿Está seguro de eliminar la enfermedad "${enf.nombre}"?`)) {
      setLoading(true);
      try {
        const resultado = await eliminarEnfermedad(enf.id);
        if (resultado?.data?.success) {
          toast.success('Enfermedad eliminada correctamente');
          await cargarEnfermedades();
        } else {
          toast.error(resultado?.data?.error || 'Error al eliminar');
        }
      } catch (error) {
        console.error('Error:', error);
        toast.error(error.response?.data?.error || 'Error al eliminar la enfermedad');
      } finally {
        setLoading(false);
      }
    }
  };
  
  const cargarEnfermedades = async () => {
    try {
      const res = await obtenerEnfermedades();
      if (res.data.success) {
        setEnfermedades(res.data.data || []);
      }
    } catch (error) {
      console.error('Error al cargar enfermedades:', error);
    }
  };
  
  // ==================== FUNCIONES SÍNTOMAS ====================
  
  const handleNuevoSintoma = () => {
    abrirModal('sintoma', 'crear');
  };

  const handleEditarSintoma = (sint) => {
    abrirModal('sintoma', 'editar', sint);
  };

  const handleEliminarSintoma = async (sint) => {
    if (window.confirm(`¿Está seguro de eliminar el síntoma "${sint.nombre}"?`)) {
      setLoading(true);
      try {
        const resultado = await eliminarSintoma(sint.id);
        if (resultado?.data?.success) {
          toast.success('Síntoma eliminado correctamente');
          await cargarSintomas();
        } else {
          toast.error(resultado?.data?.error || 'Error al eliminar');
        }
      } catch (error) {
        console.error('Error:', error);
        toast.error(error.response?.data?.error || 'Error al eliminar el síntoma');
      } finally {
        setLoading(false);
      }
    }
  };
  
  const cargarSintomas = async () => {
    try {
      const res = await obtenerSintomas();
      if (res.data.success) {
        setSintomas(res.data.data || []);
      }
    } catch (error) {
      console.error('Error al cargar síntomas:', error);
    }
  };
  
  // ==================== FUNCIONES MEDICAMENTOS ====================
  
  const handleNuevoMedicamento = () => {
    abrirModal('medicamento', 'crear');
  };

  const handleEditarMedicamento = (med) => {
    abrirModal('medicamento', 'editar', med);
  };

  const handleEliminarMedicamento = async (med) => {
    if (window.confirm(`¿Está seguro de eliminar el medicamento "${med.nombre}"?`)) {
      setLoading(true);
      try {
        const resultado = await eliminarMedicamento(med.id);
        if (resultado?.data?.success) {
          toast.success('Medicamento eliminado correctamente');
          await cargarMedicamentos();
        } else {
          toast.error(resultado?.data?.error || 'Error al eliminar');
        }
      } catch (error) {
        console.error('Error:', error);
        toast.error(error.response?.data?.error || 'Error al eliminar el medicamento');
      } finally {
        setLoading(false);
      }
    }
  };
  
  const cargarMedicamentos = async () => {
    try {
      const res = await obtenerMedicamentos();
      if (res.data.success) {
        setMedicamentos(res.data.data || []);
      }
    } catch (error) {
      console.error('Error al cargar medicamentos:', error);
    }
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
      <button className="btn btn-primary mb-20" onClick={handleNuevoSintoma}>+ Nuevo Síntoma</button>
      
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
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEditarSintoma(sint)}>Editar</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleEliminarSintoma(sint)}>Eliminar</button>
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
      <button className="btn btn-primary mb-20" onClick={handleNuevoMedicamento}>+ Nuevo Medicamento</button>
      
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
                    <button className="btn btn-sm btn-secondary" onClick={() => handleEditarMedicamento(med)}>Editar</button>
                    <button className="btn btn-sm btn-danger" onClick={() => handleEliminarMedicamento(med)}>Eliminar</button>
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

      <div className="card mb-20">
        <h3>Cargar archivo .pl</h3>
        <p>Seleccione un archivo Prolog para fusionarlo con la base actual y recargar el conocimiento.</p>

        <div className="form-group">
          <label className="form-label">📁 Archivo .pl:</label>
          <div className="file-upload-wrapper">
            <input
              type="file"
              id="file-upload-prolog"
              accept=".pl"
              onChange={handleSeleccionarArchivoProlog}
              className="file-upload-input"
            />
            <label htmlFor="file-upload-prolog" className="file-upload-label">
              <span className="file-upload-icon">📂</span>
              <span>Seleccionar archivo .pl</span>
            </label>
          </div>
          {nombreArchivoPrologSeleccionado && (
            <div className="file-name-display">{nombreArchivoPrologSeleccionado}</div>
          )}
        </div>

        <button
          className="btn btn-primary"
          onClick={handleCargarArchivoProlog}
          disabled={loading || !archivoPrologSeleccionado}
        >
          ⬆️ Fusionar y Actualizar Base
        </button>
      </div>
      
      <textarea
        className="prolog-editor"
        value={codigoProlog}
        onChange={(e) => setCodigoProlog(e.target.value)}
        spellCheck={false}
      />
      
      <div className="flex gap-10 mt-20">
        <button
          className="btn btn-success"
          onClick={handleExportarProlog}
          disabled={loading}
        >
          📥 Exportar .pl
        </button>
        <button
          className="btn btn-primary"
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
        <p>Cargue un archivo de texto o pegue el contenido manualmente con el formato especificado:</p>
        
        <div className="form-group">
          <label className="form-label">📁 Cargar desde archivo:</label>
          <div className="file-upload-wrapper">
            <input
              type="file"
              id="file-upload"
              accept=".txt"
              onChange={handleCargarArchivo}
              className="file-upload-input"
            />
            <label htmlFor="file-upload" className="file-upload-label">
              <span className="file-upload-icon">📂</span>
              <span>Seleccionar archivo .txt</span>
            </label>
          </div>
          {nombreArchivoSeleccionado && (
            <div className="file-name-display">
              {nombreArchivoSeleccionado}
            </div>
          )}
        </div>
        
        <div className="form-group">
          <label className="form-label">✍️ O pegue el contenido aquí:</label>
          <textarea
            className="form-textarea"
            rows="10"
            value={archivoRPA}
            onChange={(e) => setArchivoRPA(e.target.value)}
            placeholder="ENFERMEDAD&#10;ID: e9&#10;Nombre: ...&#10;---"
          />
        </div>
        
        <div className="flex gap-10 mt-20">
          <button
            className="btn btn-primary"
            onClick={handleProcesarRPA}
            disabled={loading}
          >
            ▶️ Procesar Archivo
          </button>
          <button
            className="btn btn-secondary"
            onClick={handleLimpiarRPA}
            disabled={loading}
          >
            🗑️ Limpiar
          </button>
        </div>
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
        
        {(credencialesConfiguradas.remitente && credencialesConfiguradas.password)}
        
        <div className="form-group">
          <label className="form-label">
            Correo Remitente (Gmail):
          </label>
          <input
            type="email"
            className="form-input"
            value={emailRemitente}
            onChange={(e) => setEmailRemitente(e.target.value)}
            placeholder={credencialesConfiguradas.remitente ? "Configurado en servidor" : "tu-correo@gmail.com"}
            disabled={credencialesConfiguradas.remitente}
          />
        </div>

        <div className="form-group">
          <label className="form-label">
            Contraseña de Aplicación:
            {credencialesConfiguradas.password && <span style={{color: '#28a745', marginLeft: '5px'}}></span>}
          </label>
          <input
            type="password"
            className="form-input"
            value={emailPassword}
            onChange={(e) => setEmailPassword(e.target.value)}
            placeholder={credencialesConfiguradas.password ? "Configurada en servidor" : "Contraseña de aplicación de Gmail"}
            disabled={credencialesConfiguradas.password}
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
        
        {/* Modal para CRUD */}
        {mostrarModal && (
          <div className="modal-overlay" onClick={cerrarModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>
                  {modoModal === 'crear' ? 'Agregar' : 'Editar'} {tipoModal === 'enfermedad' ? 'Enfermedad' : tipoModal === 'sintoma' ? 'Síntoma' : 'Medicamento'}
                </h2>
                <button className="btn-close" onClick={cerrarModal}>×</button>
              </div>
              
              <form onSubmit={handleSubmitModal}>
                <div className="modal-body">
                  {/* Campo ID */}
                  <div className="form-group">
                    <label>ID *</label>
                    <input
                      type="text"
                      name="id"
                      value={formData.id}
                      onChange={handleInputChange}
                      disabled={modoModal === 'editar'}
                      required
                      placeholder="Ej: e1, s1, m1"
                    />
                  </div>
                  
                  {/* Campo Nombre */}
                  <div className="form-group">
                    <label>Nombre *</label>
                    <input
                      type="text"
                      name="nombre"
                      value={formData.nombre}
                      onChange={handleInputChange}
                      required
                      placeholder="Nombre del elemento"
                    />
                  </div>
                  
                  {/* Campo Descripción */}
                  <div className="form-group">
                    <label>Descripción</label>
                    <textarea
                      name="descripcion"
                      value={formData.descripcion}
                      onChange={handleInputChange}
                      rows="3"
                      placeholder="Descripción detallada"
                    />
                  </div>
                  
                  {/* Campo Sistema */}
                  <div className="form-group">
                    <label>Sistema *</label>
                    <select
                      name="sistema"
                      value={formData.sistema}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Seleccione un sistema</option>
                      <option value="respiratorio">Respiratorio</option>
                      <option value="digestivo">Digestivo</option>
                      <option value="cardiovascular">Cardiovascular</option>
                      <option value="nervioso">Nervioso</option>
                      <option value="endocrino">Endocrino</option>
                      <option value="muscular">Muscular</option>
                      <option value="oseo">Óseo</option>
                      <option value="inmunologico">Inmunológico</option>
                      <option value="general">General</option>
                    </select>
                  </div>
                  
                  {/* Campos específicos para Enfermedad */}
                  {tipoModal === 'enfermedad' && (
                    <>
                      <div className="form-group">
                        <label>Tipo *</label>
                        <select
                          name="tipo"
                          value={formData.tipo}
                          onChange={handleInputChange}
                          required
                        >
                          <option value="">Seleccione un tipo</option>
                          <option value="viral">Viral</option>
                          <option value="bacteriana">Bacteriana</option>
                          <option value="cronica">Crónica</option>
                          <option value="degenerativa">Degenerativa</option>
                          <option value="autoinmune">Autoinmune</option>
                          <option value="genetica">Genética</option>
                        </select>
                      </div>
                      
                      <div className="form-group">
                        <label>Gravedad *</label>
                        <select
                          name="gravedad"
                          value={formData.gravedad}
                          onChange={handleInputChange}
                          required
                        >
                          <option value="">Seleccione gravedad</option>
                          <option value="leve">Leve</option>
                          <option value="moderada">Moderada</option>
                          <option value="grave">Grave</option>
                          <option value="critica">Crítica</option>
                        </select>
                      </div>
                    </>
                  )}
                  
                  {/* Campos específicos para Medicamento */}
                  {tipoModal === 'medicamento' && (
                    <>
                      <div className="form-group">
                        <label>Principio Activo</label>
                        <input
                          type="text"
                          name="principio"
                          value={formData.principio}
                          onChange={handleInputChange}
                          placeholder="Principio activo del medicamento"
                        />
                      </div>
                      
                      <div className="form-group">
                        <label>Tipo *</label>
                        <select
                          name="tipo"
                          value={formData.tipo}
                          onChange={handleInputChange}
                          required
                        >
                          <option value="">Seleccione un tipo</option>
                          <option value="analgesico">Analgésico</option>
                          <option value="antibiotico">Antibiótico</option>
                          <option value="antiinflamatorio">Antiinflamatorio</option>
                          <option value="antipiretico">Antipirético</option>
                          <option value="antiviral">Antiviral</option>
                        </select>
                      </div>
                    </>
                  )}
                </div>
                
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={cerrarModal}>
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Guardando...' : 'Guardar'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Administrador;
