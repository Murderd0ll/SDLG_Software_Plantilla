import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                             QPushButton, QHBoxLayout, QWidget, QFrame,
                             QLineEdit, QVBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont

# Importar la clase del sidebar
from sidebar import MainWindow

class AnimatedLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar el diseño desde la carpeta ui
        ui_path = os.path.join("ui", "login.ui")
        uic.loadUi(ui_path, self)
        
        # Configurar fondo manualmente
        self.setup_background()
        self.setup_logo()
        
        # Aplicar estilos CSS mejorados
        self.setup_styles()
        
        # Configurar placeholders simples
        self.setup_placeholders()
        
        # Configurar botón de mostrar contraseña
        self.setup_password_toggle()
        
        # Conectar eventos
        self.setup_events()
        
        # Centrar ventana
        self.center_window()
        
        # Configurar animaciones
        self.setup_animations()
        
        print("✅ Ventana cargada correctamente")
    
    def setup_background(self):
        """Configurar la imagen de fondo manualmente"""
        fondo_path = os.path.join("img", "fondologin.png")
        if os.path.exists(fondo_path):
            try:
                palette = QPalette()
                pixmap = QPixmap(fondo_path)
                palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(
                    self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
                self.setPalette(palette)
                print("✅ Fondo cargado desde:", fondo_path)
            except Exception as e:
                print(f"❌ Error cargando fondo: {e}")
        else:
            print(f"⚠️ No se encontró el fondo en: {fondo_path}")

    def setup_logo(self):
        """Configurar la imagen del logo"""
        logo_path = os.path.join("img", "logo.png")
        if os.path.exists(logo_path):
            try:
                if hasattr(self, 'labelLogo'):
                    pixmap = QPixmap(logo_path)
                    scaled_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.labelLogo.setPixmap(scaled_pixmap)
                    self.labelLogo.setAlignment(Qt.AlignCenter)
                    print("✅ Logo cargado desde:", logo_path)
                else:
                    print("⚠️ No se encontró labelLogo en el diseño")
            except Exception as e:
                print(f"❌ Error cargando logo: {e}")
        else:
            print(f"⚠️ No se encontró el logo en: {logo_path}")
            if hasattr(self, 'labelLogo'):
                self.labelLogo.setText("🐄")
                self.labelLogo.setStyleSheet("font-size: 48px; color: white;")
                print("✅ Logo de texto configurado")

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def setup_styles(self):
        """Aplicar estilos CSS mejorados sin bordes visibles"""
        style = """
        QMainWindow {
            background: transparent;
            border: none;
        }
        
        /* Contenedor principal completamente transparente */
        QWidget {
            background: rgba(0, 0, 0, 0.4);
            border: none;
            border-radius: 20px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }
        
        /* Eliminar bordes de todos los frames */
        QFrame, QWidget {
            background: transparent;
            border: none;
            border-radius: 0px;
        }
        
        QLabel {
            color: #FFFFFF;
            font-family: 'Segoe UI', Arial;
            font-weight: bold;
            background: transparent;
            border: none;
        }
        
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.1);
            border: none;
            border-radius: 12px;
            padding: 15px 20px;
            color: #FFFFFF;
            font-size: 14px;
            font-family: 'Segoe UI', Arial;
            font-weight: bold;
            selection-background-color: rgba(160, 145, 114, 0.5);
        }
        
        QLineEdit:focus {
            background-color: rgba(255, 255, 255, 0.15);
            border: none;
            outline: none;
        }
        
        QLineEdit::placeholder {
            color: rgba(255, 255, 255, 0.6);
            font-weight: normal;
        }
        
        QPushButton#btnLogin {
            background-color: rgba(160, 145, 114, 0.9);
            border: none;
            color: #FFFFFF;
            border-radius: 12px;
            padding: 15px 25px;
            font-weight: bold;
            font-size: 16px;
            margin-top: 10px;
        }
        
        QPushButton#btnLogin:hover {
            background-color: rgba(160, 145, 114, 1);
        }
        
        QPushButton#btnLogin:pressed {
            background-color: rgba(140, 125, 94, 0.9);
        }
        
        /* Botón de mostrar contraseña - TRANSPARENTE */
        #btnTogglePassword {
            background-color: rgba(255, 255, 255, 0.0);
            border: none;
            color: rgba(255, 255, 255, 0.7);
            border-radius: 6px;
            padding: 5px;
            font-size: 16px;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        }
        
        #btnTogglePassword:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.9);
        }
        
        #btnTogglePassword:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        QLabel#labelError {
            color: #ff6b6b;
            font-size: 12px;
            font-weight: bold;
            background: transparent;
            padding: 8px;
            border-radius: 8px;
            background-color: rgba(231, 76, 60, 0.15);
            border: none;
        }
        """
        self.setStyleSheet(style)
    
    def setup_password_toggle(self):
        """Configurar botón de mostrar contraseña con posición corregida"""
        try:
            if hasattr(self, 'lineEditPassword'):
                print("🔧 Configurando botón de contraseña...")
                
                # Crear el botón TRANSPARENTE
                self.btnTogglePassword = QPushButton("👁️", self)
                self.btnTogglePassword.setObjectName("btnTogglePassword")
                self.btnTogglePassword.setCursor(Qt.PointingHandCursor)
                self.btnTogglePassword.setFixedSize(30, 30)
                self.btnTogglePassword.clicked.connect(self.toggle_password_visibility)
                
                # Posicionar el botón CORRECTAMENTE al lado del campo de contraseña
                self.update_toggle_position()
                
                # Mostrar el botón
                self.btnTogglePassword.show()
                
                self.password_visible = False
                print("✅ Botón de contraseña creado y posicionado")
                
        except Exception as e:
            print(f"❌ Error creando botón de contraseña: {e}")
    
    def update_toggle_position(self):
        """Actualizar la posición del botón de contraseña - POSICIÓN CORREGIDA"""
        try:
            if hasattr(self, 'lineEditPassword') and hasattr(self, 'btnTogglePassword'):
                # Obtener posición y tamaño del campo de contraseña
                password_pos = self.lineEditPassword.pos()
                password_size = self.lineEditPassword.size()
                
                # Calcular posición CORRECTA del botón
                # A la derecha del campo, pero CENTRADO VERTICALMENTE
                button_x = password_pos.x() + password_size.width() - 35  # Un poco más adentro
                button_y = password_pos.y() + (password_size.height() - 30) // 2
                
                # Mover el botón a la posición corregida
                self.btnTogglePassword.move(button_x, button_y)
                
                print(f"📍 Botón posicionado en: ({button_x}, {button_y})")
                
        except Exception as e:
            print(f"❌ Error posicionando botón: {e}")
    
    def resizeEvent(self, event):
        """Redimensionar el fondo y reposicionar botón"""
        super().resizeEvent(event)
        self.setup_background()
        # Esperar un poco para que los widgets se redimensionen
        QTimer.singleShot(50, self.update_toggle_position)
    
    def moveEvent(self, event):
        """Reposicionar botón cuando se mueve la ventana"""
        super().moveEvent(event)
        QTimer.singleShot(50, self.update_toggle_position)
    
    def showEvent(self, event):
        """Ejecutar animación al mostrar la ventana"""
        super().showEvent(event)
        self.enter_animation.start()
        # Esperar a que la ventana se muestre completamente antes de posicionar
        QTimer.singleShot(100, self.update_toggle_position)
    
    def toggle_password_visibility(self):
        """Alternar entre mostrar y ocultar la contraseña"""
        try:
            if hasattr(self, 'lineEditPassword') and hasattr(self, 'btnTogglePassword'):
                if self.password_visible:
                    # Ocultar contraseña
                    self.lineEditPassword.setEchoMode(QLineEdit.Password)
                    self.btnTogglePassword.setText("👁️")
                    self.password_visible = False
                    print("🔒 Contraseña oculta")
                else:
                    # Mostrar contraseña
                    self.lineEditPassword.setEchoMode(QLineEdit.Normal)
                    self.btnTogglePassword.setText("🔒")
                    self.password_visible = True
                    print("👀 Contraseña visible")
        except Exception as e:
            print(f"❌ Error alternando visibilidad: {e}")
    
    def setup_animations(self):
        """Configurar animaciones para la ventana"""
        try:
            # Animación de entrada (fade in)
            self.enter_animation = QPropertyAnimation(self, b"windowOpacity")
            self.enter_animation.setDuration(800)
            self.enter_animation.setStartValue(0.0)
            self.enter_animation.setEndValue(1.0)
            self.enter_animation.setEasingCurve(QEasingCurve.OutCubic)
            
            print("✅ Animaciones configuradas")
            
        except Exception as e:
            print(f"❌ Error configurando animaciones: {e}")
    
    def setup_placeholders(self):
        """Configurar placeholders simples"""
        try:
            if hasattr(self, 'lineEditUsuario'):
                self.lineEditUsuario.setPlaceholderText("👤 Usuario")
                print("✅ Placeholder usuario configurado")
            
            if hasattr(self, 'lineEditPassword'):
                self.lineEditPassword.setPlaceholderText("🔒 Contraseña")
                self.lineEditPassword.setEchoMode(QLineEdit.Password)
                print("✅ Placeholder contraseña configurado")
                
        except Exception as e:
            print(f"❌ Error configurando placeholders: {e}")
    
    def setup_events(self):
        """Conectar eventos de manera segura"""
        try:
            if hasattr(self, 'btnLogin'):
                self.btnLogin.clicked.connect(self.validar_login)
                print("✅ Botón login conectado")
            else:
                print("❌ No se encontró btnLogin")
            
            if hasattr(self, 'lineEditUsuario'):
                self.lineEditUsuario.returnPressed.connect(self.validar_login)
                self.lineEditUsuario.setFocus()
                print("✅ Campo usuario conectado")
            
            if hasattr(self, 'lineEditPassword'):
                self.lineEditPassword.returnPressed.connect(self.validar_login)
                print("✅ Campo contraseña conectado")
                
        except Exception as e:
            print(f"❌ Error conectando eventos: {e}")
    
    def validar_login(self):
        """Validar credenciales con animación"""
        try:
            usuario = ""
            contrasena = ""
            
            if hasattr(self, 'lineEditUsuario'):
                usuario = self.lineEditUsuario.text().strip()
            
            if hasattr(self, 'lineEditPassword'):
                contrasena = self.lineEditPassword.text()
            
            print(f"🔐 Validando: usuario='{usuario}', contraseña='{contrasena}'")
            
            # Validación simple
            if usuario == "admin" and contrasena == "1234":
                self.mostrar_mensaje("✓ Acceso concedido", "éxito")
                QTimer.singleShot(1000, self.abrir_menu_principal)
            else:
                self.mostrar_mensaje("✗ Usuario o contraseña incorrectos", "error")
                if hasattr(self, 'lineEditPassword'):
                    self.lineEditPassword.clear()
                    self.lineEditPassword.setFocus()
                
        except Exception as e:
            print(f"❌ Error al validar: {e}")
            self.mostrar_mensaje("Error en la validación", "error")
    
    def mostrar_mensaje(self, mensaje, tipo):
        """Mostrar mensaje de error/éxito"""
        try:
            if hasattr(self, 'labelError'):
                self.labelError.setText(mensaje)
                if tipo == "error":
                    self.labelError.setStyleSheet("""
                        color: #ff6b6b;
                        font-size: 12px;
                        font-weight: bold;
                        background: transparent;
                        padding: 8px;
                        border-radius: 8px;
                        background-color: rgba(231, 76, 60, 0.15);
                    """)
                else:
                    self.labelError.setStyleSheet("""
                        color: #2ecc71;
                        font-size: 12px;
                        font-weight: bold;
                        background: transparent;
                        padding: 8px;
                        border-radius: 8px;
                        background-color: rgba(46, 204, 113, 0.15);
                    """)
                print(f"📢 Mensaje: {mensaje}")
        except Exception as e:
            print(f"❌ Error mostrando mensaje: {e}")
    
    def abrir_menu_principal(self):
        """Abrir ventana principal con animación"""
        try:
            # Animación de salida
            exit_animation = QPropertyAnimation(self, b"windowOpacity")
            exit_animation.setDuration(600)
            exit_animation.setStartValue(1.0)
            exit_animation.setEndValue(0.0)
            exit_animation.setEasingCurve(QEasingCurve.InCubic)
            exit_animation.start()
            
            exit_animation.finished.connect(self._open_sidebar)
            
        except Exception as e:
            print(f"❌ Error en animación de salida: {e}")
            self._open_sidebar()
    
    def _open_sidebar(self):
        """Abrir el sidebar después de la animación"""
        try:
            self.hide()
            self.sidebar = MainWindow()
            self.sidebar.destroyed.connect(self.cerrar_aplicacion)
            self.sidebar.show()
            self.sidebar.showMaximized()
            print("✅ Sidebar abierto correctamente")
        except Exception as e:
            print(f"❌ Error al abrir el sidebar: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo abrir el menú principal: {e}")
    
    def cerrar_aplicacion(self):
        """Cerrar toda la aplicación cuando se cierra el sidebar"""
        self.close()

def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente global
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Ignorar warning de libpng
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.svg.warning=false'
    
    # Verificar que los archivos existen
    ui_path = os.path.join("ui", "login.ui")
    fondo_path = os.path.join("img", "fondologin.png")
    
    if not os.path.exists(ui_path):
        print(f"❌ ERROR: No encuentro {ui_path}")
        print("💡 Asegúrate de que:")
        print("   1. Existe la carpeta 'ui'")
        print("   2. El archivo 'login.ui' está dentro")
        print("   3. Está en la misma carpeta que este script")
        input("Presiona Enter para salir...")
        return
    
    if not os.path.exists(fondo_path):
        print(f"⚠️ Advertencia: No encuentro {fondo_path}")
    
    try:
        window = AnimatedLoginWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()