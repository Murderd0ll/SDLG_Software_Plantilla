# propietarios_controller.py - VERSIÓN ACTUALIZADA CON BITÁCORA
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from controllers.Apropietarios import AgregarPropietarioController
from controllers.Epropietarios import EditarPropietarioController

class PropietariosController:
    def __init__(self, propietarios_widget, bitacora_controller=None):
        self.propietarios_widget = propietarios_widget
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        self.setup_connections()
        self.configurar_tabla()
        print("✅ PropietariosController inicializado correctamente")
        
        # Cargar datos automáticamente al iniciar
        self.cargar_propietarios()

    def set_bitacora_controller(self, bitacora_controller):
        """Establecer el controlador de bitácora"""
        self.bitacora_controller = bitacora_controller
        print("✅ Bitácora asignada a PropietariosController")
        
    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para propietarios...")
            
            # Buscar elementos por objectName específico para propietarios
            self.btn_agregar = self.propietarios_widget.findChild(QtWidgets.QPushButton, "btn_agregar_propietario")
            if not self.btn_agregar:
                # Buscar por texto o posición
                buttons = self.propietarios_widget.findChildren(QtWidgets.QPushButton)
                for btn in buttons:
                    if "agregar" in btn.text().lower() or "nuevo" in btn.text().lower():
                        self.btn_agregar = btn
                        break
            
            if self.btn_agregar:
                self.btn_agregar.clicked.connect(self.agregar_propietario)
                print("✅ Botón agregar conectado")
            else:
                print("⚠️ No se encontró botón agregar específico")
                # Crear botón temporal si no existe
                self.btn_agregar = QtWidgets.QPushButton("Agregar Propietario")
                self.btn_agregar.clicked.connect(self.agregar_propietario)
                
            # Buscar buscador
            self.buscador = self.propietarios_widget.findChild(QtWidgets.QLineEdit, "buscador_propietarios")
            if not self.buscador:
                line_edits = self.propietarios_widget.findChildren(QtWidgets.QLineEdit)
                if line_edits:
                    self.buscador = line_edits[0]
            
            if self.buscador:
                self.buscador.textChanged.connect(self.buscar_propietarios)
                print("✅ Buscador conectado")
            else:
                print("⚠️ No se encontró buscador específico")
                
            # Buscar tabla
            self.tabla = self.propietarios_widget.findChild(QtWidgets.QTableWidget, "tabla_propietarios")
            if not self.tabla:
                tablas = self.propietarios_widget.findChildren(QtWidgets.QTableWidget)
                if tablas:
                    self.tabla = tablas[0]
            
            if self.tabla:
                print("✅ Tabla encontrada")
                self.configurar_tabla()
            else:
                print("❌ NO SE ENCONTRÓ TABLA - Creando tabla temporal")
                self.crear_tabla_temporal()
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()
    
    def crear_tabla_temporal(self):
        """Crea una tabla temporal si no se encuentra en el UI"""
        self.tabla = QtWidgets.QTableWidget()
        layout = self.propietarios_widget.layout()
        if layout:
            layout.addWidget(self.tabla)
        else:
            new_layout = QtWidgets.QVBoxLayout(self.propietarios_widget)
            new_layout.addWidget(self.tabla)
        self.configurar_tabla()
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla"""
        try:
            # ✅ COLUMNAS CON FOTO PRIMERO + OBSERVACIONES
            columnas = [
                "ID", "Foto", "Nombre", "Teléfono", "Correo", "Dirección", 
                "PSG", "UPP", "RFC", "Observaciones", "Opciones"
            ]
            
            self.tabla.setColumnCount(len(columnas))
            self.tabla.setHorizontalHeaderLabels(columnas)
            
            # ✅ TAMAÑOS DE COLUMNAS OPTIMIZADOS
            self.tabla.setColumnWidth(0, 40)    # ID
            self.tabla.setColumnWidth(1, 80)    # Foto (PRIMERA COLUMNA VISIBLE)
            self.tabla.setColumnWidth(2, 150)   # Nombre
            self.tabla.setColumnWidth(3, 100)   # Teléfono
            self.tabla.setColumnWidth(4, 150)   # Correo
            self.tabla.setColumnWidth(5, 120)   # Dirección
            self.tabla.setColumnWidth(6, 80)    # PSG
            self.tabla.setColumnWidth(7, 80)    # UPP
            self.tabla.setColumnWidth(8, 100)   # RFC
            self.tabla.setColumnWidth(9, 150)   # Observaciones
            self.tabla.setColumnWidth(10, 120)  # Opciones
            
            # Configurar altura de filas para las fotos
            self.tabla.verticalHeader().setDefaultSectionSize(80)
            
            # Mejorar apariencia
            self.tabla.setAlternatingRowColors(True)
            self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tabla.verticalHeader().setVisible(False)
            
            # ✅ CORRECCIÓN: Desconectar antes de conectar para evitar múltiples conexiones
            try:
                self.tabla.cellDoubleClicked.disconnect()
            except:
                pass
                
            # ✅ CONEXIÓN ÚNICA: Doble clic en celdas - SOLO PARA OBSERVACIONES
            self.tabla.cellDoubleClicked.connect(self.on_cell_double_clicked)
            
            # Estilo para la tabla
            self.tabla.setStyleSheet("""
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
            
            print("✅ Tabla de propietarios configurada correctamente - FOTO PRIMERO + OBSERVACIONES CLICKEABLES")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def on_cell_double_clicked(self, row, column):
        """Maneja el doble clic en celdas específicas - SOLO OBSERVACIONES"""
        # ✅ SOLO responder a doble clic en columna de Observaciones (9)
        if column == 9:  
            id_item = self.tabla.item(row, 0)  # Columna ID
            observacion_item = self.tabla.item(row, 9)  # Columna Observaciones
            
            if id_item and observacion_item:
                id_propietario = id_item.text()
                observaciones = observacion_item.data(QtCore.Qt.UserRole)  # Datos completos
                
                # ✅ VERIFICAR que hay observaciones antes de abrir el diálogo
                if observaciones and observaciones.strip():
                    self.mostrar_observaciones_completas(id_propietario, observaciones)
                else:
                    print("ℹ️ No hay observaciones para mostrar")
    
    def cargar_propietarios(self):
        """Carga todos los propietarios en la tabla"""
        try:
            print("🔄 Cargando propietarios desde la base de datos...")
            propietarios = self.db.obtener_propietarios_completos()
            print(f"📊 {len(propietarios)} propietarios encontrados")
            self.llenar_tabla(propietarios)
        except Exception as e:
            print(f"❌ Error al cargar propietarios: {e}")
            import traceback
            traceback.print_exc()
    
    def llenar_tabla(self, propietarios):
        """Llena la tabla con los datos de los propietarios"""
        if not self.tabla:
            print("❌ No hay tabla disponible")
            return

        try:
            self.tabla.setRowCount(0)

            for row_number, propietario in enumerate(propietarios):
                self.tabla.insertRow(row_number)
                self.tabla.setRowHeight(row_number, 80)  # Altura mayor para las fotos
                
                # ID (oculto pero necesario para operaciones)
                id_item = QtWidgets.QTableWidgetItem(str(propietario[0] if propietario[0] is not None else ""))
                self.tabla.setItem(row_number, 0, id_item)
                
                # ✅ FOTO EN COLUMNA 1 (PRIMERA VISIBLE)
                id_propietario = str(propietario[0] if propietario[0] else "")
                self.mostrar_foto_en_tabla(row_number, 1, id_propietario)
                
                # Nombre (2)
                nombre_item = QtWidgets.QTableWidgetItem(str(propietario[1] if propietario[1] else ""))
                self.tabla.setItem(row_number, 2, nombre_item)
                
                # Teléfono (3)
                telefono_item = QtWidgets.QTableWidgetItem(str(propietario[2] if propietario[2] else ""))
                self.tabla.setItem(row_number, 3, telefono_item)
                
                # Correo (4)
                correo_item = QtWidgets.QTableWidgetItem(str(propietario[3] if propietario[3] else ""))
                self.tabla.setItem(row_number, 4, correo_item)
                
                # Dirección (5)
                direccion_item = QtWidgets.QTableWidgetItem(str(propietario[4] if propietario[4] else ""))
                self.tabla.setItem(row_number, 5, direccion_item)
                
                # PSG (6)
                psg_item = QtWidgets.QTableWidgetItem(str(propietario[5] if propietario[5] else ""))
                self.tabla.setItem(row_number, 6, psg_item)
                
                # UPP (7)
                upp_item = QtWidgets.QTableWidgetItem(str(propietario[6] if propietario[6] else ""))
                self.tabla.setItem(row_number, 7, upp_item)
                
                # RFC (8)
                rfc_item = QtWidgets.QTableWidgetItem(str(propietario[7] if propietario[7] else ""))
                self.tabla.setItem(row_number, 8, rfc_item)
                
                # ✅ OBSERVACIONES EN COLUMNA 9 - CLICKEABLE
                observacion = str(propietario[8] if len(propietario) > 8 and propietario[8] is not None else "")
                observacion_preview = observacion[:30] + "..." if len(observacion) > 30 else observacion
                observacion_item = QtWidgets.QTableWidgetItem(observacion_preview)
                
                # ✅ GUARDAR OBSERVACIONES COMPLETAS para el doble clic
                observacion_item.setData(QtCore.Qt.UserRole, observacion)
                
                # ✅ HACER QUE LA CELDA SEA CLICKEABLE SOLO SI HAY OBSERVACIONES
                if observacion and observacion.strip():
                    observacion_item.setForeground(QtGui.QColor('#2980b9'))
                    observacion_item.setToolTip("Doble clic para ver observaciones completas")
                    observacion_item.setFlags(observacion_item.flags() | QtCore.Qt.ItemIsEnabled)
                else:
                    observacion_item.setToolTip("Sin observaciones")
                    observacion_item.setForeground(QtGui.QColor('#95a5a6'))
                    
                self.tabla.setItem(row_number, 9, observacion_item)
                
                # ✅ OPCIONES EN COLUMNA 10 CON BOTONES
                self.agregar_botones_opciones(row_number, 10, id_propietario)

            # Ocultar columna ID
            self.tabla.setColumnHidden(0, True)
            
            print(f"✅ Tabla llenada con {len(propietarios)} registros")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_foto_en_tabla(self, row, column, id_propietario):
        """Muestra la foto en pequeño directamente en la tabla usando el id"""
        try:
            foto_data = self.db.obtener_foto_propietario_por_id(id_propietario)
            
            if foto_data:
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(foto_data):
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
                    label_foto.mousePressEvent = lambda event, id=id_propietario: self.mostrar_foto_completa_por_id(id)
                    
                    self.tabla.setCellWidget(row, column, label_foto)
                else:
                    self.mostrar_placeholder_foto_por_id(row, column, id_propietario, "❌ Error carga")
            else:
                self.mostrar_placeholder_foto_por_id(row, column, id_propietario, "📷 Sin foto")
                
        except Exception as e:
            print(f"❌ Error al mostrar foto en tabla: {e}")
            self.mostrar_placeholder_foto_por_id(row, column, id_propietario, f"❌ Error: {str(e)}")

    def mostrar_placeholder_foto_por_id(self, row, column, id_propietario, motivo="Sin foto"):
        """Muestra un placeholder cuando no hay foto o hay error"""
        try:
            label_placeholder = QtWidgets.QLabel("👤")
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
            label_placeholder.mousePressEvent = lambda event, id=id_propietario, msg=motivo: self.mostrar_info_foto_por_id(id, msg)
            
            self.tabla.setCellWidget(row, column, label_placeholder)
            
        except Exception as e:
            print(f"❌ Error al mostrar placeholder: {e}")

    def mostrar_info_foto_por_id(self, id_propietario, mensaje):
        """Muestra información de debug sobre la foto usando id"""
        try:
            # Obtener información actualizada de la foto
            foto_data = self.db.obtener_foto_propietario_por_id(id_propietario)
            info_propietario = self.db.obtener_propietario_por_id(id_propietario)
            
            mensaje_detallado = f"""
            Información de foto - Propietario ID: {id_propietario}
            
            Estado: {mensaje}
            Datos en BD: {'Sí' if foto_data else 'No'}
            Tamaño datos: {len(foto_data) if foto_data else 0} bytes
            ID: {id_propietario}
            Nombre: {info_propietario[1] if info_propietario else 'N/A'}
            """
            
            QtWidgets.QMessageBox.information(
                self.propietarios_widget,
                "Información de Foto",
                mensaje_detallado
            )
            
        except Exception as e:
            print(f"❌ Error al mostrar info foto: {e}")

    def mostrar_foto_completa_por_id(self, id_propietario):
        """Muestra la foto en tamaño completo al hacer clic en la miniatura"""
        try:
            foto_data = self.db.obtener_foto_propietario_por_id(id_propietario)
            
            if foto_data:
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                if pixmap.loadFromData(foto_data):
                    # Mostrar en un diálogo
                    dialog = QtWidgets.QDialog(self.propietarios_widget)
                    dialog.setWindowTitle("Foto del Propietario - Vista Completa")
                    dialog.setModal(True)
                    dialog.resize(600, 600)
                    
                    layout = QtWidgets.QVBoxLayout(dialog)
                    
                    # Información del propietario
                    propietario = self.db.obtener_propietario_por_id(id_propietario)
                    if propietario:
                        info_text = f"ID: {propietario[0]} | Nombre: {propietario[1]}"
                        label_info = QtWidgets.QLabel(info_text)
                        label_info.setAlignment(QtCore.Qt.AlignCenter)
                        label_info.setStyleSheet("font-weight: bold; margin: 10px; font-size: 14px;")
                        layout.addWidget(label_info)
                
                    # Label para la foto
                    label_foto = QtWidgets.QQLabel()
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
                else:
                    QtWidgets.QMessageBox.warning(
                        self.propietarios_widget, 
                        "Error", 
                        "No se pudo cargar la foto del propietario"
                    )
            else:
                QtWidgets.QMessageBox.information(
                    self.propietarios_widget, 
                    "Información", 
                    "No hay foto disponible para este propietario"
                )
                    
        except Exception as e:
            print(f"❌ Error al mostrar foto completa: {e}")
            QtWidgets.QMessageBox.critical(
                self.propietarios_widget,
                "Error",
                f"Error al mostrar foto: {str(e)}"
            )
    
    def agregar_botones_opciones(self, row, column, id_propietario):
        """Agrega botones de editar y eliminar en la columna de opciones"""
        try:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(4)
            
            # Botón Editar
            btn_editar = QtWidgets.QPushButton("✏️")
            btn_editar.setToolTip("Editar propietario")
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
            btn_editar.clicked.connect(lambda: self.editar_propietario(id_propietario))
            
            # Botón Eliminar
            btn_eliminar = QtWidgets.QPushButton("🗑️")
            btn_eliminar.setToolTip("Eliminar propietario")
            btn_eliminar.setStyleSheet("""
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
            btn_eliminar.clicked.connect(lambda: self.eliminar_propietario(id_propietario))
            
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            layout.addStretch()
            
            self.tabla.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")

    def mostrar_observaciones_completas(self, id_propietario, observaciones):
        """Muestra las observaciones completas en un diálogo"""
        try:
            print(f"📋 Mostrando observaciones completas para propietario ID: {id_propietario}")
            
            # Obtener información del propietario para el título
            propietario = self.db.obtener_propietario_por_id(id_propietario)
            nombre_propietario = propietario[1] if propietario and len(propietario) > 1 else "N/A"
            
            # Crear diálogo
            dialog = QtWidgets.QDialog(self.propietarios_widget)
            dialog.setWindowTitle(f"Observaciones - {nombre_propietario} (ID: {id_propietario})")
            dialog.setModal(True)
            dialog.resize(500, 400)
            
            layout = QtWidgets.QVBoxLayout(dialog)
            
            # Título
            titulo = QtWidgets.QLabel(f"Observaciones del propietario: {nombre_propietario}")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
            titulo.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(titulo)
            
            # Subtítulo
            subtitulo = QtWidgets.QLabel(f"ID: {id_propietario}")
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
                self.propietarios_widget,
                "Error",
                f"No se pudieron mostrar las observaciones: {str(e)}"
            )
    
    def agregar_propietario(self):
        """Abre diálogo para agregar nuevo propietario"""
        try:
            print("📝 Abriendo diálogo para agregar propietario...")
            # ✅ PASAR BITÁCORA AL DIÁLOGO
            dialog = AgregarPropietarioController(
                parent=self.propietarios_widget, 
                bitacora_controller=self.bitacora_controller
            )
            resultado = dialog.exec_()
            
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_propietarios()
                print("✅ Propietario agregado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al abrir diálogo de agregar: {e}")
    
    def editar_propietario(self, id_propietario):
        """Abre diálogo para editar propietario existente"""
        try:
            print(f"✏️ Editando propietario con ID: {id_propietario}")
            propietario_data = self.db.obtener_propietario_por_id_dict(id_propietario)
            
            if propietario_data:
                datos_completos = {
                     'id': propietario_data.get('id', ''),
                     'nombre': propietario_data.get('nombre', ''),
                     'telefono': propietario_data.get('telefono', ''),
                     'correo': propietario_data.get('correo', ''),
                     'direccion': propietario_data.get('direccion', ''),
                     'psg': propietario_data.get('psg', ''),
                     'upp': propietario_data.get('upp', ''),
                     'rfc': propietario_data.get('rfc', ''), 
                     'observaciones': propietario_data.get('observaciones', ''),
                     'foto': propietario_data.get('foto', None)
                }
                print(f"🎯 Enviando datos al editor: {datos_completos}")
                # ✅ PASAR BITÁCORA AL DIÁLOGO DE EDICIÓN
                dialog = EditarPropietarioController(
                    propietario_data=datos_completos, 
                    parent=self.propietarios_widget,
                    bitacora_controller=self.bitacora_controller
                )
                resultado = dialog.exec_()
                
                if resultado == QtWidgets.QDialog.Accepted:
                    # ✅ REGISTRAR EN BITÁCORA LA EDICIÓN
                    if self.bitacora_controller:
                        cambios = f"Propietario editado - ID: {id_propietario}, Nombre: {propietario_data.get('nombre', '')}"
                        self.bitacora_controller.registrar_accion(
                            modulo="Propietarios",
                            accion="ACTUALIZAR",
                            descripcion="Edición de datos de propietario",
                            detalles=cambios
                        )
                        print("✅ Edición registrada en bitácora")
                    
                    self.cargar_propietarios()
                    print("✅ Propietario actualizado")
            else:
                print(f"❌ No se encontró propietario con ID: {id_propietario}")
                
        except Exception as e:
            print(f"❌ Error al editar propietario: {e}")
    
    def eliminar_propietario(self, id_propietario):
        """Elimina un propietario después de confirmación"""
        try:
            propietario = self.db.obtener_propietario_por_id(id_propietario)
            nombre_propietario = propietario[1] if propietario and len(propietario) > 1 else "este propietario"
            
            respuesta = QtWidgets.QMessageBox.question(
                self.propietarios_widget, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar al propietario?\n\n"
                f"Nombre: {nombre_propietario}\n"
                f"ID: {id_propietario}",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                # ✅ REGISTRAR EN BITÁCORA ANTES DE ELIMINAR
                if self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Propietarios",
                        accion="ELIMINAR",
                        descripcion="Eliminación de propietario",
                        detalles=f"ID: {id_propietario}, Nombre: {nombre_propietario}"
                    )
                    print("✅ Eliminación registrada en bitácora")
                
                resultado = self.db.eliminar_propietario_por_id(id_propietario)
                
                if resultado:
                    QtWidgets.QMessageBox.information(
                        self.propietarios_widget, 
                        "Éxito", 
                        f"Propietario '{nombre_propietario}' eliminado correctamente"
                    )
                    self.cargar_propietarios()
                else:
                    QtWidgets.QMessageBox.warning(
                        self.propietarios_widget, 
                        "Error", 
                        "Error al eliminar el propietario. Puede que tenga registros relacionados."
                    )
        except Exception as e:
            print(f"❌ Error al eliminar propietario: {e}")
    
    def buscar_propietarios(self):
        """Busca propietarios según el texto en el buscador"""
        try:
            if self.buscador:
                texto = self.buscador.text().strip()
                if texto:
                    propietarios = self.db.buscar_propietarios_en_todos_los_campos(texto)
                else:
                    propietarios = self.db.obtener_propietarios_completos()
                self.llenar_tabla(propietarios)
        except Exception as e:
            print(f"❌ Error al buscar propietarios: {e}")

    def actualizar_tabla(self):
        """Fuerza la actualización de la tabla"""
        print("🔄 Forzando actualización de tabla...")
        self.cargar_propietarios()