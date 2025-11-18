# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editarbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class EditarBecerroController(QtWidgets.QDialog):
    def __init__(self, becerro_data=None, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        # Variable para almacenar la foto
        self.foto_data = None
        self.foto_ruta = None
        self.becerro_original = becerro_data  # Datos originales del becerro
        self.arete_original = becerro_data.get('arete', '') if becerro_data else ''
        
        self.setup_connections()
        self.configurar_combobox()
        self.cargar_datos_combo()
        self.cargar_datos_becerro()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_cambios)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables"""
        # Combobox editables
        self.ui.comboBox.setEditable(True)    # Corral
        self.ui.comboBox_5.setEditable(True)  # Arete madre
        
        # Combobox no editables
        self.ui.comboBox_2.setEditable(False)  # Sexo
        self.ui.comboBox_4.setEditable(False)  # Estatus (ahora es comboBox_4)
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos para editar becerro...")
            
            # 1. SEXO - Valores fijos
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            print(f"✅ Sexos cargados: {sexos}")
            
            # 2. ESTATUS - Valores por defecto (ahora es comboBox_4)
            self.ui.comboBox_4.clear()
            estatus = ["Activo", "Inactivo", "Vendido", "Muerto"]
            self.ui.comboBox_4.addItems(estatus)
            print(f"✅ Estatus cargados: {estatus}")
            
            # 3. CORRALES - Solo los disponibles (con capacidad) + el corral actual
            corral_actual = self.becerro_original.get('corral', '') if self.becerro_original else ''
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
            
            # 4. ARETE MADRE - De BD
            aretes_madres = self.db.obtener_aretes_madres()
            self.ui.comboBox_5.clear()
            if aretes_madres:
                self.ui.comboBox_5.addItems(aretes_madres)
                print(f"✅ Arete madres cargados: {len(aretes_madres)}")
            else:
                self.ui.comboBox_5.addItem("Sin madre registrada")
                print("📋 Usando arete madre por defecto")
            
            print("🎉 Datos cargados correctamente para editar becerro")
            
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
        self.ui.comboBox_4.clear()
        self.ui.comboBox_4.addItems(["Activo", "Inactivo"])
        
        # Limpiar los demás campos
        self.ui.comboBox.clear()
        self.ui.comboBox_5.clear()
        self.ui.comboBox_5.addItem("Sin madre registrada")
    
    def cargar_datos_becerro(self):
        """Carga los datos del becerro en el formulario"""
        if not self.becerro_original:
            print("❌ No hay datos de becerro para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del becerro: {self.becerro_original}")
            
            # Campos básicos - arete en dos lugares diferentes
            arete = self.becerro_original.get('arete', '')
            self.ui.lineEdit.setText(arete)  # Arete editable principal
            self.ui.lineEdit_4.setText(arete)  # Arete en la esquina superior derecha (solo lectura)
            self.ui.lineEdit_4.setReadOnly(True)  # Hacerlo de solo lectura
            
            self.ui.lineEdit_2.setText(self.becerro_original.get('nombre', ''))
            
            # Peso - manejo seguro
            peso = self.becerro_original.get('peso', 0.0)
            try:
                peso_float = float(peso) if peso else 0.0
                self.ui.doubleSpinBox.setValue(peso_float)
            except (ValueError, TypeError):
                self.ui.doubleSpinBox.setValue(0.0)
                print("⚠️ Valor de peso inválido, usando 0.0")
            
            # Combobox - establecer valores
            sexo = self.becerro_original.get('sexo', 'Macho')
            index_sexo = self.ui.comboBox_2.findText(sexo)
            if index_sexo >= 0:
                self.ui.comboBox_2.setCurrentIndex(index_sexo)
            
            # El corral ya se estableció en cargar_datos_combo()
            # Aquí solo nos aseguramos de que esté seleccionado el correcto
            
            estatus = self.becerro_original.get('estatus', 'Activo')
            index_estatus = self.ui.comboBox_4.findText(estatus)  # Ahora es comboBox_4
            if index_estatus >= 0:
                self.ui.comboBox_4.setCurrentIndex(index_estatus)
            
            arete_madre = self.becerro_original.get('aretemadre', '')
            if arete_madre:
                index_madre = self.ui.comboBox_5.findText(arete_madre)
                if index_madre >= 0:
                    self.ui.comboBox_5.setCurrentIndex(index_madre)
                else:
                    self.ui.comboBox_5.setEditText(arete_madre)
            
            # Campos que ahora son lineedits
            raza = self.becerro_original.get('raza', '')
            self.ui.lineEdit_7.setText(raza)  # Raza
            
            # Fecha de nacimiento
            fecha_nacimiento = self.becerro_original.get('nacimiento', '')
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
            observaciones = self.becerro_original.get('observacion', '')
            if hasattr(self.ui, 'textEdit') and observaciones:
                self.ui.textEdit.setPlainText(observaciones)
            
            # Foto - cargar si existe
            foto_data = self.becerro_original.get('foto')
            if foto_data:
                self.foto_data = foto_data
                self.ui.indexbtn2.setText("✓ Foto Cargada")
                self.ui.indexbtn2.setStyleSheet("QPushButton { background-color: #27ae60; color: white; }")
                self.ui.lineEdit_5.setText("Foto cargada desde BD")
                print("✅ Foto del becerro cargada desde BD")
            else:
                self.ui.lineEdit_5.clear()
            
            print("🎉 Datos del becerro cargados correctamente")
            
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
            # Configurar los filtros de archivo
            filtros = "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Todos los archivos (*)"
            
            # Abrir diálogo de selección de archivo
            ruta_archivo, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 
                "Seleccionar foto del becerro", 
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
                self.ui.lineEdit_5.setText(nombre_archivo)
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
            peso = self.ui.doubleSpinBox.value()
            
            if not arete:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Arete es obligatorio")
                self.ui.lineEdit.setFocus()
                return False
                
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
                
            if peso <= 0:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso debe ser mayor a 0")
                self.ui.doubleSpinBox.setFocus()
                return False
            
            # Verificar si el arete ya existe (solo si cambió el arete)
            if arete != self.arete_original:
                becerro_existente = self.db.obtener_becerro_por_arete(arete)
                if becerro_existente:
                    QtWidgets.QMessageBox.warning(
                        self, 
                        "Arete duplicado", 
                        f"Ya existe un becerro con el arete: {arete}"
                    )
                    self.ui.lineEdit.setFocus()
                    return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error en validación: {str(e)}")
            return False

    def validar_capacidad_corral(self, corral_destino: str) -> bool:
        """Valida que el corral destino tenga capacidad disponible"""
        try:
            # Obtener el corral actual del becerro
            corral_actual = self.becerro_original.get('corral', '')
            
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
    
    def guardar_cambios(self):
        """Guarda los cambios del becerro en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            arete_original = self.arete_original
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            sexo = self.ui.comboBox_2.currentText()
            raza = self.ui.lineEdit_7.text().strip()  # Ahora es lineEdit
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            
            # Obtener corral (quitando la información de capacidad del texto)
            corral_completo = self.ui.comboBox.currentText().strip()
            corral = corral_completo.split(' (')[0]  # Solo el nombre del corral
            
            estatus = self.ui.comboBox_4.currentText()  # Ahora es comboBox_4
            arete_madre = self.ui.comboBox_5.currentText().strip()
            
            # Obtener observaciones
            observaciones = self.obtener_texto_observaciones()
            
            # Si arete_madre es el valor por defecto, guardar como None
            if arete_madre in ["Sin madre registrada", "Sin madre", ""]:
                arete_madre = None
            
            print(f"📝 Guardando cambios del becerro: {nombre}, Arete: {arete}")
            print(f"   Arete original: {arete_original}")
            print(f"   Corral seleccionado: {corral}")
            print(f"   Peso: {peso}, Sexo: {sexo}, Raza: {raza}")
            print(f"   Corral: {corral}, Estatus: {estatus}")
            print(f"   Arete madre: {arete_madre}")
            print(f"   Observaciones: {observaciones}")
            print(f"   Foto actualizada: {'Sí' if self.foto_data else 'No'}")
            
            # Validar capacidad del corral destino
            if not self.validar_capacidad_corral(corral):
                return
            
            # ✅ REGISTRAR EN BITÁCORA ANTES DE ACTUALIZAR
            if self.bitacora_controller:
                cambios = []
                if arete != arete_original:
                    cambios.append(f"Arete: {arete_original} → {arete}")
                if nombre != self.becerro_original.get('nombre', ''):
                    cambios.append(f"Nombre: {self.becerro_original.get('nombre', '')} → {nombre}")
                if peso != float(self.becerro_original.get('peso', 0)):
                    cambios.append(f"Peso: {self.becerro_original.get('peso', 0)} → {peso}")
                if sexo != self.becerro_original.get('sexo', ''):
                    cambios.append(f"Sexo: {self.becerro_original.get('sexo', '')} → {sexo}")
                if raza != self.becerro_original.get('raza', ''):
                    cambios.append(f"Raza: {self.becerro_original.get('raza', '')} → {raza}")
                if corral != self.becerro_original.get('corral', ''):
                    cambios.append(f"Corral: {self.becerro_original.get('corral', '')} → {corral}")
                if estatus != self.becerro_original.get('estatus', ''):
                    cambios.append(f"Estatus: {self.becerro_original.get('estatus', '')} → {estatus}")
                if arete_madre != self.becerro_original.get('aretemadre', ''):
                    cambios.append(f"Arete madre: {self.becerro_original.get('aretemadre', '')} → {arete_madre}")
                
                if cambios:
                    cambios_str = ", ".join(cambios)
                    self.bitacora_controller.registrar_accion(
                        modulo="Becerros",
                        accion="ACTUALIZAR",
                        descripcion=f"Edición de becerro: {nombre}",
                        detalles=cambios_str,
                        arete_afectado=arete_original
                    )
                    print("✅ Edición registrada en bitácora con cambios detallados")
            
            # Actualizar en la base de datos
            if self.db.actualizar_becerro(
                arete_original=arete_original,
                arete=arete,
                nombre=nombre,
                peso=str(peso),
                sexo=sexo,
                raza=raza,
                nacimiento=fecha_nacimiento,
                corral=corral,
                estatus=estatus,
                aretemadre=arete_madre,
                observacion=observaciones if observaciones else None,
                foto=self.foto_data
            ):
                QtWidgets.QMessageBox.information(self, "Éxito", "Becerro actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el becerro")
                
        except Exception as e:
            print(f"❌ Error al actualizar becerro: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def get_datos_actualizados(self):
        """Retorna los datos actualizados del becerro"""
        return {
            'arete': self.ui.lineEdit.text().strip(),
            'nombre': self.ui.lineEdit_2.text().strip(),
            'peso': self.ui.doubleSpinBox.value(),
            'sexo': self.ui.comboBox_2.currentText(),
            'raza': self.ui.lineEdit_7.text().strip(),  # Ahora es lineEdit
            'nacimiento': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            'corral': self.ui.comboBox.currentText().strip(),
            'estatus': self.ui.comboBox_4.currentText(),  # Ahora es comboBox_4
            'aretemadre': self.ui.comboBox_5.currentText().strip(),
            'observacion': self.obtener_texto_observaciones(),
            'foto': self.foto_data
        }