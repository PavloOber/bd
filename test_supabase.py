from database import Database

def test_connection():
    # Crear una instancia de la base de datos
    db = Database()
    
    # Intentar obtener usuarios (debería devolver una lista vacía ya que no hay datos)
    print("\n=== Probando conexión con Supabase ===")
    print(f"URL: {db.client.supabase_url}")
    
    try:
        usuarios = db.obtener_usuarios()
        print(f"\nNúmero de usuarios: {len(usuarios)}")
        
        # Intentar obtener materiales
        materiales = db.obtener_materiales()
        print(f"Número de materiales: {len(materiales)}")
        
        # Intentar obtener préstamos
        prestamos = db.obtener_prestamos()
        print(f"Número de préstamos: {len(prestamos)}")
        
        print("\n¡Conexión exitosa!")
        
    except Exception as e:
        print(f"Error al conectar: {str(e)}")

if __name__ == "__main__":
    test_connection()
