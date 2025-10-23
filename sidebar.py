# sidebar.py - VERSIÓN CORREGIDA
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt

from sidebar_ui import Ui_MainWindow
from becerros_ui import Ui_BecerrosPage
from becerros_controller import BecerrosController

def cargar_estilos_sidebar(window):
    """Cargar estilos SOLO para el sidebar"""
    try:
        if os.path.exists('stylemenu.qss'):
            with open('stylemenu.qss', 'r', encoding='utf-8') as f:
                estilo = f.read()
            window.setStyleSheet(estilo)
            print("✅ Estilos de sidebar cargados correctamente")
        else:
            print("⚠️  Archivo stylemenu.qss no encontrado")
    except Exception as e:
        print(f"❌ Error cargando estilos sidebar: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # CARGAR ESTILOS DEL SIDEBAR
        cargar_estilos_sidebar(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.indexbtn2.setChecked(True) 
        
        # Inicializar controladores
        self.becerros_controller = None
        
        print("📚 Páginas en stackedWidget:")
        for i in range(self.ui.stackedWidget.count()):
            widget = self.ui.stackedWidget.widget(i)
            print(f"   Página {i}: {widget.objectName()}")
        
        # Reemplazar la página de becerros
        self.reemplazar_pagina_becerros()
        
        # CONECTAR SEÑALES - ESTE MÉTODO SÍ EXISTE
        self.connect_signals()
        
        # Inicializar controlador de becerros
        self.inicializar_controladores()
        
        print(f"✅ Sidebar inicializado - Página actual: {self.ui.stackedWidget.currentIndex()}")
        
    def reemplazar_pagina_becerros(self):
        """Reemplaza la página de becerros existente con tu diseño personalizado"""
        try:
            becerros_page_index = 1
            becerros_widget = QWidget()
            self.becerros_ui = Ui_BecerrosPage()
            self.becerros_ui.setupUi(becerros_widget)
            
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.widget(becerros_page_index))
            self.ui.stackedWidget.insertWidget(becerros_page_index, becerros_widget)
            
            print(f"✅ Página de becerros reemplazada en índice: {becerros_page_index}")
            
        except Exception as e:
            print(f"❌ Error reemplazando página de becerros: {e}")
        
    def inicializar_controladores(self):
        """Inicializa todos los controladores de la aplicación"""
        try:
            becerros_widget = self.ui.stackedWidget.widget(1)
            if becerros_widget:
                self.becerros_controller = BecerrosController(becerros_widget)
                print("✅ Controlador de becerros inicializado correctamente")
            else:
                print("❌ No se pudo obtener el widget de becerros")
        except Exception as e:
            print(f"❌ Error al inicializar controlador: {e}")
        
    def connect_signals(self):  # ✅ ESTE MÉTODO SÍ EXISTE AHORA
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

    def cambiar_pagina(self, index, button_name):
        """Método unificado para cambiar de página"""
        print(f"🔄 Cambiando a página {index} ({button_name})")
        
        self.ui.stackedWidget.setCurrentIndex(index)
        
        if index == 1 and self.becerros_controller:
            print("🐄 Cargando datos de becerros...")
            self.becerros_controller.cargar_becerros()

    # ========== MÉTODOS PARA CADA BOTÓN ==========
    
    def on_indexbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(0, "Página principal")

    def on_indexbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(0, "Página principal")

    def on_becerrosbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(1, "Becerros")

    def on_becerrosbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(1, "Becerros")

    def on_animalesbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(2, "Animales")

    def on_animalesbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(2, "Animales")

    def on_corralesbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Corrales")

    def on_corralesbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Corrales")

    def on_propietariosbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Propietarios")

    def on_propietariosbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Propietarios")

    def on_bitacorabtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(5, "Bitácora")

    def on_bitacorabtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(5, "Bitácora")

    def on_reportesbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(6, "Reportes")

    def on_reportesbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(6, "Reportes")

    def on_seguridadbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(7, "Seguridad")

    def on_seguridadbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(7, "Seguridad")

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        print("🔴 Cerrando aplicación...")
        if self.becerros_controller and self.becerros_controller.db:
            self.becerros_controller.db.disconnect()
        event.accept()