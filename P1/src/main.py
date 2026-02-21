"""
MEDILOGIC - Sistema Experto de Diagnóstico Médico
Archivo principal de la aplicación
Autor: [Tu Nombre]
Carnet: [Tu Carnet]
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio src al path para imports
sys.path.append(os.path.dirname(__file__))

from modulos.inicio import PantallaInicio
from modulos.paciente import ModuloPaciente
from modulos.admin import ModuloAdministrador
from utils.prolog_engine import PrologEngine


class MediLogicApp:
    """Aplicación principal de MediLogic"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MediLogic - Sistema Experto de Diagnóstico Médico")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Inicializar motor Prolog
        try:
            self.prolog_engine = PrologEngine()
            print("✓ Motor Prolog inicializado correctamente")
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"No se pudo inicializar el motor Prolog:\n{str(e)}"
            )
            sys.exit(1)
        
        # Container principal
        self.container = ttk.Frame(root)
        self.container.pack(fill='both', expand=True)
        
        # Diccionario para almacenar frames
        self.frames = {}
        
        # Crear todos los frames
        self.crear_frames()
        
        # Mostrar pantalla de inicio
        self.mostrar_frame("Inicio")
    
    def configurar_estilos(self):
        """Configurar estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema médico
        style.configure('TFrame', background='#f0f4f8')
        style.configure('TLabel', background='#f0f4f8', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), foreground='#2c5f8d')
        style.configure('Subtitle.TLabel', font=('Arial', 14), foreground='#4a6fa5')
        style.configure('TButton', font=('Arial', 11), padding=10)
        style.configure('Primary.TButton', font=('Arial', 12, 'bold'))
        
    def crear_frames(self):
        """Crear todos los frames de la aplicación"""
        # Frame de inicio
        self.frames["Inicio"] = PantallaInicio(
            self.container, 
            self,
            self.prolog_engine
        )
        self.frames["Inicio"].grid(row=0, column=0, sticky='nsew')
        
        # Frame de paciente
        self.frames["Paciente"] = ModuloPaciente(
            self.container,
            self,
            self.prolog_engine
        )
        self.frames["Paciente"].grid(row=0, column=0, sticky='nsew')
        
        # Frame de administrador
        self.frames["Administrador"] = ModuloAdministrador(
            self.container,
            self,
            self.prolog_engine
        )
        self.frames["Administrador"].grid(row=0, column=0, sticky='nsew')
        
        # Configurar peso de filas y columnas
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
    def mostrar_frame(self, nombre_frame):
        """Mostrar un frame específico"""
        frame = self.frames[nombre_frame]
        frame.tkraise()
        
        # Refrescar frame si tiene método refresh
        if hasattr(frame, 'refresh'):
            frame.refresh()


def main():
    """Función principal"""
    root = tk.Tk()
    app = MediLogicApp(root)
    
    # Centrar ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Ejecutar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
