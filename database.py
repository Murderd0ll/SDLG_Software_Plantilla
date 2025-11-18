import hashlib
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
                   corralbece, estatusbece, aretemadre, observacionbece, fotobece
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
                       aretemadre: str, observacion: str, foto: bytes = None) -> bool:
        """Inserta un nuevo registro en la tabla tbecerros"""
        query = """
        INSERT INTO tbecerros (aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                           corralbece, estatusbece, aretemadre, observacionbece, fotobece)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (arete, nombre, peso, sexo, raza, nacimiento, corral, estatus, 
                 aretemadre, observacion, foto)
        cursor = self.ejecutar_consulta(query, params)
        return cursor is not None

    def actualizar_becerro(self, arete_original, arete, nombre, peso, sexo, raza, nacimiento, 
                      corral, estatus, aretemadre=None, observacion=None, foto=None):
        """Actualiza un becerro en la base de datos"""
        try:
            query = """
            UPDATE tbecerros 
            SET aretebece = ?, nombrebece = ?, pesobece = ?, sexobece = ?, razabece = ?, 
                nacimientobece = ?, corralbece = ?, estatusbece = ?, aretemadre = ?, 
                observacionbece = ?, fotobece = ?
            WHERE aretebece = ?
            """
            params = (
                arete, nombre, peso, sexo, raza, nacimiento, corral, 
                estatus, aretemadre, observacion, foto, arete_original
            )
            cursor = self.ejecutar_consulta(query, params)
            if cursor:
                print(f"✅ Becerro actualizado: {arete}")
                return True
            else:
                print(f"❌ Error al actualizar becerro: cursor es None")
                return False
        except Exception as e:
            print(f"❌ Error al actualizar becerro: {e}")
            return False

    def eliminar_registros_salud_por_arete(self, arete: str) -> bool:
        """Elimina todos los registros de salud asociados a un arete"""
        try:
            print(f"🗑️ BD - Intentando eliminar registros de salud para arete: {arete}")
            query = "DELETE FROM tsalud WHERE areteanimal = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
        
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Registros de salud eliminados: {filas_afectadas}")
                return True
            else:
                print("🗑️ BD - Error: cursor es None al eliminar registros de salud")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_registros_salud_por_arete: {e}")
            return False

    def eliminar_registros_reproduccion_por_arete(self, arete: str) -> bool:
        """Elimina todos los registros de reproducción asociados a un arete"""
        try:
            print(f"🗑️ BD - Intentando eliminar registros de reproducción para arete: {arete}")
            query = "DELETE FROM treprod WHERE areteanimal = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
        
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Registros de reproducción eliminados: {filas_afectadas}")
                return True
            else:
                print("🗑️ BD - Error: cursor es None al eliminar registros de reproducción")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_registros_reproduccion_por_arete: {e}")
            return False

    def eliminar_becerro_por_arete(self, arete: str) -> bool:
        """Elimina un registro de la tabla tbecerros por arete y sus registros relacionados"""
        try:
            print(f"🗑️ BD - Intentando eliminar becerro y registros relacionados por arete: {arete}")
        
        # 1. PRIMERO: Eliminar registros de salud relacionados
            print("🗑️ BD - Eliminando registros de salud relacionados...")
            self.eliminar_registros_salud_por_arete(arete)
        
        # 2. SEGUNDO: Eliminar registros de reproducción relacionados  
            print("🗑️ BD - Eliminando registros de reproducción relacionados...")
            self.eliminar_registros_reproduccion_por_arete(arete)
        
        # 3. FINALMENTE: Eliminar el becerro
            print("🗑️ BD - Eliminando becerro...")
            query = "DELETE FROM tbecerros WHERE aretebece = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
        
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Becerro eliminado. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_becerro_por_arete: {e}")
            return False
        
    def buscar_becerros_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca becerros en todos los campos de la tabla"""
        try:
            print(f"🔍 BD - Buscando becerros en todos los campos: '{texto}'")
        
            # Verificar si el texto es un número para búsquedas en peso
            texto_like = f'%{texto}%'
        
            query = """
            SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                corralbece, estatusbece, aretemadre, observacionbece, fotobece
            FROM tbecerros
            WHERE aretebece LIKE ? OR 
                nombrebece LIKE ? OR 
                razabece LIKE ? OR 
                corralbece LIKE ? OR 
                estatusbece LIKE ? OR 
                aretemadre LIKE ? OR 
                observacionbece LIKE ? OR
                sexobece LIKE ? OR
                pesobece LIKE ? OR
                nacimientobece LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like, texto_like, texto_like, texto_like
            ))
        
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} becerros encontrados en búsqueda múltiple")
                return resultados
            return []
        
        except Exception as e:
            print(f"❌ BD - Error en buscar_becerros_en_todos_los_campos: {e}")
            return []
    

    def obtener_becerro_por_arete(self, arete: str) -> Optional[Tuple]:
        """Obtiene un becerro por su arete"""
        query = """
        SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
               corralbece, estatusbece, aretemadre, observacionbece, fotobece
        FROM tbecerros
        WHERE aretebece = ?
        """
        cursor = self.ejecutar_consulta(query, (arete,))
        if cursor:
            return cursor.fetchone()
        return None
    
    def obtener_becerro_completo_por_arete(self, arete):
        """Obtiene todos los datos de un becerro por su arete incluyendo foto"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                       corralbece, estatusbece, aretemadre, observacionbece, fotobece
                FROM tbecerros 
                WHERE aretebece = ?
            """, (arete,))
            return cursor.fetchone()
        except Exception as e:
            print(f"❌ Error al obtener becerro completo por arete: {e}")
            return None
    
    def obtener_corrales(self) -> List[Tuple]:
        """Obtiene todos los corrales de la tabla tcorral"""
        try:
            print("🔍 BD - Obteniendo corrales desde tcorral...")
            query = "SELECT identcorral, nomcorral FROM tcorral"  # Cambiado a tcorral
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} corrales encontrados")
            
                # Debug: mostrar los corrales encontrados
                for corral in resultados:
                    print(f"   - ID: {corral[0]}, Nombre: {corral[1]}")
                
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_corrales")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_corrales: {e}")
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
        try:
            print("🔍 BD - Buscando aretes de madres...")
            query = """
            SELECT DISTINCT aretebece FROM tbecerros 
            WHERE aretebece IS NOT NULL AND aretebece != '' AND sexobece = 'Hembra'
            UNION
            SELECT DISTINCT aretegdo FROM tganado 
            WHERE aretegdo IS NOT NULL AND aretegdo != '' AND sexogdo = 'Hembra'
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
                print(f"✅ BD - Arete madres encontrados: {len(resultados)} - {resultados}")
                return resultados
            print("🔍 No se encontraron aretes de madres en la BD")
            return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_aretes_madres: {e}")
            return []

    def obtener_capacidad_corral(self, nombre_corral: str) -> dict:
        """Obtiene la capacidad máxima y actual de un corral"""
        try:
            query = "SELECT capmax, capactual FROM tcorral WHERE nomcorral = ?"
            cursor = self.ejecutar_consulta(query, (nombre_corral,))
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    capmax, capactual = resultado
                # Convertir a enteros, manejando casos nulos
                    try:
                        if capmax is None or capmax == '':
                            capmax_int = 0
                        else:
                            capmax_int = int(capmax)
                    except (ValueError, TypeError):
                        capmax_int = 0
                    
                    try:
                        if capactual is None or capactual == '':
                            capactual_int = 0
                        else:
                            capactual_int = int(capactual)
                    except (ValueError, TypeError):
                        capactual_int = 0
                
                    return {
                        'capacidad_maxima': capmax_int,
                        'capacidad_actual': capactual_int
                    }
            return {'capacidad_maxima': 0, 'capacidad_actual': 0}
        except Exception as e:
            print(f"❌ Error al obtener capacidad del corral: {e}")
            return {'capacidad_maxima': 0, 'capacidad_actual': 0}

    def contar_animales_en_corral(self, nombre_corral: str) -> int:
        """Cuenta cuántos animales hay en un corral específico"""
        try:
            # Contar en tganado
            query_ganado = "SELECT COUNT(*) FROM tganado WHERE corralgdo = ? AND estatusgdo != 'Muerto' AND estatusgdo != 'Vendido'"
            cursor_ganado = self.ejecutar_consulta(query_ganado, (nombre_corral,))
            count_ganado = cursor_ganado.fetchone()[0] if cursor_ganado else 0
        # Contar en tbecerros (si es necesario)
            query_becerros = "SELECT COUNT(*) FROM tbecerros WHERE corralbece = ? AND estatusbece != 'Muerto' AND estatusbece != 'Vendido'"
            cursor_becerros = self.ejecutar_consulta(query_becerros, (nombre_corral,))
            count_becerros = cursor_becerros.fetchone()[0] if cursor_becerros else 0
        
            total = count_ganado + count_becerros
            print(f"🔢 Animales en corral {nombre_corral}: {total} (ganado: {count_ganado}, becerros: {count_becerros})")
            return total
        except Exception as e:
            print(f"❌ Error al contar animales en corral: {e}")
            return 0

    def obtener_corrales_disponibles(self) -> List[Tuple]:
        """Obtiene solo los corrales que tienen capacidad disponible"""
        try:
            print("🔍 BD - Obteniendo corrales disponibles...")
            query = "SELECT identcorral, nomcorral, capmax, capactual FROM tcorral"
            cursor = self.ejecutar_consulta(query)
            if cursor:
                todos_corrales = cursor.fetchall()
                corrales_disponibles = []
            
                for corral in todos_corrales:
                    identcorral, nomcorral, capmax, capactual = corral
                
                    try:
                        if capmax is None or capmax == '':
                            capmax_int = 0
                        else:
                            capmax_int = int(capmax)
                    except (ValueError, TypeError):
                        capmax_int = 0

                    try:
                        if capactual is None or capactual == '':
                            capactual_int = 0
                        else:
                            capactual_int = int(capactual)
                    except (ValueError, TypeError):
                        capactual_int = 0

                    if capmax_int == 0:
                        corrales_disponibles.append(corral)
                        print(f"✅ Corral sin límite: {nomcorral}")
                        continue
                
                # Contar animales actuales en el corral
                    animales_actuales = self.contar_animales_en_corral(nomcorral)
                
                    if animales_actuales < capmax_int:
                        corrales_disponibles.append(corral)
                        print(f"✅ Corral disponible: {nomcorral} ({animales_actuales}/{capmax_int})")
                    else:
                        print(f"❌ Corral lleno: {nomcorral} ({animales_actuales}/{capmax_int})")
            
                print(f"✅ BD - {len(corrales_disponibles)} corrales disponibles encontrados")
                
                return corrales_disponibles
            else:
                print("❌ BD - Error: cursor es None en obtener_corrales_disponibles")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_corrales_disponibles: {e}")
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

    # MÉTODOS PARA ANIMALES (GANADO)
    def obtener_animales(self) -> List[Tuple]:
        """Obtiene todos los registros de la tabla tganado"""
        try:
            print("🔍 BD - Ejecutando consulta para obtener animales...")
            query = """
            SELECT idgdo, aretegdo, nombregdo, corralgdo, sexogdo, razagdo, prodgdo, 
                   alimentogdo, nacimientogdo, estatusgdo, observaciongdo, fotogdo
            FROM tganado
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} animales obtenidos")
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_animales")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_animales: {e}")
            return []

    def obtener_animal_por_arete(self, arete: str) -> Optional[dict]:
        """Obtiene un animal completo por su arete incluyendo foto - DEVUELVE DICCIONARIO"""
        try:
            query = """
            SELECT idgdo, aretegdo, nombregdo, corralgdo, sexogdo, razagdo, prodgdo, 
                   alimentogdo, nacimientogdo, estatusgdo, observaciongdo, fotogdo
            FROM tganado 
            WHERE aretegdo = ?
            """
            cursor = self.ejecutar_consulta(query, (arete,))
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    # Convertir a diccionario para fácil acceso
                    animal_data = {
                        'id': resultado[0],
                        'arete': resultado[1],
                        'nombre': resultado[2],
                        'corral': resultado[3],
                        'sexo': resultado[4],
                        'raza': resultado[5],
                        'tipo_produccion': resultado[6],
                        'tipo_alimento': resultado[7],
                        'fecha_nacimiento': resultado[8],
                        'estatus': resultado[9],
                        'observaciones': resultado[10],
                        'foto': resultado[11]
                    }
                    print(f"✅ Animal encontrado: {animal_data['nombre']} - {animal_data['arete']}")
                    return animal_data
            print(f"❌ No se encontró animal con arete: {arete}")
            return None
        except Exception as e:
            print(f"❌ Error al obtener animal por arete: {e}")
            return None

    def obtener_animal_por_arete_tupla(self, arete: str) -> Optional[Tuple]:
        """Obtiene un animal por su arete (versión tupla - para compatibilidad)"""
        query = """
        SELECT idgdo, aretegdo, nombregdo, corralgdo, sexogdo, razagdo, prodgdo, 
               alimentogdo, nacimientogdo, estatusgdo, observaciongdo, fotogdo
        FROM tganado
        WHERE aretegdo = ?
        """
        cursor = self.ejecutar_consulta(query, (arete,))
        if cursor:
            return cursor.fetchone()
        return None

    def insertar_animal(self, arete: str, nombre: str, sexo: str, raza: str, tipo_produccion: str,
                       tipo_alimento: str, fecha_nacimiento: str, corral: str, estatus: str,
                       observaciones: str = None, foto: bytes = None) -> bool:
        """Inserta un nuevo registro en la tabla tganado"""
        query = """
        INSERT INTO tganado (aretegdo, nombregdo, sexogdo, razagdo, prodgdo, alimentogdo, 
                           nacimientogdo, corralgdo, estatusgdo, observaciongdo, fotogdo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (arete, nombre, sexo, raza, tipo_produccion, tipo_alimento, fecha_nacimiento, 
                 corral, estatus, observaciones, foto)
        cursor = self.ejecutar_consulta(query, params)
        
        if cursor:
            print(f"✅ Animal insertado correctamente: {nombre} - {arete}")
            return True
        else:
            print(f"❌ Error al insertar animal: {nombre} - {arete}")
            return False

    def actualizar_animal(self, arete_original: str, arete: str, nombre: str, sexo: str, raza: str, 
                         tipo_produccion: str, tipo_alimento: str, fecha_nacimiento: str, 
                         corral: str, estatus: str, observaciones: str = None, foto: bytes = None) -> bool:
        """Actualiza un animal en la base de datos"""
        try:
            query = """
            UPDATE tganado 
            SET aretegdo = ?, nombregdo = ?, sexogdo = ?, razagdo = ?, prodgdo = ?, 
                alimentogdo = ?, nacimientogdo = ?, corralgdo = ?, estatusgdo = ?, 
                observaciongdo = ?, fotogdo = ?
            WHERE aretegdo = ?
            """
            params = (arete, nombre, sexo, raza, tipo_produccion, tipo_alimento, 
                     fecha_nacimiento, corral, estatus, observaciones, foto, arete_original)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"✅ Animal actualizado: {nombre} - {arete}. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print(f"❌ Error al actualizar animal: cursor es None")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar animal: {e}")
            return False

    def obtener_estatus_animales(self) -> List[str]:
        """Obtiene estatus únicos de la tabla tganado"""
        query = "SELECT DISTINCT estatusgdo FROM tganado WHERE estatusgdo IS NOT NULL AND estatusgdo != ''"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
            print(f"🔍 Estatus animales encontrados en BD: {resultados}")
            return resultados
        print("🔍 No se encontraron estatus en la BD para animales")
        return ["Activo", "Enfermo", "Vendido", "Muerto", "En producción"]

    def obtener_razas_animales(self) -> List[str]:
        """Obtiene las razas únicas de la tabla tganado"""
        query = "SELECT DISTINCT razagdo FROM tganado WHERE razagdo IS NOT NULL AND razagdo != ''"
        cursor = self.ejecutar_consulta(query)
        if cursor:
            resultados = [fila[0] for fila in cursor.fetchall() if fila[0]]
            print(f"🔍 Razas animales encontradas en BD: {resultados}")
            return resultados
        print("🔍 No se encontraron razas en la BD para animales")
        return []

    def obtener_foto_animal_por_arete(self, arete: str) -> Optional[bytes]:
        """Obtiene la foto de un animal por su arete"""
        try:
            print(f"🔍 BD - Buscando foto para animal arete: {arete}")
            query = "SELECT fotogdo FROM tganado WHERE aretegdo = ?"
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
            print(f"❌ BD - Error en obtener_foto_animal_por_arete: {e}")
            return None

    def buscar_animales_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        try:
            print(f"🔍 BD - Buscando animales en todos los campos: '{texto}'")
    
            texto_like = f'%{texto}%'
    
            query = """
            SELECT idgdo, aretegdo, nombregdo, corralgdo, sexogdo, razagdo, prodgdo, 
                alimentogdo, nacimientogdo, estatusgdo, observaciongdo, fotogdo
            FROM tganado
            WHERE aretegdo LIKE ? OR 
                nombregdo LIKE ? OR 
                corralgdo LIKE ? OR 
                sexogdo LIKE ? OR 
                razagdo LIKE ? OR 
                prodgdo LIKE ? OR 
                alimentogdo LIKE ? OR 
                estatusgdo LIKE ? OR 
                observaciongdo LIKE ? OR
                nacimientogdo LIKE ?  -- ✅ INCLUYE FECHA DE NACIMIENTO
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like  # ✅ 10 parámetros
            ))
    
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} animales encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_animales_en_todos_los_campos: {e}")
            return []

    def eliminar_animal_por_arete(self, arete: str) -> bool:
        """Elimina un registro de la tabla tganado por arete y sus registros relacionados"""
        try:
            print(f"🗑️ BD - Intentando eliminar animal y registros relacionados por arete: {arete}")
        
        # 1. PRIMERO: Eliminar registros de salud relacionados
            print("🗑️ BD - Eliminando registros de salud relacionados...")
            self.eliminar_registros_salud_por_arete(arete)
        
        # 2. SEGUNDO: Eliminar registros de reproducción relacionados  
            print("🗑️ BD - Eliminando registros de reproducción relacionados...")
            self.eliminar_registros_reproduccion_por_arete(arete)
        
        # 3. FINALMENTE: Eliminar el animal
            print("🗑️ BD - Eliminando animal...")
            query = "DELETE FROM tganado WHERE aretegdo = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
        
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Animal eliminado. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_animal_por_arete: {e}")
            return False

    # MÉTODOS PARA SALUD
    def obtener_archivo_salud(self, id_salud: int) -> Optional[bytes]:
        """Obtiene el archivo asociado a un registro de salud"""
        query = "SELECT archivo FROM tsalud WHERE id_salud = ?"
        cursor = self.ejecutar_consulta(query, (id_salud,))
        if cursor:
            resultado = cursor.fetchone()
            if resultado and resultado[0]:
                return resultado[0]
        return None

    # MÉTODOS PARA CORRALES
    def obtener_corrales_completos(self) -> List[Tuple]:
        """Obtiene todos los registros completos de la tabla tcorral"""
        try:
            print("🔍 BD - Ejecutando consulta para obtener corrales completos...")
            query = """
            SELECT identcorral, nomcorral, ubicorral, capmax, capactual, 
                   fechamant, condicion, observacioncorral
            FROM tcorral
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} corrales completos obtenidos")
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_corrales_completos")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_corrales_completos: {e}")
            return []

    def obtener_corral_por_id(self, idcorral: str) -> Optional[Tuple]:
        """Obtiene un corral por su ID"""
        query = """
        SELECT identcorral, nomcorral, ubicorral, capmax, capactual, 
               fechamant, condicion, observacioncorral
        FROM tcorral
        WHERE identcorral = ?
        """
        cursor = self.ejecutar_consulta(query, (idcorral,))
        if cursor:
            return cursor.fetchone()
        return None

    def buscar_corrales_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca corrales en todos los campos de la tabla tcorral"""
        try:
            print(f"🔍 BD - Buscando corrales en todos los campos: '{texto}'")
    
            texto_like = f'%{texto}%'
    
            query = """
            SELECT identcorral, nomcorral, ubicorral, capmax, capactual, 
                fechamant, condicion, observacioncorral
            FROM tcorral
            WHERE nomcorral LIKE ? OR 
                ubicorral LIKE ? OR 
                capmax LIKE ? OR 
                capactual LIKE ? OR 
                fechamant LIKE ? OR 
                condicion LIKE ? OR 
                observacioncorral LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like
            ))
    
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} corrales encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_corrales_en_todos_los_campos: {e}")
            return []

    def eliminar_corral_por_id(self, idcorral: str) -> bool:
        """Elimina un registro de la tabla tcorral por ID"""
        try:
            print(f"🗑️ BD - Intentando eliminar corral por ID: {idcorral}")
            query = "DELETE FROM tcorral WHERE identcorral = ?"
            cursor = self.ejecutar_consulta(query, (idcorral,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_corral_por_id: {e}")
            return False
        

    # MÉTODOS PARA PROPIETARIOS
    def obtener_propietarios_completos(self) -> List[Tuple]:
        """Obtiene todos los registros completos de la tabla tpropietarios"""
        try:
            print("🔍 BD - Ejecutando consulta para obtener propietarios completos...")
            query = """
            SELECT idprop, nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop
            FROM tpropietarios
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} propietarios completos obtenidos")
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_propietarios_completos")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_propietarios_completos: {e}")
            return []

    def obtener_propietario_por_id(self, idpropietario: str) -> Optional[Tuple]:
        """Obtiene un propietario por su ID"""
        query = """
        SELECT idprop, nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop
        FROM tpropietarios
        WHERE idprop = ?
        """
        cursor = self.ejecutar_consulta(query, (idpropietario,))
        if cursor:
            return cursor.fetchone()
        return None

    def obtener_foto_propietario_por_id(self, idpropietario: str) -> Optional[bytes]:
        """Obtiene la foto de un propietario por su ID"""
        try:
            print(f"🔍 BD - Buscando foto para propietario ID: {idpropietario}")
            query = "SELECT fotoprop FROM tpropietarios WHERE idprop = ?"
            cursor = self.ejecutar_consulta(query, (idpropietario,))
            
            if cursor:
                resultado = cursor.fetchone()
                if resultado and resultado[0]:
                    foto_data = resultado[0]
                    print(f"✅ BD - Foto encontrada por ID - Tamaño: {len(foto_data)} bytes")
                    return foto_data
                else:
                    print(f"❌ BD - No se encontró foto para ID: {idpropietario}")
                    return None
            else:
                print(f"❌ BD - Error en consulta para ID: {idpropietario}")
                return None
        except Exception as e:
            print(f"❌ BD - Error en obtener_foto_propietario_por_id: {e}")
            return None

    def buscar_propietarios_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca propietarios en todos los campos de la tabla tpropietarios"""
        try:
            print(f"🔍 BD - Buscando propietarios en todos los campos: '{texto}'")
    
            texto_like = f'%{texto}%'
    
            query = """
            SELECT idprop, nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop
            FROM tpropietarios
            WHERE nombreprop LIKE ? OR 
                telprop LIKE ? OR 
                correoprop LIKE ? OR 
                dirprop LIKE ? OR 
                psgprop LIKE ? OR 
                uppprop LIKE ? OR 
                rfcprop LIKE ? OR 
                observacionprop LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like, texto_like
            ))
    
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} propietarios encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_propietarios_en_todos_los_campos: {e}")
            return []

    def eliminar_propietario_por_id(self, idpropietario: str) -> bool:
        """Elimina un registro de la tabla tpropietarios por ID"""
        try:
            print(f"🗑️ BD - Intentando eliminar propietario por ID: {idpropietario}")
            query = "DELETE FROM tpropietarios WHERE idprop = ?"
            cursor = self.ejecutar_consulta(query, (idpropietario,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_propietario_por_id: {e}")
            return False

    # MÉTODOS DE DIAGNÓSTICO
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

    # MÉTODOS PARA CORRALES - INSERTAR Y ACTUALIZAR
    def insertar_corral(self, identificador: str, nombre: str, ubicacion: str, capacidad_maxima: str, 
                       capacidad_actual: str, fecha_mantenimiento: str, condicion: str, 
                       observaciones: str = None) -> bool:
        """Inserta un nuevo corral en la tabla tcorral"""
        try:
            print(f"💾 BD - Insertando nuevo corral: {nombre} ({identificador})")
            
            query = """
            INSERT INTO tcorral 
            (identcorral, nomcorral, ubicorral, capmax, capactual, fechamant, condicion, observacioncorral)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (identificador, nombre, ubicacion, capacidad_maxima, capacidad_actual,
                     fecha_mantenimiento, condicion, observaciones)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Corral insertado correctamente: {nombre} - {identificador}")
                return True
            else:
                print(f"❌ Error al insertar corral: {nombre} - {identificador}")
                return False
                
        except Exception as e:
            print(f"❌ Error en insertar_corral: {e}")
            return False

    def actualizar_corral(self, identificador_original: str, identificador: str, nombre: str, 
                         ubicacion: str, capacidad_maxima: str, capacidad_actual: str, 
                         fecha_mantenimiento: str, condicion: str, observaciones: str = None) -> bool:
        """Actualiza un corral en la base de datos"""
        try:
            print(f"💾 BD - Actualizando corral: {nombre} ({identificador})")
            
            query = """
            UPDATE tcorral 
            SET identcorral = ?, nomcorral = ?, ubicorral = ?, capmax = ?, capactual = ?, 
                fechamant = ?, condicion = ?, observacioncorral = ?
            WHERE identcorral = ?
            """
            params = (identificador, nombre, ubicacion, capacidad_maxima, capacidad_actual,
                     fecha_mantenimiento, condicion, observaciones, identificador_original)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"✅ Corral actualizado: {nombre} - {identificador}. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print(f"❌ Error al actualizar corral: cursor es None")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar corral: {e}")
            return False

    # MÉTODOS PARA PROPIETARIOS - INSERTAR Y ACTUALIZAR
    def insertar_propietario(self, nombre: str, telefono: str, correo: str = None, direccion: str = None,
                            psg: str = None, upp: str = None, rfc: str = None, observaciones: str = None,
                            foto: bytes = None) -> bool:
        """Inserta un nuevo propietario en la tabla tpropietarios"""
        try:
            print(f"💾 BD - Insertando nuevo propietario: {nombre}")
            
            query = """
            INSERT INTO tpropietarios 
            (nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (nombre, telefono, correo, direccion, psg, upp, rfc, observaciones, foto)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Propietario insertado correctamente: {nombre}")
                return True
            else:
                print(f"❌ Error al insertar propietario: {nombre}")
                return False
                
        except Exception as e:
            print(f"❌ Error en insertar_propietario: {e}")
            return False

    def actualizar_propietario(self, id_propietario: str, nombre: str, telefono: str, correo: str = None, 
                              direccion: str = None, psg: str = None, upp: str = None, rfc: str = None, 
                              observaciones: str = None, foto: bytes = None) -> bool:
        """Actualiza un propietario en la base de datos"""
        try:
            print(f"💾 BD - Actualizando propietario: {nombre} (ID: {id_propietario})")
            
            query = """
            UPDATE tpropietarios 
            SET nombreprop = ?, telprop = ?, correoprop = ?, dirprop = ?, 
                psgprop = ?, uppprop = ?, rfcprop = ?, observacionprop = ?, fotoprop = ?
            WHERE idprop = ?
            """
            params = (nombre, telefono, correo, direccion, psg, upp, rfc, observaciones, foto, id_propietario)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"✅ Propietario actualizado: {nombre}. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print(f"❌ Error al actualizar propietario: cursor es None")
                return False
                
        except Exception as e:
            print(f"❌ Error al actualizar propietario: {e}")
            return False

    # MÉTODOS ADICIONALES PARA OBTENER DATOS ESPECÍFICOS
    def obtener_propietario_por_id_dict(self, idpropietario: str) -> Optional[dict]:
        """Obtiene un propietario por su ID y devuelve un diccionario"""
        try:
            query = """
            SELECT idprop, nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop
            FROM tpropietarios
            WHERE idprop = ?
            """
            cursor = self.ejecutar_consulta(query, (idpropietario,))
            
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    propietario_data = {
                        'id': resultado[0],
                        'nombre': resultado[1],
                        'telefono': resultado[2],
                        'correo': resultado[3],
                        'direccion': resultado[4],
                        'psg': resultado[5],
                        'upp': resultado[6],
                        'rfc': resultado[7],
                        'observaciones': resultado[8],
                        'foto': resultado[9]
                    }
                    print(f"✅ Propietario encontrado: {propietario_data['nombre']}")
                    return propietario_data
            print(f"❌ No se encontró propietario con ID: {idpropietario}")
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener propietario por ID: {e}")
            return None

    def obtener_corral_por_id_dict(self, idcorral: str) -> Optional[dict]:
        """Obtiene un corral por su ID y devuelve un diccionario"""
        try:
            query = """
            SELECT identcorral, nomcorral, ubicorral, capmax, capactual, 
                   fechamant, condicion, observacioncorral
            FROM tcorral
            WHERE identcorral = ?
            """
            cursor = self.ejecutar_consulta(query, (idcorral,))
            
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    corral_data = {
                        'identificador': resultado[0],
                        'nombre': resultado[1],
                        'ubicacion': resultado[2],
                        'capacidad_maxima': resultado[3],
                        'capacidad_actual': resultado[4],
                        'fecha_mantenimiento': resultado[5],
                        'condicion': resultado[6],
                        'observaciones': resultado[7]
                    }
                    print(f"✅ Corral encontrado: {corral_data['nombre']}")
                    return corral_data
            print(f"❌ No se encontró corral con ID: {idcorral}")
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener corral por ID: {e}")
            return None

    # MÉTODO PARA VERIFICAR SI UN IDENTIFICADOR DE CORRAL YA EXISTE
    def existe_corral_por_id(self, identificador: str) -> bool:
        """Verifica si ya existe un corral con el identificador dado"""
        try:
            query = "SELECT COUNT(*) FROM tcorral WHERE identcorral = ?"
            cursor = self.ejecutar_consulta(query, (identificador,))
            
            if cursor:
                resultado = cursor.fetchone()
                return resultado[0] > 0 if resultado else False
            return False
            
        except Exception as e:
            print(f"❌ Error verificando existencia de corral: {e}")
            return False

    # MÉTODO PARA VERIFICAR SI UN PROPIETARIO YA EXISTE (por nombre y teléfono)
    def existe_propietario(self, nombre: str, telefono: str) -> bool:
        """Verifica si ya existe un propietario con el mismo nombre y teléfono"""
        try:
            query = "SELECT COUNT(*) FROM tpropietarios WHERE nombreprop = ? AND telprop = ?"
            cursor = self.ejecutar_consulta(query, (nombre, telefono))
            
            if cursor:
                resultado = cursor.fetchone()
                return resultado[0] > 0 if resultado else False
            return False
            
        except Exception as e:
            print(f"❌ Error verificando existencia de propietario: {e}")
            return False
        
    def obtener_registros_reproduccion_por_arete(self, arete_animal: str) -> List[Tuple]:
        """Obtiene todos los registros de reproducción de un animal"""
        try:
            query = """
            SELECT id_reproduccion, tipo_servicio, fecha_servicio, toro, 
                   fecha_diagnostico, resultado, observaciones, veterinario
            FROM treproduccion 
            WHERE arete_animal = ?
            ORDER BY fecha_servicio DESC
            """
            cursor = self.ejecutar_consulta(query, (arete_animal,))
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"❌ Error obteniendo registros de reproducción: {e}")
            return []


    def obtener_registros_salud_por_arete(self, arete_animal: str) -> List[Tuple]:
        """Obtiene todos los registros de salud de un animal por su arete - CORREGIDO"""
        try:
            print(f"🔍 BD - Buscando registros de salud para arete: '{arete_animal}'")
        
            # Verificar que el arete no esté vacío
            if not arete_animal or arete_animal.strip() == "":
                print("❌ BD - Arete vacío, retornando lista vacía")
                return []
        
            # Asegurarse de que la conexión esté activa
            if not self.connection:
                self.connect()
            
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            WHERE areteanimal = ?
            ORDER BY fecharev DESC
            """
        
            cursor = self.connection.cursor()
            cursor.execute(query, (arete_animal.strip(),))
            resultados = cursor.fetchall()
        
            print(f"✅ BD - {len(resultados)} registros de salud encontrados para arete: '{arete_animal}'")
        
        # Debug: mostrar los primeros registros
            for i, resultado in enumerate(resultados[:3]):
                print(f"   Registro {i+1}: Arete={resultado[1]}, Procedimiento={resultado[4]}")
            
            return resultados
        
        except Exception as e:
            print(f"❌ BD - Error en obtener_registros_salud_por_arete: {e}")
            import traceback
            traceback.print_exc()
            return []
        
    def buscar_registros_salud_por_arete_y_texto(self, arete_animal: str, texto: str) -> List[Tuple]:
        """Busca registros de salud por texto pero SOLO para un arete específico"""
        try:
            print(f"🔍 BD - Buscando en arete específico '{arete_animal}' con texto: '{texto}'")

            texto_like = f'%{texto}%'
    
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud
            WHERE areteanimal = ? AND (
                tipoanimal LIKE ? OR 
                nomvet LIKE ? OR 
                procedimiento LIKE ? OR 
                medprev LIKE ? OR 
                condicionsalud LIKE ? OR 
                observacionsalud LIKE ? OR
                fecharev LIKE ?
            )
            ORDER BY fecharev DESC
            """
        
            # Asegurarse de que la conexión esté activa
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, (
                arete_animal.strip(),  # El arete específico
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like  # La búsqueda en otros campos
            ))
        
            resultados = cursor.fetchall()
            print(f"✅ BD - {len(resultados)} registros encontrados para arete '{arete_animal}' con texto '{texto}'")
        
        # Debug detallado
            for i, resultado in enumerate(resultados):
                print(f"   Registro {i+1}: Arete={resultado[1]}, Veterinario={resultado[3]}, Procedimiento={resultado[4]}")
            
            return resultados
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_registros_salud_por_arete_y_texto: {e}")
            import traceback
            traceback.print_exc()
            return []

    # En database.py, dentro de la clase Database, agrega estos métodos:

    def obtener_todos_registros_salud(self):
        """Obtiene todos los registros de salud"""
        try:
            # Verificar si la tabla existe
            tablas = self.listar_tablas()
            if 'tsalud' not in tablas:
                print("❌ La tabla 'tsalud' no existe")
                return []
                
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            ORDER BY fecharev DESC
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ {len(resultados)} registros de salud obtenidos")
                return resultados
            return []
        except Exception as e:
            print(f"❌ Error en obtener_todos_registros_salud: {e}")
            return []

    def buscar_registros_salud(self, texto):
        """Busca registros de salud por texto en múltiples campos"""
        try:
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            WHERE areteanimal LIKE ? OR nomvet LIKE ? OR procedimiento LIKE ? 
               OR condicionsalud LIKE ? OR observacionsalud LIKE ? OR tipoanimal LIKE ?
            ORDER BY fecharev DESC
            """
            like_text = f'%{texto}%'
            cursor = self.ejecutar_consulta(query, (like_text, like_text, like_text, like_text, like_text, like_text))
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"❌ Error en buscar_registros_salud: {e}")
            return []

    def diagnostico_tabla_salud(self):
        """Diagnóstico de la tabla tsalud"""
        try:
            print("\n🔍 DIAGNÓSTICO TABLA tsalud:")
            
            # Verificar si la tabla existe
            tablas = self.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tsalud' not in tablas:
                print("❌ ERROR: La tabla 'tsalud' no existe")
                return False
                
            # Contar registros totales
            query_count = "SELECT COUNT(*) FROM tsalud"
            cursor_count = self.ejecutar_consulta(query_count)
            if cursor_count:
                total = cursor_count.fetchone()[0]
                print(f"📊 Total de registros en tsalud: {total}")
                
            # Verificar algunos registros de ejemplo
            query_ejemplo = "SELECT idsalud, areteanimal, procedimiento FROM tsalud LIMIT 3"
            cursor_ejemplo = self.ejecutar_consulta(query_ejemplo)
            if cursor_ejemplo:
                ejemplos = cursor_ejemplo.fetchall()
                print("📝 Ejemplos de registros en tsalud:")
                for ej in ejemplos:
                    print(f"   - ID: {ej[0]}, Arete: {ej[1]}, Procedimiento: {ej[2]}")
            
            return True
                    
        except Exception as e:
            print(f"❌ Error en diagnóstico tabla salud: {e}")
            return False

            # MÉTODOS PARA REPRODUCCIÓN (TREPROD)
    def obtener_todos_registros_reproduccion(self):
        """Obtiene todos los registros de la tabla treprod"""
        try:
            # Verificar si la tabla existe
            tablas = self.listar_tablas()
            if 'treprod' not in tablas:
                print("❌ La tabla 'treprod' no existe")
                return []
                
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod 
            ORDER BY fservicioactual DESC
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ {len(resultados)} registros de reproducción obtenidos")
                return resultados
            return []
        except Exception as e:
            print(f"❌ Error en obtener_todos_registros_reproduccion: {e}")
            return []

    def obtener_registros_reproduccion_por_arete(self, arete_animal: str):
        """Obtiene registros de reproducción por arete"""
        try:
            print(f"🔍 BD - Buscando registros de reproducción para arete: '{arete_animal}'")
            
            if not arete_animal or arete_animal.strip() == "":
                print("❌ BD - Arete vacío, retornando lista vacía")
                return []
            
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod 
            WHERE areteanimal = ?
            ORDER BY fservicioactual DESC
            """
            cursor = self.ejecutar_consulta(query, (arete_animal.strip(),))
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} registros de reproducción encontrados para arete: '{arete_animal}'")
                return resultados
            return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_registros_reproduccion_por_arete: {e}")
            return []

    def buscar_registros_reproduccion(self, texto):
        """Busca registros de reproducción por texto"""
        try:
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod 
            WHERE areteanimal LIKE ? OR tecnica LIKE ? OR observacion LIKE ?
            ORDER BY fservicioactual DESC
            """
            like_text = f'%{texto}%'
            cursor = self.ejecutar_consulta(query, (like_text, like_text, like_text))
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"❌ Error en buscar_registros_reproduccion: {e}")
            return []

    def obtener_registros_reproduccion_por_fecha(self, fecha_inicio, fecha_fin):
        """Obtiene registros de reproducción por rango de fechas"""
        try:
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod 
            WHERE fservicioactual BETWEEN ? AND ?
            ORDER BY fservicioactual DESC
            """
            cursor = self.ejecutar_consulta(query, (fecha_inicio, fecha_fin))
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"❌ Error en obtener_registros_reproduccion_por_fecha: {e}")
            return []

    def diagnostico_tabla_reproduccion(self):
        """Diagnóstico de la tabla treprod"""
        try:
            print("\n🔍 DIAGNÓSTICO TABLA treprod:")
            
            # Verificar si la tabla existe
            tablas = self.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'treprod' not in tablas:
                print("❌ ERROR: La tabla 'treprod' no existe")
                return False
                
            # Contar registros totales
            query_count = "SELECT COUNT(*) FROM treprod"
            cursor_count = self.ejecutar_consulta(query_count)
            if cursor_count:
                total = cursor_count.fetchone()[0]
                print(f"📊 Total de registros en treprod: {total}")
                
            # Verificar algunos registros de ejemplo
            query_ejemplo = "SELECT idreprod, areteanimal, fservicioactual FROM treprod LIMIT 3"
            cursor_ejemplo = self.ejecutar_consulta(query_ejemplo)
            if cursor_ejemplo:
                ejemplos = cursor_ejemplo.fetchall()
                print("📝 Ejemplos de registros en treprod:")
                for ej in ejemplos:
                    print(f"   - ID: {ej[0]}, Arete: {ej[1]}, Fecha Servicio: {ej[2]}")
            
            return True
                    
        except Exception as e:
            print(f"❌ Error en diagnóstico tabla reproducción: {e}")
            return False

    def buscar_registros_reproduccion_por_arete_y_texto(self, arete_animal: str, texto: str) -> List[Tuple]:
        """Busca registros de reproducción por texto pero SOLO para un arete específico"""
        try:
            print(f"🔍 BD - Buscando en arete específico '{arete_animal}' con texto: '{texto}'")

            texto_like = f'%{texto}%'
    
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod
            WHERE areteanimal = ? AND (
                cargada LIKE ? OR 
                cantpartos LIKE ? OR 
                fservicioactual LIKE ? OR 
                faproxparto LIKE ? OR 
                fnuevoservicio LIKE ? OR 
                tecnica LIKE ? OR 
                observacion LIKE ?
            )
            ORDER BY fservicioactual DESC
            """
        
            # Asegurarse de que la conexión esté activa
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, (
                arete_animal.strip(),  # El arete específico
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like  # La búsqueda en otros campos
            ))
        
            resultados = cursor.fetchall()
            print(f"✅ BD - {len(resultados)} registros encontrados para arete '{arete_animal}' con texto '{texto}'")
        
        # Debug detallado
            for i, resultado in enumerate(resultados):
                print(f"   Registro {i+1}: Arete={resultado[1]}, Cargada={resultado[2]}, Técnica={resultado[7]}")
            
            return resultados
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_registros_reproduccion_por_arete_y_texto: {e}")
            import traceback
            traceback.print_exc()
            return []

    def obtener_registros_reproduccion_por_arete_y_fecha(self, arete_animal: str, fecha_inicio: str, fecha_fin: str) -> List[Tuple]:
        """Obtiene registros de reproducción por rango de fechas SOLO para un arete específico"""
        try:
            print(f"🔍 BD - Filtrando por fecha para arete específico '{arete_animal}': {fecha_inicio} a {fecha_fin}")
        
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod 
            WHERE areteanimal = ? AND fservicioactual BETWEEN ? AND ?
            ORDER BY fservicioactual DESC
            """
        
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, (arete_animal.strip(), fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
        
            print(f"✅ BD - {len(resultados)} registros encontrados para arete '{arete_animal}' en el rango de fechas")
            return resultados
        
        except Exception as e:
            print(f"❌ BD - Error en obtener_registros_reproduccion_por_arete_y_fecha: {e}")
            return []
        
    def obtener_registros_salud_por_arete_y_fecha(self, arete_animal: str, fecha_inicio: str, fecha_fin: str) -> List[Tuple]:
        """Obtiene registros de salud por rango de fechas SOLO para un arete específico"""
        try:
            print(f"🔍 BD - Filtrando por fecha para arete específico '{arete_animal}': {fecha_inicio} a {fecha_fin}")
        
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            WHERE areteanimal = ? AND fecharev BETWEEN ? AND ?
            ORDER BY fecharev DESC
            """
        
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, (arete_animal.strip(), fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
        
            print(f"✅ BD - {len(resultados)} registros encontrados para arete '{arete_animal}' en el rango de fechas")
            return resultados
        
        except Exception as e:
            print(f"❌ BD - Error en obtener_registros_salud_por_arete_y_fecha: {e}")
            return []

    def obtener_registros_salud_por_fecha(self, fecha_inicio, fecha_fin):
        """Obtiene registros de salud por rango de fechas - MEJORADO"""
        try:
            print(f"🔍 BD - Buscando registros entre {fecha_inicio} y {fecha_fin}")
            
            fecha_inicio_bd = self.convertir_fecha_a_formato_bd(fecha_inicio)
            fecha_fin_bd = self.convertir_fecha_a_formato_bd(fecha_fin)
        
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            WHERE fecharev BETWEEN ? AND ?
            ORDER BY 
                substr(fecharev, 7, 4) || substr(fecharev, 4, 2) || substr(fecharev, 1, 2) DESC
            """
            cursor = self.ejecutar_consulta(query, (fecha_inicio_bd, fecha_fin_bd))
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} registros encontrados por fecha")
                return resultados
            return []
        except Exception as e:
            print(f"❌ Error en obtener_registros_salud_por_fecha: {e}")
            return []

    def obtener_registros_salud_por_arete_y_fecha(self, arete_animal: str, fecha_inicio: str, fecha_fin: str):
        """Obtiene registros de salud por arete y rango de fechas - MEJORADO"""
        try:
            print(f"🔍 BD - Buscando registros para arete '{arete_animal}' entre {fecha_inicio} y {fecha_fin}")

            fecha_inicio_bd = self.convertir_fecha_a_formato_bd(fecha_inicio)
            fecha_fin_bd = self.convertir_fecha_a_formato_bd(fecha_fin)
        
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud 
            WHERE areteanimal = ? AND fecharev BETWEEN ? AND ?
            ORDER BY 
                substr(fecharev, 7, 4) || substr(fecharev, 4, 2) || substr(fecharev, 1, 2) DESC
            """
        
            if not self.connection:
                self.connect()
        
            cursor = self.connection.cursor()
            cursor.execute(query, (arete_animal.strip(), fecha_inicio_bd, fecha_fin_bd))
            resultados = cursor.fetchall()
        
            print(f"✅ BD - {len(resultados)} registros encontrados para arete '{arete_animal}' en el rango de fechas")
            return resultados
        
        except Exception as e:
            print(f"❌ BD - Error en obtener_registros_salud_por_arete_y_fecha: {e}")
            return []

    def convertir_fecha_a_formato_bd(self, fecha_iso: str) -> str:
        """Convierte fecha de formato yyyy-MM-dd a dd/MM/yyyy"""
        try:
        # Parsear fecha ISO (yyyy-MM-dd)
            partes = fecha_iso.split('-')
            if len(partes) == 3:
                año, mes, dia = partes
            # Convertir a formato BD (dd/MM/yyyy)
                return f"{int(dia)}/{int(mes)}/{año}"
            return fecha_iso
        except Exception as e:
            print(f"❌ Error convirtiendo fecha {fecha_iso}: {e}")
            return fecha_iso

    def verificar_tabla_usuarios(self):
        """Verifica si la tabla de usuarios existe y la crea si no, con la estructura correcta"""
        try:
            print("🔍 Verificando tabla de usuarios...")
            
            # Verificar si la tabla existe
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name='tusuarios'"
            cursor = self.ejecutar_consulta(query)
            
            if cursor:
                tabla_existe = cursor.fetchone() is not None
                
                if not tabla_existe:
                    print("🔧 La tabla 'tusuarios' no existe, creándola...")
                    query_crear = """
                    CREATE TABLE tusuarios (
                        idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        usuario TEXT UNIQUE NOT NULL,
                        rol TEXT NOT NULL,
                        telefono TEXT,
                        pass TEXT NOT NULL
                    )
                    """
                    cursor_crear = self.ejecutar_consulta(query_crear)
                    if cursor_crear:
                        print("✅ Tabla 'tusuarios' creada exitosamente")
                        return True
                    else:
                        print("❌ Error al crear tabla 'tusuarios'")
                        return False
                else:
                    print("✅ Tabla 'tusuarios' ya existe")
                    # Verificar la estructura de la tabla
                    return self.verificar_estructura_tusuarios()
            else:
                print("❌ Error al verificar existencia de tabla")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando tabla usuarios: {e}")
            return False

    def verificar_estructura_tusuarios(self):
        """Verifica que la tabla tusuarios tenga la estructura correcta"""
        try:
            print("🔍 Verificando estructura de tabla tusuarios...")
            
            query = "PRAGMA table_info(tusuarios)"
            cursor = self.ejecutar_consulta(query)
            
            if cursor:
                columnas = cursor.fetchall()
                columnas_esperadas = ['idusuario', 'nombre', 'usuario', 'rol', 'telefono', 'pass']
                columnas_actuales = [col[1] for col in columnas]
                
                print(f"📋 Columnas actuales: {columnas_actuales}")
                print(f"📋 Columnas esperadas: {columnas_esperadas}")
                
                # Verificar que todas las columnas esperadas existan
                for col_esperada in columnas_esperadas:
                    if col_esperada not in columnas_actuales:
                        print(f"❌ Columna faltante: {col_esperada}")
                        return False
                
                print("✅ Estructura de tabla correcta")
                return True
            else:
                print("❌ Error al obtener estructura de tabla")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando estructura: {e}")
            return False

    def diagnostico_completo_usuarios(self):
        """Diagnóstico completo de la tabla de usuarios"""
        try:
            print("\n🔍 DIAGNÓSTICO COMPLETO - TABLA USUARIOS:")
            
            # Verificar todas las tablas
            tablas = self.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tusuarios' in tablas:
                print("✅ La tabla 'tusuarios' existe")
                
                # Verificar estructura
                query_estructura = "PRAGMA table_info(tusuarios)"
                cursor_estructura = self.ejecutar_consulta(query_estructura)
                if cursor_estructura:
                    columnas = cursor_estructura.fetchall()
                    print("📋 Estructura de la tabla:")
                    for col in columnas:
                        print(f"   - {col[1]} ({col[2]})")
                
                # Verificar usuarios existentes
                query_usuarios = "SELECT idusuario, usuario, nombre, rol FROM tusuarios"
                cursor_usuarios = self.ejecutar_consulta(query_usuarios)
                if cursor_usuarios:
                    usuarios = cursor_usuarios.fetchall()
                    print(f"👥 Usuarios en la tabla ({len(usuarios)}):")
                    for usuario in usuarios:
                        print(f"   - ID: {usuario[0]}, Usuario: {usuario[1]}, Nombre: {usuario[2]}, Rol: {usuario[3]}")
                        
                    if len(usuarios) == 0:
                        print("⚠️  No hay usuarios en la tabla. Debes crear al menos un usuario.")
            else:
                print("❌ La tabla 'tusuarios' NO existe")
                 
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")

            # MÉTODOS PARA USUARIOS (TEXTO PLANO)
    def obtener_usuarios(self) -> List[Tuple]:
        """Obtiene todos los usuarios de la tabla tusuarios"""
        try:
            print("🔍 BD - Ejecutando consulta para obtener usuarios...")
            query = """
            SELECT idusuario, usuario, nombre, telefono, rol
            FROM tusuarios
            ORDER BY idusuario DESC
            """
            cursor = self.ejecutar_consulta(query)
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} usuarios obtenidos")
                return resultados
            else:
                print("❌ BD - Error: cursor es None en obtener_usuarios")
                return []
        except Exception as e:
            print(f"❌ BD - Error en obtener_usuarios: {e}")
            return []

    def obtener_usuario_por_nombre(self, usuario: str) -> Optional[Tuple]:
        """Obtiene un usuario por su nombre de usuario"""
        try:
            query = "SELECT idusuario, usuario, nombre, telefono, rol FROM tusuarios WHERE usuario = ?"
            cursor = self.ejecutar_consulta(query, (usuario,))
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    print(f"✅ Usuario encontrado: {resultado[1]}")
                else:
                    print(f"ℹ️  Usuario no encontrado: {usuario}")
                return resultado
            return None
        except Exception as e:
            print(f"❌ Error en obtener_usuario_por_nombre: {e}")
            return None

    def insertar_usuario(self, usuario: str, nombre: str, telefono: str, contrasena: str, rol: str) -> bool:
        """Inserta un nuevo usuario en la tabla tusuarios (contraseña en texto plano)"""
        try:
            query = """
            INSERT INTO tusuarios (usuario, nombre, telefono, pass, rol)
            VALUES (?, ?, ?, ?, ?)
            """
            params = (usuario, nombre, telefono, contrasena, rol)
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Usuario insertado correctamente: {nombre} - {usuario}")
                return True
            else:
                print(f"❌ Error al insertar usuario: {nombre} - {usuario}")
                return False
        except Exception as e:
            print(f"❌ Error al insertar usuario: {e}")
            return False

    def buscar_usuarios_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca usuarios en todos los campos de la tabla tusuarios"""
        try:
            print(f"🔍 BD - Buscando usuarios en todos los campos: '{texto}'")
    
            texto_like = f'%{texto}%'
    
            query = """
            SELECT idusuario, usuario, nombre, telefono, rol
            FROM tusuarios
            WHERE usuario LIKE ? OR 
                nombre LIKE ? OR 
                telefono LIKE ? OR 
                rol LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like
            ))
    
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} usuarios encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_usuarios_en_todos_los_campos: {e}")
            return []

    def eliminar_usuario_por_id(self, id_usuario: int) -> bool:
        """Elimina un usuario por su ID"""
        try:
            query = "DELETE FROM tusuarios WHERE idusuario = ?"
            cursor = self.ejecutar_consulta(query, (id_usuario,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Usuario eliminado. Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_usuario_por_id: {e}")
            return False

    def verificar_credenciales(self, usuario: str, password: str) -> Optional[Tuple]:
        """Verifica las credenciales de un usuario (para login) - CONTRASEÑA EN TEXTO PLANO"""
        try:
            print(f"🔐 Verificando credenciales para usuario: {usuario}")
            
            query = "SELECT idusuario, usuario, nombre, rol, telefono FROM tusuarios WHERE usuario = ? AND pass = ?"
            cursor = self.ejecutar_consulta(query, (usuario, password))
            
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    print(f"✅ Credenciales válidas para: {usuario}")
                    return resultado
                else:
                    print(f"❌ Credenciales inválidas para: {usuario}")
                    # Debug: verificar si el usuario existe pero la contraseña es incorrecta
                    query_usuario = "SELECT usuario, pass FROM tusuarios WHERE usuario = ?"
                    cursor_usuario = self.ejecutar_consulta(query_usuario, (usuario,))
                    if cursor_usuario:
                        usuario_data = cursor_usuario.fetchone()
                        if usuario_data:
                            print(f"🔍 Usuario existe pero contraseña no coincide")
                            print(f"🔍 Contraseña en BD: '{usuario_data[1]}'")
                            print(f"🔍 Contraseña ingresada: '{password}'")
                        else:
                            print(f"🔍 Usuario no existe: {usuario}")
                return None
            return None
        except Exception as e:
            print(f"❌ Error verificando credenciales: {e}")
            return None

    def verificar_tabla_usuarios(self):
        """Verifica si la tabla de usuarios existe y la crea si no (sin usuario por defecto)"""
        try:
            print("🔍 Verificando tabla de usuarios...")
            
            # Verificar si la tabla existe
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name='tusuarios'"
            cursor = self.ejecutar_consulta(query)
            
            if cursor:
                tabla_existe = cursor.fetchone() is not None
                
                if not tabla_existe:
                    print("🔧 La tabla 'tusuarios' no existe, creándola...")
                    query_crear = """
                    CREATE TABLE tusuarios (
                        idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        usuario TEXT UNIQUE NOT NULL,
                        rol TEXT NOT NULL,
                        telefono TEXT,
                        pass TEXT NOT NULL
                    )
                    """
                    cursor_crear = self.ejecutar_consulta(query_crear)
                    if cursor_crear:
                        print("✅ Tabla 'tusuarios' creada exitosamente")
                        return True
                    else:
                        print("❌ Error al crear tabla 'tusuarios'")
                        return False
                else:
                    print("✅ Tabla 'tusuarios' ya existe")
                    # Verificar la estructura de la tabla
                    return self.verificar_estructura_tusuarios()
            else:
                print("❌ Error al verificar existencia de tabla")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando tabla usuarios: {e}")
            return False

    def obtener_usuario_por_id(self, id_usuario: int) -> Optional[Tuple]:
        """Obtiene un usuario por su ID"""
        try:
            query = "SELECT idusuario, usuario, nombre, telefono, rol FROM tusuarios WHERE idusuario = ?"
            cursor = self.ejecutar_consulta(query, (id_usuario,))
            if cursor:
                resultado = cursor.fetchone()
                if resultado:
                    print(f"✅ Usuario encontrado por ID: {resultado[1]}")
                return resultado
            return None
        except Exception as e:
            print(f"❌ Error en obtener_usuario_por_id: {e}")
            return None

    def actualizar_usuario(self, id_usuario: int, usuario: str, nombre: str, telefono: str, 
                          contrasena: str = None, rol: str = None) -> bool:
        """Actualiza un usuario en la base de datos (contraseña en texto plano)"""
        try:
            if contrasena:
                # Actualizar incluyendo contraseña
                query = """
                UPDATE tusuarios 
                SET usuario = ?, nombre = ?, telefono = ?, pass = ?, rol = ?
                WHERE idusuario = ?
                """
                params = (usuario, nombre, telefono, contrasena, rol, id_usuario)
            else:
                # Actualizar sin cambiar contraseña
                query = """
                UPDATE tusuarios 
                SET usuario = ?, nombre = ?, telefono = ?, rol = ?
                WHERE idusuario = ?
                """
                params = (usuario, nombre, telefono, rol, id_usuario)
            
            cursor = self.ejecutar_consulta(query, params)
            
            if cursor:
                print(f"✅ Usuario actualizado correctamente ID {id_usuario}: {nombre}")
                return True
            else:
                print(f"❌ Error al actualizar usuario ID {id_usuario}")
                return False
                
        except Exception as e:
            print(f"❌ Error en actualizar_usuario: {e}")
            return False

    def diagnostico_completo_usuarios(self):
        """Diagnóstico completo de la tabla de usuarios"""
        try:
            print("\n🔍 DIAGNÓSTICO COMPLETO - TABLA USUARIOS:")
            
            # Verificar todas las tablas
            tablas = self.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tusuarios' in tablas:
                print("✅ La tabla 'tusuarios' existe")
                
                # Verificar estructura
                query_estructura = "PRAGMA table_info(tusuarios)"
                cursor_estructura = self.ejecutar_consulta(query_estructura)
                if cursor_estructura:
                    columnas = cursor_estructura.fetchall()
                    print("📋 Estructura de la tabla:")
                    for col in columnas:
                        print(f"   - {col[1]} ({col[2]})")
                
                # Verificar usuarios existentes con contraseñas
                query_usuarios = "SELECT idusuario, usuario, nombre, rol, pass FROM tusuarios"
                cursor_usuarios = self.ejecutar_consulta(query_usuarios)
                if cursor_usuarios:
                    usuarios = cursor_usuarios.fetchall()
                    print(f"👥 Usuarios en la tabla ({len(usuarios)}):")
                    for usuario in usuarios:
                        print(f"   - ID: {usuario[0]}, Usuario: {usuario[1]}, Nombre: {usuario[2]}, Rol: {usuario[3]}, Pass: '{usuario[4]}'")
                        
                    if len(usuarios) == 0:
                        print("⚠️  No hay usuarios en la tabla. Debes crear al menos un usuario.")
            else:
                print("❌ La tabla 'tusuarios' NO existe")
                
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
# En tu database.py, agrega este método para actualizar la tabla de bitácora

    def actualizar_tabla_bitacora(self):
        """Actualizar la tabla de bitácora con las columnas necesarias"""
        try:
            print("🔧 Actualizando estructura de tabla bitácora...")
            
            # Verificar si la tabla existe y obtener su estructura
            query = "PRAGMA table_info(tbitacora)"
            cursor = self.ejecutar_consulta(query)
            
            if not cursor:
                print("❌ No se puede acceder a la estructura de tbitacora (cursor es None)")
                return False
            
            columnas = cursor.fetchall()
            columnas_existentes = [col[1] for col in columnas]
            
            # Agregar columna arete_afectado si no existe
            if 'arete_afectado' not in columnas_existentes:
                print("🔧 Agregando columna 'arete_afectado' a tbitacora...")
                query_alter = "ALTER TABLE tbitacora ADD COLUMN arete_afectado TEXT"
                cursor_alter = self.ejecutar_consulta(query_alter)
                if cursor_alter:
                    print("✅ Columna 'arete_afectado' agregada correctamente")
                else:
                    print("❌ Error al agregar columna 'arete_afectado'")
            
            # También verificar otras columnas que puedan faltar
            columnas_necesarias = ['fecha', 'usuario', 'modulo', 'accion', 'descripcion', 'detalles', 'arete_afectado']
            
            for columna in columnas_necesarias:
                if columna not in columnas_existentes:
                    print(f"🔧 Agregando columna '{columna}' a tbitacora...")
                    query_alter = f"ALTER TABLE tbitacora ADD COLUMN {columna} TEXT"
                    cursor_alter = self.ejecutar_consulta(query_alter)
                    if cursor_alter:
                        print(f"✅ Columna '{columna}' agregada correctamente")
                    else:
                        print(f"❌ Error al agregar columna '{columna}'")
            
            return True
        except Exception as e:
            print(f"❌ Error actualizando tabla bitácora: {e}")
            return False

    def buscar_registros_salud_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca registros de salud en todos los campos de la tabla tsalud"""
        try:
            print(f"🔍 BD - Buscando registros de salud en todos los campos: '{texto}'")

            texto_like = f'%{texto}%'
    
            query = """
            SELECT idsalud, areteanimal, tipoanimal, nomvet, procedimiento, 
                   medprev, condicionsalud, fecharev, observacionsalud, archivo
            FROM tsalud
            WHERE areteanimal LIKE ? OR 
                tipoanimal LIKE ? OR 
                nomvet LIKE ? OR 
                procedimiento LIKE ? OR 
                medprev LIKE ? OR 
                condicionsalud LIKE ? OR 
                observacionsalud LIKE ? OR
                fecharev LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like, texto_like
            ))
    
            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} registros de salud encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_registros_salud_en_todos_los_campos: {e}")
            return []
    
    def buscar_registros_reproduccion_en_todos_los_campos(self, texto: str) -> List[Tuple]:
        """Busca registros de reproducción en todos los campos de la tabla treprod"""
        try:
            print(f"🔍 BD - Buscando registros de reproducción en todos los campos: '{texto}'")
    
            texto_like = f'%{texto}%'
    
            query = """
            SELECT idreprod, areteanimal, cargada, cantpartos, fservicioactual, 
                   faproxparto, fnuevoservicio, tecnica, observacion
            FROM treprod
            WHERE areteanimal LIKE ? OR 
                cargada LIKE ? OR 
                cantpartos LIKE ? OR 
                fservicioactual LIKE ? OR 
                faproxparto LIKE ? OR 
                fnuevoservicio LIKE ? OR 
                tecnica LIKE ? OR 
                observacion LIKE ?
            """
            cursor = self.ejecutar_consulta(query, (
                texto_like, texto_like, texto_like, texto_like, 
                texto_like, texto_like, texto_like, texto_like
            ))

            if cursor:
                resultados = cursor.fetchall()
                print(f"✅ BD - {len(resultados)} registros de reproducción encontrados en búsqueda múltiple")
                return resultados
            return []
    
        except Exception as e:
            print(f"❌ BD - Error en buscar_registros_reproduccion_en_todos_los_campos: {e}")
            return []
   
   