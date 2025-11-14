# main.py - VERSIÓN MEJORADA
import sys
import os
from PyQt5 import QtWidgets
from ui.login_ui import Ui_login
from controllers.login_controller import LoginController

def cargar_estilos_login(window):
    """Cargar estilos SOLO para la ventana de login"""
    try:
        if os.path.exists('style.qss'):
            with open('style.qss', 'r', encoding='utf-8') as f:
                estilo = f.read()
            window.setStyleSheet(estilo)
            print("✅ Estilos de login cargados correctamente")
        else:
            print("⚠️  Archivo style.qss no encontrado")
    except Exception as e:
        print(f"❌ Error cargando estilos login: {e}")

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login()
        self.ui.setupUi(self)
        
        # Cargar estilos SOLO para esta ventana
        cargar_estilos_login(self)
        
        # Inicializar el controlador
        self.controller = LoginController(self.ui, self)
        
        print("🚀 Aplicación de login iniciada")
        
    def closeEvent(self, event):
        """Manejar el cierre de la ventana de login"""
        print("🔴 Cerrando aplicación desde login window...")
        # Cerrar la aplicación completamente
        QtWidgets.QApplication.quit()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Configurar la aplicación
    app.setApplicationName("SDLG - Sistema de Gestión Ganadera")
    app.setApplicationVersion("1.0")
    
    # NO cargar estilos globalmente aquí
    # Los estilos se cargarán individualmente en cada ventana
    
    # Crear y mostrar ventana de login
    login_window = LoginWindow()
    login_window.show()
    
    print("🎯 Sistema de login listo")
    print("📝 Características:")
    print("   🔐 Validación contra base de datos")
    print("   👑 Redirección a Admin/Empleado según rol") 
    print("   👁️  Mostrar/ocultar contraseña")
    print("   ↩️  Enter para iniciar sesión")
    print("   🔒 Cierre de sesión seguro")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()