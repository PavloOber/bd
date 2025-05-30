from utils import cargar_materiales, cargar_usuarios
from menu import Menu
#1111
if __name__ == "__main__":
    # Cargar materiales y usuarios al inicio
    materiales = cargar_materiales()
    usuarios = cargar_usuarios()
    
    # Ejecutar menú principal
    Menu(materiales, usuarios)
