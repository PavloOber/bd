from datetime import datetime
from typing import List

class Prestamo:
    def __init__(self, id_material: str, id_usuario: str, fecha_prestamo: datetime, fecha_devolucion: datetime = None):
        self.id_material = id_material
        self.id_usuario = id_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def devolver(self):
        self.fecha_devolucion = datetime.now()

    def esta_devuelto(self) -> bool:
        return self.fecha_devolucion is not None

    def mostrar_info(self):
        print(f"\n--- PRÉSTAMO ---")
        print(f"ID Material: {self.id_material}")
        print(f"ID Usuario: {self.id_usuario}")
        print(f"Fecha de préstamo: {self.fecha_prestamo.strftime('%d/%m/%Y')}")
        if self.fecha_devolucion:
            print(f"Fecha de devolución: {self.fecha_devolucion.strftime('%d/%m/%Y')}")
        else:
            print("Aún no devuelto")

class GestorPrestamos:
    def __init__(self):
        self.prestamos: List[Prestamo] = []

    def agregar_prestamo(self, id_material: str, id_usuario: str):
        nuevo_prestamo = Prestamo(id_material, id_usuario, datetime.now())
        self.prestamos.append(nuevo_prestamo)
        return nuevo_prestamo

    def devolver_prestamo(self, id_material: str):
        for prestamo in self.prestamos:
            if prestamo.id_material == id_material and not prestamo.esta_devuelto():
                prestamo.devolver()
                return True
        return False

    def listar_prestamos(self):
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return

        print("\n--- LISTA DE PRÉSTAMOS ---")
        for i, prestamo in enumerate(self.prestamos):
            print(f"{i+1}.")
            prestamo.mostrar_info()

    def buscar_prestamo(self, id_material: str = None, id_usuario: str = None):
        resultados = []
        for prestamo in self.prestamos:
            if (id_material and prestamo.id_material == id_material) or \
               (id_usuario and prestamo.id_usuario == id_usuario):
                resultados.append(prestamo)
        return resultados
