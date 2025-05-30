from utils import cargar_materiales, cargar_usuarios, cargar_prestamos
from menu import Menu
from database import Database

if __name__ == "__main__":
    try:
        # Inicializar la base de datos
        db = Database()
        print("\nInicializando la base de datos...")
        db.init_db()
        
        # Cargar datos
        print("\nCargando datos...")
        materiales = cargar_materiales()
        usuarios = cargar_usuarios()
        prestamos = cargar_prestamos()
        
        # Ejecutar menú principal
        print("\nIniciando aplicación...")
        Menu(materiales, usuarios, prestamos)
        
    except Exception as e:
        print(f"\nError al iniciar la aplicación: {str(e)}")
        print("Verifica que las tablas existen en Supabase y que la API key es correcta.")
