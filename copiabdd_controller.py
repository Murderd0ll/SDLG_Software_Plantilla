from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil
import sqlite3
from datetime import datetime
import sys

class CopiaBDDController:
    def __init__(self, copiabdd_widget):
        self.copiabdd_widget = copiabdd_widget
        self.setup_connections()
        self.configurar_fecha()
        print("✅ CopiaBDDController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para CopiaBDD...")
            
            # Buscar elementos
            self.btn_regresar = self.copiabdd_widget.findChild(QtWidgets.QPushButton, "btnRegresar")
            self.btn_crear = self.copiabdd_widget.findChild(QtWidgets.QPushButton, "pushButton")
            self.date_edit = self.copiabdd_widget.findChild(QtWidgets.QDateEdit, "dateEdit")
            
            if self.btn_regresar:
                self.btn_regresar.clicked.connect(self.regresar_a_seguridad)
                print("✅ Botón regresar conectado")
            else:
                print("❌ No se encontró btnRegresar")
                
            if self.btn_crear:
                self.btn_crear.clicked.connect(self.crear_copia_seguridad)
                print("✅ Botón crear conectado")
            else:
                print("❌ No se encontró pushButton (Crear)")
                
            if self.date_edit:
                print("✅ DateEdit encontrado")
            else:
                print("❌ No se encontró dateEdit")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def configurar_fecha(self):
        """Configura la fecha actual en el dateEdit"""
        try:
            if self.date_edit:
                self.date_edit.setDate(QtCore.QDate.currentDate())
                self.date_edit.setCalendarPopup(True)
                self.date_edit.setDisplayFormat("dd/MM/yyyy")
                print("✅ Fecha configurada correctamente")
        except Exception as e:
            print(f"❌ Error configurando fecha: {e}")

    def regresar_a_seguridad(self):
        """Regresa a la página de Seguridad"""
        try:
            print("🔙 Regresando a página de Seguridad...")
            main_window = self.get_main_window()
            if main_window:
                main_window.cambiar_pagina(7, "Seguridad")
            else:
                print("❌ No se pudo encontrar la ventana principal")
        except Exception as e:
            print(f"❌ Error al regresar a seguridad: {e}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.copiabdd_widget
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

    def crear_copia_seguridad(self):
        """Crea una copia de seguridad de la base de datos"""
        try:
            # Obtener la fecha seleccionada
            fecha = self.date_edit.date().toString("dd-MM-yyyy")
            print(f"💾 Creando copia de seguridad para la fecha: {fecha}")
            
            # Ruta de la base de datos original
            db_path = "bdd/SDLGAPP.db"
            
            # Verificar si existe la base de datos
            if not os.path.exists(db_path):
                self.mostrar_error("No se encontró la base de datos original.")
                return
            
            # Crear directorio de backups si no existe
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                print(f"✅ Directorio de backups creado: {backup_dir}")
            
            # Nombre del archivo de backup
            backup_name = f"SDLGAPP_backup_{fecha}.db"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Verificar si ya existe un backup para esa fecha
            if os.path.exists(backup_path):
                respuesta = QtWidgets.QMessageBox.question(
                    self.copiabdd_widget,
                    "Copia existente",
                    f"Ya existe una copia de seguridad para la fecha {fecha}. ¿Desea reemplazarla?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.No
                )
                if respuesta == QtWidgets.QMessageBox.No:
                    return
            
            # Crear la copia de seguridad
            self.realizar_copia_seguridad(db_path, backup_path, fecha)
            
        except Exception as e:
            print(f"❌ Error al crear copia de seguridad: {e}")
            self.mostrar_error(f"Error al crear copia de seguridad: {str(e)}")

    def realizar_copia_seguridad(self, origen, destino, fecha):
        """Realiza la copia de seguridad de la base de datos"""
        try:
            # Mostrar progreso
            progress_dialog = QtWidgets.QProgressDialog("Creando copia de seguridad...", "Cancelar", 0, 100, self.copiabdd_widget)
            progress_dialog.setWindowTitle("Procesando")
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            
            # Simular progreso
            for i in range(101):
                QtCore.QThread.msleep(20)  # Pequeña pausa para simular trabajo
                progress_dialog.setValue(i)
                QtWidgets.QApplication.processEvents()
                
                if progress_dialog.wasCanceled():
                    progress_dialog.close()
                    self.mostrar_informacion("Copia de seguridad cancelada.")
                    return
            
            progress_dialog.close()
            
            # Realizar la copia real del archivo
            shutil.copy2(origen, destino)
            
            # Verificar que se creó correctamente
            if os.path.exists(destino):
                tamaño_original = os.path.getsize(origen)
                tamaño_backup = os.path.getsize(destino)
                
                mensaje = f"""
✅ Copia de seguridad creada exitosamente

📊 Detalles:
• Fecha: {fecha}
• Archivo: {os.path.basename(destino)}
• Tamaño original: {self.formatear_tamaño(tamaño_original)}
• Tamaño backup: {self.formatear_tamaño(tamaño_backup)}
• Ubicación: {destino}
                """
                
                self.mostrar_informacion(mensaje)
                print(f"✅ Copia de seguridad creada: {destino}")
                
                # Registrar en logs
                self.registrar_backup(fecha, destino, tamaño_backup)
            else:
                self.mostrar_error("No se pudo crear la copia de seguridad.")
                
        except Exception as e:
            print(f"❌ Error en realizar_copia_seguridad: {e}")
            self.mostrar_error(f"Error durante la copia: {str(e)}")

    def formatear_tamaño(self, bytes):
        """Formatea el tamaño en bytes a formato legible"""
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unidad}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"

    def registrar_backup(self, fecha, archivo, tamaño):
        """Registra el backup en un archivo de log"""
        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file = os.path.join(log_dir, "backups.log")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] Backup creado - Fecha: {fecha}, Archivo: {archivo}, Tamaño: {tamaño} bytes\n")
            
            print(f"✅ Backup registrado en log: {log_file}")
            
        except Exception as e:
            print(f"⚠️ Error registrando backup en log: {e}")

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.copiabdd_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def mostrar_informacion(self, mensaje):
        """Muestra un mensaje informativo"""
        try:
            msg = QtWidgets.QMessageBox(self.copiabdd_widget)
            msg.setWindowTitle("Éxito")
            msg.setText(mensaje)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()
        except Exception as e:
            print(f"❌ Error mostrando mensaje informativo: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("💾 Cargando página de copia de seguridad...")
        # Configurar fecha actual cada vez que se abre la página
        self.configurar_fecha()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador CopiaBDD...")