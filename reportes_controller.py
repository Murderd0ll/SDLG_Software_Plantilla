# controllers/reportes_controller.py - VERSIÓN ACTUALIZADA CON NAVEGACIÓN A SBUSCAR Y RBUSCAR
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

class ReportesController:
    def __init__(self, reportes_widget):
        self.reportes_widget = reportes_widget
        self.setup_connections()
        print("✅ ReportesController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para reportes...")
            
            # Conectar botones de reportes
            self.pushButton_2 = self.reportes_widget.findChild(QtWidgets.QPushButton, "pushButton_2")  # Reproducción
            self.pushButton_3 = self.reportes_widget.findChild(QtWidgets.QPushButton, "pushButton_3")  # Salud
            
            if self.pushButton_2:
                self.pushButton_2.clicked.connect(self.abrir_reportes_reproduccion)
                print("✅ Botón Reportes Reproducción conectado")
            else:
                print("❌ No se encontró pushButton_2 (Reportes Reproducción)")
                
            if self.pushButton_3:
                self.pushButton_3.clicked.connect(self.abrir_reportes_salud)
                print("✅ Botón Reportes Salud conectado")
            else:
                print("❌ No se encontró pushButton_3 (Reportes Salud)")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def abrir_reportes_reproduccion(self):
        """Abre los reportes de reproducción (Rbuscar) en el mismo stackedWidget"""
        try:
            print("🐄 Navegando a reportes de reproducción...")
            
            # Obtener la ventana principal para cambiar de página
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de Rbuscar (índice 9)
                main_window.cambiar_pagina(9, "Reportes de Reproducción")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo navegar a reportes de reproducción")
            
        except Exception as e:
            print(f"❌ Error al abrir reportes de reproducción: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error(f"No se pudo abrir reportes de reproducción: {str(e)}")

    def abrir_reportes_salud(self):
        """Abre los reportes de salud (Sbuscar) en el mismo stackedWidget"""
        try:
            print("🏥 Navegando a reportes de salud...")
            
            # Obtener la ventana principal para cambiar de página
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de Sbuscar (índice 8)
                main_window.cambiar_pagina(8, "Reportes de Salud")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo navegar a reportes de salud")
            
        except Exception as e:
            print(f"❌ Error al abrir reportes de salud: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error(f"No se pudo abrir reportes de salud: {str(e)}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.reportes_widget
            while parent is not None:
                if hasattr(parent, 'cambiar_pagina') and hasattr(parent, 'ui'):
                    return parent
                parent = parent.parent()
            
            # Si no se encuentra, buscar entre las ventanas de la aplicación
            app = QtWidgets.QApplication.instance()
            for widget in app.topLevelWidgets():
                if hasattr(widget, 'cambiar_pagina') and hasattr(widget, 'ui'):
                    return widget
            
            return None
        except Exception as e:
            print(f"❌ Error obteniendo main window: {e}")
            return None

    def mostrar_mensaje_temporal(self, titulo, mensaje, icono=None):
        """Muestra un mensaje temporal indicando que se está abriendo el módulo"""
        try:
            msg = QtWidgets.QMessageBox(self.reportes_widget)
            msg.setWindowTitle(titulo)
            msg.setText(mensaje)
            
            if icono:
                msg.setIconPixmap(icono.scaled(64, 64, QtCore.Qt.KeepAspectRatio))
            else:
                msg.setIcon(QtWidgets.QMessageBox.Information)
                
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            
        except Exception as e:
            print(f"❌ Error mostrando mensaje temporal: {e}")

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.reportes_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página de reportes"""
        print("📊 Cargando página de reportes...")

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador de reportes...")