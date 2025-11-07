# login_controller.py COMPLETO
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from sidebar import MainWindow

class LoginController:
    def __init__(self, login_ui, login_window):
        """
        Controlador completo para la ventana de login
        """
        self.ui = login_ui
        self.login_window = login_window
        self.password_visible = False
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Conectar señales
        self.connect_signals()
        
        print("✅ Controlador de login inicializado")
    
    def setup_ui(self):
        """Configuración inicial de la interfaz"""
        # Establecer el foco en el campo de usuario
        self.ui.lineEditUsuario.setFocus()
        
        # Configurar el campo de contraseña para mostrar asteriscos
        self.ui.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Configurar el botón de mostrar/ocultar contraseña
        self.ui.hide.setCheckable(True)
        self.ui.hide.setChecked(False)
        
        # Aplicar estilo inicial al botón del ojo
        self.actualizar_estilo_ojo()
    
    def connect_signals(self):
        """Conectar todas las señales de la interfaz"""
        try:
            # Botón de login
            self.ui.btnLogin.clicked.connect(self.validar_login)
            
            # Botón de mostrar/ocultar contraseña
            self.ui.hide.clicked.connect(self.toggle_password_visibility)
            
            # Enter en los campos de texto
            self.ui.lineEditUsuario.returnPressed.connect(self.validar_login)
            self.ui.lineEditPassword.returnPressed.connect(self.validar_login)
            
            print("✅ Señales del login conectadas correctamente")
            
        except Exception as e:
            print(f"❌ Error conectando señales: {e}")
            self.mostrar_error("Error", f"Error al conectar funciones: {str(e)}")
    
    def actualizar_estilo_ojo(self):
        """Actualizar el estilo del botón del ojo según su estado"""
        if self.password_visible:
            estilo = """
                QPushButton#hide {
                    background-image: url(":/icons/img/icons/ojont.png");
                    background-repeat: no-repeat;
                    background-position: center center;
                    border: none;
                    background-color: transparent;
                    min-width: 45px;
                    max-width: 45px;
                    min-height: 45px;
                    max-height: 45px;
                }
                QPushButton#hide:hover {
                    background-color: rgba(160, 145, 114, 0.1);
                }
            """
        else:
            estilo = """
                QPushButton#hide {
                    background-image: url(":/icons/img/icons/ojo.png");
                    background-repeat: no-repeat;
                    background-position: center center;
                    border: none;
                    background-color: transparent;
                    min-width: 45px;
                    max-width: 45px;
                    min-height: 45px;
                    max-height: 45px;
                }
                QPushButton#hide:hover {
                    background-color: rgba(160, 145, 114, 0.1);
                }
            """
        self.ui.hide.setStyleSheet(estilo)
    
    def toggle_password_visibility(self):
        """Alternar entre mostrar y ocultar la contraseña"""
        self.password_visible = not self.password_visible
        
        if self.password_visible:
            # Mostrar contraseña
            self.ui.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            # Ocultar contraseña
            self.ui.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Actualizar el icono del ojo
        self.actualizar_estilo_ojo()
        
        print(f"🔐 Visibilidad de contraseña: {'Visible' if self.password_visible else 'Oculta'}")
    
    def validar_login(self):
        """Validar las credenciales del usuario"""
        try:
            # Obtener datos de los campos
            usuario = self.ui.lineEditUsuario.text().strip()
            password = self.ui.lineEditPassword.text().strip()
            
            print(f"🔐 Intentando login - Usuario: '{usuario}', Contraseña: '{password}'")
            
            # Validar campos vacíos
            if not usuario or not password:
                self.mostrar_error("Error de validación", "Por favor, complete todos los campos.")
                return
            
            # Validar credenciales (usuario: admin, contraseña: 1234)
            if usuario == "admin" and password == "1234":
                self.login_exitoso()
            else:
                self.mostrar_error("Credenciales incorrectas", 
                                 "Usuario o contraseña incorrectos.\n\n"
                                 "Credenciales de prueba:\n"
                                 "Usuario: admin\n"
                                 "Contraseña: 1234")
                                 
        except Exception as e:
            print(f"❌ Error en validar_login: {e}")
            self.mostrar_error("Error", f"Error al validar credenciales: {str(e)}")
    
    def login_exitoso(self):
        """Manejar el login exitoso"""
        try:
            print("✅ Login exitoso - Abriendo aplicación principal...")
            
            # Ocultar ventana de login
            self.login_window.hide()
            
            # Crear y mostrar la ventana principal (sidebar)
            self.main_window = MainWindow()
            self.main_window.show()
            
            # Conectar el cierre de la ventana principal para cerrar toda la aplicación
            if hasattr(self.main_window.ui, 'cerrarbtn1'):
                self.main_window.ui.cerrarbtn1.clicked.connect(self.cerrar_aplicacion)
            if hasattr(self.main_window.ui, 'cerrarbtn2'):
                self.main_window.ui.cerrarbtn2.clicked.connect(self.cerrar_aplicacion)
            
            print("✅ Aplicación principal iniciada correctamente")
            
        except Exception as e:
            print(f"❌ Error al abrir la aplicación principal: {e}")
            self.mostrar_error("Error", f"No se pudo iniciar la aplicación: {str(e)}")
            # Mostrar nuevamente la ventana de login
            self.login_window.show()
    
    def mostrar_error(self, titulo, mensaje):
        """Mostrar mensaje de error"""
        QMessageBox.warning(self.login_window, titulo, mensaje)
        
        # Limpiar campos y poner foco según el error
        if "Credenciales incorrectas" in titulo:
            self.ui.lineEditPassword.clear()
            self.ui.lineEditPassword.setFocus()
        else:
            self.ui.lineEditUsuario.setFocus()
    
    def cerrar_aplicacion(self):
        """Cerrar toda la aplicación"""
        print("🔴 Cerrando aplicación desde login controller...")
        
        # Cerrar ventana principal si existe
        if hasattr(self, 'main_window'):
            self.main_window.close()
        
        # Cerrar ventana de login
        self.login_window.close()
    
    def closeEvent(self, event):
        """Manejar el cierre de la ventana"""
        self.cerrar_aplicacion()
        event.accept()