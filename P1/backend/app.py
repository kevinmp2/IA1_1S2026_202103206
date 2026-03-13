"""
Backend Flask para MediLogic
API REST para el sistema 
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.prolog_engine import PrologEngine
from utils.pdf_generator import PDFGenerator
from modulos.rpa import RPA_MediLogic

app = Flask(__name__)
CORS(app)

# Configurar encoding para JSON
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# Inicializar motor Prolog
prolog_engine = PrologEngine()
pdf_generator = PDFGenerator()
rpa = RPA_MediLogic()

# Usuarios para autenticaciOn
USUARIOS = {
    'admin': {
        'password': 'admin123',
        'nombre_completo': 'Administrador Sistema',
        'rol': 'administrador',
        'permisos': ['lectura', 'escritura', 'admin']
    },
    'medico': {
        'password': 'medico123',
        'nombre_completo': 'Dr. Médico General',
        'rol': 'medico',
        'permisos': ['lectura', 'escritura']
    }
}


# ==================== ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del servidor"""
    return jsonify({
        'status': 'ok',
        'message': 'MediLogic API está funcionando'
    })


@app.route('/api/sintomas', methods=['GET'])
def obtener_sintomas():
    """Obtener lista de síntomas disponibles"""
    try:
        sintomas = prolog_engine.obtener_sintomas()
        return jsonify({
            'success': True,
            'data': sintomas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enfermedades', methods=['GET'])
def obtener_enfermedades():
    """Obtener lista de enfermedades"""
    try:
        enfermedades = prolog_engine.obtener_enfermedades()
        return jsonify({
            'success': True,
            'data': enfermedades
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/medicamentos', methods=['GET'])
def obtener_medicamentos():
    """Obtener lista de medicamentos"""
    try:
        medicamentos = prolog_engine.obtener_medicamentos()
        return jsonify({
            'success': True,
            'data': medicamentos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enfermedades-cronicas', methods=['GET'])
def obtener_enfermedades_cronicas():
    """Obtener lista de enfermedades crónicas"""
    try:
        cronicas = prolog_engine.obtener_enfermedades_cronicas()
        return jsonify({
            'success': True,
            'data': cronicas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== MÓDULO PACIENTE ====================

@app.route('/api/diagnosticar', methods=['POST'])
def diagnosticar():
    """
    Realizar diagnóstico médico
    
    Body:
    {
        "sintomas": [{"id": "s1", "nombre": "Tos", "severidad": "severo"}, ...],
        "alergias": ["penicilina", ...],
        "cronicas": ["ec1", ...]
    }
    """
    try:
        data = request.get_json()
        
        sintomas = data.get('sintomas', [])
        alergias = data.get('alergias', [])
        cronicas = data.get('cronicas', [])
        
        # Validar datos
        if not sintomas:
            return jsonify({
                'success': False,
                'error': 'Debe seleccionar al menos un síntoma'
            }), 400
        
        # Realizar diagnóstico
        diagnosticos = prolog_engine.diagnosticar(
            [(s['id'], s['nombre'], s['severidad']) for s in sintomas],
            alergias,
            cronicas
        )
        
        return jsonify({
            'success': True,
            'data': {
                'diagnosticos': diagnosticos,
                'sintomas': sintomas,
                'alergias': alergias,
                'cronicas': cronicas
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generar-pdf', methods=['POST'])
def generar_pdf():
    """
    Generar informe PDF y enviarlo directamente (sin guardar en servidor)
    
    Body:
    {
        "datos_paciente": {...},
        "diagnosticos": [...]
    }
    """
    try:
        data = request.get_json()
        
        datos_paciente = data.get('datos_paciente', {})
        diagnosticos = data.get('diagnosticos', [])
        
        # Extraer datos del paciente
        sintomas = datos_paciente.get('sintomas', [])
        alergias = datos_paciente.get('alergias', [])
        cronicas = datos_paciente.get('cronicas', [])
        
        # Generar PDF en memoria
        pdf_buffer = pdf_generator.generar_informe_en_memoria(
            sintomas,
            alergias,
            cronicas,
            diagnosticos
        )
        
        if pdf_buffer is None:
            return jsonify({
                'success': False,
                'error': 'Error al generar el PDF'
            }), 500
        
        # Generar nombre de archivo con timestamp
        nombre_archivo = f"informe_medilogic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Enviar directamente desde memoria
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== AUTENTICACIÓN ====================

@app.route('/api/login', methods=['POST'])
def login():
    """
    Autenticar usuario administrador
    
    Body:
    {
        "usuario": "admin",
        "password": "admin123"
    }
    """
    try:
        data = request.get_json()
        
        usuario = data.get('usuario', '')
        password = data.get('password', '')
        
        if usuario in USUARIOS and USUARIOS[usuario]['password'] == password:
            user_data = USUARIOS[usuario]
            # En producción: generar JWT token
            return jsonify({
                'success': True,
                'data': {
                    'usuario': usuario,
                    'nombre_completo': user_data['nombre_completo'],
                    'rol': user_data['rol'],
                    'permisos': user_data['permisos'],
                    'token': 'dummy_token_' + usuario  # Placeholder
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Credenciales incorrectas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== MÓDULO ADMINISTRADOR ====================

@app.route('/api/admin/enfermedad', methods=['POST'])
def crear_enfermedad():
    """Crear nueva enfermedad"""
    try:
        # TODO: Verificar autenticación
        data = request.get_json()
        
        id_enf = data.get('id')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        sistema = data.get('sistema')
        tipo = data.get('tipo')
        gravedad = data.get('gravedad')
        
        # Agregar a Prolog
        success = prolog_engine.agregar_enfermedad(
            id_enf, nombre, descripcion, sistema, tipo, gravedad
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Enfermedad creada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al crear enfermedad'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/enfermedad/<id>', methods=['PUT'])
def editar_enfermedad(id):
    """Editar enfermedad existente"""
    try:
        data = request.get_json()
        
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        sistema = data.get('sistema')
        tipo = data.get('tipo')
        gravedad = data.get('gravedad')
        
        resultado = prolog_engine.editar_enfermedad(
            id, nombre, descripcion, sistema, tipo, gravedad
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Enfermedad actualizada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/enfermedad/<id>', methods=['DELETE'])
def eliminar_enfermedad(id):
    """Eliminar enfermedad"""
    try:
        resultado = prolog_engine.eliminar_enfermedad(id)
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Enfermedad eliminada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== ENDPOINTS SÍNTOMAS ====================

@app.route('/api/admin/sintoma', methods=['POST'])
def crear_sintoma():
    """Crear nuevo síntoma"""
    try:
        data = request.get_json()
        
        id_sintoma = data.get('id')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        sistema = data.get('sistema')
        
        resultado = prolog_engine.agregar_sintoma(
            id_sintoma, nombre, descripcion, sistema
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Síntoma creado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error al crear síntoma')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/sintoma/<id>', methods=['PUT'])
def editar_sintoma(id):
    """Editar síntoma existente"""
    try:
        data = request.get_json()
        
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')
        sistema = data.get('sistema')
        
        resultado = prolog_engine.editar_sintoma(
            id, nombre, descripcion, sistema
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Síntoma actualizado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/sintoma/<id>', methods=['DELETE'])
def eliminar_sintoma(id):
    """Eliminar síntoma"""
    try:
        resultado = prolog_engine.eliminar_sintoma(id)
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Síntoma eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== ENDPOINTS MEDICAMENTOS ====================

@app.route('/api/admin/medicamento', methods=['POST'])
def crear_medicamento():
    """Crear nuevo medicamento"""
    try:
        data = request.get_json()
        
        id_med = data.get('id')
        nombre = data.get('nombre')
        principio = data.get('principio', '')
        tipo = data.get('tipo')
        descripcion = data.get('descripcion', '')
        
        resultado = prolog_engine.agregar_medicamento(
            id_med, nombre, principio, tipo, descripcion
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Medicamento creado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error al crear medicamento')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/medicamento/<id>', methods=['PUT'])
def editar_medicamento(id):
    """Editar medicamento existente"""
    try:
        data = request.get_json()
        
        nombre = data.get('nombre')
        principio = data.get('principio', '')
        tipo = data.get('tipo')
        descripcion = data.get('descripcion', '')
        
        resultado = prolog_engine.editar_medicamento(
            id, nombre, principio, tipo, descripcion
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Medicamento actualizado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/medicamento/<id>', methods=['DELETE'])
def eliminar_medicamento(id):
    """Eliminar medicamento"""
    try:
        resultado = prolog_engine.eliminar_medicamento(id)
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': 'Medicamento eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Error desconocido')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/prolog', methods=['GET'])
def obtener_archivo_prolog():
    """Obtener contenido del archivo Prolog"""
    try:
        # Obtener ruta absoluta del archivo Prolog
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo_pl = os.path.join(ruta_base, 'base_conocimiento', 'medilogic.pl')
        
        if not os.path.exists(archivo_pl):
            return jsonify({
                'success': False,
                'error': f'Archivo no encontrado: {archivo_pl}'
            }), 404
        
        with open(archivo_pl, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        return jsonify({
            'success': True,
            'data': {
                'contenido': contenido
            }
        })
        
    except Exception as e:
        print(f"Error en /api/admin/prolog GET: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/prolog', methods=['POST'])
def guardar_archivo_prolog():
    """Guardar cambios en archivo Prolog"""
    try:
        data = request.get_json()
        contenido = data.get('contenido', '')
        
        # Obtener ruta absoluta del archivo Prolog
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo_pl = os.path.join(ruta_base, 'base_conocimiento', 'medilogic.pl')
        
        with open(archivo_pl, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Recargar base de conocimiento
        prolog_engine.recargar_base_conocimiento()
        
        return jsonify({
            'success': True,
            'message': 'Archivo guardado y base de conocimiento recargada'
        })
        
    except Exception as e:
        print(f"Error en /api/admin/prolog POST: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/prolog/upload', methods=['POST'])
def cargar_archivo_prolog():
    """Cargar un archivo .pl y fusionarlo con la base de conocimiento actual"""
    try:
        if 'archivo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se recibió ningún archivo'
            }), 400

        archivo = request.files['archivo']

        if not archivo or not archivo.filename:
            return jsonify({
                'success': False,
                'error': 'Archivo inválido'
            }), 400

        if not archivo.filename.lower().endswith('.pl'):
            return jsonify({
                'success': False,
                'error': 'Solo se permiten archivos .pl'
            }), 400

        # Obtener ruta absoluta del archivo Prolog
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo_pl = os.path.join(ruta_base, 'base_conocimiento', 'medilogic.pl')

        # Crear respaldo antes de sobrescribir
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        respaldo = os.path.join(ruta_base, 'base_conocimiento', f'medilogic_backup_{timestamp}.pl')

        if os.path.exists(archivo_pl):
            with open(archivo_pl, 'r', encoding='utf-8') as f_origen:
                contenido_origen = f_origen.read()
            with open(respaldo, 'w', encoding='utf-8') as f_respaldo:
                f_respaldo.write(contenido_origen)

        # Guardar nuevo archivo
        contenido_bytes = archivo.read()
        try:
            contenido = contenido_bytes.decode('utf-8-sig')
        except UnicodeDecodeError:
            return jsonify({
                'success': False,
                'error': 'El archivo no está en UTF-8 válido'
            }), 400

        if not contenido.strip():
            return jsonify({
                'success': False,
                'error': 'El archivo está vacío'
            }), 400

        # Parsear hechos del archivo cargado
        predicados_soportados = {
            'sintoma',
            'enfermedad',
            'medicamento',
            'presenta_sintoma',
            'trata_enfermedad',
            'contraindicacion'
        }
        predicados_entidad = {'sintoma', 'enfermedad', 'medicamento'}
        orden_predicados = [
            'sintoma',
            'enfermedad',
            'medicamento',
            'presenta_sintoma',
            'trata_enfermedad',
            'contraindicacion'
        ]

        hechos_cargados = {p: [] for p in orden_predicados}
        vistos = {p: set() for p in orden_predicados}

        for linea in contenido.splitlines():
            linea_limpia = linea.strip()
            if not linea_limpia or linea_limpia.startswith('%') or linea_limpia.startswith(':-'):
                continue

            match = re.match(r'^([a-z_][a-zA-Z0-9_]*)\((.*)\)\.$', linea_limpia)
            if not match:
                continue

            predicado = match.group(1)
            if predicado not in predicados_soportados:
                continue

            # Evitar duplicados exactos dentro del archivo cargado
            if linea_limpia in vistos[predicado]:
                continue

            vistos[predicado].add(linea_limpia)
            argumentos = match.group(2)
            id_primario = argumentos.split(',', 1)[0].strip() if ',' in argumentos else argumentos.strip()

            hechos_cargados[predicado].append({
                'linea': linea_limpia,
                'id': id_primario
            })

        if all(len(hechos_cargados[p]) == 0 for p in hechos_cargados):
            return jsonify({
                'success': False,
                'error': 'El archivo no contiene hechos Prolog soportados para fusionar'
            }), 400

        # Leer base actual y fusionar
        with open(archivo_pl, 'r', encoding='utf-8') as f_actual:
            lineas_actuales = f_actual.readlines()

        def _buscar_ultima_linea_predicado(predicado):
            idx = None
            patron = re.compile(rf'^\s*{predicado}\(.*\)\.$')
            for i, ln in enumerate(lineas_actuales):
                if patron.match(ln.strip()):
                    idx = i
            return idx

        def _existe_linea_exacta(linea_facto):
            objetivo = linea_facto.strip()
            for ln in lineas_actuales:
                if ln.strip() == objetivo:
                    return True
            return False

        insertados = 0
        actualizados = 0

        for predicado in orden_predicados:
            for hecho in hechos_cargados[predicado]:
                linea_nueva = hecho['linea'] + '\n'

                if predicado in predicados_entidad:
                    # Para entidades: actualizar por ID si existe, insertar si no existe
                    patron_id = re.compile(rf'^\s*{predicado}\(\s*{re.escape(hecho["id"])}\s*,.*\)\.$')
                    indice_existente = None
                    for i, ln in enumerate(lineas_actuales):
                        if patron_id.match(ln.strip()):
                            indice_existente = i
                            break

                    if indice_existente is not None:
                        lineas_actuales[indice_existente] = linea_nueva
                        actualizados += 1
                    else:
                        idx_ultimo = _buscar_ultima_linea_predicado(predicado)
                        if idx_ultimo is not None:
                            lineas_actuales.insert(idx_ultimo + 1, linea_nueva)
                        else:
                            lineas_actuales.append(linea_nueva)
                        insertados += 1
                else:
                    # Para relaciones: agregar solo si no existe exactamente
                    if not _existe_linea_exacta(hecho['linea']):
                        idx_ultimo = _buscar_ultima_linea_predicado(predicado)
                        if idx_ultimo is not None:
                            lineas_actuales.insert(idx_ultimo + 1, linea_nueva)
                        else:
                            lineas_actuales.append(linea_nueva)
                        insertados += 1

        # Persistir archivo fusionado
        with open(archivo_pl, 'w', encoding='utf-8') as f_final:
            f_final.writelines(lineas_actuales)

        # Recargar base de conocimiento
        prolog_engine.recargar_base_conocimiento()

        with open(archivo_pl, 'r', encoding='utf-8') as f_final:
            contenido_fusionado = f_final.read()

        return jsonify({
            'success': True,
            'message': 'Archivo .pl fusionado con la base actual y recargado correctamente',
            'data': {
                'contenido': contenido_fusionado,
                'archivo_original': archivo.filename,
                'respaldo': os.path.basename(respaldo),
                'insertados': insertados,
                'actualizados': actualizados
            }
        })

    except Exception as e:
        print(f"Error en /api/admin/prolog/upload: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== MÓDULO RPA ====================

@app.route('/api/rpa/procesar', methods=['POST'])
def procesar_rpa():
    """
    Procesar archivo de enfermedades con RPA
    
    Body:
    {
        "archivo_contenido": "ENFERMEDAD\nID: e9\n...",
        "guardar_en_prolog": true (opcional, default: true)
    }
    """
    try:
        data = request.get_json()
        contenido = data.get('archivo_contenido', '')
        guardar_en_prolog = data.get('guardar_en_prolog', True)
        
        # Guardar temporalmente
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(contenido)
            temp_file = f.name
        
        # Procesar con RPA
        enfermedades = rpa.cargar_enfermedades_desde_archivo(temp_file)
        
        # Clasificar
        for enf in enfermedades:
            rpa.clasificar_enfermedad(enf)
        
        # Guardar en base de conocimiento Prolog si se solicita
        prolog_actualizado = False
        error_prolog = None
        
        if guardar_en_prolog and enfermedades:
            try:
                print(f"[RPA] Iniciando guardado en Prolog de {len(enfermedades)} enfermedades...")
                
                # Obtener ruta del archivo Prolog
                ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                archivo_prolog = os.path.join(ruta_base, 'base_conocimiento', 'medilogic.pl')
                
                print(f"[RPA] Ruta archivo Prolog: {archivo_prolog}")
                
                # Agregar a Prolog
                rpa.agregar_enfermedades_a_prolog(enfermedades, archivo_prolog)
                print(f"[RPA] Enfermedades agregadas al archivo")
                
                # Recargar motor Prolog para reflejar cambios
                print("[RPA] Recargando motor Prolog...")
                resultado_recarga = prolog_engine.recargar_base_conocimiento()
                
                if resultado_recarga:
                    prolog_actualizado = True
                    print("[RPA] ✓ Motor Prolog recargado exitosamente")
                else:
                    error_prolog = "No se pudo recargar el motor Prolog"
                    print(f"[RPA] ✗ {error_prolog}")
                
            except Exception as e:
                error_prolog = str(e)
                print(f"[RPA] ✗ Error al guardar en Prolog: {error_prolog}")
                rpa._registrar_log(f"Error al guardar en Prolog: {error_prolog}", tipo='ERROR')
        
        # Generar informe
        archivo_informe = rpa.generar_informe_txt(enfermedades)
        
        # Leer informe
        with open(archivo_informe, 'r', encoding='utf-8') as f:
            informe_contenido = f.read()
        
        # Limpiar archivo temporal
        os.unlink(temp_file)
        
        respuesta = {
            'success': True,
            'data': {
                'enfermedades_procesadas': len(enfermedades),
                'informe': informe_contenido,
                'prolog_actualizado': prolog_actualizado,
                'log': rpa.obtener_log()
            }
        }
        
        if error_prolog:
            respuesta['data']['error_prolog'] = error_prolog
        
        return jsonify(respuesta)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rpa/enviar-correo', methods=['POST'])
def enviar_correo_rpa():
    """
    Enviar informe por correo
    
    Body:
    {
        "informe": "contenido...",
        "destinatarios": ["admin@correo.com"],
        "remitente": "medilogic@correo.com" (opcional - usa .env),
        "password": "password" (opcional - usa .env)
    }
    """
    try:
        data = request.get_json()
        
        informe = data.get('informe', '')
        destinatarios = data.get('destinatarios', [])
        
        # Usar valores de .env como predeterminados si no se envían
        remitente = data.get('remitente') or os.getenv('EMAIL_REMITENTE', '')
        password = data.get('password') or os.getenv('EMAIL_PASSWORD', '')
        
        # Validar que tengamos las credenciales (de frontend o .env)
        if not remitente or not password:
            return jsonify({
                'success': False,
                'error': 'Credenciales de correo no configuradas.'
            }), 400
        
        # Guardar informe temporalmente
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(informe)
            temp_file = f.name
        
        # Enviar correo
        exito = rpa.enviar_informe_por_correo(
            temp_file,
            destinatarios,
            remitente=remitente,
            password=password
        )
        
        # Limpiar
        os.unlink(temp_file)
        
        if exito:
            return jsonify({
                'success': True,
                'message': 'Correo enviado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al enviar correo'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/rpa/verificar-credenciales', methods=['GET'])
def verificar_credenciales():
    """
    Verificar si las credenciales de correo están configuradas en .env
    
    Retorna:
    {
        "remitente_configurado": true/false,
        "password_configurado": true/false
    }
    """
    remitente = os.getenv('EMAIL_REMITENTE', '')
    password = os.getenv('EMAIL_PASSWORD', '')
    
    return jsonify({
        'remitente_configurado': bool(remitente),
        'password_configurado': bool(password),
        'remitente': remitente if remitente else None  # Para pre-llenar el formulario
    })


# ==================== INICIAR SERVIDOR ====================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
