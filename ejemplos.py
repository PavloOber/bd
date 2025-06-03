from models import Libro, Revista, DVD, MaterialBiblioteca, Usuario
from database import Database
from datetime import datetime, timedelta

def guardar_material(material: MaterialBiblioteca):
    try:
        material.validar_datos()
        data = {
            'titulo': material.get_titulo(),
            'autor': material.get_autor(),
            'codigo_inventario': material.get_codigo_inventario(),
            'ubicacion': material.get_ubicacion(),
            'disponible': material.get_disponible()
        }
        
        # Agregar campos específicos según el tipo
        if isinstance(material, Libro):
            data['tipo'] = 'libro'
            data['num_paginas'] = material.get_num_paginas()
        elif isinstance(material, Revista):
            data['tipo'] = 'revista'
            data['numero_edicion'] = material.get_numero_edicion()
            data['fecha_publicacion'] = material.get_fecha_publicacion()
        elif isinstance(material, DVD):
            data['tipo'] = 'dvd'
            data['duracion'] = material.get_duracion()
            data['formato'] = material.get_formato()
        
        response = client.table('materiales').insert(data).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Error al guardar material: {str(e)}")
        return False

def crear_ejemplos():
    # Crear instancia de Database
    db = Database()
    
    # Primero eliminar datos existentes
    print("\nEliminando datos existentes...")
    db.eliminar_datos()
    
    # Ejemplos de usuarios
    usuarios = [
        Usuario(
            id_usuario="USR001",
            nombre="Juan Pérez",
            correo="juan.perez@example.com",
            tipo_usuario="cliente"
        ),
        Usuario(
            id_usuario="USR002",
            nombre="María García",
            correo="maria.garcia@example.com",
            tipo_usuario="cliente"
        ),
        Usuario(
            id_usuario="USR003",
            nombre="Pedro Rodríguez",
            correo="pedro.rodriguez@example.com",
            tipo_usuario="administrador"
        )
    ]
    
    # Guardar usuarios
    print("\nGuardando usuarios...")
    for usuario in usuarios:
        try:
            usuario.validar_datos()
            data = {
                'id_usuario': usuario.get_id_usuario(),
                'nombre': usuario.get_nombre(),
                'correo': usuario.get_correo(),
                'tipo_usuario': usuario.get_tipo_usuario()
            }
            response = db.client.table('usuarios').insert(data).execute()
            if response.data:
                print(f"Usuario {usuario.get_id_usuario()} guardado exitosamente")
            else:
                print(f"Error al guardar usuario {usuario.get_id_usuario()}")
        except Exception as e:
            print(f"Error al guardar usuario: {str(e)}")
    
    # Lista de ejemplos de materiales
    ejemplos = [
        # Ejemplos de Libros
        Libro(
            titulo="El Señor de los Anillos",
            autor="J.R.R. Tolkien",
            codigo_inventario="LIB001",
            ubicacion="Biblioteca principal",
            disponible=True,
            num_paginas=1178
        ),
        Libro(
            titulo="1984",
            autor="George Orwell",
            codigo_inventario="LIB002",
            ubicacion="Biblioteca principal",
            disponible=True,
            num_paginas=328
        ),
        
        # Ejemplos de Revistas
        Revista(
            titulo="National Geographic",
            autor="National Geographic Society",
            codigo_inventario="REV001",
            ubicacion="Biblioteca principal",
            numero_edicion="12",
            fecha_publicacion="01/05/2023",
            disponible=True
        ),
        Revista(
            titulo="Science",
            autor="American Association for the Advancement of Science",
            codigo_inventario="REV002",
            ubicacion="Biblioteca principal",
            numero_edicion="25",
            fecha_publicacion="15/04/2023",
            disponible=True
        ),
        
        # Ejemplos de DVD
        DVD(
            titulo="El Padrino",
            autor="Francis Ford Coppola",
            codigo_inventario="DVD001",
            ubicacion="Biblioteca principal",
            disponible=True,
            duracion=175,
            formato="Blu-ray"
        ),
        DVD(
            titulo="Friends: The Complete Series",
            autor="Various",
            codigo_inventario="DVD002",
            ubicacion="Biblioteca principal",
            disponible=True,
            duracion=1200,
            formato="DVD"
        )
    ]
    
    # Crear instancia de Database
    db = Database()
    
    # Guardar cada material usando el método guardar_material
    for material in ejemplos:
        if db.guardar_material(material):
            print(f"Material {material.get_codigo_inventario()} guardado exitosamente")
        else:
            print(f"Error al guardar material {material.get_codigo_inventario()}")
    
    print("\n=== Ejemplos de materiales creados y guardados ===")
    print(f"Número total de ejemplos: {len(ejemplos)}")
    
    # Mostrar información de cada ejemplo
    for i, material in enumerate(ejemplos):
        print(f"\nEjemplo {i+1} - Tipo: {material.__class__.__name__}")
        material.mostrar_info()

def crear_ejemplo_libro():
    """Crear un solo ejemplo de libro"""
    libro = Libro(
        titulo="El Quijote",
        autor="Miguel de Cervantes",
        codigo_inventario="LIB003",
        num_paginas=900,
        ubicacion="Biblioteca principal"
    )
    guardar_materiales([libro])
    print("\n=== Ejemplo de libro creado y guardado ===")
    libro.mostrar_info()

def crear_ejemplo_revista():
    """Crear un solo ejemplo de revista"""
    revista = Revista(
        titulo="Nature",
        autor="Nature Publishing Group",
        codigo_inventario="REV003",
        numero_edicion="30",
        fecha_publicacion="01/06/2023",
        ubicacion="Biblioteca principal"
    )
    guardar_materiales([revista])
    print("\n=== Ejemplo de revista creado y guardado ===")
    revista.mostrar_info()

def crear_ejemplo_dvd():
    """Crear un solo ejemplo de DVD"""
    dvd = DVD(
        titulo="Star Wars: The Complete Saga",
        autor="George Lucas",
        codigo_inventario="DVD003",
        duracion=1800,
        formato="Blu-ray",
        ubicacion="Biblioteca principal"
    )
    guardar_materiales([dvd])
    print("\n=== Ejemplo de DVD creado y guardado ===")
    dvd.mostrar_info()

if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    crear_ejemplos()
    
    # También puedes ejecutar los ejemplos individuales
    # crear_ejemplo_libro()
    # crear_ejemplo_revista()
    # crear_ejemplo_dvd()
