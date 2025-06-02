from database import Database
from datetime import datetime
from models import MaterialBiblioteca, Usuario
from prestamo import Prestamo, GestorPrestamos

def cargar_materiales():
    db = Database()
    return db.obtener_materiales()

def guardar_materiales(materiales):
    db = Database()
    for material in materiales:
        db.guardar_material(material)
    return True

def cargar_usuarios():
    db = Database()
    return db.obtener_usuarios()

def guardar_usuarios(usuarios):
    db = Database()
    for usuario in usuarios:
        db.guardar_usuario(usuario)
    return True



def cargar_prestamos():
    db = Database()
    prestamos_data = db.obtener_prestamos()
    prestamos = []
    
    for prestamo_data in prestamos_data:
        try:
            # Convertir las fechas de string a datetime
            fecha_prestamo = datetime.fromisoformat(prestamo_data['fecha_prestamo'])
            fecha_devolucion = datetime.fromisoformat(prestamo_data['fecha_devolucion']) if prestamo_data['fecha_devolucion'] else None
            
            # Crear objeto Prestamo
            prestamo = Prestamo(
                codigo_material=prestamo_data['codigo_material'],
                id_usuario=prestamo_data['id_usuario'],
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion=fecha_devolucion
            )
            prestamos.append(prestamo)
        except Exception as e:
            print(f"Error al cargar préstamo: {str(e)}")
            continue
    
    return prestamos

def guardar_prestamos(prestamos):
    db = Database()
    for prestamo in prestamos:
        db.guardar_prestamo(prestamo)
    return True

def mostrar_contenido_archivo():
    db = Database()
    print("\n=== Contenido de la base de datos ===")
    
    # Mostrar usuarios
    usuarios = db.obtener_usuarios()
    print("\n=== Usuarios ===")
    print(f"Número de usuarios: {len(usuarios)}")
    for i, usuario in enumerate(usuarios):
        print(f"\nUsuario {i+1}:")
        usuario.mostrar_info()

    # Mostrar contenido de usuarios.pkl
    try:
        with open("usuarios.pkl", "rb") as f:
            datos = pickle.load(f)
            print("\n=== Contenido del archivo usuarios.pkl ===")
            print(f"Número de usuarios: {len(datos)}")
            for i, usuario in enumerate(datos):
                print(f"\nUsuario {i+1}:")
                if isinstance(usuario, Usuario):
                    usuario.mostrar_info()
    except FileNotFoundError:
        print("El archivo usuarios.pkl no existe o está vacío.")
    except Exception as e:
        print(f"Error al leer usuarios.pkl: {str(e)}")

    # Mostrar contenido de prestamos.pkl
    try:
        with open("prestamos.pkl", "rb") as f:
            datos = pickle.load(f)
            print("\n=== Contenido del archivo prestamos.pkl ===")
            print(f"Número de préstamos: {len(datos)}")
            for i, prestamo in enumerate(datos):
                print(f"\nPrestamo {i+1}:")
                if isinstance(prestamo, Prestamo):
                    prestamo.mostrar_info()
    except FileNotFoundError:
        print("El archivo prestamos.pkl no existe o está vacío.")
    except Exception as e:
        print(f"Error al leer prestamos.pkl: {str(e)}")