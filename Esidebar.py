# Esidebar.py - VERSIÓN COMPLETA DEFINITIVA PARA EMPLEADOS CON BITÁCORA
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal 

from ui.sidebar_ui import Ui_MainWindow
from ui.becerros_ui import Ui_BecerrosPage
from ui.animales_ui import Ui_AnimalesPage
from ui.index_ui import Ui_IndexPage
from salud_ui import Ui_SaludPage
from ui.reproduccion_ui import Ui_ReproduccionPage
from ui.bitacora_ui import Ui_BitacoraPage  # Para crear el controlador de bitácora

from controllers.becerros_controller import BecerrosController
from controllers.animales_controller import AnimalesController
from controllers.index_controller import MainController
from salud_controller import SaludController
from reproduccion_controller import ReproduccionController
from controllers.bitacora_controller import BitacoraController
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
        
        # ✅ RECREAR STACKEDWIDGET SOLO CON PÁGINAS PERMITIDAS PARA EMPLEADOS
        self.recrear_stackedwidget_empleado()
        
        # CONECTAR SEÑALES
        self.connect_signals()
        
        print(f"✅ Sidebar Empleado inicializado - Usuario: {self.usuario_actual}")
    
    def recrear_stackedwidget_empleado(self):
        """Recrea el stackedWidget solo con páginas permitidas para empleados"""
        try:
            print("🔄 Recreando stackedWidget para empleado...")
            
            # 1. LIMPIAR TODAS LAS PÁGINAS EXISTENTES
            while self.ui.stackedWidget.count() > 0:
                widget = self.ui.stackedWidget.widget(0)
                if widget:
                    self.ui.stackedWidget.removeWidget(widget)
            
            # 2. CREAR SOLO PÁGINAS PERMITIDAS PARA EMPLEADOS
            
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
            
            # ✅ PÁGINA SALUD - ÍNDICE 3
            salud_widget = QWidget()
            self.salud_ui = Ui_SaludPage()
            self.salud_ui.setupUi(salud_widget)
            self.ui.stackedWidget.addWidget(salud_widget)
            self.salud_controller = SaludController(salud_widget)
            print("✅ Página salud creada en índice 3")

            # ✅ PÁGINA REPRODUCCIÓN - ÍNDICE 4
            reproduccion_widget = QWidget()
            self.reproduccion_ui = Ui_ReproduccionPage()
            self.reproduccion_ui.setupUi(reproduccion_widget)
            self.ui.stackedWidget.addWidget(reproduccion_widget)
            self.reproduccion_controller = ReproduccionController(reproduccion_widget)
            print("✅ Página reproducción creada en índice 4")

            # 3. CREAR CONTROLADOR DE BITÁCORA (NO SE AGREGA AL STACKEDWIDGET)
            self.crear_controlador_bitacora()

            # 4. CONFIGURAR PÁGINA PRINCIPAL COMO INICIAL
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.indexbtn2.setChecked(True)
            
            # ✅ COMPARTIR CONTROLADOR DE BITÁCORA CON OTROS CONTROLADORES
            self.compartir_bitacora_controller()
            
            print("📊 PÁGINAS DISPONIBLES PARA EMPLEADO:")
            for i in range(self.ui.stackedWidget.count()):
                print(f"   📄 Página {i}: {self.get_nombre_pagina(i)}")
                
        except Exception as e:
            print(f"❌ Error recreando stackedWidget empleado: {e}")
            import traceback
            traceback.print_exc()

    def crear_controlador_bitacora(self):
        """Crea el controlador de bitácora sin agregarlo al stackedWidget"""
        try:
            # Crear un widget temporal para la bitácora (no se muestra)
            bitacora_widget = QWidget()
            self.bitacora_ui = Ui_BitacoraPage()
            self.bitacora_ui.setupUi(bitacora_widget)
            
            # ✅ CREAR CONTROLADOR DE BITÁCORA CON USUARIO ACTUAL
            self.bitacora_controller = BitacoraController(
                ui=self.bitacora_ui,
                db=Database(),
                usuario_actual=self.usuario_actual
            )
            print("✅ Controlador de bitácora creado para empleado")
            
        except Exception as e:
            print(f"❌ Error creando controlador de bitácora: {e}")

    def get_nombre_pagina(self, index):
        """Obtener nombre de página por índice"""
        paginas = {
            0: "Página Principal",
            1: "Becerros",
            2: "Animales", 
            3: "Salud",
            4: "Reproducción"
        }
        return paginas.get(index, f"Página {index}")

    def compartir_bitacora_controller(self):
        """Compartir el controlador de bitácora con otros controladores"""
        try:
            print("🔄 Compartiendo controlador de bitácora en Esidebar...")
            
            controladores = [
                ('becerros_controller', self.becerros_controller),
                ('animales_controller', self.animales_controller),
                ('salud_controller', self.salud_controller),
                ('reproduccion_controller', self.reproduccion_controller)
            ]
            
            for nombre, controlador in controladores:
                if controlador and hasattr(controlador, 'set_bitacora_controller'):
                    controlador.set_bitacora_controller(self.bitacora_controller)
                    print(f"✅ Bitácora compartida con {nombre}")
                elif controlador:
                    print(f"⚠️  {nombre} no tiene método set_bitacora_controller")
                else:
                    print(f"❌ {nombre} no disponible")
                    
        except Exception as e:
            print(f"❌ Error compartiendo controlador de bitácora: {e}")

    def get_bitacora_controller(self):
        """Obtener el controlador de bitácora para compartirlo"""
        return self.bitacora_controller

    def set_usuario_actual(self, usuario_actual):
        """Establecer usuario actual"""
        self.usuario_actual = usuario_actual
        
        # ✅ ACTUALIZAR USUARIO EN CONTROLADOR DE BITÁCORA
        if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
            self.bitacora_controller.set_usuario_actual(usuario_actual)
            print(f"✅ Usuario actual actualizado en bitácora: {usuario_actual.get('nombre', 'N/A')}")

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
            
            # Botones de salud
            self._connect_button(self.ui.saludbtn1, self.on_saludbtn1_toggled)
            self._connect_button(self.ui.saludbtn2, self.on_saludbtn2_toggled)
            
            # Botones de reproducción
            self._connect_button(self.ui.reproduccionbtn1, self.on_reproduccionbtn1_toggled)
            self._connect_button(self.ui.reproduccionbtn2, self.on_reproduccionbtn2_toggled)
            
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
            
            # ✅ REGISTRAR EN BITÁCORA LA NAVEGACIÓN
            if hasattr(self, 'bitacora_controller') and self.bitacora_controller:
                nombre_pagina = self.get_nombre_pagina(index)
                self.bitacora_controller.registrar_accion(
                    modulo="Navegación",
                    accion="CAMBIAR_PAGINA",
                    descripcion=f"Navegó a {nombre_pagina}",
                    detalles=f"Desde botón: {button_name}"
                )
            
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
            elif index == 3:  # Salud
                if hasattr(self, 'salud_controller') and self.salud_controller:
                    print("🏥 Cargando página de salud...")
                    self.salud_controller.cargar_datos()
            elif index == 4:  # Reproducción
                if hasattr(self, 'reproduccion_controller') and self.reproduccion_controller:
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
                self.ui.saludbtn1, self.ui.saludbtn2,
                self.ui.reproduccionbtn1, self.ui.reproduccionbtn2
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
                    
            elif index == 3:  # Salud
                if self.ui.saludbtn1:
                    self.ui.saludbtn1.blockSignals(True)
                    self.ui.saludbtn1.setChecked(True)
                    self.ui.saludbtn1.blockSignals(False)
                if self.ui.saludbtn2:
                    self.ui.saludbtn2.blockSignals(True)
                    self.ui.saludbtn2.setChecked(True)
                    self.ui.saludbtn2.blockSignals(False)
                    
            elif index == 4:  # Reproducción
                if self.ui.reproduccionbtn1:
                    self.ui.reproduccionbtn1.blockSignals(True)
                    self.ui.reproduccionbtn1.setChecked(True)
                    self.ui.reproduccionbtn1.blockSignals(False)
                if self.ui.reproduccionbtn2:
                    self.ui.reproduccionbtn2.blockSignals(True)
                    self.ui.reproduccionbtn2.setChecked(True)
                    self.ui.reproduccionbtn2.blockSignals(False)
            
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

    def on_saludbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Salud")

    def on_saludbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(3, "Salud")

    def on_reproduccionbtn1_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Reproducción")

    def on_reproduccionbtn2_toggled(self, checked):
        if checked:
            self.cambiar_pagina(4, "Reproducción")

    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        print("🔴 Cerrando aplicación empleado...")
        
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
            
        # Limpiar recursos de todos los controladores
        controllers = [
            'bitacora_controller', 'salud_controller', 'reproduccion_controller'
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
    app.setApplicationName("SDLG - Sistema de Gestión Ganadera (Empleado)")
    app.setApplicationVersion("1.0")
    
    # Crear y mostrar ventana principal
    window = EMainWindow()
    window.show()
    
    print("🚀 Aplicación Empleado iniciada correctamente")
    print("🎯 Páginas disponibles para Empleado:")
    print("   🏠  Índice 0: Página Principal")
    print("   🐄  Índice 1: Becerros") 
    print("   🐮  Índice 2: Animales")
    print("   🏥  Índice 3: Salud")
    print("   🐄  Índice 4: Reproducción")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()