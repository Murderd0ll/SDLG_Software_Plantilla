# sbuscar_controller.py (modificado)
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
import os

class SbuscarController:
    def __init__(self, sbuscar_widget):
        self.sbuscar_widget = sbuscar_widget
        self.db = Database()
        self.setup_connections()
        print("✅ SbuscarController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para Sbuscar...")
            
            # Conectar botones de Sbuscar
            self.pushButton = self.sbuscar_widget.findChild(QtWidgets.QPushButton, "pushButton")  # Botón Ir
            self.lineEdit = self.sbuscar_widget.findChild(QtWidgets.QLineEdit, "lineEdit")  # Campo de texto
            self.btnRegresar = self.sbuscar_widget.findChild(QtWidgets.QPushButton, "btnRegresar")  # Botón Regresar
            
            if self.pushButton:
                self.pushButton.clicked.connect(self.buscar_y_redirigir)
                print("✅ Botón 'Ir' conectado")
            else:
                print("❌ No se encontró pushButton (Botón Ir)")
                
            if self.btnRegresar:
                self.btnRegresar.clicked.connect(self.regresar_a_reportes)
                print("✅ Botón 'Regresar' conectado")
            else:
                print("❌ No se encontró btnRegresar")
                
            # Conectar Enter en el lineEdit también
            if self.lineEdit:
                self.lineEdit.returnPressed.connect(self.buscar_y_redirigir)
                print("✅ Enter en lineEdit conectado")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def buscar_y_redirigir(self):
        """Busca y redirige a la página de salud con los resultados"""
        try:
            arete = self.lineEdit.text().strip()
            print(f"🔍 Buscando y redirigiendo para arete: {arete}")
            
            if not arete:
                self.mostrar_error("Por favor ingrese un arete")
                return
            
            # Redirigir a la página de salud
            self.redirigir_a_salud(arete)
                
        except Exception as e:
            print(f"❌ Error al buscar y redirigir: {e}")
            self.mostrar_error(f"Error al buscar: {str(e)}")

    def redirigir_a_salud(self, arete):
        """Redirige a la página de salud con el arete específico"""
        try:
            print(f"🔄 Redirigiendo a página de salud con arete: {arete}")
            
            # Obtener la ventana principal
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de salud (índice 13 - asumiendo que Salud está en índice 13)
                # Necesitarías agregar Salud al sidebar primero
                main_window.cambiar_pagina(13, "Salud")
                
                # Pasar el arete al controlador de salud
                if hasattr(main_window, 'salud_controller') and main_window.salud_controller:
                    main_window.salud_controller.mostrar_registros_por_arete(arete)
                else:
                    print("⚠️ Controlador de salud no disponible")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                
        except Exception as e:
            print(f"❌ Error redirigiendo a salud: {e}")
            self.mostrar_error(f"No se pudo redirigir a la página de salud: {str(e)}")

    def regresar_a_reportes(self):
        """Regresa a la página de Reportes"""
        try:
            print("🔙 Regresando a página de Reportes...")
            main_window = self.get_main_window()
            if main_window:
                main_window.cambiar_pagina(6, "Reportes")
            else:
                print("❌ No se pudo encontrar la ventana principal")
        except Exception as e:
            print(f"❌ Error al regresar a reportes: {e}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            parent = self.sbuscar_widget
            while parent is not None:
                if hasattr(parent, 'cambiar_pagina') and hasattr(parent, 'ui'):
                    return parent
                parent = parent.parent()
            
            app = QtWidgets.QApplication.instance()
            for widget in app.topLevelWidgets():
                if hasattr(widget, 'cambiar_pagina') and hasattr(widget, 'ui'):
                    return widget
            
            return None
        except Exception as e:
            print(f"❌ Error obteniendo main window: {e}")
            return None

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.sbuscar_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("🏥 Cargando página de búsqueda de salud...")
        # Limpiar el campo de búsqueda al cargar
        if hasattr(self, 'lineEdit') and self.lineEdit:
            self.lineEdit.clear()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Sbuscar...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()