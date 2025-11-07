# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editaranimal_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class EditarAnimalController(QtWidgets.QDialog):
    def __init__(self, animal_data=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        self.animal_original = animal_data  # Datos originales del animal
        self.arete_original = animal_data.get('arete', '') if animal_data else ''
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.cargar_datos_animal()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_cambios)  # Guardar
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
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos en combobox para editar animal...")
            
            # 1. SEXO - Valores fijos
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - De BD o valores por defecto
            self.ui.comboBox_6.clear()
            estatus = self.db.obtener_estatus_animales()
            if not estatus:
                estatus = ["Activo", "Enfermo", "Vendido", "Muerto", "En producción"]
                print("📋 Usando estatus por defecto para animales")
            self.ui.comboBox_6.addItems(estatus)
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
            print(f"✅ Tipos de producción cargados: {tipos_produccion}")
            
            # 6. TIPO DE ALIMENTO - Valores por defecto
            self.ui.comboBox_5.clear()
            tipos_alimento = ["Pastura", "Granos", "Mixto", "Concentrado", "Suplementado"]
            self.ui.comboBox_5.addItems(tipos_alimento)
            print(f"✅ Tipos de alimento cargados: {tipos_alimento}")
            
            print("🎉 Todos los combobox cargados correctamente para editar animal")
            
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
    
    def cargar_datos_animal(self):
        """Carga los datos del animal en el formulario"""
        if not self.animal_original:
            print("❌ No hay datos de animal para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del animal: {self.animal_original}")
            
            # Campos básicos - arete en dos lugares diferentes
            arete = self.animal_original.get('arete', '')
            self.ui.lineEdit.setText(arete)  # Arete editable
            self.ui.lineEdit_5.setText(arete)  # Arete en la esquina superior derecha
            
            self.ui.lineEdit_2.setText(self.animal_original.get('nombre', ''))
            
            # Combobox - establecer valores
            sexo = self.animal_original.get('sexo', 'Macho')
            index_sexo = self.ui.comboBox_2.findText(sexo)
            if index_sexo >= 0:
                self.ui.comboBox_2.setCurrentIndex(index_sexo)
            
            raza = self.animal_original.get('raza', '')
            index_raza = self.ui.comboBox_3.findText(raza)
            if index_raza >= 0:
                self.ui.comboBox_3.setCurrentIndex(index_raza)
            else:
                self.ui.comboBox_3.setEditText(raza)
            
            tipo_produccion = self.animal_original.get('tipo_produccion', '')
            if tipo_produccion:
                index_produccion = self.ui.comboBox_4.findText(tipo_produccion)
                if index_produccion >= 0:
                    self.ui.comboBox_4.setCurrentIndex(index_produccion)
                else:
                    self.ui.comboBox_4.setEditText(tipo_produccion)
            
            tipo_alimento = self.animal_original.get('tipo_alimento', '')
            if tipo_alimento:
                index_alimento = self.ui.comboBox_5.findText(tipo_alimento)
                if index_alimento >= 0:
                    self.ui.comboBox_5.setCurrentIndex(index_alimento)
                else:
                    self.ui.comboBox_5.setEditText(tipo_alimento)
            
            corral = self.animal_original.get('corral', '')
            index_corral = self.ui.comboBox.findText(corral)
            if index_corral >= 0:
                self.ui.comboBox.setCurrentIndex(index_corral)
            else:
                self.ui.comboBox.setEditText(corral)
            
            estatus = self.animal_original.get('estatus', 'Activo')
            index_estatus = self.ui.comboBox_6.findText(estatus)
            if index_estatus >= 0:
                self.ui.comboBox_6.setCurrentIndex(index_estatus)
            
            # Fecha de nacimiento
            fecha_nacimiento = self.animal_original.get('fecha_nacimiento', '')
            if fecha_nacimiento:
                try:
                    if isinstance(fecha_nacimiento, str):
                        qdate = QtCore.QDate.fromString(fecha_nacimiento, "yyyy-MM-dd")
                    else:
                        qdate = QtCore.QDate(fecha_nacimiento)
                    self.ui.dateEdit.setDate(qdate)
                except:
                    # Si hay error con la fecha, usar fecha actual
                    self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
                    print("⚠️ Error al cargar fecha, usando fecha actual")
            
            # Observaciones
            observaciones = self.animal_original.get('observaciones', '')
            if hasattr(self.ui, 'textEdit') and observaciones:
                self.ui.textEdit.setPlainText(observaciones)
            
            # Foto - cargar si existe
            foto_data = self.animal_original.get('foto')
            if foto_data:
                self.foto_data = foto_data
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                self.ui.lineEdit_4.setText("Foto cargada desde BD")
                print("✅ Foto del animal cargada desde BD")
            else:
                self.ui.lineEdit_4.clear()
            
            print("🎉 Datos del animal cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del animal: {e}")
            import traceback
            traceback.print_exc()
    
    def obtener_texto_observaciones(self):
        """Obtiene el texto de observaciones del QTextEdit"""
        if hasattr(self.ui, 'textEdit'):
            return self.ui.textEdit.toPlainText().strip()
        return ""
    
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
                
                # Actualizar la interfaz
                self.ui.lineEdit_4.setText(nombre_archivo)
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
            
            # Verificar si el arete ya existe (solo si cambió el arete)
            if arete != self.arete_original:
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
    
    def guardar_cambios(self):
        """Guarda los cambios del animal en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete_original = self.arete_original
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
            
            print(f"📝 Guardando cambios del animal: {nombre}, Arete: {arete}")
            print(f"   Arete original: {arete_original}")
            print(f"   Sexo: {sexo}, Raza: {raza}")
            print(f"   Producción: {tipo_produccion}, Alimento: {tipo_alimento}")
            print(f"   Corral: {corral}, Estatus: {estatus}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto actualizada: {'Sí' if self.foto_data else 'No'}")
            
            # Actualizar en la base de datos
            if self.db.actualizar_animal(
                arete_original=arete_original,
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
                foto=self.foto_data  # Incluir la foto como BLOB (puede ser None)
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Animal actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el animal")
                
        except Exception as e:
            print(f"❌ Error al actualizar animal: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def get_datos_actualizados(self):
        """Retorna los datos actualizados del animal"""
        return {
            'arete': self.ui.lineEdit.text().strip(),
            'nombre': self.ui.lineEdit_2.text().strip(),
            'sexo': self.ui.comboBox_2.currentText(),
            'raza': self.ui.comboBox_3.currentText().strip(),
            'tipo_produccion': self.ui.comboBox_4.currentText().strip(),
            'tipo_alimento': self.ui.comboBox_5.currentText().strip(),
            'fecha_nacimiento': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            'corral': self.ui.comboBox.currentText().strip(),
            'estatus': self.ui.comboBox_6.currentText(),
            'observaciones': self.obtener_texto_observaciones(),
            'foto': self.foto_data
        }