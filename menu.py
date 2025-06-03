from models import Libro, Revista, DVD, Usuario
from prestamo import GestorPrestamos
from utils import cargar_materiales, cargar_usuarios, guardar_prestamos, guardar_usuarios
from database import Database


def agregar_material(materiales, db):
    """Agrega un nuevo material a la biblioteca"""
    print("\n--- Tipo de material ---")
    
    # Validar tipo de material
    while True:
        tipo = input("¿Qué deseas agregar? (libro / revista / dvd): ").strip().lower()
        if tipo in ['libro', 'revista', 'dvd']:
            break
        print("Por favor, ingresa un tipo válido (libro, revista o dvd)")

    # Validar datos comunes
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            break
        print("El título no puede estar vacío")

    while True:
        autor = input("Autor/Director: ").strip()
        if autor:
            break
        print("El autor no puede estar vacío")

    while True:
        codigo = input("Código de inventario: ").strip()
        if codigo and not any(m.get_codigo_inventario() == codigo for m in materiales):
            break
        print("El código de inventario ya existe o está vacío")

    ubicacion = "Biblioteca principal"

    try:
        # Crear el material según su tipo
        if tipo == "libro":
            while True:
                try:
                    paginas = int(input("Número de páginas: "))
                    if paginas > 0:
                        break
                    print("El número de páginas debe ser mayor que 0")
                except ValueError:
                    print("Por favor, ingresa un número válido")
            
            libro = Libro(titulo, autor, codigo, ubicacion, True, paginas)
            materiales.append(libro)
            if db.guardar_material(libro):
                print("Libro agregado correctamente.")
            else:
                print("Error al guardar el libro en la base de datos")
                materiales.pop()

        elif tipo == "revista":
            edicion = input("Número de edición: ").strip()
            fecha = input("Fecha de publicación (dd/mm/aaaa): ").strip()
            
            revista = Revista(titulo, autor, codigo, ubicacion, edicion, fecha)
            materiales.append(revista)
            if db.guardar_material(revista):
                print("Revista agregada correctamente.")
            else:
                print("Error al guardar la revista en la base de datos")
                materiales.pop()

        elif tipo == "dvd":
            while True:
                try:
                    duracion = int(input("Duración (en minutos): "))
                    if duracion > 0:
                        break
                    print("La duración debe ser mayor que 0")
                except ValueError:
                    print("Por favor, ingresa un número válido")
            
            formato = input("Formato (ej. Blu-ray, DVD): ").strip()
            
            dvd = DVD(titulo, autor, codigo, ubicacion, duracion, formato)
            materiales.append(dvd)
            if db.guardar_material(dvd):
                print("DVD agregado correctamente.")
            else:
                print("Error al guardar el DVD en la base de datos")
                materiales.pop()

    except Exception as e:
        print(f"Error al agregar el material: {str(e)}")
        if len(materiales) > 0:
            materiales.pop()

def eliminar_material(materiales):
    if not materiales:
        print("No hay materiales registrados.")
        return

    listar_materiales(materiales)
    try:
        index = int(input("Selecciona el número del material a eliminar: ")) - 1
        if 0 <= index < len(materiales):
            material = materiales.pop(index)
            db = Database()
            db.eliminar_material(material.get_codigo_inventario())
            print("Material eliminado correctamente.")
        else:
            print("Índice fuera de rango.")
    except ValueError:
        print("Entrada inválida.")
    except Exception as e:
        print(f"Error al eliminar el material: {str(e)}")
        # Restaurar el material en caso de error
        materiales.insert(index, material)

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

def Menu(materiales, usuarios, prestamos, db):
    """Muestra el menú principal y maneja las opciones del usuario"""
    gestor_prestamos = GestorPrestamos()
    gestor_prestamos.prestamos = prestamos
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

        if opcion == "1":
            agregar_material(materiales)
        elif opcion == "2":
            if not materiales:
                print("No hay materiales registrados.")
            else:
                listar_materiales(materiales)
        elif opcion == "3":
            mostrar_info_material(materiales)
        elif opcion == "4":
            eliminar_material(materiales)
        elif opcion == "5":
            cambiar_disponibilidad(materiales)
        elif opcion == "6":
            gestion_usuarios(materiales, usuarios)
        elif opcion == "7":
            gestion_prestamos(materiales, usuarios, gestor_prestamos)
        elif opcion == "8":
            mostrar_contenido_archivo()
        elif opcion == "9":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intenta de nuevo.")

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
                id_inventario = input("Introduce el ID del material: ")
                resultados = gestor_prestamos.buscar_prestamo(id_inventario=id_inventario)
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
            try:
                nuevo_usuario = agregar_usuario(usuarios)
                if nuevo_usuario:
                    guardar_usuarios(usuarios)
                    print(f"Usuario agregado exitosamente!\nID: {nuevo_usuario.get_id_usuario()}\nNombre: {nuevo_usuario.get_nombre()}\nCorreo: {nuevo_usuario.get_correo()}\nTipo: {nuevo_usuario.get_tipo_usuario()}")
                    mostrar_usuarios(usuarios)
            except Exception as e:
                print(f"Error al agregar el usuario: {str(e)}")
        elif opcion == "2":
            mostrar_usuarios(usuarios)
        elif opcion == "3":
            try:
                eliminar_usuario(usuarios)
                guardar_usuarios(usuarios)
                print("Usuario eliminado exitosamente.")
                mostrar_usuarios(usuarios)
            except Exception as e:
                print(f"Error al eliminar el usuario: {str(e)}")
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def agregar_usuario(usuarios):
    print("\n--- Nuevo Usuario ---")
    while True:
        id_usuario = input("ID del usuario: ")
        # Verificar si el ID ya existe
        if any(u.get_id_usuario() == id_usuario for u in usuarios):
            print(f"Error: El ID {id_usuario} ya está en uso. Por favor, elige otro ID.")
            continue
        break
    
    nombre = input("Nombre completo: ")
    correo = input("Correo electrónico: ")
    tipo = input("Tipo de usuario (cliente/estudiante/profesor): ").lower()
    
    try:
        nuevo_usuario = Usuario(id_usuario, nombre, correo, tipo)
        usuarios.append(nuevo_usuario)
        print("Usuario agregado correctamente.")
        return nuevo_usuario
    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        return None

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
        try:
            prestamo = gestor_prestamos.agregar_prestamo(material.get_codigo_inventario(), usuarios[usuario_index].get_id_usuario())
            if prestamo:
                material.set_disponible(False)
                usuarios[usuario_index].prestar_libro(material)
                print("\nPréstamo realizado exitosamente!")
                print(f"ID Material: {material.get_codigo_inventario()}")
                print(f"ID Usuario: {usuarios[usuario_index].get_id_usuario()}")
                print(f"Fecha de préstamo: {prestamo.fecha_prestamo}")
                # Guardar el préstamo inmediatamente
                guardar_prestamos([prestamo])
            else:
                print("Error al crear el préstamo.")
        except Exception as e:
            print(f"Error al procesar el préstamo: {str(e)}")
            material.set_disponible(True)  # Restaurar disponibilidad si hay error
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
            if material in usuario.get_libros_prestados():
                usuario.devolver_libro(material)
                break
    except Exception as e:
        print(f"Error al actualizar libros prestados: {str(e)}")
