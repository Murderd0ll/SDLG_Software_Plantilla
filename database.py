# database.py
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
            self._crear_tablas_si_no_existen()
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
                self.connect()
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
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece
        FROM tbecerros
        """
        cursor = self.ejecutar_consulta(query)
        if cursor:
            return cursor.fetchall()
        return []
        
    def insertar_becerro(self, arete: str, nombre: str, peso: float, sexo: str, raza: str, 
                       nacimiento: str, corral: str, estatus: str, 
                       aretemadre: str, aretepadre: str, observacion: str) -> bool:
        """Inserta un nuevo registro en la tabla tbecerros"""
        query = """
        INSERT INTO tbecerros (aretebece, nombrebece, pesobece, sexobece, razabece, nacimientobece, 
                           corralbece, estatusbece, aretemadre, aretepadre, observacionbece)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (arete, nombre, peso, sexo, raza, nacimiento, corral, estatus, 
                 aretemadre, aretepadre, observacion)
        cursor = self.ejecutar_consulta(query, params)
        return cursor is not None

    def actualizar_becerro(self, idbece: int, arete: str, nombre: str, peso: float, sexo: str, 
                         raza: str, nacimiento: str, corral: str, estatus: str, 
                         aretemadre: str, aretepadre: str, observacion: str) -> bool:
        """Actualiza un registro existente en la tabla tbecerros"""
        query = """
        UPDATE tbecerros 
        SET aretebece=?, nombrebece=?, pesobece=?, sexobece=?, razabece=?, nacimientobece=?, 
            corralbece=?, estatusbece=?, aretemadre=?, aretepadre=?, observacionbece=?
        WHERE idbece=?
        """
        params = (arete, nombre, peso, sexo, raza, nacimiento, corral, estatus, 
                 aretemadre, aretepadre, observacion, idbece)
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
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece
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
               corralbece, estatusbece, aretemadre, aretepadre, observacionbece
        FROM tbecerros
        WHERE idbece = ?
        """
        cursor = self.ejecutar_consulta(query, (idbece,))
        if cursor:
            return cursor.fetchone()
        return None