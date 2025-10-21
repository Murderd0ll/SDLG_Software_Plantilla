import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                             QPushButton, QHBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont

# Importar la clase del sidebar
from sidebar import MainWindow  # Asegúrate de que el archivo se llame sidebar.py

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar el diseño desde la carpeta ui
        ui_path = os.path.join("ui", "login.ui")
        uic.loadUi(ui_path, self)
        
        # Configurar fondo manualmente
        self.setup_background()
        self.setup_logo()
        
        # Aplicar estilos CSS básicos
        self.setup_styles()
        
        # Configurar placeholders simples
        self.setup_placeholders()
        
        # Conectar eventos
        self.setup_events()
        
        # Centrar ventana
        self.center_window()
        
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
                    scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        """Aplicar estilos CSS básicos"""
        style = """
        QMainWindow {
            background: transparent;
        }
        
        QLabel {
            color: #FFFFFF;
            font-family: 'Segoe UI', Arial;
        }
        
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 12px 15px;
            color: #1D2128;
            font-size: 14px;
            font-family: 'Segoe UI', Arial;
        }
        
        QPushButton#btnLogin {
            background-color: #a09172;
            border: 2px solid #a09172;
            color: #FFFFFF;
            border-radius: 8px;
            padding: 12px 25px;
            font-weight: bold;
            font-size: 15px;
        }
        
        QLabel#labelError {
            color: #e74c3c;
            font-size: 12px;
            font-weight: bold;
        }
        """
        self.setStyleSheet(style)
    
    def setup_placeholders(self):
        """Configurar placeholders simples"""
        try:
            if hasattr(self, 'lineEditUsuario'):
                self.lineEditUsuario.setPlaceholderText("Usuario")
                print("✅ Placeholder usuario configurado")
            
            if hasattr(self, 'lineEditPassword'):
                self.lineEditPassword.setPlaceholderText("Contraseña")
                self.lineEditPassword.setEchoMode(self.lineEditPassword.Password)
                print("✅ Placeholder contraseña configurado")
                
        except Exception as e:
            print(f"❌ Error configurando placeholders: {e}")
    
    def setup_events(self):
        """Conectar eventos de manera segura"""
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
    
    def resizeEvent(self, event):
        """Redimensionar el fondo cuando cambia el tamaño de la ventana"""
        super().resizeEvent(event)
        self.setup_background()
    
    def validar_login(self):
        """Validar credenciales"""
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
                    self.labelError.setStyleSheet("color: #e74c3c;")
                else:
                    self.labelError.setStyleSheet("color: #2ecc71;")
                print(f"📢 Mensaje: {mensaje}")
        except Exception as e:
            print(f"❌ Error mostrando mensaje: {e}")
    
    def abrir_menu_principal(self):
        """Abrir ventana principal (sidebar)"""
        try:
            # Ocultar el login
            self.hide()
            
            # Crear y mostrar el sidebar
            self.sidebar = MainWindow()
            
            # Conectar la señal de cierre del sidebar para cerrar toda la aplicación
            self.sidebar.destroyed.connect(self.cerrar_aplicacion)
            
            # Mostrar el sidebar
            self.sidebar.show()
            
            # Opcional: Maximizar la ventana del sidebar
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
    
    # Cargar estilo QSS si existe
    style_path = "style.qss"
    if os.path.exists(style_path):
        try:
            with open(style_path, "r") as style_file:
                style_str = style_file.read()
                app.setStyleSheet(style_str)
                print("✅ Estilo QSS cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando estilo QSS: {e}")
    
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
        window = LoginWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()