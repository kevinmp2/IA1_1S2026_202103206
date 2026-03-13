import { Link } from 'react-router-dom';
import { FaHeartbeat, FaFlask, FaShieldAlt, FaChevronRight, FaUserMd, FaUserCog, FaCheckCircle } from 'react-icons/fa';
import './Home.css';

function Home() {
  return (
    <div className="home">

      {/* ── HERO SPLIT ── */}
      <section className="hero-split">
        <div className="hero-left">
          <span className="hero-badge">Sistema Experto IA</span>
          <h1 className="hero-title">
            Diagnóstico<br />
            <span className="hero-accent">médico</span> basado<br />
            en lógica Prolog
          </h1>
          <p className="hero-subtitle">
            MediLogic analiza tus síntomas mediante un motor de inferencia simbólica
            y te ofrece un diagnóstico preliminar con medicamentos sugeridos.
          </p>
          <div className="hero-actions">
            <Link to="/paciente" className="btn-hero-primary">
              Iniciar diagnóstico <FaChevronRight />
            </Link>
            <Link to="/login" className="btn-hero-ghost">
              Panel administrador
            </Link>
          </div>
          <div className="hero-note">
            <FaShieldAlt />
            <span>Solo de uso preliminar · No reemplaza consulta médica</span>
          </div>
        </div>

        <div className="hero-right">
          <div className="diag-panel">
            <div className="diag-panel-header">
              <span className="diag-dot red" /><span className="diag-dot yellow" /><span className="diag-dot green" />
              <span className="diag-panel-title">motor_inferencia.pl</span>
            </div>
            <div className="diag-panel-body">
              <div className="diag-line comment">% Análisis de síntomas activo</div>
              <div className="diag-line"><span className="kw">diagnosticar</span>(<span className="str">Paciente</span>) <span className="op">:-</span></div>
              <div className="diag-line indent"><span className="kw">sintomas</span>(<span className="str">Paciente</span>, <span className="var">Lista</span>),</div>
              <div className="diag-line indent"><span className="kw">calcular_afinidad</span>(<span className="var">Lista</span>, <span className="var">Score</span>),</div>
              <div className="diag-line indent"><span className="kw">Score</span> <span className="op">&gt;</span> <span className="num">0.5</span>,</div>
              <div className="diag-line indent"><span className="kw">suggest_med</span>(<span className="str">Paciente</span>, <span className="var">_</span>).</div>
              <div className="diag-line mt">&nbsp;</div>
              <div className="diag-line result-line">
                <FaCheckCircle className="result-icon" />
                Resultado: <span className="result-enf">Gripe · 87.3%</span>
              </div>
              <div className="diag-line result-line">
                <FaCheckCircle className="result-icon dim" />
                Alternativa: <span className="result-alt">Resfriado · 61.0%</span>
              </div>
            </div>
          </div>

          <div className="hero-stats-col">
            <div className="stat-pill"><FaHeartbeat /><span>15+</span> enfermedades</div>
            <div className="stat-pill"><FaFlask /><span>15+</span> síntomas</div>
            <div className="stat-pill"><FaShieldAlt /><span>8+</span> medicamentos</div>
          </div>
        </div>
      </section>

      {/* ── CÓMO FUNCIONA ── */}
      <section className="how-section">
        <h2 className="section-title">¿Cómo funciona?</h2>
        <div className="steps-row">
          <div className="step">
            <div className="step-number">01</div>
            <h4>Ingresa tus síntomas</h4>
            <p>Selecciona los síntomas que presentas y su nivel de severidad.</p>
          </div>
          <div className="step-connector" />
          <div className="step">
            <div className="step-number">02</div>
            <h4>Motor de inferencia</h4>
            <p>Prolog evalúa reglas lógicas y calcula afinidad con cada enfermedad.</p>
          </div>
          <div className="step-connector" />
          <div className="step">
            <div className="step-number">03</div>
            <h4>Resultado y medicación</h4>
            <p>Obtienes diagnóstico preliminar con medicamentos sugeridos y PDF descargable.</p>
          </div>
        </div>
      </section>

      {/* ── MÓDULOS ── */}
      <section className="modules-section">
        <h2 className="section-title">Accede al sistema</h2>
        <div className="modules-row">

          <div className="module-card paciente-card">
            <div className="module-card-icon-wrap paciente-wrap">
              <FaUserMd />
            </div>
            <div className="module-card-body">
              <h3>Módulo Paciente</h3>
              <p>Describe tus síntomas y recibe un análisis diagnóstico preliminar generado por inteligencia artificial simbólica.</p>
              <ul className="module-features">
                <li><FaCheckCircle /> Diagnóstico por síntomas</li>
                <li><FaCheckCircle /> Medicamentos sugeridos</li>
                <li><FaCheckCircle /> Informe PDF descargable</li>
              </ul>
              <Link to="/paciente" className="module-btn paciente-btn">
                Acceder al módulo <FaChevronRight />
              </Link>
            </div>
          </div>

          <div className="module-card admin-card">
            <div className="module-card-icon-wrap admin-wrap">
              <FaUserCog />
            </div>
            <div className="module-card-body">
              <h3>Módulo Administrador</h3>
              <p>Gestiona enfermedades, síntomas y medicamentos. Edita la base de conocimiento Prolog y usa el módulo RPA.</p>
              <ul className="module-features">
                <li><FaCheckCircle /> CRUD de base de conocimiento</li>
                <li><FaCheckCircle /> Editor Prolog integrado</li>
                <li><FaCheckCircle /> Automatización RPA + correo</li>
              </ul>
              <Link to="/login" className="module-btn admin-btn">
                Iniciar sesión <FaChevronRight />
              </Link>
            </div>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Home;
