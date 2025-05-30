from abc import ABC, abstractmethod

class MaterialBiblioteca(ABC):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, disponible=True):
        self.__titulo = titulo
        self.__autor = autor
        self.__codigo_inventario = codigo_inventario
        self.__ubicacion = ubicacion
        self.__disponible = disponible

    @abstractmethod
    def mostrar_info(self):
        print(f"Título: {self.__titulo}")
        print(f"Autor: {self.__autor}")
        print(f"Disponible: {'Sí' if self.__disponible else 'No'}")
        print(f"Código de inventario: {self.__codigo_inventario}")
        print(f"Ubicación: {self.__ubicacion}")

    # Getters
    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_codigo_inventario(self):
        return self.__codigo_inventario

    def get_ubicacion(self):
        return self.__ubicacion

    def get_disponible(self):
        return self.__disponible

    def get_tipo(self):
        return self.tipo

    # Setters
    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_autor(self, autor):
        self.__autor = autor

    def set_codigo_inventario(self, codigo_inventario):
        self.__codigo_inventario = codigo_inventario

    def set_ubicacion(self, ubicacion):
        self.__ubicacion = ubicacion

    def set_disponible(self, disponible):
        self.__disponible = disponible

class Libro(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, num_paginas=None, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, disponible)
        self.tipo = "Libro"
        self.num_paginas = num_paginas

    def get_num_paginas(self):
        return self.num_paginas

    def set_num_paginas(self, num_paginas):
        self.num_paginas = num_paginas

    def get_tipo(self):
        return self.tipo

    def mostrar_info(self):
        print(f"\n--- LIBRO ---")
        super().mostrar_info()
        if self.num_paginas is not None:
            print(f"Número de páginas: {self.num_paginas}")

class Revista(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, numero_edicion, fecha_publicacion, ubicacion, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, disponible)
        self.tipo = "Revista"
        self.numero_edicion = numero_edicion
        self.fecha_publicacion = fecha_publicacion

    def get_numero_edicion(self):
        return self.numero_edicion

    def set_numero_edicion(self, numero_edicion):
        self.numero_edicion = numero_edicion

    def get_fecha_publicacion(self):
        return self.fecha_publicacion

    def set_fecha_publicacion(self, fecha_publicacion):
        self.fecha_publicacion = fecha_publicacion

    def mostrar_info(self):
        print(f"\n--- REVISTA ---")
        super().mostrar_info()
        print(f"Edición: {self.__numero_edicion}")
        print(f"Fecha: {self.__fecha_publicacion}")

class DVD(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, duracion, formato, ubicacion, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, disponible)
        self.tipo = "DVD"
        self.duracion = duracion
        self.formato = formato

    def get_duracion(self):
        return self.duracion

    def set_duracion(self, duracion):
        self.duracion = duracion

    def get_formato(self):
        return self.formato

    def set_formato(self, formato):
        self.formato = formato

    def mostrar_info(self):
        print(f"\n--- DVD ---")
        super().mostrar_info()
        print(f"Duración: {self.__duracion} minutos")
        print(f"Formato: {self.__formato}")

class Usuario:
    def __init__(self, id_usuario, nombre, correo, tipo_usuario="cliente"):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__correo = correo
        self.__tipo_usuario = tipo_usuario
        self.__libros_prestados = []

    def get_id_usuario(self):
        return self.__id_usuario

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_tipo_usuario(self):
        return self.__tipo_usuario

    def mostrar_info(self):
        print(f"\n--- USUARIO ---")
        print(f"ID: {self.__id_usuario}")
        print(f"Nombre: {self.__nombre}")
        print(f"Correo: {self.__correo}")
        print(f"Tipo de usuario: {self.__tipo_usuario}")
        print("Libros prestados:")
        for libro in self.__libros_prestados:
            print(f"- {libro.get_titulo()}")

    def prestar_libro(self, libro):
        if libro.get_disponible():
            self.__libros_prestados.append(libro)
            libro.set_disponible(False)
            return True
        return False

    def devolver_libro(self, libro):
        if libro in self.__libros_prestados:
            self.__libros_prestados.remove(libro)
            libro.set_disponible(True)
            return True
        return False

    # Getters
    def get_id_usuario(self):
        return self.__id_usuario

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_tipo_usuario(self):
        return self.__tipo_usuario

    def get_libros_prestados(self):
        return self.__libros_prestados

    # Setters
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_correo(self, correo):
        self.__correo = correo

    def set_tipo_usuario(self, tipo_usuario):
        self.__tipo_usuario = tipo_usuario
