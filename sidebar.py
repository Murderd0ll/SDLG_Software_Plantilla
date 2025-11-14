# sidebar.py - VERSIÓN COMPLETA CORREGIDA
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore

from salud_controller import SaludController
from ui.sidebar_ui import Ui_MainWindow
from ui.becerros_ui import Ui_BecerrosPage
from ui.animales_ui import Ui_AnimalesPage
from ui.propietarios_ui import Ui_PropietariosPage
from ui.corrales_ui import Ui_CorralesPage
from ui.bitacora_ui import Ui_BitacoraPage
from ui.sbuscar_ui import Ui_SbuscarPage
from ui.rbuscar_ui import Ui_RbuscarPage
from ui.usuarios_ui import Ui_UsuariosPage
from ui.copiabdd_ui import Ui_CopiaBDDPage
from restaurar_ui import Ui_RestaurarPage
from ui.index_ui import Ui_IndexPage
from ui.reportes_ui import Ui_ReportesPage
from ui.seguridad_ui import Ui_SeguridadPage
from salud_ui import Ui_SaludPage 
from ui.reproduccion_ui import Ui_ReproduccionPage

from controllers.becerros_controller import BecerrosController
from controllers.animales_controller import AnimalesController
from controllers.propietarios_controller import PropietariosController
from controllers.corrales_controller import CorralesController
from controllers.bitacora_controller import BitacoraController
from controllers.sbuscar_controller import SbuscarController
from controllers.rbuscar_controller import RbuscarController
from controllers.usuarios_controller import UsuariosController
from copiabdd_controller import CopiaBDDController
from restaurar_controller import RestaurarController
from controllers.index_controller import MainController
from controllers.reportes_controller import ReportesController
from controllers.seguridad_controller import SeguridadController
from salud_controller import SaludController
from reproduccion_controller import ReproduccionController

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

class MainWindow(QMainWindow):
    cerrar_sesion_solicitado = pyqtSignal()
    
    def __init__(self, usuario_actual=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ✅ GUARDAR USUARIO ACTUAL
        self.usuario_actual = usuario_actual
        
        # CARGAR ESTILOS DEL SIDEBAR
        cargar_estilos_sidebar(self)

        self.ui.icon_only_widget.hide()
        
        # ✅ INICIALIZAR CONTROLADOR DE BITÁCORA PRIMERO
        self.bitacora_controller = None
        
        # ✅ CREAR PÁGINAS CON MANEJO DE ERRORES
        self.crear_paginas_con_seguridad()
        
        # CONECTAR SEÑALES
        self.connect_signals()
        
        print(f"✅ Sidebar inicializado - Página actual: {self.ui.stackedWidget.currentIndex()}")
        print(f"👤 Usuario en sidebar: {self.usuario_actual}")
    
    def crear_paginas_con_seguridad(self):
        """Crea todas las páginas con manejo de errores individual"""
        try:
            print("🔄 Creando páginas con manejo de errores...")
            
            # 1. LIMPIAR TODAS LAS PÁGINAS EXISTENTES
            while self.ui.stackedWidget.count() > 0:
                widget = self.ui.stackedWidget.widget(0)
                if widget:
                    self.ui.stackedWidget.removeWidget(widget)
            
            # 2. CREAR PÁGINAS CON MANEJO DE ERRORES INDIVIDUAL
            self.crear_pagina_principal(0)
            self.crear_pagina_becerros(1)
            self.crear_pagina_animales(2)
            self.crear_pagina_propietarios(3)
            self.crear_pagina_corrales(4)
            self.crear_pagina_bitacora(5)
            self.crear_pagina_reportes(6)
            self.crear_pagina_seguridad(7)
            self.crear_pagina_sbuscar(8)
            self.crear_pagina_rbuscar(9)
            self.crear_pagina_usuarios(10)
            self.crear_pagina_copiabdd(11)
            self.crear_pagina_restaurar(12)
            self.crear_pagina_salud(13)
            self.crear_pagina_reproduccion(14)

            # 3. CONFIGURAR PÁGINA PRINCIPAL COMO INICIAL
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.indexbtn2.setChecked(True)
            
            # ✅ COMPARTIR CONTROLADOR DE BITÁCORA CON OTROS CONTROLADORES
            self.compartir_bitacora_controller()
            
            # 4. DIAGNÓSTICO FINAL
            print("📊 DIAGNÓSTICO FINAL DE PÁGINAS:")
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
        """Crear página principal con manejo de errores"""
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
        """Crear página becerros con manejo de errores"""
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
        """Crear página animales con manejo de errores"""
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
        """Crear página propietarios con manejo de errores"""
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
        """Crear página corrales con manejo de errores"""
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

    def crear_pagina_bitacora(self, index):
        """Crear página bitácora con manejo de errores"""
        try:
            bitacora_widget = QWidget()
            self.bitacora_ui = Ui_BitacoraPage()
            self.bitacora_ui.setupUi(bitacora_widget)
            self.ui.stackedWidget.addWidget(bitacora_widget)
            
            # ✅ CREAR CONTROLADOR DE BITÁCORA CON USUARIO ACTUAL
            self.bitacora_controller = BitacoraController(
                ui=self.bitacora_ui,
                db=Database(),
                usuario_actual=self.usuario_actual
            )
            print(f"✅ Página bitácora REAL creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página bitácora: {e}")
            self.crear_widget_vacio(index, "Bitácora")

    def crear_pagina_reportes(self, index):
        """Crear página reportes con manejo de errores"""
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

    def crear_pagina_seguridad(self, index):
        """Crear página seguridad con manejo de errores"""
        try:
            seguridad_widget = QWidget()
            self.seguridad_ui = Ui_SeguridadPage()
            self.seguridad_ui.setupUi(seguridad_widget)
            self.ui.stackedWidget.addWidget(seguridad_widget)
            self.seguridad_controller = SeguridadController(seguridad_widget)
            print(f"✅ Página seguridad creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página seguridad: {e}")
            self.crear_widget_vacio(index, "Seguridad")

    def crear_pagina_sbuscar(self, index):
        """Crear página sbuscar con manejo de errores"""
        try:
            sbuscar_widget = QWidget()
            self.sbuscar_ui = Ui_SbuscarPage()
            self.sbuscar_ui.setupUi(sbuscar_widget)
            self.ui.stackedWidget.addWidget(sbuscar_widget)
            self.sbuscar_controller = SbuscarController(sbuscar_widget)
            print(f"✅ Página Sbuscar (Reportes Salud) creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página Sbuscar: {e}")
            self.crear_widget_vacio(index, "Sbuscar")

    def crear_pagina_rbuscar(self, index):
        """Crear página rbuscar con manejo de errores"""
        try:
            rbuscar_widget = QWidget()
            self.rbuscar_ui = Ui_RbuscarPage()
            self.rbuscar_ui.setupUi(rbuscar_widget)
            self.ui.stackedWidget.addWidget(rbuscar_widget)
            self.rbuscar_controller = RbuscarController(rbuscar_widget)
            print(f"✅ Página Rbuscar (Reportes Reproducción) creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página Rbuscar: {e}")
            self.crear_widget_vacio(index, "Rbuscar")

    def crear_pagina_usuarios(self, index):
        """Crear página usuarios con manejo de errores"""
        try:
            usuarios_widget = QWidget()
            self.usuarios_ui = Ui_UsuariosPage()
            self.usuarios_ui.setupUi(usuarios_widget)
            self.ui.stackedWidget.addWidget(usuarios_widget)
            self.usuarios_controller = UsuariosController(usuarios_widget)
            print(f"✅ Página Usuarios creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página Usuarios: {e}")
            self.crear_widget_vacio(index, "Usuarios")

    def crear_pagina_copiabdd(self, index):
        """Crear página copia BDD con manejo de errores"""
        try:
            copiabdd_widget = QWidget()
            self.copiabdd_ui = Ui_CopiaBDDPage()
            self.copiabdd_ui.setupUi(copiabdd_widget)
            self.ui.stackedWidget.addWidget(copiabdd_widget)
            self.copiabdd_controller = CopiaBDDController(copiabdd_widget)
            print(f"✅ Página CopiaBDD creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página CopiaBDD: {e}")
            self.crear_widget_vacio(index, "CopiaBDD")

    def crear_pagina_restaurar(self, index):
        """Crear página restaurar con manejo de errores"""
        try:
            restaurar_widget = QWidget()
            self.restaurar_ui = Ui_RestaurarPage()
            self.restaurar_ui.setupUi(restaurar_widget)
            self.ui.stackedWidget.addWidget(restaurar_widget)
            self.restaurar_controller = RestaurarController(restaurar_widget)
            print(f"✅ Página Restaurar creada en índice {index}")
        except Exception as e:
            print(f"❌ Error creando página Restaurar: {e}")
            self.crear_widget_vacio(index, "Restaurar")

    def crear_pagina_salud(self, index):
        """Crear página salud con manejo de errores"""
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
        """Crear página reproducción con manejo de errores"""
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
        """Compartir el controlador de bitácora con otros controladores que lo necesiten"""
        try:
            print("🔄 Compartiendo controlador de bitácora...")
            
            if not self.bitacora_controller:
                print("⚠️  No hay controlador de bitácora para compartir")
                return
            
            # ✅ LISTA DE CONTROLADORES QUE NECESITAN BITÁCORA
            controladores = [
                ('animales_controller', self.animales_controller),
                ('becerros_controller', self.becerros_controller),
                ('propietarios_controller', self.propietarios_controller),
                ('corrales_controller', self.corrales_controller),
                ('salud_controller', self.salud_controller),
                ('reproduccion_controller', self.reproduccion_controller),
                ('usuarios_controller', self.usuarios_controller),
                ('copiabdd_controller', self.copiabdd_controller),
                ('restaurar_controller', self.restaurar_controller)
            ]
            
            for nombre, controlador in controladores:
                if controlador:
                    try:
                        if hasattr(controlador, 'set_bitacora_controller'):
                            controlador.set_bitacora_controller(self.bitacora_controller)
                            print(f"✅ Bitácora compartida con {nombre}")
                        else:
                            # Intentar asignar directamente
                            controlador.bitacora_controller = self.bitacora_controller
                            print(f"✅ Bitácora asignada directamente a {nombre}")
                    except Exception as e:
                        print(f"⚠️  Error asignando bitácora a {nombre}: {e}")
                else:
                    print(f"⚠️  {nombre} no disponible")
                    
            print("🎯 Bitácora compartida exitosamente")
                    
        except Exception as e:
            print(f"❌ Error compartiendo controlador de bitácora: {e}")

    def connect_signals(self):
        """Conectar todas las señales de los botones de manera segura"""
        try:
            print("🔌 Conectando señales del sidebar...")
            
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
            
            # Botones de bitácora
            self._connect_button(self.ui.bitacorabtn1, self.on_bitacorabtn1_toggled)
            self._connect_button(self.ui.bitacorabtn2, self.on_bitacorabtn2_toggled)
            
            # Resto de las conexiones...
            self._connect_button(self.ui.reportesbtn1, self.on_reportesbtn1_toggled)
            self._connect_button(self.ui.reportesbtn2, self.on_reportesbtn2_toggled)
            self._connect_button(self.ui.seguridadbtn1, self.on_seguridadbtn1_toggled)
            self._connect_button(self.ui.seguridadbtn2, self.on_seguridadbtn2_toggled)
            
            # Conectar botón de cerrar sesión
            if hasattr(self.ui, 'cerrarbtn1'):
                self.ui.cerrarbtn1.clicked.connect(self.solicitar_cerrar_sesion)
            if hasattr(self.ui, 'cerrarbtn2'):
                self.ui.cerrarbtn2.clicked.connect(self.solicitar_cerrar_sesion)
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

    def solicitar_cerrar_sesion(self):
        """Solicitar cierre de sesión de manera segura"""
        try:
            print("🔒 Solicitando cierre de sesión...")
            
            # ✅ REGISTRAR EN BITÁCORA INTENTO DE CIERRE DE SESIÓN
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
                
                # ✅ REGISTRAR EN BITÁCORA CIERRE DE SESIÓN CONFIRMADO
                if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                    self.bitacora_controller.registrar_logout(
                        self.usuario_actual.get('nombre', 'Desconocido')
                    )
                
                # ✅ EMITIR SEÑAL EN LUGAR DE CERRAR DIRECTAMENTE
                self.cerrar_sesion_solicitado.emit()
            else:
                print("❌ Usuario canceló cierre de sesión")
                
                # ✅ REGISTRAR EN BITÁCORA CANCELACIÓN DE CIERRE DE SESIÓN
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
        
            self.actualizar_botones_sidebar(index)
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
            elif index == 5 and hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                print("📝 Página de bitácora - Configurando fechas por defecto")
            elif index == 6 and hasattr(self, 'reportes_controller') and self.reportes_controller:
                print("📊 Cargando página de reportes...")
                self.reportes_controller.cargar_datos()
            elif index == 7 and hasattr(self, 'seguridad_controller') and self.seguridad_controller:
                print("🔒 Cargando página de seguridad...")
                self.seguridad_controller.cargar_datos()
            elif index == 8 and hasattr(self, 'sbuscar_controller') and self.sbuscar_controller:
                print("🏥 Cargando página de reportes de salud...")
                self.sbuscar_controller.cargar_datos()
            elif index == 9 and hasattr(self, 'rbuscar_controller') and self.rbuscar_controller:
                print("🐄 Cargando página de reportes de reproducción...")
                self.rbuscar_controller.cargar_datos()
            elif index == 10 and hasattr(self, 'usuarios_controller') and self.usuarios_controller:
                print("👥 Cargando página de gestión de usuarios...")
                self.usuarios_controller.cargar_datos()
            elif index == 11 and hasattr(self, 'copiabdd_controller') and self.copiabdd_controller:
                print("💾 Cargando página de copia de seguridad...")
                self.copiabdd_controller.cargar_datos()
            elif index == 12 and hasattr(self, 'restaurar_controller') and self.restaurar_controller:
                print("📂 Cargando página de restauración...")
                self.restaurar_controller.cargar_datos()
            elif index == 13 and hasattr(self, 'salud_controller') and self.salud_controller:
                print("🏥 Cargando página de salud...")
                self.salud_controller.cargar_datos()
            elif index == 14 and hasattr(self, 'reproduccion_controller') and self.reproduccion_controller:
                print("🐄 Cargando página de reproducción...")
                self.reproduccion_controller.cargar_datos() 
                
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
                    
            elif index in [6, 8, 9]:  # Reportes general, Reportes de Salud, Reportes de Reproducción
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
            
            print("✅ Botones del sidebar actualizados correctamente")
            
        except Exception as e:
            print(f"❌ Error actualizando botones del sidebar: {e}")
            import traceback
            traceback.print_exc()

    def mostrar_reportes_salud_con_filtro(self, arete):
        try:
            print(f"🏥 Mostrando reportes de salud filtrados por arete: {arete}")
        
            # Cambiar a la página de reportes de salud (índice 8 - Sbuscar)
            self.cambiar_pagina(8, "Reportes de Salud")
        
            # Filtrar por el arete en el controlador de Sbuscar
            if hasattr(self, 'sbuscar_controller') and self.sbuscar_controller:
                # Esperar un momento para que la página se cargue completamente
                QtCore.QTimer.singleShot(100, lambda: self._aplicar_filtro_arete(arete))
            else:
                print("⚠️ Controlador de Sbuscar no disponible")
            
        except Exception as e:
            print(f"❌ Error mostrando reportes de salud con filtro: {e}")

    def _aplicar_filtro_arete(self, arete):
        try:
            if hasattr(self.sbuscar_controller, 'filtrar_por_arete'):
                self.sbuscar_controller.filtrar_por_arete(arete)
            elif hasattr(self.sbuscar_controller, 'lineEdit'):
                # Si no hay método específico, establecer el texto en el buscador
                self.sbuscar_controller.lineEdit.setText(arete)
                if hasattr(self.sbuscar_controller, 'buscar'):
                    self.sbuscar_controller.buscar()
        except Exception as e:
            print(f"❌ Error aplicando filtro por arete: {e}")

    def mostrar_reportes_reproduccion_con_filtro(self, arete):
        """Mostrar reportes de reproducción con filtro por arete - VERSIÓN SEGURA"""
        try:
            print(f"🐄 Mostrando reportes de reproducción filtrados por arete: {arete}")
            
            # Verificar que la página Rbuscar existe
            if self.ui.stackedWidget.count() <= 9:
                print("❌ La página Rbuscar (índice 9) no existe")
                QMessageBox.warning(self, "Error", "La página de reportes de reproducción no está disponible")
                return
            
            # Cambiar a la página de reportes de reproducción (índice 9 - Rbuscar)
            self.cambiar_pagina(9, "Reportes de Reproducción")

            # Filtrar por el arete en el controlador de Rbuscar
            if hasattr(self, 'rbuscar_controller') and self.rbuscar_controller:
                # Esperar un momento para que la página se cargue completamente
                QtCore.QTimer.singleShot(100, lambda: self._aplicar_filtro_arete_reproduccion(arete))
            else:
                print("⚠️ Controlador de Rbuscar no disponible")
            
        except Exception as e:
            print(f"❌ Error mostrando reportes de reproducción con filtro: {e}")

    def _aplicar_filtro_arete_reproduccion(self, arete):
        try:
            if hasattr(self.rbuscar_controller, 'filtrar_por_arete'):
                self.rbuscar_controller.filtrar_por_arete(arete)
            elif hasattr(self.rbuscar_controller, 'lineEdit'):
                # Si no hay método específico, establecer el texto en el buscador
                self.rbuscar_controller.lineEdit.setText(arete)
                if hasattr(self.rbuscar_controller, 'buscar'):
                    self.rbuscar_controller.buscar()
        except Exception as e:
            print(f"❌ Error aplicando filtro por arete en reproducción: {e}")

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
        
        # ✅ REGISTRAR EN BITÁCORA EL CIERRE DE LA APLICACIÓN
        if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
            self.bitacora_controller.registrar_accion(
                modulo="Sistema",
                accion="CERRAR_APLICACION",
                descripcion="Cerró la aplicación"
            )
        
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
            'bitacora_controller', 'reportes_controller', 'seguridad_controller', 'sbuscar_controller',
            'rbuscar_controller', 'usuarios_controller', 'copiabdd_controller',
            'restaurar_controller', 'salud_controller', 'reproduccion_controller'
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
    print("   🏥  Índice 13: Salud")
    print("   🐄  Índice 14: Reproducción")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()