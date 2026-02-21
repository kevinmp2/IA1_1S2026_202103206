"""
Pantalla de inicio de MediLogic
"""

import tkinter as tk
from tkinter import ttk


class PantallaInicio(ttk.Frame):
    """Pantalla principal de bienvenida"""
    
    def __init__(self, parent, controller, prolog_engine):
        super().__init__(parent)
        self.controller = controller
        self.prolog_engine = prolog_engine
        
        self.configure(style='TFrame')
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crear elementos de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self, style='TFrame', padding=40)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo/Título
        titulo = ttk.Label(
            main_frame,
            text="MediLogic",
            style='Title.TLabel',
            font=('Arial', 48, 'bold'),
            foreground='#2c5f8d'
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ttk.Label(
            main_frame,
            text="Sistema Experto de Diagnóstico Médico",
            style='Subtitle.TLabel',
            font=('Arial', 16)
        )
        subtitulo.pack(pady=10)
        
        # Descripción
        descripcion = ttk.Label(
            main_frame,
            text=(
                "MediLogic es una herramienta de apoyo diagnóstico preliminar\n"
                "que utiliza inteligencia artificial y lógica computacional\n"
                "para analizar síntomas y sugerir posibles diagnósticos.\n\n"
                "⚠️ IMPORTANTE: Esta herramienta no sustituye la consulta médica profesional"
            ),
            style='TLabel',
            font=('Arial', 11),
            justify='center',
            foreground='#555'
        )
        descripcion.pack(pady=30)
        
        # Frame para botones
        botones_frame = ttk.Frame(main_frame, style='TFrame')
        botones_frame.pack(pady=20)
        
        # Botón Módulo Paciente
        btn_paciente = ttk.Button(
            botones_frame,
            text="🏥 Módulo Paciente",
            command=self.ir_a_paciente,
            style='Primary.TButton',
            width=25
        )
        btn_paciente.pack(pady=10)
        
        # Botón Módulo Administrador
        btn_admin = ttk.Button(
            botones_frame,
            text="⚕️ Módulo Administrador",
            command=self.ir_a_administrador,
            style='Primary.TButton',
            width=25
        )
        btn_admin.pack(pady=10)
        
        # Información adicional
        info_frame = ttk.Frame(main_frame, style='TFrame')
        info_frame.pack(pady=30)
        
        info = ttk.Label(
            info_frame,
            text=(
                "Desarrollado por: [Tu Nombre]\n"
                "Carnet: [Tu Carnet]\n"
                "Curso: Inteligencia Artificial 1 - 1S2026\n"
                "Universidad de San Carlos de Guatemala"
            ),
            style='TLabel',
            font=('Arial', 9),
            justify='center',
            foreground='#777'
        )
        info.pack()
    
    def ir_a_paciente(self):
        """Navegar al módulo de paciente"""
        self.controller.mostrar_frame("Paciente")
    
    def ir_a_administrador(self):
        """Navegar al módulo de administrador"""
        self.controller.mostrar_frame("Administrador")
    
    def refresh(self):
        """Refrescar la pantalla"""
        pass
