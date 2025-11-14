# login_controller.py COMPLETO CON CIERRE DE SESIÓN - VERSIÓN CORREGIDA
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
from sidebar import MainWindow
from Esidebar import EMainWindow  # Importar el sidebar para empleados
from database import Database

class LoginController:
    def __init__(self, login_ui, login_window):
        """
        Controlador completo para la ventana de login
        """
        self.ui = login_ui
        self.login_window = login_window
        self.db = Database()
        self.password_visible = False
        self.main_window = None
        
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
        """Validar las credenciales del usuario en la base de datos"""
        try:
            # Obtener datos de los campos
            usuario = self.ui.lineEditUsuario.text().strip()
            password = self.ui.lineEditPassword.text().strip()
            
            print(f"🔐 Intentando login - Usuario: '{usuario}'")
            
            # Validar campos vacíos
            if not usuario or not password:
                self.mostrar_error("Error de validación", "Por favor, complete todos los campos.")
                return
            
            # Verificar que la tabla de usuarios exista
            if not self.db.verificar_tabla_usuarios():
                self.mostrar_error("Error", "No se pudo verificar la tabla de usuarios.")
                return
            
            # Validar credenciales en la base de datos
            usuario_data = self.db.verificar_credenciales(usuario, password)
            
            if usuario_data:
                # Login exitoso
                id_usuario, nombre_usuario, nombre_completo, rol = usuario_data
                self.login_exitoso(id_usuario, nombre_usuario, nombre_completo, rol)
            else:
                # Credenciales incorrectas
                self.mostrar_error("Credenciales incorrectas", 
                                 "Usuario o contraseña incorrectos.")
                                 
        except Exception as e:
            print(f"❌ Error en validar_login: {e}")
            self.mostrar_error("Error", f"Error al validar credenciales: {str(e)}")

    def login_exitoso(self, id_usuario, nombre_usuario, nombre_completo, rol):
        """Manejar el login exitoso según el rol del usuario - CORREGIDO"""
        try:
            print(f"✅ Login exitoso - Usuario: {nombre_completo}, Rol: {rol}")
            print("🔄 Abriendo aplicación principal...")
            
            # Ocultar ventana de login
            self.login_window.hide()
            
            # ✅ CREAR OBJETO USUARIO ACTUAL COMPLETO
            usuario_actual = {
                'id': id_usuario,
                'usuario': nombre_usuario,
                'nombre': nombre_completo,
                'rol': rol
            }
            
            print(f"👤 Creando sidebar con usuario: {usuario_actual}")
            
            # Crear y mostrar la ventana principal según el rol
            if rol == "Administrador":
                print("👑 Abriendo interfaz de Administrador...")
                self.main_window = MainWindow(usuario_actual=usuario_actual)
                
                # ✅ VERIFICAR QUE EL USUARIO SE ESTABLECIÓ CORRECTAMENTE
                if hasattr(self.main_window, 'usuario_actual'):
                    print(f"✅ Usuario establecido en MainWindow: {self.main_window.usuario_actual}")
                else:
                    print("❌ No se pudo establecer usuario en MainWindow")
                    
            elif rol == "Usuario":
                print("👨‍💼 Abriendo interfaz de Usuario...")
                self.main_window = EMainWindow(usuario_actual=usuario_actual)
                
                # ✅ VERIFICAR QUE EL USUARIO SE ESTABLECIÓ CORRECTAMENTE
                if hasattr(self.main_window, 'usuario_actual'):
                    print(f"✅ Usuario establecido en EMainWindow: {self.main_window.usuario_actual}")
                else:
                    print("❌ No se pudo establecer usuario en EMainWindow")
            
            # ✅ VERIFICAR CONTROLADOR DE BITÁCORA
            if hasattr(self.main_window, 'bitacora_controller'):
                if hasattr(self.main_window.bitacora_controller, 'usuario_actual'):
                    print(f"✅ Usuario en bitácora: {self.main_window.bitacora_controller.usuario_actual}")
                else:
                    print("❌ No hay usuario en controlador de bitácora")
            else:
                print("❌ No se encontró controlador de bitácora")
            
            # Mostrar la ventana principal
            self.main_window.show()
            
            # ✅ REGISTRAR LOGIN EN BITÁCORA
            if hasattr(self.main_window, 'bitacora_controller') and self.main_window.bitacora_controller:
                self.main_window.bitacora_controller.registrar_login(nombre_completo)
                print("✅ Login registrado en bitácora")
            
            # ✅ CONFIGURAR CIERRE DE SESIÓN
            self.configurar_cierre_sesion()
            
            # Conectar el cierre de la ventana principal para cerrar toda la aplicación
            self.conectar_cierre_aplicacion()
            
            print("✅ Aplicación principal iniciada correctamente")
            
        except Exception as e:
            print(f"❌ Error al abrir la aplicación principal: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error("Error", f"No se pudo iniciar la aplicación: {str(e)}")
            # Mostrar nuevamente la ventana de login
            self.login_window.show()
    
    def configurar_cierre_sesion(self):
        """Configurar el cierre de sesión desde los sidebars"""
        try:
            if hasattr(self, 'main_window') and self.main_window:
                # Conectar señales de cierre de sesión
                if hasattr(self.main_window, 'cerrar_sesion_solicitado'):
                    self.main_window.cerrar_sesion_solicitado.connect(self.cerrar_sesion_volver_login)
                    print("✅ Señal de cierre de sesión conectada")
                else:
                    print("⚠️  No se encontró señal de cierre de sesión en el sidebar")
                    
        except Exception as e:
            print(f"❌ Error configurando cierre de sesión: {e}")
    
    def cerrar_sesion_volver_login(self):
        """Cerrar sesión y volver al login"""
        try:
            print("🔒 Cerrando sesión y volviendo al login...")
            
            # Cerrar ventana principal si existe
            if hasattr(self, 'main_window') and self.main_window:
                print("🔴 Cerrando ventana principal...")
                
                # Desconectar todas las señales primero
                try:
                    if hasattr(self.main_window, 'cerrar_sesion_solicitado'):
                        self.main_window.cerrar_sesion_solicitado.disconnect()
                except Exception as e:
                    print(f"⚠️  Error desconectando señales: {e}")
                
                # Cerrar la ventana
                self.main_window.close()
                self.main_window = None
            
            # Mostrar y resetear ventana de login
            print("🔄 Mostrando ventana de login...")
            self.login_window.show()
            self.login_window.ui.lineEditUsuario.clear()
            self.login_window.ui.lineEditPassword.clear()
            self.login_window.ui.lineEditUsuario.setFocus()
            
            # Limpiar contraseña visible
            self.password_visible = False
            self.ui.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
            self.actualizar_estilo_ojo()
            
            print("✅ Sesión cerrada, volviendo al login")
            
        except Exception as e:
            print(f"❌ Error al cerrar sesión: {e}")
            # En caso de error, al menos mostrar el login
            self.login_window.show()
    
    def conectar_cierre_aplicacion(self):
        """Conectar los botones de cierre de la ventana principal"""
        try:
            if hasattr(self, 'main_window') and self.main_window:
                # Intentar conectar con diferentes nombres de botones de cierre
                if hasattr(self.main_window.ui, 'cerrarbtn1'):
                    self.main_window.ui.cerrarbtn1.clicked.connect(self.cerrar_aplicacion)
                    print("✅ Botón cerrar 1 conectado")
                
                if hasattr(self.main_window.ui, 'cerrarbtn2'):
                    self.main_window.ui.cerrarbtn2.clicked.connect(self.cerrar_aplicacion)
                    print("✅ Botón cerrar 2 conectado")
                
                if hasattr(self.main_window.ui, 'btnCerrar'):
                    self.main_window.ui.btnCerrar.clicked.connect(self.cerrar_aplicacion)
                    print("✅ Botón btnCerrar conectado")
                    
        except Exception as e:
            print(f"⚠️  No se pudieron conectar todos los botones de cierre: {e}")
    
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
        if hasattr(self, 'main_window') and self.main_window:
            try:
                self.main_window.close()
            except Exception as e:
                print(f"⚠️  Error cerrando ventana principal: {e}")
        
        # Cerrar ventana de login
        try:
            self.login_window.close()
        except Exception as e:
            print(f"⚠️  Error cerrando ventana de login: {e}")
        
        # Salir de la aplicación
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event):
        """Manejar el cierre de la ventana"""
        self.cerrar_aplicacion()
        event.accept()