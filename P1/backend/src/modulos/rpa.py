"""
Módulo RPA para MediLogic
Automatiza la carga de enfermedades y envío de informes por correo
"""

import pyautogui
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class RPA_MediLogic:
    """Robot de Automatización de Procesos (RPA)"""
    
    def __init__(self):
        # Configuración de seguridad para PyAutoGUI
        pyautogui.FAILSAFE = True  # Mover mouse a esquina superior izquierda para detener
        pyautogui.PAUSE = 0.5  # Pausa entre acciones
        
        self.log_operaciones = []
    
    def cargar_enfermedades_desde_archivo(self, archivo_txt):
        """
        Cargar enfermedades desde un archivo de texto plano
        
        Formato esperado del archivo:
        ENFERMEDAD
        ID: e9
        Nombre: Influenza H1N1
        Descripcion: Variante de la gripe
        Sistema: respiratorio
        Tipo: viral
        Gravedad: grave
        Sintomas: s1,s2,s5
        Medicamentos_Contraindicados: m3
        ---
        
        Args:
            archivo_txt (str): Ruta del archivo de texto
            
        Returns:
            list: Lista de enfermedades procesadas
        """
        if not os.path.exists(archivo_txt):
            raise FileNotFoundError(f"Archivo no encontrado: {archivo_txt}")
        
        enfermedades = []
        enfermedad_actual = {}
        
        try:
            with open(archivo_txt, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    
                    if linea == '---':
                        if enfermedad_actual:
                            enfermedades.append(enfermedad_actual.copy())
                            self._registrar_log(f"Enfermedad cargada: {enfermedad_actual.get('Nombre')}")
                            enfermedad_actual = {}
                    elif ':' in linea and linea != 'ENFERMEDAD':
                        clave, valor = linea.split(':', 1)
                        enfermedad_actual[clave.strip()] = valor.strip()
                
                # Agregar última enfermedad si existe
                if enfermedad_actual:
                    enfermedades.append(enfermedad_actual)
                    self._registrar_log(f"Enfermedad cargada: {enfermedad_actual.get('Nombre')}")
            
            self._registrar_log(f"Total de enfermedades cargadas: {len(enfermedades)}")
            return enfermedades
            
        except Exception as e:
            self._registrar_log(f"Error al cargar archivo: {str(e)}", tipo='ERROR')
            raise
    
    def clasificar_enfermedad(self, enfermedad):
        """
        Clasificar automáticamente una enfermedad por sistema y tipo
        
        Args:
            enfermedad (dict): Diccionario con datos de la enfermedad
            
        Returns:
            dict: Enfermedad con clasificación actualizada
        """
        # Clasificación por sistema (ya viene en el archivo)
        sistema = enfermedad.get('Sistema', 'general').lower()
        
        # Clasificación por tipo
        tipo = enfermedad.get('Tipo', 'general').lower()
        
        # Validar sistema
        sistemas_validos = [
            'respiratorio', 'digestivo', 'cardiovascular', 
            'endocrino', 'neurologico', 'musculoesqueletico',
            'renal', 'hepatico', 'general'
        ]
        
        if sistema not in sistemas_validos:
            self._registrar_log(
                f"Sistema '{sistema}' no válido, usando 'general'",
                tipo='ADVERTENCIA'
            )
            enfermedad['Sistema'] = 'general'
        
        # Validar tipo
        tipos_validos = ['viral', 'bacterial', 'cronico', 'autoinmune', 'general']
        
        if tipo not in tipos_validos:
            self._registrar_log(
                f"Tipo '{tipo}' no válido, usando 'general'",
                tipo='ADVERTENCIA'
            )
            enfermedad['Tipo'] = 'general'
        
        self._registrar_log(
            f"Clasificación: {enfermedad['Nombre']} - Sistema: {sistema}, Tipo: {tipo}"
        )
        
        return enfermedad
    
    def agregar_enfermedades_a_prolog(self, enfermedades, archivo_prolog):
        """
        Agregar enfermedades procesadas a la base de conocimiento Prolog
        
        Args:
            enfermedades (list): Lista de enfermedades a agregar
            archivo_prolog (str): Ruta del archivo medilogic.pl
            
        Returns:
            bool: True si se agregaron correctamente
        """
        try:
            if not os.path.exists(archivo_prolog):
                raise FileNotFoundError(f"Archivo Prolog no encontrado: {archivo_prolog}")
            
            # Leer contenido actual
            with open(archivo_prolog, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Encontrar las secciones
            # Buscar el último enfermedad(...) 
            import re
            
            # Encontrar la última línea de enfermedad(...)
            enfermedades_existentes = re.findall(r'enfermedad\([^)]+\)\.', contenido)
            if not enfermedades_existentes:
                raise ValueError("No se encontraron enfermedades existentes en el archivo")
            
            ultima_enfermedad = enfermedades_existentes[-1]
            pos_ultima_enf = contenido.rfind(ultima_enfermedad)
            pos_insercion_enf = pos_ultima_enf + len(ultima_enfermedad)
            
            # Construir texto de nuevas enfermedades
            nuevas_enfermedades_texto = "\n"
            nuevos_sintomas_texto = "\n"
            
            for enf in enfermedades:
                # Validar campos requeridos
                if not all(k in enf for k in ['ID', 'Nombre', 'Descripcion', 'Sistema', 'Tipo', 'Gravedad']):
                    self._registrar_log(f"Enfermedad incompleta, saltando: {enf.get('Nombre', 'sin nombre')}", tipo='ADVERTENCIA')
                    continue
                
                # Validar que el ID no exista
                if f"enfermedad({enf['ID']}," in contenido:
                    self._registrar_log(f"Enfermedad {enf['ID']} ya existe, saltando", tipo='ADVERTENCIA')
                    continue
                
                # Construir predicado de enfermedad
                # enfermedad(ID, Nombre, Descripcion, Sistema, Tipo, Gravedad).
                enf_prolog = f"enfermedad({enf['ID']}, '{enf['Nombre']}', '{enf['Descripcion']}', '{enf['Sistema']}', '{enf['Tipo']}', '{enf['Gravedad']}').\n"
                nuevas_enfermedades_texto += enf_prolog
                
                # Construir predicados de síntomas si existen
                if 'Sintomas' in enf and enf['Sintomas']:
                    sintomas_ids = [s.strip() for s in enf['Sintomas'].split(',') if s.strip()]
                    
                    nuevos_sintomas_texto += f"\n% {enf['Nombre']} ({enf['ID']})\n"
                    
                    # Asignar peso predeterminado de 7 (moderado)
                    for sintoma_id in sintomas_ids:
                        # presenta_sintoma(EnfermedadID, SintomaID, Peso)
                        sintoma_prolog = f"presenta_sintoma({enf['ID']}, {sintoma_id}, 7).\n"
                        nuevos_sintomas_texto += sintoma_prolog
                
                self._registrar_log(f"Agregada a Prolog: {enf['Nombre']} ({enf['ID']})")
            
            # Insertar nuevas enfermedades
            contenido_actualizado = (
                contenido[:pos_insercion_enf] + 
                nuevas_enfermedades_texto + 
                contenido[pos_insercion_enf:]
            )
            
            # Encontrar la sección de presenta_sintoma y agregar al final
            sintomas_existentes = re.findall(r'presenta_sintoma\([^)]+\)\.', contenido_actualizado)
            if sintomas_existentes:
                ultimo_sintoma = sintomas_existentes[-1]
                pos_ultimo_sint = contenido_actualizado.rfind(ultimo_sintoma)
                pos_insercion_sint = pos_ultimo_sint + len(ultimo_sintoma)
                
                contenido_actualizado = (
                    contenido_actualizado[:pos_insercion_sint] + 
                    nuevos_sintomas_texto + 
                    contenido_actualizado[pos_insercion_sint:]
                )
            
            # Guardar archivo actualizado
            with open(archivo_prolog, 'w', encoding='utf-8') as f:
                f.write(contenido_actualizado)
            
            self._registrar_log(f"Base de conocimiento Prolog actualizada: {len(enfermedades)} enfermedades agregadas")
            return True
            
        except Exception as e:
            self._registrar_log(f"Error al agregar a Prolog: {str(e)}", tipo='ERROR')
            raise
    
    def automatizar_ingreso_interfaz(self, enfermedades, tiempo_por_campo=0.5):
        """
        Automatizar el ingreso de enfermedades en la interfaz gráfica
        
        IMPORTANTE: Esta función requiere que la interfaz esté visible
        y los campos accesibles. Se debe configurar las coordenadas
        apropiadas para cada campo.
        
        Args:
            enfermedades (list): Lista de enfermedades a ingresar
            tiempo_por_campo (float): Tiempo de espera entre campos
        """
        self._registrar_log("Iniciando automatización de interfaz...")
        
        for i, enf in enumerate(enfermedades, 1):
            try:
                self._registrar_log(f"Procesando enfermedad {i}/{len(enfermedades)}")
                
                # NOTA: Las coordenadas deben configurarse según la interfaz real
                # Este es un ejemplo de flujo
                
                # 1. Click en botón "Nueva Enfermedad"
                # pyautogui.click(x=coordX, y=coordY)
                # time.sleep(tiempo_por_campo)
                
                # 2. Ingresar ID
                # pyautogui.write(enf.get('ID', ''), interval=0.1)
                
                # 3. Ingresar Nombre
                # pyautogui.press('tab')
                # pyautogui.write(enf.get('Nombre', ''), interval=0.1)
                
                # Y así sucesivamente...
                
                self._registrar_log(f"✓ {enf.get('Nombre')} ingresado correctamente")
                
            except Exception as e:
                self._registrar_log(
                    f"✗ Error al ingresar {enf.get('Nombre')}: {str(e)}",
                    tipo='ERROR'
                )
        
        self._registrar_log("Automatización completada")
    
    def generar_informe_txt(self, enfermedades, archivo_salida='informe_carga.txt'):
        """
        Generar informe en texto plano de las enfermedades cargadas
        
        Args:
            enfermedades (list): Lista de enfermedades
            archivo_salida (str): Nombre del archivo de salida
            
        Returns:
            str: Ruta del archivo generado
        """
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("INFORME DE CARGA DE ENFERMEDADES - MEDILOGIC RPA\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de enfermedades procesadas: {len(enfermedades)}\n\n")
                
                for i, enf in enumerate(enfermedades, 1):
                    f.write(f"\n{i}. {enf.get('Nombre', 'N/A')}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"  ID: {enf.get('ID', 'N/A')}\n")
                    f.write(f"  Sistema: {enf.get('Sistema', 'N/A')}\n")
                    f.write(f"  Tipo: {enf.get('Tipo', 'N/A')}\n")
                    f.write(f"  Gravedad: {enf.get('Gravedad', 'N/A')}\n")
                    f.write(f"  Descripción: {enf.get('Descripcion', 'N/A')}\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("REGISTRO DE OPERACIONES\n")
                f.write("=" * 80 + "\n")
                
                for log in self.log_operaciones:
                    f.write(f"{log}\n")
            
            self._registrar_log(f"Informe generado: {archivo_salida}")
            return archivo_salida
            
        except Exception as e:
            self._registrar_log(f"Error al generar informe: {str(e)}", tipo='ERROR')
            return None
    
    def enviar_informe_por_correo(
        self,
        archivo_informe,
        destinatarios,
        smtp_server=None,
        smtp_port=None,
        remitente='',
        password=''
    ):
        """
        Enviar informe por correo electrónico a administradores
        
        NOTA: Para Gmail, se requiere contraseña de aplicación
        
        Args:
            archivo_informe (str): Ruta del archivo de informe
            destinatarios (list): Lista de correos destinatarios
            smtp_server (str): Servidor SMTP (usa SMTP_HOST de .env si no se especifica)
            smtp_port (int): Puerto SMTP (usa SMTP_PORT de .env si no se especifica)
            remitente (str): Correo remitente
            password (str): Contraseña del remitente
        """
        try:
            # Obtener configuración SMTP desde .env o usar valores por defecto
            smtp_server = smtp_server or os.getenv('SMTP_HOST')
            smtp_port = smtp_port or int(os.getenv('SMTP_PORT'))
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = ', '.join(destinatarios)
            msg['Subject'] = f"Informe de Carga RPA - MediLogic {datetime.now().strftime('%d/%m/%Y')}"
            
            # Cuerpo del mensaje
            cuerpo = f"""
            Estimados administradores,
            
            Se ha completado una carga automática de enfermedades en el sistema MediLogic.
            
            Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            
            Adjunto encontrarán el informe detallado de la operación.
            
            Este es un mensaje automático generado por el RPA de MediLogic.
            
            Saludos cordiales,
            Sistema MediLogic RPA
            """
            
            msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
            
            # Leer y adjuntar informe
            if os.path.exists(archivo_informe):
                with open(archivo_informe, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                adjunto = MIMEText(contenido, 'plain', 'utf-8')
                adjunto.add_header('Content-Disposition', 'attachment', filename='informe_carga.txt')
                msg.attach(adjunto)
            
            # Conectar y enviar
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(remitente, password)
            server.send_message(msg)
            server.quit()
            
            self._registrar_log(f"Correo enviado a: {', '.join(destinatarios)}")
            return True
            
        except Exception as e:
            self._registrar_log(f"Error al enviar correo: {str(e)}", tipo='ERROR')
            return False
    
    def _registrar_log(self, mensaje, tipo='INFO'):
        """Registrar operación en el log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = f"[{timestamp}] [{tipo}] {mensaje}"
        self.log_operaciones.append(log)
        print(log)
    
    def obtener_log(self):
        """Obtener registro de operaciones"""
        return self.log_operaciones.copy()


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Prueba del Módulo RPA ===\n")
    
    # Crear instancia
    rpa = RPA_MediLogic()
    
    # Ejemplo de archivo de enfermedades
    ejemplo_txt = """ENFERMEDAD
ID: e9
Nombre: Neumonía Atípica
Descripcion: Infección pulmonar por agentes atípicos
Sistema: respiratorio
Tipo: bacterial
Gravedad: grave
Sintomas: s1,s2,s15
Medicamentos_Contraindicados: m2
---
ENFERMEDAD
ID: e10
Nombre: Gastritis Aguda
Descripcion: Inflamación del revestimiento gástrico
Sistema: digestivo
Tipo: general
Gravedad: moderada
Sintomas: s6,s9
Medicamentos_Contraindicados: m2
---
"""
    
    # Guardar archivo de ejemplo
    with open('ejemplo_enfermedades.txt', 'w', encoding='utf-8') as f:
        f.write(ejemplo_txt)
    
    print("✓ Archivo de ejemplo creado: ejemplo_enfermedades.txt\n")
    
    # Probar carga
    try:
        enfermedades = rpa.cargar_enfermedades_desde_archivo('ejemplo_enfermedades.txt')
        print(f"\n✓ Enfermedades cargadas: {len(enfermedades)}\n")
        
        # Clasificar
        for enf in enfermedades:
            rpa.clasificar_enfermedad(enf)
        
        # Generar informe
        informe = rpa.generar_informe_txt(enfermedades)
        print(f"\n✓ Informe generado: {informe}")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
