# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from controllers.Aanimal import AgregarAnimalController
from controllers.Eanimal import EditarAnimalController

class AnimalesController:
    def __init__(self, animales_widget):
        self.animales_widget = animales_widget
        self.db = Database()
        self.setup_connections()
        self.configurar_tabla()
        print("✅ AnimalesController inicializado con widget directo")
        
        # Cargar datos automáticamente al iniciar
        self.cargar_animales()
        
    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Buscando elementos UI en Animales...")
            
            # Listar todos los widgets hijos para debug
            hijos = self.animales_widget.findChildren(QtWidgets.QWidget)
            print(f"📋 Widgets hijos encontrados: {len(hijos)}")
            for hijo in hijos:
                if hasattr(hijo, 'objectName') and hijo.objectName():
                    print(f"   - {hijo.objectName()}: {type(hijo).__name__}")
            
            # Buscar elementos específicos
            self.indexbtn2 = self.animales_widget.findChild(QtWidgets.QPushButton, "indexbtn2")
            if self.indexbtn2:
                self.indexbtn2.clicked.connect(self.agregar_animal)
                print("✅ Botón agregar conectado")
            else:
                print("❌ NO SE ENCONTRÓ indexbtn2")
                
            # Buscar lineEdit para búsqueda
            self.lineEdit = self.animales_widget.findChild(QtWidgets.QLineEdit, "lineEdit")
            if self.lineEdit:
                self.lineEdit.textChanged.connect(self.buscar_animales)
                print("✅ Buscador conectado")
            else:
                print("❌ NO SE ENCONTRÓ lineEdit")
                
            # Buscar tableWidget
            self.tableWidget = self.animales_widget.findChild(QtWidgets.QTableWidget, "tableWidget")
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
            # Columnas según el diseño UI
            columnas = [
                "ID", "Foto", "Arete", "Nombre", "Corral", "Sexo", "Raza", 
                "Tipo de producción", "Tipo de alimento", "Fecha de nacimiento", 
                "Estatus", "Observaciones", "Opciones"
            ]
            
            self.tableWidget.setColumnCount(len(columnas))
            self.tableWidget.setHorizontalHeaderLabels(columnas)
            
            # Configurar tamaños de columnas
            self.tableWidget.setColumnWidth(0, 40)    # ID
            self.tableWidget.setColumnWidth(1, 80)    # Foto
            self.tableWidget.setColumnWidth(2, 80)    # Arete
            self.tableWidget.setColumnWidth(3, 120)   # Nombre
            self.tableWidget.setColumnWidth(4, 80)    # Corral
            self.tableWidget.setColumnWidth(5, 60)    # Sexo
            self.tableWidget.setColumnWidth(6, 100)   # Raza
            self.tableWidget.setColumnWidth(7, 120)   # Tipo de producción
            self.tableWidget.setColumnWidth(8, 120)   # Tipo de alimento
            self.tableWidget.setColumnWidth(9, 100)   # Fecha de nacimiento
            self.tableWidget.setColumnWidth(10, 80)   # Estatus
            self.tableWidget.setColumnWidth(11, 150)  # Observaciones
            self.tableWidget.setColumnWidth(12, 150)  # Opciones
            
            # Configurar altura de filas para las fotos
            self.tableWidget.verticalHeader().setDefaultSectionSize(80)
            
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
                }
                QTableWidget::item {
                    padding: 5px;
                    border-bottom: 1px solid #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #27ae60;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }
            """)
            
            print("✅ Tabla de animales configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def on_cell_double_clicked(self, row, column):
        """Maneja el doble clic en celdas específicas - SOLO OBSERVACIONES"""
        if column == 11:  # Columna de Observaciones
            arete_item = self.tableWidget.item(row, 2)  # Columna Arete
            observacion_item = self.tableWidget.item(row, 11)  # Columna Observaciones
            
            if arete_item and observacion_item:
                arete = arete_item.text()
                observaciones = observacion_item.data(QtCore.Qt.UserRole)  # Datos completos
                
                if observaciones and observaciones.strip():
                    print(f"🖱️ Doble clic en observaciones para animal arete: {arete}")
                    self.mostrar_observaciones_completas(arete, observaciones)
                else:
                    print("ℹ️ No hay observaciones para mostrar")
    
    def cargar_animales(self):
        """Carga todos los animales en la tabla"""
        try:
            print("🔄 Cargando animales desde la base de datos...")
            
            animales = self.db.obtener_animales()
            print(f"📊 {len(animales)} animales encontrados en el controlador")
            
            if len(animales) == 0:
                print("⚠️ ADVERTENCIA: No se encontraron animales en la base de datos")
                QtWidgets.QMessageBox.information(
                    self.animales_widget, 
                    "Información", 
                    "No se encontraron animales en la base de datos."
                )
            
            self.llenar_tabla(animales)
        except Exception as e:
            print(f"❌ Error al cargar animales: {e}")
            import traceback
            traceback.print_exc()
    
    def llenar_tabla(self, animales):
        """Llena la tabla con los datos de los animales"""
        if not self.tableWidget:
            print("❌ No hay tableWidget disponible")
            return

        try:
            self.tableWidget.setRowCount(0)

            for row_number, animal in enumerate(animales):
                self.tableWidget.insertRow(row_number)
                self.tableWidget.setRowHeight(row_number, 80)  # Altura mayor para las fotos
                
                # ID (oculto pero necesario para operaciones)
                id_item = QtWidgets.QTableWidgetItem(str(animal[0] if animal[0] is not None else ""))
                self.tableWidget.setItem(row_number, 0, id_item)
                
                # Foto
                arete = str(animal[1] if animal[1] else "")
                self.mostrar_foto_en_tabla(row_number, 1, arete)
                
                # Arete (2)
                arete_item = QtWidgets.QTableWidgetItem(arete)
                self.tableWidget.setItem(row_number, 2, arete_item)
                
                # Nombre (3)
                nombre_item = QtWidgets.QTableWidgetItem(str(animal[2] if animal[2] else ""))
                self.tableWidget.setItem(row_number, 3, nombre_item)
                
                # Corral (4)
                corral_item = QtWidgets.QTableWidgetItem(str(animal[3] if animal[3] else ""))
                self.tableWidget.setItem(row_number, 4, corral_item)
                
                # Sexo (5)
                sexo_item = QtWidgets.QTableWidgetItem(str(animal[4] if animal[4] else ""))
                self.tableWidget.setItem(row_number, 5, sexo_item)
                
                # Raza (6)
                raza_item = QtWidgets.QTableWidgetItem(str(animal[5] if animal[5] else ""))
                self.tableWidget.setItem(row_number, 6, raza_item)
                
                # Tipo de producción (7)
                prod_item = QtWidgets.QTableWidgetItem(str(animal[6] if animal[6] else ""))
                self.tableWidget.setItem(row_number, 7, prod_item)
                
                # Tipo de alimento (8)
                alimento_item = QtWidgets.QTableWidgetItem(str(animal[7] if animal[7] else ""))
                self.tableWidget.setItem(row_number, 8, alimento_item)
                
                # Fecha de nacimiento (9)
                fecha_item = QtWidgets.QTableWidgetItem(str(animal[8] if animal[8] else ""))
                self.tableWidget.setItem(row_number, 9, fecha_item)
                
                # Estatus (10)
                estatus_item = QtWidgets.QTableWidgetItem(str(animal[9] if animal[9] else ""))
                self.tableWidget.setItem(row_number, 10, estatus_item)
                
                # Observaciones (11)
                observacion = str(animal[10] if len(animal) > 10 and animal[10] is not None else "")
                observacion_preview = observacion[:30] + "..." if len(observacion) > 30 else observacion
                observacion_item = QtWidgets.QTableWidgetItem(observacion_preview)
                
                # Guardar observaciones completas para el doble clic
                observacion_item.setData(QtCore.Qt.UserRole, observacion)
                
                # Hacer que la celda sea clickeable solo si hay observaciones
                if observacion and observacion.strip():
                    observacion_item.setForeground(QtGui.QColor('#2980b9'))
                    observacion_item.setToolTip("Doble clic para ver observaciones completas")
                    observacion_item.setFlags(observacion_item.flags() | QtCore.Qt.ItemIsEnabled)
                else:
                    observacion_item.setToolTip("Sin observaciones")
                    observacion_item.setForeground(QtGui.QColor('#95a5a6'))
                    
                self.tableWidget.setItem(row_number, 11, observacion_item)
                
                # Opciones (12)
                self.agregar_botones_opciones(row_number, 12, arete)

            # Ocultar columna ID
            self.tableWidget.setColumnHidden(0, True)
            
            print(f"✅ Tabla llenada con {len(animales)} registros de animales")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_foto_en_tabla(self, row, column, arete_animal):
        """Muestra la foto en pequeño directamente en la tabla usando el arete"""
        try:
            print(f"📸 Intentando mostrar foto para animal arete: {arete_animal}")
            foto_data = self.db.obtener_foto_animal_por_arete(arete_animal)
            
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
                    label_foto.mousePressEvent = lambda event, arete=arete_animal: self.mostrar_foto_completa_por_arete(arete)
                    
                    self.tableWidget.setCellWidget(row, column, label_foto)
                    print(f"✅ Miniatura de foto mostrada en tabla para arete: {arete_animal}")
                else:
                    print("❌ No se pudo cargar el pixmap desde los datos BLOB")
                    self.mostrar_placeholder_foto_por_arete(row, column, arete_animal, "❌ Error carga")
            else:
                print(f"❌ No hay datos de foto para animal arete: {arete_animal}")
                self.mostrar_placeholder_foto_por_arete(row, column, arete_animal, "📷 Sin foto")
                
        except Exception as e:
            print(f"❌ Error al mostrar foto en tabla: {e}")
            self.mostrar_placeholder_foto_por_arete(row, column, arete_animal, f"❌ Error: {str(e)}")

    def mostrar_placeholder_foto_por_arete(self, row, column, arete_animal, motivo="Sin foto"):
        """Muestra un placeholder cuando no hay foto o hay error"""
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
            label_placeholder.mousePressEvent = lambda event, arete=arete_animal, msg=motivo: self.mostrar_info_foto_por_arete(arete, msg)
            
            self.tableWidget.setCellWidget(row, column, label_placeholder)
            
        except Exception as e:
            print(f"❌ Error al mostrar placeholder: {e}")

    def mostrar_info_foto_por_arete(self, arete_animal, mensaje):
        """Muestra información de debug sobre la foto usando arete"""
        try:
            # Obtener información actualizada de la foto
            foto_data = self.db.obtener_foto_animal_por_arete(arete_animal)
            info_animal = self.db.obtener_animal_por_arete(arete_animal)
            
            mensaje_detallado = f"""
            Información de foto - Animal Arete: {arete_animal}
            
            Estado: {mensaje}
            Datos en BD: {'Sí' if foto_data else 'No'}
            Tamaño datos: {len(foto_data) if foto_data else 0} bytes
            Arete: {arete_animal}
            Nombre: {info_animal['nombre'] if info_animal else 'N/A'}
            ID en BD: {info_animal['id'] if info_animal else 'N/A'}
            """
            
            QtWidgets.QMessageBox.information(
                self.animales_widget,
                "Información de Foto",
                mensaje_detallado
            )
            
        except Exception as e:
            print(f"❌ Error al mostrar info foto: {e}")

    def mostrar_foto_completa_por_arete(self, arete_animal):
        """Muestra la foto en tamaño completo al hacer clic en la miniatura"""
        try:
            print(f"📷 Solicitando foto completa para animal arete: {arete_animal}")
            foto_data = self.db.obtener_foto_animal_por_arete(arete_animal)
            
            if foto_data:
                print(f"✅ Foto encontrada - Tamaño: {len(foto_data)} bytes")
                
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(foto_data):
                    print("✅ Pixmap cargado para vista completa")
                    
                    # Mostrar en un diálogo
                    dialog = QtWidgets.QDialog(self.animales_widget)
                    dialog.setWindowTitle("Foto del Animal - Vista Completa")
                    dialog.setModal(True)
                    dialog.resize(600, 600)
                    
                    layout = QtWidgets.QVBoxLayout(dialog)
                    
                    # Información del animal
                    animal = self.db.obtener_animal_por_arete(arete_animal)
                    if animal:
                        info_text = f"Arete: {animal['arete']} | Nombre: {animal['nombre']} | ID: {animal['id']}"
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
                            background-color: #27ae60;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-weight: bold;
                            margin: 10px;
                        }
                        QPushButton:hover {
                            background-color: #219a52;
                        }
                    """)
                    
                    layout.addWidget(label_foto)
                    layout.addWidget(btn_cerrar)
                    
                    dialog.exec_()
                    print("✅ Foto completa mostrada correctamente")
                else:
                    print("❌ No se pudo cargar el pixmap para vista completa")
                    QtWidgets.QMessageBox.warning(
                        self.animales_widget, 
                        "Error", 
                        "No se pudo cargar la foto del animal"
                    )
            else:
                print("❌ No hay datos de foto para vista completa")
                QtWidgets.QMessageBox.information(
                    self.animales_widget, 
                    "Información", 
                    "No hay foto disponible para este animal"
                )
                    
        except Exception as e:
            print(f"❌ Error al mostrar foto completa: {e}")
            QtWidgets.QMessageBox.critical(
                self.animales_widget,
                "Error",
                f"Error al mostrar foto: {str(e)}"
            )
    
    def agregar_botones_opciones(self, row, column, arete_animal):
        """Agrega botones de salud, editar y eliminar en la columna de opciones"""
        try:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(4)
            
            # Botón: Salud del animal
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
            btn_salud.clicked.connect(lambda: self.abrir_registro_salud(arete_animal))
            
            # Botón Editar
            btn_editar = QtWidgets.QPushButton("✏️")
            btn_editar.setToolTip("Editar animal")
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
            btn_editar.clicked.connect(lambda: self.editar_animal(arete_animal))
            
            # Botón eliminar
            btn_eliminar = QtWidgets.QPushButton("🗑️")
            btn_eliminar.setToolTip("Eliminar animal")
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
            btn_eliminar.clicked.connect(lambda: self.eliminar_animal(arete_animal))
            
            layout.addWidget(btn_salud)
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            layout.addStretch()
            
            self.tableWidget.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")
    

    def mostrar_observaciones_completas(self, arete_animal, observaciones):
        """Muestra las observaciones completas en un diálogo"""
        try:
            print(f"📋 Mostrando observaciones completas para animal arete: {arete_animal}")
            
            # Obtener información del animal para el título
            animal = self.db.obtener_animal_por_arete(arete_animal)
            nombre_animal = animal['nombre'] if animal else "N/A"
            
            # Crear diálogo
            dialog = QtWidgets.QDialog(self.animales_widget)
            dialog.setWindowTitle(f"Observaciones - {nombre_animal} (Arete: {arete_animal})")
            dialog.setModal(True)
            dialog.resize(500, 400)
            
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Título
            titulo = QtWidgets.QLabel(f"Observaciones del animal: {nombre_animal}")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
            titulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(titulo)
            
            # Subtítulo
            subtitulo = QtWidgets.QLabel(f"Arete: {arete_animal}")
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
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #219a52;
                }
            """)
            layout.addWidget(btn_cerrar)
            
            dialog.exec_()
            print("✅ Observaciones mostradas correctamente")
            
        except Exception as e:
            print(f"❌ Error al mostrar observaciones: {e}")
            QtWidgets.QMessageBox.critical(
                self.animales_widget,
                "Error",
                f"No se pudieron mostrar las observaciones: {str(e)}"
            )
    
    def agregar_animal(self):
        """Abre diálogo para agregar nuevo animal"""
        try:
            print("📝 Abriendo diálogo para agregar animal...")
            
            # Crear y mostrar el diálogo modal
            dialog = AgregarAnimalController(self.animales_widget)
            resultado = dialog.exec_()
            
            # Si se guardó correctamente, recargar la tabla
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_animales()
                print("✅ Animal agregado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al abrir diálogo de agregar: {e}")
            QtWidgets.QMessageBox.critical(
                self.animales_widget, 
                "Error", 
                f"No se pudo abrir el formulario: {str(e)}"
            )
    
    def editar_animal(self, arete_animal):
        """Abre diálogo para editar animal existente"""
        try:
            print(f"✏️ Editando animal con arete: {arete_animal}")
            
            # Obtener datos completos del animal
            animal_data = self.db.obtener_animal_por_arete(arete_animal)
            if not animal_data:
                QtWidgets.QMessageBox.warning(
                    self.animales_widget, 
                    "Error", 
                    f"No se encontró el animal con arete: {arete_animal}"
                )
                return
            
            # Ya viene como diccionario, no necesitamos convertirlo
            print(f"📋 Datos del animal a editar: {animal_data['nombre']} (Arete: {animal_data['arete']})")
            
            # Crear y mostrar el diálogo de edición
            dialog = EditarAnimalController(animal_data=animal_data, parent=self.animales_widget)
            resultado = dialog.exec_()
            
            # Si se guardaron los cambios, recargar la tabla
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_animales()
                print("✅ Animal actualizado, tabla recargada")
                
        except Exception as e:
            print(f"❌ Error al editar animal: {e}")
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self.animales_widget,
                "Error",
                f"No se pudo abrir el formulario de edición: {str(e)}"
            )
    
    def eliminar_animal(self, arete_animal):
        """Elimina un animal por su arete después de confirmación"""
        try:
            print(f"🔍 ELIMINAR - Arete recibido: '{arete_animal}'")
            
            # Verificar que el arete es válido
            if not arete_animal or arete_animal.strip() == "":
                QtWidgets.QMessageBox.warning(self.animales_widget, "Error", "Arete de animal inválido")
                return
            
            # Obtener información del animal para mostrar en el mensaje
            animal = self.db.obtener_animal_por_arete(arete_animal)
            print(f"🔍 ELIMINAR - Animal encontrado en BD: {animal}")
            
            if not animal:
                QtWidgets.QMessageBox.warning(
                    self.animales_widget, 
                    "Error", 
                    f"No se encontró el animal con arete: {arete_animal}"
                )
                return
                
            nombre_animal = animal['nombre'] if animal else "este animal"
            arete_confirmacion = animal['arete'] if animal else arete_animal
            
            respuesta = QtWidgets.QMessageBox.question(
                self.animales_widget, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar el animal?\n\n"
                f"Nombre: {nombre_animal}\n"
                f"Arete: {arete_confirmacion}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No  # Botón por defecto
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                print(f"🗑️ EJECUTANDO ELIMINACIÓN - Arete: {arete_animal}")
                
                # Intentar eliminar por arete
                resultado = self.db.eliminar_animal_por_arete(arete_animal)
                print(f"🔍 ELIMINAR - Resultado de eliminar_animal_por_arete(): {resultado}")
                
                if resultado:
                    QtWidgets.QMessageBox.information(
                        self.animales_widget, 
                        "Éxito", 
                        f"Animal '{nombre_animal}' (Arete: {arete_confirmacion}) eliminado correctamente"
                    )
                    self.cargar_animales()
                    print("✅ Animal eliminado, tabla actualizada")
                else:
                    QtWidgets.QMessageBox.warning(
                        self.animales_widget, 
                        "Error", 
                        f"Error al eliminar el animal con arete: {arete_animal}. "
                        f"Puede que tenga registros relacionados."
                    )
                    print("❌ ERROR - No se pudo eliminar el animal")
        except Exception as e:
            print(f"❌ ERROR CRÍTICO al eliminar animal: {e}")
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self.animales_widget,
                "Error",
                f"Error crítico al eliminar animal: {str(e)}"
            )
    
    def buscar_animales(self):
        """Busca animales según el texto en el buscador"""
        try:
            if self.lineEdit:
                texto = self.lineEdit.text().strip()
                if texto:
                    print(f"🔍 Buscando animales: '{texto}'")
                    animales = self.db.buscar_animales_por_nombre(texto)
                    print(f"📊 {len(animales)} animales encontrados en la búsqueda")
                else:
                    animales = self.db.obtener_animales()
                self.llenar_tabla(animales)
        except Exception as e:
            print(f"❌ Error al buscar animales: {e}")
    
    def actualizar_tabla(self):
        """Fuerza la actualización de la tabla"""
        print("🔄 Forzando actualización de tabla...")
        self.cargar_animales()