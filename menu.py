from models import Libro, Revista, DVD, Usuario
from prestamo import GestorPrestamos
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
    gestor_prestamos = GestorPrestamos()
    while True:
        print("\n===== MENÚ BIBLIOTECA =====")
        print("1. Agregar nuevo material")
        print("2. Listar todos los materiales")
        print("3. Mostrar información de un material")
        print("4. Eliminar un material")
        print("5. Cambiar disponibilidad de un material")
        print("6. Gestionar usuarios")
        print("7. Gestionar préstamos")
        print("8. Mostrar contenido del archivo")
        print("9. Salir")
        opcion = input("\nElige una opción: ")

        if opcion == "7":
            gestion_prestamos(materiales, usuarios, gestor_prestamos)
        elif opcion == "6":
            gestion_usuarios(materiales, usuarios)

def gestion_prestamos(materiales, usuarios, gestor_prestamos):
    while True:
        print("\n===== MENÚ GESTIÓN DE PRÉSTAMOS =====")
        print("1. Prestar material")
        print("2. Devolver material")
        print("3. Listar préstamos")
        print("4. Buscar préstamo")
        print("5. Volver al menú principal")
        opcion = input("\nElige una opción: ")

        if opcion == "1":
            prestar_libro(usuarios, materiales, gestor_prestamos)
        elif opcion == "2":
            devolver_libro(usuarios, materiales, gestor_prestamos)
        elif opcion == "3":
            gestor_prestamos.listar_prestamos()
        elif opcion == "4":
            print("\n--- Buscar préstamo ---")
            print("1. Buscar por ID material")
            print("2. Buscar por ID usuario")
            opcion_busqueda = input("Elige una opción: ")
            
            if opcion_busqueda == "1":
                id_material = input("Introduce el ID del material: ")
                resultados = gestor_prestamos.buscar_prestamo(id_material=id_material)
            elif opcion_busqueda == "2":
                id_usuario = input("Introduce el ID del usuario: ")
                resultados = gestor_prestamos.buscar_prestamo(id_usuario=id_usuario)
            else:
                print("Opción inválida.")
                continue

            if resultados:
                print("\n--- RESULTADOS DE BÚSQUEDA ---")
                for i, prestamo in enumerate(resultados):
                    print(f"{i+1}.")
                    prestamo.mostrar_info()
            else:
                print("No se encontraron préstamos.")
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def gestion_usuarios(materiales, usuarios):
    while True:
        print("\n===== MENÚ GESTIÓN DE USUARIOS =====")
        print("1. Agregar nuevo usuario")
        print("2. Listar usuarios")
        print("3. Eliminar usuario")
        print("4. Volver al menú principal")
        opcion = input("\nElige una opción: ")

        if opcion == "1":
            agregar_usuario(usuarios)
        elif opcion == "2":
            mostrar_usuarios(usuarios)
        elif opcion == "3":
            eliminar_usuario(usuarios)
        elif opcion == "4":
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

def mostrar_usuarios(lista_usuarios):
    if not lista_usuarios:
        print("No hay usuarios registrados.")
        return

    print("\n--- Lista de usuarios ---")
    for i, usuario in enumerate(lista_usuarios):
        print(f"{i+1}. {usuario.get_nombre()} (ID: {usuario.get_id_usuario()})")
        # Alternativamente, podríamos usar el método mostrar_info() del usuario
        # usuario.mostrar_info()

def eliminar_usuario(usuarios):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    mostrar_usuarios(usuarios)
    try:
        index = int(input("Selecciona el número del usuario a eliminar: ")) - 1
        if 0 <= index < len(usuarios):
            usuarios.pop(index)
            print("Usuario eliminado correctamente.")
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")

def prestar_libro(usuarios, materiales, gestor_prestamos):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    if not materiales:
        print("No hay materiales registrados.")
        return

    print("\n--- Prestar Material ---")
    mostrar_usuarios(usuarios)
    try:
        usuario_index = int(input("Selecciona el número del usuario: ")) - 1
        if not (0 <= usuario_index < len(usuarios)):
            print("Índice de usuario inválido.")
            return

        listar_materiales(materiales)
        material_index = int(input("Selecciona el número del material: ")) - 1
        if not (0 <= material_index < len(materiales)):
            print("Índice de material inválido.")
            return

        material = materiales[material_index]
        if not material.get_disponible():
            print("Este material no está disponible para préstamo.")
            return

        # Crear préstamo y actualizar disponibilidad
        prestamo = gestor_prestamos.agregar_prestamo(material.get_codigo_inventario(), usuarios[usuario_index].get_id_usuario())
        material.set_disponible(False)
        usuarios[usuario_index].prestar_libro(material)
        print("Material prestado correctamente.")
    except ValueError:
        print("Entrada inválida.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

def devolver_libro(usuarios, materiales, gestor_prestamos):
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    if not materiales:
        print("No hay materiales registrados.")
        return

    print("\n--- Devolver Material ---")
    listar_materiales(materiales)
    try:
        material_index = int(input("Selecciona el número del material: ")) - 1
        if not (0 <= material_index < len(materiales)):
            print("Índice de material inválido.")
            return

        material = materiales[material_index]
        if not gestor_prestamos.devolver_prestamo(material.get_codigo_inventario()):
            print("Este material no está prestado.")
            return

        material.set_disponible(True)
        print("Material devuelto correctamente.")
    except ValueError:
        print("Entrada inválida.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

    # Actualizar la lista de libros prestados del usuario
    try:
        # Buscar el usuario que tiene el material prestado
        for usuario in usuarios:
            if material in usuario.__libros_prestados:
                usuario.__libros_prestados.remove(material)
                break
    except Exception as e:
        print(f"Error al actualizar libros prestados: {str(e)}")
