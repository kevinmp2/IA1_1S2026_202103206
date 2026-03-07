"""
Módulo de Administrador - MediLogic
Gestión de la base de conocimiento médico
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os


class ModuloAdministrador(ttk.Frame):
    """Módulo para administradores"""
    
    # Credenciales de ejemplo (en producción usar hash y BD)
    USUARIOS = {
        'admin': 'admin123',
        'medico': 'medico123'
    }
    
    def __init__(self, parent, controller, prolog_engine):
        super().__init__(parent)
        self.controller = controller
        self.prolog_engine = prolog_engine
        
        self.autenticado = False
        self.usuario_actual = None
        
        self.configure(style='TFrame')
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crear interfaz del módulo"""
        # La interfaz cambia según autenticación
        if not self.autenticado:
            self.crear_login()
        else:
            self.crear_panel_admin()
    
    def crear_login(self):
        """Crear pantalla de login"""
        # Limpiar frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame de login centrado
        login_frame = ttk.Frame(self, style='TFrame', padding=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título
        ttk.Label(
            login_frame,
            text="🔐 Acceso Administrador",
            style='Title.TLabel',
            font=('Arial', 24, 'bold')
        ).pack(pady=20)
        
        ttk.Label(
            login_frame,
            text="Ingrese sus credenciales para acceder al panel de administración",
            style='Subtitle.TLabel'
        ).pack(pady=10)
        
        # Campos de entrada
        campos_frame = ttk.Frame(login_frame, style='TFrame')
        campos_frame.pack(pady=20)
        
        ttk.Label(campos_frame, text="Usuario:").grid(row=0, column=0, pady=10, sticky='e', padx=5)
        self.usuario_entry = ttk.Entry(campos_frame, width=30)
        self.usuario_entry.grid(row=0, column=1, pady=10)
        
        ttk.Label(campos_frame, text="Contraseña:").grid(row=1, column=0, pady=10, sticky='e', padx=5)
        self.password_entry = ttk.Entry(campos_frame, width=30, show='*')
        self.password_entry.grid(row=1, column=1, pady=10)
        
        # Botones
        botones_frame = ttk.Frame(login_frame, style='TFrame')
        botones_frame.pack(pady=20)
        
        ttk.Button(
            botones_frame,
            text="Iniciar Sesión",
            command=self.autenticar,
            style='Primary.TButton',
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            botones_frame,
            text="Cancelar",
            command=self.volver_inicio,
            width=20
        ).pack(side='left', padx=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.autenticar())
    
    def autenticar(self):
        """Autenticar usuario"""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        
        if usuario in self.USUARIOS and self.USUARIOS[usuario] == password:
            self.autenticado = True
            self.usuario_actual = usuario
            self.crear_widgets()  # Recrear con panel admin
        else:
            messagebox.showerror(
                "Error de Autenticación",
                "Usuario o contraseña incorrectos"
            )
            self.password_entry.delete(0, tk.END)
    
    def crear_panel_admin(self):
        """Crear panel de administración"""
        # Limpiar frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = ttk.Frame(self, style='TFrame')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(
            header_frame,
            text="← Cerrar Sesión",
            command=self.cerrar_sesion
        ).pack(side='left')
        
        ttk.Label(
            header_frame,
            text=f"Panel de Administración - {self.usuario_actual}",
            style='Title.TLabel'
        ).pack(side='left', padx=20)
        
        # Notebook con pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestaña 1: Gestión de Enfermedades
        self.tab_enfermedades = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_enfermedades, text='🦠 Enfermedades')
        self.crear_gestion_enfermedades(self.tab_enfermedades)
        
        # Pestaña 2: Gestión de Síntomas
        self.tab_sintomas = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_sintomas, text='🩺 Síntomas')
        self.crear_gestion_sintomas(self.tab_sintomas)
        
        # Pestaña 3: Gestión de Medicamentos
        self.tab_medicamentos = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_medicamentos, text='💊 Medicamentos')
        self.crear_gestion_medicamentos(self.tab_medicamentos)
        
        # Pestaña 4: Archivo Prolog
        self.tab_prolog = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_prolog, text='📝 Archivo Prolog')
        self.crear_gestion_prolog(self.tab_prolog)
        
        # Pestaña 5: RPA - Automatización
        self.tab_rpa = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_rpa, text='🤖 RPA')
        self.crear_gestion_rpa(self.tab_rpa)
    
    def crear_gestion_enfermedades(self, parent):
        """Crear interfaz de gestión de enfermedades"""
        # Frame principal
        main_frame = ttk.Frame(parent, style='TFrame', padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Nueva Enfermedad",
            command=self.nueva_enfermedad,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Editar",
            command=self.editar_enfermedad,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_enfermedad,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Actualizar",
            command=self.actualizar_lista_enfermedades,
            width=15
        ).pack(side='left', padx=5)
        
        # Treeview para mostrar enfermedades
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree_enfermedades = ttk.Treeview(
            tree_frame,
            columns=('id', 'nombre', 'sistema', 'tipo', 'gravedad'),
            show='headings',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar columnas
        self.tree_enfermedades.heading('id', text='ID')
        self.tree_enfermedades.heading('nombre', text='Nombre')
        self.tree_enfermedades.heading('sistema', text='Sistema')
        self.tree_enfermedades.heading('tipo', text='Tipo')
        self.tree_enfermedades.heading('gravedad', text='Gravedad')
        
        self.tree_enfermedades.column('id', width=80)
        self.tree_enfermedades.column('nombre', width=200)
        self.tree_enfermedades.column('sistema', width=150)
        self.tree_enfermedades.column('tipo', width=120)
        self.tree_enfermedades.column('gravedad', width=100)
        
        self.tree_enfermedades.pack(side='left', fill='both', expand=True)
        
        scrollbar_y.config(command=self.tree_enfermedades.yview)
        scrollbar_x.config(command=self.tree_enfermedades.xview)
        
        # Cargar datos iniciales
        self.actualizar_lista_enfermedades()
    
    def crear_gestion_sintomas(self, parent):
        """Crear interfaz de gestión de síntomas"""
        main_frame = ttk.Frame(parent, style='TFrame', padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Botones
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Nuevo Síntoma",
            command=self.nuevo_sintoma,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Editar",
            command=self.editar_sintoma,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_sintoma,
            width=15
        ).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_sintomas = ttk.Treeview(
            tree_frame,
            columns=('id', 'nombre', 'descripcion', 'sistema'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        self.tree_sintomas.heading('id', text='ID')
        self.tree_sintomas.heading('nombre', text='Nombre')
        self.tree_sintomas.heading('descripcion', text='Descripción')
        self.tree_sintomas.heading('sistema', text='Sistema')
        
        self.tree_sintomas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree_sintomas.yview)
        
        self.actualizar_lista_sintomas()
    
    def crear_gestion_medicamentos(self, parent):
        """Crear interfaz de gestión de medicamentos"""
        main_frame = ttk.Frame(parent, style='TFrame', padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Botones
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Nuevo Medicamento",
            command=self.nuevo_medicamento,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Editar",
            command=self.editar_medicamento,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_medicamento,
            width=15
        ).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_medicamentos = ttk.Treeview(
            tree_frame,
            columns=('id', 'nombre', 'principio', 'tipo'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        self.tree_medicamentos.heading('id', text='ID')
        self.tree_medicamentos.heading('nombre', text='Nombre')
        self.tree_medicamentos.heading('principio', text='Principio Activo')
        self.tree_medicamentos.heading('tipo', text='Tipo')
        
        self.tree_medicamentos.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree_medicamentos.yview)
        
        self.actualizar_lista_medicamentos()
    
    def crear_gestion_prolog(self, parent):
        """Crear interfaz de gestión del archivo Prolog"""
        main_frame = ttk.Frame(parent, style='TFrame', padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Botones
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            btn_frame,
            text="📂 Cargar Archivo .pl",
            command=self.cargar_archivo_pl,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="💾 Guardar Archivo .pl",
            command=self.guardar_archivo_pl,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="📥 Exportar",
            command=self.exportar_archivo_pl,
            width=15
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Recargar",
            command=self.recargar_prolog,
            width=15
        ).pack(side='left', padx=5)
        
        # Área de texto para mostrar/editar el archivo
        ttk.Label(
            main_frame,
            text="Contenido del archivo medilogic.pl:",
            font=('Arial', 11, 'bold')
        ).pack(anchor='w', pady=5)
        
        self.prolog_text = scrolledtext.ScrolledText(
            main_frame,
            width=100,
            height=30,
            font=('Courier', 9),
            wrap=tk.NONE
        )
        self.prolog_text.pack(fill='both', expand=True, pady=10)
        
        # Cargar contenido actual
        self.mostrar_archivo_prolog()
    
    def actualizar_lista_enfermedades(self):
        """Actualizar la lista de enfermedades"""
        # Limpiar treeview
        for item in self.tree_enfermedades.get_children():
            self.tree_enfermedades.delete(item)
        
        # Obtener enfermedades
        enfermedades = self.prolog_engine.obtener_enfermedades()
        
        # Insertar en treeview
        for enf in enfermedades:
            self.tree_enfermedades.insert(
                '',
                'end',
                values=(enf['id'], enf['nombre'], enf['sistema'], enf['tipo'], enf['gravedad'])
            )
    
    def actualizar_lista_sintomas(self):
        """Actualizar la lista de síntomas"""
        for item in self.tree_sintomas.get_children():
            self.tree_sintomas.delete(item)
        
        sintomas = self.prolog_engine.obtener_sintomas()
        
        for sint in sintomas:
            self.tree_sintomas.insert(
                '',
                'end',
                values=(sint['id'], sint['nombre'], sint['descripcion'], sint['sistema'])
            )
    
    def actualizar_lista_medicamentos(self):
        """Actualizar la lista de medicamentos"""
        for item in self.tree_medicamentos.get_children():
            self.tree_medicamentos.delete(item)
        
        medicamentos = self.prolog_engine.obtener_medicamentos()
        
        for med in medicamentos:
            self.tree_medicamentos.insert(
                '',
                'end',
                values=(med['id'], med['nombre'], med['principio'], med['tipo'])
            )
    
    def mostrar_archivo_prolog(self):
        """Mostrar contenido del archivo Prolog"""
        try:
            with open(self.prolog_engine.archivo_pl, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            self.prolog_text.delete(1.0, tk.END)
            self.prolog_text.insert(1.0, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
    
    # Funciones placeholder para CRUD
    def nueva_enfermedad(self):
        messagebox.showinfo("Función en desarrollo", "Crear nueva enfermedad")
    
    def editar_enfermedad(self):
        messagebox.showinfo("Función en desarrollo", "Editar enfermedad")
    
    def eliminar_enfermedad(self):
        messagebox.showinfo("Función en desarrollo", "Eliminar enfermedad")
    
    def nuevo_sintoma(self):
        messagebox.showinfo("Función en desarrollo", "Crear nuevo síntoma")
    
    def editar_sintoma(self):
        messagebox.showinfo("Función en desarrollo", "Editar síntoma")
    
    def eliminar_sintoma(self):
        messagebox.showinfo("Función en desarrollo", "Eliminar síntoma")
    
    def nuevo_medicamento(self):
        messagebox.showinfo("Función en desarrollo", "Crear nuevo medicamento")
    
    def editar_medicamento(self):
        messagebox.showinfo("Función en desarrollo", "Editar medicamento")
    
    def eliminar_medicamento(self):
        messagebox.showinfo("Función en desarrollo", "Eliminar medicamento")
    
    def cargar_archivo_pl(self):
        messagebox.showinfo("Función en desarrollo", "Cargar archivo .pl")
    
    def guardar_archivo_pl(self):
        messagebox.showinfo("Función en desarrollo", "Guardar archivo .pl")
    
    def exportar_archivo_pl(self):
        """Exportar archivo Prolog"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pl",
            filetypes=[("Prolog files", "*.pl"), ("All files", "*.*")]
        )
        if archivo:
            try:
                contenido = self.prolog_text.get(1.0, tk.END)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", "Archivo exportado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")
    
    def recargar_prolog(self):
        """Recargar motor Prolog"""
        if self.prolog_engine.recargar_base_conocimiento():
            messagebox.showinfo("Éxito", "Base de conocimiento recargada")
            self.mostrar_archivo_prolog()
        else:
            messagebox.showerror("Error", "No se pudo recargar")
    
    def crear_gestion_rpa(self, parent):
        """Crear interfaz de gestión RPA"""
        from modulos.rpa import RPA_MediLogic
        
        main_frame = ttk.Frame(parent, style='TFrame', padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Automatización de Procesos (RPA)",
            style='Subtitle.TLabel'
        ).pack(pady=10)
        
        # Frame para carga de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Carga Masiva de Enfermedades", padding=15)
        file_frame.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(
            file_frame,
            text="Seleccione un archivo de texto con el formato especificado:"
        ).pack(anchor='w')
        
        # Frame para botones de archivo
        btn_file_frame = ttk.Frame(file_frame)
        btn_file_frame.pack(fill='x', pady=10)
        
        self.archivo_rpa_var = tk.StringVar()
        
        ttk.Button(
            btn_file_frame,
            text="📁 Seleccionar Archivo",
            command=self.seleccionar_archivo_rpa
        ).pack(side='left', padx=5)
        
        ttk.Label(
            btn_file_frame,
            textvariable=self.archivo_rpa_var,
            foreground='blue'
        ).pack(side='left', padx=10)
        
        # Botones de acción
        action_frame = ttk.Frame(file_frame)
        action_frame.pack(fill='x', pady=10)
        
        ttk.Button(
            action_frame,
            text="▶️ Procesar Archivo",
            command=self.procesar_archivo_rpa,
            width=20
        ).pack(side='left', padx=5)
        
        ttk.Button(
            action_frame,
            text="📊 Ver Informe",
            command=self.ver_informe_rpa,
            width=20
        ).pack(side='left', padx=5)
        
        # Frame para envío de correo
        email_frame = ttk.LabelFrame(main_frame, text="Notificación por Correo", padding=15)
        email_frame.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(email_frame, text="Correo remitente:").grid(row=0, column=0, sticky='w', pady=5)
        self.email_remitente_entry = ttk.Entry(email_frame, width=40)
        self.email_remitente_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(email_frame, text="Contraseña:").grid(row=1, column=0, sticky='w', pady=5)
        self.email_password_entry = ttk.Entry(email_frame, width=40, show='*')
        self.email_password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(email_frame, text="Destinatarios (separados por coma):").grid(row=2, column=0, sticky='w', pady=5)
        self.email_destinatarios_entry = ttk.Entry(email_frame, width=40)
        self.email_destinatarios_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Button(
            email_frame,
            text="📧 Enviar Informe",
            command=self.enviar_informe_correo
        ).grid(row=3, column=1, sticky='e', pady=10)
        
        # Log de operaciones
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Operaciones", padding=10)
        log_frame.pack(fill='both', expand=True, pady=10, padx=10)
        
        self.rpa_log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Consolas', 9)
        )
        self.rpa_log_text.pack(fill='both', expand=True)
        
        # Inicializar RPA
        self.rpa_instance = RPA_MediLogic()
        self.archivo_rpa_seleccionado = None
        self.enfermedades_procesadas = []
        self.archivo_informe_rpa = None
    
    def seleccionar_archivo_rpa(self):
        """Seleccionar archivo para procesamiento RPA"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de enfermedades",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if archivo:
            self.archivo_rpa_seleccionado = archivo
            self.archivo_rpa_var.set(os.path.basename(archivo))
            self.agregar_log_rpa(f"Archivo seleccionado: {archivo}")
    
    def procesar_archivo_rpa(self):
        """Procesar archivo con RPA"""
        if not self.archivo_rpa_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un archivo primero")
            return
        
        try:
            self.agregar_log_rpa("Iniciando procesamiento...")
            
            # Cargar enfermedades
            self.enfermedades_procesadas = self.rpa_instance.cargar_enfermedades_desde_archivo(
                self.archivo_rpa_seleccionado
            )
            
            # Clasificar cada enfermedad
            for enf in self.enfermedades_procesadas:
                self.rpa_instance.clasificar_enfermedad(enf)
            
            # Generar informe
            self.archivo_informe_rpa = self.rpa_instance.generar_informe_txt(
                self.enfermedades_procesadas
            )
            
            # Mostrar logs
            for log in self.rpa_instance.obtener_log():
                self.agregar_log_rpa(log)
            
            messagebox.showinfo(
                "Éxito",
                f"Se procesaron {len(self.enfermedades_procesadas)} enfermedades correctamente"
            )
            
        except Exception as e:
            error_msg = f"Error al procesar archivo: {str(e)}"
            self.agregar_log_rpa(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def ver_informe_rpa(self):
        """Ver informe generado por RPA"""
        if not self.archivo_informe_rpa or not os.path.exists(self.archivo_informe_rpa):
            messagebox.showwarning("Advertencia", "No hay informe disponible. Procese un archivo primero.")
            return
        
        # Abrir archivo de informe
        try:
            os.startfile(self.archivo_informe_rpa)
        except:
            # En sistemas no Windows
            import subprocess
            subprocess.run(['xdg-open', self.archivo_informe_rpa])
    
    def enviar_informe_correo(self):
        """Enviar informe por correo electrónico"""
        if not self.archivo_informe_rpa or not os.path.exists(self.archivo_informe_rpa):
            messagebox.showwarning("Advertencia", "No hay informe para enviar. Procese un archivo primero.")
            return
        
        remitente = self.email_remitente_entry.get()
        password = self.email_password_entry.get()
        destinatarios_str = self.email_destinatarios_entry.get()
        
        if not remitente or not password or not destinatarios_str:
            messagebox.showwarning("Advertencia", "Complete todos los campos de correo")
            return
        
        destinatarios = [d.strip() for d in destinatarios_str.split(',')]
        
        try:
            self.agregar_log_rpa("Enviando correo...")
            
            exito = self.rpa_instance.enviar_informe_por_correo(
                archivo_informe=self.archivo_informe_rpa,
                destinatarios=destinatarios,
                remitente=remitente,
                password=password
            )
            
            if exito:
                messagebox.showinfo("Éxito", "Informe enviado por correo correctamente")
                self.agregar_log_rpa("✓ Correo enviado exitosamente")
            else:
                messagebox.showerror("Error", "No se pudo enviar el correo")
                
        except Exception as e:
            error_msg = f"Error al enviar correo: {str(e)}"
            self.agregar_log_rpa(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def agregar_log_rpa(self, mensaje):
        """Agregar mensaje al log de RPA"""
        self.rpa_log_text.insert(tk.END, mensaje + '\n')
        self.rpa_log_text.see(tk.END)
    
    def cerrar_sesion(self):
        """Cerrar sesión de administrador"""
        self.autenticado = False
        self.usuario_actual = None
        self.crear_widgets()
    
    def volver_inicio(self):
        """Volver a la pantalla de inicio"""
        self.controller.mostrar_frame("Inicio")
    
    def refresh(self):
        """Refrescar el módulo"""
        if not self.autenticado:
            self.crear_login()
