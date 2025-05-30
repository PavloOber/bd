from models import Libro, Revista, DVD
from utils import guardar_materiales

def crear_ejemplos():
    # Lista de ejemplos de materiales
    ejemplos = [
        # Ejemplos de Libros
        Libro(
            titulo="El Señor de los Anillos",
            autor="J.R.R. Tolkien",
            codigo_inventario="LIB001",
            num_paginas=1178,
            ubicacion="Biblioteca principal"
        ),
        Libro(
            titulo="1984",
            autor="George Orwell",
            codigo_inventario="LIB002",
            num_paginas=328,
            ubicacion="Biblioteca principal"
        ),
        
        # Ejemplos de Revistas
        Revista(
            titulo="National Geographic",
            autor="National Geographic Society",
            codigo_inventario="REV001",
            numero_edicion="12",
            fecha_publicacion="01/05/2023",
            ubicacion="Biblioteca principal"
        ),
        Revista(
            titulo="Science",
            autor="American Association for the Advancement of Science",
            codigo_inventario="REV002",
            numero_edicion="25",
            fecha_publicacion="15/04/2023",
            ubicacion="Biblioteca principal"
        ),
        
        # Ejemplos de DVD
        DVD(
            titulo="El Padrino",
            autor="Francis Ford Coppola",
            codigo_inventario="DVD001",
            duracion=175,
            formato="Blu-ray",
            ubicacion="Biblioteca principal"
        ),
        DVD(
            titulo="Friends: The Complete Series",
            autor="Various",
            codigo_inventario="DVD002",
            duracion=1200,
            formato="DVD",
            ubicacion="Biblioteca principal"
        )
    ]
    
    # Guardar los ejemplos en el archivo
    guardar_materiales(ejemplos)
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
