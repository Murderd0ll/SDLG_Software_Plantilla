# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarreproduccion_ui import Ui_Dialog
from database import Database

class AgregarReproduccionController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None, arete_animal=None, main_window=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        self.arete_animal = arete_animal
        self.main_window = main_window
        
        self.setup_connections()
        self.configurar_combobox()
        self.configurar_fechas()
        self.verificar_widgets()
        
        # Si se proporcionó un arete, establecerlo en el campo correspondiente
        if self.arete_animal:
            self.ui.lineEdit_7.setText(self.arete_animal)
        
    def verificar_widgets(self):
        """Función temporal para verificar que todos los widgets existen"""
        print("\n🔍 VERIFICANDO WIDGETS REPRODUCCIÓN:")
        widgets = [
            'lineEdit_7', 'comboBox_2', 'comboBox', 'spinBox',
            'dateEdit_4', 'dateEdit_2', 'dateEdit_3', 'textEdit'
        ]
        
        for widget_name in widgets:
            widget = getattr(self.ui, widget_name, None)
            if widget:
                print(f"✅ {widget_name}: ENCONTRADO")
            else:
                print(f"❌ {widget_name}: NO ENCONTRADO")
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_reproduccion)  # Guardar
        self.ui.pushButton_3.clicked.connect(self.ver_registros_reproduccion)  # Ver registros
        
    def configurar_combobox(self):
        """Configura los combobox"""
        # Los combobox ya tienen los items del diseño, pero podemos verificar
        print("✅ Combobox de reproducción configurados")
        
    def configurar_fechas(self):
        """Configura las fechas con valores por defecto"""
        fecha_actual = QtCore.QDate.currentDate()
        
        # Fecha de servicio actual (hoy)
        self.ui.dateEdit_4.setDate(fecha_actual)
        
        # Fecha aproximada del parto (280 días después - gestación bovina)
        fecha_parto_aproximada = fecha_actual.addDays(274)
        self.ui.dateEdit_2.setDate(fecha_parto_aproximada)
        
        # Fecha de nuevo servicio (60 días después del parto)
        fecha_nuevo_servicio = fecha_parto_aproximada.addDays(365)
        self.ui.dateEdit_3.setDate(fecha_nuevo_servicio)
        
        print("✅ Fechas de reproducción configuradas")
        
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit_7.text().strip()
            cargada = self.ui.comboBox_2.currentText().strip()
            tecnica = self.ui.comboBox.currentText().strip()
            cantpartos = self.ui.spinBox.value()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit_7.setFocus()
                return False
                
            if not cargada:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Debe especificar si el animal está cargado")
                self.ui.comboBox_2.setFocus()
                return False
                
            if not tecnica:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Debe seleccionar una técnica de preñez")
                self.ui.comboBox.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def verificar_y_actualizar_tabla(self):
        """Verifica y actualiza la estructura de la tabla treprod si es necesario"""
        try:
            # Verificar si la tabla existe
            tablas = self.db.listar_tablas()
            if 'treprod' not in tablas:
                print("❌ La tabla 'treprod' no existe")
                return self.crear_tabla_reproduccion()
            
            # Verificar si tiene la columna 'observaciones'
            cursor = self.db.ejecutar_consulta("PRAGMA table_info(treprod)")
            if cursor:
                columnas = [col[1] for col in cursor.fetchall()]  # [id, areteanimal, cargada, ...]
                print(f"📋 Columnas actuales en treprod: {columnas}")
                
                if 'observaciones' not in columnas:
                    print("🔄 Agregando columna 'observaciones' a la tabla existente...")
                    return self.agregar_columna_observaciones()
                else:
                    print("✅ La tabla ya tiene la columna 'observaciones'")
                    return True
            return False
            
        except Exception as e:
            print(f"❌ Error verificando estructura de tabla: {e}")
            return False

    def agregar_columna_observaciones(self):
        """Agrega la columna observaciones a la tabla existente"""
        try:
            query = "ALTER TABLE treprod ADD COLUMN observaciones TEXT"
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Columna 'observaciones' agregada exitosamente")
                return True
            else:
                print("❌ Error al agregar columna 'observaciones'")
                return False
        except Exception as e:
            print(f"❌ Error agregando columna observaciones: {e}")
            return False
    
    def guardar_reproduccion(self):
        """Guarda el nuevo registro de reproducción en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete = self.ui.lineEdit_7.text().strip()
            cargada = self.ui.comboBox_2.currentText().strip()
            tecnica = self.ui.comboBox.currentText().strip()
            cantpartos = self.ui.spinBox.value()
            fservicioactual = self.ui.dateEdit_4.date().toString("yyyy-MM-dd")
            faproxparto = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
            fnuevoservicio = self.ui.dateEdit_3.date().toString("yyyy-MM-dd")
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando registro de reproducción:")
            print(f"   Arete: {arete}")
            print(f"   Cargada: {cargada}")
            print(f"   Técnica: {tecnica}")
            print(f"   Cantidad de partos: {cantpartos}")
            print(f"   Fecha servicio: {fservicioactual}")
            print(f"   Fecha parto: {faproxparto}")
            print(f"   Fecha nuevo servicio: {fnuevoservicio}")
            print(f"   Observaciones: {observaciones}")
            
            # Insertar en la base de datos
            if self.insertar_registro_reproduccion(
                arete=arete,
                cargada=cargada,
                tecnica=tecnica,
                cantpartos=cantpartos,
                fservicioactual=fservicioactual,
                faproxparto=faproxparto,
                fnuevoservicio=fnuevoservicio,
                observaciones=observaciones
            ):
                # ✅ REGISTRAR EN BITÁCORA: Inserción exitosa
                if self.bitacora_controller:
                    datos_reproduccion = f"Arete: {arete}, Técnica: {tecnica}, Cargada: {cargada}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Reproducción",
                        accion="ALTA_REGISTRO_REPRODUCCION",
                        descripcion="Nuevo registro de reproducción agregado",
                        detalles=datos_reproduccion,
                        arete_afectado=arete
                    )
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Registro de reproducción guardado correctamente")
                self.accept()
            else:
                # ✅ REGISTRAR EN BITÁCORA: Error en inserción
                if self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Reproducción",
                        accion="ERROR_INSERTAR_REPRODUCCION",
                        descripcion="Error al intentar agregar registro de reproducción",
                        detalles=f"Arete: {arete}, Técnica: {tecnica}",
                        arete_afectado=arete
                    )
                
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el registro de reproducción")
                
        except Exception as e:
            print(f"❌ Error al guardar registro de reproducción: {e}")
            
            # ✅ REGISTRAR EN BITÁCORA: Excepción
            if self.bitacora_controller:
                self.bitacora_controller.registrar_accion(
                    modulo="Reproducción",
                    accion="EXCEPCION_INSERTAR_REPRODUCCION",
                    descripcion="Excepción al guardar registro de reproducción",
                    detalles=f"Error: {str(e)}",
                    arete_afectado=self.ui.lineEdit_7.text().strip()
                )
            
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def insertar_registro_reproduccion(self, arete, cargada, tecnica, cantpartos, 
                                     fservicioactual, faproxparto, fnuevoservicio, observaciones):
        """Inserta el registro de reproducción en la base de datos"""
        try:
            # Primero verificamos y actualizamos la tabla si es necesario
            if not self.verificar_y_actualizar_tabla():
                print("❌ No se pudo verificar/actualizar la tabla treprod")
                return False
            
            # Insertar en la tabla treprod
            query = """
            INSERT INTO treprod
            (areteanimal, cargada, tecnica, cantpartos, fservicioactual, 
             faproxparto, fnuevoservicio, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (arete, cargada, tecnica, cantpartos, fservicioactual,
                     faproxparto, fnuevoservicio, observaciones)
            
            cursor = self.db.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Registro de reproducción insertado correctamente para arete: {arete}")
                return True
            else:
                print(f"❌ Error al insertar registro de reproducción")
                return False
                
        except Exception as e:
            print(f"❌ Error en insertar_registro_reproduccion: {e}")
            return False
    
    def crear_tabla_reproduccion(self):
        """Crea la tabla treprod si no existe"""
        try:
            query = """
            CREATE TABLE IF NOT EXISTS treprod (
                idreprod INTEGER PRIMARY KEY AUTOINCREMENT,
                areteanimal TEXT NOT NULL,
                cargada TEXT NOT NULL,
                tecnica TEXT NOT NULL,
                cantpartos INTEGER,
                fservicioactual DATE NOT NULL,
                faproxparto DATE,
                fnuevoservicio DATE,
                observaciones TEXT
            )
            """
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Tabla 'treprod' creada exitosamente")
                return True
            else:
                print("❌ Error al crear tabla 'treprod'")
                return False
        except Exception as e:
            print(f"❌ Error creando tabla reproducción: {e}")
            return False


    def _obtener_main_window(self):
        """Obtiene la ventana principal (MainWindow) de la jerarquía de padres"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'cambiar_pagina') and hasattr(parent, 'mostrar_reportes_reproduccion_con_filtro'):
                return parent
            parent = parent.parent()
        return None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit_7.clear()
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.spinBox.setValue(0)
        self.ui.textEdit.clear()
        
        # Restablecer fechas
        self.configurar_fechas()
        
        print("✅ Formulario de reproducción limpiado")

    
    def ver_registros_reproduccion(self):
        """Abre la página de reportes de reproducción con el arete actual filtrado"""
        try:
            arete = self.ui.lineEdit_7.text().strip()
            if not arete:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    "Ingrese un arete para ver sus registros de reproducción"
                )
                return

            print(f"🔍 Abriendo reportes de reproducción para arete: {arete}")
            
            # ✅ USAR LA REFERENCIA DIRECTA EN LUGAR DE BUSCAR EN LA JERARQUÍA
            if self.main_window:
                # Cerrar este diálogo primero
                self.accept()
                # Abrir la página de reportes de reproducción con el arete filtrado
                self.main_window.mostrar_reportes_reproduccion_con_filtro(arete)
            else:
                # Si no hay referencia directa, intentar buscar en la jerarquía
                main_window = self._obtener_main_window()
                if main_window:
                    self.accept()
                    main_window.mostrar_reportes_reproduccion_con_filtro(arete)
                else:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Error", 
                        "No se pudo encontrar la ventana principal."
                    )
                
        except Exception as e:
            print(f"❌ Error al ver registros de reproducción: {e}")
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error al abrir reportes: {str(e)}"
            )