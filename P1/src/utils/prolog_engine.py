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
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_proyecto = os.path.dirname(os.path.dirname(ruta_actual))
        ruta_pl = os.path.join(ruta_proyecto, 'base_conocimiento', 'medilogic.pl')
        return ruta_pl
    
    def cargar_base_conocimiento(self):
        """Cargar el archivo Prolog con la base de conocimiento"""
        try:
            # Convertir ruta a formato Unix para Windows
            ruta_unix = self.archivo_pl.replace('\\', '/')
            self.prolog.consult(ruta_unix)
            print(f"✓ Base de conocimiento cargada desde: {self.archivo_pl}")
        except Exception as e:
            raise Exception(f"Error al cargar base de conocimiento: {str(e)}")
    
    def recargar_base_conocimiento(self):
        """Recargar el archivo Prolog"""
        try:
            self.prolog.retractall("sintoma(_, _, _, _)")
            self.prolog.retractall("enfermedad(_, _, _, _, _, _)")
            self.prolog.retractall("medicamento(_, _, _, _, _)")
            self.cargar_base_conocimiento()
            return True
        except Exception as e:
            print(f"Error al recargar: {str(e)}")
            return False
    
    def consultar(self, query):
        """
        Realizar una consulta a Prolog
        
        Args:
            query (str): Consulta en sintaxis Prolog
            
        Returns:
            list: Lista de resultados
        """
        try:
            resultados = list(self.prolog.query(query))
            return resultados
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
        # Esta función guardará los cambios permanentemente
        # Implementación completa más adelante
        pass


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
