# controllers/index_controller.py
from PyQt5 import QtCore, QtGui, QtWidgets
from database import Database

class MainController:
    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.db = Database()
        self.setup_connections()
        self.cargar_estadisticas()
        print("✅ MainController inicializado para página principal")

    def setup_connections(self):
        """Configura las conexiones de los botones y señales"""
        try:
            print("🔍 Configurando conexiones para página principal...")
            
            # Conectar botones de acciones rápidas
            self.pushButton = self.main_widget.findChild(QtWidgets.QPushButton, "pushButton")
            self.pushButton_2 = self.main_widget.findChild(QtWidgets.QPushButton, "pushButton_2")
            self.pushButton_3 = self.main_widget.findChild(QtWidgets.QPushButton, "pushButton_3")
            
            if self.pushButton:
                self.pushButton.clicked.connect(self.abrir_animales)
                print("✅ Botón Animales conectado")
            else:
                print("❌ No se encontró pushButton (Animales)")
                
            if self.pushButton_2:
                self.pushButton_2.clicked.connect(self.abrir_becerros)
                print("✅ Botón Becerros conectado")
            else:
                print("❌ No se encontró pushButton_2 (Becerros)")
                
            if self.pushButton_3:
                self.pushButton_3.clicked.connect(self.abrir_corrales)
                print("✅ Botón Corrales conectado")
            else:
                print("❌ No se encontró pushButton_3 (Corrales)")
                
        except Exception as e:
            print(f"❌ Error en setup_connections: {e}")
            import traceback
            traceback.print_exc()

    def cargar_estadisticas(self):
        """Carga las estadísticas en la página principal"""
        try:
            print("📊 Cargando estadísticas...")
            
            # Obtener datos de la base de datos
            total_ganado = self.obtener_total_ganado()
            total_machos = self.obtener_total_machos()
            total_hembras = self.obtener_total_hembras()
            total_becerros = self.obtener_total_becerros()
            
            # Actualizar las etiquetas
            self.actualizar_etiqueta("label_7", str(total_ganado))      # Total Ganado
            self.actualizar_etiqueta("label_10", str(total_machos))     # Machos
            self.actualizar_etiqueta("label_13", str(total_hembras))    # Hembras
            self.actualizar_etiqueta("label_16", str(total_becerros))   # Becerros
            
            print(f"✅ Estadísticas cargadas - Total: {total_ganado}, Machos: {total_machos}, Hembras: {total_hembras}, Becerros: {total_becerros}")
            
        except Exception as e:
            print(f"❌ Error al cargar estadísticas: {e}")
            # Establecer valores por defecto en caso de error
            self.actualizar_etiqueta("label_7", "0")
            self.actualizar_etiqueta("label_10", "0")
            self.actualizar_etiqueta("label_13", "0")
            self.actualizar_etiqueta("label_16", "0")

    def actualizar_etiqueta(self, nombre_etiqueta, texto):
        """Actualiza el texto de una etiqueta por su nombre"""
        try:
            etiqueta = self.main_widget.findChild(QtWidgets.QLabel, nombre_etiqueta)
            if etiqueta:
                etiqueta.setText(texto)
            else:
                print(f"❌ No se encontró la etiqueta: {nombre_etiqueta}")
        except Exception as e:
            print(f"❌ Error al actualizar etiqueta {nombre_etiqueta}: {e}")

    def obtener_total_ganado(self):
        """Obtiene el total de animales (ganado + becerros) - CORREGIDO CON DIAGNÓSTICO"""
        try:
            print("🔍 Calculando total de ganado...")
            
            # Conectar a la base de datos si no está conectada
            if not self.db.connection:
                self.db.connect()
            
            # Contar animales de ganado
            animales = self.db.obtener_animales()
            total_animales = len(animales) if animales else 0
            print(f"📊 Animales encontrados: {total_animales}")
            
            # DEBUG: Mostrar algunos animales si existen
            if animales and len(animales) > 0:
                print(f"🐮 Primer animal: {animales[0]}")
            
            # Contar becerros
            becerros = self.db.obtener_becerros()
            total_becerros = len(becerros) if becerros else 0
            print(f"📊 Becerros encontrados: {total_becerros}")
            
            # DEBUG: Mostrar algunos becerros si existen
            if becerros and len(becerros) > 0:
                print(f"🐂 Primer becerro: {becerros[0]}")
            
            # ✅ CORRECCIÓN: Sumar animales + becerros para el total general
            total_general = total_animales + total_becerros
            
            print(f"📊 Total ganado calculado: {total_animales} animales + {total_becerros} becerros = {total_general}")
            
            return total_general
            
        except Exception as e:
            print(f"❌ Error al obtener total ganado: {e}")
            import traceback
            traceback.print_exc()
            return 0

    def obtener_total_machos(self):
        """Obtiene el total de animales machos - CORREGIDO CON DIAGNÓSTICO"""
        try:
            total_machos = 0
            
            # Contar machos en ganado
            animales = self.db.obtener_animales()
            if animales:
                print(f"🔍 Revisando {len(animales)} animales para machos...")
                for i, animal in enumerate(animales):
                    if len(animal) > 4 and animal[4]:
                        sexo = str(animal[4]).lower().strip()
                        if sexo in ['macho', 'm', 'male']:
                            total_machos += 1
                            print(f"🐂 Macho #{total_machos} en animales: {animal[2] if len(animal) > 2 else 'N/A'} - Sexo: '{sexo}'")
            
            # Contar machos en becerros
            becerros = self.db.obtener_becerros()
            if becerros:
                print(f"🔍 Revisando {len(becerros)} becerros para machos...")
                for i, becerro in enumerate(becerros):
                    if len(becerro) > 4 and becerro[4]:
                        sexo = str(becerro[4]).lower().strip()
                        if sexo in ['macho', 'm', 'male']:
                            total_machos += 1
                            print(f"🐂 Macho #{total_machos} en becerros: {becerro[2] if len(becerro) > 2 else 'N/A'} - Sexo: '{sexo}'")
            
            print(f"📊 Total machos encontrados: {total_machos}")
            return total_machos
            
        except Exception as e:
            print(f"❌ Error al obtener total machos: {e}")
            import traceback
            traceback.print_exc()
            return 0

    def obtener_total_hembras(self):
        """Obtiene el total de animales hembras - CORREGIDO CON DIAGNÓSTICO"""
        try:
            total_hembras = 0
            
            # Contar hembras en ganado
            animales = self.db.obtener_animales()
            if animales:
                print(f"🔍 Revisando {len(animales)} animales para hembras...")
                for i, animal in enumerate(animales):
                    if len(animal) > 4 and animal[4]:
                        sexo = str(animal[4]).lower().strip()
                        if sexo in ['hembra', 'h', 'f', 'female']:
                            total_hembras += 1
                            print(f"🐄 Hembra #{total_hembras} en animales: {animal[2] if len(animal) > 2 else 'N/A'} - Sexo: '{sexo}'")
            
            # Contar hembras en becerros
            becerros = self.db.obtener_becerros()
            if becerros:
                print(f"🔍 Revisando {len(becerros)} becerros para hembras...")
                for i, becerro in enumerate(becerros):
                    if len(becerro) > 4 and becerro[4]:
                        sexo = str(becerro[4]).lower().strip()
                        if sexo in ['hembra', 'h', 'f', 'female']:
                            total_hembras += 1
                            print(f"🐄 Hembra #{total_hembras} en becerros: {becerro[2] if len(becerro) > 2 else 'N/A'} - Sexo: '{sexo}'")
            
            print(f"📊 Total hembras encontradas: {total_hembras}")
            return total_hembras
            
        except Exception as e:
            print(f"❌ Error al obtener total hembras: {e}")
            import traceback
            traceback.print_exc()
            return 0

    def obtener_total_becerros(self):
        """Obtiene el total de becerros - CORREGIDO CON DIAGNÓSTICO"""
        try:
            becerros = self.db.obtener_becerros()
            total = len(becerros) if becerros else 0
            print(f"📊 Total becerros encontrados: {total}")
            
            # DEBUG: Mostrar información de becerros
            if becerros:
                for i, becerro in enumerate(becerros[:3]):  # Mostrar primeros 3
                    print(f"🐂 Becerro {i+1}: {becerro[1] if len(becerro) > 1 else 'N/A'} - {becerro[2] if len(becerro) > 2 else 'N/A'}")
            
            return total
        except Exception as e:
            print(f"❌ Error al obtener total becerros: {e}")
            import traceback
            traceback.print_exc()
            return 0

    def abrir_animales(self):
        """Abre la sección de animales - NAVEGACIÓN REAL CON ACTUALIZACIÓN DE BOTONES"""
        try:
            print("🐄 Navegando a sección de animales...")
            
            # ✅ NAVEGACIÓN REAL: Buscar el main window y cambiar página
            main_window = self.get_main_window()
            if main_window:
                # ✅ ACTUALIZAR BOTONES DEL SIDEBAR ANTES DE CAMBIAR
                self.actualizar_botones_sidebar(main_window, 2)  # 2 = índice de animales
                main_window.cambiar_pagina(2, "Animales")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                QtWidgets.QMessageBox.information(
                    self.main_widget, 
                    "Animales", 
                    "Navegando a gestión de animales..."
                )
            
        except Exception as e:
            print(f"❌ Error al navegar a animales: {e}")
            QtWidgets.QMessageBox.warning(
                self.main_widget,
                "Error",
                f"No se pudo abrir la sección de animales: {str(e)}"
            )

    def abrir_becerros(self):
        """Abre la sección de becerros - NAVEGACIÓN REAL CON ACTUALIZACIÓN DE BOTONES"""
        try:
            print("🐂 Navegando a sección de becerros...")
            
            # ✅ NAVEGACIÓN REAL: Buscar el main window y cambiar página
            main_window = self.get_main_window()
            if main_window:
                # ✅ ACTUALIZAR BOTONES DEL SIDEBAR ANTES DE CAMBIAR
                self.actualizar_botones_sidebar(main_window, 1)  # 1 = índice de becerros
                main_window.cambiar_pagina(1, "Becerros")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                QtWidgets.QMessageBox.information(
                    self.main_widget, 
                    "Becerros", 
                    "Navegando a gestión de becerros..."
                )
            
        except Exception as e:
            print(f"❌ Error al navegar a becerros: {e}")
            QtWidgets.QMessageBox.warning(
                self.main_widget,
                "Error",
                f"No se pudo abrir la sección de becerros: {str(e)}"
            )

    def abrir_corrales(self):
        """Abre la sección de corrales - NAVEGACIÓN REAL CON ACTUALIZACIÓN DE BOTONES"""
        try:
            print("🏠 Navegando a sección de corrales...")
            
            # ✅ NAVEGACIÓN REAL: Buscar el main window y cambiar página
            main_window = self.get_main_window()
            if main_window:
                # ✅ ACTUALIZAR BOTONES DEL SIDEBAR ANTES DE CAMBIAR
                self.actualizar_botones_sidebar(main_window, 4)  # 4 = índice de corrales
                main_window.cambiar_pagina(4, "Corrales")
            else:
                print("❌ No se pudo encontrar la ventana principal")
                QtWidgets.QMessageBox.information(
                    self.main_widget, 
                    "Corrales", 
                    "Navegando a gestión de corrales..."
                )
            
        except Exception as e:
            print(f"❌ Error al navegar a corrales: {e}")
            QtWidgets.QMessageBox.warning(
                self.main_widget,
                "Error",
                f"No se pudo abrir la sección de corrales: {str(e)}"
            )

    def actualizar_botones_sidebar(self, main_window, indice_destino):
        """Actualiza los botones del sidebar para que reflejen la página activa"""
        try:
            print(f"🔄 Actualizando botones del sidebar para página {indice_destino}")
            
            # ✅ DESMARCAR TODOS LOS BOTONES PRIMERO
            botones_por_indice = {
                0: ['indexbtn1', 'indexbtn2'],      # Página principal
                1: ['becerrosbtn1', 'becerrosbtn2'], # Becerros
                2: ['animalesbtn1', 'animalesbtn2'], # Animales
                3: ['propietariosbtn1', 'propietariosbtn2'], # Propietarios
                4: ['corralesbtn1', 'corralesbtn2'], # Corrales
                5: ['bitacorabtn1', 'bitacorabtn2'], # Bitácora
                6: ['reportesbtn1', 'reportesbtn2'], # Reportes
                7: ['seguridadbtn1', 'seguridadbtn2'] # Seguridad
            }
            
            # Desmarcar todos los botones
            for botones in botones_por_indice.values():
                for nombre_boton in botones:
                    boton = getattr(main_window.ui, nombre_boton, None)
                    if boton:
                        boton.setChecked(False)
            
            # ✅ MARCAR LOS BOTONES CORRESPONDIENTES A LA PÁGINA DESTINO
            if indice_destino in botones_por_indice:
                for nombre_boton in botones_por_indice[indice_destino]:
                    boton = getattr(main_window.ui, nombre_boton, None)
                    if boton:
                        boton.setChecked(True)
                        print(f"✅ Botón {nombre_boton} marcado")
            
            print(f"✅ Botones del sidebar actualizados para página {indice_destino}")
            
        except Exception as e:
            print(f"❌ Error actualizando botones del sidebar: {e}")

    def get_main_window(self):
        """Obtiene la referencia a la ventana principal"""
        try:
            # Navegar hacia arriba en la jerarquía de widgets para encontrar MainWindow
            parent = self.main_widget
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

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas (para llamar desde otras partes de la aplicación)"""
        print("🔄 Actualizando estadísticas...")
        self.cargar_estadisticas()

    def refresh_data(self):
        """Método para refrescar todos los datos de la página principal"""
        print("🔄 Refrescando datos de la página principal...")
        self.cargar_estadisticas()

    def limpiar_recursos(self):
        """Método para limpiar recursos cuando se cierra la aplicación"""
        print("🧹 Limpiando recursos del controlador principal...")
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()