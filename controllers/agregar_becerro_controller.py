from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarBecerroController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.verificar_widgets()  # Para debug
        
        # Diagnóstico inmediato de bitácora
        self.diagnostico_bitacora_avanzado()
        
    def verificar_widgets(self):
        """Función temporal para verificar que todos los widgets existen"""
        print("\n🔍 VERIFICANDO WIDGETS:")
        widgets = [
            'lineEdit', 'lineEdit_2', 'lineEdit_4', 
            'textEdit', 'plainTextEdit', 'observacionTextEdit'  # Posibles nombres para observaciones
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
        self.ui.pushButton_2.clicked.connect(self.guardar_becerro)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables"""
        # Combobox editables
        self.ui.comboBox_3.setEditable(True)  # Raza
        self.ui.comboBox.setEditable(True)    # Corral
        self.ui.comboBox_5.setEditable(True)  # Arete madre
        
        # Combobox no editables
        self.ui.comboBox_2.setEditable(False)  # Sexo (solo opciones fijas)
        self.ui.comboBox_6.setEditable(False)  # Estatus (datos de BD pero no editable)
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos en combobox...")
            
            # 1. SEXO - Valores fijos (SIEMPRE debe funcionar)
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            self.ui.comboBox_2.setCurrentIndex(0)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - De BD o valores por defecto
            self.ui.comboBox_6.clear()
            estatus = self.db.obtener_estatus_becerros()
            if not estatus:
                estatus = ["Activo", "Enfermo", "Vendido", "Muerto"]
                print("📋 Usando estatus por defecto")
            self.ui.comboBox_6.addItems(estatus)
            self.ui.comboBox_6.setCurrentIndex(0)
            print(f"✅ Estatus cargados: {estatus}")
            
            # 3. CORRALES - De BD
            corrales_data = self.db.obtener_corrales()
            self.ui.comboBox.clear()
            if corrales_data:
                corrales = [str(corral[1]) for corral in corrales_data]
                self.ui.comboBox.addItems(corrales)
                print(f"✅ Corrales cargados: {len(corrales)}")
            else:
                self.ui.comboBox.addItems(["Corral 1", "Corral 2", "Corral 3"])
                print("📋 Usando corrales por defecto")
            
            # 4. RAZAS - De BD
            razas = self.db.obtener_razas_becerros()
            self.ui.comboBox_3.clear()
            if razas:
                self.ui.comboBox_3.addItems(razas)
                print(f"✅ Razas cargadas: {len(razas)}")
            else:
                razas_default = ["Angus", "Hereford", "Charolais", "Brahman"]
                self.ui.comboBox_3.addItems(razas_default)
                print("📋 Usando razas por defecto")
            
            # 5. ARETE MADRE - De BD
            aretes_madres = self.db.obtener_aretes_madres()
            self.ui.comboBox_5.clear()
            if aretes_madres:
                self.ui.comboBox_5.addItems(aretes_madres)
                print(f"✅ Arete madres cargados: {len(aretes_madres)}")
            else:
                self.ui.comboBox_5.addItem("Sin madre registrada")
                print("📋 Usando arete madre por defecto")
            
            # Configurar fecha actual
            fecha_actual = QtCore.QDate.currentDate()
            self.ui.dateEdit.setDate(fecha_actual)
            
            print("🎉 Todos los combobox cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar combobox: {e}")
            import traceback
            traceback.print_exc()
            
            # Cargar valores mínimos por si hay error
            self.cargar_valores_minimos()
    
    def cargar_valores_minimos(self):
        """Carga valores mínimos en caso de error"""
        try:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(["Macho", "Hembra"])
            
            self.ui.comboBox_6.clear()
            self.ui.comboBox_6.addItems(["Activo", "Enfermo"])
            
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["Corral 1"])
            
            self.ui.comboBox_3.clear()
            self.ui.comboBox_3.addItems(["Angus"])
            
            self.ui.comboBox_5.clear()
            self.ui.comboBox_5.addItem("Sin madre")
            
            print("🆘 Valores mínimos cargados por error")
        except Exception as e:
            print(f"💥 Error incluso cargando valores mínimos: {e}")
    
    def obtener_widget_observaciones(self):
        """Obtiene el widget de observaciones (puede ser QTextEdit o QLineEdit)"""
        # Prueba diferentes nombres posibles
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit
        elif hasattr(self.ui, 'plainTextEdit'):
            return self.ui.plainTextEdit
        elif hasattr(self.ui, 'observacionTextEdit'):
            return self.ui.observacionTextEdit
        elif hasattr(self.ui, 'lineEdit_3'):
            return self.ui.lineEdit_3
        else:
            print("⚠️ No se encontró widget de observaciones")
            return None
    
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones según el tipo de widget"""
        widget = self.obtener_widget_observaciones()
        if widget:
            if isinstance(widget, QtWidgets.QTextEdit):
                return widget.toPlainText().strip()
            elif isinstance(widget, QtWidgets.QPlainTextEdit):
                return widget.toPlainText().strip()
            elif isinstance(widget, QtWidgets.QLineEdit):
                return widget.text().strip()
        return ""
    
    def limpiar_observaciones(self):
        """Limpia el widget de observaciones"""
        widget = self.obtener_widget_observaciones()
        if widget:
            if isinstance(widget, QtWidgets.QTextEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QPlainTextEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
    
    def subir_foto(self):
        """Abre un diálogo para seleccionar y cargar una foto"""
        try:
            # Configurar los filtros de archivo
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del becerro", 
                "", 
                filtros
            )
            
            if ruta_archivo:
                # Verificar tamaño del archivo (máximo 5MB)
                tamaño_archivo = os.path.getsize(ruta_archivo)
                if tamaño_archivo > 5 * 1024 * 1024:  # 5MB en bytes
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Archivo muy grande", 
                        "La imagen no puede ser mayor a 5MB"
                    )
                    return
                
                # Leer el archivo como bytes
                with open(ruta_archivo, 'rb') as archivo:
                    self.foto_data = archivo.read()
                    self.foto_ruta = ruta_archivo
                
                # Mostrar información al usuario
                nombre_archivo = Path(ruta_archivo).name
                tamaño_kb = tamaño_archivo / 1024
                
                # MODIFICACIÓN: Poner el nombre del archivo en lineEdit_2 en lugar del botón
                self.ui.lineEdit_4.setText(nombre_archivo)
                
                # Opcional: También puedes mantener el botón con un indicador de que la foto fue cargada
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                
                print(f"✅ Foto cargada: {nombre_archivo} ({tamaño_kb:.1f} KB)")
                
        except Exception as e:
            print(f"❌ Error al subir foto: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo cargar la foto: {str(e)}"
            )
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            if peso <= 0:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso debe ser mayor a 0")
                self.ui.doubleSpinBox.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False

    def diagnostico_bitacora_avanzado(self):
        """Diagnóstico avanzado del controlador de bitácora"""
        try:
            print("\n🔍 DIAGNÓSTICO AVANZADO BITÁCORA:")
            print(f"✅ Controlador de bitácora presente: {self.bitacora_controller is not None}")
            
            if self.bitacora_controller:
                print(f"✅ Tipo: {type(self.bitacora_controller)}")
                print(f"✅ Usuario actual: {getattr(self.bitacora_controller, 'usuario_actual', 'NO TIENE')}")
                
                # Verificar métodos disponibles
                metodos = ['registrar_accion', 'registrar_alta_becerro']
                for metodo in metodos:
                    if hasattr(self.bitacora_controller, metodo):
                        print(f"✅ Método {metodo}: DISPONIBLE")
                    else:
                        print(f"❌ Método {metodo}: NO DISPONIBLE")
                
                # Probar registro directo
                print("🧪 Probando registro directo...")
                resultado = self.bitacora_controller.registrar_accion(
                    modulo="Becerros",
                    accion="PRUEBA_DIAGNOSTICO",
                    descripcion="Prueba de diagnóstico desde AgregarBecerro",
                    detalles="Este es un registro de prueba",
                    arete_afectado="TEST_123"
                )
                print(f"✅ Resultado prueba: {resultado}")
                
            else:
                print("❌ NO hay controlador de bitácora")
                print("💡 Posibles causas:")
                print("   - No se pasó al crear el diálogo")
                print("   - El controlador padre no tiene bitácora")
                print("   - Hay un error en la inicialización")
                
        except Exception as e:
            print(f"❌ Error en diagnóstico avanzado: {e}")

    def registrar_accion_bitacora_completo(self, arete, nombre, peso, sexo, raza, corral):
        """Intentar registrar la acción en bitácora de múltiples formas"""
        try:
            if not self.bitacora_controller:
                print("❌ No hay controlador de bitácora para registrar")
                return False
            
            datos_becerro = f"Nombre: {nombre}, Arete: {arete}, Peso: {peso}kg, Sexo: {sexo}, Raza: {raza}, Corral: {corral}"
            
            # MÉTODO 1: Usar el método específico
            print("🔄 Intentando registro con método específico...")

            resultado = self.bitacora_controller.registrar_accion(
                modulo="Becerros",
                accion="ALTA",
                descripcion=f"Alta de nuevo becerro: {nombre}",
                detalles=datos_becerro,
                arete_afectado=arete
            )

            print(f"✅ Resultado registro bitácora: {resultado}")

            self.verificar_ultimo_registro_bitacora()
        
            return resultado
        
        except Exception as e:
            print(f"❌ Error crítico registrando en bitácora: {e}")
            import traceback
            traceback.print_exc()
            return False

            

    def verificar_ultimo_registro_bitacora(self):
        """Verificar el último registro en la bitácora directamente"""
        try:
            if not self.bitacora_controller:
                return
                
            # Obtener registros recientes
            from datetime import datetime, timedelta
            fecha_hasta = datetime.now().strftime('%Y-%m-%d')
            fecha_desde = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            registros = self.bitacora_controller.obtener_registros_bitacora(fecha_desde, fecha_hasta)
            
            print(f"📊 Últimos 3 registros en bitácora:")
            for i, registro in enumerate(registros[:3]):
                fecha, usuario, modulo, accion, descripcion, detalles, arete = registro
                print(f"   {i+1}. {fecha} - {modulo} - {accion} - {descripcion}")
                
        except Exception as e:
            print(f"❌ Error verificando últimos registros: {e}")
    
    def guardar_becerro(self):
        """Guarda el nuevo becerro en la base de datos - CON BITÁCORA"""
        try:
            print("🔄 Iniciando proceso de guardado de becerro...")
            
            if not self.validar_datos():
                print("❌ Validación de datos fallida")
                return False
                
            # Obtener datos del formulario
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            sexo = self.ui.comboBox_2.currentText()
            raza = self.ui.comboBox_3.currentText().strip()
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            corral = self.ui.comboBox.currentText().strip()
            estatus = self.ui.comboBox_6.currentText()
            arete_madre = self.ui.comboBox_5.currentText().strip()
            observaciones = self.obtener_texto_observaciones()
            
            if arete_madre == "Sin madre registrada" or arete_madre == "Sin madre":
                arete_madre = None
            
            print(f"📝 Intentando guardar becerro: {nombre} (Arete: {arete})")
            
            # Insertar en la base de datos
            resultado = self.db.insertar_becerro(
                arete=arete,
                nombre=nombre,
                peso=peso,
                sexo=sexo,
                raza=raza,
                nacimiento=fecha_nacimiento,
                corral=corral,
                estatus=estatus,
                aretemadre=arete_madre,
                observacion=observaciones if observaciones else None,
                foto=self.foto_data
            )
            
            if resultado:
                print("✅ Becerro insertado correctamente en la base de datos")
                
                # ✅ REGISTRAR EN BITÁCORA - AÑADIDO
                if self.bitacora_controller:
                    datos_becerro = f"Nombre: {nombre}, Arete: {arete}, Peso: {peso}kg, Sexo: {sexo}, Raza: {raza}, Corral: {corral}"
                    resultado_bitacora = self.bitacora_controller.registrar_accion(
                        modulo="Becerros",
                        accion="ALTA",
                        descripcion=f"Alta de nuevo becerro: {nombre}",
                        detalles=datos_becerro,
                        arete_afectado=arete
                    )
                    
                    if resultado_bitacora:
                        print("✅ Acción registrada en bitácora")
                    else:
                        print("❌ Error al registrar en bitácora")
                
                QtWidgets.QMessageBox.information(
                    self, 
                    "Éxito", 
                    f"Becerro '{nombre}' agregado correctamente\nArete: {arete}"
                )
                self.accept()
                return True
                
            else:
                print("❌ Error al insertar becerro en la base de datos")
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error", 
                    "No se pudo guardar el becerro en la base de datos.\n"
                    "Puede que el arete ya exista o haya un problema de conexión."
                )
                return False
                
        except Exception as e:
            print(f"❌ Error crítico al guardar becerro: {e}")
            import traceback
            traceback.print_exc()
            
            QtWidgets.QMessageBox.critical(
                self, 
                "Error Crítico", 
                f"Error inesperado al guardar:\n{str(e)}\n\n"
                "Por favor, contacte al administrador del sistema."
            )
            return False
        
    def registrar_en_bitacora_simple(self, arete, nombre, peso, sexo, raza, corral):
        try:
        # ✅ VERIFICACIÓN DIRECTA como en generar_reporte_pdf
            if not self.bitacora_controller:
               print("⚠️  No hay controlador de bitácora disponible")
               return False
        
        # ✅ DATOS SIMPLES como en generar_reporte_pdf
            datos_becerro = f"Nombre: {nombre}, Arete: {arete}, Peso: {peso}kg, Sexo: {sexo}, Raza: {raza}, Corral: {corral}"
        
        # ✅ LLAMADA DIRECTA como en generar_reporte_pdf
            resultado = self.bitacora_controller.registrar_accion(
            modulo="Becerros",
            accion="ALTA",
            descripcion=f"Agregó becerro: {nombre}",
            detalles=datos_becerro,
            arete_afectado=arete
            )
        
            if resultado:
                print("✅ Registro en bitácora exitoso (método simple)")
            else:
                print("❌ Falló el registro en bitácora")
            
            return resultado
        
        except Exception as e:
            print(f"❌ Error en registro bitácora simple: {e}")
            return False

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario incluyendo la foto"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.doubleSpinBox.setValue(0.0)
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_6.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
        self.ui.lineEdit_4.clear()
        
        # Limpiar observaciones
        self.limpiar_observaciones()
        
        # Limpiar foto
        self.foto_data = None
        self.foto_ruta = None
        self.ui.indexbtn2.setText("Subir archivo")
        self.ui.indexbtn2.setStyleSheet("")  # Resetear estilo
        
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)