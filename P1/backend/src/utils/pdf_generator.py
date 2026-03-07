"""
Generador de informes PDF para MediLogic
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO


class PDFGenerator:
    """Generador de informes PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configurar estilos personalizados"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c5f8d'),
            spaceAfter=30,
            alignment=1  # Centrado
        ))
        
        # Estilo para advertencias
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            borderColor=colors.red,
            borderWidth=1,
            borderPadding=10,
            spaceAfter=20
        ))
    
    def generar_informe_diagnostico(
        self,
        archivo_salida,
        sintomas,
        alergias,
        enfermedades_cronicas,
        diagnosticos
    ):
        """
        Generar informe de diagnóstico en PDF
        
        Args:
            archivo_salida (str): Ruta del archivo PDF a generar
            sintomas (list): Lista de síntomas del paciente
            alergias (list): Lista de alergias
            enfermedades_cronicas (list): Lista de enfermedades crónicas
            diagnosticos (list): Lista de diagnósticos generados
        """
        try:
            # Crear documento
            doc = SimpleDocTemplate(
                archivo_salida,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenedor de elementos
            elements = []
            
            # Título
            elements.append(Paragraph(
                "INFORME DE DIAGNÓSTICO MÉDICO PRELIMINAR",
                self.styles['CustomTitle']
            ))
            elements.append(Spacer(1, 12))
            
            # Subtítulo
            elements.append(Paragraph(
                "Sistema MediLogic - Diagnóstico Asistido por IA",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            elements.append(Paragraph(
                f"<b>Fecha del diagnóstico:</b> {fecha_actual}",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 20))
            
            # Datos del paciente
            elements.append(Paragraph(
                "<b>DATOS INGRESADOS</b>",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            # Tabla de datos
            data_paciente = [
                ['Síntomas reportados:', str(len(sintomas))],
                ['Alergias declaradas:', str(len(alergias))],
                ['Enfermedades crónicas:', str(len(enfermedades_cronicas))]
            ]
            
            tabla_datos = Table(data_paciente, colWidths=[3*inch, 3*inch])
            tabla_datos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(tabla_datos)
            elements.append(Spacer(1, 20))
            
            # Diagnósticos
            elements.append(Paragraph(
                "<b>DIAGNÓSTICOS SUGERIDOS</b>",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            if diagnosticos:
                for i, diag in enumerate(diagnosticos, 1):
                    elements.append(Paragraph(
                        f"<b>{i}. {diag.get('nombre', 'N/A')}</b>",
                        self.styles['Heading3']
                    ))
                    elements.append(Paragraph(
                        f"Afinidad: {diag.get('afinidad', 0):.1f}%",
                        self.styles['Normal']
                    ))
                    elements.append(Paragraph(
                        f"Gravedad: {diag.get('gravedad', 'N/A')}",
                        self.styles['Normal']
                    ))
                    elements.append(Spacer(1, 12))
            else:
                elements.append(Paragraph(
                    "No se encontraron diagnósticos compatibles.",
                    self.styles['Normal']
                ))
            
            elements.append(Spacer(1, 30))
            
            # Advertencia
            warning_text = """
            <b>⚠️ ADVERTENCIA IMPORTANTE:</b><br/>
            Este es un sistema de apoyo diagnóstico preliminar basado en inteligencia artificial.
            <b>NO sustituye la consulta con un médico profesional.</b><br/>
            Siempre busque atención médica calificada para diagnósticos y tratamientos definitivos.
            """
            elements.append(Paragraph(warning_text, self.styles['Warning']))
            
            # Pie de página
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(
                "MediLogic - Universidad de San Carlos de Guatemala",
                self.styles['Normal']
            ))
            
            # Generar PDF
            doc.build(elements)
            return True
            
        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return False
    
    def generar_informe_en_memoria(
        self,
        sintomas,
        alergias,
        enfermedades_cronicas,
        diagnosticos
    ):
        """
        Generar informe de diagnóstico en memoria (BytesIO) sin guardarlo en disco
        
        Args:
            sintomas (list): Lista de síntomas del paciente
            alergias (list): Lista de alergias
            enfermedades_cronicas (list): Lista de enfermedades crónicas
            diagnosticos (list): Lista de diagnósticos generados
            
        Returns:
            BytesIO: Buffer con el contenido del PDF
        """
        try:
            # Crear buffer en memoria
            buffer = BytesIO()
            
            # Crear documento
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenedor de elementos
            elements = []
            
            # Título
            elements.append(Paragraph(
                "INFORME DE DIAGNÓSTICO MÉDICO PRELIMINAR",
                self.styles['CustomTitle']
            ))
            elements.append(Spacer(1, 12))
            
            # Subtítulo
            elements.append(Paragraph(
                "Sistema MediLogic - Diagnóstico Asistido por IA",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            # Fecha
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            elements.append(Paragraph(
                f"<b>Fecha del diagnóstico:</b> {fecha_actual}",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 20))
            
            # Datos del paciente
            elements.append(Paragraph(
                "<b>DATOS INGRESADOS</b>",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            # Tabla de datos
            data_paciente = [
                ['Síntomas reportados:', str(len(sintomas))],
                ['Alergias declaradas:', str(len(alergias))],
                ['Enfermedades crónicas:', str(len(enfermedades_cronicas))]
            ]
            
            tabla_datos = Table(data_paciente, colWidths=[3*inch, 3*inch])
            tabla_datos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(tabla_datos)
            elements.append(Spacer(1, 20))
            
            # Diagnósticos
            elements.append(Paragraph(
                "<b>DIAGNÓSTICOS SUGERIDOS</b>",
                self.styles['Heading2']
            ))
            elements.append(Spacer(1, 12))
            
            if diagnosticos:
                for i, diag in enumerate(diagnosticos, 1):
                    elements.append(Paragraph(
                        f"<b>{i}. {diag.get('nombre', 'N/A')}</b>",
                        self.styles['Heading3']
                    ))
                    elements.append(Paragraph(
                        f"Afinidad: {diag.get('afinidad', 0):.1f}%",
                        self.styles['Normal']
                    ))
                    elements.append(Paragraph(
                        f"Gravedad: {diag.get('gravedad', 'N/A')}",
                        self.styles['Normal']
                    ))
                    elements.append(Spacer(1, 12))
            else:
                elements.append(Paragraph(
                    "No se encontraron diagnósticos compatibles.",
                    self.styles['Normal']
                ))
            
            elements.append(Spacer(1, 30))
            
            # Advertencia
            warning_text = """
            <b>⚠️ ADVERTENCIA IMPORTANTE:</b><br/>
            Este es un sistema de apoyo diagnóstico preliminar basado en inteligencia artificial.
            <b>NO sustituye la consulta con un médico profesional.</b><br/>
            Siempre busque atención médica calificada para diagnósticos y tratamientos definitivos.
            """
            elements.append(Paragraph(warning_text, self.styles['Warning']))
            
            # Pie de página
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(
                "MediLogic - Universidad de San Carlos de Guatemala",
                self.styles['Normal']
            ))
            
            # Generar PDF en memoria
            doc.build(elements)
            
            # Posicionar el cursor al inicio del buffer
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            print(f"Error al generar PDF en memoria: {str(e)}")
            return None


if __name__ == "__main__":
    # Prueba del generador
    generator = PDFGenerator()
    
    # Datos de prueba
    sintomas_test = [('s1', 'moderado'), ('s2', 'severo')]
    alergias_test = ['Penicilina']
    cronicas_test = ['ec1']
    diagnosticos_test = [
        {'nombre': 'Gripe', 'afinidad': 85.5, 'gravedad': 'moderada'},
        {'nombre': 'Resfriado común', 'afinidad': 65.2, 'gravedad': 'leve'}
    ]
    
    resultado = generator.generar_informe_diagnostico(
        'test_informe.pdf',
        sintomas_test,
        alergias_test,
        cronicas_test,
        diagnosticos_test
    )
    
    if resultado:
        print("✓ PDF de prueba generado correctamente")
    else:
        print("✗ Error al generar PDF")
