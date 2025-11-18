# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarusuario_ui import Ui_Dialog
from database import Database
# ⬇️ Eliminamos la importación de hashlib
# import hashlib

class AgregarUsuarioController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        self.setup_connections()
        self.configurar_combobox()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_usuario)  # Guardar
        
    def configurar_combobox(self):
        """Configura el combobox de roles"""
        try:
            # Limpiar y agregar roles
            self.ui.comboBox.clear()
            roles = ["Administrador", "Empleado"]
            self.ui.comboBox.addItems(roles)
            self.ui.comboBox.setCurrentIndex(0)
            print("✅ Combobox de roles configurado correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando combobox: {e}")

    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            usuario = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            telefono = self.ui.lineEdit_3.text().strip()
            contrasena = self.ui.lineEdit_4.text().strip()
            rol = self.ui.comboBox.currentText()
            
            # Validar campos obligatorios
            if not usuario:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Usuario es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            if not telefono:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Teléfono es obligatorio")
                self.ui.lineEdit_3.setFocus()
                return False
                
            if not contrasena:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Contraseña es obligatorio")
                self.ui.lineEdit_4.setFocus()
                return False
            
            # Validar longitud mínima de contraseña
            if len(contrasena) < 6:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Contraseña muy corta", 
                    "La contraseña debe tener al menos 6 caracteres"
                )
                self.ui.lineEdit_4.setFocus()
                return False
            
            # Validar formato de teléfono (solo números)
            if not telefono.isdigit():
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Teléfono inválido", 
                    "El teléfono debe contener solo números"
                )
                self.ui.lineEdit_3.setFocus()
                return False
            
            # Verificar si el usuario ya existe
            usuario_existente = self.db.obtener_usuario_por_nombre(usuario)
            if usuario_existente:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Usuario duplicado", 
                    f"Ya existe un usuario con el nombre: {usuario}"
                )
                self.ui.lineEdit.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error en validación: {str(e)}")
            return False
    
    def guardar_usuario(self):
        """Guarda el nuevo usuario en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            usuario = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            telefono = self.ui.lineEdit_3.text().strip()
            contrasena_plana = self.ui.lineEdit_4.text().strip()  # ⬅️ Contraseña en texto plano
            rol = self.ui.comboBox.currentText()
            
            # ⬇️ AHORA GUARDAMOS DIRECTAMENTE LA CONTRASEÑA EN TEXTO PLANO
            # (sin encriptación)
            
            print(f"📝 Guardando usuario: {nombre}, Usuario: {usuario}")
            print(f"   Teléfono: {telefono}, Rol: {rol}")
            print(f"   Contraseña (texto plano): {contrasena_plana}")
            
            # Insertar en la base de datos
            if self.db.insertar_usuario(
                usuario=usuario,
                nombre=nombre,
                telefono=telefono,
                contrasena=contrasena_plana,  # ⬅️ Enviamos la contraseña en texto plano
                rol=rol
            ):
                # ✅ REGISTRAR EN BITÁCORA
                if self.bitacora_controller:
                    datos_usuario = f"Usuario: {usuario}, Nombre: {nombre}, Tel: {telefono}, Rol: {rol}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Usuarios",
                        accion="INSERTAR",
                        descripcion="Alta de nuevo usuario",
                        detalles=datos_usuario
                    )
                    print("✅ Acción registrada en bitácora")
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el usuario")
                
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.comboBox.setCurrentIndex(0)