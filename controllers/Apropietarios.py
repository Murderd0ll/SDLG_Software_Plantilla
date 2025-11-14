from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarprop_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarPropietarioController(QtWidgets.QDialog):
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
        self.verificar_widgets()
        
    def verificar_widgets(self):
        """Función temporal para verificar que todos los widgets existen"""
        print("\n🔍 VERIFICANDO WIDGETS PROPIETARIO:")
        widgets = [
            'lineEdit_3', 'lineEdit_5', 'lineEdit_6', 'lineEdit_7', 
            'lineEdit_8', 'lineEdit_9', 'lineEdit_10', 'textEdit',
            'indexbtn2', 'pushButton', 'pushButton_2'
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
        self.ui.pushButton_2.clicked.connect(self.guardar_propietario)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones del QTextEdit"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def limpiar_observaciones(self):
        """Limpia el widget de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            self.ui.textEdit.clear()
    
    def subir_foto(self):
        """Abre un diálogo para seleccionar y cargar una foto"""
        try:
            # Configurar los filtros de archivo
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del propietario", 
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
                
                # Poner el nombre del archivo en lineEdit_4
                self.ui.lineEdit_4.setText(nombre_archivo)
                
                # Cambiar el estilo del botón para indicar que la foto fue cargada
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
            nombre = self.ui.lineEdit_3.text().strip()
            telefono = self.ui.lineEdit_7.text().strip()
            correo = self.ui.lineEdit_5.text().strip()
            
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_3.setFocus()
                return False
                
            if not telefono:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Teléfono es obligatorio")
                self.ui.lineEdit_7.setFocus()
                return False
            
            # Validar formato de correo si se ingresó
            if correo and "@" not in correo:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El formato del correo electrónico no es válido")
                self.ui.lineEdit_5.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def guardar_propietario(self):
        """Guarda el nuevo propietario en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            nombre = self.ui.lineEdit_3.text().strip()
            correo = self.ui.lineEdit_5.text().strip()
            upp = self.ui.lineEdit_6.text().strip()
            telefono = self.ui.lineEdit_7.text().strip()
            direccion = self.ui.lineEdit_8.text().strip()
            psg = self.ui.lineEdit_9.text().strip()
            rfc = self.ui.lineEdit_10.text().strip()
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando propietario: {nombre}")
            print(f"   Teléfono: {telefono}, Correo: {correo}")
            print(f"   RFC: {rfc}, UPP: {upp}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto cargada: {'Sí' if self.foto_data else 'No'}")
            
            # Insertar en la base de datos
            if self.db.insertar_propietario(
                nombre=nombre,
                telefono=telefono,
                correo=correo if correo else None,
                direccion=direccion if direccion else None,
                psg=psg if psg else None,
                upp=upp if upp else None,
                rfc=rfc if rfc else None,
                observaciones=observaciones if observaciones else None,
                foto=self.foto_data  # Incluir la foto como BLOB
            ):
                # ✅ REGISTRAR EN BITÁCORA - AÑADIDO
                if self.bitacora_controller:
                    datos_propietario = f"Nombre: {nombre}, Tel: {telefono}, Correo: {correo}, RFC: {rfc}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Propietarios",
                        accion="INSERTAR",
                        descripcion="Alta de nuevo propietario",
                        detalles=datos_propietario
                    )
                    print("✅ Acción registrada en bitácora")
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Propietario agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el propietario")
                
        except Exception as e:
            print(f"❌ Error al guardar propietario: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario incluyendo la foto"""
        # Limpiar campos de texto
        self.ui.lineEdit_3.clear()  # Nombre
        self.ui.lineEdit_5.clear()  # Correo
        self.ui.lineEdit_6.clear()  # UPP
        self.ui.lineEdit_7.clear()  # Teléfono
        self.ui.lineEdit_8.clear()  # Dirección
        self.ui.lineEdit_9.clear()  # PSG
        self.ui.lineEdit_10.clear() # RFC
        
        # Limpiar observaciones
        self.limpiar_observaciones()
        
        # Limpiar foto
        self.foto_data = None
        self.foto_ruta = None
        self.ui.lineEdit_4.clear()  # Nombre del archivo
        self.ui.indexbtn2.setText("Subir archivo")
        self.ui.indexbtn2.setStyleSheet("")  # Resetear estilo
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        self.limpiar_formulario()
        event.accept()