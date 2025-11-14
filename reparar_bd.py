# reparar_bitacora.py
from database import Database
from datetime import datetime

def reparar_bitacora_completa():
    """Reparar completamente la tabla de bitácora"""
    print("🔧 INICIANDO REPARACIÓN COMPLETA DE BITÁCORA...")
    
    db = Database()
    
    if db.connect():
        try:
            # 1. Verificar si existe la tabla
            tablas = db.listar_tablas()
            print(f"📋 Tablas en la BD: {tablas}")
            
            if 'tbitacora' not in tablas:
                print("❌ La tabla tbitacora no existe, creándola...")
                query_crear = """
                CREATE TABLE tbitacora (
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
                db.ejecutar_consulta(query_crear)
                print("✅ Tabla tbitacora creada")
            
            # 2. Verificar estructura
            query_estructura = "PRAGMA table_info(tbitacora)"
            cursor = db.ejecutar_consulta(query_estructura)
            
            if cursor:
                columnas = cursor.fetchall()
                print("🔍 Estructura actual de tbitacora:")
                for col in columnas:
                    print(f"   - {col[1]} ({col[2]})")
                
                # 3. Agregar columnas faltantes
                columnas_requeridas = ['usuario', 'modulo', 'accion', 'descripcion', 'detalles', 'arete_afectado']
                columnas_actuales = [col[1] for col in columnas]
                
                for columna in columnas_requeridas:
                    if columna not in columnas_actuales:
                        print(f"🔧 Agregando columna: {columna}")
                        query_alter = f"ALTER TABLE tbitacora ADD COLUMN {columna} TEXT"
                        db.ejecutar_consulta(query_alter)
                
                # 4. Verificar registros existentes
                query_count = "SELECT COUNT(*) FROM tbitacora"
                cursor_count = db.ejecutar_consulta(query_count)
                if cursor_count:
                    total = cursor_count.fetchone()[0]
                    print(f"📊 Total de registros en bitácora: {total}")
                    
                    if total > 0:
                        # Mostrar algunos registros de ejemplo
                        query_ejemplo = "SELECT * FROM tbitacora ORDER BY fecha DESC LIMIT 5"
                        cursor_ejemplo = db.ejecutar_consulta(query_ejemplo)
                        if cursor_ejemplo:
                            registros = cursor_ejemplo.fetchall()
                            print("📝 Últimos 5 registros de bitácora:")
                            for i, reg in enumerate(registros):
                                print(f"   {i+1}. Fecha: {reg[1]}, Usuario: {reg[2]}, Acción: {reg[4]}")
            
            print("✅ Reparación de bitácora completada")
            
        except Exception as e:
            print(f"❌ Error en reparación: {e}")
        finally:
            db.disconnect()
    else:
        print("❌ No se pudo conectar a la base de datos")

if __name__ == "__main__":
    reparar_bitacora_completa()