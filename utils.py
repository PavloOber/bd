import pickle
from models import MaterialBiblioteca, Usuario
from prestamo import Prestamo, GestorPrestamos

def cargar_materiales():
    try:
        with open("materiales.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return []

def guardar_materiales(materiales):
    try:
        if not isinstance(materiales, list):
            print("Error: Los materiales deben ser una lista")
            return False
            
        with open("materiales.pkl", "wb") as f:
            pickle.dump(materiales, f)
        print("Materiales guardados en 'materiales.pkl'.")
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {str(e)}")
        return False

def cargar_usuarios():
    try:
        with open("usuarios.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar usuarios: {str(e)}")
        return []

def guardar_usuarios(usuarios):
    try:
        if not isinstance(usuarios, list):
            print("Error: Los usuarios deben ser una lista")
            return False
            
        with open("usuarios.pkl", "wb") as f:
            pickle.dump(usuarios, f)
        print("Usuarios guardados en 'usuarios.pkl'.")
        return True
    except Exception as e:
        print(f"Error al guardar usuarios: {str(e)}")
        return False

def mostrar_usuarios():
    try:
        usuarios = cargar_usuarios()
        print("\n=== Lista de Usuarios ===")
        print(f"Número total de usuarios: {len(usuarios)}")
        for i, usuario in enumerate(usuarios):
            print(f"\nUsuario {i+1}:")
            usuario.mostrar_info()
    except Exception as e:
        print(f"Error al mostrar usuarios: {str(e)}")

def cargar_prestamos():
    try:
        with open("prestamos.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar préstamos: {str(e)}")
        return []

def guardar_prestamos(prestamos):
    try:
        if not isinstance(prestamos, list):
            print("Error: Los préstamos deben ser una lista")
            return False
            
        with open("prestamos.pkl", "wb") as f:
            pickle.dump(prestamos, f)
        print("Préstamos guardados en 'prestamos.pkl'.")
        return True
    except Exception as e:
        print(f"Error al guardar préstamos: {str(e)}")
        return False

def mostrar_contenido_archivo():
    print("\n=== Contenido de los archivos ===")
    
    # Mostrar contenido de materiales.pkl
    try:
        with open("materiales.pkl", "rb") as f:
            datos = pickle.load(f)
            print("\n=== Contenido del archivo materiales.pkl ===")
            print(f"Número de elementos: {len(datos)}")
            for i, material in enumerate(datos):
                print(f"\nMaterial {i+1}:")
                if isinstance(material, MaterialBiblioteca):
                    print(f"Tipo: {material.__class__.__name__}")
                    material.mostrar_info()
    except FileNotFoundError:
        print("El archivo materiales.pkl no existe o está vacío.")
    except Exception as e:
        print(f"Error al leer materiales.pkl: {str(e)}")

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