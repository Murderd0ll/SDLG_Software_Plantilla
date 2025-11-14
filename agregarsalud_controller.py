from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarsalud_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarSaludController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None, arete_animal=None, tipo_animal=None, main_window=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        self.arete_animal = arete_animal
        self.tipo_animal = tipo_animal
        self.main_window = main_window 
        
        # Variables para almacenar archivos
        self.archivo_data = None
        self.archivo_ruta = None
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.configurar_fecha()
        self.verificar_widgets()
        
        # Si se proporcionó un arete, establecerlo en el campo correspondiente
        if self.arete_animal:
            self.ui.lineEdit_5.setText(self.arete_animal)
        
    def verificar_widgets(self):
        """Función temporal para verificar que todos los widgets existen"""
        print("\n🔍 VERIFICANDO WIDGETS SALUD:")
        widgets = [
            'lineEdit', 'lineEdit_5', 'lineEdit_4', 'textEdit',
            'comboBox', 'comboBox_3', 'dateEdit',
            'checkBox_4', 'checkBox_5', 'checkBox_6', 'checkBox', 'checkBox_2',
            'checkBox_9', 'checkBox_8', 'checkBox_10', 'checkBox_7', 'checkBox_3'
        ]
        
        for widget_name in widgets:
            widget = getattr(self.ui, widget_name, None)
            if widget:
                print(f"✅ {widget_name}: ENCONTRADO")
            else:
                print(f"❌ {widget_name}: NO ENCONTRADO")
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_salud)  # Guardar
        self.ui.pushButton_3.clicked.connect(self.ver_registros_salud)  # Ver registros
        self.ui.indexbtn2.clicked.connect(self.subir_archivo)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables"""
        # Combobox editables
        self.ui.comboBox.setEditable(True)  # Procedimiento
        self.ui.comboBox_3.setEditable(True)  # Condición de salud
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos en combobox salud...")
            
            # 1. PROCEDIMIENTOS - Valores comunes
            self.ui.comboBox.clear()
            procedimientos = [
                "Consulta general", "Vacunación", "Desparasitación", 
                "Cirugía menor", "Cirugía mayor", "Tratamiento médico",
                "Control rutinario", "Emergencia", "Parto asistido"
            ]
            self.ui.comboBox.addItems(procedimientos)
            self.ui.comboBox.setCurrentIndex(0)
            print(f"✅ Procedimientos cargados: {len(procedimientos)}")
            
            # 2. CONDICIONES DE SALUD - Valores comunes
            self.ui.comboBox_3.clear()
            condiciones = [
                "Excelente", "Buena", "Regular", "Mala", "Crítica",
                "En tratamiento", "Recuperación", "Curado", "Crónico"
            ]
            self.ui.comboBox_3.addItems(condiciones)
            self.ui.comboBox_3.setCurrentIndex(0)
            print(f"✅ Condiciones de salud cargadas: {len(condiciones)}")
            
            print("🎉 Combobox de salud cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar combobox salud: {e}")
            import traceback
            traceback.print_exc()
            
    def configurar_fecha(self):
        """Configura la fecha actual"""
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)
        
    def obtener_medicina_preventiva(self):
        """Obtiene la medicina preventiva seleccionada como string"""
        medicinas = []
        
        # Vacunas
        if self.ui.checkBox_4.isChecked():
            medicinas.append("Vacuna contra Brucelosis")
        if self.ui.checkBox_5.isChecked():
            medicinas.append("Vacuna contra IBR")
        if self.ui.checkBox_6.isChecked():
            medicinas.append("Vacuna contra BVD")
        if self.ui.checkBox.isChecked():
            medicinas.append("Bacterina contra clostridiosis")
        if self.ui.checkBox_2.isChecked():
            medicinas.append("Bacterina contra pasteurelosis")
            
        # Manejo
        if self.ui.checkBox_9.isChecked():
            medicinas.append("Baño garrapaticida")
        if self.ui.checkBox_8.isChecked():
            medicinas.append("Control de moscas")
        if self.ui.checkBox_10.isChecked():
            medicinas.append("Desparacitación interna")
        if self.ui.checkBox_7.isChecked():
            medicinas.append("Desparacitación externa")
        if self.ui.checkBox_3.isChecked():
            medicinas.append("No aplica")
            
        return ", ".join(medicinas) if medicinas else "Ninguna"
    
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def subir_archivo(self):
        """Abre un diálogo para seleccionar y cargar un archivo"""
        try:
            # Configurar los filtros de archivo (imágenes y PDFs)
            filtros = "Archivos médicos (*.png *.jpg *.jpeg *.bmp *.pdf *.doc *.docx);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar archivo médico", 
                "", 
                filtros
            )
            
            if ruta_archivo:
                # Verificar tamaño del archivo (máximo 10MB)
                tamaño_archivo = os.path.getsize(ruta_archivo)
                if tamaño_archivo > 10 * 1024 * 1024:  # 10MB en bytes
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Archivo muy grande", 
                        "El archivo no puede ser mayor a 10MB"
                    )
                    return
                
                # Leer el archivo como bytes
                with open(ruta_archivo, 'rb') as archivo:
                    self.archivo_data = archivo.read()
                    self.archivo_ruta = ruta_archivo
                
                # Mostrar información al usuario
                nombre_archivo = Path(ruta_archivo).name
                tamaño_kb = tamaño_archivo / 1024
                
                # Poner el nombre del archivo en lineEdit_4
                self.ui.lineEdit_4.setText(nombre_archivo)
                
                # Opcional: Cambiar el estilo del botón para indicar que el archivo fue cargado
                self.ui.indexbtn2.setText("✓ Archivo Cargado")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                
                print(f"✅ Archivo cargado: {nombre_archivo} ({tamaño_kb:.1f} KB)")
                
        except Exception as e:
            print(f"❌ Error al subir archivo: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo cargar el archivo: {str(e)}"
            )
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit_5.text().strip()
            veterinario = self.ui.lineEdit.text().strip()
            procedimiento = self.ui.comboBox.currentText().strip()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit_5.setFocus()
                return False
                
            if not veterinario:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre del veterinario es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not procedimiento:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Procedimiento es obligatorio")
                self.ui.comboBox.setFocus()
                return False
                
            # Verificar que el animal existe en la base de datos
            if not self.verificar_animal_existe(arete):
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    f"No se encontró un animal con el arete: {arete}"
                )
                self.ui.lineEdit_5.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def verificar_animal_existe(self, arete):
        """Verifica si el animal existe en la base de datos"""
        try:
            # Buscar en becerros
            becerro = self.db.obtener_becerro_por_arete(arete)
            if becerro:
                self.tipo_animal = "Becerro"
                return True
                
            # Buscar en ganado
            animal = self.db.obtener_animal_por_arete(arete)
            if animal:
                self.tipo_animal = "Ganado"
                return True
                
            return False
            
        except Exception as e:
            print(f"❌ Error verificando existencia del animal: {e}")
            return False
    
    def guardar_salud(self):
        """Guarda el nuevo registro de salud en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete = self.ui.lineEdit_5.text().strip()
            veterinario = self.ui.lineEdit.text().strip()
            procedimiento = self.ui.comboBox.currentText().strip()
            condicion_salud = self.ui.comboBox_3.currentText().strip()
            medicina_preventiva = self.obtener_medicina_preventiva()
            fecha_revision = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando registro de salud:")
            print(f"   Arete: {arete}")
            print(f"   Veterinario: {veterinario}")
            print(f"   Procedimiento: {procedimiento}")
            print(f"   Condición: {condicion_salud}")
            print(f"   Medicina preventiva: {medicina_preventiva}")
            print(f"   Fecha: {fecha_revision}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Archivo cargado: {'Sí' if self.archivo_data else 'No'}")
            
            # Determinar el tipo de animal si no se proporcionó
            if not self.tipo_animal:
                self.verificar_animal_existe(arete)
            
            # Insertar en la base de datos
            if self.insertar_registro_salud(
                arete=arete,
                tipo_animal=self.tipo_animal or "Desconocido",
                veterinario=veterinario,
                procedimiento=procedimiento,
                medicina_preventiva=medicina_preventiva,
                condicion_salud=condicion_salud,
                fecha_revision=fecha_revision,
                observaciones=observaciones,
                archivo=self.archivo_data
            ):
                # ✅ REGISTRAR EN BITÁCORA: Inserción exitosa
                if self.bitacora_controller:
                    datos_salud = f"Arete: {arete}, Procedimiento: {procedimiento}, Veterinario: {veterinario}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Salud",
                        accion="ALTA_REGISTRO_SALUD",
                        descripcion="Nuevo registro de salud agregado",
                        detalles=datos_salud,
                        arete_afectado=arete
                    )
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Registro de salud guardado correctamente")
                self.accept()
            else:
                # ✅ REGISTRAR EN BITÁCORA: Error en inserción
                if self.bitacora_controller:
                    self.bitacora_controller.registrar_accion(
                        modulo="Salud",
                        accion="ERROR_INSERTAR_SALUD",
                        descripcion="Error al intentar agregar registro de salud",
                        detalles=f"Arete: {arete}, Procedimiento: {procedimiento}",
                        arete_afectado=arete
                    )
                
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el registro de salud")
                
        except Exception as e:
            print(f"❌ Error al guardar registro de salud: {e}")
            
            # ✅ REGISTRAR EN BITÁCORA: Excepción
            if self.bitacora_controller:
                self.bitacora_controller.registrar_accion(
                    modulo="Salud",
                    accion="EXCEPCION_INSERTAR_SALUD",
                    descripcion="Excepción al guardar registro de salud",
                    detalles=f"Error: {str(e)}",
                    arete_afectado=self.ui.lineEdit_5.text().strip()
                )
            
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def insertar_registro_salud(self, arete, tipo_animal, veterinario, procedimiento, 
                              medicina_preventiva, condicion_salud, fecha_revision, 
                              observaciones, archivo=None):
        """Inserta el registro de salud en la base de datos"""
        try:
            # Primero verificamos si la tabla tsalud existe
            tablas = self.db.listar_tablas()
            if 'tsalud' not in tablas:
                print("❌ La tabla 'tsalud' no existe, creándola...")
                if not self.crear_tabla_salud():
                    return False
            
            # Insertar en la tabla tsalud
            query = """
            INSERT INTO tsalud 
            (areteanimal, tipoanimal, nomvet, procedimiento, medprev, condicionsalud, fecharev, observacionsalud, archivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (arete, tipo_animal, veterinario, procedimiento, medicina_preventiva, 
                     condicion_salud, fecha_revision, observaciones, archivo)
            
            cursor = self.db.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Registro de salud insertado correctamente para arete: {arete}")
                return True
            else:
                print(f"❌ Error al insertar registro de salud")
                return False
                
        except Exception as e:
            print(f"❌ Error en insertar_registro_salud: {e}")
            return False
    
    def crear_tabla_salud(self):
        """Crea la tabla tsalud si no existe"""
        try:
            query = """
            CREATE TABLE IF NOT EXISTS tsalud (
                idsalud INTEGER PRIMARY KEY AUTOINCREMENT,
                areteanimal TEXT NOT NULL,
                tipoanimal TEXT NOT NULL,
                nomvet TEXT NOT NULL,
                procedimiento TEXT NOT NULL,
                medprev TEXT,
                condicionsalud TEXT,
                fecharev DATE NOT NULL,
                observacionsalud TEXT,
                archivo BLOB
            )
            """
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Tabla 'tsalud' creada exitosamente")
                return True
            else:
                print("❌ Error al crear tabla 'tsalud'")
                return False
        except Exception as e:
            print(f"❌ Error creando tabla salud: {e}")
            return False

    def ver_registros_salud(self):
        """Abre la página de reportes de salud con el arete actual filtrado"""
        try:
            arete = self.ui.lineEdit_5.text().strip()
            if not arete:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    "Ingrese un arete para ver sus registros de salud"
                )
                return

            print(f"🔍 Abriendo reportes de salud para arete: {arete}")
            
            # Buscar el MainWindow en la jerarquía de padres
            if self.main_window:
            # Cerrar este diálogo primero
                self.accept()
            # Abrir la página de reportes de salud con el arete filtrado
                self.main_window.mostrar_reportes_salud_con_filtro(arete)
            else:
            # Si no hay referencia directa, intentar buscar en la jerarquía
                main_window = self._obtener_main_window()
                if main_window:
                    self.accept()
                    main_window.mostrar_reportes_salud_con_filtro(arete)
                else:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Error", 
                       "No se pudo encontrar la ventana principal."
                    )
                
        except Exception as e:
            print(f"❌ Error al ver registros de salud: {e}")
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error al abrir reportes: {str(e)}"
            )

    def _obtener_main_window(self):
        """Obtiene la ventana principal (MainWindow) de la jerarquía de padres"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'cambiar_pagina') and hasattr(parent, 'mostrar_reportes_salud_con_filtro'):
                return parent
            parent = parent.parent()
        return None

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_4.clear()
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.textEdit.clear()
        
        # Limpiar checkboxes
        for i in range(4, 11):  # checkBox_4 a checkBox_10
            checkbox = getattr(self.ui, f'checkBox_{i}', None)
            if checkbox:
                checkbox.setChecked(False)
        
        # Limpiar checkBox, checkBox_2, checkBox_3 (numeración irregular)
        if hasattr(self.ui, 'checkBox'):
            self.ui.checkBox.setChecked(False)
        if hasattr(self.ui, 'checkBox_2'):
            self.ui.checkBox_2.setChecked(False)
        if hasattr(self.ui, 'checkBox_3'):
            self.ui.checkBox_3.setChecked(False)
        
        # Limpiar archivo
        self.archivo_data = None
        self.archivo_ruta = None
        self.ui.indexbtn2.setText("Subir archivo")
        self.ui.indexbtn2.setStyleSheet("")  # Resetear estilo
        
        # Restablecer fecha actual
        self.configurar_fecha()
        
        print("✅ Formulario de salud limpiado")