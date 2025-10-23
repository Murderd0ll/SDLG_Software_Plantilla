# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from saludbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class SaludBecerroController(QtWidgets.QDialog):
    def __init__(self, parent=None, arete_becerro=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.arete_becerro = arete_becerro
        
        # Variables para archivos
        self.archivo_data = None
        self.archivo_ruta = None
        self.archivo_nombre = None
        
        self.setup_connections()
        self.cargar_datos_becerro()
        self.cargar_combobox()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_registro_salud)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_archivo)  # Subir archivo
        
    def cargar_datos_becerro(self):
        """Carga los datos del becerro en la interfaz"""
        if not self.arete_becerro:
            return
            
        try:
            # Obtener información del becerro
            becerro = self.db.obtener_becerro_por_arete(self.arete_becerro)
            if becerro:
                # Establecer el arete en el lineEdit
                self.ui.lineEdit_4.setText(self.arete_becerro)
                
                # También podrías mostrar el nombre si quieres
                nombre_becerro = becerro[2] if len(becerro) > 2 else "N/A"
                self.ui.label.setText(f"Salud - {nombre_becerro}")
                
            print(f"✅ Datos del becerro cargados: {self.arete_becerro}")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del becerro: {e}")
    
    def cargar_combobox(self):
        """Carga datos en los combobox"""
        try:
            # Procedimientos comunes
            procedimientos = [
                "Vacunación",
                "Desparasitación", 
                "Aplicación de vitaminas",
                "Curaciones",
                "Cirugía menor",
                "Revisión general",
                "Atención de emergencia"
            ]
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(procedimientos)
            
            # Condiciones de salud
            condiciones = [
                "Excelente",
                "Buena",
                "Regular", 
                "Mala",
                "Enfermo",
                "En recuperación",
                "Crítico"
            ]
            self.ui.comboBox_3.clear()
            self.ui.comboBox_3.addItems(condiciones)
            
            # Configurar fecha actual
            fecha_actual = QtCore.QDate.currentDate()
            self.ui.dateEdit.setDate(fecha_actual)
            
            print("✅ Combobox de salud cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar combobox: {e}")
    
    def subir_archivo(self):
        """Abre un diálogo para seleccionar y cargar un archivo (receta, diagnóstico, etc.)"""
        try:
            # Configurar los filtros de archivo
            filtros = "Documentos (*.pdf *.doc *.docx *.txt);;Imágenes (*.png *.jpg *.jpeg);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar archivo (receta, diagnóstico, etc.)", 
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
                    self.archivo_nombre = Path(ruta_archivo).name
                
                # Actualizar la interfaz para mostrar que se cargó el archivo
                self.ui.indexbtn2.setText(f"Archivo: {self.archivo_nombre}")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                
                tamaño_kb = tamaño_archivo / 1024
                print(f"✅ Archivo cargado: {self.archivo_nombre} ({tamaño_kb:.1f} KB)")
                
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
            veterinario = self.ui.lineEdit.text().strip()
            tratamiento = self.ui.lineEdit_2.text().strip()
            
            if not veterinario:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Veterinario es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not tratamiento:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Tratamiento es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            return False
    
    def guardar_registro_salud(self):
        """Guarda el registro de salud en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            veterinario = self.ui.lineEdit.text().strip()
            procedimiento = self.ui.comboBox.currentText()
            condicion_salud = self.ui.comboBox_3.currentText()
            tratamiento = self.ui.lineEdit_2.text().strip()
            fecha_revision = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            observaciones = self.ui.lineEdit_3.text().strip()
            
            print(f"📝 Guardando registro de salud para becerro: {self.arete_becerro}")
            print(f"   Veterinario: {veterinario}")
            print(f"   Procedimiento: {procedimiento}")
            print(f"   Condición: {condicion_salud}")
            print(f"   Tratamiento: {tratamiento}")
            print(f"   Archivo cargado: {'Sí' if self.archivo_data else 'No'}")
            
            # Insertar en la tabla tsalud (debes crear esta tabla en tu BD)
            if self.insertar_registro_salud(
                arete_becerro=self.arete_becerro,
                veterinario=veterinario,
                procedimiento=procedimiento,
                condicion_salud=condicion_salud,
                tratamiento=tratamiento,
                fecha_revision=fecha_revision,
                observaciones=observaciones,
                archivo=self.archivo_data,
                nombre_archivo=self.archivo_nombre
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Registro de salud guardado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el registro de salud")
                
        except Exception as e:
            print(f"❌ Error al guardar registro de salud: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def insertar_registro_salud(self, arete_becerro, veterinario, procedimiento, condicion_salud, 
                              tratamiento, fecha_revision, observaciones, archivo=None, nombre_archivo=None):
        """Inserta un nuevo registro en la tabla tsalud"""
        try:
            # Primero verificar si la tabla tsalud existe, si no, crearla
            if not self.verificar_tabla_salud():
                self.crear_tabla_salud()
            
            query = """
            INSERT INTO tsalud (arete_becerro, veterinario, procedimiento, condicion_salud, 
                              tratamiento, fecha_revision, observaciones, archivo, nombre_archivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (arete_becerro, veterinario, procedimiento, condicion_salud, 
                     tratamiento, fecha_revision, observaciones, archivo, nombre_archivo)
            
            cursor = self.db.ejecutar_consulta(query, params)
            return cursor is not None
            
        except Exception as e:
            print(f"❌ Error al insertar registro de salud: {e}")
            return False
    
    def verificar_tabla_salud(self):
        """Verifica si existe la tabla tsalud"""
        try:
            tablas = self.db.listar_tablas()
            return 'tsalud' in tablas
        except Exception as e:
            print(f"❌ Error verificando tabla salud: {e}")
            return False
    
    def crear_tabla_salud(self):
        """Crea la tabla tsalud si no existe"""
        try:
            query = """
            CREATE TABLE IF NOT EXISTS tsalud (
                id_salud INTEGER PRIMARY KEY AUTOINCREMENT,
                arete_becerro TEXT NOT NULL,
                veterinario TEXT NOT NULL,
                procedimiento TEXT,
                condicion_salud TEXT,
                tratamiento TEXT NOT NULL,
                fecha_revision DATE NOT NULL,
                observaciones TEXT,
                archivo BLOB,
                nombre_archivo TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (arete_becerro) REFERENCES tbecerros(aretebece)
            )
            """
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Tabla tsalud creada exitosamente")
                return True
            else:
                print("❌ Error al crear tabla tsalud")
                return False
        except Exception as e:
            print(f"❌ Error creando tabla salud: {e}")
            return False
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.ui.lineEdit.clear()
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        
        # Limpiar archivo
        self.archivo_data = None
        self.archivo_ruta = None
        self.archivo_nombre = None
        self.ui.indexbtn2.setText("Subir archivo")
        self.ui.indexbtn2.setStyleSheet("")  # Resetear estilo
        
        # Configurar fecha actual
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)