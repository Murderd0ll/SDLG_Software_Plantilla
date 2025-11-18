# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.agregarbecerro_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class AgregarBecerroController(QtWidgets.QDialog):
    def __init__(self, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
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
        self.ui.pushButton_2.clicked.connect(self.guardar_becerro)  # Guardar
        self.ui.indexbtn2.clicked.connect(self.subir_foto)  # Subir archivo
        
    def configurar_combobox(self):
        """Configura los combobox para ser editables"""
        # Combobox editables
        self.ui.comboBox.setEditable(True)    # Corral
        self.ui.comboBox_5.setEditable(True)  # Arete madre
        
        # Combobox no editables
        self.ui.comboBox_2.setEditable(False)  # Sexo
        self.ui.comboBox_3.setEditable(False)  # Estatus
        
    def configurar_fecha(self):
        """Configura la fecha actual en el dateEdit"""
        fecha_actual = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(fecha_actual)
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox desde la base de datos"""
        try:
            print("🔄 Iniciando carga de datos para becerros...")
        
            # 1. SEXO - Valores fijos
            self.ui.comboBox_2.clear()
            sexos = ["Macho", "Hembra"]
            self.ui.comboBox_2.addItems(sexos)
            self.ui.comboBox_2.setCurrentIndex(0)
            print(f"✅ Sexos cargados: {sexos}")
        
            # 2. ESTATUS - Valores por defecto
            self.ui.comboBox_3.clear()
            estatus = ["Activo", "Inactivo", "Vendido", "Muerto"]
            self.ui.comboBox_3.addItems(estatus)
            self.ui.comboBox_3.setCurrentIndex(0)
            print(f"✅ Estatus cargados: {estatus}")
        
            # 3. CORRALES - Solo los disponibles (con capacidad)
            corrales_data = self.db.obtener_corrales_disponibles()
            self.ui.comboBox.clear()
        
            if corrales_data:
                corrales = []
                for corral in corrales_data:
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
                        corrales.append(f"{nomcorral} ({animales_actuales}/{capmax_int})")
                    else:
                        corrales.append(f"{nomcorral} ({animales_actuales}/∞)")
                
                self.ui.comboBox.addItems(corrales)
                print(f"✅ Corrales disponibles cargados: {len(corrales)}")
                
                # Si no hay corrales disponibles, mostrar advertencia
                if len(corrales) == 0:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Sin corrales disponibles",
                        "No hay corrales con capacidad disponible. Por favor, agregue más corrales o libere espacio en los existentes."
                    )
            else:
                print("⚠️ No se encontraron corrales disponibles")
                QtWidgets.QMessageBox.warning(
                    self,
                    "Sin corrales",
                    "No se encontraron corrales en el sistema. Por favor, agregue corrales primero."
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
        
            print("🎉 Datos cargados correctamente para becerros")
        
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
        self.ui.comboBox_3.addItems(["Activo", "Inactivo"])
        
        # Limpiar los demás campos
        self.ui.comboBox.clear()
        self.ui.comboBox_5.clear()
        self.ui.comboBox_5.addItem("Sin madre registrada")
    
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
            
            # Verificar si el arete ya existe
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

    def validar_capacidad_corral(self, corral: str) -> bool:
        """Valida que el corral tenga capacidad disponible"""
        try:
            capacidad = self.db.obtener_capacidad_corral(corral)
            animales_actuales = self.db.contar_animales_en_corral(corral)
            
            capacidad_maxima = capacidad['capacidad_maxima']
            
            if capacidad_maxima > 0 and animales_actuales >= capacidad_maxima:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Corral lleno",
                    f"El corral '{corral}' ha alcanzado su capacidad máxima ({capacidad_maxima} animales).\n\n"
                    f"Actualmente tiene {animales_actuales} animales.\n"
                    f"Por favor, seleccione otro corral con capacidad disponible."
                )
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error validando capacidad del corral: {e}")
            return True  # Por seguridad, permitir continuar si hay error
    
    def guardar_becerro(self):
        """Guarda el nuevo becerro en la base de datos"""
        try:
            if not self.validar_datos():
                return
            
            # Obtener datos del formulario
            arete = self.ui.lineEdit.text().strip()
            nombre = self.ui.lineEdit_2.text().strip()
            peso = self.ui.doubleSpinBox.value()
            sexo = self.ui.comboBox_2.currentText()
            raza = self.ui.lineEdit_3.text().strip()  # Ahora es lineEdit
            tipo_produccion = self.ui.lineEdit_7.text().strip() if hasattr(self.ui, 'lineEdit_7') else ""
            tipo_alimento = self.ui.lineEdit_6.text().strip() if hasattr(self.ui, 'lineEdit_6') else ""
            fecha_nacimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            
            # Obtener corral (quitando la información de capacidad del texto)
            corral_completo = self.ui.comboBox.currentText().strip()
            corral = corral_completo.split(' (')[0]  # Solo el nombre del corral
            
            estatus = self.ui.comboBox_3.currentText()  # Ahora es comboBox_3
            arete_madre = self.ui.comboBox_5.currentText().strip()
            observaciones = self.obtener_texto_observaciones()
            
            if arete_madre == "Sin madre registrada" or arete_madre == "Sin madre":
                arete_madre = None
        
            print(f"📝 Guardando becerro: {nombre}, Arete: {arete}")
            print(f"   Corral seleccionado: {corral}")
        
            # Validar capacidad del corral antes de guardar
            if not self.validar_capacidad_corral(corral):
                return
        
            # Insertar en la base de datos
            if self.db.insertar_becerro(
                arete=arete,
                nombre=nombre,
                peso=peso,
                sexo=sexo,
                raza=raza,
                nacimiento=fecha_nacimiento,
                corral=corral,
                estatus=estatus,
                aretemadre=arete_madre,
                observacion=observaciones,
                foto=self.foto_data
            ):
                # ✅ REGISTRAR EN BITÁCORA
                if self.bitacora_controller:
                    datos_becerro = f"Nombre: {nombre}, Arete: {arete}, Peso: {peso}kg, Sexo: {sexo}, Raza: {raza}, Corral: {corral}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Becerros",
                        accion="ALTA",
                        descripcion=f"Alta de nuevo becerro: {nombre}",
                        detalles=datos_becerro,
                        arete_afectado=arete
                    )
                    print("✅ Acción registrada en bitácora")
                else:
                    print("⚠️ No hay controlador de bitácora disponible")
            
                QtWidgets.QMessageBox.information(self, "Éxito", "Becerro agregado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al guardar el becerro")
            
        except Exception as e:
            print(f"❌ Error al guardar becerro: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario incluyendo la foto"""
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()  # Raza
        self.ui.doubleSpinBox.setValue(0.0)
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
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