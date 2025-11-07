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
                       aretemadre: str, aretepadre: str, observacion: str, foto: bytes = None) -> bool:
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
                , observacionbece = ?, fotobece = ?
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
               corralbece, estatusbece, aretemadre, observacionbece, fotobece
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
               corralbece, estatusbece, aretemadre, observacionbece, fotobece
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

    def buscar_animales_por_nombre(self, nombre: str) -> List[Tuple]:
        """Busca animales por nombre"""
        query = """
        SELECT idgdo, aretegdo, nombregdo, corralgdo, sexogdo, razagdo, prodgdo, 
               alimentogdo, nacimientogdo, estatusgdo, observaciongdo, fotogdo
        FROM tganado
        WHERE nombregdo LIKE ?
        """
        cursor = self.ejecutar_consulta(query, (f'%{nombre}%',))
        if cursor:
            return cursor.fetchall()
        return []

    def eliminar_animal_por_arete(self, arete: str) -> bool:
        """Elimina un registro de la tabla tganado por arete"""
        try:
            print(f"🗑️ BD - Intentando eliminar animal por arete: {arete}")
            query = "DELETE FROM tganado WHERE aretegdo = ?"
            cursor = self.ejecutar_consulta(query, (arete,))
            
            if cursor:
                filas_afectadas = cursor.rowcount
                print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
                return filas_afectadas > 0
            else:
                print("🗑️ BD - Error: cursor es None")
                return False
        except Exception as e:
            print(f"🗑️ BD - Error en eliminar_animal_por_arete: {e}")
            return False

    # MÉTODOS PARA SALUD
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

    def buscar_corrales_por_nombre(self, nombre: str) -> List[Tuple]:
        """Busca corrales por nombre"""
        query = """
        SELECT identcorral, nomcorral, ubicorral, capmax, capactual, 
               fechamant, condicion, observacioncorral
        FROM tcorral
        WHERE nomcorral LIKE ?
        """
        cursor = self.ejecutar_consulta(query, (f'%{nombre}%',))
        if cursor:
            return cursor.fetchall()
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

    def buscar_propietarios_por_nombre(self, nombre: str) -> List[Tuple]:
        """Busca propietarios por nombre"""
        query = """
        SELECT idprop, nombreprop, telprop, correoprop, dirprop, psgprop, uppprop, rfcprop, observacionprop, fotoprop
        FROM tpropietarios
        WHERE nombreprop LIKE ?
        """
        cursor = self.ejecutar_consulta(query, (f'%{nombre}%',))
        if cursor:
            return cursor.fetchall()
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
        
def obtener_usuarios(self):
    """Obtiene todos los usuarios de la base de datos"""
    try:
        query = """
        SELECT id_usuario, usuario, nombre_completo, telefono, rol, fecha_creacion
        FROM tusuarios 
        ORDER BY nombre_completo
        """
        cursor = self.ejecutar_consulta(query)
        if cursor:
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"❌ Error obteniendo usuarios: {e}")
        # Retornar datos de ejemplo para desarrollo
        return [
            (1, 'admin', 'Administrador Principal', '555-1234', 'Administrador', '2024-01-01'),
            (2, 'usuario1', 'Usuario Normal', '555-5678', 'Usuario', '2024-01-02'),
            (3, 'veterinario', 'Dr. Veterinario', '555-9012', 'Veterinario', '2024-01-03')
        ]

def buscar_usuarios_por_nombre(self, nombre: str):
    """Busca usuarios por nombre"""
    try:
        query = """
        SELECT id_usuario, usuario, nombre_completo, telefono, rol, fecha_creacion
        FROM tusuarios 
        WHERE nombre_completo LIKE ? OR usuario LIKE ?
        ORDER BY nombre_completo
        """
        cursor = self.ejecutar_consulta(query, (f'%{nombre}%', f'%{nombre}%'))
        if cursor:
            return cursor.fetchall()
        return []
    except Exception as e:
        print(f"❌ Error buscando usuarios: {e}")
        return []

def eliminar_usuario_por_id(self, id_usuario: str) -> bool:
    """Elimina un usuario por su ID"""
    try:
        print(f"🗑️ BD - Intentando eliminar usuario por ID: {id_usuario}")
        query = "DELETE FROM tusuarios WHERE id_usuario = ?"
        cursor = self.ejecutar_consulta(query, (id_usuario,))
        
        if cursor:
            filas_afectadas = cursor.rowcount
            print(f"🗑️ BD - Filas afectadas: {filas_afectadas}")
            return filas_afectadas > 0
        else:
            print("🗑️ BD - Error: cursor es None")
            return False
    except Exception as e:
        print(f"🗑️ BD - Error en eliminar_usuario_por_id: {e}")
        return False