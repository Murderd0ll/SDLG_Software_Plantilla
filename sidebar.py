# sidebar.py - VERSIÓN COMPLETA DEFINITIVA CON TODAS LAS PÁGINAS
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt

from sidebar_ui import Ui_MainWindow
from ui.becerros_ui import Ui_BecerrosPage
from ui.animales_ui import Ui_AnimalesPage
from ui.propietarios_ui import Ui_PropietariosPage
from ui.corrales_ui import Ui_CorralesPage
from sbuscar_ui import Ui_SbuscarPage
from rbuscar_ui import Ui_RbuscarPage
from usuarios_ui import Ui_UsuariosPage
from copiabdd_ui import Ui_CopiaBDDPage
from restaurar_ui import Ui_RestaurarPage
from index_ui import Ui_IndexPage
from reportes_ui import Ui_ReportesPage
from seguridad_ui import Ui_SeguridadPage

from controllers.becerros_controller import BecerrosController
from controllers.animales_controller import AnimalesController
from controllers.propietarios_controller import PropietariosController
from controllers.corrales_controller import CorralesController
from sbuscar_controller import SbuscarController
from rbuscar_controller import RbuscarController
from usuarios_controller import UsuariosController
from copiabdd_controller import CopiaBDDController
from restaurar_controller import RestaurarController
from controllers.index_controller import MainController
from reportes_controller import ReportesController
from seguridad_controller import SeguridadController


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
        
        # ✅ LIMPIAR COMPLETAMENTE EL STACKEDWIDGET Y CREARLO DESDE CERO
        self.recrear_stackedwidget_completo()
        
        # CONECTAR SEÑALES
        self.connect_signals()
        
        print(f"✅ Sidebar inicializado - Página actual: {self.ui.stackedWidget.currentIndex()}")
    
    def recrear_stackedwidget_completo(self):
        """Recrea completamente el stackedWidget en el orden correcto"""
        try:
            print("🔄 Recreando stackedWidget completo...")
            
            # 1. LIMPIAR TODAS LAS PÁGINAS EXISTENTES
            while self.ui.stackedWidget.count() > 0:
                widget = self.ui.stackedWidget.widget(0)
                if widget:
                    self.ui.stackedWidget.removeWidget(widget)
            
            # 2. CREAR PÁGINAS EN EL ORDEN CORRECTO
            
            # ✅ PÁGINA PRINCIPAL - ÍNDICE 0
            main_widget = QWidget()
            self.main_ui = Ui_IndexPage()
            self.main_ui.setupUi(main_widget)
            self.ui.stackedWidget.addWidget(main_widget)
            self.main_controller = MainController(main_widget)
            print("✅ Página principal creada en índice 0")
            
            # ✅ PÁGINA BECERROS - ÍNDICE 1
            becerros_widget = QWidget()
            self.becerros_ui = Ui_BecerrosPage()
            self.becerros_ui.setupUi(becerros_widget)
            self.ui.stackedWidget.addWidget(becerros_widget)
            self.becerros_controller = BecerrosController(becerros_widget)
            print("✅ Página becerros creada en índice 1")
            
            # ✅ PÁGINA ANIMALES - ÍNDICE 2
            animales_widget = QWidget()
            self.animales_ui = Ui_AnimalesPage()
            self.animales_ui.setupUi(animales_widget)
            self.ui.stackedWidget.addWidget(animales_widget)
            self.animales_controller = AnimalesController(animales_widget)
            print("✅ Página animales creada en índice 2")
            
            # ✅ PÁGINA PROPIETARIOS - ÍNDICE 3
            propietarios_widget = QWidget()
            self.propietarios_ui = Ui_PropietariosPage()
            self.propietarios_ui.setupUi(propietarios_widget)
            self.ui.stackedWidget.addWidget(propietarios_widget)
            self.propietarios_controller = PropietariosController(propietarios_widget)
            print("✅ Página propietarios creada en índice 3")
            
            # ✅ PÁGINA CORRALES - ÍNDICE 4
            corrales_widget = QWidget()
            self.corrales_ui = Ui_CorralesPage()
            self.corrales_ui.setupUi(corrales_widget)
            self.ui.stackedWidget.addWidget(corrales_widget)
            self.corrales_controller = CorralesController(corrales_widget)
            print("✅ Página corrales creada en índice 4")
            
            # ✅ PÁGINA BITÁCORA - ÍNDICE 5
            bitacora_widget = QWidget()
            bitacora_widget.setObjectName("BitacoraPage")
            self.ui.stackedWidget.addWidget(bitacora_widget)
            print("✅ Página bitácora (placeholder) creada en índice 5")
            
            # ✅ PÁGINA REPORTES - ÍNDICE 6
            reportes_widget = QWidget()
            self.reportes_ui = Ui_ReportesPage()
            self.reportes_ui.setupUi(reportes_widget)
            self.ui.stackedWidget.addWidget(reportes_widget)
            self.reportes_controller = ReportesController(reportes_widget)
            print("✅ Página reportes creada en índice 6")
            
            # ✅ PÁGINA SEGURIDAD - ÍNDICE 7
            seguridad_widget = QWidget()
            self.seguridad_ui = Ui_SeguridadPage()
            self.seguridad_ui.setupUi(seguridad_widget)
            self.ui.stackedWidget.addWidget(seguridad_widget)
            self.seguridad_controller = SeguridadController(seguridad_widget)
            print("✅ Página seguridad creada en índice 7")
            
            # ✅ PÁGINA SBUSCAR (REPORTES SALUD) - ÍNDICE 8
            sbuscar_widget = QWidget()
            self.sbuscar_ui = Ui_SbuscarPage()
            self.sbuscar_ui.setupUi(sbuscar_widget)
            self.ui.stackedWidget.addWidget(sbuscar_widget)
            self.sbuscar_controller = SbuscarController(sbuscar_widget)
            print("✅ Página Sbuscar (Reportes Salud) creada en índice 8")
            
            # ✅ PÁGINA RBUSCAR (REPORTES REPRODUCCIÓN) - ÍNDICE 9
            rbuscar_widget = QWidget()
            self.rbuscar_ui = Ui_RbuscarPage()
            self.rbuscar_ui.setupUi(rbuscar_widget)
            self.ui.stackedWidget.addWidget(rbuscar_widget)
            self.rbuscar_controller = RbuscarController(rbuscar_widget)
            print("✅ Página Rbuscar (Reportes Reproducción) creada en índice 9")
            
            # ✅ PÁGINA USUARIOS - ÍNDICE 10
            usuarios_widget = QWidget()
            self.usuarios_ui = Ui_UsuariosPage()
            self.usuarios_ui.setupUi(usuarios_widget)
            self.ui.stackedWidget.addWidget(usuarios_widget)
            self.usuarios_controller = UsuariosController(usuarios_widget)
            print("✅ Página Usuarios creada en índice 10")
            
            # ✅ PÁGINA COPIA BDD - ÍNDICE 11
            copiabdd_widget = QWidget()
            self.copiabdd_ui = Ui_CopiaBDDPage()
            self.copiabdd_ui.setupUi(copiabdd_widget)
            self.ui.stackedWidget.addWidget(copiabdd_widget)
            self.copiabdd_controller = CopiaBDDController(copiabdd_widget)
            print("✅ Página CopiaBDD creada en índice 11")
            
            # ✅ PÁGINA RESTAURAR - ÍNDICE 12
            restaurar_widget = QWidget()
            self.restaurar_ui = Ui_RestaurarPage()
            self.restaurar_ui.setupUi(restaurar_widget)
            self.ui.stackedWidget.addWidget(restaurar_widget)
            self.restaurar_controller = RestaurarController(restaurar_widget)
            print("✅ Página Restaurar creada en índice 12")
            
            # 3. CONFIGURAR PÁGINA PRINCIPAL COMO INICIAL
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.indexbtn2.setChecked(True)
            
            # 4. DIAGNÓSTICO FINAL
            print("📊 DIAGNÓSTICO FINAL DE PÁGINAS:")
            for i in range(self.ui.stackedWidget.count()):
                widget = self.ui.stackedWidget.widget(i)
                nombre = widget.objectName() if widget else "Sin nombre"
                print(f"   📄 Página {i}: {nombre}")
                
        except Exception as e:
            print(f"❌ Error recreando stackedWidget: {e}")
            import traceback
            traceback.print_exc()

    def connect_signals(self):
        """Conectar todas las señales de los botones de manera segura"""
        try:
            # Botones del índice/inicio
            self._connect_button(self.ui.indexbtn1, self.on_indexbtn1_toggled)
            self._connect_button(self.ui.indexbtn2, self.on_indexbtn2_toggled)
            
            # Botones de becerros
            self._connect_button(self.ui.becerrosbtn1, self.on_becerrosbtn1_toggled)
            self._connect_button(self.ui.becerrosbtn2, self.on_becerrosbtn2_toggled)
            
            # Botones de animales
            self._connect_button(self.ui.animalesbtn1, self.on_animalesbtn1_toggled)
            self._connect_button(self.ui.animalesbtn2, self.on_animalesbtn2_toggled)
            
            # Botones de propietarios
            self._connect_button(self.ui.propietariosbtn1, self.on_propietariosbtn1_toggled)
            self._connect_button(self.ui.propietariosbtn2, self.on_propietariosbtn2_toggled)
            
            # Botones de corrales
            self._connect_button(self.ui.corralesbtn1, self.on_corralesbtn1_toggled)
            self._connect_button(self.ui.corralesbtn2, self.on_corralesbtn2_toggled)
            
            # Resto de las conexiones...
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
            import traceback
            traceback.print_exc()
    
    def _connect_button(self, button, handler):
        """Conecta un botón de manera segura"""
        if button:
            button.toggled.connect(handler)
        else:
            print(f"⚠️ Botón no encontrado: {button}")

    def cambiar_pagina(self, index, button_name):
        """Método unificado para cambiar de página - MEJORADO"""
        print(f"🔄 Cambiando a página {index} ({button_name})")
    
        try:
            # ✅ VERIFICAR SI LA PÁGINA EXISTE ANTES DE CAMBIAR
            if index >= self.ui.stackedWidget.count():
                print(f"❌ Índice {index} no existe, máximo es {self.ui.stackedWidget.count()-1}")
                return
            
            # ✅ ACTUALIZAR BOTONES DEL SIDEBAR PRIMERO
            self.actualizar_botones_sidebar(index)
            
            # ✅ CAMBIAR LA PÁGINA
            self.ui.stackedWidget.setCurrentIndex(index)
            
            # CARGAR DATOS SEGÚN LA PÁGINA
            if index == 0:  # Página principal
                if hasattr(self, 'main_controller') and self.main_controller:
                    print("🏠 Cargando estadísticas de página principal...")
                    self.main_controller.cargar_estadisticas()
            elif index == 1:  # Becerros
                if hasattr(self, 'becerros_controller') and self.becerros_controller:
                    print("🐄 Cargando datos de becerros...")
                    self.becerros_controller.cargar_becerros()
            elif index == 2:  # Animales
                if hasattr(self, 'animales_controller') and self.animales_controller:
                    print("🐮 Cargando datos de animales...")
                    self.animales_controller.cargar_animales()
            elif index == 3:  # Propietarios
                if hasattr(self, 'propietarios_controller') and self.propietarios_controller:
                    print("👤 Cargando datos de propietarios...")
                    self.propietarios_controller.cargar_propietarios()
            elif index == 4:  # Corrales
                if hasattr(self, 'corrales_controller') and self.corrales_controller:
                    print("🏠 Cargando datos de corrales...")
                    self.corrales_controller.cargar_corrales()
            elif index == 5:  # Bitácora
                print("📝 Página de bitácora - Sin controlador")
                # Aquí puedes agregar el controlador de bitácora cuando lo tengas
            elif index == 6:  # Reportes
                if hasattr(self, 'reportes_controller') and self.reportes_controller:
                    print("📊 Cargando página de reportes...")
                    self.reportes_controller.cargar_datos()
            elif index == 7:  # Seguridad
                if hasattr(self, 'seguridad_controller') and self.seguridad_controller:
                    print("🔒 Cargando página de seguridad...")
                    self.seguridad_controller.cargar_datos()
            elif index == 8:  # Sbuscar - Reportes de Salud
                if hasattr(self, 'sbuscar_controller') and self.sbuscar_controller:
                    print("🏥 Cargando página de reportes de salud...")
                    self.sbuscar_controller.cargar_datos()
            elif index == 9:  # Rbuscar - Reportes de Reproducción
                if hasattr(self, 'rbuscar_controller') and self.rbuscar_controller:
                    print("🐄 Cargando página de reportes de reproducción...")
                    self.rbuscar_controller.cargar_datos()
            elif index == 10:  # Usuarios
                if hasattr(self, 'usuarios_controller') and self.usuarios_controller:
                    print("👥 Cargando página de gestión de usuarios...")
                    self.usuarios_controller.cargar_datos()
            elif index == 11:  # CopiaBDD
                if hasattr(self, 'copiabdd_controller') and self.copiabdd_controller:
                    print("💾 Cargando página de copia de seguridad...")
                    self.copiabdd_controller.cargar_datos()
            elif index == 12:  # Restaurar
                if hasattr(self, 'restaurar_controller') and self.restaurar_controller:
                    print("📂 Cargando página de restauración...")
                    self.restaurar_controller.cargar_datos()
                    
        except Exception as e:
            print(f"❌ Error cambiando a página {index}: {e}")
            import traceback
            traceback.print_exc()
            
    def actualizar_botones_sidebar(self, index):
        """Actualizar el estado de los botones del sidebar según la página actual"""
        try:
            print(f"🔘 Actualizando botones del sidebar para la página {index}...")
            
            # Desmarcar todos los botones primero
            botones = [
                self.ui.indexbtn1, self.ui.indexbtn2,
                self.ui.becerrosbtn1, self.ui.becerrosbtn2,
                self.ui.animalesbtn1, self.ui.animalesbtn2,
                self.ui.propietariosbtn1, self.ui.propietariosbtn2,
                self.ui.corralesbtn1, self.ui.corralesbtn2,
                self.ui.bitacorabtn1, self.ui.bitacorabtn2,
                self.ui.reportesbtn1, self.ui.reportesbtn2,
                self.ui.seguridadbtn1, self.ui.seguridadbtn2
            ]
            
            for btn in botones:
                if btn:
                    # Usar blockSignals para evitar bucles infinitos
                    btn.blockSignals(True)
                    btn.setChecked(False)
                    btn.blockSignals(False)
            
            # Marcar el botón correspondiente según el índice
            if index == 0:  # Página principal
                if self.ui.indexbtn1:
                    self.ui.indexbtn1.blockSignals(True)
                    self.ui.indexbtn1.setChecked(True)
                    self.ui.indexbtn1.blockSignals(False)
                if self.ui.indexbtn2:
                    self.ui.indexbtn2.blockSignals(True)
                    self.ui.indexbtn2.setChecked(True)
                    self.ui.indexbtn2.blockSignals(False)
                    
            elif index == 1:  # Becerros
                if self.ui.becerrosbtn1:
                    self.ui.becerrosbtn1.blockSignals(True)
                    self.ui.becerrosbtn1.setChecked(True)
                    self.ui.becerrosbtn1.blockSignals(False)
                if self.ui.becerrosbtn2:
                    self.ui.becerrosbtn2.blockSignals(True)
                    self.ui.becerrosbtn2.setChecked(True)
                    self.ui.becerrosbtn2.blockSignals(False)
                    
            elif index == 2:  # Animales
                if self.ui.animalesbtn1:
                    self.ui.animalesbtn1.blockSignals(True)
                    self.ui.animalesbtn1.setChecked(True)
                    self.ui.animalesbtn1.blockSignals(False)
                if self.ui.animalesbtn2:
                    self.ui.animalesbtn2.blockSignals(True)
                    self.ui.animalesbtn2.setChecked(True)
                    self.ui.animalesbtn2.blockSignals(False)
                    
            elif index == 3:  # Propietarios
                if self.ui.propietariosbtn1:
                    self.ui.propietariosbtn1.blockSignals(True)
                    self.ui.propietariosbtn1.setChecked(True)
                    self.ui.propietariosbtn1.blockSignals(False)
                if self.ui.propietariosbtn2:
                    self.ui.propietariosbtn2.blockSignals(True)
                    self.ui.propietariosbtn2.setChecked(True)
                    self.ui.propietariosbtn2.blockSignals(False)
                    
            elif index == 4:  # Corrales
                if self.ui.corralesbtn1:
                    self.ui.corralesbtn1.blockSignals(True)
                    self.ui.corralesbtn1.setChecked(True)
                    self.ui.corralesbtn1.blockSignals(False)
                if self.ui.corralesbtn2:
                    self.ui.corralesbtn2.blockSignals(True)
                    self.ui.corralesbtn2.setChecked(True)
                    self.ui.corralesbtn2.blockSignals(False)
                    
            elif index == 5:  # Bitácora
                if self.ui.bitacorabtn1:
                    self.ui.bitacorabtn1.blockSignals(True)
                    self.ui.bitacorabtn1.setChecked(True)
                    self.ui.bitacorabtn1.blockSignals(False)
                if self.ui.bitacorabtn2:
                    self.ui.bitacorabtn2.blockSignals(True)
                    self.ui.bitacorabtn2.setChecked(True)
                    self.ui.bitacorabtn2.blockSignals(False)
                    
            elif index == 6:  # Reportes
                if self.ui.reportesbtn1:
                    self.ui.reportesbtn1.blockSignals(True)
                    self.ui.reportesbtn1.setChecked(True)
                    self.ui.reportesbtn1.blockSignals(False)
                if self.ui.reportesbtn2:
                    self.ui.reportesbtn2.blockSignals(True)
                    self.ui.reportesbtn2.setChecked(True)
                    self.ui.reportesbtn2.blockSignals(False)
                    
            elif index == 7:  # Seguridad
                if self.ui.seguridadbtn1:
                    self.ui.seguridadbtn1.blockSignals(True)
                    self.ui.seguridadbtn1.setChecked(True)
                    self.ui.seguridadbtn1.blockSignals(False)
                if self.ui.seguridadbtn2:
                    self.ui.seguridadbtn2.blockSignals(True)
                    self.ui.seguridadbtn2.setChecked(True)
                    self.ui.seguridadbtn2.blockSignals(False)
            
            # NOTA: Para las páginas 8-12 no hay botones específicos en el sidebar
            # ya que se acceden desde la página de Reportes o Seguridad
            
            print("✅ Botones del sidebar actualizados correctamente")
            
        except Exception as e:
            print(f"❌ Error actualizando botones del sidebar: {e}")
            import traceback
            traceback.print_exc()

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

    def on_propietariosbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Propietarios")

    def on_propietariosbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Propietarios")

    def on_corralesbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Corrales")

    def on_corralesbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Corrales")

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
        
        # ✅ LIMPIAR RECURSOS DE TODOS LOS CONTROLADORES
        if hasattr(self, 'main_controller') and self.main_controller:
            self.main_controller.limpiar_recursos()
            
        if hasattr(self, 'becerros_controller') and self.becerros_controller and self.becerros_controller.db:
            self.becerros_controller.db.disconnect()
        if hasattr(self, 'animales_controller') and self.animales_controller and self.animales_controller.db:
            self.animales_controller.db.disconnect()
        if hasattr(self, 'propietarios_controller') and self.propietarios_controller and self.propietarios_controller.db:
            self.propietarios_controller.db.disconnect()
        if hasattr(self, 'corrales_controller') and self.corrales_controller and self.corrales_controller.db:
            self.corrales_controller.db.disconnect()
            
        # Limpiar recursos de todos los controladores
        controllers = [
            'reportes_controller', 'seguridad_controller', 'sbuscar_controller',
            'rbuscar_controller', 'usuarios_controller', 'copiabdd_controller',
            'restaurar_controller'
        ]
        
        for controller_name in controllers:
            if hasattr(self, controller_name) and getattr(self, controller_name):
                controller = getattr(self, controller_name)
                if hasattr(controller, 'limpiar_recursos'):
                    controller.limpiar_recursos()
            
        event.accept()

# ✅ FUNCIÓN PRINCIPAL
def main():
    app = QApplication(sys.argv)
    
    # Configurar la aplicación
    app.setApplicationName("SDLG - Sistema de Gestión Ganadera")
    app.setApplicationVersion("1.0")
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    print("🚀 Aplicación iniciada correctamente")
    print("🎯 Todas las páginas integradas:")
    print("   🏠  Índice 0: Página Principal")
    print("   🐄  Índice 1: Becerros") 
    print("   🐮  Índice 2: Animales")
    print("   👤  Índice 3: Propietarios")
    print("   🏠  Índice 4: Corrales")
    print("   📝  Índice 5: Bitácora")
    print("   📊  Índice 6: Reportes")
    print("   🔒  Índice 7: Seguridad")
    print("   🏥  Índice 8: Reportes de Salud (Sbuscar)")
    print("   🐄  Índice 9: Reportes de Reproducción (Rbuscar)")
    print("   👥  Índice 10: Gestión de Usuarios")
    print("   💾  Índice 11: Realizar Copia de Seguridad")
    print("   📂  Índice 12: Restaurar Copia de Seguridad")
    
    print("\n🎮 Navegación especial:")
    print("   📊 Reportes → 🏥 Salud (índice 8)")
    print("   📊 Reportes → 🐄 Reproducción (índice 9)") 
    print("   🔒 Seguridad → 👥 Usuarios (índice 10)")
    print("   🔒 Seguridad → 💾 Copia Seguridad (índice 11)")
    print("   🔒 Seguridad → 📂 Restaurar Copia (índice 12)")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()