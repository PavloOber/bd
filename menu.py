from models import Libro, Revista, DVD, Usuario
from utils import guardar_materiales, guardar_usuarios


def agregar_material(materiales):
    print("\n--- Tipo de material ---")
    tipo = input("¿Qué deseas agregar? (libro / revista / dvd): ").strip().lower()

    titulo = input("Título: ")
    autor = input("Autor/Director: ")
    codigo = input("Código de inventario: ")
    ubicacion = "Biblioteca principal"

    if tipo == "libro":
        paginas = int(input("Número de páginas: "))
        materiales.append(Libro(titulo, autor, codigo, paginas, ubicacion))
        print("Libro agregado correctamente.")
    elif tipo == "revista":
        edicion = input("Número de edición: ")
        fecha = input("Fecha de publicación (dd/mm/aaaa): ")
        materiales.append(Revista(titulo, autor, codigo, edicion, fecha, ubicacion))
        print("Revista agregada correctamente.")
    elif tipo == "dvd":
        duracion = int(input("Duración (en minutos): "))
        formato = input("Formato (ej. Blu-ray, DVD): ")
        materiales.append(DVD(titulo, autor, codigo, duracion, formato, ubicacion))
        print("DVD agregado correctamente.")
    else:
        print("Tipo de material no reconocido.")

def eliminar_material(materiales):
    if not materiales:
        print("No hay materiales registrados.")
        return

    listar_materiales(materiales)
    try:
        index = int(input("Selecciona el número del material a eliminar: ")) - 1
        if 0 <= index < len(materiales):
            materiales.pop(index)
            print("Material eliminado correctamente.")
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def cambiar_disponibilidad(materiales):
    if not materiales:
        print("No hay materiales registrados.")
        return

    listar_materiales(materiales)
    try:
        index = int(input("Selecciona el número del material para cambiar disponibilidad: ")) - 1
        if 0 <= index < len(materiales):
            material = materiales[index]
            actual = material.get_disponible()
            material.set_disponible(not actual)
            print(f"Disponibilidad cambiada a: {'Sí' if not actual else 'No'}")
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def listar_materiales(materiales):
    if not materiales:
        print("No hay materiales registrados.")
        return

    print("\n--- Lista de materiales ---")
    for i, material in enumerate(materiales):
        print(f"{i+1}. {material.get_titulo()} ({material.get_codigo_inventario()})")

def mostrar_info_material(materiales):
    if not materiales:
        print("No hay materiales registrados.")
        return

    listar_materiales(materiales)
    try:
        index = int(input("Selecciona el número del material para ver información: ")) - 1
        if 0 <= index < len(materiales):
            materiales[index].mostrar_info()
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def Menu(materiales, usuarios):
    while True:
        print("\n===== MENÚ BIBLIOTECA =====")
        print("1. Agregar nuevo material")
        print("2. Listar todos los materiales")
        print("3. Mostrar información de un material")
        print("4. Eliminar un material")
        print("5. Cambiar disponibilidad de un material")
        print("6. Gestionar usuarios")
        print("7. Mostrar contenido del archivo")
        print("8. Salir")
        opcion = input("\nElige una opción: ")

        if opcion == "6":
            gestion_usuarios(materiales, usuarios)

def gestion_usuarios(materiales, usuarios):
    while True:
        print("\n===== MENÚ GESTIÓN DE USUARIOS =====")
        print("1. Agregar nuevo usuario")
        print("2. Listar usuarios")
        print("3. Eliminar usuario")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Volver al menú principal")
        opcion = input("\nElige una opción: ")

        if opcion == "1":
            agregar_usuario(usuarios)
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            eliminar_usuario(usuarios)
        elif opcion == "4":
            prestar_libro(usuarios, materiales)
        elif opcion == "5":
            devolver_libro(usuarios, materiales)
        elif opcion == "6":
            guardar_usuarios(usuarios)
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

        if opcion != "2":  # Solo guardar cambios si no es listar usuarios
            guardar_usuarios(usuarios)

def agregar_usuario(usuarios):
    print("\n--- Nuevo Usuario ---")
    id_usuario = input("ID del usuario: ")
    nombre = input("Nombre completo: ")
    correo = input("Correo electrónico: ")
    tipo = input("Tipo de usuario (cliente/estudiante/profesor): ").lower()
    usuarios.append(Usuario(id_usuario, nombre, correo, tipo))
    print("Usuario agregado correctamente.")

def eliminar_usuario(usuarios):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    mostrar_usuarios()
    try:
        index = int(input("Selecciona el número del usuario a eliminar: ")) - 1
        if 0 <= index < len(usuarios):
            usuarios.pop(index)
            print("Usuario eliminado correctamente.")
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def prestar_libro(usuarios, materiales):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    if not materiales:
        print("No hay materiales disponibles.")
        return

    mostrar_usuarios()
    try:
        usuario_index = int(input("Selecciona el número del usuario: ")) - 1
        if not (0 <= usuario_index < len(usuarios)):
            print("Índice de usuario inválido.")
            return

        listar_materiales(materiales)
        material_index = int(input("Selecciona el número del material a prestar: ")) - 1
        if not (0 <= material_index < len(materiales)):
            print("Índice de material inválido.")
            return

        usuario = usuarios[usuario_index]
        material = materiales[material_index]
        
        if usuario.prestar_libro(material):
            print("Libro prestado correctamente.")
        else:
            print("El libro no está disponible.")
    except ValueError:
        print("Entrada inválida.")

def devolver_libro(usuarios, materiales):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    if not materiales:
        print("No hay materiales disponibles.")
        return

    mostrar_usuarios()
    try:
        usuario_index = int(input("Selecciona el número del usuario: ")) - 1
        if not (0 <= usuario_index < len(usuarios)):
            print("Índice de usuario inválido.")
            return

        listar_materiales(materiales)
        material_index = int(input("Selecciona el número del material a devolver: ")) - 1
        if not (0 <= material_index < len(materiales)):
            print("Índice de material inválido.")
            return

        usuario = usuarios[usuario_index]
        material = materiales[material_index]
        
        if usuario.devolver_libro(material):
            print("Libro devuelto correctamente.")
        else:
            print("El libro no está prestado a este usuario.")
    except ValueError:
        print("Entrada inválida.")
