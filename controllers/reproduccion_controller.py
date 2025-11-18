# reproduccion_controller.py - VERSIÓN COMPLETA CORREGIDA
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from datetime import datetime
import os
import tempfile

class ReproduccionController:
    def __init__(self, reproduccion_widget):
        self.reproduccion_widget = reproduccion_widget
        self.db = Database()
        self.setup_connections()
        self.configurar_tabla()
        print("✅ ReproduccionController inicializado")
        
        # Variable para controlar diálogos abiertos
        self.dialogo_abierto = False
        
        # Cargar datos automáticamente al iniciar
        self.cargar_registros_reproduccion()
        
    def setup_connections(self):
        """Configura las conexiones de los elementos UI según el diseño"""
        try:
            print("🔍 Configurando conexiones para Reproducción...")
            
            # Buscar elementos según el diseño UI
            self.lineEdit = self.reproduccion_widget.findChild(QtWidgets.QLineEdit, "lineEdit")  # Buscador general
            self.lineEdit_5 = self.reproduccion_widget.findChild(QtWidgets.QLineEdit, "lineEdit_5")  # Filtro por arete
            self.pushButton = self.reproduccion_widget.findChild(QtWidgets.QPushButton, "pushButton")  # Botón Exportar PDF
            self.tableWidget = self.reproduccion_widget.findChild(QtWidgets.QTableWidget, "tableWidget")  # Tabla principal
            
            # Conectar señales
            if self.lineEdit:
                self.lineEdit.textChanged.connect(self.buscar_registros_reproduccion)
                print("✅ Buscador general conectado")
                
            if self.lineEdit_5:
                self.lineEdit_5.textChanged.connect(self.filtrar_por_arete)
                print("✅ Filtro por arete conectado")
                
            if self.pushButton:
                self.pushButton.clicked.connect(self.exportar_a_pdf)
                print("✅ Botón Exportar PDF conectado")
                
            if self.tableWidget:
                print("✅ TableWidget encontrado")
                self.configurar_tabla()
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla según el diseño"""
        if not self.tableWidget:
            return
            
        try:
            # Configurar tamaños de columnas para la tabla de reproducción
            self.tableWidget.setColumnWidth(0, 80)   # ID
            self.tableWidget.setColumnWidth(1, 100)  # Arete Animal
            self.tableWidget.setColumnWidth(2, 80)   # Cargada
            self.tableWidget.setColumnWidth(3, 80)   # Cant. Partos
            self.tableWidget.setColumnWidth(4, 120)  # Fecha Servicio Actual
            self.tableWidget.setColumnWidth(5, 120)  # Fecha Aprox. Parto
            self.tableWidget.setColumnWidth(6, 120)  # Fecha Nuevo Servicio
            self.tableWidget.setColumnWidth(7, 120)  # Técnica
            self.tableWidget.setColumnWidth(8, 150)  # Observaciones
            
            # Mejorar apariencia
            self.tableWidget.setAlternatingRowColors(True)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.verticalHeader().setVisible(False)
            
            # Conexión para doble clic en observaciones
            self.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)
            
            # Estilo para la tabla
            self.tableWidget.setStyleSheet("""
                QTableWidget {
                    gridline-color: #d0d0d0;
                    background-color: white;
                    alternate-background-color: #f8f8f8;
                    border: 1px solid #d0d0d0;
                    border-radius: 4px;
                }
                QTableWidget::item {
                    padding: 6px;
                    border-bottom: 1px solid #e0e0e0;
                }
                QTableWidget::item:selected {
                    background-color: #e74c3c;
                    color: white;
                }
                QHeaderView::section {
                    background-color: #e74c3c;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                    font-size: 11px;
                }
            """)
            
            print("✅ Tabla de reproducción configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def on_cell_double_clicked(self, row, column):
        """Maneja el doble clic en celdas específicas - SOLO OBSERVACIONES"""
        # Prevenir múltiples aperturas
        if self.dialogo_abierto:
            return
            
        if column == 8:  # Columna de Observaciones (índice 8)
            observacion_item = self.tableWidget.item(row, 8)
            if observacion_item:
                observaciones_completas = observacion_item.data(QtCore.Qt.UserRole)
                if observaciones_completas and observaciones_completas.strip():
                    self.dialogo_abierto = True
                    self.mostrar_observaciones_completas(observaciones_completas)
    
    def cargar_registros_reproduccion(self):
        """Carga todos los registros de reproducción en la tabla"""
        try:
            print("🔄 Cargando registros de reproducción desde la base de datos...")
            
            # Obtener todos los registros de reproducción
            registros = self.obtener_todos_los_registros_reproduccion()
            print(f"📊 {len(registros)} registros de reproducción encontrados")
            
            if len(registros) == 0:
                print("ℹ️ No se encontraron registros de reproducción en la base de datos")
            
            self.llenar_tabla(registros)
        except Exception as e:
            print(f"❌ Error al cargar registros de reproducción: {e}")
            import traceback
            traceback.print_exc()
    
    def obtener_todos_los_registros_reproduccion(self):
        """Obtiene todos los registros de reproducción de la base de datos"""
        try:
            # Obtener registros de la tabla treprod
            registros = self.db.obtener_todos_registros_reproduccion()
            return registros
        except Exception as e:
            print(f"❌ Error obteniendo registros de reproducción: {e}")
            return []
    
    def llenar_tabla(self, registros):
        """Llena la tabla con los datos de los registros de reproducción - CORREGIDO"""
        if not self.tableWidget:
            print("❌ No hay tableWidget disponible")
            return

        try:
            # Limpiar la tabla completamente
            self.tableWidget.setRowCount(0)
            
            print(f"🔄 Llenando tabla con {len(registros)} registros...")

            for row_number, registro in enumerate(registros):
                # Insertar nueva fila
                self.tableWidget.insertRow(row_number)
                
                # Debug: mostrar qué registro se está procesando
                print(f"📝 Procesando registro {row_number}: {registro}")
                
                # ID (0) - idreprod en posición 0
                id_reproduccion = registro[0] if len(registro) > 0 and registro[0] is not None else ""
                id_item = QtWidgets.QTableWidgetItem(str(id_reproduccion))
                self.tableWidget.setItem(row_number, 0, id_item)
                
                # Arete Animal (1) - areteanimal en posición 1
                arete = registro[1] if len(registro) > 1 and registro[1] is not None else ""
                arete_item = QtWidgets.QTableWidgetItem(str(arete))
                self.tableWidget.setItem(row_number, 1, arete_item)
                
                # Cargada (2) - cargada en posición 2
                cargada = registro[2] if len(registro) > 2 and registro[2] is not None else ""
                cargada_item = QtWidgets.QTableWidgetItem(str(cargada))
                self.tableWidget.setItem(row_number, 2, cargada_item)
                
                # Cantidad de Partos (3) - cantpartos en posición 3
                cant_partos = registro[3] if len(registro) > 3 and registro[3] is not None else ""
                cant_partos_item = QtWidgets.QTableWidgetItem(str(cant_partos))
                self.tableWidget.setItem(row_number, 3, cant_partos_item)
                
                # Fecha Servicio Actual (4) - fservicioactual en posición 4
                fecha_servicio = registro[4] if len(registro) > 4 and registro[4] is not None else ""
                fecha_servicio_item = QtWidgets.QTableWidgetItem(str(fecha_servicio))
                self.tableWidget.setItem(row_number, 4, fecha_servicio_item)
                
                # Fecha Aproximada de Parto (5) - faproxparto en posición 5
                fecha_parto = registro[5] if len(registro) > 5 and registro[5] is not None else ""
                fecha_parto_item = QtWidgets.QTableWidgetItem(str(fecha_parto))
                self.tableWidget.setItem(row_number, 5, fecha_parto_item)
                
                # Fecha Nuevo Servicio (6) - fnuevoservicio en posición 6
                fecha_nuevo_servicio = registro[6] if len(registro) > 6 and registro[6] is not None else ""
                fecha_nuevo_servicio_item = QtWidgets.QTableWidgetItem(str(fecha_nuevo_servicio))
                self.tableWidget.setItem(row_number, 6, fecha_nuevo_servicio_item)
                
                # Técnica (7) - tecnica en posición 7
                tecnica = registro[7] if len(registro) > 7 and registro[7] is not None else ""
                tecnica_item = QtWidgets.QTableWidgetItem(str(tecnica))
                self.tableWidget.setItem(row_number, 7, tecnica_item)
                
                # Observaciones (8) - observacion en posición 8 - CORREGIDO
                observacion = registro[8] if len(registro) > 8 and registro[8] is not None else ""
                
                # Manejar correctamente el caso cuando observacion es None o vacío
                if observacion and observacion.strip():
                    observacion_preview = observacion[:50] + "..." if len(observacion) > 50 else observacion
                else:
                    observacion_preview = ""  # Cadena vacía en lugar de None
                    
                observacion_item = QtWidgets.QTableWidgetItem(observacion_preview)
                
                # Guardar observaciones completas para el doble clic
                observacion_item.setData(QtCore.Qt.UserRole, observacion)
                
                # Hacer que la celda sea clickeable solo si hay observaciones
                if observacion and observacion.strip():
                    observacion_item.setForeground(QtGui.QColor('#2980b9'))
                    observacion_item.setToolTip("Doble clic para ver observaciones completas")
                else:
                    observacion_item.setToolTip("Sin observaciones")
                    observacion_item.setForeground(QtGui.QColor('#95a5a6'))
                    
                self.tableWidget.setItem(row_number, 8, observacion_item)

            print(f"✅ Tabla llenada correctamente con {len(registros)} registros de reproducción")
            
            # Debug: verificar cuántas filas tiene la tabla
            print(f"🔍 Tabla tiene {self.tableWidget.rowCount()} filas después de llenar")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_observaciones_completas(self, observaciones):
        """Muestra las observaciones completas en un diálogo - CORREGIDO"""
        try:
            # Verificar si las observaciones son None
            if observaciones is None:
                observaciones = "Sin observaciones"
            
            # Crear el diálogo
            dialog = QtWidgets.QDialog(self.reproduccion_widget)
            dialog.setWindowTitle("Observaciones Completas - Registro de Reproducción")
            dialog.setModal(True)
            dialog.resize(500, 400)
            
            # Conectar el evento de cierre para resetear el flag
            dialog.finished.connect(self.on_dialogo_cerrado)
            
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Título
            titulo = QtWidgets.QLabel("Observaciones del Registro de Reproducción")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #e74c3c;")
            titulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(titulo)
            
            # Área de texto para las observaciones
            text_edit = QtWidgets.QTextEdit()
            text_edit.setPlainText(str(observaciones))  # Aseguramos que sea string
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #f8f9fa;
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                    line-height: 1.4;
                    margin: 10px;
                }
            """)
            layout.addWidget(text_edit)
            
            # Botón cerrar
            btn_cerrar = QtWidgets.QPushButton("Cerrar")
            btn_cerrar.clicked.connect(dialog.accept)
            btn_cerrar.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            layout.addWidget(btn_cerrar)
            
            dialog.exec_()
            
        except Exception as e:
            print(f"❌ Error al mostrar observaciones: {e}")
            self.mostrar_error(f"No se pudieron mostrar las observaciones: {str(e)}")
            # Asegurarse de resetear el flag incluso si hay error
            self.dialogo_abierto = False

    def on_dialogo_cerrado(self):
        """Se llama cuando se cierra un diálogo para resetear el flag"""
        self.dialogo_abierto = False

    def buscar_registros_reproduccion(self):
        """Busca registros de reproducción según el texto en el buscador general, COMBINADO con el filtro de arete actual"""
        try:
            if self.lineEdit:
                texto = self.lineEdit.text().strip()
                arete_actual = self.lineEdit_5.text().strip() if self.lineEdit_5 else ""
                
                print(f"🔍 Buscando registros de reproducción: '{texto}' para arete: '{arete_actual}'")
                
                if arete_actual:
                    # Si hay un arete específico seleccionado, buscar SOLO en los registros de ese arete
                    if texto:
                        registros = self.db.buscar_registros_reproduccion_por_arete_y_texto(arete_actual, texto)
                        print(f"📊 Búsqueda combinada: {len(registros)} registros encontrados para arete '{arete_actual}' con texto '{texto}'")
                    else:
                        # Si no hay texto de búsqueda, mostrar todos los registros del arete
                        registros = self.db.obtener_registros_reproduccion_por_arete(arete_actual)
                        print(f"📊 Mostrando todos los {len(registros)} registros del arete '{arete_actual}'")
                else:
                    # Si no hay arete específico, búsqueda general en todos los registros
                    if texto:
                        registros = self.db.buscar_registros_reproduccion_en_todos_los_campos(texto)
                    else:
                        registros = self.obtener_todos_los_registros_reproduccion()
                        
                self.llenar_tabla(registros)
        except Exception as e:
            print(f"❌ Error al buscar registros de reproducción: {e}")
            import traceback
            traceback.print_exc()

    def filtrar_por_arete(self):
        """Filtra los registros por el arete del animal - MEJORADO"""
        try:
            if self.lineEdit_5:
                arete = self.lineEdit_5.text().strip()
                print(f"🔍 Filtrando por arete: '{arete}'")
                
                # Limpiar el buscador general cuando se filtra por arete
                if self.lineEdit:
                    self.lineEdit.clear()
                    print("🧹 Buscador general limpiado")
                
                if arete:
                    registros = self.db.obtener_registros_reproduccion_por_arete(arete)
                    print(f"📊 {len(registros)} registros encontrados para arete: '{arete}'")
                    
                    if registros:
                        for i, reg in enumerate(registros[:3]):
                            arete_en_registro = reg[1] if len(reg) > 1 and reg[1] is not None else "N/A"
                            print(f"   Registro {i+1} - Arete en BD: '{arete_en_registro}'")
                    else:
                        print(f"⚠️ No se encontraron registros para el arete: '{arete}'")
                        
                    self.llenar_tabla(registros)
                else:
                    # Si no hay arete, mostrar todos los registros
                    registros = self.obtener_todos_los_registros_reproduccion()
                    self.llenar_tabla(registros)
                    
        except Exception as e:
            print(f"❌ Error al filtrar por arete: {e}")
            import traceback
            traceback.print_exc()

    def exportar_a_pdf(self):
        """Exporta los registros actuales a PDF"""
        try:
            print("📄 Exportando registros de reproducción a PDF...")
            
            # Obtener los registros actualmente mostrados
            row_count = self.tableWidget.rowCount()
            if row_count == 0:
                self.mostrar_informacion("No hay datos para exportar")
                return
            
            # Crear nombre de archivo con fecha
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_reproduccion_{fecha_actual}.pdf"
            ruta_completa = os.path.join(tempfile.gettempdir(), nombre_archivo)
            
            try:
                # Intentar importar reportlab
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                
                # Crear el documento PDF
                doc = SimpleDocTemplate(ruta_completa, pagesize=A4)
                elementos = []
                
                # Estilos
                estilos = getSampleStyleSheet()
                estilo_titulo = estilos['Heading1']
                estilo_normal = estilos['Normal']
                
                # Título
                titulo = Paragraph("Reporte de Reproducción", estilo_titulo)
                elementos.append(titulo)
                elementos.append(Spacer(1, 12))
                
                # Información del reporte
                fecha_reporte = Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_normal)
                elementos.append(fecha_reporte)
                
                arete_filtro = self.lineEdit_5.text().strip()
                if arete_filtro:
                    filtro_texto = Paragraph(f"Filtrado por arete: {arete_filtro}", estilo_normal)
                    elementos.append(filtro_texto)
                
                elementos.append(Spacer(1, 20))
                
                # Preparar datos de la tabla
                datos = []
                
                # Encabezados
                encabezados = []
                for col in range(self.tableWidget.columnCount()):
                    encabezados.append(self.tableWidget.horizontalHeaderItem(col).text())
                datos.append(encabezados)
                
                # Datos de las filas
                for row in range(row_count):
                    fila = []
                    for col in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, col)
                        if item is not None:
                            texto = item.text()
                            # Acortar observaciones largas para el PDF
                            if col == 8 and len(texto) > 50:  # Observaciones en columna 8
                                texto = texto[:50] + "..."
                            fila.append(texto)
                        else:
                            fila.append("")
                    datos.append(fila)
                
                # Crear tabla en PDF
                tabla = Table(datos)
                estilo_tabla = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 7),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
                ])
                
                # Aplicar estilo a la tabla
                tabla.setStyle(estilo_tabla)
                elementos.append(tabla)
                
                # Generar PDF
                doc.build(elementos)
                
                self.mostrar_informacion(
                    f"✅ Reporte exportado exitosamente\n\n"
                    f"Archivo: {nombre_archivo}\n"
                    f"Ubicación: {ruta_completa}\n\n"
                    f"Total de registros: {row_count}"
                )
                
                print(f"✅ PDF exportado correctamente: {ruta_completa}")
                
            except ImportError:
                self.mostrar_error(
                    "La biblioteca 'reportlab' no está instalada.\n\n"
                    "Para exportar a PDF, instálela con:\n"
                    "pip install reportlab"
                )
                print("❌ reportlab no está instalado")
            
        except Exception as e:
            print(f"❌ Error exportando a PDF: {e}")
            self.mostrar_error(f"Error al exportar a PDF: {str(e)}")

    def actualizar_tabla(self):
        """Fuerza la actualización de la tabla"""
        print("🔄 Forzando actualización de tabla de reproducción...")
        self.cargar_registros_reproduccion()

    def cargar_datos(self):
        """Método para cargar datos cuando se opens la página"""
        print("🐄 Cargando página de reproducción...")
        self.cargar_registros_reproduccion()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Reproducción...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()

    # Método para integración con RbuscarController
    def mostrar_registros_por_arete(self, arete):
        """Método público para que RbuscarController pueda mostrar registros específicos - MEJORADO"""
        try:
            print(f"🐄 Mostrando registros de reproducción para arete: {arete}")
            
            # Actualizar el campo de arete
            if self.lineEdit_5:
                self.lineEdit_5.setText(arete)
            
            # Limpiar el buscador general
            if self.lineEdit:
                self.lineEdit.clear()
                print("🧹 Buscador general limpiado al mostrar registros por arete")
            
            # Filtrar por arete
            self.filtrar_por_arete()
            
        except Exception as e:
            print(f"❌ Error mostrando registros por arete: {e}")

    # Métodos auxiliares para mostrar mensajes
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.reproduccion_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def mostrar_informacion(self, mensaje):
        """Muestra un mensaje informativo"""
        try:
            QtWidgets.QMessageBox.information(
                self.reproduccion_widget,
                "Información",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje informativo: {e}")