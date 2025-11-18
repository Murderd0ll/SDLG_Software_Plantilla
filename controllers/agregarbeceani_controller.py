# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarbeceani_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarBecerroAAnimalesController(QtWidgets.QDialog):
    def __init__(self, becerro_data=None, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        # Datos del becerro que se va a transferir
        self.becerro_data = becerro_data
        self.arete_original = becerro_data.get('arete', '') if becerro_data else ''
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.cargar_datos_becerro()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_animal)  # Guardar como animal
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables según sea necesario"""
        # Combobox editables
        self.ui.comboBox.setEditable(True)    # Corral
        self.ui.comboBox_2.setEditable(True)  # Sexo (aunque normalmente no se edita)
        self.ui.comboBox_3.setEditable(True)  # Estatus
        
        # Los lineEdit para raza, tipo producción y tipo alimento ya son editables
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos para transferir becerro a animal...")
            
            # 1. SEXO - Valores fijos (pero editable por si acaso)
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - Valores comunes para animales
            self.ui.comboBox_3.clear()
            estatus = ["Activo", "En producción", "Enfermo", "Vendido", "Muerto", "Inactivo"]
            self.ui.comboBox_3.addItems(estatus)
            print(f"✅ Estatus cargados: {estatus}")
            
            # 3. CORRALES - Solo los disponibles (con capacidad) + el corral actual del becerro
            corral_actual = self.becerro_data.get('corral', '') if self.becerro_data else ''
            corrales_data = self.db.obtener_corrales_disponibles()
            
            # Si el corral actual no está en los disponibles, lo agregamos
            corral_actual_encontrado = False
            corrales_finales = []
            
            for corral in corrales_data:
                identcorral, nomcorral, capmax, capactual = corral
                if nomcorral == corral_actual:
                    corral_actual_encontrado = True
                corrales_finales.append(corral)
            
            # Si el corral actual no está en los disponibles, lo buscamos y agregamos
            if corral_actual and not corral_actual_encontrado:
                print(f"🔄 Agregando corral actual que no está disponible: {corral_actual}")
                # Buscar información del corral actual
                query = "SELECT identcorral, nomcorral, capmax, capactual FROM tcorral WHERE nomcorral = ?"
                cursor = self.db.ejecutar_consulta(query, (corral_actual,))
                if cursor:
                    corral_actual_data = cursor.fetchone()
                    if corral_actual_data:
                        corrales_finales.append(corral_actual_data)
                        print(f"✅ Corral actual agregado: {corral_actual}")
            
            self.ui.comboBox.clear()
            
            if corrales_finales:
                corrales = []
                for corral in corrales_finales:
                    identcorral, nomcorral, capmax, capactual = corral
                    animales_actuales = self.db.contar_animales_en_corral(nomcorral)
                    
                    # Convertir capacidades a enteros
                    try:
                        if capmax is None or capmax == '':
                            capmax_int = 0
                        else:
                            capmax_int = int(capmax)
                    except (ValueError, TypeError):
                        capmax_int = 0
                    
                    # Mostrar información de capacidad en el combobox
                    if capmax_int > 0:
                        # Si es el corral actual, mostramos información especial
                        if nomcorral == corral_actual:
                            corrales.append(f"{nomcorral} ({animales_actuales}/{capmax_int}) - Actual")
                        else:
                            corrales.append(f"{nomcorral} ({animales_actuales}/{capmax_int})")
                    else:
                        if nomcorral == corral_actual:
                            corrales.append(f"{nomcorral} ({animales_actuales}/∞) - Actual")
                        else:
                            corrales.append(f"{nomcorral} ({animales_actuales}/∞)")
                
                self.ui.comboBox.addItems(corrales)
                print(f"✅ Corrales cargados: {len(corrales)} (incluyendo corral actual)")
                
                # Seleccionar el corral actual por defecto
                for i, corral_text in enumerate(corrales):
                    if corral_actual in corral_text:
                        self.ui.comboBox.setCurrentIndex(i)
                        break
            else:
                print("⚠️ No se encontraron corrales")
                QtWidgets.QMessageBox.warning(
                    self,
                    "Sin corrales",
                    "No se encontraron corrales en el sistema."
                )
            
            # 4. TIPOS DE PRODUCCIÓN - Valores comunes
            tipos_produccion = ["Leche", "Carne", "Doble propósito", "Cría", "Trabajo"]
            self.ui.lineEdit_7.setText(tipos_produccion[0])  # Valor por defecto
            
            # 5. TIPOS DE ALIMENTO - Valores comunes
            tipos_alimento = ["Pastura", "Granos", "Concentrado", "Mixto", "Suplementado"]
            self.ui.lineEdit_6.setText(tipos_alimento[0])  # Valor por defecto
            
            print("🎉 Datos cargados correctamente para transferir becerro a animal")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar datos: {e}")
            import traceback
            traceback.print_exc()
            self.cargar_valores_minimos()
    
    def cargar_valores_minimos(self):
        """Carga valores mínimos en caso de error"""
        # Sexo
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(["Macho", "Hembra"])
        
        # Estatus
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItems(["Activo", "En producción"])
        
        # Corral
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Corral 1")
        
    def cargar_datos_becerro(self):
        """Carga los datos del becerro en el formulario de animal"""
        if not self.becerro_data:
            print("❌ No hay datos de becerro para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del becerro para transferir: {self.becerro_data}")
            
            # Campos básicos - arete en dos lugares
            arete = self.becerro_data.get('arete', '')
            self.ui.lineEdit.setText(arete)  # Arete editable principal
            self.ui.lineEdit_8.setText(arete)  # Arete en la esquina superior derecha (solo lectura)
            self.ui.lineEdit_8.setReadOnly(True)
            
            # Nombre
            self.ui.lineEdit_2.setText(self.becerro_data.get('nombre', ''))
            
            # Corral (ya se estableció en cargar_datos_combo)
            # Solo nos aseguramos de que esté seleccionado el correcto
            
            # Sexo
            sexo = self.becerro_data.get('sexo', 'Macho')
            index_sexo = self.ui.comboBox_2.findText(sexo)
            if index_sexo >= 0:
                self.ui.comboBox_2.setCurrentIndex(index_sexo)
            
            # Raza
            raza = self.becerro_data.get('raza', '')
            self.ui.lineEdit_5.setText(raza)
            
            # Estatus - por defecto "Activo" para animales nuevos
            estatus = "Activo"
            index_estatus = self.ui.comboBox_3.findText(estatus)
            if index_estatus >= 0:
                self.ui.comboBox_3.setCurrentIndex(index_estatus)
            
            # Fecha de nacimiento
            fecha_nacimiento = self.becerro_data.get('nacimiento', '')
            if fecha_nacimiento:
                try:
                    if isinstance(fecha_nacimiento, str):
                        qdate = QtCore.QDate.fromString(fecha_nacimiento, "yyyy-MM-dd")
                    else:
                        qdate = QtCore.QDate(fecha_nacimiento)
                    self.ui.dateEdit.setDate(qdate)
                except:
                    self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
                    print("⚠️ Error al cargar fecha, usando fecha actual")
            
            # Observaciones
            observaciones = self.becerro_data.get('observacion', '')
            if hasattr(self.ui, 'textEdit') and observaciones:
                self.ui.textEdit.setPlainText(observaciones)
            
            # Foto - cargar si existe
            foto_data = self.becerro_data.get('foto')
            if foto_data:
                self.foto_data = foto_data
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                self.ui.lineEdit_4.setText("Foto cargada desde becerro")
                print("✅ Foto del becerro cargada para transferencia")
            else:
                self.ui.lineEdit_4.clear()
            
            print("🎉 Datos del becerro cargados correctamente para transferencia")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del becerro: {e}")
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
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del animal", 
                "", 
                filtros
            )
            
            if ruta_archivo:
                tamaño_archivo = os.path.getsize(ruta_archivo)
                if tamaño_archivo > 5 * 1024 * 1024:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Archivo muy grande", 
                        "La imagen no puede ser mayor a 5MB"
                    )
                    return
                
                with open(ruta_archivo, 'rb') as archivo:
                    self.foto_data = archivo.read()
                    self.foto_ruta = ruta_archivo
                
                nombre_archivo = Path(ruta_archivo).name
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
    
    def validar_capacidad_corral(self, corral_destino: str) -> bool:
        """Valida que el corral destino tenga capacidad disponible"""
        try:
            # Obtener el corral actual del becerro
            corral_actual = self.becerro_data.get('corral', '') if self.becerro_data else ''
            
            # Si es el mismo corral, no hay problema de capacidad
            if corral_destino == corral_actual:
                return True
            
            # Validar capacidad del corral destino
            capacidad = self.db.obtener_capacidad_corral(corral_destino)
            animales_actuales = self.db.contar_animales_en_corral(corral_destino)
            
            capacidad_maxima = capacidad['capacidad_maxima']
            
            if capacidad_maxima > 0 and animales_actuales >= capacidad_maxima:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Corral lleno",
                    f"El corral '{corral_destino}' ha alcanzado su capacidad máxima ({capacidad_maxima} animales).\n\n"
                    f"Actualmente tiene {animales_actuales} animales.\n"
                    f"Por favor, seleccione otro corral con capacidad disponible."
                )
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error validando capacidad del corral: {e}")
            return True  # Por seguridad, permitir continuar si hay error
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            corral_completo = self.ui.comboBox.currentText().strip()
            corral = corral_completo.split(' (')[0]  # Solo el nombre del corral
            sexo = self.ui.comboBox_2.currentText().strip()
            raza = self.ui.lineEdit_5.text().strip()
            tipo_produccion = self.ui.lineEdit_7.text().strip()
            tipo_alimento = self.ui.lineEdit_6.text().strip()
            estatus = self.ui.comboBox_3.currentText().strip()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            if not corral:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Corral es obligatorio")
                self.ui.comboBox.setFocus()
                return False
                
            if not sexo:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Sexo es obligatorio")
                self.ui.comboBox_2.setFocus()
                return False
                
            if not raza:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Raza es obligatorio")
                self.ui.lineEdit_5.setFocus()
                return False
                
            if not tipo_produccion:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Tipo de producción es obligatorio")
                self.ui.lineEdit_7.setFocus()
                return False
                
            if not tipo_alimento:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Tipo de alimento es obligatorio")
                self.ui.lineEdit_6.setFocus()
                return False
            
            # Validar capacidad del corral
            if not self.validar_capacidad_corral(corral):
                return False
            
            # Verificar si el arete ya existe en animales (si cambió el arete)
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
    
    def guardar_animal(self):
        """Guarda el becerro como animal y lo elimina de la tabla de becerros"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete_original = self.arete_original
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            corral_completo = self.ui.comboBox.currentText().strip()
            corral = corral_completo.split(' (')[0]  # Solo el nombre del corral
            sexo = self.ui.comboBox_2.currentText().strip()
            raza = self.ui.lineEdit_5.text().strip()
            tipo_produccion = self.ui.lineEdit_7.text().strip()
            tipo_alimento = self.ui.lineEdit_6.text().strip()
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            estatus = self.ui.comboBox_3.currentText().strip()
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            print(f"📝 Guardando becerro como animal: {nombre}, Arete: {arete}")
            print(f"   Corral: {corral}, Sexo: {sexo}, Raza: {raza}")
            print(f"   Tipo producción: {tipo_produccion}, Tipo alimento: {tipo_alimento}")
            print(f"   Estatus: {estatus}")
            print(f"   Foto transferida: {'Sí' if self.foto_data else 'No'}")
            
            # ✅ REGISTRAR EN BITÁCORA LA TRANSFERENCIA
            if self.bitacora_controller:
                self.bitacora_controller.registrar_accion(
                    modulo="Transferencia",
                    accion="TRANSFERIR",
                    descripcion=f"Transferencia de becerro a animal: {nombre}",
                    detalles=f"Becerro {arete_original} transferido a animales con arete {arete}",
                    arete_afectado=arete_original
                )
                print("✅ Transferencia registrada en bitácora")
            
            # 1. INSERTAR EN TABLA DE ANIMALES
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
                observaciones=observaciones if observaciones else None,
                foto=self.foto_data
            ):
                print("✅ Animal insertado correctamente en tganado")
                
                # 2. ELIMINAR DE TABLA DE BECERROS
                if self.db.eliminar_becerro_por_arete(arete_original):
                    print("✅ Becerro eliminado correctamente de tbecerros")
                    
                    QtWidgets.QMessageBox.information(
                        self, 
                        "Éxito", 
                        f"Becerro '{nombre}' transferido correctamente a animales y eliminado de becerros"
                    )
                    self.accept()
                else:
                    # Si no se pudo eliminar el becerro, revertir la inserción del animal
                    self.db.eliminar_animal_por_arete(arete)
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Error", 
                        "Error al eliminar el becerro. La operación fue revertida."
                    )
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Error", 
                    "Error al insertar el animal en la base de datos"
                )
                
        except Exception as e:
            print(f"❌ Error al transferir becerro a animal: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"Error durante la transferencia: {str(e)}"
            )
    
    def get_datos_animal(self):
        """Retorna los datos del animal creado"""
        return {
            'arete': self.ui.lineEdit.text().strip(),
            'nombre': self.ui.lineEdit_2.text().strip(),
            'corral': self.ui.comboBox.currentText().strip().split(' (')[0],  # Solo el nombre del corral
            'sexo': self.ui.comboBox_2.currentText().strip(),
            'raza': self.ui.lineEdit_5.text().strip(),
            'tipo_produccion': self.ui.lineEdit_7.text().strip(),
            'tipo_alimento': self.ui.lineEdit_6.text().strip(),
            'fecha_nacimiento': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            'estatus': self.ui.comboBox_3.currentText().strip(),
            'observaciones': self.obtener_texto_observaciones(),
            'foto': self.foto_data
        }