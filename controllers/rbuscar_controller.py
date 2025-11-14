# rbuscar_controller.py - VERSIÓN CORREGIDA
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database
import os

class RbuscarController:
    def __init__(self, rbuscar_widget):
        self.rbuscar_widget = rbuscar_widget
        self.db = Database()
        self.setup_connections()
        print("✅ RbuscarController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para Rbuscar...")
            
            # Conectar botones de Rbuscar
            self.pushButton = self.rbuscar_widget.findChild(QtWidgets.QPushButton, "pushButton")  # Botón Ir
            self.lineEdit = self.rbuscar_widget.findChild(QtWidgets.QLineEdit, "lineEdit")  # Campo de texto
            self.btnRegresar = self.rbuscar_widget.findChild(QtWidgets.QPushButton, "btnRegresar")  # Botón Regresar
            
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
        """Busca y redirige a la página de reproducción con los resultados"""
        try:
            arete = self.lineEdit.text().strip()
            print(f"🔍 Buscando y redirigiendo para arete: {arete}")
            
            if not arete:
                self.mostrar_error("Por favor ingrese un arete")
                return
            
            # Verificar si existe algún registro de reproducción con ese arete
            registros = self.db.obtener_registros_reproduccion_por_arete(arete)
            if not registros:
                self.mostrar_error(f"No se encontraron registros de reproducción para el arete: {arete}")
                return
            
            # Redirigir a la página de reproducción
            self.redirigir_a_reproduccion(arete)
                
        except Exception as e:
            print(f"❌ Error al buscar y redirigir: {e}")
            self.mostrar_error(f"Error al buscar: {str(e)}")

    def redirigir_a_reproduccion(self, arete):
        """Redirige a la página de reproducción con el arete específico"""
        try:
            print(f"🔄 Redirigiendo a página de reproducción con arete: {arete}")
            
            # Obtener la ventana principal
            main_window = self.get_main_window()
            if main_window:
                # ✅ CORREGIDO: Cambiar a la página de reproducción (índice 14 según tu sidebar)
                main_window.cambiar_pagina(14, "Reproducción")
                
                # Pasar el arete al controlador de reproducción
                if hasattr(main_window, 'reproduccion_controller') and main_window.reproduccion_controller:
                    main_window.reproduccion_controller.mostrar_registros_por_arete(arete)
                    print(f"✅ Arete '{arete}' pasado al controlador de reproducción")
                else:
                    print("⚠️ Controlador de reproducción no disponible")
                    self.mostrar_informacion(f"Redirigido a reproducción con arete: {arete}")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo redirigir a la página de reproducción")
                
        except Exception as e:
            print(f"❌ Error redirigiendo a reproducción: {e}")
            self.mostrar_error(f"No se pudo redirigir a la página de reproducción: {str(e)}")

    def regresar_a_reportes(self):
        """Regresa a la página de Reportes"""
        try:
            print("🔙 Regresando a página de Reportes...")
            main_window = self.get_main_window()
            if main_window:
                main_window.cambiar_pagina(6, "Reportes")
                print("✅ Regresado a página de Reportes")
            else:
                print("❌ No se pudo encontrar la ventana principal")
        except Exception as e:
            print(f"❌ Error al regresar a reportes: {e}")
            self.mostrar_error(f"Error al regresar a reportes: {str(e)}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            parent = self.rbuscar_widget
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
                self.rbuscar_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def mostrar_informacion(self, mensaje):
        """Muestra un mensaje informativo"""
        try:
            QtWidgets.QMessageBox.information(
                self.rbuscar_widget,
                "Información",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje informativo: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("🐄 Cargando página de búsqueda de reproducción...")
        # Limpiar el campo de búsqueda al cargar
        if hasattr(self, 'lineEdit') and self.lineEdit:
            self.lineEdit.clear()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Rbuscar...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()