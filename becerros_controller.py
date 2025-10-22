from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from agregar_becerro_controller import AgregarBecerroController

class BecerrosController:
    def __init__(self, becerros_widget):
        self.becerros_widget = becerros_widget
        self.db = Database()
        self.setup_connections()
        print("✅ BecerrosController inicializado con widget directo")
        
    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            # Buscar elementos dentro del widget de becerros
            self.indexbtn2 = self.becerros_widget.findChild(QtWidgets.QPushButton, "indexbtn2")
            if self.indexbtn2:
                self.indexbtn2.clicked.connect(self.agregar_becerro)
                print("✅ Botón agregar conectado")
            else:
                print("⚠️ No se encontró el botón indexbtn2 en el widget de becerros")
                
            # Buscar lineEdit para búsqueda
            self.lineEdit = self.becerros_widget.findChild(QtWidgets.QLineEdit, "lineEdit")
            if self.lineEdit:
                self.lineEdit.textChanged.connect(self.buscar_becerros)
                print("✅ Buscador conectado")
            else:
                print("⚠️ No se encontró lineEdit en el widget de becerros")
                
            # Buscar tableWidget
            self.tableWidget = self.becerros_widget.findChild(QtWidgets.QTableWidget, "tableWidget")
            if self.tableWidget:
                print("✅ TableWidget encontrado")
            else:
                print("❌ No se encontró tableWidget en el widget de becerros")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
        
    def cargar_becerros(self):
        """Carga todos los becerros en la tabla"""
        try:
            print("🔄 Cargando becerros desde la base de datos...")
            becerros = self.db.obtener_becerros()
            print(f"📊 {len(becerros)} becerros encontrados")
            self.llenar_tabla(becerros)
        except Exception as e:
            print(f"❌ Error al cargar becerros: {e}")
    
    def llenar_tabla(self, becerros):
        """Llena la tabla con los datos de los becerros"""
        if not self.tableWidget:
            print("❌ No hay tableWidget disponible")
            return

        try:
            self.tableWidget.setRowCount(0)

            for row_number, becerro in enumerate(becerros):
                self.tableWidget.insertRow(row_number)

                # becerro[0] es el ID, lo saltamos
                for column_number in range(1, 13):  # Ahora son 13 columnas incluyendo foto
                    data = becerro[column_number] if column_number < len(becerro) else ""
                    actual_column = column_number - 1  # Ajustar índice

                    # Si es la columna de foto (índice 11)
                    if actual_column == 11:
                        self.agregar_botones_opciones(row_number, actual_column, becerro[0])
                    elif actual_column == 10:  # Columna de opciones (antes era 10, ahora 11)
                        self.agregar_botones_opciones(row_number, actual_column, becerro[0])
                    else:
                        item = QtWidgets.QTableWidgetItem(str(data) if data is not None else "")
                        self.tableWidget.setItem(row_number, actual_column, item)

            print(f"✅ Tabla llenada con {len(becerros)} registros")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")
    
    def agregar_botones_opciones(self, row, column, id_becerro):
        """Agrega botones de editar y eliminar en la columna de opciones"""
        try:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(2)
            
            btn_editar = QtWidgets.QPushButton("Editar")
            btn_editar.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; padding: 5px; border-radius: 3px; }")
            btn_editar.clicked.connect(lambda: self.editar_becerro(id_becerro))
            
            btn_eliminar = QtWidgets.QPushButton("Eliminar")
            btn_eliminar.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; border: none; padding: 5px; border-radius: 3px; }")
            btn_eliminar.clicked.connect(lambda: self.eliminar_becerro(id_becerro))
            
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            
            self.tableWidget.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")
    
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
    
    def editar_becerro(self, id_becerro):
        """Abre diálogo para editar becerro existente"""
        try:
            print(f"✏️ Editando becerro ID: {id_becerro}")
            QtWidgets.QMessageBox.information(
                self.becerros_widget,
                "Funcionalidad en desarrollo", 
                f"La función para editar becerros (ID: {id_becerro}) estará disponible pronto."
            )
        except Exception as e:
            print(f"❌ Error al editar becerro: {e}")
    
    def eliminar_becerro(self, id_becerro):
        """Elimina un becerro después de confirmación"""
        try:
            respuesta = QtWidgets.QMessageBox.question(
                self.becerros_widget, 
                "Confirmar eliminación", 
                "¿Estás seguro de que quieres eliminar este becerro?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                if self.db.eliminar_becerro(id_becerro):
                    QtWidgets.QMessageBox.information(self.becerros_widget, "Éxito", "Becerro eliminado correctamente")
                    self.cargar_becerros()
                else:
                    QtWidgets.QMessageBox.warning(self.becerros_widget, "Error", "Error al eliminar becerro")
        except Exception as e:
            print(f"❌ Error al eliminar becerro: {e}")
    
    def buscar_becerros(self):
        """Busca becerros según el texto en el buscador"""
        try:
            if self.lineEdit:
                texto = self.lineEdit.text().strip()
                if texto:
                    becerros = self.db.buscar_becerros_por_nombre(texto)
                else:
                    becerros = self.db.obtener_becerros()
                self.llenar_tabla(becerros)
        except Exception as e:
            print(f"❌ Error al buscar becerros: {e}")

    def mostrar_foto_becerro(self, id_becerro):
        """Muestra la foto de un becerro en un diálogo"""
        try:
            foto_data = self.db.obtener_foto_becerro(id_becerro)
            if foto_data:
                # Crear un pixmap desde los datos BLOB
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(foto_data)
                
                # Mostrar en un diálogo
                dialog = QtWidgets.QDialog(self.becerros_widget)
                dialog.setWindowTitle("Foto del Becerro")
                layout = QtWidgets.QVBoxLayout(dialog)
                
                label_foto = QtWidgets.QLabel()
                label_foto.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))
                layout.addWidget(label_foto)
                
                dialog.exec_()
            else:
                QtWidgets.QMessageBox.information(self.becerros_widget, "Información", "No hay foto disponible para este becerro")
                
        except Exception as e:
            print(f"❌ Error al mostrar foto: {e}")