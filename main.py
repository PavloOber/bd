from utils import cargar_materiales, cargar_usuarios, cargar_prestamos
from menu import Menu
from database import Database

if __name__ == "__main__":
    try:
        # Inicializar la base de datos
        db = Database()
        print("\nInicializando la base de datos...")
        
        # Intentar inicializar la base de datos
        if not db.init_db():
            print("Error al inicializar la base de datos.")
            print("Verificando y creando tablas...")
            if not db._verificar_tablas():
                print("Error al verificar/crear tablas")
                exit(1)
            print("Tablas verificadas/creadas exitosamente")
            
            # Intentar insertar datos iniciales nuevamente
            if not db._insertar_datos_iniciales():
                print("Error al insertar datos iniciales")
                exit(1)
            print("Datos iniciales insertados exitosamente")

        print("\nCargando datos...")
        try:
            materiales = cargar_materiales()
            usuarios = cargar_usuarios()
            prestamos = cargar_prestamos()
            print("Datos cargados exitosamente")
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")
            exit(1)

        print("\nIniciando aplicación...")
        try:
            Menu(materiales, usuarios, prestamos, db)
        except Exception as e:
            print(f"Error al iniciar la aplicación: {str(e)}")
            exit(1)
        print("Verifica que las tablas existen en Supabase y que la API key es correcta.")

    except Exception as e:
        print(f"\nError al iniciar la aplicación: {str(e)}")
        exit(1)
