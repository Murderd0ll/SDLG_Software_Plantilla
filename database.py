import sqlite3
import os
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name="bdd/SDLGAPP.db"):
        self.db_name = db_name
        self.connection = None
        self.verificar_columna_foto()  # Verificar que la columna de foto existe
        
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
            
            abs_path = os.path.abspath(self.db_name)
            print(f"Abriendo base de datos en: {abs_path}")
        
            self.connection = sqlite3.connect(self.db_name)
            return True
        except sqlite3.Error as e:
            print(f"Error conectando a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()

    def listar_tablas(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            return [fila[0] for fila in cursor.fetchall()]
        return []
            
    def ejecutar_consulta(self, query: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """Ejecuta una consulta y retorna el cursor"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error ejecutando consulta: {e}")
            return None
        
    # MÉTODOS PARA BECERROS
    def obtener_becerros(self) -> List[Tuple]:
        """Obtiene todos los registros de la tabla tbecerros"""
        try:
            print("🔍 BD - Ejecutando consulta para obtener becerros...")
            query = """
            SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                   corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece
            FROM tbecerros
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} registros obtenidos")
                
                # Debug: mostrar los primeros registros con sus IDs
                for i, resultado in enumerate(resultados[:3]):
                    print(f"   Registro {i+1}: ID={resultado[0]}, Arete={resultado[1]}")
                    
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_becerros")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_becerros: {e}")
            return []
        
    def insertar_becerro(self, arete: str, nombre: str, peso: float, sexo: str, raza: str, 
                       nacimiento: str, corral: str, estatus: str, 
                       aretemadre: str, aretepadre: str, observacion: str, foto: bytes = None) -> bool:
        """Inserta un nuevo registro en la tabla tbecerros"""
        query = """
        INSERT INTO tbecerros (aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                           corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (arete, nombre, peso, sexo, raza, nacimiento, corral, estatus, 
                 aretemadre, aretepadre, observacion, foto)
        cursor = self.ejecutar_consulta(query, params)
        return cursor is not None

    def actualizar_becerro(self, idbece: int, arete: str, nombre: str, peso: float, sexo: str, 
                         raza: str, nacimiento: str, corral: str, estatus: str, 
                         aretemadre: str, aretepadre: str, observacion: str, foto: bytes = None) -> bool:
        """Actualiza un registro existente en la tabla tbecerros"""
        query = """
        UPDATE tbecerros 
        SET aretebece=?, nombrebece=?, pesobece=?, sexobece=?, razabece=?, nacimientobece=?, 
            corralbece=?, estatusbece=?, aretemadre=?, aretepadre=?, observacionbece=?, fotobece=?
        WHERE idbece=?
        """
        params = (arete, nombre, peso, sexo, raza, nacimiento, corral, estatus, 
                 aretemadre, aretepadre, observacion, foto, idbece)
        cursor = self.ejecutar_consulta(query, params)
        return cursor is not None

    def eliminar_becerro_por_arete(self, arete: str) -> bool:
        """Elimina un registro de la tabla tbecerros por arete"""
        try:
            print(f"🗑️ BD - Intentando eliminar becerro por arete: {arete}")
            query = "DELETE FROM tbecerros WHERE aretebece = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_becerro_por_arete: {e}")
            return False

    def buscar_becerros_por_nombre(self, nombre: str) -> List[Tuple]:
        """Busca becerros por nombre"""
        query = """
        SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece
        FROM tbecerros
        WHERE nombrebece LIKE ?
        """
        cursor = self.ejecutar_consulta(query, (f'%{nombre}%',))
        if cursor:
            return cursor.fetchall()
        return []

    def obtener_becerro_por_id(self, idbece: int) -> Optional[Tuple]:
        """Obtiene un becerro por su ID"""
        query = """
        SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece
        FROM tbecerros
        WHERE idbece = ?
        """
        cursor = self.ejecutar_consulta(query, (idbece,))
        if cursor:
            return cursor.fetchone()
        return None

    def obtener_becerro_por_arete(self, arete: str) -> Optional[Tuple]:
        """Obtiene un becerro por su arete"""
        query = """
        SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece
        FROM tbecerros
        WHERE aretebece = ?
        """
        cursor = self.ejecutar_consulta(query, (arete,))
        if cursor:
            return cursor.fetchone()
        return None
    
    def obtener_corrales(self) -> List[Tuple]:
        """Obtiene todos los corrales de la tabla tcorrales"""
        query = "SELECT idcorral, nombrecorral FROM tcorrales"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            return cursor.fetchall()
        return []
    
    def obtener_razas_becerros(self) -> List[str]:
        """Obtiene las razas únicas de la tabla tbecerros"""
        query = "SELECT DISTINCT razabece FROM tbecerros WHERE razabece IS NOT NULL AND razabece != ''"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
            print(f"🔍 Razas encontradas en BD: {resultados}")
            return resultados
        print("🔍 No se encontraron razas en la BD")
        return []
    
    def obtener_aretes_madres(self) -> List[str]:
        """Obtiene aretes únicos de animales que pueden ser madres"""
        query = """
        SELECT DISTINCT aretebece FROM tbecerros 
        WHERE aretebece IS NOT NULL AND aretebece != '' AND sexobece = 'Hembra'
        UNION
        SELECT DISTINCT arete FROM tanimales 
        WHERE arete IS NOT NULL AND arete != '' AND sexo = 'Hembra'
        """
        cursor = self.ejecutar_consulta(query)
        if cursor:
            resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
            print(f"🔍 Arete madres encontrados en BD: {resultados}")
            return resultados
        print("🔍 No se encontraron aretes de madres en la BD")
        return []
    
    def obtener_estatus_becerros(self) -> List[str]:
        """Obtiene estatus únicos de la tabla tbecerros"""
        query = "SELECT DISTINCT estatusbece FROM tbecerros WHERE estatusbece IS NOT NULL AND estatusbece != ''"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
            print(f"🔍 Estatus encontrados en BD: {resultados}")
            return resultados
        print("🔍 No se encontraron estatus en la BD")
        return ["Activo", "Enfermo", "Vendido", "Muerto"]  # Valores por defecto
    
    def insertar_nueva_raza(self, raza: str) -> bool:
        """Inserta una nueva raza en algún registro para que aparezca en las opciones"""
        # Buscamos un registro existente para actualizar
        query = "UPDATE tbecerros SET razabece = ? WHERE idbece = (SELECT idbece FROM tbecerros LIMIT 1)"
        cursor = self.ejecutar_consulta(query, (raza,))
        return cursor is not None
    
    def insertar_nuevo_corral(self, nombre_corral: str) -> bool:
        """Inserta un nuevo corral en la tabla tcorrales"""
        query = "INSERT INTO tcorrales (nombrecorral) VALUES (?)"
        cursor = self.ejecutar_consulta(query, (nombre_corral,))
        return cursor is not None
    
    def obtener_corral_por_nombre(self, nombre_corral: str) -> Optional[Tuple]:
        """Obtiene un corral por su nombre"""
        query = "SELECT idcorral, nombrecorral FROM tcorrales WHERE nombrecorral = ?"
        cursor = self.ejecutar_consulta(query, (nombre_corral,))
        if cursor:
            return cursor.fetchone()
        return None

    def obtener_foto_becerro_por_arete(self, arete: str) -> Optional[bytes]:
        """Obtiene la foto de un becerro por su arete"""
        try:
            print(f"🔍 BD - Buscando foto para becerro arete: {arete}")
            query = "SELECT fotobece FROM tbecerros WHERE aretebece = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
            
            if cursor:
                resultado = cursor.fetchone()
                if resultado and resultado[0]:
                    foto_data = resultado[0]
                    print(f"✅ BD - Foto encontrada por arete - Tamaño: {len(foto_data)} bytes")
                    return foto_data
                else:
                    print(f"❌ BD - No se encontró foto para arete: {arete}")
                    return None
            else:
                print(f"❌ BD - Error en consulta para arete: {arete}")
                return None
        except Exception as e:
            print(f"❌ BD - Error en obtener_foto_becerro_por_arete: {e}")
            return None

    def verificar_columna_foto(self):
        """Verifica si existe la columna de foto y la crea si no existe"""
        try:
            # Verificar si la columna existe
            query = "PRAGMA table_info(tbecerros)"
            cursor = self.ejecutar_consulta(query)
            if cursor:
                columnas = cursor.fetchall()
                columnas_existentes = [col[1] for col in columnas]
                
                if 'fotobece' not in columnas_existentes:
                    print("🔧 Columna 'fotobece' no existe, creándola...")
                    query_alter = "ALTER TABLE tbecerros ADD COLUMN fotobece BLOB"
                    cursor_alter = self.ejecutar_consulta(query_alter)
                    if cursor_alter:
                        print("✅ Columna 'fotobece' creada exitosamente")
                        return True
                    else:
                        print("❌ Error al crear columna 'fotobece'")
                        return False
                else:
                    print("✅ Columna 'fotobece' ya existe")
                    return True
        except Exception as e:
            print(f"❌ Error verificando columna foto: {e}")
            return False

    # ✅ MÉTODO NUEVO: Diagnóstico rápido
    def diagnostico_rapido_fotos(self):
        """Diagnóstico rápido para verificar datos"""
        try:
            print("\n🔍 DIAGNÓSTICO RÁPIDO:")
            
            # Verificar si la tabla existe
            tablas = self.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tbecerros' not in tablas:
                print("❌ ERROR: La tabla 'tbecerros' no existe")
                return
                
            # Contar registros totales
            query_count = "SELECT COUNT(*) FROM tbecerros"
            cursor_count = self.ejecutar_consulta(query_count)
            if cursor_count:
                total = cursor_count.fetchone()[0]
                print(f"📊 Total de registros en tbecerros: {total}")
                
            # Verificar algunos registros de ejemplo
            query_ejemplo = "SELECT idbece, aretebece, nombrebece FROM tbecerros LIMIT 3"
            cursor_ejemplo = self.ejecutar_consulta(query_ejemplo)
            if cursor_ejemplo:
                ejemplos = cursor_ejemplo.fetchall()
                print("📝 Ejemplos de registros:")
                for ej in ejemplos:
                    print(f"   - ID: {ej[0]}, Arete: {ej[1]}, Nombre: {ej[2]}")
                
        except Exception as e:
            print(f"❌ Error en diagnóstico rápido: {e}")

    def debug_estructura_tabla(self):
        """Muestra información de debug sobre la estructura de la tabla"""
        try:
            print("\n🔍 DEBUG - ESTRUCTURA TABLA tbecerros:")
            
            # Obtener estructura de la tabla
            query = "PRAGMA table_info(tbecerros)"
            cursor = self.ejecutar_consulta(query)
            if cursor:
                columnas = cursor.fetchall()
                print("📋 Columnas de la tabla:")
                for col in columnas:
                    print(f"   - {col[1]} ({col[2]})")
            
            # Contar registros con fotos
            query_fotos = "SELECT COUNT(*) FROM tbecerros WHERE fotobece IS NOT NULL"
            cursor_fotos = self.ejecutar_consulta(query_fotos)
            if cursor_fotos:
                count_fotos = cursor_fotos.fetchone()[0]
                print(f"📊 Registros con fotos: {count_fotos}")
                
            # Mostrar algunos aretes con sus IDs para referencia
            query_ejemplos = "SELECT idbece, aretebece FROM tbecerros LIMIT 5"
            cursor_ejemplos = self.ejecutar_consulta(query_ejemplos)
            if cursor_ejemplos:
                ejemplos = cursor_ejemplos.fetchall()
                print("📝 Primeros 5 becerros (ID - Arete):")
                for ej in ejemplos:
                    print(f"   - {ej[0]}: {ej[1]}")
                    
        except Exception as e:
            print(f"❌ Error en debug_estructura_tabla: {e}")

    # Método de eliminación por ID (por si acaso lo necesitas)
    def eliminar_becerro(self, idbece: int) -> bool:
        """Elimina un registro de la tabla tbecerros por ID"""
        try:
            print(f"🗑️ BD - Intentando eliminar becerro por ID: {idbece}")
            query = "DELETE FROM tbecerros WHERE idbece = ?"
            cursor = self.ejecutar_consulta(query, (idbece,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_becerro: {e}")
            return False

    def diagnostico_completo(self):
        """Diagnóstico completo de la base de datos"""
        try:
            print("\n🔍 DIAGNÓSTICO COMPLETO DE LA BASE DE DATOS:")
            
            # 1. Verificar estructura de la tabla
            print("\n📋 1. ESTRUCTURA DE TABLA tbecerros:")
            query_estructura = "PRAGMA table_info(tbecerros)"
            cursor_estructura = self.ejecutar_consulta(query_estructura)
            if cursor_estructura:
                columnas = cursor_estructura.fetchall()
                for col in columnas:
                    print(f"   - {col[0]}: {col[1]} ({col[2]}) - PK: {col[5]}")
            
            # 2. Verificar todos los registros con sus IDs
            print("\n📊 2. TODOS LOS REGISTROS CON SUS IDs:")
            query_registros = "SELECT idbece, aretebece, nombrebece FROM tbecerros"
            cursor_registros = self.ejecutar_consulta(query_registros)
            if cursor_registros:
                registros = cursor_registros.fetchall()
                for reg in registros:
                    print(f"   - ID: {reg[0]}, Arete: {reg[1]}, Nombre: {reg[2]}")
            
            # 3. Verificar fotos específicamente
            print("\n🖼️  3. INFORMACIÓN DE FOTOS:")
            query_fotos = """
            SELECT idbece, aretebece, 
                   CASE WHEN fotobece IS NULL THEN 'NULL' 
                        WHEN fotobece = '' THEN 'VACÍO' 
                        ELSE 'CON DATOS' END as estado_foto,
                   LENGTH(fotobece) as tamaño_bytes
            FROM tbecerros
            """
            cursor_fotos = self.ejecutar_consulta(query_fotos)
            if cursor_fotos:
                fotos = cursor_fotos.fetchall()
                for foto in fotos:
                    print(f"   - ID: {foto[0]}, Arete: {foto[1]}, Estado: {foto[2]}, Tamaño: {foto[3]} bytes")
                    
        except Exception as e:
            print(f"❌ Error en diagnóstico completo: {e}")

        # En tu archivo database.py, agrega estos métodos:

def obtener_registros_salud_por_arete(self, arete_becerro: str) -> List[Tuple]:
    """Obtiene todos los registros de salud de un becerro"""
    query = """
    SELECT id_salud, veterinario, procedimiento, condicion_salud, tratamiento, 
           fecha_revision, observaciones, nombre_archivo, fecha_registro
    FROM tsalud 
    WHERE arete_becerro = ?
    ORDER BY fecha_revision DESC
    """
    cursor = self.ejecutar_consulta(query, (arete_becerro,))
    if cursor:
        return cursor.fetchall()
    return []

def obtener_archivo_salud(self, id_salud: int) -> Optional[bytes]:
    """Obtiene el archivo asociado a un registro de salud"""
    query = "SELECT archivo FROM tsalud WHERE id_salud = ?"
    cursor = self.ejecutar_consulta(query, (id_salud,))
    if cursor:
        resultado = cursor.fetchone()
        if resultado and resultado[0]:
            return resultado[0]
    return None