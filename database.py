import supabase
from config import SUPABASE_URL, SUPABASE_KEY
from models import MaterialBiblioteca, Usuario, Libro, Revista, DVD
from prestamo import Prestamo

class Database:
    def __init__(self):
        self.client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

    def init_db(self):
        """Inicializa las tablas necesarias en Supabase"""
        try:
            # Crear tabla de usuarios
            self.client.rpc('create_table', {
                'name': 'usuarios',
                'columns': 'id_usuario text primary key, nombre text, correo text, tipo_usuario text'
            })

            # Crear tabla de materiales
            self.client.rpc('create_table', {
                'name': 'materiales',
                'columns': 'codigo_inventario text primary key, titulo text, autor text, tipo text, disponible boolean, ubicacion text'
            })

            # Crear tabla de préstamos
            self.client.rpc('create_table', {
                'name': 'prestamos',
                'columns': 'id serial primary key, id_material text, id_usuario text, fecha_prestamo timestamp, fecha_devolucion timestamp'
            })
            
            print("\nTablas creadas exitosamente:")
            print("- usuarios")
            print("- materiales")
            print("- préstamos")
            
        except Exception as e:
            print(f"Error al crear las tablas: {str(e)}")
            print("Verificando si las tablas ya existen...")
            
            # Verificar si las tablas existen
            try:
                # Intentar obtener datos de las tablas
                self.client.table('usuarios').select('*').execute()
                self.client.table('materiales').select('*').execute()
                self.client.table('prestamos').select('*').execute()
                print("\nLas tablas ya existen en la base de datos.")
            except Exception as e:
                print(f"Error al verificar las tablas: {str(e)}")
                print("Por favor, crea las tablas manualmente en el panel de Supabase:")
                print("1. Ve a SQL Editor")
                print("2. Ejecuta estas consultas:")
                print("CREATE TABLE usuarios (id_usuario text primary key, nombre text, correo text, tipo_usuario text);")
                print("CREATE TABLE materiales (codigo_inventario text primary key, titulo text, autor text, tipo text, disponible boolean, ubicacion text);")
                print("CREATE TABLE prestamos (id serial primary key, id_material text, id_usuario text, fecha_prestamo timestamp, fecha_devolucion timestamp);")

    def guardar_usuario(self, usuario: Usuario):
        """Guarda un usuario en la base de datos"""
        data = {
            'id_usuario': usuario.get_id_usuario(),
            'nombre': usuario.get_nombre(),
            'correo': usuario.get_correo(),
            'tipo_usuario': usuario.get_tipo_usuario()
        }
        self.client.table('usuarios').insert(data).execute()

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos"""
        response = self.client.table('usuarios').select('*').execute()
        usuarios = []
        for row in response.data:
            usuario = Usuario(
                id_usuario=row['id_usuario'],
                nombre=row['nombre'],
                correo=row['correo'],
                tipo_usuario=row['tipo_usuario']
            )
            usuarios.append(usuario)
        return usuarios

    def guardar_material(self, material: MaterialBiblioteca):
        """Guarda un material en la base de datos"""
        data = {
            'codigo_inventario': material.get_codigo_inventario(),
            'titulo': material.get_titulo(),
            'autor': material.get_autor(),
            'tipo': material.__class__.__name__,
            'disponible': material.get_disponible(),
            'ubicacion': material.get_ubicacion()
        }
        self.client.table('materiales').insert(data).execute()

    def obtener_materiales(self):
        """Obtiene todos los materiales de la base de datos"""
        response = self.client.table('materiales').select('*').execute()
        materiales = []
        for row in response.data:
            if row['tipo'] == 'Libro':
                material = Libro(
                    titulo=row['titulo'],
                    autor=row['autor'],
                    codigo_inventario=row['codigo_inventario'],
                    ubicacion=row['ubicacion'],
                    disponible=row['disponible']
                )
            elif row['tipo'] == 'Revista':
                material = Revista(
                    titulo=row['titulo'],
                    autor=row['autor'],
                    codigo_inventario=row['codigo_inventario'],
                    ubicacion=row['ubicacion'],
                    disponible=row['disponible']
                )
            elif row['tipo'] == 'DVD':
                material = DVD(
                    titulo=row['titulo'],
                    autor=row['autor'],
                    codigo_inventario=row['codigo_inventario'],
                    ubicacion=row['ubicacion'],
                    disponible=row['disponible']
                )
            materiales.append(material)
        return materiales

    def guardar_prestamo(self, prestamo: Prestamo):
        """Guarda un préstamo en la base de datos"""
        data = {
            'id_material': prestamo.id_material,
            'id_usuario': prestamo.id_usuario,
            'fecha_prestamo': prestamo.fecha_prestamo.isoformat(),
            'fecha_devolucion': prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
        }
        self.client.table('prestamos').insert(data).execute()

    def obtener_prestamos(self):
        """Obtiene todos los préstamos de la base de datos"""
        response = self.client.table('prestamos').select('*').execute()
        prestamos = []
        for row in response.data:
            prestamo = Prestamo(
                id_material=row['id_material'],
                id_usuario=row['id_usuario'],
                fecha_prestamo=datetime.fromisoformat(row['fecha_prestamo']),
                fecha_devolucion=datetime.fromisoformat(row['fecha_devolucion']) if row['fecha_devolucion'] else None
            )
            prestamos.append(prestamo)
        return prestamos
