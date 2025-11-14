# bitacora_controller.py - VERSIÓN CORREGIDA
import os
import sqlite3
from datetime import datetime, date, timedelta
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch

try:
    import pytz
    PYTZ_DISPONIBLE = True
except ImportError:
    PYTZ_DISPONIBLE = False
    print("⚠️  pytz no está instalado. Usando hora local. Instala con: pip install pytz")

class BitacoraController:
    def __init__(self, ui, db, usuario_actual=None):
        """
        Controlador para la gestión de bitácora de actividades
        """
        self.ui = ui
        self.db = db
        self.usuario_actual = usuario_actual
        self.setup_ui()
        self.connect_signals()
        
        # Crear tabla de bitácora si no existe
        self.crear_tabla_bitacora()
        
        print("✅ Controlador de bitácora inicializado")

    def setup_ui(self):
        """Configuración inicial de la interfaz"""
        # Establecer fechas por defecto (últimos 30 días)
        fecha_hasta = date.today()
        fecha_desde = fecha_hasta - timedelta(days=30)
        
        self.ui.dateEdit_desde.setDate(fecha_desde)
        self.ui.dateEdit_hasta.setDate(fecha_hasta)
        
        print("✅ UI de bitácora configurada")

    def connect_signals(self):
        """Conectar todas las señales de la interfaz"""
        try:
            # Botón de generar reporte
            self.ui.pushButton_generar.clicked.connect(self.generar_reporte_pdf)
            
            print("✅ Señales de bitácora conectadas correctamente")
            
        except Exception as e:
            print(f"❌ Error conectando señales de bitácora: {e}")

    def obtener_hora_mexico(self):
        """Obtener la hora actual de México (Central Time) - CORREGIDO"""
        try:
            if PYTZ_DISPONIBLE:
                # Zona horaria de México (Ciudad de México)
                zona_mexico = pytz.timezone('America/Mexico_City')
                hora_actual = datetime.now(zona_mexico)
                return hora_actual.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Fallback: usar hora local con offset manual para México (UTC-6)
                # NOTA: Usamos datetime.utcnow() directamente sin importar de nuevo
                hora_utc = datetime.utcnow()
                hora_mexico = hora_utc - timedelta(hours=6)  # Aproximación para UTC-6
                return hora_mexico.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"⚠️  Error obteniendo hora México: {e}, usando hora local")
            # Fallback final: hora local del sistema
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def crear_tabla_bitacora(self):
        """Crear la tabla de bitácora si no existe - ACTUALIZADO"""
        try:
            query = """
            CREATE TABLE IF NOT EXISTS tbitacora (
                id_bitacora INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario TEXT NOT NULL,
                modulo TEXT NOT NULL,
                accion TEXT NOT NULL,
                descripcion TEXT,
                detalles TEXT,
                arete_afectado TEXT
            )
            """
            cursor = self.db.ejecutar_consulta(query)
            if cursor:
                print("✅ Tabla de bitácora verificada/creada correctamente")
                
                # ✅ VERIFICAR Y AGREGAR COLUMNAS FALTANTES
                self.verificar_estructura_bitacora()
                
                return True
            return False
        except Exception as e:
            print(f"❌ Error creando tabla de bitácora: {e}")
            return False

    def verificar_estructura_bitacora(self):
        """Verificar y actualizar la estructura de la tabla bitácora"""
        try:
            print("🔍 Verificando estructura de tabla bitácora...")
            
            # Verificar columnas existentes
            query = "PRAGMA table_info(tbitacora)"
            cursor = self.db.ejecutar_consulta(query)
            
            if cursor:
                columnas = cursor.fetchall()
                columnas_existentes = [col[1] for col in columnas]
                
                print(f"📋 Columnas existentes: {columnas_existentes}")
                
                # Columnas que deben existir
                columnas_requeridas = [
                    'usuario', 'modulo', 'accion', 'descripcion', 
                    'detalles', 'arete_afectado'
                ]
                
                for columna in columnas_requeridas:
                    if columna not in columnas_existentes:
                        print(f"🔧 Agregando columna faltante: {columna}")
                        query_alter = f"ALTER TABLE tbitacora ADD COLUMN {columna} TEXT"
                        resultado = self.db.ejecutar_consulta(query_alter)
                        if resultado:
                            print(f"✅ Columna {columna} agregada correctamente")
                        else:
                            print(f"❌ Error agregando columna {columna}")
                
                print("✅ Estructura de bitácora verificada")
                
        except Exception as e:
            print(f"❌ Error verificando estructura bitácora: {e}")
            
    def registrar_accion(self, modulo, accion, descripcion="", detalles="", arete_afectado=""):
        """
        Registrar una acción en la bitácora - CORREGIDO DEFINITIVO
        """
        try:
            # ✅ VERIFICAR SI HAY USUARIO ACTUAL - ESTRATEGIA MEJORADA
            if not self.usuario_actual:
                print("⚠️  No hay usuario actual para registrar en bitácora")
                usuario = "Desconocido"
            else:
                # ✅ ESTRATEGIA MEJORADA: Priorizar nombre de usuario sobre nombre completo
                if isinstance(self.usuario_actual, dict):
                    print(f"🔍 DEBUG - Diccionario usuario: {self.usuario_actual}")
                    
                    # ESTRATEGIA 1: Buscar específicamente el campo 'usuario' (login)
                    usuario_login = self.usuario_actual.get('usuario')
                    nombre_completo = self.usuario_actual.get('nombre')
                    rol = self.usuario_actual.get('rol')
                    
                    print(f"   🔍 Usuario (login): '{usuario_login}'")
                    print(f"   🔍 Nombre completo: '{nombre_completo}'") 
                    print(f"   🔍 Rol: '{rol}'")
                    
                    # ✅ DECISIÓN INTELIGENTE: Usar login si está disponible
                    if usuario_login and usuario_login.strip():
                        usuario = usuario_login
                        print(f"   ✅ Usando LOGIN: {usuario}")
                    elif nombre_completo and nombre_completo.strip():
                        usuario = nombre_completo
                        print(f"   ✅ Usando NOMBRE: {usuario}")
                    elif rol and rol.strip():
                        usuario = rol
                        print(f"   ✅ Usando ROL: {usuario}")
                    else:
                        usuario = "Desconocido"
                        print("   ⚠️  Usando valor por defecto")
                        
                else:
                    usuario = str(self.usuario_actual)
                    print(f"   ℹ️  Usuario no es diccionario: {usuario}")
                
                print(f"👤 FINAL - Usuario para bitácora: {usuario}")
            
            # ✅ OBTENER HORA DE MÉXICO
            fecha_hora = self.obtener_hora_mexico()
            
            # ✅ REGISTRAR EN BASE DE DATOS
            try:
                query = """
                INSERT INTO tbitacora 
                (fecha, usuario, modulo, accion, descripcion, detalles, arete_afectado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                params = (fecha_hora, usuario, modulo, accion, descripcion, detalles, arete_afectado)
                
                cursor = self.db.ejecutar_consulta(query, params)
                
                if cursor:
                    print(f"✅ Acción registrada en bitácora: {usuario} - {modulo} - {accion}")
                    return True
                else:
                    print(f"❌ Error al registrar acción en bitácora")
                    return False
                    
            except Exception as e:
                print(f"⚠️  Error con consulta completa: {e}")
                
                # ✅ FALLBACK: Intentar con consulta simple
                try:
                    query_simple = """
                    INSERT INTO tbitacora 
                    (fecha, usuario, modulo, accion, descripcion)
                    VALUES (?, ?, ?, ?, ?)
                    """
                    params_simple = (fecha_hora, usuario, modulo, accion, descripcion)
                    
                    cursor_simple = self.db.ejecutar_consulta(query_simple, params_simple)
                    
                    if cursor_simple:
                        print(f"✅ Acción registrada (consulta simple): {usuario} - {modulo} - {accion}")
                        return True
                    else:
                        print(f"❌ Error al registrar acción (consulta simple)")
                        return False
                        
                except Exception as e2:
                    print(f"❌ Error fatal registrando acción: {e2}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en registrar_accion: {e}")
            return False

    def obtener_registros_bitacora(self, fecha_desde, fecha_hasta):
        """
        Obtener registros de bitácora en un rango de fechas
        
        Args:
            fecha_desde (str): Fecha inicial en formato YYYY-MM-DD
            fecha_hasta (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            list: Lista de tuplas con los registros
        """
        try:
            query = """
            SELECT fecha, usuario, modulo, accion, descripcion, detalles, arete_afectado
            FROM tbitacora 
            WHERE DATE(fecha) BETWEEN ? AND ?
            ORDER BY fecha DESC
            """
            cursor = self.db.ejecutar_consulta(query, (fecha_desde, fecha_hasta))
            
            if cursor:
                registros = cursor.fetchall()
                print(f"✅ {len(registros)} registros de bitácora obtenidos del {fecha_desde} al {fecha_hasta}")
                return registros
            return []
            
        except Exception as e:
            print(f"❌ Error obteniendo registros de bitácora: {e}")
            return []

    def generar_reporte_pdf(self):
        """Generar reporte PDF de la bitácora"""
        try:
            # Obtener fechas seleccionadas
            fecha_desde = self.ui.dateEdit_desde.date().toString('yyyy-MM-dd')
            fecha_hasta = self.ui.dateEdit_hasta.date().toString('yyyy-MM-dd')
            
            # Validar fechas
            if fecha_desde > fecha_hasta:
                self.mostrar_error("Error de fechas", "La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.")
                return
            
            # Obtener registros
            registros = self.obtener_registros_bitacora(fecha_desde, fecha_hasta)
            
            if not registros:
                self.mostrar_informacion("Sin registros", 
                                       f"No hay registros de bitácora para el período {fecha_desde} a {fecha_hasta}.")
                return
            
            # Solicitar ubicación para guardar el PDF
            file_path, _ = QFileDialog.getSaveFileName(
                None, 
                "Guardar Reporte de Bitácora", 
                f"Bitacora_{fecha_desde}_a_{fecha_hasta}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return  # Usuario canceló
            
            # Generar PDF
            if self.crear_pdf(registros, file_path, fecha_desde, fecha_hasta):
                self.mostrar_informacion("Éxito", f"Reporte generado exitosamente:\n{file_path}")
                
                # Registrar la acción en la bitácora
                self.registrar_accion(
                    modulo="Bitácora",
                    accion="GENERAR_REPORTE",
                    descripcion=f"Generó reporte PDF del {fecha_desde} al {fecha_hasta}",
                    detalles=f"Total de registros: {len(registros)}"
                )
            else:
                self.mostrar_error("Error", "No se pudo generar el reporte PDF.")
                
        except Exception as e:
            print(f"❌ Error generando reporte PDF: {e}")
            self.mostrar_error("Error", f"Error al generar reporte: {str(e)}")

    def crear_pdf(self, registros, file_path, fecha_desde, fecha_hasta):
        try:
            # Crear documento
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                topMargin=1*inch,
                bottomMargin=1*inch
            )
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Centrado
            )
            
            # Contenido
            story = []
            
            # Título
            title = Paragraph("REPORTE DE BITÁCORA - SISTEMA GANADERO", title_style)
            story.append(title)
            
            # Información del reporte
            usuario_nombre = self.usuario_actual.get('nombre', 'N/A') if self.usuario_actual else 'N/A'
            
            # ✅ CORREGIDO: Usar datetime.now() directamente sin conflicto
            from datetime import datetime
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            info_text = f"""
            <b>Período:</b> {fecha_desde} a {fecha_hasta}<br/>
            <b>Total de registros:</b> {len(registros)}<br/>
            <b>Generado por:</b> {usuario_nombre}<br/>
            <b>Fecha de generación:</b> {fecha_generacion}
            """
            info = Paragraph(info_text, styles['Normal'])
            story.append(info)
            story.append(Spacer(1, 0.3*inch))
            
            # ✅ CORREGIDO: Preparar datos para la tabla SIN la columna ARETE
            table_data = [['Fecha/Hora', 'Usuario', 'Módulo', 'Acción', 'Descripción']]  # Quitado 'Arete'
            
            for registro in registros:
                fecha, usuario, modulo, accion, descripcion, detalles, arete = registro
                
                # Formatear fecha
                if isinstance(fecha, str):
                    fecha_str = fecha
                else:
                    fecha_str = fecha.strftime('%Y-%m-%d %H:%M') if hasattr(fecha, 'strftime') else str(fecha)
                
                # Limitar longitud de campos para que quepan en la tabla
                descripcion_short = (descripcion or '')[:50] + '...' if descripcion and len(descripcion) > 50 else (descripcion or '')
                
                # ✅ CORREGIDO: Quitar el campo arete de la tabla
                table_data.append([
                    fecha_str,
                    usuario or 'N/A',
                    modulo or 'N/A', 
                    accion or 'N/A',
                    descripcion_short
                    # arete or 'N/A'  # ❌ ELIMINADO
                ])
            
            # Crear tabla
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                
                # Filas de datos
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            story.append(table)
            
            # Generar PDF
            doc.build(story)
            print(f"✅ PDF generado exitosamente: {file_path}")
            return True
        
        except Exception as e:
            print(f"❌ Error creando PDF: {e}")
            return False

    def mostrar_error(self, titulo, mensaje):
        """Mostrar mensaje de error"""
        QMessageBox.critical(None, titulo, mensaje)

    def mostrar_informacion(self, titulo, mensaje):
        """Mostrar mensaje informativo"""
        QMessageBox.information(None, titulo, mensaje)

    def mostrar_advertencia(self, titulo, mensaje):
        """Mostrar mensaje de advertencia"""
        QMessageBox.warning(None, titulo, mensaje)

    # Métodos específicos para registrar acciones comunes
    def registrar_login(self, usuario):
        """Registrar inicio de sesión"""
        self.registrar_accion(
            modulo="Sistema",
            accion="LOGIN",
            descripcion="Inicio de sesión en el sistema",
            detalles=f"Usuario: {usuario}"
        )

    def registrar_logout(self, usuario):
        """Registrar cierre de sesión"""
        self.registrar_accion(
            modulo="Sistema",
            accion="LOGOUT",
            descripcion="Cierre de sesión del sistema",
            detalles=f"Usuario: {usuario}"
        )

    def registrar_alta_becerro(self, arete, datos):
        """Registrar alta de becerro"""
        self.registrar_accion(
            modulo="Becerros",
            accion="INSERTAR",
            descripcion="Alta de nuevo becerro",
            detalles=f"Datos: {datos}",
            arete_afectado=arete
        )

    def registrar_edicion_becerro(self, arete, cambios):
        """Registrar edición de becerro"""
        self.registrar_accion(
            modulo="Becerros",
            accion="ACTUALIZAR",
            descripcion="Edición de datos de becerro",
            detalles=f"Cambios: {cambios}",
            arete_afectado=arete
        )

    def registrar_eliminacion_becerro(self, arete):
        """Registrar eliminación de becerro"""
        self.registrar_accion(
            modulo="Becerros",
            accion="ELIMINAR",
            descripcion="Eliminación de becerro",
            detalles=f"Arete eliminado: {arete}",
            arete_afectado=arete
        )

    def registrar_alta_animal(self, arete, datos):
        """Registrar alta de animal"""
        self.registrar_accion(
            modulo="Animales",
            accion="INSERTAR",
            descripcion="Alta de nuevo animal",
            detalles=f"Datos: {datos}",
            arete_afectado=arete
        )

    def registrar_edicion_animal(self, arete, cambios):
        """Registrar edición de animal"""
        self.registrar_accion(
            modulo="Animales",
            accion="ACTUALIZAR",
            descripcion="Edición de datos de animal",
            detalles=f"Cambios: {cambios}",
            arete_afectado=arete
        )

    def registrar_eliminacion_animal(self, arete):
        """Registrar eliminación de animal"""
        self.registrar_accion(
            modulo="Animales",
            accion="ELIMINAR",
            descripcion="Eliminación de animal",
            detalles=f"Arete eliminado: {arete}",
            arete_afectado=arete
        )

    def registrar_consulta(self, modulo, criterios):
        """Registrar consulta realizada"""
        self.registrar_accion(
            modulo=modulo,
            accion="CONSULTAR",
            descripcion="Consulta de información",
            detalles=f"Criterios: {criterios}"
        )

    def set_usuario_actual(self, usuario_actual):
        """Establecer el usuario actual - MEJORADO"""
        self.usuario_actual = usuario_actual

        self.diagnostico_usuario_detallado()
    
        # Diagnóstico automático
        try:
            print(f"✅ Usuario actual establecido en bitácora:")
            if isinstance(usuario_actual, dict):
                nombre = usuario_actual.get('nombre', 'No disponible')
                usuario = usuario_actual.get('usuario', 'No disponible')
                rol = usuario_actual.get('rol', 'No disponible')
                print(f"   👤 Nombre: {nombre}")
                print(f"   🔑 Usuario: {usuario}")
                print(f"   🎯 Rol: {rol}")
            else:
                print(f"   📝 Tipo: {type(usuario_actual)}")
                print(f"   📊 Valor: {usuario_actual}")
        except Exception as e:
            print(f"⚠️  Error diagnosticando usuario actual: {e}")

    def diagnostico_bitacora(self):
        """Diagnóstico de la tabla de bitácora"""
        try:
            print("\n🔍 DIAGNÓSTICO TABLA BITÁCORA:")
            
            # Verificar si la tabla existe
            tablas = self.db.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tbitacora' not in tablas:
                print("❌ ERROR: La tabla 'tbitacora' no existe")
                return False
                
            # Contar registros totales
            query_count = "SELECT COUNT(*) FROM tbitacora"
            cursor_count = self.db.ejecutar_consulta(query_count)
            if cursor_count:
                total = cursor_count.fetchone()[0]
                print(f"📊 Total de registros en tbitacora: {total}")
                
            # Verificar algunos registros de ejemplo
            query_ejemplo = "SELECT fecha, usuario, modulo, accion FROM tbitacora ORDER BY fecha DESC LIMIT 5"
            cursor_ejemplo = self.db.ejecutar_consulta(query_ejemplo)
            if cursor_ejemplo:
                ejemplos = cursor_ejemplo.fetchall()
                print("📝 Ejemplos de registros en bitácora:")
                for i, ej in enumerate(ejemplos):
                    print(f"   {i+1}. Fecha: {ej[0]}, Usuario: {ej[1]}, Módulo: {ej[2]}, Acción: {ej[3]}")
            
            # Verificar estructura
            query_estructura = "PRAGMA table_info(tbitacora)"
            cursor_estructura = self.db.ejecutar_consulta(query_estructura)
            if cursor_estructura:
                columnas = cursor_estructura.fetchall()
                print("📋 Estructura de la tabla:")
                for col in columnas:
                    print(f"   - {col[1]} ({col[2]})")
            
            return True
                    
        except Exception as e:
            print(f"❌ Error en diagnóstico bitácora: {e}")
            return False

    def limpiar_recursos(self):
        """Limpiar recursos del controlador"""
        try:
            if hasattr(self.db, 'disconnect'):
                self.db.disconnect()
            print("✅ Recursos de bitácora limpiados")
        except Exception as e:
            print(f"⚠️  Error limpiando recursos de bitácora: {e}")

    def diagnostico_usuario_detallado(self):
        """Diagnóstico detallado del usuario actual"""
        try:
            print("\n🔍 DIAGNÓSTICO DETALLADO USUARIO ACTUAL:")
            
            if not self.usuario_actual:
                print("❌ No hay usuario actual establecido")
                return None
                
            print(f"📋 Tipo: {type(self.usuario_actual)}")
            print(f"📊 Contenido completo: {self.usuario_actual}")
            
            if isinstance(self.usuario_actual, dict):
                print("🗂️  Todas las claves disponibles:")
                for key, value in self.usuario_actual.items():
                    print(f"   - '{key}': '{value}' (tipo: {type(value)})")
                
                # Verificar campos específicos
                campos = ['id', 'usuario', 'nombre', 'rol', 'telefono']
                for campo in campos:
                    valor = self.usuario_actual.get(campo, 'NO EXISTE')
                    print(f"   🔍 {campo}: '{valor}'")
                    
            return self.usuario_actual
            
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            return None

# Script de reparación rápido
def reparar_bitacora_rapido():
    """Reparación rápida de la bitácora"""
    from database import Database
    
    print("🔧 REPARACIÓN RÁPIDA BITÁCORA...")
    db = Database()
    
    if db.connect():
        try:
            # Verificar tabla
            tablas = db.listar_tablas()
            print(f"📋 Tablas: {tablas}")
            
            if 'tbitacora' in tablas:
                # Verificar registros
                query = "SELECT COUNT(*) FROM tbitacora"
                cursor = db.ejecutar_consulta(query)
                if cursor:
                    count = cursor.fetchone()[0]
                    print(f"📊 Registros en bitácora: {count}")
                    
                    # Mostrar últimos registros
                    query_ejemplo = "SELECT * FROM tbitacora ORDER BY fecha DESC LIMIT 3"
                    cursor_ejemplo = db.ejecutar_consulta(query_ejemplo)
                    if cursor_ejemplo:
                        registros = cursor_ejemplo.fetchall()
                        print("📝 Últimos registros:")
                        for reg in registros:
                            print(f"   - {reg}")
            
            # Verificar estructura
            query_estructura = "PRAGMA table_info(tbitacora)"
            cursor_estructura = db.ejecutar_consulta(query_estructura)
            if cursor_estructura:
                columnas = cursor_estructura.fetchall()
                print("📋 Estructura actual:")
                for col in columnas:
                    print(f"   - {col[1]} ({col[2]})")
            
            db.disconnect()
            print("✅ Reparación rápida completada")
            
        except Exception as e:
            print(f"❌ Error en reparación: {e}")
    else:
        print("❌ No se pudo conectar a la BD")

if __name__ == "__main__":
    reparar_bitacora_rapido()