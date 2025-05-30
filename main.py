from utils import cargar_materiales, cargar_usuarios, cargar_prestamos
from menu import Menu

if __name__ == "__main__":
    # Cargar materiales y usuarios al inicio
    materiales = cargar_materiales()
    usuarios = cargar_usuarios()
    prestamos = cargar_prestamos()
    
    # Ejecutar menú principal
    Menu(materiales, usuarios, prestamos)
