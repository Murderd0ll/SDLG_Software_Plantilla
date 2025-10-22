import sqlite3
import os
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name="bdd/SDLGAPP.db"):
        self.db_name = db_name
        self.connection = None
        
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
        query = """
        SELECT idbece, aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece, fotobece
        FROM tbecerros
        """
        cursor = self.ejecutar_consulta(query)
        if cursor:
            return cursor.fetchall()
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

    def eliminar_becerro(self, idbece: int) -> bool:
        """Elimina un registro de la tabla tbecerros"""
        query = "DELETE FROM tbecerros WHERE idbece=?"
        cursor = self.ejecutar_consulta(query, (idbece,))
        return cursor is not None

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

    def obtener_foto_becerro(self, idbece: int) -> Optional[bytes]:
        """Obtiene la foto de un becerro por su ID"""
        query = "SELECT fotobece FROM tbecerros WHERE idbece = ?"
        cursor = self.ejecutar_consulta(query, (idbece,))
        if cursor:
            resultado = cursor.fetchone()
            return resultado[0] if resultado and resultado[0] else None
        return None