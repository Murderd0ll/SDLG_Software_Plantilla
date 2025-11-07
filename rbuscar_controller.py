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
                self.pushButton.clicked.connect(self.buscar_registros_reproduccion)
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
                self.lineEdit.returnPressed.connect(self.buscar_registros_reproduccion)
                print("✅ Enter en lineEdit conectado")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

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
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.rbuscar_widget
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

    def buscar_registros_reproduccion(self):
        """Busca los registros de reproducción del animal por arete"""
        try:
            arete = self.lineEdit.text().strip()
            print(f"🔍 Buscando registros de reproducción para arete: {arete}")
            
            if not arete:
                self.mostrar_error("Por favor ingrese un arete")
                return
            
            # Buscar registros de reproducción en la base de datos
            registros_reproduccion = self.db.obtener_registros_reproduccion_por_arete(arete)
            
            if registros_reproduccion:
                print(f"✅ Encontrados {len(registros_reproduccion)} registros de reproducción")
                self.mostrar_resultados(arete, registros_reproduccion)
            else:
                print(f"❌ No se encontraron registros de reproducción para arete: {arete}")
                self.mostrar_informacion(f"No se encontraron registros de reproducción para el animal con arete: {arete}")
                
        except Exception as e:
            print(f"❌ Error al buscar registros de reproducción: {e}")
            self.mostrar_error(f"Error al buscar registros: {str(e)}")

    def mostrar_resultados(self, arete, registros_reproduccion):
        """Muestra los resultados en la misma página en lugar de un diálogo"""
        try:
            # Buscar o crear un widget para mostrar resultados en la misma página
            resultados_widget = self.rbuscar_widget.findChild(QtWidgets.QWidget, "resultadosWidget")
            
            if not resultados_widget:
                # Crear el widget de resultados si no existe
                resultados_widget = QtWidgets.QWidget()
                resultados_widget.setObjectName("resultadosWidget")
                layout = QtWidgets.QVBoxLayout(resultados_widget)
                
                # Título
                titulo = QtWidgets.QLabel(f"Registros de Reproducción - Animal: {arete}")
                titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
                layout.addWidget(titulo)
                
                # Crear tabla
                table = QtWidgets.QTableWidget()
                table.setObjectName("tablaResultados")
                table.setColumnCount(8)
                table.setHorizontalHeaderLabels([
                    "ID", "Tipo Servicio", "Fecha Servicio", "Toro", 
                    "Fecha Diagnóstico", "Resultado", "Observaciones", "Veterinario"
                ])
                layout.addWidget(table)
                
                # Botones
                btn_layout = QtWidgets.QHBoxLayout()
                btn_exportar = QtWidgets.QPushButton("Exportar a PDF")
                btn_exportar.setObjectName("btnExportar")
                btn_limpiar = QtWidgets.QPushButton("Limpiar Búsqueda")
                btn_limpiar.setObjectName("btnLimpiar")
                
                btn_exportar.clicked.connect(lambda: self.exportar_a_pdf(arete, registros_reproduccion))
                btn_limpiar.clicked.connect(self.limpiar_busqueda)
                
                btn_layout.addWidget(btn_exportar)
                btn_layout.addWidget(btn_limpiar)
                layout.addLayout(btn_layout)
                
                # Agregar el widget de resultados al layout principal
                main_layout = self.rbuscar_widget.layout()
                main_layout.addWidget(resultados_widget)
            
            # Obtener la tabla
            table = resultados_widget.findChild(QtWidgets.QTableWidget, "tablaResultados")
            
            if table:
                # Llenar tabla con datos
                table.setRowCount(len(registros_reproduccion))
                for row, registro in enumerate(registros_reproduccion):
                    for col, valor in enumerate(registro[:8]):  # Primeros 8 campos
                        item = QtWidgets.QTableWidgetItem(str(valor) if valor is not None else "")
                        table.setItem(row, col, item)
                
                # Ajustar columnas
                table.resizeColumnsToContents()
                
            print(f"✅ Resultados mostrados en la página para arete: {arete}")
            
        except Exception as e:
            print(f"❌ Error mostrando resultados: {e}")
            self.mostrar_error(f"Error al mostrar resultados: {str(e)}")

    def limpiar_busqueda(self):
        """Limpia la búsqueda y oculta los resultados"""
        try:
            # Limpiar el campo de búsqueda
            if hasattr(self, 'lineEdit') and self.lineEdit:
                self.lineEdit.clear()
            
            # Ocultar o eliminar el widget de resultados
            resultados_widget = self.rbuscar_widget.findChild(QtWidgets.QWidget, "resultadosWidget")
            if resultados_widget:
                resultados_widget.hide()
                
        except Exception as e:
            print(f"❌ Error limpiando búsqueda: {e}")

    def exportar_a_pdf(self, arete, registros_reproduccion):
        """Exporta los registros a PDF (placeholder)"""
        try:
            print(f"📄 Exportando a PDF para arete: {arete}")
            self.mostrar_informacion(f"Funcionalidad de exportación a PDF en desarrollo para arete: {arete}")
        except Exception as e:
            print(f"❌ Error exportando a PDF: {e}")

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
        self.limpiar_busqueda()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador Rbuscar...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()