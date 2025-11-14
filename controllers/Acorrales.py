# Acorrales.py - VERSIÓN CON BITÁCORA
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarcorral_ui import Ui_Dialog
from database import Database
import uuid

class AgregarCorralController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        self.setup_connections()
        self.configurar_widgets()
        self.verificar_widgets()
        
    def verificar_widgets(self):
        """Función temporal para verificar que todos los widgets existen"""
        print("\n🔍 VERIFICANDO WIDGETS CORRAL:")
        widgets = [
            'lineEdit_2', 'lineEdit_3', 'spinBox', 'spinBox_2', 
            'comboBox_4', 'dateEdit', 'textEdit', 'pushButton', 'pushButton_2'
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
        self.ui.pushButton_2.clicked.connect(self.guardar_corral)  # Guardar
        
    def configurar_widgets(self):
        """Configura los widgets con valores por defecto"""
        # Configurar fecha actual
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)
        
        # Configurar spinboxes
        self.ui.spinBox.setMinimum(0)
        self.ui.spinBox.setMaximum(1000)
        self.ui.spinBox.setValue(0)
        
        self.ui.spinBox_2.setMinimum(1)
        self.ui.spinBox_2.setMaximum(1000)
        self.ui.spinBox_2.setValue(10)
        
        # Configurar combobox de condición
        self.configurar_combobox_condicion()
        
    def configurar_combobox_condicion(self):
        """Configura el combobox con las opciones de condición"""
        condiciones = [
            "Excelente",
            "Buena", 
            "Regular",
            "Mala",
            "En reparación",
            "Deshabilitado"
        ]
        
        self.ui.comboBox_4.clear()
        self.ui.comboBox_4.addItems(condiciones)
        self.ui.comboBox_4.setCurrentIndex(0)
        
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones del QTextEdit"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def limpiar_observaciones(self):
        """Limpia el widget de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            self.ui.textEdit.clear()
    
    def generar_identificador_unico(self):
        """Genera un identificador único para el corral"""
        identificador = f"CORRAL_{uuid.uuid4().hex[:8].upper()}"
        return identificador
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            nombre = self.ui.lineEdit_2.text().strip()
            ubicacion = self.ui.lineEdit_3.text().strip()
            capacidad_actual = self.ui.spinBox.value()
            capacidad_maxima = self.ui.spinBox_2.value()
            
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            if not ubicacion:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Ubicación es obligatorio")
                self.ui.lineEdit_3.setFocus()
                return False
                
            if capacidad_actual < 0:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "La capacidad actual no puede ser negativa")
                self.ui.spinBox.setFocus()
                return False
                
            if capacidad_maxima <= 0:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "La capacidad máxima debe ser mayor a 0")
                self.ui.spinBox_2.setFocus()
                return False
                
            if capacidad_actual > capacidad_maxima:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    "La capacidad actual no puede ser mayor que la capacidad máxima"
                )
                self.ui.spinBox.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def guardar_corral(self):
        """Guarda el nuevo corral en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            nombre = self.ui.lineEdit_2.text().strip()
            ubicacion = self.ui.lineEdit_3.text().strip()
            capacidad_actual = self.ui.spinBox.value()
            capacidad_maxima = self.ui.spinBox_2.value()
            condicion = self.ui.comboBox_4.currentText()
            fecha_mantenimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            # Generar identificador único
            identificador = self.generar_identificador_unico()
            
            print(f"📝 Guardando corral: {nombre}")
            print(f"   Identificador: {identificador}")
            print(f"   Ubicación: {ubicacion}")
            print(f"   Capacidad: {capacidad_actual}/{capacidad_maxima}")
            print(f"   Condición: {condicion}")
            print(f"   Fecha mantenimiento: {fecha_mantenimiento}")
            print(f"   Observaciones: {observaciones}")
            
            # Verificar si ya existe un corral con el mismo identificador
            if self.db.existe_corral_por_id(identificador):
                identificador = self.generar_identificador_unico()
                print(f"🔄 Identificador ya existía, nuevo: {identificador}")
            
            # Insertar en la base de datos
            if self.db.insertar_corral(
                identificador=identificador,
                nombre=nombre,
                ubicacion=ubicacion,
                capacidad_maxima=str(capacidad_maxima),
                capacidad_actual=str(capacidad_actual),
                fecha_mantenimiento=fecha_mantenimiento,
                condicion=condicion,
                observaciones=observaciones if observaciones else None
            ):
                # ✅ REGISTRAR EN BITÁCORA - AÑADIDO
                if self.bitacora_controller:
                    datos_corral = f"ID: {identificador}, Nombre: {nombre}, Ubicación: {ubicacion}, Capacidad: {capacidad_actual}/{capacidad_maxima}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Corrales",
                        accion="INSERTAR",
                        descripcion="Alta de nuevo corral",
                        detalles=datos_corral
                    )
                    print("✅ Acción registrada en bitácora")
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Corral agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el corral")
                
        except Exception as e:
            print(f"❌ Error al guardar corral: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.spinBox.setValue(0)
        self.ui.spinBox_2.setValue(10)
        self.ui.comboBox_4.setCurrentIndex(0)
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)
        self.limpiar_observaciones()
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        self.limpiar_formulario()
        event.accept()