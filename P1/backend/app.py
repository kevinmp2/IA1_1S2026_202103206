"""
Backend Flask para MediLogic
API REST para el sistema 
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.prolog_engine import PrologEngine
from utils.pdf_generator import PDFGenerator
from modulos.rpa import RPA_MediLogic

app = Flask(__name__)
CORS(app)  

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


# ==================== DESCARGA PDF (LEGACY - YA NO SE USA) ====================
# Los PDFs ahora se generan y descargan directamente en memoria sin guardarse en el servidor
# Este endpoint se mantiene comentado por referencia

# @app.route('/api/descargar-pdf/<nombre_archivo>', methods=['GET'])
# def descargar_pdf(nombre_archivo):
#     """Descargar archivo PDF generado (YA NO SE USA - PDFs se generan en memoria)"""
#     try:
#         # Ruta al directorio de informes
#         directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         directorio_informes = os.path.join(directorio_base, 'informes')
#         ruta_archivo = os.path.join(directorio_informes, nombre_archivo)
#         
#         if os.path.exists(ruta_archivo):
#             return send_file(
#                 ruta_archivo,
#                 mimetype='application/pdf',
#                 as_attachment=True,
#                 download_name=nombre_archivo
#             )
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': 'Archivo no encontrado'
#             }), 404
#             
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500


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
        # TODO: Implementar lógica de edición
        return jsonify({
            'success': True,
            'message': 'Funcionalidad en desarrollo'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/admin/enfermedad/<id>', methods=['DELETE'])
def eliminar_enfermedad(id):
    """Eliminar enfermedad"""
    try:
        # TODO: Implementar lógica de eliminación
        return jsonify({
            'success': True,
            'message': 'Funcionalidad en desarrollo'
        })
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
                'error': 'Credenciales de correo no configuradas. Configure EMAIL_REMITENTE y EMAIL_PASSWORD en el archivo .env'
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
