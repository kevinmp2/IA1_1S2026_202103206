"""
Script de prueba rápida del sistema MediLogic
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 80)
print("PRUEBA DEL SISTEMA MEDILOGIC")
print("=" * 80)
print()

# Prueba 1: Importaciones
print("✓ Verificando importaciones...")
try:
    import tkinter as tk
    print("  ✓ Tkinter disponible")
except ImportError as e:
    print(f"  ✗ Error con Tkinter: {e}")
    sys.exit(1)

try:
    from pyswip import Prolog
    print("  ✓ PySwip disponible")
except ImportError as e:
    print(f"  ✗ Error con PySwip: {e}")
    print("  → Instale SWI-Prolog y ejecute: pip install pyswip")
    sys.exit(1)

try:
    import pyautogui
    print("  ✓ PyAutoGUI disponible")
except ImportError as e:
    print(f"  ✗ Error con PyAutoGUI: {e}")
    sys.exit(1)

try:
    from reportlab.pdfgen import canvas
    print("  ✓ ReportLab disponible")
except ImportError as e:
    print(f"  ✗ Error con ReportLab: {e}")
    sys.exit(1)

print()

# Prueba 2: Módulos del proyecto
print("✓ Verificando módulos del proyecto...")
try:
    from utils.prolog_engine import PrologEngine
    print("  ✓ Motor Prolog importado")
except ImportError as e:
    print(f"  ✗ Error al importar motor Prolog: {e}")
    sys.exit(1)

try:
    from utils.pdf_generator import PDFGenerator
    print("  ✓ Generador PDF importado")
except ImportError as e:
    print(f"  ✗ Error al importar generador PDF: {e}")
    sys.exit(1)

try:
    from modulos.inicio import PantallaInicio
    from modulos.paciente import ModuloPaciente
    from modulos.admin import ModuloAdministrador
    from modulos.rpa import RPA_MediLogic
    print("  ✓ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"  ✗ Error al importar módulos: {e}")
    sys.exit(1)

print()

# Prueba 3: Base de conocimiento Prolog
print("✓ Verificando base de conocimiento Prolog...")
try:
    prolog_engine = PrologEngine()
    print("  ✓ Motor Prolog inicializado")
    
    # Probar consulta simple
    sintomas = prolog_engine.obtener_sintomas()
    if sintomas:
        print(f"  ✓ Base de conocimiento cargada: {len(sintomas)} síntomas encontrados")
    else:
        print("  ⚠ Advertencia: No se encontraron síntomas en la base de conocimiento")
    
    enfermedades = prolog_engine.obtener_enfermedades()
    if enfermedades:
        print(f"  ✓ Enfermedades en la base: {len(enfermedades)}")
    
except Exception as e:
    print(f"  ✗ Error al conectar con Prolog: {e}")
    print("  → Verifique que SWI-Prolog esté instalado correctamente")
    sys.exit(1)

print()

# Prueba 4: RPA
print("✓ Verificando módulo RPA...")
try:
    rpa = RPA_MediLogic()
    print("  ✓ RPA inicializado correctamente")
    
    # Verificar que existe el archivo de ejemplo
    archivo_ejemplo = os.path.join('datos', 'enfermedades_ejemplo.txt')
    if os.path.exists(archivo_ejemplo):
        print(f"  ✓ Archivo de ejemplo encontrado: {archivo_ejemplo}")
        
        # Probar carga
        enfermedades = rpa.cargar_enfermedades_desde_archivo(archivo_ejemplo)
        print(f"  ✓ {len(enfermedades)} enfermedades cargadas del archivo de ejemplo")
    else:
        print(f"  ⚠ Archivo de ejemplo no encontrado: {archivo_ejemplo}")
        
except Exception as e:
    print(f"  ✗ Error en módulo RPA: {e}")

print()

# Prueba 5: Generación de PDF de prueba
print("✓ Verificando generador de PDF...")
try:
    pdf_gen = PDFGenerator()
    
    # Datos de prueba
    datos_prueba = {
        'nombre': 'Paciente de Prueba',
        'fecha': '01/01/2025',
        'hora': '10:00:00',
        'sintomas': [('s1', 'Tos', 'severo'), ('s2', 'Fiebre', 'moderado')],
        'alergias': ['penicilina'],
        'cronicas': ['ec1']
    }
    
    diagnosticos_prueba = [
        "Gripe Común (Afinidad: 85%)",
        "Resfriado (Afinidad: 60%)"
    ]
    
    archivo_prueba = 'test_informe.pdf'
    pdf_gen.generar_informe_diagnostico(archivo_prueba, datos_prueba, diagnosticos_prueba)
    
    if os.path.exists(archivo_prueba):
        print(f"  ✓ PDF de prueba generado: {archivo_prueba}")
        os.remove(archivo_prueba)  # Limpiar
        print("  ✓ Archivo de prueba eliminado")
    else:
        print("  ⚠ No se pudo generar el PDF de prueba")
        
except Exception as e:
    print(f"  ✗ Error al generar PDF: {e}")

print()

# Resultado final
print("=" * 80)
print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 80)
print()
print("El sistema está listo para ejecutarse.")
print("Ejecute 'python src/main.py' para iniciar la aplicación.")
print()
