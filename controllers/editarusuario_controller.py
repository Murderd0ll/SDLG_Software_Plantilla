# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editarusuario_ui import Ui_Dialog
from database import Database
import hashlib

class EditarUsuarioController(QtWidgets.QDialog):
    def __init__(self, id_usuario, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.id_usuario = id_usuario
        self.usuario_original = None
        self.bitacora_controller = bitacora_controller
        
        self.setup_connections()
        self.configurar_combobox()
        self.configurar_placeholders()
        self.cargar_datos_usuario()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.actualizar_usuario)  # Guardar
        
    def configurar_combobox(self):
        """Configura el combobox de roles"""
        try:
            # Limpiar y agregar roles
            self.ui.comboBox.clear()
            roles = ["Administrador", "Empleado"]
            self.ui.comboBox.addItems(roles)
            print("✅ Combobox de roles configurado correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando combobox: {e}")
    
    def configurar_placeholders(self):
        """Configura los placeholders para los campos"""
        try:
            # Placeholder para contraseña
            self.ui.lineEdit_4.setPlaceholderText("Dejar en blanco para mantener la contraseña actual")
            
            # También puedes agregar placeholders para otros campos si quieres
            self.ui.lineEdit.setPlaceholderText("Ingrese el nombre de usuario")
            self.ui.lineEdit_2.setPlaceholderText("Ingrese el nombre completo")
            self.ui.lineEdit_3.setPlaceholderText("Ingrese el número telefónico")
            
            # Opcional: Cambiar el estilo del placeholder de contraseña para que sea más visible
            self.ui.lineEdit_4.setStyleSheet("""
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border-color: #3498db;
                }
            """)
            
            print("✅ Placeholders configurados correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando placeholders: {e}")
    
    def cargar_datos_usuario(self):
        """Carga los datos del usuario a editar"""
        try:
            print(f"🔄 Cargando datos del usuario ID: {self.id_usuario}")
            
            # Obtener datos del usuario desde la base de datos
            usuarios = self.db.obtener_usuarios()
            usuario_encontrado = None
            
            for usuario in usuarios:
                if usuario[0] == int(self.id_usuario):
                    usuario_encontrado = usuario
                    break
            
            if usuario_encontrado:
                # [idusuario, usuario, nombre, telefono, rol]
                self.usuario_original = usuario_encontrado[1]  # Guardar usuario original para validaciones
                
                # Llenar los campos con los datos actuales
                self.ui.lineEdit.setText(usuario_encontrado[1])  # Usuario
                self.ui.lineEdit_2.setText(usuario_encontrado[2])  # Nombre
                self.ui.lineEdit_3.setText(usuario_encontrado[3])  # Teléfono
                
                # Establecer el rol en el combobox
                rol_index = self.ui.comboBox.findText(usuario_encontrado[4])
                if rol_index >= 0:
                    self.ui.comboBox.setCurrentIndex(rol_index)
                
                # La contraseña se deja en blanco por seguridad, pero con placeholder
                self.ui.lineEdit_4.clear()
                
                print(f"✅ Datos cargados para usuario: {usuario_encontrado[1]}")
            else:
                print(f"❌ No se encontró usuario con ID: {self.id_usuario}")
                QtWidgets.QMessageBox.warning(self, "Error", "No se encontró el usuario a editar")
                self.reject()
                
        except Exception as e:
            print(f"❌ Error cargando datos del usuario: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
            self.reject()
    
    def encriptar_contrasena(self, contrasena):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(contrasena.encode()).hexdigest()
    
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
            
            # Validar formato de teléfono (solo números)
            if not telefono.isdigit():
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Teléfono inválido", 
                    "El teléfono debe contener solo números"
                )
                self.ui.lineEdit_3.setFocus()
                return False
            
            # Verificar si el usuario ya existe (solo si cambió el nombre de usuario)
            if usuario != self.usuario_original:
                usuario_existente = self.db.obtener_usuario_por_nombre(usuario)
                if usuario_existente:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Usuario duplicado", 
                        f"Ya existe un usuario con el nombre: {usuario}"
                    )
                    self.ui.lineEdit.setFocus()
                    return False
            
            # Si se ingresó una nueva contraseña, validar longitud
            if contrasena and len(contrasena) < 6:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Contraseña muy corta", 
                    "La contraseña debe tener al menos 6 caracteres"
                )
                self.ui.lineEdit_4.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error en validación: {str(e)}")
            return False
    
    def actualizar_usuario(self):
        """Actualiza el usuario en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            usuario = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            telefono = self.ui.lineEdit_3.text().strip()
            contrasena_plana = self.ui.lineEdit_4.text().strip()
            rol = self.ui.comboBox.currentText()
            
            print(f"📝 Actualizando usuario ID: {self.id_usuario}")
            print(f"   Nuevos datos - Usuario: {usuario}, Nombre: {nombre}")
            print(f"   Teléfono: {telefono}, Rol: {rol}")
            
            # Determinar si se actualiza la contraseña
            if contrasena_plana:
                contrasena_encriptada = self.encriptar_contrasena(contrasena_plana)
                print("   🔑 Contraseña: Se actualizará")
            else:
                contrasena_encriptada = None
                print("   🔑 Contraseña: Se mantendrá la actual")
            
            # Actualizar en la base de datos
            if self.actualizar_usuario_en_bd(usuario, nombre, telefono, contrasena_encriptada, rol):
                # ✅ REGISTRAR EN BITÁCORA - AÑADIDO
                if self.bitacora_controller:
                    cambios = f"ID: {self.id_usuario}, Usuario: {usuario}, Nombre: {nombre}, Tel: {telefono}, Rol: {rol}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Usuarios",
                        accion="ACTUALIZAR",
                        descripcion="Actualización de datos de usuario",
                        detalles=cambios
                    )
                    print("✅ Actualización registrada en bitácora")
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el usuario")
                
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def actualizar_usuario_en_bd(self, usuario, nombre, telefono, contrasena, rol):
        """Actualiza el usuario en la base de datos"""
        try:
            if contrasena:
                # Actualizar incluyendo contraseña
                query = """
                UPDATE tusuarios 
                SET usuario = ?, nombre = ?, telefono = ?, pass = ?, rol = ?
                WHERE idusuario = ?
                """
                params = (usuario, nombre, telefono, contrasena, rol, self.id_usuario)
            else:
                # Actualizar sin cambiar contraseña
                query = """
                UPDATE tusuarios 
                SET usuario = ?, nombre = ?, telefono = ?, rol = ?
                WHERE idusuario = ?
                """
                params = (usuario, nombre, telefono, rol, self.id_usuario)
            
            cursor = self.db.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Usuario actualizado correctamente: {nombre} - {usuario}")
                return True
            else:
                print(f"❌ Error al actualizar usuario: {nombre} - {usuario}")
                return False
                
        except Exception as e:
            print(f"❌ Error en actualizar_usuario_en_bd: {e}")
            return False
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.comboBox.setCurrentIndex(0)