import { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { FaSearch, FaTrash, FaDownload, FaHistory } from 'react-icons/fa';
import { obtenerSintomas, obtenerEnfermedadesCronicas, diagnosticar, generarPDF } from '../services/api';
import './Paciente.css';

function Paciente() {
  const [sintomas, setSintomas] = useState([]);
  const [cronicas, setCronicas] = useState([]);
  const [sintomasSeleccionados, setSintomasSeleccionados] = useState([]);
  const [alergias, setAlergias] = useState('');
  const [cronicasSeleccionadas, setCronicasSeleccionadas] = useState([]);
  const [diagnosticos, setDiagnosticos] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingDatos, setLoadingDatos] = useState(true);
  const [historial, setHistorial] = useState([]);

  useEffect(() => {
    cargarDatos();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Solo ejecutar una vez al montar

  const cargarDatos = async () => {
    setLoadingDatos(true);
    console.log('🔄 Cargando datos iniciales del módulo de paciente...');
    
    try {
      const [resSintomas, resCronicas] = await Promise.all([
        obtenerSintomas(),
        obtenerEnfermedadesCronicas()
      ]);

      // Procesar síntomas
      if (resSintomas?.data?.success && Array.isArray(resSintomas.data.data)) {
        setSintomas(resSintomas.data.data);
        console.log(`✓ Síntomas cargados: ${resSintomas.data.data.length}`);
      } else {
        setSintomas([]);
        console.warn('No se pudieron cargar síntomas (success=false o datos inválidos)');
      }

      // Procesar enfermedades crónicas
      if (resCronicas?.data?.success && Array.isArray(resCronicas.data.data)) {
        setCronicas(resCronicas.data.data);
        console.log(`✓ Enfermedades crónicas cargadas: ${resCronicas.data.data.length}`);
      } else {
        setCronicas([]);
        console.warn('No se pudieron cargar enfermedades crónicas (success=false o datos inválidos)');
      }

      console.log('✓ Datos cargados correctamente:', { 
        sintomas: resSintomas?.data?.data?.length || 0, 
        cronicas: resCronicas?.data?.data?.length || 0 
      });
    } catch (error) {
      console.error('✗ Error al cargar datos:', error);
      toast.error('Error al cargar datos: ' + (error.response?.data?.error || error.message));
      
      // Asegurar que los arrays se inicialicen incluso si hay error
      setSintomas([]);
      setCronicas([]);
    } finally {
      setLoadingDatos(false);
    }
  };

  const handleSintomaChange = (sintomaId, sintomaNombre, checked) => {
    if (checked) {
      setSintomasSeleccionados([
        ...sintomasSeleccionados,
        { id: sintomaId, nombre: sintomaNombre, severidad: 'moderado' }
      ]);
    } else {
      setSintomasSeleccionados(
        sintomasSeleccionados.filter(s => s.id !== sintomaId)
      );
    }
  };

  const handleSeveridadChange = (sintomaId, severidad) => {
    setSintomasSeleccionados(
      sintomasSeleccionados.map(s =>
        s.id === sintomaId ? { ...s, severidad } : s
      )
    );
  };

  const handleCronicaChange = (cronicaId, checked) => {
    if (checked) {
      setCronicasSeleccionadas([...cronicasSeleccionadas, cronicaId]);
    } else {
      setCronicasSeleccionadas(cronicasSeleccionadas.filter(c => c !== cronicaId));
    }
  };

  const handleDiagnosticar = async () => {
    if (sintomasSeleccionados.length === 0) {
      toast.warning('Debe seleccionar al menos un síntoma');
      return;
    }

    setLoading(true);

    try {
      const alergiasArray = alergias
        .split(',')
        .map(a => a.trim())
        .filter(a => a.length > 0);

      const response = await diagnosticar({
        sintomas: sintomasSeleccionados,
        alergias: alergiasArray,
        cronicas: cronicasSeleccionadas
      });

      if (response.data.success) {
        setDiagnosticos(response.data.data);
        
        // Agregar al historial
        setHistorial([
          ...historial,
          {
            fecha: new Date(),
            diagnosticos: response.data.data
          }
        ]);

        toast.success('Diagnóstico realizado correctamente');
      }
    } catch (error) {
      toast.error('Error al realizar diagnóstico: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleLimpiar = () => {
    setSintomasSeleccionados([]);
    setAlergias('');
    setCronicasSeleccionadas([]);
    setDiagnosticos(null);
  };

  const handleDescargarPDF = async () => {
    if (!diagnosticos) {
      toast.warning('No hay diagnóstico para descargar');
      return;
    }

    try {
      // Hacer petición con responseType blob para recibir el PDF directamente
      const response = await generarPDF({
        datos_paciente: {
          fecha: new Date().toLocaleDateString(),
          hora: new Date().toLocaleTimeString(),
          sintomas: sintomasSeleccionados,
          alergias: alergias.split(',').map(a => a.trim()).filter(a => a),
          cronicas: cronicasSeleccionadas
        },
        diagnosticos: diagnosticos.diagnosticos
      });

      // El PDF viene directamente en response.data como blob
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      
      // Crear enlace temporal para descargar
      const link = document.createElement('a');
      link.href = url;
      link.download = `informe_medilogic_${new Date().getTime()}.pdf`;
      document.body.appendChild(link);
      link.click();
      
      // Limpiar
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('✓ PDF descargado correctamente');
    } catch (error) {
      toast.error('Error al generar PDF: ' + (error.response?.data?.error || error.message));
    }
  };

  // Agrupar síntomas por sistema
  const sintomasPorSistema = sintomas.reduce((acc, sintoma) => {
    const sistema = sintoma.sistema || 'general';
    if (!acc[sistema]) {
      acc[sistema] = [];
    }
    acc[sistema].push(sintoma);
    return acc;
  }, {});

  return (
    <div className="paciente-page">
      <div className="container">
        <h1>Módulo de Paciente</h1>
        <p className="subtitle">Complete el formulario con sus síntomas para obtener un diagnóstico preliminar</p>

        <div className="paciente-grid">
          {/* Formulario */}
          <div className="formulario-section">
            <div className="card">
              <h2 className="card-title">Selección de Síntomas</h2>
              
              {loadingDatos ? (
                <div className="loading-message">
                  <p>Cargando síntomas...</p>
                </div>
              ) : sintomas.length === 0 ? (
                <div className="empty-message">
                  <p>No se pudieron cargar los síntomas. Por favor, recargue la página.</p>
                </div>
              ) : (
                Object.entries(sintomasPorSistema).map(([sistema, sintomasSistema]) => (
                  <div key={sistema} className="sistema-group">
                    <h3 className="sistema-title">
                      {sistema.charAt(0).toUpperCase() + sistema.slice(1)}
                    </h3>
                    
                    {sintomasSistema.map(sintoma => {
                    const seleccionado = sintomasSeleccionados.find(s => s.id === sintoma.id);
                    
                    return (
                      <div key={sintoma.id} className="sintoma-item">
                        <div className="checkbox-group">
                          <input
                            type="checkbox"
                            id={sintoma.id}
                            checked={!!seleccionado}
                            onChange={(e) =>
                              handleSintomaChange(sintoma.id, sintoma.nombre, e.target.checked)
                            }
                          />
                          <label htmlFor={sintoma.id}>{sintoma.nombre}</label>
                        </div>
                        
                        {seleccionado && (
                          <div className="severidad-select">
                            <select
                              value={seleccionado.severidad}
                              onChange={(e) =>
                                handleSeveridadChange(sintoma.id, e.target.value)
                              }
                              className="form-select"
                            >
                              <option value="leve">🟢 Leve</option>
                              <option value="moderado">🟡 Moderado</option>
                              <option value="severo">🔴 Severo</option>
                            </select>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ))
              )}
            </div>

            <div className="card">
              <h2 className="card-title">Información Adicional</h2>
              
              <div className="form-group">
                <label className="form-label">Alergias (separadas por comas):</label>
                <input
                  type="text"
                  className="form-input"
                  value={alergias}
                  onChange={(e) => setAlergias(e.target.value)}
                  placeholder="Ej: penicilina, ibuprofeno"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Enfermedades Crónicas:</label>
                {cronicas.map(cronica => (
                  <div key={cronica.id} className="checkbox-group">
                    <input
                      type="checkbox"
                      id={cronica.id}
                      checked={cronicasSeleccionadas.includes(cronica.id)}
                      onChange={(e) =>
                        handleCronicaChange(cronica.id, e.target.checked)
                      }
                    />
                    <label htmlFor={cronica.id}>{cronica.nombre}</label>
                  </div>
                ))}
              </div>
            </div>

            <div className="acciones">
              <button
                className="btn btn-primary"
                onClick={handleDiagnosticar}
                disabled={loading}
              >
                <FaSearch /> {loading ? 'Procesando...' : 'Realizar Diagnóstico'}
              </button>
              
              <button className="btn btn-danger" onClick={handleLimpiar}>
                <FaTrash /> Limpiar
              </button>
            </div>
          </div>

          {/* Resultados */}
          <div className="resultados-section">
            {diagnosticos ? (
              <div className="card">
                <h2 className="card-title">Resultados del Diagnóstico</h2>
                
                <div className="diagnosticos-list">
                  {diagnosticos.diagnosticos && diagnosticos.diagnosticos.length > 0 ? (
                    diagnosticos.diagnosticos.map((diag, index) => (
                      <div key={index} className="diagnostico-item">
                        <div className="diagnostico-header">
                          <h3>{diag.nombre}</h3>
                          <span className={`badge badge-${diag.gravedad}`}>{diag.gravedad}</span>
                        </div>
                        <p><strong>Afinidad:</strong> {diag.afinidad}%</p>
                        <p><strong>Nivel de urgencia:</strong> {diag.urgencia}</p>
                        
                        {diag.medicamentos && diag.medicamentos.length > 0 && (
                          <div className="medicamentos-section">
                            <strong>Medicamentos sugeridos:</strong>
                            <ul>
                              {diag.medicamentos.map((med, i) => (
                                <li key={i}>
                                  <strong>{med.nombre}</strong> ({med.tipo})
                                  <span className="efectividad"> - Efectividad: {med.efectividad}/10</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <p className="no-diagnosticos">
                      No se encontraron diagnósticos compatibles con los síntomas ingresados.
                    </p>
                  )}
                </div>

                <div className="alert alert-warning mt-20">
                  <strong>⚠️ Advertencia:</strong> Este es un diagnóstico preliminar para propósitos educativos. 
                  NO sustituye la consulta médica profesional.
                </div>

                <button className="btn btn-success mt-20" onClick={handleDescargarPDF}>
                  <FaDownload /> Descargar PDF
                </button>
              </div>
            ) : (
              <div className="card placeholder-card">
                <FaHistory className="placeholder-icon" />
                <p>Complete el formulario y presione "Realizar Diagnóstico" para ver los resultados</p>
              </div>
            )}

            {historial.length > 0 && (
              <div className="card">
                <h2 className="card-title">Historial de Sesión</h2>
                <p className="historial-count">{historial.length} diagnóstico(s) en esta sesión</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Paciente;
