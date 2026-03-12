"""
Motor de Prolog para MediLogic
Maneja la conexión con SWI-Prolog usando pyswip
"""

from pyswip import Prolog
import os


class PrologEngine:
    """Motor de inferencia Prolog"""
    
    def __init__(self):
        """Inicializar el motor Prolog"""
        self.prolog = Prolog()
        self.archivo_pl = self._obtener_ruta_pl()
        self.cargar_base_conocimiento()
    
    def _obtener_ruta_pl(self):
        """Obtener ruta absoluta del archivo .pl"""
        ruta_actual = os.path.dirname(os.path.abspath(__file__))  # P1/backend/src/utils
        ruta_src = os.path.dirname(ruta_actual)                    # P1/backend/src
        ruta_backend = os.path.dirname(ruta_src)                   # P1/backend
        ruta_proyecto = os.path.dirname(ruta_backend)              # P1
        ruta_pl = os.path.join(ruta_proyecto, 'base_conocimiento', 'medilogic.pl')
        return ruta_pl
    
    def cargar_base_conocimiento(self):
        """Cargar el archivo Prolog con la base de conocimiento"""
        try:
            ruta_unix = self.archivo_pl.replace('\\', '/')
            self.prolog.consult(ruta_unix)
            print(f"Base de conocimiento cargada desde: {self.archivo_pl}")
        except Exception as e:
            raise Exception(f"Error al cargar base de conocimiento: {str(e)}")
    
    def recargar_base_conocimiento(self):
        """Recargar el archivo Prolog"""
        try:
            ruta_unix = self.archivo_pl.replace('\\', '/')
            self.prolog.consult(ruta_unix)
            print(f"Base de conocimiento recargada desde: {self.archivo_pl}")
            return True
        except Exception as e:
            print(f"Error al recargar: {str(e)}")
            return False
    
    def _corregir_codificacion(self, texto):
        """
        Corregir problemas de codificación UTF-8
        
        PySwip a veces devuelve cadenas con codificación incorrecta.
        Esta función intenta corregirlas.
        """
        if not isinstance(texto, str):
            return texto
        
        try:
            # Intentar decodificar como latin-1 y recodificar como UTF-8
            return texto.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Si falla, devolver el texto original
            return texto
    
    def _procesar_resultado(self, resultado):
        """
        Procesar un resultado de Prolog corrigiendo la codificación
        """
        if isinstance(resultado, dict):
            return {k: self._corregir_codificacion(v) if isinstance(v, str) else v 
                    for k, v in resultado.items()}
        return resultado
    
    def consultar(self, query):
        """
        Realizar una consulta a Prolog
        
        Args:
            query (str): Consulta en sintaxis Prolog
            
        Returns:
            list: Lista de resultados con codificación corregida
        """
        try:
            resultados = list(self.prolog.query(query))
            # Corregir la codificación de cada resultado
            return [self._procesar_resultado(r) for r in resultados]
        except Exception as e:
            print(f"Error en consulta: {str(e)}")
            return []
    
    def obtener_sintomas(self):
        """Obtener todos los síntomas disponibles"""
        query = "sintoma(ID, Nombre, Descripcion, Sistema)"
        resultados = self.consultar(query)
        return [
            {
                'id': r['ID'],
                'nombre': r['Nombre'],
                'descripcion': r['Descripcion'],
                'sistema': r['Sistema']
            }
            for r in resultados
        ]
    
    def obtener_enfermedades(self):
        """Obtener todas las enfermedades disponibles"""
        query = "enfermedad(ID, Nombre, Descripcion, Sistema, Tipo, Gravedad)"
        resultados = self.consultar(query)
        return [
            {
                'id': r['ID'],
                'nombre': r['Nombre'],
                'descripcion': r['Descripcion'],
                'sistema': r['Sistema'],
                'tipo': r['Tipo'],
                'gravedad': r['Gravedad']
            }
            for r in resultados
        ]
    
    def obtener_medicamentos(self):
        """Obtener todos los medicamentos disponibles"""
        query = "medicamento(ID, Nombre, Principio, Tipo, Descripcion)"
        resultados = self.consultar(query)
        return [
            {
                'id': r['ID'],
                'nombre': r['Nombre'],
                'principio': r['Principio'],
                'tipo': r['Tipo'],
                'descripcion': r['Descripcion']
            }
            for r in resultados
        ]
    
    def obtener_enfermedades_cronicas(self):
        """Obtener enfermedades crónicas definidas"""
        query = "enfermedad_cronica(ID, Nombre, Sistema)"
        resultados = self.consultar(query)
        return [
            {
                'id': r['ID'],
                'nombre': r['Nombre'],
                'sistema': r['Sistema']
            }
            for r in resultados
        ]
    
    def diagnosticar(self, sintomas_paciente, alergias, enfermedades_cronicas):
        """
        Realizar diagnóstico basado en síntomas del paciente
        
        Args:
            sintomas_paciente (list): Lista de tuplas (id_sintoma, nombre, severidad)
            alergias (list): Lista de nombres de medicamentos
            enfermedades_cronicas (list): Lista de IDs de enfermedades crónicas
            
        Returns:
            list: Lista de diagnósticos con afinidad y tratamiento
        """
        # Construir lista de síntomas para Prolog
        sintomas_str = self._construir_lista_sintomas(sintomas_paciente)
        alergias_str = self._construir_lista_strings(alergias)
        cronicas_str = self._construir_lista_ids(enfermedades_cronicas)
        
        # Consulta Prolog
        query = f"diagnosticar({sintomas_str}, {alergias_str}, {cronicas_str}, Diagnosticos)"
        
        print(f"Query Prolog: {query}")
        
        try:
            resultados = self.consultar(query)
            print(f"Resultados crudos: {resultados}")
            
            if resultados and 'Diagnosticos' in resultados[0]:
                diagnosticos_raw = resultados[0]['Diagnosticos']
                print(f"Diagnósticos raw: {diagnosticos_raw}")
                return self._procesar_diagnosticos_mejorado(diagnosticos_raw)
            return []
        except Exception as e:
            print(f"Error en diagnóstico: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def _construir_lista_sintomas(self, sintomas):
        """Construir lista Prolog de síntomas"""
        if not sintomas:
            return "[]"
        items = [f"sintoma({sid}, {sev})" for sid, nombre, sev in sintomas]
        return f"[{', '.join(items)}]"
    
    def _construir_lista_strings(self, items):
        """Construir lista Prolog de strings"""
        if not items:
            return "[]"
        items_quoted = [f"'{item}'" for item in items]
        return f"[{', '.join(items_quoted)}]"
    
    def _construir_lista_ids(self, items):
        """Construir lista Prolog de IDs"""
        if not items:
            return "[]"
        return f"[{', '.join(items)}]"
    
    def _procesar_diagnosticos(self, diagnosticos):
        """Procesar resultados del diagnóstico"""
        if not diagnosticos:
            return []
        
        resultados = []
        for diag in diagnosticos:
            # Los diagnósticos vienen como strings o estructuras de Prolog
            # Intentar extraer información si es un dict
            if isinstance(diag, dict):
                resultados.append(diag)
            else:
                # Si es una estructura de Prolog, intentar parsearlo
                diag_str = str(diag)
                resultados.append({
                    'raw': diag_str,
                    'tipo': 'diagnostico'
                })
        
        return resultados
    
    def _procesar_diagnosticos_mejorado(self, diagnosticos):
        """Procesar y estructurar los diagnósticos de Prolog"""
        if not diagnosticos:
            return []
        
        resultados = []
        
        for diag in diagnosticos:
            try:
                # Convertir a string si no lo es
                diag_str = str(diag)
                
                # Intentar parsear el diagnóstico
                # Formato: diagnostico(ID, Nombre, Afinidad, Gravedad, Urgencia, [medicamentos])
                import re
                
                # Buscar patrón: diagnostico(id, nombre, afinidad, gravedad, urgencia, medicamentos)
                pattern = r"diagnostico\((\w+),\s*([^,]+),\s*([\d.]+),\s*(\w+),\s*([^,\[]+),\s*(\[.*\])\)"
                match = re.search(pattern, diag_str)
                
                if match:
                    enfermedad_id = match.group(1)
                    nombre = match.group(2).strip()
                    afinidad = float(match.group(3))
                    gravedad = match.group(4)
                    urgencia = match.group(5).strip()
                    medicamentos_str = match.group(6)
                    
                    # Parsear medicamentos
                    medicamentos = []
                    med_pattern = r"medicamento\((\w+),\s*([^,]+),\s*(\w+),\s*(\d+)\)"
                    for med_match in re.finditer(med_pattern, medicamentos_str):
                        medicamentos.append({
                            'id': med_match.group(1),
                            'nombre': med_match.group(2).strip(),
                            'tipo': med_match.group(3),
                            'efectividad': int(med_match.group(4))
                        })
                    
                    resultados.append({
                        'enfermedad_id': enfermedad_id,
                        'nombre': nombre,
                        'afinidad': round(afinidad, 2),
                        'gravedad': gravedad,
                        'urgencia': urgencia,
                        'medicamentos': medicamentos
                    })
                else:
                    # Si no puede parsear, devolver raw
                    resultados.append({
                        'raw': diag_str,
                        'error': 'No se pudo parsear el diagnóstico'
                    })
            except Exception as e:
                print(f"Error al procesar diagnóstico {diag}: {str(e)}")
                resultados.append({
                    'raw': str(diag),
                    'error': str(e)
                })
        
        return resultados
    
    def agregar_sintoma(self, id_sintoma, nombre, descripcion, sistema):
        """Agregar un nuevo síntoma a la base de conocimiento"""
        try:
            query = f"assertz(sintoma('{id_sintoma}', '{nombre}', '{descripcion}', '{sistema}'))"
            self.consultar(query)
            self._guardar_en_archivo()
            return True
        except Exception as e:
            print(f"Error al agregar síntoma: {str(e)}")
            return False
    
    def agregar_enfermedad(self, id_enf, nombre, descripcion, sistema, tipo, gravedad):
        """Agregar una nueva enfermedad a la base de conocimiento"""
        try:
            query = f"assertz(enfermedad('{id_enf}', '{nombre}', '{descripcion}', '{sistema}', '{tipo}', '{gravedad}'))"
            self.consultar(query)
            self._guardar_en_archivo()
            return True
        except Exception as e:
            print(f"Error al agregar enfermedad: {str(e)}")
            return False
    
    def _guardar_en_archivo(self):
        """Guardar cambios en el archivo .pl"""
        try:
            # Obtener todos los datos actuales de Prolog
            sintomas = self.obtener_sintomas()
            enfermedades = self.obtener_enfermedades()
            medicamentos = self.obtener_medicamentos()
            
            # Leer el archivo actual para preservar otras secciones
            with open(self.archivo_pl, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Encontrar las secciones y reemplazarlas
            import re
            
            # Construir nuevas secciones
            nueva_seccion_sintomas = self._construir_seccion_sintomas(sintomas)
            nueva_seccion_enfermedades = self._construir_seccion_enfermedades(enfermedades)
            nueva_seccion_medicamentos = self._construir_seccion_medicamentos(medicamentos)
            
            # Reemplazar secciones (mantener el resto del archivo intacto)
            # Esto es complejo, por ahora recargaremos el archivo
            self.recargar_base_conocimiento()
            return True
        except Exception as e:
            print(f"Error al guardar en archivo: {str(e)}")
            return False
    
    def _construir_seccion_sintomas(self, sintomas):
        """Construir texto de la sección de síntomas"""
        lineas = ["% ==============================================================================\n"]
        lineas.append("% HECHOS: SÍNTOMAS\n")
        lineas.append("% ==============================================================================\n")
        lineas.append("% sintoma(ID, Nombre, Descripcion, Sistema)\n")
        for s in sintomas:
            lineas.append(f"sintoma({s['id']}, '{s['nombre']}', '{s['descripcion']}', '{s['sistema']}').\n")
        return ''.join(lineas)
    
    def _construir_seccion_enfermedades(self, enfermedades):
        """Construir texto de la sección de enfermedades"""
        lineas = ["% ==============================================================================\n"]
        lineas.append("% HECHOS: ENFERMEDADES\n")
        lineas.append("% ==============================================================================\n")
        lineas.append("% enfermedad(ID, Nombre, Descripcion, Sistema, Tipo, Gravedad)\n")
        for e in enfermedades:
            lineas.append(f"enfermedad({e['id']}, '{e['nombre']}', '{e['descripcion']}', '{e['sistema']}', '{e['tipo']}', '{e['gravedad']}').\n")
        return ''.join(lineas)
    
    def _construir_seccion_medicamentos(self, medicamentos):
        """Construir texto de la sección de medicamentos"""
        lineas = ["% ==============================================================================\n"]
        lineas.append("% HECHOS: MEDICAMENTOS\n")
        lineas.append("% ==============================================================================\n")
        lineas.append("% medicamento(ID, Nombre, Principio, Tipo, Descripcion)\n")
        for m in medicamentos:
            lineas.append(f"medicamento({m['id']}, '{m['nombre']}', '{m['principio']}', '{m['tipo']}', '{m['descripcion']}').\n")
        return ''.join(lineas)
    
    # ==================== CRUD ENFERMEDADES ====================
    
    def agregar_enfermedad(self, id_enf, nombre, descripcion, sistema, tipo, gravedad):
        """Agregar una nueva enfermedad"""
        try:
            # Verificar que no exista
            query_check = f"enfermedad('{id_enf}', _, _, _, _, _)"
            existe = self.consultar(query_check)
            if existe:
                return {'success': False, 'error': f'La enfermedad con ID {id_enf} ya existe'}
            
            # Agregar a Prolog en memoria
            query = f"assertz(enfermedad('{id_enf}', '{nombre}', '{descripcion}', '{sistema}', '{tipo}', '{gravedad}'))"
            self.consultar(query)
            
            # Guardar en archivo
            self._agregar_al_archivo_pl('enfermedad', (id_enf, nombre, descripcion, sistema, tipo, gravedad))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def editar_enfermedad(self, id_enf, nombre, descripcion, sistema, tipo, gravedad):
        """Editar una enfermedad existente"""
        try:
            # Eliminar la anterior
            query_retract = f"retract(enfermedad('{id_enf}', _, _, _, _, _))"
            self.consultar(query_retract)
            
            # Agregar la nueva
            query_assert = f"assertz(enfermedad('{id_enf}', '{nombre}', '{descripcion}', '{sistema}', '{tipo}', '{gravedad}'))"
            self.consultar(query_assert)
            
            # Actualizar archivo
            self._actualizar_en_archivo_pl('enfermedad', id_enf, (id_enf, nombre, descripcion, sistema, tipo, gravedad))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def eliminar_enfermedad(self, id_enf):
        """Eliminar una enfermedad"""
        try:
            # Eliminar de Prolog en memoria
            query = f"retract(enfermedad('{id_enf}', _, _, _, _, _))"
            self.consultar(query)
            
            # Eliminar del archivo
            self._eliminar_del_archivo_pl('enfermedad', id_enf)
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== CRUD SÍNTOMAS ====================
    
    def agregar_sintoma(self, id_sintoma, nombre, descripcion, sistema):
        """Agregar un nuevo síntoma"""
        try:
            # Verificar que no exista
            query_check = f"sintoma('{id_sintoma}', _, _, _)"
            existe = self.consultar(query_check)
            if existe:
                return {'success': False, 'error': f'El síntoma con ID {id_sintoma} ya existe'}
            
            # Agregar a Prolog
            query = f"assertz(sintoma('{id_sintoma}', '{nombre}', '{descripcion}', '{sistema}'))"
            self.consultar(query)
            
            # Guardar en archivo
            self._agregar_al_archivo_pl('sintoma', (id_sintoma, nombre, descripcion, sistema))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def editar_sintoma(self, id_sintoma, nombre, descripcion, sistema):
        """Editar un síntoma existente"""
        try:
            query_retract = f"retract(sintoma('{id_sintoma}', _, _, _))"
            self.consultar(query_retract)
            
            query_assert = f"assertz(sintoma('{id_sintoma}', '{nombre}', '{descripcion}', '{sistema}'))"
            self.consultar(query_assert)
            
            self._actualizar_en_archivo_pl('sintoma', id_sintoma, (id_sintoma, nombre, descripcion, sistema))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def eliminar_sintoma(self, id_sintoma):
        """Eliminar un síntoma"""
        try:
            query = f"retract(sintoma('{id_sintoma}', _, _, _))"
            self.consultar(query)
            
            self._eliminar_del_archivo_pl('sintoma', id_sintoma)
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== CRUD MEDICAMENTOS ====================
    
    def agregar_medicamento(self, id_med, nombre, principio, tipo, descripcion):
        """Agregar un nuevo medicamento"""
        try:
            query_check = f"medicamento('{id_med}', _, _, _, _)"
            existe = self.consultar(query_check)
            if existe:
                return {'success': False, 'error': f'El medicamento con ID {id_med} ya existe'}
            
            query = f"assertz(medicamento('{id_med}', '{nombre}', '{principio}', '{tipo}', '{descripcion}'))"
            self.consultar(query)
            
            self._agregar_al_archivo_pl('medicamento', (id_med, nombre, principio, tipo, descripcion))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def editar_medicamento(self, id_med, nombre, principio, tipo, descripcion):
        """Editar un medicamento existente"""
        try:
            query_retract = f"retract(medicamento('{id_med}', _, _, _, _))"
            self.consultar(query_retract)
            
            query_assert = f"assertz(medicamento('{id_med}', '{nombre}', '{principio}', '{tipo}', '{descripcion}'))"
            self.consultar(query_assert)
            
            self._actualizar_en_archivo_pl('medicamento', id_med, (id_med, nombre, principio, tipo, descripcion))
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def eliminar_medicamento(self, id_med):
        """Eliminar un medicamento"""
        try:
            query = f"retract(medicamento('{id_med}', _, _, _, _))"
            self.consultar(query)
            
            self._eliminar_del_archivo_pl('medicamento', id_med)
            
            self.recargar_base_conocimiento()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== MÉTODOS AUXILIARES PARA ARCHIVO ====================
    
    def _agregar_al_archivo_pl(self, tipo, datos):
        """Agregar un predicado al archivo Prolog"""
        try:
            with open(self.archivo_pl, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            # Construir la nueva línea según el tipo
            import re
            if tipo == 'enfermedad':
                nueva_linea = f"enfermedad({datos[0]}, '{datos[1]}', '{datos[2]}', '{datos[3]}', '{datos[4]}', '{datos[5]}').\n"
                # Buscar justo antes del comentario "RELACIONES: ENFERMEDAD - SÍNTOMAS"
                patron_siguiente_seccion = r'% RELACIONES: ENFERMEDAD - S[ÍI]NTOMAS'
            elif tipo == 'sintoma':
                nueva_linea = f"sintoma({datos[0]}, '{datos[1]}', '{datos[2]}', '{datos[3]}').\n"
                # Buscar justo antes del comentario "HECHOS: ENFERMEDADES"
                patron_siguiente_seccion = r'% HECHOS: ENFERMEDADES'
            elif tipo == 'medicamento':
                nueva_linea = f"medicamento({datos[0]}, '{datos[1]}', '{datos[2]}', '{datos[3]}', '{datos[4]}').\n"
                # Buscar específicamente antes del comentario "RELACIONES: ENFERMEDAD - TRATAMIENTO"
                patron_siguiente_seccion = r'% RELACIONES: ENFERMEDAD - TRATAMIENTO'
            else:
                return False
            
            # Encontrar la posición de inserción (antes del siguiente comentario de sección)
            posicion_insercion = None
            for i, linea in enumerate(lineas):
                if re.search(patron_siguiente_seccion, linea):
                    # Retroceder hasta encontrar una línea que no esté vacía o sea comentario
                    for j in range(i-1, -1, -1):
                        if lineas[j].strip() and not lineas[j].strip().startswith('%'):
                            posicion_insercion = j + 1
                            break
                    break
            
            if posicion_insercion is not None:
                # Insertar en la posición encontrada
                lineas.insert(posicion_insercion, nueva_linea)
            else:
                # Si no se encuentra el patrón, buscar la última ocurrencia del tipo
                ultima_linea = None
                patron_tipo = None
                if tipo == 'enfermedad':
                    patron_tipo = r'^enfermedad\('
                elif tipo == 'sintoma':
                    patron_tipo = r'^sintoma\('
                elif tipo == 'medicamento':
                    patron_tipo = r'^medicamento\('
                
                if patron_tipo:
                    for i, linea in enumerate(lineas):
                        if re.match(patron_tipo, linea.strip()):
                            ultima_linea = i
                    if ultima_linea is not None:
                        lineas.insert(ultima_linea + 1, nueva_linea)
                    else:
                        lineas.append(nueva_linea)
                else:
                    lineas.append(nueva_linea)
            
            # Guardar archivo
            with open(self.archivo_pl, 'w', encoding='utf-8') as f:
                f.writelines(lineas)
            
            return True
        except Exception as e:
            print(f"Error al agregar al archivo: {str(e)}")
            return False
    
    def _actualizar_en_archivo_pl(self, tipo, id_entidad, nuevos_datos):
        """Actualizar un predicado en el archivo Prolog"""
        try:
            with open(self.archivo_pl, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            # Buscar y reemplazar la línea
            import re
            if tipo == 'enfermedad':
                patron = re.compile(rf"enfermedad\({id_entidad},.*?\)\.")
                nueva_linea = f"enfermedad({nuevos_datos[0]}, '{nuevos_datos[1]}', '{nuevos_datos[2]}', '{nuevos_datos[3]}', '{nuevos_datos[4]}', '{nuevos_datos[5]}').\n"
            elif tipo == 'sintoma':
                patron = re.compile(rf"sintoma\({id_entidad},.*?\)\.")
                nueva_linea = f"sintoma({nuevos_datos[0]}, '{nuevos_datos[1]}', '{nuevos_datos[2]}', '{nuevos_datos[3]}').\n"
            elif tipo == 'medicamento':
                patron = re.compile(rf"medicamento\({id_entidad},.*?\)\.")
                nueva_linea = f"medicamento({nuevos_datos[0]}, '{nuevos_datos[1]}', '{nuevos_datos[2]}', '{nuevos_datos[3]}', '{nuevos_datos[4]}').\n"
            else:
                return False
            
            # Reemplazar en las líneas
            lineas_nuevas = []
            for linea in lineas:
                if patron.search(linea):
                    lineas_nuevas.append(nueva_linea)
                else:
                    lineas_nuevas.append(linea)
            
            # Guardar archivo
            with open(self.archivo_pl, 'w', encoding='utf-8') as f:
                f.writelines(lineas_nuevas)
            
            return True
        except Exception as e:
            print(f"Error al actualizar archivo: {str(e)}")
            return False
    
    def _eliminar_del_archivo_pl(self, tipo, id_entidad):
        """Eliminar un predicado del archivo Prolog"""
        try:
            with open(self.archivo_pl, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
            
            # Buscar y eliminar la línea
            import re
            if tipo == 'enfermedad':
                patron = re.compile(rf"enfermedad\({id_entidad},.*?\)\.")
            elif tipo == 'sintoma':
                patron = re.compile(rf"sintoma\({id_entidad},.*?\)\.")
            elif tipo == 'medicamento':
                patron = re.compile(rf"medicamento\({id_entidad},.*?\)\.")
            else:
                return False
            
            # Filtrar líneas que no coinciden
            lineas_nuevas = [linea for linea in lineas if not patron.search(linea)]
            
            # Guardar archivo
            with open(self.archivo_pl, 'w', encoding='utf-8') as f:
                f.writelines(lineas_nuevas)
            
            return True
        except Exception as e:
            print(f"Error al eliminar del archivo: {str(e)}")
            return False


if __name__ == "__main__":
    # Pruebas del motor
    try:
        engine = PrologEngine()
        print("\n=== Prueba de Motor Prolog ===\n")
        
        print("Síntomas disponibles:")
        sintomas = engine.obtener_sintomas()
        for s in sintomas[:5]:
            print(f"  - {s['nombre']}: {s['descripcion']}")
        
        print(f"\nTotal síntomas: {len(sintomas)}")
        print(f"Total enfermedades: {len(engine.obtener_enfermedades())}")
        print(f"Total medicamentos: {len(engine.obtener_medicamentos())}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
