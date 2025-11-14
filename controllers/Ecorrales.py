# Ecorrales.py - VERSIÓN CON BITÁCORA
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.editarcorral_ui import Ui_Dialog
from database import Database
import os
from pathlib import Path

class EditarCorralController(QtWidgets.QDialog):
    def __init__(self, corral_data=None, parent=None, bitacora_controller=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = Database()
        self.bitacora_controller = bitacora_controller
        
        # Datos originales del corral
        self.corral_original = corral_data
        
        self.setup_connections()
        self.configurar_widgets()
        self.cargar_datos_combo()
        self.cargar_datos_corral()
        
    def setup_connections(self):
        """Configura las conexiones de los botones"""
        self.ui.pushButton.clicked.connect(self.reject)  # Cancelar
        self.ui.pushButton_2.clicked.connect(self.guardar_cambios)  # Guardar
        
    def configurar_widgets(self):
        """Configura los widgets según la UI real"""
        try:
            print("🔍 Configurando widgets según UI...")
            
            self.ui.comboBox_3.setEditable(True)
            self.ui.comboBox_4.setEditable(False)
            
            self.ui.spinBox.setMinimum(0)
            self.ui.spinBox.setMaximum(1000)
            
            self.ui.spinBox_2.setMinimum(1)
            self.ui.spinBox_2.setMaximum(1000)
            
            self.ui.dateEdit.setCalendarPopup(True)
            self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
            
            print("✅ Widgets configurados correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando widgets: {e}")
        
    def cargar_datos_combo(self):
        """Carga datos en los combobox"""
        try:
            print("🔄 Iniciando carga de datos en combobox...")
            
            # Ubicaciones
            self.ui.comboBox_3.clear()
            ubicaciones = ["Norte", "Sur", "Este", "Oeste", "Centro", "Zona A", "Zona B", "Zona C"]
            self.ui.comboBox_3.addItems(ubicaciones)
            print(f"✅ Ubicaciones cargadas: {ubicaciones}")
            
            # Condición
            self.ui.comboBox_4.clear()
            condiciones = ["Excelente", "Bueno", "Regular", "Malo", "En reparación", "Deshabilitado"]
            self.ui.comboBox_4.addItems(condiciones)
            print(f"✅ Condiciones cargadas: {condiciones}")
            
            print("🎉 Todos los combobox cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error crítico al cargar combobox: {e}")
            import traceback
            traceback.print_exc()
            self.cargar_valores_minimos()
    
    def cargar_valores_minimos(self):
        """Carga valores mínimos en caso de error"""
        try:
            self.ui.comboBox_3.clear()
            self.ui.comboBox_3.addItems(["Norte"])
            
            self.ui.comboBox_4.clear()
            self.ui.comboBox_4.addItems(["Bueno"])
            
            print("🆘 Valores mínimos cargados por error")
        except Exception as e:
            print(f"💥 Error incluso cargando valores mínimos: {e}")
    
    def cargar_datos_corral(self):
        """Carga los datos del corral en el formulario"""
        if not self.corral_original:
            print("❌ No hay datos de corral para cargar")
            return
            
        try:
            print(f"🔄 Cargando datos del corral: {self.corral_original}")
            
            self.ui.lineEdit_2.setText(self.corral_original.get('nombre', ''))
            
            ubicacion = self.corral_original.get('ubicacion', '')
            index_ubicacion = self.ui.comboBox_3.findText(ubicacion)
            if index_ubicacion >= 0:
                self.ui.comboBox_3.setCurrentIndex(index_ubicacion)
            else:
                self.ui.comboBox_3.setEditText(ubicacion)
            
            capacidad_actual = self.corral_original.get('capacidad_actual', '0')
            try:
                self.ui.spinBox.setValue(int(capacidad_actual))
            except (ValueError, TypeError):
                self.ui.spinBox.setValue(0)
            
            capacidad_maxima = self.corral_original.get('capacidad_maxima', '10')
            try:
                self.ui.spinBox_2.setValue(int(capacidad_maxima))
            except (ValueError, TypeError):
                self.ui.spinBox_2.setValue(10)
            
            condicion = self.corral_original.get('condicion', 'Bueno')
            index_condicion = self.ui.comboBox_4.findText(condicion)
            if index_condicion >= 0:
                self.ui.comboBox_4.setCurrentIndex(index_condicion)
            
            fecha_mantenimiento = self.corral_original.get('fecha_mantenimiento')
            if fecha_mantenimiento:
                try:
                    if isinstance(fecha_mantenimiento, str):
                        qdate = QtCore.QDate.fromString(fecha_mantenimiento, "yyyy-MM-dd")
                        if not qdate.isValid():
                            qdate = QtCore.QDate.fromString(fecha_mantenimiento, "dd/MM/yyyy")
                    else:
                        qdate = QtCore.QDate(fecha_mantenimiento)
                    
                    if qdate.isValid():
                        self.ui.dateEdit.setDate(qdate)
                    else:
                        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
                except Exception as fecha_error:
                    print(f"⚠️ Error al cargar fecha: {fecha_error}")
                    self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
            else:
                self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
            
            observaciones = self.corral_original.get('observaciones', '')
            self.ui.textEdit.setPlainText(observaciones if observaciones else '')
            
            print("🎉 Datos del corral cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar datos del corral: {e}")
            import traceback
            traceback.print_exc()
    
    def validar_datos(self):
        """Valida que los datos ingresados sean correctos"""
        try:
            nombre = self.ui.lineEdit_2.text().strip()
            
            if not nombre:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El campo Nombre es obligatorio")
                self.ui.lineEdit_2.setFocus()
                return False
            
            capacidad_actual = self.ui.spinBox.value()
            capacidad_maxima = self.ui.spinBox_2.value()
            
            if capacidad_actual > capacidad_maxima:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    f"La capacidad actual ({capacidad_actual}) no puede ser mayor a la capacidad máxima ({capacidad_maxima})"
                )
                self.ui.spinBox.setFocus()
                return False
                
            if capacidad_actual < 0:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Advertencia",
                    "La capacidad actual no puede ser negativa"
                )
                self.ui.spinBox.setFocus()
                return False
                
            if capacidad_maxima <= 0:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Advertencia",
                    "La capacidad máxima debe ser mayor a 0"
                )
                self.ui.spinBox_2.setFocus()
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Error en validación: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error en validación: {str(e)}")
            return False
    
    def guardar_cambios(self):
        """Guarda los cambios del corral en la base de datos"""
        try:
            if not self.validar_datos():
                return
                
            # Obtener datos del formulario
            identificador_original = self.corral_original.get('identificador')
            nombre = self.ui.lineEdit_2.text().strip()
            ubicacion = self.ui.comboBox_3.currentText().strip()
            capacidad_maxima = str(self.ui.spinBox_2.value())
            capacidad_actual = str(self.ui.spinBox.value())
            fecha_mantenimiento = self.ui.dateEdit.date().toString("yyyy-MM-dd")
            condicion = self.ui.comboBox_4.currentText()
            observaciones = self.ui.textEdit.toPlainText().strip()
            
            print(f"📝 Guardando cambios del corral: {nombre}")
            print(f"   Identificador original: {identificador_original}")
            print(f"   Nombre: {nombre}")
            print(f"   Ubicación: {ubicacion}")
            print(f"   Capacidad: {capacidad_actual}/{capacidad_maxima}")
            print(f"   Condición: {condicion}")
            print(f"   Fecha mantenimiento: {fecha_mantenimiento}")
            print(f"   Observaciones: {observaciones}")
            
            # Actualizar en la base de datos
            if self.db.actualizar_corral(
                identificador_original=identificador_original,
                identificador=identificador_original,
                nombre=nombre,
                ubicacion=ubicacion,
                capacidad_maxima=capacidad_maxima,
                capacidad_actual=capacidad_actual,
                fecha_mantenimiento=fecha_mantenimiento,
                condicion=condicion,
                observaciones=observaciones if observaciones else None
            ):
                # ✅ REGISTRAR EN BITÁCORA - AÑADIDO
                if self.bitacora_controller:
                    cambios = f"ID: {identificador_original}, Nombre: {nombre}, Ubicación: {ubicacion}, Capacidad: {capacidad_actual}/{capacidad_maxima}, Condición: {condicion}"
                    self.bitacora_controller.registrar_accion(
                        modulo="Corrales",
                        accion="ACTUALIZAR",
                        descripcion="Actualización de datos de corral",
                        detalles=cambios
                    )
                    print("✅ Actualización registrada en bitácora")
                
                QtWidgets.QMessageBox.information(self, "Éxito", "Corral actualizado correctamente")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Error al actualizar el corral")
                
        except Exception as e:
            print(f"❌ Error al actualizar corral: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al actualizar: {str(e)}")
    
    def get_datos_actualizados(self):
        """Retorna los datos actualizados del corral"""
        return {
            'identificador': self.corral_original.get('identificador'),
            'nombre': self.ui.lineEdit_2.text().strip(),
            'ubicacion': self.ui.comboBox_3.currentText().strip(),
            'capacidad_maxima': str(self.ui.spinBox_2.value()),
            'capacidad_actual': str(self.ui.spinBox.value()),
            'fecha_mantenimiento': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            'condicion': self.ui.comboBox_4.currentText(),
            'observaciones': self.ui.textEdit.toPlainText().strip()
        }