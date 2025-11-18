# Esidebar.py - VERSIÓN COMPLETA CORREGIDA CON TODAS LAS PÁGINAS
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtWidgets, QtCore

from ui.sidebar_ui import Ui_MainWindow
from ui.becerros_ui import Ui_BecerrosPage
from ui.animales_ui import Ui_AnimalesPage
from ui.index_ui import Ui_IndexPage
from ui.salud_ui import Ui_SaludPage
from ui.reproduccion_ui import Ui_ReproduccionPage
from ui.bitacora_ui import Ui_BitacoraPage
from ui.corrales_ui import Ui_CorralesPage
from ui.propietarios_ui import Ui_PropietariosPage
from ui.reportes_ui import Ui_ReportesPage
from ui.sbuscar_ui import Ui_SbuscarPage  # ✅ Reportes de Salud
from ui.rbuscar_ui import Ui_RbuscarPage  # ✅ Reportes de Reproducción

from controllers.becerros_controller import BecerrosController
from controllers.animales_controller import AnimalesController
from controllers.index_controller import MainController
from controllers.salud_controller import SaludController
from controllers.reproduccion_controller import ReproduccionController
from controllers.bitacora_controller import BitacoraController
from controllers.corrales_controller import CorralesController
from controllers.propietarios_controller import PropietariosController
from controllers.reportes_controller import ReportesController
from controllers.sbuscar_controller import SbuscarController  # ✅ Controlador Reportes Salud
from controllers.rbuscar_controller import RbuscarController  # ✅ Controlador Reportes Reproducción
from database import Database

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

class EMainWindow(QMainWindow):
    cerrar_sesion_solicitado = pyqtSignal()
    
    def __init__(self, usuario_actual=None):
        super(EMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ✅ GUARDAR USUARIO ACTUAL
        self.usuario_actual = usuario_actual
        
        # CARGAR ESTILOS DEL SIDEBAR
        cargar_estilos_sidebar(self)

        self.ui.icon_only_widget.hide()
        
        # ✅ OCULTAR SOLO BOTONES DE SEGURIDAD Y BITÁCORA
        self.ocultar_botones_no_permitidos()
        
        # ✅ INICIALIZAR CONTROLADOR DE BITÁCORA PRIMERO
        self.bitacora_controller = None
        
        # ✅ CREAR TODAS LAS PÁGINAS PERMITIDAS PARA EMPLEADOS
        self.crear_paginas_completas()
        
        # CONECTAR SEÑALES
        self.connect_signals_admin_style()
        
        print(f"✅ Sidebar Empleado inicializado - Página actual: {self.ui.stackedWidget.currentIndex()}")
        print(f"👤 Usuario en sidebar: {self.usuario_actual}")
    
    def ocultar_botones_no_permitidos(self):
        """Ocultar solo botones de Seguridad y Bitácora"""
        try:
            print("🔒 Ocultando botones de Seguridad y Bitácora para empleados...")
            
            botones_a_ocultar = [
                'seguridadbtn1', 'seguridadbtn2',
                'bitacorabtn1', 'bitacorabtn2'
            ]
            
            for boton_name in botones_a_ocultar:
                if hasattr(self.ui, boton_name):
                    boton = getattr(self.ui, boton_name)
                    boton.hide()
                    print(f"✅ Ocultado: {boton_name}")
                    
            print("✅ Botones no permitidos ocultados correctamente")
            
        except Exception as e:
            print(f"❌ Error ocultando botones: {e}")

    def crear_paginas_completas(self):
        """Crear TODAS las páginas permitidas para empleados"""
        try:
            print("🔄 Creando páginas COMPLETAS para empleado...")
            
            # 1. LIMPIAR TODAS LAS PÁGINAS EXISTENTES
            while self.ui.stackedWidget.count() > 0:
                widget = self.ui.stackedWidget.widget(0)
                if widget:
                    self.ui.stackedWidget.removeWidget(widget)
            
            # 2. CREAR TODAS LAS PÁGINAS PERMITIDAS PARA EMPLEADOS
            self.crear_pagina_principal(0)
            self.crear_pagina_becerros(1)
            self.crear_pagina_animales(2)
            self.crear_pagina_propietarios(3)
            self.crear_pagina_corrales(4)
            self.crear_pagina_salud(5)
            self.crear_pagina_reproduccion(6)
            self.crear_pagina_reportes(7)
            self.crear_pagina_sbuscar(8)  # ✅ Reportes de Salud
            self.crear_pagina_rbuscar(9)  # ✅ Reportes de Reproducción

            # 3. CONFIGURAR PÁGINA PRINCIPAL COMO INICIAL
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.indexbtn2.setChecked(True)
            
            # ✅ COMPARTIR CONTROLADOR DE BITÁCORA
            self.compartir_bitacora_controller()
            
            # 4. DIAGNÓSTICO FINAL
            print("📊 DIAGNÓSTICO FINAL DE PÁGINAS PARA EMPLEADO:")
            print(f"   📄 Total de páginas creadas: {self.ui.stackedWidget.count()}")
            for i in range(self.ui.stackedWidget.count()):
                widget = self.ui.stackedWidget.widget(i)
                nombre = widget.objectName() if widget and widget.objectName() else f"Página {i}"
                print(f"   📄 Página {i}: {nombre}")
                
        except Exception as e:
            print(f"❌ Error general creando páginas: {e}")
            import traceback
            traceback.print_exc()

    def crear_pagina_principal(self, index):
        """Crear página principal"""
        try:
            main_widget = QWidget()
            self.main_ui = Ui_IndexPage()
            self.main_ui.setupUi(main_widget)
            self.ui.stackedWidget.addWidget(main_widget)
            self.main_controller = MainController(main_widget)
            print(f"✅ Página principal creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página principal: {e}")
            self.crear_widget_vacio(index, "Principal")

    def crear_pagina_becerros(self, index):
        """Crear página becerros"""
        try:
            becerros_widget = QWidget()
            self.becerros_ui = Ui_BecerrosPage()
            self.becerros_ui.setupUi(becerros_widget)
            self.ui.stackedWidget.addWidget(becerros_widget)
            self.becerros_controller = BecerrosController(becerros_widget)
            print(f"✅ Página becerros creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página becerros: {e}")
            self.crear_widget_vacio(index, "Becerros")

    def crear_pagina_animales(self, index):
        """Crear página animales"""
        try:
            animales_widget = QWidget()
            self.animales_ui = Ui_AnimalesPage()
            self.animales_ui.setupUi(animales_widget)
            self.ui.stackedWidget.addWidget(animales_widget)
            self.animales_controller = AnimalesController(animales_widget)
            print(f"✅ Página animales creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página animales: {e}")
            self.crear_widget_vacio(index, "Animales")

    def crear_pagina_propietarios(self, index):
        """Crear página propietarios"""
        try:
            propietarios_widget = QWidget()
            self.propietarios_ui = Ui_PropietariosPage()
            self.propietarios_ui.setupUi(propietarios_widget)
            self.ui.stackedWidget.addWidget(propietarios_widget)
            self.propietarios_controller = PropietariosController(propietarios_widget)
            print(f"✅ Página propietarios creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página propietarios: {e}")
            self.crear_widget_vacio(index, "Propietarios")

    def crear_pagina_corrales(self, index):
        """Crear página corrales"""
        try:
            corrales_widget = QWidget()
            self.corrales_ui = Ui_CorralesPage()
            self.corrales_ui.setupUi(corrales_widget)
            self.ui.stackedWidget.addWidget(corrales_widget)
            self.corrales_controller = CorralesController(corrales_widget)
            print(f"✅ Página corrales creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página corrales: {e}")
            self.crear_widget_vacio(index, "Corrales")

    def crear_pagina_salud(self, index):
        """Crear página salud"""
        try:
            salud_widget = QWidget()
            self.salud_ui = Ui_SaludPage()
            self.salud_ui.setupUi(salud_widget)
            self.ui.stackedWidget.addWidget(salud_widget)
            self.salud_controller = SaludController(salud_widget)
            print(f"✅ Página salud creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página salud: {e}")
            self.crear_widget_vacio(index, "Salud")

    def crear_pagina_reproduccion(self, index):
        """Crear página reproducción"""
        try:
            reproduccion_widget = QWidget()
            self.reproduccion_ui = Ui_ReproduccionPage()
            self.reproduccion_ui.setupUi(reproduccion_widget)
            self.ui.stackedWidget.addWidget(reproduccion_widget)
            self.reproduccion_controller = ReproduccionController(reproduccion_widget)
            print(f"✅ Página reproducción creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página reproducción: {e}")
            self.crear_widget_vacio(index, "Reproducción")

    def crear_pagina_reportes(self, index):
        """Crear página reportes"""
        try:
            reportes_widget = QWidget()
            self.reportes_ui = Ui_ReportesPage()
            self.reportes_ui.setupUi(reportes_widget)
            self.ui.stackedWidget.addWidget(reportes_widget)
            self.reportes_controller = ReportesController(reportes_widget)
            print(f"✅ Página reportes creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página reportes: {e}")
            self.crear_widget_vacio(index, "Reportes")

    def crear_pagina_sbuscar(self, index):
        """Crear página reportes de salud (Sbuscar)"""
        try:
            sbuscar_widget = QWidget()
            self.sbuscar_ui = Ui_SbuscarPage()
            self.sbuscar_ui.setupUi(sbuscar_widget)
            self.ui.stackedWidget.addWidget(sbuscar_widget)
            self.sbuscar_controller = SbuscarController(sbuscar_widget)
            print(f"✅ Página reportes de salud creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página reportes de salud: {e}")
            self.crear_widget_vacio(index, "Reportes de Salud")

    def crear_pagina_rbuscar(self, index):
        """Crear página reportes de reproducción (Rbuscar)"""
        try:
            rbuscar_widget = QWidget()
            self.rbuscar_ui = Ui_RbuscarPage()
            self.rbuscar_ui.setupUi(rbuscar_widget)
            self.ui.stackedWidget.addWidget(rbuscar_widget)
            self.rbuscar_controller = RbuscarController(rbuscar_widget)
            print(f"✅ Página reportes de reproducción creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página reportes de reproducción: {e}")
            self.crear_widget_vacio(index, "Reportes de Reproducción")

    def crear_widget_vacio(self, index, nombre_pagina):
        """Crear un widget vacío cuando falla la creación de una página"""
        try:
            widget_vacio = QWidget()
            widget_vacio.setObjectName(f"widget_vacio_{nombre_pagina}")
            label = QLabel(f"Página {nombre_pagina} no disponible\nError al cargar")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: red; font-size: 16px;")
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(label)
            widget_vacio.setLayout(layout)
            self.ui.stackedWidget.addWidget(widget_vacio)
            print(f"⚠️  Widget vacío creado para {nombre_pagina} en índice {index}")
        except Exception as e:
            print(f"❌ Error creando widget vacío: {e}")

    def compartir_bitacora_controller(self):
        """Compartir el controlador de bitácora con otros controladores"""
        try:
            print("🔄 Compartiendo controlador de bitácora en Esidebar...")
            
            if not self.bitacora_controller:
                print("⚠️  No hay controlador de bitácora para compartir")
                return
            
            controladores = [
                ('animales_controller', self.animales_controller),
                ('becerros_controller', self.becerros_controller),
                ('propietarios_controller', self.propietarios_controller),
                ('corrales_controller', self.corrales_controller),
                ('salud_controller', self.salud_controller),
                ('reproduccion_controller', self.reproduccion_controller),
                ('reportes_controller', self.reportes_controller),
                ('sbuscar_controller', self.sbuscar_controller),
                ('rbuscar_controller', self.rbuscar_controller)
            ]
            
            for nombre, controlador in controladores:
                if controlador:
                    try:
                        if hasattr(controlador, 'set_bitacora_controller'):
                            controlador.set_bitacora_controller(self.bitacora_controller)
                            print(f"✅ Bitácora compartida con {nombre}")
                        else:
                            controlador.bitacora_controller = self.bitacora_controller
                            print(f"✅ Bitácora asignada directamente a {nombre}")
                    except Exception as e:
                        print(f"⚠️  Error asignando bitácora a {nombre}: {e}")
                    
            print("🎯 Bitácora compartida exitosamente")
                    
        except Exception as e:
            print(f"❌ Error compartiendo controlador de bitácora: {e}")

    def connect_signals_admin_style(self):
        """Conectar señales usando la misma estructura que el sidebar de admin"""
        try:
            print("🔌 Conectando señales del sidebar empleado...")
            
            # Botones del índice/inicio
            self._connect_button_safe(self.ui.indexbtn1, self.on_indexbtn1_toggled)
            self._connect_button_safe(self.ui.indexbtn2, self.on_indexbtn2_toggled)
            
            # Botones de becerros
            self._connect_button_safe(self.ui.becerrosbtn1, self.on_becerrosbtn1_toggled)
            self._connect_button_safe(self.ui.becerrosbtn2, self.on_becerrosbtn2_toggled)
            
            # Botones de animales
            self._connect_button_safe(self.ui.animalesbtn1, self.on_animalesbtn1_toggled)
            self._connect_button_safe(self.ui.animalesbtn2, self.on_animalesbtn2_toggled)
            
            # Botones de propietarios
            self._connect_button_safe(self.ui.propietariosbtn1, self.on_propietariosbtn1_toggled)
            self._connect_button_safe(self.ui.propietariosbtn2, self.on_propietariosbtn2_toggled)
            
            # Botones de corrales
            self._connect_button_safe(self.ui.corralesbtn1, self.on_corralesbtn1_toggled)
            self._connect_button_safe(self.ui.corralesbtn2, self.on_corralesbtn2_toggled)
            
            # Botones de reportes
            self._connect_button_safe(self.ui.reportesbtn1, self.on_reportesbtn1_toggled)
            self._connect_button_safe(self.ui.reportesbtn2, self.on_reportesbtn2_toggled)
            
            # Botones de salud y reproducción (usando botones ocultos)
            self._connect_button_safe(self.ui.seguridadbtn1, self.on_saludbtn1_toggled)
            self._connect_button_safe(self.ui.seguridadbtn2, self.on_saludbtn2_toggled)
            self._connect_button_safe(self.ui.bitacorabtn1, self.on_reproduccionbtn1_toggled)
            self._connect_button_safe(self.ui.bitacorabtn2, self.on_reproduccionbtn2_toggled)
            
            # Conectar botón de cerrar sesión
            self._connect_button_safe(self.ui.cerrarbtn1, self.solicitar_cerrar_sesion, is_clicked=True)
            self._connect_button_safe(self.ui.cerrarbtn2, self.solicitar_cerrar_sesion, is_clicked=True)
            
            print("✅ Todas las señales conectadas correctamente")
            
        except Exception as e:
            print(f"❌ Error conectando señales: {e}")
            import traceback
            traceback.print_exc()

    def _connect_button_safe(self, button, handler, is_clicked=False):
        """Conectar botón de manera segura"""
        if button:
            if is_clicked:
                button.clicked.connect(handler)
            else:
                button.toggled.connect(handler)

    def solicitar_cerrar_sesion(self):
        """Solicitar cierre de sesión de manera segura"""
        try:
            print("🔒 Solicitando cierre de sesión...")
            
            if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                self.bitacora_controller.registrar_accion(
                    modulo="Sistema",
                    accion="INTENTO_LOGOUT",
                    descripcion="Intentó cerrar sesión del sistema"
                )
            
            respuesta = QMessageBox.question(
                self, 
                "Cerrar sesión", 
                "¿Estás seguro de que quieres cerrar sesión?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                print("✅ Usuario confirmó cierre de sesión")
                
                if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                    self.bitacora_controller.registrar_logout(
                        self.usuario_actual.get('nombre', 'Desconocido')
                    )
                
                self.cerrar_sesion_solicitado.emit()
            else:
                print("❌ Usuario canceló cierre de sesión")
                
                if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Sistema",
                        accion="CANCELAR_LOGOUT",
                        descripcion="Canceló el cierre de sesión"
                    )
                
        except Exception as e:
            print(f"❌ Error al solicitar cierre de sesión: {e}")

    def cambiar_pagina(self, index, button_name):
        """Cambiar página con verificación de índice seguro"""
        try:
            max_index = self.ui.stackedWidget.count() - 1
            if index > max_index:
                print(f"❌ Índice {index} no existe, máximo es {max_index}")
                QMessageBox.warning(self, "Error", f"La página {index} no está disponible")
                return
        
            self.actualizar_botones_sidebar_admin_style(index)
            self.ui.stackedWidget.setCurrentIndex(index)
            print(f"✅ Cambiando a página {index}: {button_name}")
        
            # CARGAR DATOS SEGÚN LA PÁGINA
            if index == 0 and hasattr(self, 'main_controller') and self.main_controller:
                print("🏠 Cargando estadísticas de página principal...")
                self.main_controller.cargar_estadisticas()
            elif index == 1 and hasattr(self, 'becerros_controller') and self.becerros_controller:
                print("🐄 Cargando datos de becerros...")
                self.becerros_controller.cargar_becerros()
            elif index == 2 and hasattr(self, 'animales_controller') and self.animales_controller:
                print("🐮 Cargando datos de animales...")
                self.animales_controller.cargar_animales()
            elif index == 3 and hasattr(self, 'propietarios_controller') and self.propietarios_controller:
                print("👤 Cargando datos de propietarios...")
                self.propietarios_controller.cargar_propietarios()
            elif index == 4 and hasattr(self, 'corrales_controller') and self.corrales_controller:
                print("🏠 Cargando datos de corrales...")
                self.corrales_controller.cargar_corrales()
            elif index == 5 and hasattr(self, 'salud_controller') and self.salud_controller:
                print("🏥 Cargando página de salud...")
                self.salud_controller.cargar_datos()
            elif index == 6 and hasattr(self, 'reproduccion_controller') and self.reproduccion_controller:
                print("🐄 Cargando página de reproducción...")
                self.reproduccion_controller.cargar_datos()
            elif index == 7 and hasattr(self, 'reportes_controller') and self.reportes_controller:
                print("📊 Cargando página de reportes...")
                self.reportes_controller.cargar_datos()
            elif index == 8 and hasattr(self, 'sbuscar_controller') and self.sbuscar_controller:
                print("🏥 Cargando página de reportes de salud...")
                self.sbuscar_controller.cargar_datos()
            elif index == 9 and hasattr(self, 'rbuscar_controller') and self.rbuscar_controller:
                print("🐄 Cargando página de reportes de reproducción...")
                self.rbuscar_controller.cargar_datos()
                
        except Exception as e:
            print(f"❌ Error cambiando a página {index}: {e}")
            import traceback
            traceback.print_exc()

    def actualizar_botones_sidebar_admin_style(self, index):
        """Actualizar botones del sidebar"""
        try:
            print(f"🔘 Actualizando botones del sidebar para la página {index}...")
            
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
                    btn.blockSignals(True)
                    btn.setChecked(False)
                    btn.blockSignals(False)
            
            # Marcar el botón correspondiente según el índice
            if index == 0:  # Página principal
                self.marcar_boton_safe(self.ui.indexbtn1)
                self.marcar_boton_safe(self.ui.indexbtn2)
                    
            elif index == 1:  # Becerros
                self.marcar_boton_safe(self.ui.becerrosbtn1)
                self.marcar_boton_safe(self.ui.becerrosbtn2)
                    
            elif index == 2:  # Animales
                self.marcar_boton_safe(self.ui.animalesbtn1)
                self.marcar_boton_safe(self.ui.animalesbtn2)
                    
            elif index == 3:  # Propietarios
                self.marcar_boton_safe(self.ui.propietariosbtn1)
                self.marcar_boton_safe(self.ui.propietariosbtn2)
                    
            elif index == 4:  # Corrales
                self.marcar_boton_safe(self.ui.corralesbtn1)
                self.marcar_boton_safe(self.ui.corralesbtn2)
                    
            elif index == 5:  # Salud (usa botones de seguridad)
                self.marcar_boton_safe(self.ui.seguridadbtn1)
                self.marcar_boton_safe(self.ui.seguridadbtn2)
                    
            elif index == 6:  # Reproducción (usa botones de bitácora)
                self.marcar_boton_safe(self.ui.bitacorabtn1)
                self.marcar_boton_safe(self.ui.bitacorabtn2)
                    
            elif index == 7:  # Reportes
                self.marcar_boton_safe(self.ui.reportesbtn1)
                self.marcar_boton_safe(self.ui.reportesbtn2)
                    
            elif index == 8:  # Reportes de Salud
                self.marcar_boton_safe(self.ui.reportesbtn1)
                self.marcar_boton_safe(self.ui.reportesbtn2)
                    
            elif index == 9:  # Reportes de Reproducción
                self.marcar_boton_safe(self.ui.reportesbtn1)
                self.marcar_boton_safe(self.ui.reportesbtn2)
            
            print("✅ Botones del sidebar actualizados correctamente")
            
        except Exception as e:
            print(f"❌ Error actualizando botones del sidebar: {e}")
            import traceback
            traceback.print_exc()

    def marcar_boton_safe(self, boton):
        """Marca un botón de manera segura si existe"""
        if boton:
            boton.blockSignals(True)
            boton.setChecked(True)
            boton.blockSignals(False)

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

    def on_reportesbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(7, "Reportes")

    def on_reportesbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(7, "Reportes")

    def on_saludbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(5, "Salud")

    def on_saludbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(5, "Salud")

    def on_reproduccionbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(6, "Reproducción")

    def on_reproduccionbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(6, "Reproducción")

    def set_usuario_actual(self, usuario_actual):
        """Establecer usuario actual y crear controlador de bitácora"""
        self.usuario_actual = usuario_actual
        
        try:
            bitacora_widget = QWidget()
            self.bitacora_ui = Ui_BitacoraPage()
            self.bitacora_ui.setupUi(bitacora_widget)
            
            self.bitacora_controller = BitacoraController(
                ui=self.bitacora_ui,
                db=Database(),
                usuario_actual=self.usuario_actual
            )
            print("✅ Controlador de bitácora creado para empleado")
            
            self.compartir_bitacora_controller()
            
        except Exception as e:
            print(f"❌ Error creando controlador de bitácora: {e}")

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        print("🔴 Cerrando aplicación empleado...")
        
        if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
            self.bitacora_controller.registrar_accion(
                modulo="Sistema",
                accion="CERRAR_APLICACION",
                descripcion="Cerró la aplicación"
            )
        
        controllers = [
            'main_controller', 'becerros_controller', 'animales_controller',
            'propietarios_controller', 'corrales_controller', 'salud_controller',
            'reproduccion_controller', 'reportes_controller', 'sbuscar_controller',
            'rbuscar_controller', 'bitacora_controller'
        ]
        
        for controller_name in controllers:
            if hasattr(self, controller_name) and getattr(self, controller_name):
                controller = getattr(self, controller_name)
                if hasattr(controller, 'limpiar_recursos'):
                    controller.limpiar_recursos()
                elif hasattr(controller, 'db') and controller.db:
                    controller.db.disconnect()
            
        event.accept()

# ✅ FUNCIÓN PRINCIPAL
def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("SDLG - Sistema de Gestión Ganadera (Empleado)")
    app.setApplicationVersion("1.0")
    
    window = EMainWindow()
    window.show()
    
    print("🚀 Aplicación Empleado iniciada correctamente")
    print("🎯 Páginas disponibles para Empleado:")
    print("   🏠  Índice 0: Página Principal")
    print("   🐄  Índice 1: Becerros") 
    print("   🐮  Índice 2: Animales")
    print("   👤  Índice 3: Propietarios")
    print("   🏠  Índice 4: Corrales")
    print("   🏥  Índice 5: Salud")
    print("   🐄  Índice 6: Reproducción")
    print("   📊  Índice 7: Reportes")
    print("   🏥  Índice 8: Reportes de Salud")
    print("   🐄  Índice 9: Reportes de Reproducción")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()