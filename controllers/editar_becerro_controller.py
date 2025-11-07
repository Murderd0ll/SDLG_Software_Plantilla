from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editarbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class EditarBecerroController(QtWidgets.QDialog):
    def __init__(self, becerro_data=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        self.becerro_original = becerro_data  # Datos originales del becerro
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.cargar_datos_becerro()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_cambios)  # Guardar
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
            
            # 1. SEXO - Valores fijos
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - De BD o valores por defecto
            self.ui.comboBox_6.clear()
            estatus = self.db.obtener_estatus_becerros()
            if not estatus:
                estatus = ["Activo", "Enfermo", "Vendido", "Muerto"]
                print("📋 Usando estatus por defecto")
            self.ui.comboBox_6.addItems(estatus)
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
            
            print("🎉 Todos los combobox cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar combobox: {e}")
            import traceback
            traceback.print_exc()
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
            self.ui.comboBox_5.addItem("Sin madre registrada")
            
            print("🆘 Valores mínimos cargados por error")
        except Exception as e:
            print(f"💥 Error incluso cargando valores mínimos: {e}")
    
    def cargar_datos_becerro(self):
        """Carga los datos del becerro en el formulario"""
        if not self.becerro_original:
            print("❌ No hay datos de becerro para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del becerro: {self.becerro_original}")
            
            # Campos básicos
            self.ui.lineEdit_4.setText(self.becerro_original.get('arete', ''))  # Arete (posiblemente readonly)
            self.ui.lineEdit.setText(self.becerro_original.get('arete', ''))    # Arete editable
            self.ui.lineEdit_2.setText(self.becerro_original.get('nombre', ''))
            self.ui.doubleSpinBox.setValue(self.becerro_original.get('peso', 0.0))
            
            # Combobox - establecer valores
            sexo = self.becerro_original.get('sexo', 'Macho')
            index_sexo = self.ui.comboBox_2.findText(sexo)
            if index_sexo >= 0:
                self.ui.comboBox_2.setCurrentIndex(index_sexo)
            
            raza = self.becerro_original.get('raza', '')
            index_raza = self.ui.comboBox_3.findText(raza)
            if index_raza >= 0:
                self.ui.comboBox_3.setCurrentIndex(index_raza)
            else:
                self.ui.comboBox_3.setEditText(raza)
            
            corral = self.becerro_original.get('corral', '')
            index_corral = self.ui.comboBox.findText(corral)
            if index_corral >= 0:
                self.ui.comboBox.setCurrentIndex(index_corral)
            else:
                self.ui.comboBox.setEditText(corral)
            
            estatus = self.becerro_original.get('estatus', 'Activo')
            index_estatus = self.ui.comboBox_6.findText(estatus)
            if index_estatus >= 0:
                self.ui.comboBox_6.setCurrentIndex(index_estatus)
            
            arete_madre = self.becerro_original.get('aretemadre', '')
            if arete_madre:
                index_madre = self.ui.comboBox_5.findText(arete_madre)
                if index_madre >= 0:
                    self.ui.comboBox_5.setCurrentIndex(index_madre)
                else:
                    self.ui.comboBox_5.setEditText(arete_madre)
            
            # Fecha de nacimiento
            fecha_nacimiento = self.becerro_original.get('nacimiento')
            if fecha_nacimiento:
                try:
                    if isinstance(fecha_nacimiento, str):
                        qdate = QtCore.QDate.fromString(fecha_nacimiento, "yyyy-MM-dd")
                    else:
                        qdate = QtCore.QDate(fecha_nacimiento)
                    self.ui.dateEdit.setDate(qdate)
                except:
                    # Si hay error con la fecha, usar fecha actual
                    self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
            
            # Arete padre
            arete_padre = self.becerro_original.get('aretepadre', '')
            self.ui.lineEdit_5.setText(arete_padre if arete_padre else '')
            
            # Observaciones
            observaciones = self.becerro_original.get('observacion', '')
            self.ui.lineEdit_3.setText(observaciones if observaciones else '')
            
            # Foto - cargar si existe
            foto_data = self.becerro_original.get('foto')
            if foto_data:
                self.foto_data = foto_data
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                print("✅ Foto del becerro cargada desde BD")
            
            print("🎉 Datos del becerro cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del becerro: {e}")
            import traceback
            traceback.print_exc()
    
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
                
                # Actualizar la interfaz
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
    
    def guardar_cambios(self):
        """Guarda los cambios del becerro en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete_original = self.becerro_original.get('arete')
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            sexo = self.ui.comboBox_2.currentText()
            raza = self.ui.comboBox_3.currentText().strip()
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            corral = self.ui.comboBox.currentText().strip()
            estatus = self.ui.comboBox_6.currentText()
            arete_madre = self.ui.comboBox_5.currentText().strip()
            arete_padre = self.ui.lineEdit_5.text().strip()
            observaciones = self.ui.lineEdit_3.text().strip()
            
            # Si arete_madre es el valor por defecto, guardar como None
            if arete_madre == "Sin madre registrada" or arete_madre == "Sin madre":
                arete_madre = None
            
            print(f"📝 Guardando cambios del becerro: {nombre}, Arete: {arete}")
            print(f"   Arete original: {arete_original}")
            print(f"   Sexo: {sexo}, Estatus: {estatus}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto actualizada: {'Sí' if self.foto_data else 'No'}")
            
            # Actualizar en la base de datos
            if self.db.actualizar_becerro(
                arete_original=arete_original,
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
                foto=self.foto_data  # Incluir la foto como BLOB (puede ser None)
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Becerro actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el becerro")
                
        except Exception as e:
            print(f"❌ Error al actualizar becerro: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def get_datos_actualizados(self):
        """Retorna los datos actualizados del becerro"""
        return {
            'arete': self.ui.lineEdit.text().strip(),
            'nombre': self.ui.lineEdit_2.text().strip(),
            'peso': self.ui.doubleSpinBox.value(),
            'sexo': self.ui.comboBox_2.currentText(),
            'raza': self.ui.comboBox_3.currentText().strip(),
            'nacimiento': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            'corral': self.ui.comboBox.currentText().strip(),
            'estatus': self.ui.comboBox_6.currentText(),
            'aretemadre': self.ui.comboBox_5.currentText().strip(),
            'aretepadre': self.ui.lineEdit_5.text().strip(),
            'observacion': self.ui.lineEdit_3.text().strip(),
            'foto': self.foto_data
        }