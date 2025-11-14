# corrales_controller.py - VERSIÓN CORREGIDA
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
from controllers.Acorrales import AgregarCorralController
from controllers.Ecorrales import EditarCorralController

class CorralesController:
    def __init__(self, corrales_widget, bitacora_controller=None):
        self.corrales_widget = corrales_widget
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        self.setup_connections()
        self.configurar_tabla()
        self.cargar_corrales()  # Cargar datos al inicializar
        print("✅ CorralesController inicializado correctamente")
    
    def set_bitacora_controller(self, bitacora_controller):
        """Establecer el controlador de bitácora"""
        self.bitacora_controller = bitacora_controller
        print("✅ Bitácora asignada a CorralesController")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para corrales...")
            
            # Buscar elementos por objectName específico para corrales
            self.btn_agregar = self.corrales_widget.findChild(QtWidgets.QPushButton, "btn_agregar_corral")
            if not self.btn_agregar:
                # Si no encuentra por nombre, buscar por texto o posición
                buttons = self.corrales_widget.findChildren(QtWidgets.QPushButton)
                for btn in buttons:
                    if "agregar" in btn.text().lower() or "nuevo" in btn.text().lower():
                        self.btn_agregar = btn
                        break
            
            if self.btn_agregar:
                self.btn_agregar.clicked.connect(self.agregar_corral)
                print("✅ Botón agregar conectado")
            else:
                print("⚠️ No se encontró botón agregar específico, usando función por defecto")
                # Crear botón temporal si no existe
                self.btn_agregar = QtWidgets.QPushButton("Agregar Corral")
                self.btn_agregar.clicked.connect(self.agregar_corral)
                
            # Buscar buscador
            self.buscador = self.corrales_widget.findChild(QtWidgets.QLineEdit, "buscador_corrales")
            if not self.buscador:
                line_edits = self.corrales_widget.findChildren(QtWidgets.QLineEdit)
                if line_edits:
                    self.buscador = line_edits[0]  # Usar el primer lineEdit encontrado
            
            if self.buscador:
                self.buscador.textChanged.connect(self.buscar_corrales)
                print("✅ Buscador conectado")
            else:
                print("⚠️ No se encontró buscador específico")
                
            # Buscar tabla
            self.tabla = self.corrales_widget.findChild(QtWidgets.QTableWidget, "tabla_corrales")
            if not self.tabla:
                tablas = self.corrales_widget.findChildren(QtWidgets.QTableWidget)
                if tablas:
                    self.tabla = tablas[0]  # Usar la primera tabla encontrada
            
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
        layout = self.corrales_widget.layout()
        if layout:
            layout.addWidget(self.tabla)
        else:
            new_layout = QtWidgets.QVBoxLayout(self.corrales_widget)
            new_layout.addWidget(self.tabla)
        self.configurar_tabla()
    
    def configurar_tabla(self):
        """Configura el aspecto y comportamiento de la tabla"""
        try:
            # CORREGIDO: Quitamos la columna ID y empezamos con Nombre
            columnas = [
                "Nombre", "Ubicación", "Capacidad Máx", "Capacidad Actual", 
                "Fecha Mantenimiento", "Condición", "Observaciones", "Opciones"
            ]
            
            self.tabla.setColumnCount(len(columnas))
            self.tabla.setHorizontalHeaderLabels(columnas)
            
            # Configurar tamaños de columnas
            self.tabla.setColumnWidth(0, 120)  # Nombre
            self.tabla.setColumnWidth(1, 100)  # Ubicación
            self.tabla.setColumnWidth(2, 100)  # Capacidad Máx
            self.tabla.setColumnWidth(3, 100)  # Capacidad Actual
            self.tabla.setColumnWidth(4, 120)  # Fecha Mantenimiento
            self.tabla.setColumnWidth(5, 80)   # Condición
            self.tabla.setColumnWidth(6, 150)  # Observaciones
            self.tabla.setColumnWidth(7, 120)  # Opciones
            
            # Configurar altura de filas
            self.tabla.verticalHeader().setDefaultSectionSize(40)
            
            # Mejorar apariencia
            self.tabla.setAlternatingRowColors(True)
            self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tabla.verticalHeader().setVisible(False)
            
            print("✅ Tabla de corrales configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def cargar_corrales(self):
        """Carga todos los corrales en la tabla"""
        try:
            print("🔄 Cargando corrales desde la base de datos...")
            corrales = self.db.obtener_corrales_completos()
            print(f"📊 {len(corrales)} corrales encontrados")
            self.llenar_tabla(corrales)
        except Exception as e:
            print(f"❌ Error al cargar corrales: {e}")
            import traceback
            traceback.print_exc()
    
    def llenar_tabla(self, corrales):
        """Llena la tabla con los datos de los corrales"""
        try:
            self.tabla.setRowCount(0)

            for row_number, corral in enumerate(corrales):
                self.tabla.insertRow(row_number)
                
                # CORREGIDO: Empezamos desde la columna 1 (Nombre) en lugar de 0 (ID)
                # corral[0] = ID (lo ocultamos)
                # corral[1] = Nombre
                # corral[2] = Ubicación
                # etc...
                
                # Llenar datos visibles (empezando desde nombre)
                for col in range(1, min(8, len(corral))):  # Empezar desde 1 para omitir ID
                    item = QtWidgets.QTableWidgetItem(str(corral[col] if corral[col] is not None else ""))
                    self.tabla.setItem(row_number, col-1, item)  # col-1 porque quitamos la columna ID
                
                # Botones de opciones - usar el ID del corral (corral[0])
                self.agregar_botones_opciones(row_number, 7, str(corral[0]))  # 7 porque ahora tenemos 7 columnas visibles

            print(f"✅ Tabla llenada con {len(corrales)} registros")

        except Exception as e:
            print(f"❌ Error al llenar tabla: {e}")

    def agregar_botones_opciones(self, row, column, id_corral):
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
            btn_editar.clicked.connect(lambda checked, id=id_corral: self.editar_corral(id))
            
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
            btn_eliminar.clicked.connect(lambda checked, id=id_corral: self.eliminar_corral(id))
            
            layout.addWidget(btn_editar)
            layout.addWidget(btn_eliminar)
            layout.addStretch()
            
            self.tabla.setCellWidget(row, column, widget)
            
        except Exception as e:
            print(f"❌ Error al agregar botones: {e}")
    
    def agregar_corral(self):
        """Abre diálogo para agregar nuevo corral"""
        try:
            print("📝 Abriendo diálogo para agregar corral...")
            dialog = AgregarCorralController(parent=self.corrales_widget, 
                bitacora_controller=self.bitacora_controller)
            resultado = dialog.exec_()
            
            if resultado == QtWidgets.QDialog.Accepted:
                self.cargar_corrales()
                print("✅ Corral agregado, tabla actualizada")
                
        except Exception as e:
            print(f"❌ Error al abrir diálogo de agregar: {e}")
            import traceback
            traceback.print_exc()
    
    def editar_corral(self, id_corral):
        """Abre diálogo para editar corral existente"""
        try:
            print(f"✏️ Editando corral con ID: {id_corral}")
            
            corral_data = self.db.obtener_corral_por_id_dict(id_corral)
            
            if corral_data:
                print(f"📄 Datos del corral obtenidos: {corral_data}")
                
                datos_completos = {
                    'identificador': corral_data.get('identificador', ''),
                    'nombre': corral_data.get('nombre', ''),
                    'ubicacion': corral_data.get('ubicacion', ''),
                    'capacidad_maxima': corral_data.get('capacidad_maxima', '0'),
                    'capacidad_actual': corral_data.get('capacidad_actual', '0'),
                    'fecha_mantenimiento': corral_data.get('fecha_mantenimiento', ''),
                    'condicion': corral_data.get('condicion', 'Bueno'),
                    'observaciones': corral_data.get('observaciones', '')
                }
                
                print(f"🎯 Enviando datos al editor: {datos_completos}")
                
                # ✅ PASAR BITÁCORA AL DIÁLOGO DE EDICIÓN
                dialog = EditarCorralController(
                    corral_data=datos_completos, 
                    parent=self.corrales_widget,
                    bitacora_controller=self.bitacora_controller
                )
                resultado = dialog.exec_()
                
                if resultado == QtWidgets.QDialog.Accepted:
                    # ✅ REGISTRAR EN BITÁCORA LA EDICIÓN
                    if self.bitacora_controller:
                        cambios = f"Corral editado - ID: {id_corral}, Nombre: {corral_data.get('nombre', '')}"
                        self.bitacora_controller.registrar_accion(
                            modulo="Corrales",
                            accion="ACTUALIZAR",
                            descripcion="Edición de datos de corral",
                            detalles=cambios
                        )
                        print("✅ Edición registrada en bitácora")
                    
                    self.cargar_corrales()
                    print("✅ Corral actualizado")
            else:
                print(f"❌ No se encontró corral con ID: {id_corral}")
                QtWidgets.QMessageBox.warning(
                    self.corrales_widget, 
                    "Error", 
                    f"No se encontró el corral con ID: {id_corral}"
                )
                
        except Exception as e:
            print(f"❌ Error al editar corral: {e}")
            import traceback
            traceback.print_exc()
    
    def eliminar_corral(self, id_corral):
        """Elimina un corral después de confirmación"""
        try:
            # Obtener nombre del corral para mostrar en el mensaje
            corral_data = self.db.obtener_corral_por_id_dict(id_corral)
            nombre_corral = corral_data.get('nombre', 'este corral') if corral_data else 'este corral'
            
            respuesta = QtWidgets.QMessageBox.question(
                self.corrales_widget, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar el corral '{nombre_corral}'?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.Yes:
                # ✅ REGISTRAR EN BITÁCORA ANTES DE ELIMINAR
                if self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Corrales",
                        accion="ELIMINAR",
                        descripcion="Eliminación de corral",
                        detalles=f"ID: {id_corral}, Nombre: {nombre_corral}"
                    )
                    print("✅ Eliminación registrada en bitácora")
                
                resultado = self.db.eliminar_corral_por_id(id_corral)
                
                if resultado:
                    QtWidgets.QMessageBox.information(
                        self.corrales_widget, 
                        "Éxito", 
                        "Corral eliminado correctamente"
                    )
                    self.cargar_corrales()
                else:
                    QtWidgets.QMessageBox.warning(
                        self.corrales_widget, 
                        "Error", 
                        "Error al eliminar el corral"
                    )
        except Exception as e:
            print(f"❌ Error al eliminar corral: {e}")
            QtWidgets.QMessageBox.critical(
                self.corrales_widget,
                "Error",
                f"Error al eliminar: {str(e)}"
            )
    
    def buscar_corrales(self):
        """Busca corrales según el texto en el buscador"""
        try:
            if self.buscador:
                texto = self.buscador.text().strip()
                if texto:
                    corrales = self.db.buscar_corrales_por_nombre(texto)
                else:
                    corrales = self.db.obtener_corrales_completos()
                self.llenar_tabla(corrales)
        except Exception as e:
            print(f"❌ Error al buscar corrales: {e}")