from PyQt5 import QtCore, QtGui, QtWidgets
from agregarbecerro_ui import Ui_Dialog
from database import Database

class AgregarBecerroController(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.setup_connections()
        self.cargar_datos_combo()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_becerro)  # Guardar
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox"""
        try:
            # Cargar razas (puedes obtenerlas de la base de datos)
            razas = ["Angus", "Hereford", "Charolais", "Brahman", "Simmental", "Holstein"]
            self.ui.comboBox_3.clear()
            self.ui.comboBox_3.addItems(razas)
            
            # Cargar corrales
            corrales = ["Corral 1", "Corral 2", "Corral 3", "Corral 4"]
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(corrales)
            
            # Cargar estatus
            estatus = ["Activo", "Enfermo", "Vendido", "Muerto"]
            self.ui.comboBox_6.clear()
            self.ui.comboBox_6.addItems(estatus)
            
            # Cargar aretes de madres (puedes obtener de la base de datos)
            aretes_madres = ["M001", "M002", "M003", "M004"]
            self.ui.comboBox_5.clear()
            self.ui.comboBox_5.addItems(aretes_madres)
            
            # Configurar fecha actual
            fecha_actual = QtCore.QDate.currentDate()
            self.ui.dateEdit.setDate(fecha_actual)
            
        except Exception as e:
            print(f"❌ Error al cargar datos en combobox: {e}")
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                return False
                
            if peso <= 0:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso debe ser mayor a 0")
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
            raza = self.ui.comboBox_3.currentText()
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            corral = self.ui.comboBox.currentText()
            estatus = self.ui.comboBox_6.currentText()
            arete_madre = self.ui.comboBox_5.currentText()
            arete_padre = self.ui.lineEdit_4.text().strip()
            observaciones = self.ui.lineEdit_3.text().strip()
            
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
                aretepadre=arete_padre,
                observacion=observaciones
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Becerro agregado correctamente")
                self.accept()  # Cierra el diálogo con resultado positivo
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el becerro")
                
        except Exception as e:
            print(f"❌ Error al guardar becerro: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.doubleSpinBox.setValue(0.0)
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_6.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_3.clear()
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)