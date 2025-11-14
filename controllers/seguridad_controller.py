from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

class SeguridadController:
    def __init__(self, seguridad_widget):
        self.seguridad_widget = seguridad_widget
        self.setup_connections()
        print("✅ SeguridadController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para seguridad...")
            
            # Conectar botones de seguridad
            self.pushButton_4 = self.seguridad_widget.findChild(QtWidgets.QPushButton, "pushButton_4")  # Usuarios
            self.pushButton_3 = self.seguridad_widget.findChild(QtWidgets.QPushButton, "pushButton_3")  # Realizar copia
            self.pushButton_2 = self.seguridad_widget.findChild(QtWidgets.QPushButton, "pushButton_2")  # Seleccionar copia
            
            if self.pushButton_4:
                self.pushButton_4.clicked.connect(self.abrir_gestion_usuarios)
                print("✅ Botón Gestión de Usuarios conectado")
            else:
                print("❌ No se encontró pushButton_4 (Gestión de Usuarios)")
                
            if self.pushButton_3:
                self.pushButton_3.clicked.connect(self.abrir_realizar_copia_seguridad)
                print("✅ Botón Realizar Copia de Seguridad conectado")
            else:
                print("❌ No se encontró pushButton_3 (Realizar Copia de Seguridad)")
                
            if self.pushButton_2:
                self.pushButton_2.clicked.connect(self.abrir_restaurar_copia_seguridad)
                print("✅ Botón Seleccionar Copia de Seguridad conectado")
            else:
                print("❌ No se encontró pushButton_2 (Seleccionar Copia de Seguridad)")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def abrir_gestion_usuarios(self):
        """Abre la gestión de usuarios en el mismo stackedWidget"""
        try:
            print("👥 Navegando a gestión de usuarios...")
            
            # Obtener la ventana principal para cambiar de página
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de Usuarios (índice 10)
                main_window.cambiar_pagina(10, "Gestión de Usuarios")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo navegar a gestión de usuarios")
            
        except Exception as e:
            print(f"❌ Error al abrir gestión de usuarios: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error(f"No se pudo abrir gestión de usuarios: {str(e)}")

    def abrir_realizar_copia_seguridad(self):
        """Abre la página de realizar copia de seguridad"""
        try:
            print("💾 Navegando a realizar copia de seguridad...")
            
            # Obtener la ventana principal para cambiar de página
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de CopiaBDD (índice 11)
                main_window.cambiar_pagina(11, "Realizar Copia de Seguridad")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo navegar a realizar copia de seguridad")
            
        except Exception as e:
            print(f"❌ Error al abrir realizar copia de seguridad: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error(f"No se pudo abrir realizar copia de seguridad: {str(e)}")

    def abrir_restaurar_copia_seguridad(self):
        """Abre la página de restaurar copia de seguridad"""
        try:
            print("📂 Navegando a restaurar copia de seguridad...")
            
            # Obtener la ventana principal para cambiar de página
            main_window = self.get_main_window()
            if main_window:
                # Cambiar a la página de Restaurar (índice 12)
                main_window.cambiar_pagina(12, "Restaurar Copia de Seguridad")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                self.mostrar_error("No se pudo navegar a restaurar copia de seguridad")
            
        except Exception as e:
            print(f"❌ Error al abrir restaurar copia de seguridad: {e}")
            import traceback
            traceback.print_exc()
            self.mostrar_error(f"No se pudo abrir restaurar copia de seguridad: {str(e)}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.seguridad_widget
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
            msg = QtWidgets.QMessageBox(self.seguridad_widget)
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
                self.seguridad_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página de seguridad"""
        print("🔒 Cargando página de seguridad...")
        # Aquí puedes cargar datos iniciales si es necesario

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador de seguridad...")