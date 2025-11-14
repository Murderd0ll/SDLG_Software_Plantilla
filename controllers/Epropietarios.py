from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editarprop_ui import Ui_Dialog  # Asegúrate de que este es el nombre correcto
from database import Database
import os
from pathlib import Path

class EditarPropietarioController(QtWidgets.QDialog):
    def __init__(self, propietario_data=None, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        # Datos originales del propietario
        self.propietario_original = propietario_data
        
        self.setup_connections()
        self.cargar_datos_propietario()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_cambios)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def cargar_datos_propietario(self):
        """Carga los datos del propietario en el formulario"""
        if not self.propietario_original:
            print("❌ No hay datos de propietario para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del propietario: {self.propietario_original}")
            
            # Campos básicos - Ajusta estos nombres según tu UI real
            self.ui.lineEdit.setText(self.propietario_original.get('nombre', ''))
            self.ui.lineEdit_5.setText(self.propietario_original.get('correo', ''))
            self.ui.lineEdit_3.setText(self.propietario_original.get('upp', ''))
            self.ui.lineEdit_2.setText(self.propietario_original.get('telefono', ''))
            self.ui.lineEdit_6.setText(self.propietario_original.get('direccion', ''))
            self.ui.lineEdit_7.setText(self.propietario_original.get('psg', ''))
            self.ui.lineEdit_8.setText(self.propietario_original.get('rfc', ''))  # ✅ RFC
            
            # Observaciones
            observaciones = self.propietario_original.get('observaciones', '')
            if hasattr(self.ui, 'textEdit'):
                self.ui.textEdit.setPlainText(observaciones if observaciones else '')
            
            # Foto - cargar si existe
            foto_data = self.propietario_original.get('foto')
            if foto_data:
                self.foto_data = foto_data
                if hasattr(self.ui, 'indexbtn2'):
                    self.ui.indexbtn2.setText("✓ Foto Cargada")
                    self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                print("✅ Foto del propietario cargada desde BD")
            
            print("🎉 Datos del propietario cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del propietario: {e}")
            import traceback
            traceback.print_exc()
    
    def subir_foto(self):
        """Abre un diálogo para seleccionar y cargar una foto"""
        try:
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del propietario", 
                "", 
                filtros
            )
            
            if ruta_archivo:
                tamaño_archivo = os.path.getsize(ruta_archivo)
                if tamaño_archivo > 5 * 1024 * 1024:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Archivo muy grande", 
                        "La imagen no puede ser mayor a 5MB"
                    )
                    return
                
                with open(ruta_archivo, 'rb') as archivo:
                    self.foto_data = archivo.read()
                    self.foto_ruta = ruta_archivo
                
                nombre_archivo = Path(ruta_archivo).name
                
                # Actualizar la interfaz
                if hasattr(self.ui, 'lineEdit_4'):
                    self.ui.lineEdit_4.setText(nombre_archivo)
                
                if hasattr(self.ui, 'indexbtn2'):
                    self.ui.indexbtn2.setText("✓ Foto Cargada")
                    self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                
                print(f"✅ Foto cargada: {nombre_archivo}")
                
        except Exception as e:
            print(f"❌ Error al subir foto: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo cargar la foto: {str(e)}"
            )
    
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            nombre = self.ui.lineEdit.text().strip()
            telefono = self.ui.lineEdit_2.text().strip()
            correo = self.ui.lineEdit_5.text().strip()
            rfc = self.ui.lineEdit_8.text().strip()  # ✅ Validar RFC
            
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not telefono:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Teléfono es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
            
            # Validar formato de correo si se ingresó
            if correo and '@' not in correo:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El formato del correo electrónico no es válido")
                self.ui.lineEdit_5.setFocus()
                return False
            
            # Validar RFC si se ingresó (opcional)
            if rfc and len(rfc) < 12:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El RFC debe tener al menos 12 caracteres")
                self.ui.lineEdit_8.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def guardar_cambios(self):
        """Guarda los cambios del propietario en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            id_original = self.propietario_original.get('id')
            nombre = self.ui.lineEdit.text().strip()
            correo = self.ui.lineEdit_5.text().strip()
            upp = self.ui.lineEdit_3.text().strip()
            telefono = self.ui.lineEdit_2.text().strip()
            direccion = self.ui.lineEdit_6.text().strip()
            psg = self.ui.lineEdit_7.text().strip()
            rfc = self.ui.lineEdit_8.text().strip()  # ✅ RFC
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando cambios del propietario: {nombre}")
            print(f"   ID original: {id_original}")
            print(f"   Teléfono: {telefono}, Correo: {correo}")
            print(f"   RFC: {rfc}, UPP: {upp}")  # ✅ Mostrar RFC
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto actualizada: {'Sí' if self.foto_data else 'No'}")
            
            # Actualizar en la base de datos
            if self.db.actualizar_propietario(
                id_propietario=id_original,
                nombre=nombre,
                telefono=telefono,
                correo=correo if correo else None,
                direccion=direccion if direccion else None,
                psg=psg if psg else None,
                upp=upp if upp else None,
                rfc=rfc if rfc else None,  # ✅ Incluir RFC
                observaciones=observaciones if observaciones else None,
                foto=self.foto_data  # Incluir la foto como BLOB
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Propietario actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el propietario")
                
        except Exception as e:
            print(f"❌ Error al actualizar propietario: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def get_datos_actualizados(self):
        """Retorna los datos actualizados del propietario"""
        return {
            'nombre': self.ui.lineEdit.text().strip(),
            'correo': self.ui.lineEdit_5.text().strip(),
            'upp': self.ui.lineEdit_3.text().strip(),
            'telefono': self.ui.lineEdit_2.text().strip(),
            'direccion': self.ui.lineEdit_6.text().strip(),
            'psg': self.ui.lineEdit_7.text().strip(),
            'rfc': self.ui.lineEdit_8.text().strip(),  
            'observaciones': self.obtener_texto_observaciones(),
            'foto': self.foto_data
        }