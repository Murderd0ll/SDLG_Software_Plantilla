from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from agregar_becerro_controller import AgregarBecerroController
from salud_becerro_controller import SaludBecerroController

class BecerrosController:
    def __init__(self, becerros_widget):
        self.becerros_widget = becerros_widget
        self.db = Database()
        self.setup_connections()
        self.configurar_tabla()
        print("✅ BecerrosController inicializado con widget directo")
        
        # ✅ LINEA NUEVA: Cargar datos automáticamente al iniciar
        self.cargar_becerros()
        
    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Buscando elementos UI...")
            
            # Listar todos los widgets hijos para debug
            hijos = self.becerros_widget.findChildren(QtWidgets.QWidget)
            print(f"📋 Widgets hijos encontrados: {len(hijos)}")
            for hijo in hijos:
                if hasattr(hijo, 'objectName') and hijo.objectName():
                    print(f"   - {hijo.objectName()}: {type(hijo).__name__}")
            
            # Buscar elementos específicos
            self.indexbtn2 = self.becerros_widget.findChild(QtWidgets.QPushButton, "indexbtn2")
            if self.indexbtn2:
                self.indexbtn2.clicked.connect(self.agregar_becerro)
                print("✅ Botón agregar conectado")
            else:
                print("❌ NO SE ENCONTRÓ indexbtn2")
                
            # Buscar lineEdit para búsqueda
            self.lineEdit = self.becerros_widget.findChild(QtWidgets.QLineEdit, "lineEdit")
            if self.lineEdit:
                self.lineEdit.textChanged.connect(self.buscar_becerros)
                print("✅ Buscador conectado")
            else:
                print("❌ NO SE ENCONTRÓ lineEdit")
                
            # Buscar tableWidget
            self.tableWidget = self.becerros_widget.findChild(QtWidgets.QTableWidget, "tableWidget")
            if self.tableWidget:
                print("✅ TableWidget encontrado")
                self.configurar_tabla()
            else:
                print("❌ NO SE ENCONTRÓ tableWidget - Esto es crítico!")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla"""
        if not self.tableWidget:
            return
            
        try:
            # ✅ COLUMNAS REORGANIZADAS - FOTO PRIMERO + OBSERVACIONES
            columnas = [
                "ID", "Foto", "Arete", "Nombre", "Peso", "Sexo", "Raza", 
                "Fecha Nac.", "Corral", "Estatus", "Madre", "Observaciones", "Opciones"
            ]
            
            self.tableWidget.setColumnCount(len(columnas))
            self.tableWidget.setHorizontalHeaderLabels(columnas)
            
            # ✅ TAMAÑOS DE COLUMNAS REORGANIZADOS CON OBSERVACIONES
            self.tableWidget.setColumnWidth(0, 40)    # ID
            self.tableWidget.setColumnWidth(1, 80)    # Foto (PRIMERA COLUMNA VISIBLE)
            self.tableWidget.setColumnWidth(2, 80)    # Arete
            self.tableWidget.setColumnWidth(3, 120)   # Nombre
            self.tableWidget.setColumnWidth(4, 60)    # Peso
            self.tableWidget.setColumnWidth(5, 60)    # Sexo
            self.tableWidget.setColumnWidth(6, 100)   # Raza
            self.tableWidget.setColumnWidth(7, 100)   # Fecha Nac.
            self.tableWidget.setColumnWidth(8, 80)    # Corral
            self.tableWidget.setColumnWidth(9, 80)    # Estatus
            self.tableWidget.setColumnWidth(10, 100)  # Madre
            self.tableWidget.setColumnWidth(11, 150)  # Observaciones (más ancha ahora)
            self.tableWidget.setColumnWidth(12, 150)  # Opciones (más angosta para 3 botones)
            
            # Configurar altura de filas para las fotos
            self.tableWidget.verticalHeader().setDefaultSectionSize(80)
            
            # Mejorar apariencia
            self.tableWidget.setAlternatingRowColors(True)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.verticalHeader().setVisible(False)
            
            # ✅ CONEXIÓN NUEVA: Doble clic en celdas - SOLO PARA OBSERVACIONES
            self.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)
            
            # Estilo para la tabla
            self.tableWidget.setStyleSheet("""
                QTableWidget {
                    gridline-color: #d0d0d0;
                    background-color: white;
                    alternate-background-color: #f8f8f8;
                }
                QTableWidget::item {
                    padding: 5px;
                    border-bottom: 1px solid #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #3498db;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }
            """)
            
            print("✅ Tabla configurada correctamente - FOTO PRIMERO + OBSERVACIONES CLICKEABLES + SALUD")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def on_cell_double_clicked(self, row, column):
        """Maneja el doble clic en celdas específicas - SOLO OBSERVACIONES"""
        # ✅ SOLO responder a doble clic en columna de Observaciones (11)
        if column == 11:  
            arete_item = self.tableWidget.item(row, 2)  # Columna Arete
            observacion_item = self.tableWidget.item(row, 11)  # Columna Observaciones
            
            if arete_item and observacion_item:
                arete = arete_item.text()
                observaciones = observacion_item.data(QtCore.Qt.UserRole)  # Datos completos
                
                # ✅ VERIFICAR que hay observaciones antes de abrir el diálogo
                if observaciones and observaciones.strip():
                    print(f"🖱️ Doble clic en observaciones para arete: {arete}")
                    self.mostrar_observaciones_completas(arete, observaciones)
                else:
                    print("ℹ️ No hay observaciones para mostrar")
        
    def cargar_becerros(self):
        """Carga todos los becerros en la tabla"""
        try:
            print("🔄 Cargando becerros desde la base de datos...")
            
            # ✅ DIAGNÓSTICO MEJORADO: Verificar estado de la BD
            print("🔍 Realizando diagnóstico de BD...")
            self.db.diagnostico_completo()
            
            becerros = self.db.obtener_becerros()
            print(f"📊 {len(becerros)} becerros encontrados en el controlador")
            
            if len(becerros) == 0:
                print("⚠️ ADVERTENCIA: No se encontraron becerros en la base de datos")
                # Mostrar mensaje en la interfaz
                QtWidgets.QMessageBox.information(
                    self.becerros_widget, 
                    "Información", 
                    "No se encontraron becerros en la base de datos."
                )
            
            self.llenar_tabla(becerros)
        except Exception as e:
            print(f"❌ Error al cargar becerros: {e}")
            import traceback
            traceback.print_exc()
    
    def llenar_tabla(self, becerros):
        """Llena la tabla con los datos de los becerros"""
        if not self.tableWidget:
            print("❌ No hay tableWidget disponible")
            return

        try:
            self.tableWidget.setRowCount(0)

            for row_number, becerro in enumerate(becerros):
                self.tableWidget.insertRow(row_number)
                self.tableWidget.setRowHeight(row_number, 80)  # Altura mayor para las fotos
                
                # ID (oculto pero necesario para operaciones)
                id_item = QtWidgets.QTableWidgetItem(str(becerro[0] if becerro[0] is not None else ""))
                self.tableWidget.setItem(row_number, 0, id_item)
                
                # ✅ FOTO AHORA EN COLUMNA 1 (SEGUNDA COLUMNA, PERO PRIMERA VISIBLE)
                arete = str(becerro[1] if becerro[1] else "")
                self.mostrar_foto_en_tabla(row_number, 1, arete)
                
                # Arete (2)
                arete_item = QtWidgets.QTableWidgetItem(arete)
                self.tableWidget.setItem(row_number, 2, arete_item)
                
                # Nombre (3)
                nombre_item = QtWidgets.QTableWidgetItem(str(becerro[2] if becerro[2] else ""))
                self.tableWidget.setItem(row_number, 3, nombre_item)
                
                # Peso (4)
                peso_item = QtWidgets.QTableWidgetItem(str(becerro[3] if becerro[3] else ""))
                self.tableWidget.setItem(row_number, 4, peso_item)
                
                # Sexo (5)
                sexo_item = QtWidgets.QTableWidgetItem(str(becerro[4] if becerro[4] else ""))
                self.tableWidget.setItem(row_number, 5, sexo_item)
                
                # Raza (6)
                raza_item = QtWidgets.QTableWidgetItem(str(becerro[5] if becerro[5] else ""))
                self.tableWidget.setItem(row_number, 6, raza_item)
                
                # Fecha Nacimiento (7)
                fecha_item = QtWidgets.QTableWidgetItem(str(becerro[6] if becerro[6] else ""))
                self.tableWidget.setItem(row_number, 7, fecha_item)
                
                # Corral (8)
                corral_item = QtWidgets.QTableWidgetItem(str(becerro[7] if becerro[7] else ""))
                self.tableWidget.setItem(row_number, 8, corral_item)
                
                # Estatus (9)
                estatus_item = QtWidgets.QTableWidgetItem(str(becerro[8] if becerro[8] else ""))
                self.tableWidget.setItem(row_number, 9, estatus_item)
                
                # Arete Madre (10)
                madre_item = QtWidgets.QTableWidgetItem(str(becerro[9] if becerro[9] else ""))
                self.tableWidget.setItem(row_number, 10, madre_item)
                
                # ✅ OBSERVACIONES EN COLUMNA 11 - AHORA CLICKEABLE
                observacion = str(becerro[11] if len(becerro) > 11 and becerro[11] is not None else "")
                # Mostrar solo preview en la tabla
                observacion_preview = observacion[:30] + "..." if len(observacion) > 30 else observacion
                observacion_item = QtWidgets.QTableWidgetItem(observacion_preview)
                
                # ✅ GUARDAR OBSERVACIONES COMPLETAS para el doble clic
                observacion_item.setData(QtCore.Qt.UserRole, observacion)
                
                # ✅ HACER QUE LA CELDA SEA CLICKEABLE SOLO SI HAY OBSERVACIONES
                if observacion and observacion.strip():
                    observacion_item.setForeground(QtGui.QColor('#2980b9'))  # Color azul para indicar clickeable
                    observacion_item.setToolTip("Doble clic para ver observaciones completas")
                    # Hacer que se vea como un enlace
                    observacion_item.setFlags(observacion_item.flags() | QtCore.Qt.ItemIsEnabled)
                else:
                    observacion_item.setToolTip("Sin observaciones")
                    observacion_item.setForeground(QtGui.QColor('#95a5a6'))  # Color gris para indicar vacío
                    
                self.tableWidget.setItem(row_number, 11, observacion_item)
                
                # ✅ OPCIONES AHORA EN COLUMNA 12 CON SOLO 3 BOTONES (SIN OBSERVACIONES)
                self.agregar_botones_opciones(row_number, 12, arete)

            # Ocultar columna ID
            self.tableWidget.setColumnHidden(0, True)
            
            print(f"✅ Tabla llenada con {len(becerros)} registros - OBSERVACIONES SOLO CON DOBLE CLIC")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_foto_en_tabla(self, row, column, arete_becerro):
        """Muestra la foto en pequeño directamente en la tabla usando el arete"""
        try:
            print(f"📸 Intentando mostrar foto para becerro arete: {arete_becerro}")
            foto_data = self.db.obtener_foto_becerro_por_arete(arete_becerro)
            
            if foto_data:
                print(f"✅ Foto encontrada en BD - Tamaño: {len(foto_data)} bytes")
                
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(foto_data):
                    print("✅ Pixmap cargado correctamente desde datos BLOB")
                    
                    # Escalar la imagen a un tamaño pequeño para la tabla (60x60)
                    pixmap_escalado = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    
                    # Crear un QLabel para mostrar la imagen
                    label_foto = QtWidgets.QLabel()
                    label_foto.setPixmap(pixmap_escalado)
                    label_foto.setAlignment(QtCore.Qt.AlignCenter)
                    label_foto.setToolTip("Haz clic para ver la foto en tamaño completo")
                    label_foto.setCursor(QtCore.Qt.PointingHandCursor)
                    label_foto.setStyleSheet("""
                        border: 2px solid #bdc3c7; 
                        background-color: #ecf0f1;
                        border-radius: 5px;
                        padding: 2px;
                    """)
                    
                    # Hacer que el label sea clickeable
                    label_foto.mousePressEvent = lambda event, arete=arete_becerro: self.mostrar_foto_completa_por_arete(arete)
                    
                    self.tableWidget.setCellWidget(row, column, label_foto)
                    print(f"✅ Miniatura de foto mostrada en tabla para arete: {arete_becerro}")
                else:
                    print("❌ No se pudo cargar el pixmap desde los datos BLOB")
                    # Si no se puede cargar la foto, mostrar un placeholder
                    self.mostrar_placeholder_foto_por_arete(row, column, arete_becerro, "❌ Error carga")
            else:
                print(f"❌ No hay datos de foto para becerro arete: {arete_becerro}")
                # Si no hay foto, mostrar un placeholder
                self.mostrar_placeholder_foto_por_arete(row, column, arete_becerro, "📷 Sin foto")
                
        except Exception as e:
            print(f"❌ Error al mostrar foto en tabla: {e}")
            self.mostrar_placeholder_foto_por_arete(row, column, arete_becerro, f"❌ Error: {str(e)}")

    def mostrar_placeholder_foto_por_arete(self, row, column, arete_becerro, motivo="Sin foto"):
        """Muestra un placeholder cuando no hay foto o hay error (usando arete)"""
        try:
            label_placeholder = QtWidgets.QLabel("📷")
            label_placeholder.setAlignment(QtCore.Qt.AlignCenter)
            label_placeholder.setStyleSheet("""
                font-size: 24px; 
                color: #95a5a6; 
                border: 2px dashed #bdc3c7; 
                background-color: #ecf0f1;
                padding: 10px;
                border-radius: 5px;
            """)
            label_placeholder.setToolTip(f"{motivo} - Haz clic para más información")
            label_placeholder.setCursor(QtCore.Qt.PointingHandCursor)
            
            # Hacer clickeable para mostrar información de debug
            label_placeholder.mousePressEvent = lambda event, arete=arete_becerro, msg=motivo: self.mostrar_info_foto_por_arete(arete, msg)
            
            self.tableWidget.setCellWidget(row, column, label_placeholder)
            
        except Exception as e:
            print(f"❌ Error al mostrar placeholder: {e}")

    def mostrar_info_foto_por_arete(self, arete_becerro, mensaje):
        """Muestra información de debug sobre la foto usando arete"""
        try:
            # Obtener información actualizada de la foto
            foto_data = self.db.obtener_foto_becerro_por_arete(arete_becerro)
            info_becerro = self.db.obtener_becerro_por_arete(arete_becerro)
            
            mensaje_detallado = f"""
            Información de foto - Becerro Arete: {arete_becerro}
            
            Estado: {mensaje}
            Datos en BD: {'Sí' if foto_data else 'No'}
            Tamaño datos: {len(foto_data) if foto_data else 0} bytes
            Arete: {arete_becerro}
            Nombre: {info_becerro[2] if info_becerro else 'N/A'}
            ID en BD: {info_becerro[0] if info_becerro else 'N/A'}
            """
            
            QtWidgets.QMessageBox.information(
                self.becerros_widget,
                "Información de Foto",
                mensaje_detallado
            )
            
        except Exception as e:
            print(f"❌ Error al mostrar info foto: {e}")

    def mostrar_foto_completa_por_arete(self, arete_becerro):
        """Muestra la foto en tamaño completo al hacer clic en la miniatura (usando arete)"""
        try:
            print(f"📷 Solicitando foto completa para becerro arete: {arete_becerro}")
            foto_data = self.db.obtener_foto_becerro_por_arete(arete_becerro)
            
            if foto_data:
                print(f"✅ Foto encontrada - Tamaño: {len(foto_data)} bytes")
                
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(foto_data):
                    print("✅ Pixmap cargado para vista completa")
                    
                    # Mostrar en un diálogo
                    dialog = QtWidgets.QDialog(self.becerros_widget)
                    dialog.setWindowTitle("Foto del Becerro - Vista Completa")
                    dialog.setModal(True)
                    dialog.resize(600, 600)
                    
                    layout = QtWidgets.QVBoxLayout(dialog)
                    
                    # Información del becerro
                    becerro = self.db.obtener_becerro_por_arete(arete_becerro)
                    if becerro:
                        info_text = f"Arete: {becerro[1]} | Nombre: {becerro[2]} | ID: {becerro[0]}"
                        label_info = QtWidgets.QLabel(info_text)
                        label_info.setAlignment(QtCore.Qt.AlignCenter)
                        label_info.setStyleSheet("font-weight: bold; margin: 10px; font-size: 14px;")
                        layout.addWidget(label_info)
                
                    # Label para la foto
                    label_foto = QtWidgets.QLabel()
                    label_foto.setAlignment(QtCore.Qt.AlignCenter)
                    label_foto.setPixmap(pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                    
                    # Botón cerrar
                    btn_cerrar = QtWidgets.QPushButton("Cerrar")
                    btn_cerrar.clicked.connect(dialog.accept)
                    btn_cerrar.setStyleSheet("""
                        QPushButton {
                            background-color: #3498db;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-weight: bold;
                            margin: 10px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    """)
                    
                    layout.addWidget(label_foto)
                    layout.addWidget(btn_cerrar)
                    
                    dialog.exec_()
                    print("✅ Foto completa mostrada correctamente")
                else:
                    print("❌ No se pudo cargar el pixmap para vista completa")
                    QtWidgets.QMessageBox.warning(
                        self.becerros_widget, 
                        "Error", 
                        "No se pudo cargar la foto del becerro"
                    )
            else:
                print("❌ No hay datos de foto para vista completa")
                QtWidgets.QMessageBox.information(
                    self.becerros_widget, 
                    "Información", 
                    "No hay foto disponible para este becerro"
                )
                    
        except Exception as e:
            print(f"❌ Error al mostrar foto completa: {e}")
            QtWidgets.QMessageBox.critical(
                self.becerros_widget,
                "Error",
                f"Error al mostrar foto: {str(e)}"
            )
    
    def agregar_botones_opciones(self, row, column, arete_becerro):
        """Agrega botones de salud, editar y eliminar en la columna de opciones (SIN OBSERVACIONES)"""
        try:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(4)
            
            # ✅ BOTÓN: Salud del becerro
            btn_salud = QtWidgets.QPushButton("❤️")
            btn_salud.setToolTip("Registro de salud")
            btn_salud.setStyleSheet("""
                QPushButton { 
                    background-color: #e74c3c; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 3px;
                    font-size: 12px;
                    min-width: 25px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            btn_salud.clicked.connect(lambda: self.abrir_registro_salud(arete_becerro))
            
            # Botón editar
            btn_editar = QtWidgets.QPushButton("✏️")
            btn_editar.setToolTip("Editar becerro")
            btn_editar.setStyleSheet("""
                QPushButton { 
                    background-color: #3498db; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 3px;
                    font-size: 12px;
                    min-width: 25px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn_editar.clicked.connect(lambda: self.editar_becerro(arete_becerro))
            
            # Botón eliminar
            btn_eliminar = QtWidgets.QPushButton("🗑️")
            btn_eliminar.setToolTip("Eliminar becerro")
            btn_eliminar.setStyleSheet("""
                QPushButton { 
                    background-color: #34495e; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 3px;
                    font-size: 12px;
                    min-width: 25px;
                }
                QPushButton:hover {
                    background-color: #2c3e50;
                }
            """)
            btn_eliminar.clicked.connect(lambda: self.eliminar_becerro(arete_becerro))
            
            # ✅ AGREGAR SOLO 3 BOTONES (sin observaciones)
            layout.addWidget(btn_salud)
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            layout.addStretch()
            
            self.tableWidget.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")
    
    def abrir_registro_salud(self, arete_becerro):
        """Abre el diálogo de registro de salud para el becerro"""
        try:
            print(f"❤️ Abriendo registro de salud para becerro arete: {arete_becerro}")
            
            # Obtener información del becerro
            becerro = self.db.obtener_becerro_por_arete(arete_becerro)
            if not becerro:
                QtWidgets.QMessageBox.warning(self.becerros_widget, "Error", "No se encontró el becerro")
                return
                
            # Crear y mostrar el diálogo de salud
            dialog = SaludBecerroController(self.becerros_widget, arete_becerro)
            resultado = dialog.exec_()
            
            if resultado == QtWidgets.QDialog.Accepted:
                print("✅ Registro de salud guardado correctamente")
                # Aquí puedes recargar datos si es necesario
                
        except Exception as e:
            print(f"❌ Error al abrir registro de salud: {e}")
            QtWidgets.QMessageBox.critical(
                self.becerros_widget,
                "Error",
                f"No se pudo abrir el registro de salud: {str(e)}"
            )

    def mostrar_observaciones_completas(self, arete_becerro, observaciones):
        """Muestra las observaciones completas en un diálogo"""
        try:
            print(f"📋 Mostrando observaciones completas para becerro arete: {arete_becerro}")
            
            # Obtener información del becerro para el título
            becerro = self.db.obtener_becerro_por_arete(arete_becerro)
            nombre_becerro = becerro[2] if becerro and len(becerro) > 2 else "N/A"
            
            # Crear diálogo
            dialog = QtWidgets.QDialog(self.becerros_widget)
            dialog.setWindowTitle(f"Observaciones - {nombre_becerro} (Arete: {arete_becerro})")
            dialog.setModal(True)
            dialog.resize(500, 400)
            
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Título
            titulo = QtWidgets.QLabel(f"Observaciones del becerro: {nombre_becerro}")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
            titulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(titulo)
            
            # Subtítulo
            subtitulo = QtWidgets.QLabel(f"Arete: {arete_becerro}")
            subtitulo.setStyleSheet("font-size: 14px; color: #7f8c8d; margin: 5px;")
            subtitulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(subtitulo)
            
            # Área de texto para las observaciones (solo lectura)
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
                }
            """)
            layout.addWidget(text_edit)
            
            # Botón cerrar
            btn_cerrar = QtWidgets.QPushButton("Cerrar")
            btn_cerrar.clicked.connect(dialog.accept)
            btn_cerrar.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            layout.addWidget(btn_cerrar)
            
            dialog.exec_()
            print("✅ Observaciones mostradas correctamente")
            
        except Exception as e:
            print(f"❌ Error al mostrar observaciones: {e}")
            QtWidgets.QMessageBox.critical(
                self.becerros_widget,
                "Error",
                f"No se pudieron mostrar las observaciones: {str(e)}"
            )
    
    def agregar_becerro(self):
        """Abre diálogo para agregar nuevo becerro"""
        try:
            print("📝 Abriendo diálogo para agregar becerro...")
            
            # Crear y mostrar el diálogo modal
            dialog = AgregarBecerroController(self.becerros_widget)
            resultado = dialog.exec_()
            
            # Si se guardó correctamente, recargar la tabla
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_becerros()
                print("✅ Becerro agregado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al abrir diálogo de agregar: {e}")
            QtWidgets.QMessageBox.critical(
                self.becerros_widget, 
                "Error", 
                f"No se pudo abrir el formulario: {str(e)}"
            )
    
    def editar_becerro(self, arete_becerro):
        """Abre diálogo para editar becerro existente"""
        try:
            print(f"✏️ Editando becerro con arete: {arete_becerro}")
            QtWidgets.QMessageBox.information(
                self.becerros_widget,
                "Funcionalidad en desarrollo", 
                f"La función para editar becerros (Arete: {arete_becerro}) estará disponible pronto."
            )
        except Exception as e:
            print(f"❌ Error al editar becerro: {e}")
    
    def eliminar_becerro(self, arete_becerro):
        """Elimina un becerro por su arete después de confirmación"""
        try:
            print(f"🔍 ELIMINAR - Arete recibido: '{arete_becerro}'")
            
            # Verificar que el arete es válido
            if not arete_becerro or arete_becerro.strip() == "":
                QtWidgets.QMessageBox.warning(self.becerros_widget, "Error", "Arete de becerro inválido")
                return
            
            # Obtener información del becerro para mostrar en el mensaje
            becerro = self.db.obtener_becerro_por_arete(arete_becerro)
            print(f"🔍 ELIMINAR - Becerro encontrado en BD: {becerro}")
            
            if not becerro:
                QtWidgets.QMessageBox.warning(
                    self.becerros_widget, 
                    "Error", 
                    f"No se encontró el becerro con arete: {arete_becerro}"
                )
                return
                
            nombre_becerro = becerro[2] if becerro and len(becerro) > 2 else "este becerro"
            arete_confirmacion = becerro[1] if becerro and len(becerro) > 1 else arete_becerro
            
            respuesta = QtWidgets.QMessageBox.question(
                self.becerros_widget, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar el becerro?\n\n"
                f"Nombre: {nombre_becerro}\n"
                f"Arete: {arete_confirmacion}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No  # Botón por defecto
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                print(f"🗑️ EJECUTANDO ELIMINACIÓN - Arete: {arete_becerro}")
                
                # Intentar eliminar por arete
                resultado = self.db.eliminar_becerro_por_arete(arete_becerro)
                print(f"🔍 ELIMINAR - Resultado de eliminar_becerro_por_arete(): {resultado}")
                
                if resultado:
                    QtWidgets.QMessageBox.information(
                        self.becerros_widget, 
                        "Éxito", 
                        f"Becerro '{nombre_becerro}' (Arete: {arete_confirmacion}) eliminado correctamente"
                    )
                    self.cargar_becerros()
                    print("✅ Becerro eliminado, tabla actualizada")
                else:
                    QtWidgets.QMessageBox.warning(
                        self.becerros_widget, 
                        "Error", 
                        f"Error al eliminar el becerro con arete: {arete_becerro}. "
                        f"Puede que tenga registros relacionados."
                    )
                    print("❌ ERROR - No se pudo eliminar el becerro")
        except Exception as e:
            print(f"❌ ERROR CRÍTICO al eliminar becerro: {e}")
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self.becerros_widget,
                "Error",
                f"Error crítico al eliminar becerro: {str(e)}"
            )
    
    def buscar_becerros(self):
        """Busca becerros según el texto en el buscador"""
        try:
            if self.lineEdit:
                texto = self.lineEdit.text().strip()
                if texto:
                    print(f"🔍 Buscando becerros: '{texto}'")
                    becerros = self.db.buscar_becerros_por_nombre(texto)
                    print(f"📊 {len(becerros)} becerros encontrados en la búsqueda")
                else:
                    becerros = self.db.obtener_becerros()
                self.llenar_tabla(becerros)
        except Exception as e:
            print(f"❌ Error al buscar becerros: {e}")
    
    # ✅ MÉTODO NUEVO: Para forzar actualización
    def actualizar_tabla(self):
        """Fuerza la actualización de la tabla"""
        print("🔄 Forzando actualización de tabla...")
        self.cargar_becerros()