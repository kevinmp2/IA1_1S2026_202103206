"""
Módulo de Pacientes - MediLogic
Permite a los usuarios ingresar síntomas y obtener diagnósticos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


class ModuloPaciente(ttk.Frame):
    """Módulo para pacientes"""
    
    def __init__(self, parent, controller, prolog_engine):
        super().__init__(parent)
        self.controller = controller
        self.prolog_engine = prolog_engine
        
        # Variables
        self.sintomas_seleccionados = {}  # {id_sintoma: severidad}
        self.alergias = []
        self.enfermedades_cronicas_selec = []
        self.historial_diagnosticos = []
        
        # Configurar frame
        self.configure(style='TFrame')
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crear interfaz del módulo"""
        # Header
        header_frame = ttk.Frame(self, style='TFrame')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(
            header_frame,
            text="← Volver",
            command=self.volver_inicio
        ).pack(side='left')
        
        ttk.Label(
            header_frame,
            text="Módulo de Paciente",
            style='Title.TLabel'
        ).pack(side='left', padx=20)
        
        # Contenedor principal con scroll
        canvas = tk.Canvas(self, bg='#f0f4f8', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido principal
        self.crear_formulario(scrollable_frame)
    
    def crear_formulario(self, parent):
        """Crear formulario de ingreso de datos"""
        # Frame del formulario
        form_frame = ttk.Frame(parent, style='TFrame')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Sección 1: Síntomas
        self.crear_seccion_sintomas(form_frame)
        
        # Sección 2: Alergias
        self.crear_seccion_alergias(form_frame)
        
        # Sección 3: Enfermedades Crónicas
        self.crear_seccion_cronicas(form_frame)
        
        # Botones de acción
        self.crear_botones_accion(form_frame)
        
        # Área de resultados
        self.crear_area_resultados(form_frame)
    
    def crear_seccion_sintomas(self, parent):
        """Crear sección de selección de síntomas"""
        # Frame de la sección
        section_frame = ttk.LabelFrame(
            parent,
            text="1. Seleccione sus síntomas e indique la severidad",
            padding=15
        )
        section_frame.pack(fill='x', pady=10)
        
        # Obtener síntomas del motor Prolog
        sintomas = self.prolog_engine.obtener_sintomas()
        
        # Agrupar por sistema
        sintomas_por_sistema = {}
        for s in sintomas:
            sistema = s['sistema']
            if sistema not in sintomas_por_sistema:
                sintomas_por_sistema[sistema] = []
            sintomas_por_sistema[sistema].append(s)
        
        # Crear checkboxes por sistema
        self.sintomas_vars = {}
        self.severidad_vars = {}
        
        for sistema, lista_sintomas in sintomas_por_sistema.items():
            # Frame para cada sistema
            sistema_frame = ttk.LabelFrame(
                section_frame,
                text=sistema.capitalize(),
                padding=10
            )
            sistema_frame.pack(fill='x', pady=5)
            
            for sintoma in lista_sintomas:
                # Frame para cada síntoma
                sintoma_frame = ttk.Frame(sistema_frame)
                sintoma_frame.pack(fill='x', pady=2)
                
                # Checkbox del síntoma
                var_check = tk.BooleanVar()
                self.sintomas_vars[sintoma['id']] = var_check
                
                check = ttk.Checkbutton(
                    sintoma_frame,
                    text=f"{sintoma['nombre']} - {sintoma['descripcion']}",
                    variable=var_check,
                    command=lambda sid=sintoma['id']: self.toggle_severidad(sid)
                )
                check.pack(side='left', padx=5)
                
                # ComboBox de severidad (inicialmente deshabilitado)
                var_sev = tk.StringVar(value="moderado")
                self.severidad_vars[sintoma['id']] = var_sev
                
                combo_sev = ttk.Combobox(
                    sintoma_frame,
                    textvariable=var_sev,
                    values=['leve', 'moderado', 'severo'],
                    state='disabled',
                    width=10
                )
                combo_sev.pack(side='right', padx=5)
    
    def toggle_severidad(self, sintoma_id):
        """Habilitar/deshabilitar selector de severidad"""
        # Buscar el combobox correspondiente y cambiar su estado
        pass
    
    def crear_seccion_alergias(self, parent):
        """Crear sección de alergias"""
        section_frame = ttk.LabelFrame(
            parent,
            text="2. Alergias a medicamentos",
            padding=15
        )
        section_frame.pack(fill='x', pady=10)
        
        ttk.Label(
            section_frame,
            text="Ingrese alergias conocidas (separadas por comas):"
        ).pack(anchor='w', pady=5)
        
        self.alergias_entry = ttk.Entry(section_frame, width=60)
        self.alergias_entry.pack(fill='x', pady=5)
        
        ttk.Label(
            section_frame,
            text="Ejemplo: Penicilina, Ibuprofeno, Paracetamol",
            font=('Arial', 9, 'italic'),
            foreground='#777'
        ).pack(anchor='w')
    
    def crear_seccion_cronicas(self, parent):
        """Crear sección de enfermedades crónicas"""
        section_frame = ttk.LabelFrame(
            parent,
            text="3. Enfermedades crónicas preexistentes",
            padding=15
        )
        section_frame.pack(fill='x', pady=10)
        
        # Obtener enfermedades crónicas del motor
        cronicas = self.prolog_engine.obtener_enfermedades_cronicas()
        
        self.cronicas_vars = {}
        
        for ec in cronicas:
            var = tk.BooleanVar()
            self.cronicas_vars[ec['id']] = var
            
            check = ttk.Checkbutton(
                section_frame,
                text=f"{ec['nombre']} ({ec['sistema']})",
                variable=var
            )
            check.pack(anchor='w', pady=2)
    
    def crear_botones_accion(self, parent):
        """Crear botones de acción"""
        buttons_frame = ttk.Frame(parent, style='TFrame')
        buttons_frame.pack(pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Analizar y Diagnosticar",
            command=self.realizar_diagnostico,
            style='Primary.TButton',
            width=25
        ).pack(side='left', padx=10)
        
        ttk.Button(
            buttons_frame,
            text="🔄 Limpiar Formulario",
            command=self.limpiar_formulario,
            width=20
        ).pack(side='left', padx=10)
    
    def crear_area_resultados(self, parent):
        """Crear área para mostrar resultados"""
        results_frame = ttk.LabelFrame(
            parent,
            text="Resultados del Diagnóstico",
            padding=15
        )
        results_frame.pack(fill='both', expand=True, pady=10)
        
        self.resultados_text = scrolledtext.ScrolledText(
            results_frame,
            width=100,
            height=20,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.resultados_text.pack(fill='both', expand=True)
        
        # Botones adicionales
        btn_frame = ttk.Frame(results_frame, style='TFrame')
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="📄 Descargar PDF",
            command=self.descargar_pdf,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="📋 Ver Historial",
            command=self.ver_historial,
            width=20
        ).pack(side='left', padx=5)
    
    def realizar_diagnostico(self):
        """Realizar diagnóstico con los datos ingresados"""
        # Recopilar síntomas seleccionados
        sintomas_paciente = []
        for sintoma_id, var_check in self.sintomas_vars.items():
            if var_check.get():
                severidad = self.severidad_vars[sintoma_id].get()
                sintomas_paciente.append((sintoma_id, severidad))
        
        if not sintomas_paciente:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar al menos un síntoma para realizar el diagnóstico."
            )
            return
        
        # Recopilar alergias
        alergias_texto = self.alergias_entry.get().strip()
        alergias = [a.strip() for a in alergias_texto.split(',') if a.strip()]
        
        # Recopilar enfermedades crónicas
        cronicas = [ec_id for ec_id, var in self.cronicas_vars.items() if var.get()]
        
        # Realizar diagnóstico usando Prolog
        try:
            diagnosticos = self.prolog_engine.diagnosticar(
                sintomas_paciente,
                alergias,
                cronicas
            )
            
            # Mostrar resultados
            self.mostrar_resultados(diagnosticos, sintomas_paciente, alergias, cronicas)
            
            # Guardar en historial
            self.historial_diagnosticos.append({
                'fecha': datetime.now(),
                'sintomas': sintomas_paciente,
                'alergias': alergias,
                'cronicas': cronicas,
                'diagnosticos': diagnosticos
            })
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al realizar diagnóstico:\n{str(e)}"
            )
    
    def mostrar_resultados(self, diagnosticos, sintomas, alergias, cronicas):
        """Mostrar resultados del diagnóstico"""
        self.resultados_text.delete(1.0, tk.END)
        
        # Encabezado
        texto = "=" * 80 + "\n"
        texto += "INFORME DE DIAGNÓSTICO MÉDICO PRELIMINAR - MEDILOGIC\n"
        texto+= "=" * 80 + "\n\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        # Datos del paciente
        texto += "DATOS INGRESADOS:\n"
        texto += "-" * 80 + "\n"
        texto += f"Síntomas reportados: {len(sintomas)}\n"
        texto += f"Alergias declaradas: {len(alergias)}\n"
        texto += f"Enfermedades crónicas: {len(cronicas)}\n\n"
        
        # Resultados
        if diagnosticos:
            texto += "DIAGNÓSTICOS SUGERIDOS:\n"
            texto += "-" * 80 + "\n\n"
            
            for i, diag in enumerate(diagnosticos, 1):
                texto += f"{i}. {diag}\n\n"  # Formato depende de cómo retorne Prolog
        else:
            texto += "No se encontraron diagnósticos compatibles con los síntomas ingresados.\n"
            texto += "Se recomienda consultar con un profesional de la salud.\n"
        
        # Advertencia
        texto += "\n" + "=" * 80 + "\n"
        texto += "⚠️ ADVERTENCIA IMPORTANTE:\n"
        texto += "Este es un sistema de apoyo diagnóstico preliminar.\n"
        texto += "NO sustituye la consulta con un médico profesional.\n"
        texto += "Siempre busque atención médica calificada.\n"
        texto += "=" * 80 + "\n"
        
        self.resultados_text.insert(1.0, texto)
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        # Deseleccionar síntomas
        for var in self.sintomas_vars.values():
            var.set(False)
        
        # Resetear severidades
        for var in self.severidad_vars.values():
            var.set("moderado")
        
        # Limpiar alergias
        self.alergias_entry.delete(0, tk.END)
        
        # Deseleccionar enfermedades crónicas
        for var in self.cronicas_vars.values():
            var.set(False)
        
        # Limpiar resultados
        self.resultados_text.delete(1.0, tk.END)
    
    def descargar_pdf(self):
        """Descargar informe en PDF"""
        if not self.historial_diagnosticos:
            messagebox.showwarning(
                "Sin datos",
                "Realice un diagnóstico primero para generar el PDF"
            )
            return
        
        # Obtener último diagnóstico
        ultimo = self.historial_diagnosticos[-1]
        
        # Solicitar ubicación de guardado
        from tkinter import filedialog
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"informe_medilogic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not archivo:
            return  # Usuario canceló
        
        try:
            from utils.pdf_generator import PDFGenerator
            
            # Preparar datos del paciente
            datos_paciente = {
                'nombre': 'Paciente',  # Podría agregarse un campo de nombre
                'fecha': ultimo['fecha'].strftime('%d/%m/%Y'),
                'hora': ultimo['fecha'].strftime('%H:%M:%S'),
                'sintomas': ultimo['sintomas'],
                'alergias': ultimo['alergias'],
                'cronicas': ultimo['cronicas']
            }
            
            # Generar PDF
            pdf_gen = PDFGenerator()
            pdf_gen.generar_informe_diagnostico(
                archivo,
                datos_paciente,
                ultimo['diagnosticos']
            )
            
            messagebox.showinfo(
                "Éxito",
                f"Informe PDF generado correctamente:\n{archivo}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el PDF:\n{str(e)}"
            )
    
    def ver_historial(self):
        """Ver historial de diagnósticos"""
        if not self.historial_diagnosticos:
            messagebox.showinfo(
                "Historial",
                "No hay diagnósticos previos en esta sesión"
            )
            return
        
        # Crear ventana de historial
        ventana = tk.Toplevel(self)
        ventana.title("Historial de Diagnósticos")
        ventana.geometry("600x400")
        
        texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD)
        texto.pack(fill='both', expand=True, padx=10, pady=10)
        
        for i, hist in enumerate(self.historial_diagnosticos, 1):
            texto.insert(tk.END, f"\n{'='*60}\n")
            texto.insert(tk.END, f"Diagnóstico #{i}\n")
            texto.insert(tk.END, f"Fecha: {hist['fecha'].strftime('%d/%m/%Y %H:%M:%S')}\n")
            texto.insert(tk.END, f"Síntomas: {len(hist['sintomas'])}\n")
            texto.insert(tk.END, f"{'='*60}\n")
    
    def volver_inicio(self):
        """Volver a la pantalla de inicio"""
        self.controller.mostrar_frame("Inicio")
    
    def refresh(self):
        """Refrescar el módulo"""
        pass
