# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarreproduccion_ui import Ui_Dialog
from database import Database
from datetime import datetime, timedelta

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
        self.configurar_fechas_no_editables()
        self.verificar_widgets()
        
        # Conectar el cambio de fecha de servicio para recalcular automáticamente
        self.ui.dateEdit_4.dateChanged.connect(self.calcular_fechas)
        
        # Si se proporcionó un arete, establecerlo en el campo correspondiente
        if self.arete_animal:
            self.ui.lineEdit_7.setText(self.arete_animal)
    
    def configurar_fechas_no_editables(self):
        """Configura las fechas de parto y próximo servicio como no editables"""
        # Hacer que los dateEdit de parto y próximo servicio sean de solo lectura
        self.ui.dateEdit_2.setReadOnly(True)
        self.ui.dateEdit_3.setReadOnly(True)
        
        # Cambiar el estilo visual para indicar que son campos calculados automáticamente
        self.ui.dateEdit_2.setStyleSheet("QDateEdit:read-only { background-color: #f0f0f0; color: #666; }")
        self.ui.dateEdit_3.setStyleSheet("QDateEdit:read-only { background-color: #f0f0f0; color: #666; }")
        
        # También podemos deshabilitar el botón del calendario si existe
        self.ui.dateEdit_2.setCalendarPopup(False)
        self.ui.dateEdit_3.setCalendarPopup(False)
        
        print("✅ Fechas calculadas configuradas como no editables")
    
    def calcular_fechas(self):
        """Calcula las fechas de parto y próximo servicio basado en la fecha de servicio"""
        try:
            fecha_servicio = self.ui.dateEdit_4.date()
            
            if not fecha_servicio.isValid():
                return
            
            # Convertir QDate a datetime
            fecha_servicio_dt = datetime(
                fecha_servicio.year(), 
                fecha_servicio.month(), 
                fecha_servicio.day()
            )
            
            print(f"📅 Fecha de servicio: {fecha_servicio_dt}")
            
            # Calcular fecha aproximada de parto (9 meses después)
            fecha_parto = self._calcular_meses(fecha_servicio_dt, 9)
            
            # Calcular fecha de próximo servicio (12 meses después del servicio)
            fecha_nuevo_servicio = self._calcular_meses(fecha_servicio_dt, 12)
            
            # Actualizar los QDateEdit (que ahora son de solo lectura)
            self.ui.dateEdit_2.setDate(QtCore.QDate(
                fecha_parto.year, 
                fecha_parto.month, 
                fecha_parto.day
            ))
            
            self.ui.dateEdit_3.setDate(QtCore.QDate(
                fecha_nuevo_servicio.year, 
                fecha_nuevo_servicio.month, 
                fecha_nuevo_servicio.day
            ))
            
            print(f"✅ Fecha parto calculada: {fecha_parto}")
            print(f"✅ Fecha nuevo servicio calculada: {fecha_nuevo_servicio}")
            
        except Exception as e:
            print(f'❌ Error calculando fechas: {e}')
    
    def _calcular_meses(self, fecha_base, meses):
        """Calcula una nueva fecha sumando meses a una fecha base"""
        # Calcular nuevo año y mes
        nuevo_ano = fecha_base.year + (fecha_base.month + meses - 1) // 12
        nuevo_mes = (fecha_base.month + meses - 1) % 12 + 1
        
        # Ajustar el día si es necesario (para meses con menos días)
        ultimo_dia_mes = self._ultimo_dia_mes(nuevo_ano, nuevo_mes)
        nuevo_dia = min(fecha_base.day, ultimo_dia_mes)
        
        return datetime(nuevo_ano, nuevo_mes, nuevo_dia)
    
    def _ultimo_dia_mes(self, año, mes):
        """Devuelve el último día del mes para un año y mes dados"""
        if mes == 12:
            return 31
        siguiente_mes = datetime(año, mes + 1, 1)
        ultimo_dia_mes_actual = siguiente_mes - timedelta(days=1)
        return ultimo_dia_mes_actual.day

    def configurar_fechas(self):
        """Configura las fechas con valores por defecto usando el cálculo por meses"""
        fecha_actual = QtCore.QDate.currentDate()
        
        # Fecha de servicio actual (hoy) - ESTA SÍ ES EDITABLE
        self.ui.dateEdit_4.setDate(fecha_actual)
        
        # Las fechas de parto y próximo servicio se calcularán automáticamente
        # y serán de solo lectura
        self.calcular_fechas()
        
        print("✅ Fechas de reproducción configuradas con cálculo automático")

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
        print("✅ Combobox de reproducción configurados")
        
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones"""
        try:
            if hasattr(self.ui, 'textEdit'):
                text_edit = self.ui.textEdit
                texto = text_edit.toPlainText()
                print(f"📝 Texto obtenido de textEdit: '{texto}'")
                
                if texto is None:
                    return ""
                return texto.strip()
            else:
                print("❌ textEdit no encontrado en la UI")
                return ""
        except Exception as e:
            print(f"❌ Error obteniendo texto de observaciones: {e}")
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
            
            # Verificar si tiene la columna 'observacion' (SINGULAR)
            cursor = self.db.ejecutar_consulta("PRAGMA table_info(treprod)")
            if cursor:
                columnas = [col[1] for col in cursor.fetchall()]  # [id, areteanimal, cargada, ...]
                print(f"📋 Columnas actuales en treprod: {columnas}")
                
                if 'observacion' not in columnas:  # CAMBIADO A SINGULAR
                    print("🔄 Agregando columna 'observacion' a la tabla existente...")
                    return self.agregar_columna_observacion()  # CAMBIADO A SINGULAR
                else:
                    print("✅ La tabla ya tiene la columna 'observacion'")  # CAMBIADO A SINGULAR
                    return True
            return False
            
        except Exception as e:
            print(f"❌ Error verificando estructura de tabla: {e}")
            return False

    def agregar_columna_observacion(self):  # CAMBIADO A SINGULAR
        """Agrega la columna observacion (SINGULAR) a la tabla existente"""
        try:
            query = "ALTER TABLE treprod ADD COLUMN observacion TEXT"  # CAMBIADO A SINGULAR
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Columna 'observacion' agregada exitosamente")  # CAMBIADO A SINGULAR
                return True
            else:
                print("❌ Error al agregar columna 'observacion'")  # CAMBIADO A SINGULAR
                return False
        except Exception as e:
            print(f"❌ Error agregando columna observacion: {e}")  # CAMBIADO A SINGULAR
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
            print(f"   Observaciones: '{observaciones}'")
            
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
            
            # Asegurarnos de que observaciones no sea None
            if observaciones is None:
                observaciones = ""
            
            print(f"🔍 Insertando en BD - Observaciones: '{observaciones}'")
            
            # Insertar en la tabla treprod - USANDO EL NOMBRE CORRECTO DE LA COLUMNA (observacion)
            query = """
            INSERT INTO treprod
            (areteanimal, cargada, tecnica, cantpartos, fservicioactual, 
             faproxparto, fnuevoservicio, observacion)  -- CAMBIADO A SINGULAR
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (arete, cargada, tecnica, cantpartos, fservicioactual,
                     faproxparto, fnuevoservicio, observaciones)
            
            print(f"🔍 Parámetros para la consulta: {params}")
            
            cursor = self.db.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Registro de reproducción insertado correctamente para arete: {arete}")
                
                # Verificar que realmente se insertó
                self.verificar_insercion(arete)
                return True
            else:
                print(f"❌ Error al insertar registro de reproducción")
                return False
                
        except Exception as e:
            print(f"❌ Error en insertar_registro_reproduccion: {e}")
            return False
    
    def verificar_insercion(self, arete):
        """Verifica que el registro se insertó correctamente"""
        try:
            query = "SELECT * FROM treprod WHERE areteanimal = ? ORDER BY idreprod DESC LIMIT 1"
            cursor = self.db.ejecutar_consulta(query, (arete,))
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    print(f"✅ Registro verificado en BD:")
                    print(f"   ID: {resultado[0]}")
                    print(f"   Arete: {resultado[1]}")
                    # La columna observacion ahora está en la posición 8 (si es la última)
                    print(f"   Observacion: '{resultado[8]}'")  # CAMBIADO A SINGULAR
                else:
                    print("❌ No se encontró el registro insertado")
            else:
                print("❌ Error al verificar la inserción")
        except Exception as e:
            print(f"❌ Error verificando inserción: {e}")
    
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
                observacion TEXT  -- CAMBIADO A SINGULAR
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