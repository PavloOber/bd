from abc import ABC, abstractmethod

class MaterialBiblioteca(ABC):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, tipo, disponible=True):
        self.__titulo = titulo
        self.__autor = autor
        self.__codigo_inventario = codigo_inventario
        self.__ubicacion = ubicacion
        self.__tipo = tipo
        self.__disponible = disponible

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        if not isinstance(tipo, str):
            raise ValueError("El tipo debe ser una cadena")
        self.__tipo = tipo

    @abstractmethod
    def mostrar_info(self):
        """Muestra la información del material"""
        pass

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
        return self.__tipo

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

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def validar_datos(self):
        """Valida que los datos sean correctos"""
        if not self.__titulo or not isinstance(self.__titulo, str):
            raise ValueError("El título debe ser una cadena no vacía")
        if not self.__autor or not isinstance(self.__autor, str):
            raise ValueError("El autor debe ser una cadena no vacía")
        if not self.__codigo_inventario or not isinstance(self.__codigo_inventario, str):
            raise ValueError("El código de inventario debe ser una cadena no vacía")
        if not self.__ubicacion or not isinstance(self.__ubicacion, str):
            raise ValueError("La ubicación debe ser una cadena no vacía")
        if not isinstance(self.__disponible, bool):
            raise ValueError("El estado disponible debe ser True o False")

    def __str__(self):
        return f"{self.__tipo.capitalize()}: {self.__titulo} - {self.__autor} ({self.__codigo_inventario})"

class Libro(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, disponible, num_paginas=None, **kwargs):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, "libro", disponible)
        self.num_paginas = num_paginas

    def get_num_paginas(self):
        return self.num_paginas

    def set_num_paginas(self, num_paginas):
        if num_paginas is not None and not isinstance(num_paginas, int):
            raise ValueError("El número de páginas debe ser un número entero")
        self.num_paginas = num_paginas

    def mostrar_info(self):
        super().mostrar_info()
        if self.num_paginas is not None:
            print(f"Número de páginas: {self.num_paginas}")

    def validar_datos(self):
        super().validar_datos()
        if self.num_paginas is not None and not isinstance(self.num_paginas, int):
            raise ValueError("El número de páginas debe ser un número entero")

class Revista(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, numero_edicion, fecha_publicacion, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, "revista", disponible)
        self.numero_edicion = numero_edicion
        self.fecha_publicacion = fecha_publicacion

    def get_numero_edicion(self):
        return self.numero_edicion

    def set_numero_edicion(self, numero_edicion):
        if not isinstance(numero_edicion, str):
            raise ValueError("El número de edición debe ser una cadena")
        self.numero_edicion = numero_edicion

    def get_fecha_publicacion(self):
        return self.fecha_publicacion

    def set_fecha_publicacion(self, fecha_publicacion):
        if not isinstance(fecha_publicacion, str):
            raise ValueError("La fecha de publicación debe ser una cadena")
        self.fecha_publicacion = fecha_publicacion

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Edición: {self.get_numero_edicion()}")
        print(f"Fecha de publicación: {self.get_fecha_publicacion()}")
        print("--- REVISTA ---")

    def validar_datos(self):
        super().validar_datos()
        if not self.numero_edicion or not isinstance(self.numero_edicion, str):
            raise ValueError("El número de edición debe ser una cadena no vacía")
        if not self.fecha_publicacion or not isinstance(self.fecha_publicacion, str):
            raise ValueError("La fecha de publicación debe ser una cadena no vacía")

class DVD(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, duracion, formato, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, "dvd", disponible)
        self.duracion = duracion
        self.formato = formato

    def get_duracion(self):
        return self.duracion

    def set_duracion(self, duracion):
        if not isinstance(duracion, int):
            raise ValueError("La duración debe ser un número entero")
        self.duracion = duracion

    def get_formato(self):
        return self.formato

    def set_formato(self, formato):
        if not isinstance(formato, str):
            raise ValueError("El formato debe ser una cadena")
        self.formato = formato

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Duración: {self.duracion} minutos")
        print(f"Formato: {self.formato}")

    def validar_datos(self):
        super().validar_datos()
        if not isinstance(self.duracion, int):
            raise ValueError("La duración debe ser un número entero")
        if not self.formato or not isinstance(self.formato, str):
            raise ValueError("El formato debe ser una cadena no vacía")

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

        super().mostrar_info()
        if self.num_paginas is not None:
            print(f"Número de páginas: {self.num_paginas}")

class Revista(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, numero_edicion, fecha_publicacion, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, "revista", disponible)
        self.__numero_edicion = numero_edicion
        self.__fecha_publicacion = fecha_publicacion

    def get_numero_edicion(self):
        return self.__numero_edicion

    def set_numero_edicion(self, numero_edicion):
        if not isinstance(numero_edicion, str):
            raise ValueError("El número de edición debe ser una cadena")
        self.__numero_edicion = numero_edicion

    def get_fecha_publicacion(self):
        return self.__fecha_publicacion

    def set_fecha_publicacion(self, fecha_publicacion):
        if not isinstance(fecha_publicacion, str):
            raise ValueError("La fecha de publicación debe ser una cadena")
        self.__fecha_publicacion = fecha_publicacion

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Edición: {self.get_numero_edicion()}")
        print(f"Fecha de publicación: {self.get_fecha_publicacion()}")
        print("--- REVISTA ---")

class DVD(MaterialBiblioteca):
    def __init__(self, titulo, autor, codigo_inventario, ubicacion, duracion, formato, disponible=True):
        super().__init__(titulo, autor, codigo_inventario, ubicacion, "dvd", disponible)
        self.__duracion = duracion
        self.__formato = formato

    def get_duracion(self):
        return self.__duracion

    def set_duracion(self, duracion):
        if not isinstance(duracion, int):
            raise ValueError("La duración debe ser un número entero")
        self.__duracion = duracion

    def get_formato(self):
        return self.__formato

    def set_formato(self, formato):
        if not isinstance(formato, str):
            raise ValueError("El formato debe ser una cadena")
        self.__formato = formato

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

    def validar_datos(self):
        if not self.__id_usuario or not isinstance(self.__id_usuario, str):
            raise ValueError("El ID de usuario debe ser una cadena no vacía")
        if not self.__nombre or not isinstance(self.__nombre, str):
            raise ValueError("El nombre debe ser una cadena no vacía")
        if not self.__correo or not isinstance(self.__correo, str):
            raise ValueError("El correo debe ser una cadena no vacía")
        if not isinstance(self.__tipo_usuario, str):
            raise ValueError("El tipo de usuario debe ser una cadena")
        if self.__tipo_usuario not in ["cliente", "administrador"]:
            raise ValueError("El tipo de usuario debe ser 'cliente' o 'administrador'")
