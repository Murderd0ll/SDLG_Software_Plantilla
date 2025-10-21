# sidebar.py (modificado para usar las páginas existentes)
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt

from menu_ui import Ui_MainWindow
from becerros_ui import Ui_BecerrosPage  # Tu diseño de becerros
from becerros_controller import BecerrosController

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.indexbtn2.setChecked(True) 
        
        # Inicializar controladores
        self.becerros_controller = None
        
        # DEBUG: Ver páginas actuales
        print("📚 Páginas en stackedWidget:")
        for i in range(self.ui.stackedWidget.count()):
            widget = self.ui.stackedWidget.widget(i)
            print(f"   Página {i}: {widget.objectName()}")
        
        # Reemplazar la página de becerros existente con tu diseño
        self.reemplazar_pagina_becerros()
        
        # Conectar señales
        self.connect_signals()
        
        # Inicializar controlador de becerros
        self.inicializar_controladores()
        
        print(f"✅ Sidebar inicializado - Página actual: {self.ui.stackedWidget.currentIndex()}")
        
    def reemplazar_pagina_becerros(self):
        """Reemplaza la página de becerros existente con tu diseño personalizado"""
        try:
            # La página de becerros está en el índice 1 (page_2)
            becerros_page_index = 1
            
            # Crear tu diseño de becerros
            becerros_widget = QWidget()
            self.becerros_ui = Ui_BecerrosPage()
            self.becerros_ui.setupUi(becerros_widget)
            
            # Reemplazar la página existente
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.widget(becerros_page_index))
            self.ui.stackedWidget.insertWidget(becerros_page_index, becerros_widget)
            
            print(f"✅ Página de becerros reemplazada en índice: {becerros_page_index}")
            
        except Exception as e:
            print(f"❌ Error reemplazando página de becerros: {e}")
        
    def inicializar_controladores(self):
        """Inicializa todos los controladores de la aplicación"""
        try:
            # Obtener el widget de becerros del stackedWidget (índice 1)
            becerros_widget = self.ui.stackedWidget.widget(1)
            if becerros_widget:
                self.becerros_controller = BecerrosController(becerros_widget)
                print("✅ Controlador de becerros inicializado correctamente")
            else:
                print("❌ No se pudo obtener el widget de becerros")
        except Exception as e:
            print(f"❌ Error al inicializar controlador: {e}")
        
    def connect_signals(self):
        """Conectar todas las señales de los botones de manera segura"""
        try:
            # Botones del índice/inicio
            self._connect_button(self.ui.indexbtn1, self.on_indexbtn1_toggled)
            self._connect_button(self.ui.indexbtn2, self.on_indexbtn2_toggled)
            
            # Botones de becerros
            self._connect_button(self.ui.becerrosbtn1, self.on_becerrosbtn1_toggled)
            self._connect_button(self.ui.becerrosbtn2, self.on_becerrosbtn2_toggled)
            
            # Resto de las conexiones...
            self._connect_button(self.ui.animalesbtn1, self.on_animalesbtn1_toggled)
            self._connect_button(self.ui.animalesbtn2, self.on_animalesbtn2_toggled)
            self._connect_button(self.ui.corralesbtn1, self.on_corralesbtn1_toggled)
            self._connect_button(self.ui.corralesbtn2, self.on_corralesbtn2_toggled)
            self._connect_button(self.ui.propietariosbtn1, self.on_propietariosbtn1_toggled)
            self._connect_button(self.ui.propietariosbtn2, self.on_propietariosbtn2_toggled)
            self._connect_button(self.ui.bitacorabtn1, self.on_bitacorabtn1_toggled)
            self._connect_button(self.ui.bitacorabtn2, self.on_bitacorabtn2_toggled)
            self._connect_button(self.ui.reportesbtn1, self.on_reportesbtn1_toggled)
            self._connect_button(self.ui.reportesbtn2, self.on_reportesbtn2_toggled)
            self._connect_button(self.ui.seguridadbtn1, self.on_seguridadbtn1_toggled)
            self._connect_button(self.ui.seguridadbtn2, self.on_seguridadbtn2_toggled)
            
            # Conectar botón de cerrar sesión
            if hasattr(self.ui, 'cerrarbtn1'):
                self.ui.cerrarbtn1.clicked.connect(self.close)
            if hasattr(self.ui, 'cerrarbtn2'):
                self.ui.cerrarbtn2.clicked.connect(self.close)
            
            print("✅ Todas las señales conectadas correctamente")
            
        except Exception as e:
            print(f"❌ Error conectando señales: {e}")
    
    def _connect_button(self, button, handler):
        """Conecta un botón de manera segura"""
        if button:
            button.toggled.connect(handler)
        else:
            print(f"⚠️ Botón no encontrado: {button}")

    # ========== MÉTODOS PARA CADA BOTÓN ==========
    
    def on_indexbtn1_toggled(self):
        if self.ui.indexbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
            print("🏠 Cambiando a página de inicio")

    def on_indexbtn2_toggled(self):
        if self.ui.indexbtn2.isChecked():
            self.ui.stackedWidget.setCurrentIndex(0)
            print("🏠 Cambiando a página de inicio")

    def on_becerrosbtn1_toggled(self):
        if self.ui.becerrosbtn1.isChecked():
            print("🐄 Cambiando a página de becerros...")
            self.ui.stackedWidget.setCurrentIndex(1)  # Índice 1 para becerros
                
            if self.becerros_controller:
                print("🔄 Cargando datos de becerros...")
                self.becerros_controller.cargar_becerros()
            else:
                print("⚠️ Controlador de becerros no disponible")

    def on_becerrosbtn2_toggled(self):
        if self.ui.becerrosbtn2.isChecked():
            self.on_becerrosbtn1_toggled()

    def on_animalesbtn1_toggled(self):
        if self.ui.animalesbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(2)  # Índice 2 para animales
            print("🐮 Cambiando a página de animales")

    def on_animalesbtn2_toggled(self):
        if self.ui.animalesbtn2.isChecked():
            self.on_animalesbtn1_toggled()

    def on_corralesbtn1_toggled(self):
        if self.ui.corralesbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(3)  # Índice 3 para corrales
            print("🏠 Cambiando a página de corrales")

    def on_corralesbtn2_toggled(self):
        if self.ui.corralesbtn2.isChecked():
            self.on_corralesbtn1_toggled()

    def on_propietariosbtn1_toggled(self):
        if self.ui.propietariosbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(4)  # Índice 4 para propietarios
            print("👤 Cambiando a página de propietarios")

    def on_propietariosbtn2_toggled(self):
        if self.ui.propietariosbtn2.isChecked():
            self.on_propietariosbtn1_toggled()

    def on_bitacorabtn1_toggled(self):
        if self.ui.bitacorabtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(5)  # Índice 5 para bitácora
            print("📝 Cambiando a página de bitácora")

    def on_bitacorabtn2_toggled(self):
        if self.ui.bitacorabtn2.isChecked():
            self.on_bitacorabtn1_toggled()

    def on_reportesbtn1_toggled(self):
        if self.ui.reportesbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(6)  # Índice 6 para reportes
            print("📊 Cambiando a página de reportes")

    def on_reportesbtn2_toggled(self):
        if self.ui.reportesbtn2.isChecked():
            self.on_reportesbtn1_toggled()

    def on_seguridadbtn1_toggled(self):
        if self.ui.seguridadbtn1.isChecked():
            self.ui.stackedWidget.setCurrentIndex(7)  # Índice 7 para seguridad
            print("🔒 Cambiando a página de seguridad")

    def on_seguridadbtn2_toggled(self):
        if self.ui.seguridadbtn2.isChecked():
            self.on_seguridadbtn1_toggled()

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        print("🔴 Cerrando aplicación...")
        if self.becerros_controller and self.becerros_controller.db:
            self.becerros_controller.db.disconnect()
        event.accept()