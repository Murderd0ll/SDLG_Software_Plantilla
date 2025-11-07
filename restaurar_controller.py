from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil
import sqlite3
from datetime import datetime
import sys

class RestaurarController:
    def __init__(self, restaurar_widget):
        self.restaurar_widget = restaurar_widget
        self.setup_connections()
        self.cargar_backups()
        print("✅ RestaurarController inicializado")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para Restaurar...")
            
            # Buscar elementos
            self.btn_regresar = self.restaurar_widget.findChild(QtWidgets.QPushButton, "btnRegresar")
            self.btn_restaurar = self.restaurar_widget.findChild(QtWidgets.QPushButton, "pushButton")
            self.combo_backups = self.restaurar_widget.findChild(QtWidgets.QComboBox, "comboBox")
            
            if self.btn_regresar:
                self.btn_regresar.clicked.connect(self.regresar_a_seguridad)
                print("✅ Botón regresar conectado")
            else:
                print("❌ No se encontró btnRegresar")
                
            if self.btn_restaurar:
                self.btn_restaurar.clicked.connect(self.restaurar_backup)
                print("✅ Botón restaurar conectado")
            else:
                print("❌ No se encontró pushButton (Restaurar)")
                
            if self.combo_backups:
                print("✅ ComboBox encontrado")
            else:
                print("❌ No se encontró comboBox")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def cargar_backups(self):
        """Carga la lista de backups disponibles en el ComboBox"""
        try:
            print("🔄 Cargando lista de backups...")
            
            # Limpiar comboBox
            self.combo_backups.clear()
            
            # Directorio de backups
            backup_dir = "backups"
            
            if not os.path.exists(backup_dir):
                print("⚠️ No existe directorio de backups")
                self.combo_backups.addItem("No hay backups disponibles")
                return
            
            # Buscar archivos .db en el directorio de backups
            backups = []
            for archivo in os.listdir(backup_dir):
                if archivo.endswith('.db') and 'backup' in archivo.lower():
                    ruta_completa = os.path.join(backup_dir, archivo)
                    tamaño = os.path.getsize(ruta_completa)
                    fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                    
                    backups.append({
                        'archivo': archivo,
                        'ruta': ruta_completa,
                        'tamaño': tamaño,
                        'fecha_mod': fecha_modificacion
                    })
            
            # Ordenar por fecha de modificación (más reciente primero)
            backups.sort(key=lambda x: x['fecha_mod'], reverse=True)
            
            if not backups:
                self.combo_backups.addItem("No hay backups disponibles")
                print("ℹ️ No se encontraron backups")
                return
            
            # Agregar backups al ComboBox
            for backup in backups:
                fecha_str = backup['fecha_mod'].strftime("%d/%m/%Y %H:%M")
                tamaño_str = self.formatear_tamaño(backup['tamaño'])
                display_text = f"{backup['archivo']} - {fecha_str} - {tamaño_str}"
                
                self.combo_backups.addItem(display_text, backup['ruta'])
            
            print(f"✅ {len(backups)} backups cargados en el ComboBox")
            
        except Exception as e:
            print(f"❌ Error cargando backups: {e}")
            self.combo_backups.addItem("Error al cargar backups")

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
            parent = self.restaurar_widget
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

    def restaurar_backup(self):
        """Restaura el backup seleccionado"""
        try:
            # Verificar si hay backups disponibles
            if self.combo_backups.count() == 0 or "No hay backups" in self.combo_backups.currentText():
                self.mostrar_error("No hay backups disponibles para restaurar.")
                return
            
            # Obtener la ruta del backup seleccionado
            backup_ruta = self.combo_backups.currentData()
            
            if not backup_ruta or not os.path.exists(backup_ruta):
                self.mostrar_error("El backup seleccionado no es válido o no existe.")
                return
            
            # Ruta de la base de datos original
            db_original = "bdd/SDLGAPP.db"
            
            # Confirmar restauración
            respuesta = QtWidgets.QMessageBox.question(
                self.restaurar_widget,
                "Confirmar Restauración",
                f"¿Está seguro de que desea restaurar el backup?\n\n"
                f"Backup: {os.path.basename(backup_ruta)}\n"
                f"Esta acción reemplazará la base de datos actual.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if respuesta == QtWidgets.QMessageBox.No:
                return
            
            # Realizar la restauración
            self.ejecutar_restauracion(backup_ruta, db_original)
            
        except Exception as e:
            print(f"❌ Error al restaurar backup: {e}")
            self.mostrar_error(f"Error al restaurar backup: {str(e)}")

    def ejecutar_restauracion(self, backup_ruta, db_original):
        """Ejecuta el proceso de restauración"""
        try:
            # Mostrar progreso
            progress_dialog = QtWidgets.QProgressDialog("Restaurando copia de seguridad...", "Cancelar", 0, 100, self.restaurar_widget)
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
                    self.mostrar_informacion("Restauración cancelada.")
                    return
            
            progress_dialog.close()
            
            # Crear backup de la base de datos actual antes de restaurar
            if os.path.exists(db_original):
                backup_actual = f"backups/SDLGAPP_backup_pre_restore_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.db"
                shutil.copy2(db_original, backup_actual)
                print(f"✅ Backup de BD actual creado: {backup_actual}")
            
            # Realizar la restauración
            shutil.copy2(backup_ruta, db_original)
            
            # Verificar que se restauró correctamente
            if os.path.exists(db_original):
                tamaño_original = os.path.getsize(backup_ruta)
                tamaño_restaurado = os.path.getsize(db_original)
                
                if tamaño_original == tamaño_restaurado:
                    mensaje = f"""
✅ Restauración completada exitosamente

📊 Detalles:
• Backup restaurado: {os.path.basename(backup_ruta)}
• Tamaño: {self.formatear_tamaño(tamaño_restaurado)}
• Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🔄 La aplicación se reiniciará para aplicar los cambios.
                    """
                    
                    # Registrar en logs
                    self.registrar_restauracion(backup_ruta, tamaño_restaurado)
                    
                    # Mostrar mensaje y reiniciar
                    self.mostrar_reinicio(mensaje)
                else:
                    self.mostrar_error("Error: Los tamaños no coinciden. La restauración puede estar corrupta.")
            else:
                self.mostrar_error("No se pudo restaurar la base de datos.")
                
        except Exception as e:
            print(f"❌ Error en ejecutar_restauracion: {e}")
            self.mostrar_error(f"Error durante la restauración: {str(e)}")

    def formatear_tamaño(self, bytes):
        """Formatea el tamaño en bytes a formato legible"""
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unidad}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"

    def registrar_restauracion(self, backup_ruta, tamaño):
        """Registra la restauración en un archivo de log"""
        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file = os.path.join(log_dir, "restauraciones.log")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] Restauración - Backup: {backup_ruta}, Tamaño: {tamaño} bytes\n")
            
            print(f"✅ Restauración registrada en log: {log_file}")
            
        except Exception as e:
            print(f"⚠️ Error registrando restauración en log: {e}")

    def mostrar_reinicio(self, mensaje):
        """Muestra mensaje de reinicio"""
        try:
            msg = QtWidgets.QMessageBox(self.restaurar_widget)
            msg.setWindowTitle("Restauración Completada")
            msg.setText(mensaje)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
            # Conectar el botón OK para reiniciar la aplicación
            msg.buttonClicked.connect(self.reiniciar_aplicacion)
            msg.exec_()
            
        except Exception as e:
            print(f"❌ Error mostrando mensaje de reinicio: {e}")

    def reiniciar_aplicacion(self):
        """Reinicia la aplicación"""
        try:
            print("🔄 Reiniciando aplicación...")
            QtWidgets.QApplication.quit()
            # En un entorno real, aquí reiniciarías la aplicación
            # os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            print(f"❌ Error reiniciando aplicación: {e}")

    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        try:
            QtWidgets.QMessageBox.critical(
                self.restaurar_widget,
                "Error",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje de error: {e}")

    def mostrar_informacion(self, mensaje):
        """Muestra un mensaje informativo"""
        try:
            QtWidgets.QMessageBox.information(
                self.restaurar_widget,
                "Información",
                mensaje
            )
        except Exception as e:
            print(f"❌ Error mostrando mensaje informativo: {e}")

    def cargar_datos(self):
        """Método para cargar datos cuando se abre la página"""
        print("🔄 Cargando página de restauración...")
        # Recargar lista de backups cada vez que se abre la página
        self.cargar_backups()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Restaurar...")