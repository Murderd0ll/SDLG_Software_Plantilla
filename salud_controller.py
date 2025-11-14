# salud_controller.py - VERSIÓN CORREGIDA
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from datetime import datetime
import os
import tempfile

class SaludController:
    def __init__(self, salud_widget):
        self.salud_widget = salud_widget
        self.db = Database()
        self.setup_connections()
        self.configurar_tabla()
        self.configurar_fechas()
        print("✅ SaludController inicializado")
        
        # Variable para controlar diálogos abiertos
        self.dialogo_abierto = False
        
        # Cargar datos automáticamente al iniciar
        self.cargar_registros_salud()
        
    def setup_connections(self):
        """Configura las conexiones de los elementos UI según el diseño"""
        try:
            print("🔍 Configurando conexiones para Salud...")
            
            # Buscar elementos según el diseño UI
            self.lineEdit = self.salud_widget.findChild(QtWidgets.QLineEdit, "lineEdit")  # Buscador general
            self.lineEdit_5 = self.salud_widget.findChild(QtWidgets.QLineEdit, "lineEdit_5")  # Filtro por arete
            self.dateEdit = self.salud_widget.findChild(QtWidgets.QDateEdit, "dateEdit")  # Fecha inicio
            self.dateEdit_2 = self.salud_widget.findChild(QtWidgets.QDateEdit, "dateEdit_2")  # Fecha fin
            self.pushButton = self.salud_widget.findChild(QtWidgets.QPushButton, "pushButton")  # Botón Exportar PDF
            self.tableWidget = self.salud_widget.findChild(QtWidgets.QTableWidget, "tableWidget")  # Tabla principal
            
            # Conectar señales
            if self.lineEdit:
                self.lineEdit.textChanged.connect(self.buscar_registros_salud)
                print("✅ Buscador general conectado")
                
            if self.lineEdit_5:
                self.lineEdit_5.textChanged.connect(self.filtrar_por_arete)
                print("✅ Filtro por arete conectado")
                
            if self.dateEdit and self.dateEdit_2:
                self.dateEdit.dateChanged.connect(self.filtrar_por_fecha)
                self.dateEdit_2.dateChanged.connect(self.filtrar_por_fecha)
                print("✅ Filtros por fecha conectados")
                
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
    
    def configurar_fechas(self):
        """Configura los dateEdit con fechas por defecto"""
        try:
            if self.dateEdit and self.dateEdit_2:
                # Fecha inicio: hace 30 días
                fecha_inicio = QtCore.QDate.currentDate().addDays(-30)
                self.dateEdit.setDate(fecha_inicio)
                
                # Fecha fin: hoy
                fecha_fin = QtCore.QDate.currentDate()
                self.dateEdit_2.setDate(fecha_fin)
                
                print("✅ Fechas configuradas correctamente")
        except Exception as e:
            print(f"❌ Error configurando fechas: {e}")
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla según el diseño"""
        if not self.tableWidget:
            return
            
        try:
            # Configurar tamaños de columnas según el diseño UI
            self.tableWidget.setColumnWidth(0, 120)  # Fecha de revisión
            self.tableWidget.setColumnWidth(1, 120)  # Veterinario
            self.tableWidget.setColumnWidth(2, 150)  # Condición de salud
            self.tableWidget.setColumnWidth(3, 150)  # Procedimiento
            self.tableWidget.setColumnWidth(4, 150)  # Medicina preventiva
            self.tableWidget.setColumnWidth(5, 120)  # Manejo
            self.tableWidget.setColumnWidth(6, 200)  # Observaciones
            self.tableWidget.setColumnWidth(7, 150)  # Imagen del procedimiento
            
            # Mejorar apariencia
            self.tableWidget.setAlternatingRowColors(True)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.verticalHeader().setVisible(False)
            
            # Conexión para doble clic en observaciones - SOLO UNA VEZ
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
            
            print("✅ Tabla de salud configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def on_cell_double_clicked(self, row, column):
        """Maneja el doble clic en celdas específicas - SOLO OBSERVACIONES - CORREGIDO"""
        # Prevenir múltiples aperturas
        if self.dialogo_abierto:
            return
            
        if column == 6:  # Columna de Observaciones
            observacion_item = self.tableWidget.item(row, 6)
            if observacion_item:
                observaciones_completas = observacion_item.data(QtCore.Qt.UserRole)
                if observaciones_completas and observaciones_completas.strip():
                    self.dialogo_abierto = True
                    self.mostrar_observaciones_completas(observaciones_completas)
                    # El flag se reseteará cuando se cierre el diálogo
    
    def cargar_registros_salud(self):
        """Carga todos los registros de salud en la tabla"""
        try:
            print("🔄 Cargando registros de salud desde la base de datos...")
            
            # Obtener todos los registros de salud
            registros = self.obtener_todos_los_registros_salud()
            print(f"📊 {len(registros)} registros de salud encontrados")
            
            if len(registros) == 0:
                print("ℹ️ No se encontraron registros de salud en la base de datos")
            
            self.llenar_tabla(registros)
        except Exception as e:
            print(f"❌ Error al cargar registros de salud: {e}")
            import traceback
            traceback.print_exc()
    
    def obtener_todos_los_registros_salud(self):
        """Obtiene todos los registros de salud de la base de datos"""
        try:
            # Verificar si la tabla existe primero
            tablas = self.db.listar_tablas()
            if 'tsalud' not in tablas:
                print("❌ La tabla 'tsalud' no existe en la base de datos")
                return []
                
            registros = self.db.obtener_todos_registros_salud()
            return registros
        except Exception as e:
            print(f"❌ Error obteniendo registros de salud: {e}")
            return []
    
    def llenar_tabla(self, registros):
        """Llena la tabla con los datos de los registros de salud"""
        if not self.tableWidget:
            print("❌ No hay tableWidget disponible")
            return

        try:
            self.tableWidget.setRowCount(0)

            for row_number, registro in enumerate(registros):
                self.tableWidget.insertRow(row_number)
                
                # Fecha de revisión (0) - fecharev en posición 7
                fecha_revision = registro[7] if len(registro) > 7 else ""
                fecha_item = QtWidgets.QTableWidgetItem(str(fecha_revision if fecha_revision else ""))
                self.tableWidget.setItem(row_number, 0, fecha_item)
                
                # Veterinario (1) - nomvet en posición 3
                veterinario = registro[3] if len(registro) > 3 else ""
                veterinario_item = QtWidgets.QTableWidgetItem(str(veterinario if veterinario else ""))
                self.tableWidget.setItem(row_number, 1, veterinario_item)
                
                # Condición de salud (2) - condicionsalud en posición 6
                condicion = registro[6] if len(registro) > 6 else ""
                condicion_item = QtWidgets.QTableWidgetItem(str(condicion if condicion else ""))
                self.tableWidget.setItem(row_number, 2, condicion_item)
                
                # Procedimiento (3) - procedimiento en posición 4
                procedimiento = registro[4] if len(registro) > 4 else ""
                procedimiento_item = QtWidgets.QTableWidgetItem(str(procedimiento if procedimiento else ""))
                self.tableWidget.setItem(row_number, 3, procedimiento_item)
                
                # Medicina preventiva (4) - medprev en posición 5
                medicina = registro[5] if len(registro) > 5 else ""
                medicina_item = QtWidgets.QTableWidgetItem(str(medicina if medicina else ""))
                self.tableWidget.setItem(row_number, 4, medicina_item)
                
                # Manejo (5) - tipoanimal en posición 2
                manejo = registro[2] if len(registro) > 2 else ""
                manejo_item = QtWidgets.QTableWidgetItem(str(manejo if manejo else ""))
                self.tableWidget.setItem(row_number, 5, manejo_item)
                
                # Observaciones (6) - observacionsalud en posición 8
                observacion = registro[8] if len(registro) > 8 else ""
                observacion_preview = observacion[:50] + "..." if len(observacion) > 50 else observacion
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
                    
                self.tableWidget.setItem(row_number, 6, observacion_item)
                
                # Imagen del procedimiento (7) - archivo en posición 9
                self.agregar_boton_imagen(row_number, 7, registro)

            print(f"✅ Tabla llenada con {len(registros)} registros de salud")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
            import traceback
            traceback.print_exc()

    def agregar_boton_imagen(self, row, column, registro):
        """Agrega un botón para ver la imagen del procedimiento"""
        try:
            btn_imagen = QtWidgets.QPushButton("🖼️ Ver")
            btn_imagen.setToolTip("Ver imagen del procedimiento")
            btn_imagen.setStyleSheet("""
                QPushButton { 
                    background-color: #3498db; 
                    color: white; 
                    border: none; 
                    padding: 4px 8px; 
                    border-radius: 3px;
                    font-size: 10px;
                    min-width: 50px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:disabled {
                    background-color: #bdc3c7;
                    color: #7f8c8d;
                }
            """)
            
            # Verificar si hay imagen disponible (archivo en posición 9)
            tiene_imagen = len(registro) > 9 and registro[9] is not None
            if not tiene_imagen:
                btn_imagen.setText("📷 No")
                btn_imagen.setEnabled(False)
            else:
                btn_imagen.clicked.connect(lambda checked, r=registro: self.mostrar_imagen_procedimiento(r))
            
            self.tableWidget.setCellWidget(row, column, btn_imagen)
            
        except Exception as e:
            print(f"❌ Error al agregar botón de imagen: {e}")

    def mostrar_imagen_procedimiento(self, registro):
        """Muestra la imagen del procedimiento en tamaño completo"""
        try:
            # Obtener datos de la imagen (archivo en posición 9)
            archivo_data = registro[9] if len(registro) > 9 else None
            
            if archivo_data:
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(archivo_data):
                    # Mostrar en un diálogo
                    dialog = QtWidgets.QDialog(self.salud_widget)
                    dialog.setWindowTitle("Imagen del Procedimiento")
                    dialog.setModal(True)
                    dialog.resize(600, 500)
                    
                    layout = QtWidgets.QVBoxLayout(dialog)
                    
                    # Información del procedimiento
                    info_text = f"Procedimiento: {registro[4]}\nFecha: {registro[7]}"
                    label_info = QtWidgets.QLabel(info_text)
                    label_info.setAlignment(QtCore.Qt.AlignCenter)
                    label_info.setStyleSheet("font-weight: bold; margin: 10px; font-size: 14px;")
                    layout.addWidget(label_info)
                    
                    # Label para la imagen
                    label_imagen = QtWidgets.QLabel()
                    label_imagen.setAlignment(QtCore.Qt.AlignCenter)
                    label_imagen.setPixmap(pixmap.scaled(500, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                    
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
                    
                    layout.addWidget(label_imagen)
                    layout.addWidget(btn_cerrar)
                    
                    dialog.exec_()
                else:
                    self.mostrar_error("No se pudo cargar la imagen del procedimiento")
            else:
                self.mostrar_informacion("No hay imagen disponible para este procedimiento")
                    
        except Exception as e:
            print(f"❌ Error al mostrar imagen: {e}")
            self.mostrar_error(f"No se pudo cargar la imagen: {str(e)}")

    def mostrar_observaciones_completas(self, observaciones):
        """Muestra las observaciones completas en un diálogo - CORREGIDO PARA EVITAR DOBLE APERTURA"""
        try:
            # Crear el diálogo
            dialog = QtWidgets.QDialog(self.salud_widget)
            dialog.setWindowTitle("Observaciones Completas - Registro de Salud")
            dialog.setModal(True)
            dialog.resize(500, 400)
            
            # Conectar el evento de cierre para resetear el flag
            dialog.finished.connect(self.on_dialogo_cerrado)
            
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Título
            titulo = QtWidgets.QLabel("Observaciones del Registro de Salud")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #e74c3c;")
            titulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(titulo)
            
            # Área de texto para las observaciones
            text_edit = QtWidgets.QTextEdit()
            text_edit.setPlainText(observaciones)
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

    def buscar_registros_salud(self):
        """Busca registros de salud según el texto en el buscador general"""
        try:
            if self.lineEdit:
                texto = self.lineEdit.text().strip()
                if texto:
                    print(f"🔍 Buscando registros de salud: '{texto}'")
                    registros = self.buscar_en_base_datos(texto)
                else:
                    registros = self.obtener_todos_los_registros_salud()
                self.llenar_tabla(registros)
        except Exception as e:
            print(f"❌ Error al buscar registros de salud: {e}")

    def filtrar_por_arete(self):
        """Filtra los registros por el arete del animal - CORREGIDO"""
        try:
            if self.lineEdit_5:
                arete = self.lineEdit_5.text().strip()
                print(f"🔍 Filtrando por arete: '{arete}'")
                
                if arete:
                    registros = self.db.obtener_registros_salud_por_arete(arete)
                    print(f"📊 {len(registros)} registros encontrados para arete: '{arete}'")
                    
                    # Debug: mostrar qué aretes se están mostrando
                    if registros:
                        for i, reg in enumerate(registros[:3]):
                            arete_en_registro = reg[1] if len(reg) > 1 else "N/A"
                            print(f"   Registro {i+1} - Arete en BD: '{arete_en_registro}'")
                else:
                    registros = self.obtener_todos_los_registros_salud()
                    
                self.llenar_tabla(registros)
        except Exception as e:
            print(f"❌ Error al filtrar por arete: {e}")

    def filtrar_por_fecha(self):
        """Filtra los registros por rango de fechas"""
        try:
            if self.dateEdit and self.dateEdit_2:
                fecha_inicio = self.dateEdit.date().toString("yyyy-MM-dd")
                fecha_fin = self.dateEdit_2.date().toString("yyyy-MM-dd")
                
                print(f"📅 Filtrando por fecha: {fecha_inicio} a {fecha_fin}")
                
                # Obtener registros filtrados por fecha
                registros = self.db.obtener_registros_salud_por_fecha(fecha_inicio, fecha_fin)
                print(f"📊 {len(registros)} registros encontrados en el rango de fechas")
                
                self.llenar_tabla(registros)
                
        except Exception as e:
            print(f"❌ Error al filtrar por fecha: {e}")

    def buscar_en_base_datos(self, texto):
        """Busca registros en la base de datos por texto"""
        try:
            registros = self.db.buscar_registros_salud(texto)
            return registros
        except Exception as e:
            print(f"❌ Error en búsqueda de base de datos: {e}")
            return []

    def exportar_a_pdf(self):
        """Exporta los registros actuales a PDF - IMPLEMENTADO"""
        try:
            print("📄 Exportando registros de salud a PDF...")
            
            # Obtener los registros actualmente mostrados
            row_count = self.tableWidget.rowCount()
            if row_count == 0:
                self.mostrar_informacion("No hay datos para exportar")
                return
            
            # Crear nombre de archivo con fecha
            from datetime import datetime
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_salud_{fecha_actual}.pdf"
            ruta_completa = os.path.join(tempfile.gettempdir(), nombre_archivo)
            
            try:
                # Intentar importar reportlab
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                from reportlab.pdfgen import canvas
                
                # Crear el documento PDF
                doc = SimpleDocTemplate(ruta_completa, pagesize=A4)
                elementos = []
                
                # Estilos
                estilos = getSampleStyleSheet()
                estilo_titulo = estilos['Heading1']
                estilo_normal = estilos['Normal']
                
                # Título
                titulo = Paragraph("Reporte de Salud Animal", estilo_titulo)
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
                            if col == 6 and len(texto) > 100:
                                texto = texto[:100] + "..."
                            fila.append(texto)
                        else:
                            widget = self.tableWidget.cellWidget(row, col)
                            if widget and isinstance(widget, QtWidgets.QPushButton):
                                fila.append(widget.text())
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
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
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
        print("🔄 Forzando actualización de tabla de salud...")
        self.cargar_registros_salud()

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("🏥 Cargando página de salud...")
        self.cargar_registros_salud()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Salud...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()

    # Método para integración con SbuscarController
    def mostrar_registros_por_arete(self, arete):
        """Método público para que SbuscarController pueda mostrar registros específicos"""
        try:
            print(f"🏥 Mostrando registros de salud para arete: {arete}")
            
            # Actualizar el campo de arete
            if self.lineEdit_5:
                self.lineEdit_5.setText(arete)
            
            # Filtrar por arete
            self.filtrar_por_arete()
            
        except Exception as e:
            print(f"❌ Error mostrando registros por arete: {e}")

    # Métodos auxiliares para mostrar mensajes
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.salud_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def mostrar_informacion(self, mensaje):
        """Muestra un mensaje informativo"""
        try:
            QtWidgets.QMessageBox.information(
                self.salud_widget,
                "Información",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje informativo: {e}")