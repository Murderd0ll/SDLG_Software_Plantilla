from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from controllers.agregarusuario_controller import AgregarUsuarioController
from controllers.editarusuario_controller import EditarUsuarioController

class UsuariosController:
    def __init__(self, usuarios_widget, bitacora_controller=None):
        self.usuarios_widget = usuarios_widget
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        self.setup_connections()
        self.configurar_tabla()
        self.cargar_usuarios()
        print("✅ UsuariosController inicializado correctamente")
        
    def set_bitacora_controller(self, bitacora_controller):
        """Establecer el controlador de bitácora"""
        self.bitacora_controller = bitacora_controller
        print("✅ Bitácora asignada a UsuariosController")
        
    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para usuarios...")
            
            # Buscar elementos
            self.btn_agregar = self.usuarios_widget.findChild(QtWidgets.QPushButton, "btnAgregar")
            self.btn_regresar = self.usuarios_widget.findChild(QtWidgets.QPushButton, "btnRegresar")
            self.buscador = self.usuarios_widget.findChild(QtWidgets.QLineEdit, "lineEdit")
            self.tabla = self.usuarios_widget.findChild(QtWidgets.QTableWidget, "tableWidget")
            
            if self.btn_agregar:
                self.btn_agregar.clicked.connect(self.agregar_usuario)
                print("✅ Botón agregar conectado")
            else:
                print("❌ No se encontró botón agregar")
                
            if self.btn_regresar:
                self.btn_regresar.clicked.connect(self.regresar_a_seguridad)
                print("✅ Botón regresar conectado")
            else:
                print("❌ No se encontró botón regresar")
                
            if self.buscador:
                self.buscador.textChanged.connect(self.buscar_usuarios)
                print("✅ Buscador conectado")
            else:
                print("❌ No se encontró buscador")
                
            if self.tabla:
                print("✅ Tabla encontrada")
            else:
                print("❌ NO SE ENCONTRÓ TABLA")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()
    
    def regresar_a_seguridad(self):
        """Regresa a la página de Seguridad"""
        try:
            print("🔙 Regresando a página de Seguridad...")
            main_window = self.get_main_window()
            if main_window:
                main_window.cambiar_pagina(7, "Seguridad")
            else:
                print("❌ No se pudo encontrar la ventana principal")
        except Exception as e:
            print(f"❌ Error al regresar a seguridad: {e}")
    
    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.usuarios_widget
            while parent is not None:
                if hasattr(parent, 'cambiar_pagina') and hasattr(parent, 'ui'):
                    return parent
                parent = parent.parent()
            
            # Si no se encuentra, buscar entre las ventanas de la aplicación
            app = QtWidgets.QApplication.instance()
            for widget in app.topLevelWidgets():
                if hasattr(widget, 'cambiar_pagina') and hasattr(widget, 'ui'):
                    return widget
            
            return None
        except Exception as e:
            print(f"❌ Error obteniendo main window: {e}")
            return None
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla"""
        try:
            # Configurar encabezados (sin ID)
            encabezados = ["Usuario", "Nombre", "Teléfono", "Rol", "Opciones"]
            self.tabla.setColumnCount(len(encabezados))
            self.tabla.setHorizontalHeaderLabels(encabezados)
            
            # Configurar tamaños de columnas (sin ID)
            self.tabla.setColumnWidth(0, 120)  # Usuario
            self.tabla.setColumnWidth(1, 150)  # Nombre
            self.tabla.setColumnWidth(2, 100)  # Teléfono
            self.tabla.setColumnWidth(3, 100)  # Rol
            self.tabla.setColumnWidth(4, 120)  # Opciones
            
            # Configurar altura de filas
            self.tabla.verticalHeader().setDefaultSectionSize(40)
            
            # Mejorar apariencia
            self.tabla.setAlternatingRowColors(True)
            self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tabla.verticalHeader().setVisible(False)
            self.tabla.setSortingEnabled(True)
            
            # Mejorar estilo
            self.tabla.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    alternate-background-color: #f8f9fa;
                    gridline-color: #dee2e6;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                }
                QTableWidget::item {
                    padding: 5px;
                    border-bottom: 1px solid #dee2e6;
                }
                QTableWidget::item:selected {
                    background-color: #3498db;
                    color: white;
                }
            """)
            
            # Estilo de encabezados
            self.tabla.horizontalHeader().setStyleSheet("""
                QHeaderView::section {
                    background-color: #34495e;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                    font-size: 12px;
                }
                QHeaderView::section:first {
                    border-top-left-radius: 4px;
                }
                QHeaderView::section:last {
                    border-top-right-radius: 4px;
                }
            """)
            
            # Hacer que la última columna (Opciones) se expanda
            header = self.tabla.horizontalHeader()
            header.setStretchLastSection(False)
            
            print("✅ Tabla de usuarios configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def cargar_usuarios(self):
        """Carga todos los usuarios en la tabla"""
        try:
            print("🔄 Cargando usuarios desde la base de datos...")
            usuarios = self.db.obtener_usuarios()
            print(f"📊 {len(usuarios)} usuarios encontrados")
            self.llenar_tabla(usuarios)
        except Exception as e:
            print(f"❌ Error al cargar usuarios: {e}")
            import traceback
            traceback.print_exc()
    
    def llenar_tabla(self, usuarios):
        """Llena la tabla con los datos de los usuarios (sin ID)"""
        try:
            self.tabla.setRowCount(0)

            for row_number, usuario in enumerate(usuarios):
                self.tabla.insertRow(row_number)
                
                # Los datos vienen en este orden: [idusuario, usuario, nombre, telefono, rol]
                # Pero ahora solo mostramos: [usuario, nombre, telefono, rol, opciones]
                
                # Usuario (columna 0)
                item_usuario = QtWidgets.QTableWidgetItem(str(usuario[1] if usuario[1] else ""))
                self.tabla.setItem(row_number, 0, item_usuario)
                
                # Nombre (columna 1)
                item_nombre = QtWidgets.QTableWidgetItem(str(usuario[2] if usuario[2] else ""))
                self.tabla.setItem(row_number, 1, item_nombre)
                
                # Teléfono (columna 2)
                item_telefono = QtWidgets.QTableWidgetItem(str(usuario[3] if usuario[3] else ""))
                self.tabla.setItem(row_number, 2, item_telefono)
                
                # Rol (columna 3)
                item_rol = QtWidgets.QTableWidgetItem(str(usuario[4] if usuario[4] else ""))
                self.tabla.setItem(row_number, 3, item_rol)
                
                # Botones de opciones (columna 4) - guardamos el ID internamente
                self.agregar_botones_opciones(row_number, 4, str(usuario[0]))  # usuario[0] es el ID

            print(f"✅ Tabla llenada con {len(usuarios)} registros (ID oculto)")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")

    def agregar_botones_opciones(self, row, column, id_usuario):
        """Agrega botones de editar y eliminar"""
        try:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(4)
            
            # Botón editar
            btn_editar = QtWidgets.QPushButton("Editar")
            btn_editar.setStyleSheet("""
                QPushButton { 
                    background-color: #3498db; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 3px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            btn_editar.clicked.connect(lambda checked, id=id_usuario: self.editar_usuario(id))
            
            # Botón eliminar
            btn_eliminar = QtWidgets.QPushButton("Eliminar")
            btn_eliminar.setStyleSheet("""
                QPushButton { 
                    background-color: #e74c3c; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 3px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            btn_eliminar.clicked.connect(lambda checked, id=id_usuario: self.eliminar_usuario(id))
            
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            layout.addStretch()
            
            self.tabla.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")
    
    def agregar_usuario(self):
        """Abre diálogo para agregar nuevo usuario"""
        try:
            print("📝 Abriendo diálogo para agregar usuario...")
            
            # ✅ PASAR BITÁCORA AL DIÁLOGO
            dialog = AgregarUsuarioController(
                parent=self.usuarios_widget,
                bitacora_controller=self.bitacora_controller
            )
            resultado = dialog.exec_()
            
            # Si se guardó correctamente, recargar la tabla
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_usuarios()
                print("✅ Usuario agregado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al abrir diálogo de agregar: {e}")
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self.usuarios_widget, 
                "Error", 
                f"No se pudo abrir el formulario: {str(e)}"
            )
    
    def editar_usuario(self, id_usuario):
        """Abre diálogo para editar usuario existente"""
        try:
            print(f"✏️ Editando usuario con ID: {id_usuario}")
            
            # ✅ PASAR BITÁCORA AL DIÁLOGO
            dialog = EditarUsuarioController(
                id_usuario=id_usuario, 
                parent=self.usuarios_widget,
                bitacora_controller=self.bitacora_controller
            )
            resultado = dialog.exec_()
            
            # Si se guardó correctamente, recargar la tabla
            if resultado == QtWidgets.QDialog.Accepted:
                # ✅ REGISTRAR EN BITÁCORA LA EDICIÓN
                if self.bitacora_controller:
                    usuario_data = self.db.obtener_usuario_por_id(id_usuario)
                    if usuario_data:
                        nombre_usuario = usuario_data[1] if len(usuario_data) > 1 else "N/A"
                        cambios = f"Usuario editado - ID: {id_usuario}, Usuario: {nombre_usuario}"
                        self.bitacora_controller.registrar_accion(
                            modulo="Usuarios",
                            accion="ACTUALIZAR",
                            descripcion="Edición de datos de usuario",
                            detalles=cambios
                        )
                        print("✅ Edición registrada en bitácora")
                
                self.cargar_usuarios()
                print("✅ Usuario actualizado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al editar usuario: {e}")
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(
                self.usuarios_widget, 
                "Error", 
                f"No se pudo abrir el formulario de edición: {str(e)}"
            )
    
    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario después de confirmación"""
        try:
            # Obtener información del usuario para mostrar en el mensaje
            usuario_data = self.db.obtener_usuario_por_id(id_usuario)
            nombre_usuario = usuario_data[1] if usuario_data and len(usuario_data) > 1 else "este usuario"
            
            respuesta = QtWidgets.QMessageBox.question(
                self.usuarios_widget, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar al usuario '{nombre_usuario}'?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                # ✅ REGISTRAR EN BITÁCORA ANTES DE ELIMINAR
                if self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Usuarios",
                        accion="ELIMINAR",
                        descripcion="Eliminación de usuario",
                        detalles=f"ID: {id_usuario}, Usuario: {nombre_usuario}"
                    )
                    print("✅ Eliminación registrada en bitácora")
                
                resultado = self.db.eliminar_usuario_por_id(id_usuario)
                
                if resultado:
                    QtWidgets.QMessageBox.information(
                        self.usuarios_widget, 
                        "Éxito", 
                        f"Usuario '{nombre_usuario}' eliminado correctamente"
                    )
                    self.cargar_usuarios()
                else:
                    QtWidgets.QMessageBox.warning(
                        self.usuarios_widget, 
                        "Error", 
                        "Error al eliminar el usuario"
                    )
        except Exception as e:
            print(f"❌ Error al eliminar usuario: {e}")
            QtWidgets.QMessageBox.critical(
                self.usuarios_widget,
                "Error",
                f"Error al eliminar: {str(e)}"
            )
    
    def buscar_usuarios(self):
        """Busca usuarios según el texto en el buscador"""
        try:
            if self.buscador:
                texto = self.buscador.text().strip()
                if texto:
                    usuarios = self.db.buscar_usuarios_por_nombre(texto)
                else:
                    usuarios = self.db.obtener_usuarios()
                self.llenar_tabla(usuarios)
        except Exception as e:
            print(f"❌ Error al buscar usuarios: {e}")

    def mostrar_mensaje_temporal(self, titulo, mensaje, icono=None):
        """Muestra un mensaje temporal"""
        try:
            msg = QtWidgets.QMessageBox(self.usuarios_widget)
            msg.setWindowTitle(titulo)
            msg.setText(mensaje)
            
            if icono:
                msg.setIconPixmap(icono.scaled(64, 64, QtCore.Qt.KeepAspectRatio))
            else:
                msg.setIcon(QtWidgets.QMessageBox.Information)
                
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            
        except Exception as e:
            print(f"❌ Error mostrando mensaje temporal: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("👥 Cargando página de gestión de usuarios...")
        self.cargar_usuarios()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador de usuarios...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()