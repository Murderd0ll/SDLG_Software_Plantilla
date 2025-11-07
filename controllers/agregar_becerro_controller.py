from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarBecerroController(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.verificar_widgets()  # Para debug
        
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
    
    def guardar_becerro(self):
        """Guarda el nuevo becerro en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
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
            arete_padre = self.ui.lineEdit_4.text().strip()
            
            # Obtener observaciones del widget correcto
            observaciones = self.obtener_texto_observaciones()
            
            # Si arete_madre es el valor por defecto, guardar como None
            if arete_madre == "Sin madre registrada" or arete_madre == "Sin madre":
                arete_madre = None
            
            print(f"📝 Guardando becerro: {nombre}, Arete: {arete}")
            print(f"   Sexo: {sexo}, Estatus: {estatus}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto cargada: {'Sí' if self.foto_data else 'No'}")
            
            # Insertar en la base de datos
            if self.db.insertar_becerro(
                arete=arete,
                nombre=nombre,
                peso=peso,
                sexo=sexo,
                raza=raza,
                nacimiento=fecha_nacimiento,
                corral=corral,
                estatus=estatus,
                aretemadre=arete_madre,
                aretepadre=arete_padre if arete_padre else None,
                observacion=observaciones if observaciones else None,
                foto=self.foto_data  # Incluir la foto como BLOB
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Becerro agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el becerro")
                
        except Exception as e:
            print(f"❌ Error al guardar becerro: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
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