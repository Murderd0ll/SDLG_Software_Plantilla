# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregaranimal_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarAnimalController(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.configurar_fecha()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_animal)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables según corresponda"""
        # Combobox editables
        self.ui.comboBox.setEditable(True)    # Corral
        self.ui.comboBox_3.setEditable(True)  # Raza
        self.ui.comboBox_4.setEditable(True)  # Tipo de producción
        self.ui.comboBox_5.setEditable(True)  # Tipo de alimento
        
        # Combobox no editables (valores fijos)
        self.ui.comboBox_2.setEditable(False)  # Sexo
        self.ui.comboBox_6.setEditable(False)  # Estatus
        
    def configurar_fecha(self):
        """Configura la fecha actual en el dateEdit"""
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos en combobox para animales...")
            
            # 1. SEXO - Valores fijos
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            self.ui.comboBox_2.setCurrentIndex(0)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - De BD o valores por defecto
            self.ui.comboBox_6.clear()
            estatus = self.db.obtener_estatus_animales()
            if not estatus:
                estatus = ["Activo", "Enfermo", "Vendido", "Muerto", "En producción"]
                print("📋 Usando estatus por defecto para animales")
            self.ui.comboBox_6.addItems(estatus)
            self.ui.comboBox_6.setCurrentIndex(0)
            print(f"✅ Estatus cargados: {estatus}")
            
            # 3. CORRALES - De BD
            corrales_data = self.db.obtener_corrales()
            self.ui.comboBox.clear()
            if corrales_data:
                corrales = [str(corral[1]) for corral in corrales_data]
                self.ui.comboBox.addItems(corrales)
                print(f"✅ Corrales cargados: {len(corrales)}")
            else:
                self.ui.comboBox.addItems(["Corral 1", "Corral 2", "Corral 3"])
                print("📋 Usando corrales por defecto")
            
            # 4. RAZAS - De BD para animales
            razas = self.db.obtener_razas_animales()
            self.ui.comboBox_3.clear()
            if razas:
                self.ui.comboBox_3.addItems(razas)
                print(f"✅ Razas cargadas: {len(razas)}")
            else:
                razas_default = ["Angus", "Hereford", "Charolais", "Brahman", "Holstein"]
                self.ui.comboBox_3.addItems(razas_default)
                print("📋 Usando razas por defecto")
            
            # 5. TIPO DE PRODUCCIÓN - Valores por defecto
            self.ui.comboBox_4.clear()
            tipos_produccion = ["Carne", "Leche", "Doble propósito", "Cría"]
            self.ui.comboBox_4.addItems(tipos_produccion)
            self.ui.comboBox_4.setCurrentIndex(0)
            print(f"✅ Tipos de producción cargados: {tipos_produccion}")
            
            # 6. TIPO DE ALIMENTO - Valores por defecto
            self.ui.comboBox_5.clear()
            tipos_alimento = ["Pastura", "Granos", "Mixto", "Concentrado", "Suplementado"]
            self.ui.comboBox_5.addItems(tipos_alimento)
            self.ui.comboBox_5.setCurrentIndex(0)
            print(f"✅ Tipos de alimento cargados: {tipos_alimento}")
            
            print("🎉 Todos los combobox cargados correctamente para animales")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar combobox: {e}")
            import traceback
            traceback.print_exc()
            self.cargar_valores_minimos()
    
    def cargar_valores_minimos(self):
        """Carga valores mínimos en caso de error"""
        try:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(["Macho", "Hembra"])
            
            self.ui.comboBox_6.clear()
            self.ui.comboBox_6.addItems(["Activo", "Enfermo"])
            
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["Corral 1"])
            
            self.ui.comboBox_3.clear()
            self.ui.comboBox_3.addItems(["Angus"])
            
            self.ui.comboBox_4.clear()
            self.ui.comboBox_4.addItems(["Carne"])
            
            self.ui.comboBox_5.clear()
            self.ui.comboBox_5.addItems(["Pastura"])
            
            print("🆘 Valores mínimos cargados por error")
        except Exception as e:
            print(f"💥 Error incluso cargando valores mínimos: {e}")
    
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones del QTextEdit"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
    def limpiar_observaciones(self):
        """Limpia el widget de observaciones"""
        if hasattr(self.ui, 'textEdit'):
            self.ui.textEdit.clear()
    
    def subir_foto(self):
        """Abre un diálogo para seleccionar y cargar una foto"""
        try:
            # Configurar los filtros de archivo
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del animal", 
                "", 
                filtros
            )
            
            if ruta_archivo:
                # Verificar tamaño del archivo (máximo 5MB)
                tamaño_archivo = os.path.getsize(ruta_archivo)
                if tamaño_archivo > 5 * 1024 * 1024:  # 5MB en bytes
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Archivo muy grande", 
                        "La imagen no puede ser mayor a 5MB"
                    )
                    return
                
                # Leer el archivo como bytes
                with open(ruta_archivo, 'rb') as archivo:
                    self.foto_data = archivo.read()
                    self.foto_ruta = ruta_archivo
                
                # Mostrar información al usuario
                nombre_archivo = Path(ruta_archivo).name
                
                # Poner el nombre del archivo en lineEdit_4
                self.ui.lineEdit_4.setText(nombre_archivo)
                
                # Cambiar el texto y estilo del botón para indicar que la foto fue cargada
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                
                print(f"✅ Foto cargada: {nombre_archivo}")
                
        except Exception as e:
            print(f"❌ Error al subir foto: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"No se pudo cargar la foto: {str(e)}"
            )
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
            
            # Verificar si el arete ya existe
            animal_existente = self.db.obtener_animal_por_arete(arete)
            if animal_existente:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Arete duplicado", 
                    f"Ya existe un animal con el arete: {arete}"
                )
                self.ui.lineEdit.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error en validación: {str(e)}")
            return False
    
    def guardar_animal(self):
        """Guarda el nuevo animal en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            sexo = self.ui.comboBox_2.currentText()
            raza = self.ui.comboBox_3.currentText().strip()
            tipo_produccion = self.ui.comboBox_4.currentText().strip()
            tipo_alimento = self.ui.comboBox_5.currentText().strip()
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            corral = self.ui.comboBox.currentText().strip()
            estatus = self.ui.comboBox_6.currentText()
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando animal: {nombre}, Arete: {arete}")
            print(f"   Sexo: {sexo}, Raza: {raza}")
            print(f"   Producción: {tipo_produccion}, Alimento: {tipo_alimento}")
            print(f"   Corral: {corral}, Estatus: {estatus}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto cargada: {'Sí' if self.foto_data else 'No'}")
            
            # Insertar en la base de datos
            if self.db.insertar_animal(
                arete=arete,
                nombre=nombre,
                sexo=sexo,
                raza=raza,
                tipo_produccion=tipo_produccion,
                tipo_alimento=tipo_alimento,
                fecha_nacimiento=fecha_nacimiento,
                corral=corral,
                estatus=estatus,
                observaciones=observaciones,
                foto=self.foto_data
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Animal agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el animal")
                
        except Exception as e:
            print(f"❌ Error al guardar animal: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario incluyendo la foto"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox_4.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_6.setCurrentIndex(0)
        self.ui.lineEdit_4.clear()
        
        # Limpiar observaciones
        self.limpiar_observaciones()
        
        # Limpiar foto
        self.foto_data = None
        self.foto_ruta = None
        self.ui.indexbtn2.setText("Subir archivo")
        self.ui.indexbtn2.setStyleSheet("")  # Resetear estilo
        
        # Restablecer fecha actual
        self.configurar_fecha()