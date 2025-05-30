import supabase
from config import SUPABASE_URL, SUPABASE_KEY
from models import MaterialBiblioteca, Usuario, Libro, Revista, DVD
from prestamo import Prestamo
from datetime import datetime

class Database:
    def __init__(self):
        self.client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

    def eliminar_datos(self):
        """Elimina todos los datos existentes de las tablas"""
        try:
            # Eliminar datos de préstamos
            try:
                self.client.table('prestamos').delete().execute()
                print("Datos de préstamos eliminados")
            except:
                print("No se pudieron eliminar los datos de préstamos")
                
            # Eliminar datos de materiales
            try:
                self.client.table('materiales').delete().execute()
                print("Datos de materiales eliminados")
            except:
                print("No se pudieron eliminar los datos de materiales")
                
            # Eliminar datos de usuarios
            try:
                self.client.table('usuarios').delete().execute()
                print("Datos de usuarios eliminados")
            except:
                print("No se pudieron eliminar los datos de usuarios")
                
            print("\nTodos los datos han sido eliminados exitosamente")
        except Exception as e:
            print(f"Error al eliminar datos: {str(e)}")

    def init_db(self):
        """Inicializa las tablas necesarias en Supabase"""
        try:
            # Primero verificar si las tablas existen
            try:
                # Verificar tabla usuarios
                self.client.table('usuarios').select('*').execute()
                print("Tabla usuarios ya existe")
            except:
                # Crear tabla usuarios
                self.client.table('usuarios').insert({
                    'id_usuario': 'text',
                    'nombre': 'text',
                    'correo': 'text',
                    'tipo_usuario': 'text'
                }).execute()
                print("Tabla usuarios creada")

            # Verificar tabla materiales
            try:
                self.client.table('materiales').select('*').execute()
                print("Tabla materiales ya existe")
            except:
                # Crear tabla materiales
                self.client.table('materiales').insert({
                    'codigo_inventario': 'text',
                    'titulo': 'text',
                    'autor': 'text',
                    'ubicacion': 'text',
                    'disponible': 'boolean',
                    'tipo': 'text',
                    'num_paginas': 'integer',
                    'numero_edicion': 'text',
                    'fecha_publicacion': 'text',
                    'duracion': 'integer',
                    'formato': 'text'
                }).execute()
                print("Tabla materiales creada")

            # Verificar tabla préstamos
            try:
                self.client.table('prestamos').select('*').execute()
                print("Tabla préstamos ya existe")
            except:
                # Crear tabla préstamos
                self.client.table('prestamos').insert({
                    'id': 'text',
                    'id_usuario': 'text',
                    'codigo_material': 'text',
                    'fecha_prestamo': 'timestamp',
                    'fecha_devolucion': 'timestamp',
                    'devuelto': 'boolean'
                }).execute()
                print("Tabla préstamos creada")

            print("\nTablas inicializadas exitosamente")
        except Exception as e:
            print(f"Error al inicializar las tablas: {str(e)}")
            print("Verificando si las tablas ya existen...")

            # Verificar y actualizar tabla materiales
            try:
                # Intentar crear la tabla si no existe
                try:
                    self.client.table('materiales').insert({
                        'codigo_inventario': 'text',
                        'titulo': 'text',
                        'autor': 'text',
                        'ubicacion': 'text',
                        'disponible': 'boolean',
                        'tipo': 'text',
                        'num_paginas': 'integer',
                        'numero_edicion': 'text',
                        'fecha_publicacion': 'text',
                        'duracion': 'integer',
                        'formato': 'text'
                    }).execute()
                    print("Tabla materiales creada")
                except:
                    print("Tabla materiales ya existe")
                    
                    # Verificar si las columnas necesarias existen
                    columns = ['num_paginas', 'numero_edicion', 'fecha_publicacion', 'duracion', 'formato']
                    missing_columns = []
                    for column in columns:
                        try:
                            self.client.table('materiales').select(column).execute()
                            print(f"Columna {column} ya existe")
                        except:
                            missing_columns.append(column)
                    
                    # Si faltan columnas, mostrar mensaje y continuar
                    if missing_columns:
                        print(f"Faltan columnas: {', '.join(missing_columns)}")
                        print("Por favor, crea las columnas faltantes manualmente en el panel de Supabase:")
                        for column in missing_columns:
                            print(f"ALTER TABLE materiales ADD COLUMN {column} text;" if column != 'num_paginas' and column != 'duracion' else f"ALTER TABLE materiales ADD COLUMN {column} integer;")
                        print("\nDespués de crear las columnas, reinicia la aplicación.")
            except Exception as e:
                print(f"Error al verificar tabla materiales: {str(e)}")
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
                    print("CREATE TABLE materiales (codigo_inventario text primary key, titulo text, autor text, tipo text, disponible boolean, ubicacion text, num_paginas integer, numero_edicion text, fecha_publicacion text, duracion integer, formato text);")
                    print("CREATE TABLE prestamos (id_prestamo text primary key, id_usuario text, codigo_material text, fecha_prestamo timestamp, fecha_devolucion timestamp, devuelto boolean);")
            except Exception as e:
                print(f"Error al verificar tabla materiales: {str(e)}")
                print("Recreando tabla materiales...")
                self.client.table('materiales').insert({
                    'codigo_inventario': 'string',
                    'titulo': 'string',
                    'autor': 'string',
                    'ubicacion': 'string',
                    'disponible': 'boolean',
                    'tipo': 'string',
                    'num_paginas': 'integer',
                    'numero_edicion': 'string',
                    'fecha_publicacion': 'string',
                    'duracion': 'integer',
                    'formato': 'string'
                }).execute()
                print("Tabla materiales recreada")

            # Verificar y actualizar tabla préstamos
            try:
                self.client.table('prestamos').select('*').execute()
                print("Tabla préstamos ya existe")
            except:
                self.client.table('prestamos').insert({
                    'id_prestamo': 'string',
                    'id_usuario': 'string',
                    'codigo_material': 'string',
                    'fecha_prestamo': 'timestamp',
                    'fecha_devolucion': 'timestamp',
                    'devuelto': 'boolean'
                }).execute()
                print("Tabla préstamos creada")

            print("\nTablas inicializadas exitosamente")
        except Exception as e:
            print(f"Error al inicializar las tablas: {str(e)}")
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
        try:
            data = {
                'id_usuario': usuario.get_id_usuario(),
                'nombre': usuario.get_nombre(),
                'correo': usuario.get_correo(),
                'tipo_usuario': usuario.get_tipo_usuario()
            }
            
            # Primero intentamos insertar con el rol de administrador
            response = self.client.table('usuarios').insert(data).execute()
            
            if not response.data:
                # Si falla, intentamos con un rol específico
                response = self.client.table('usuarios').insert(data).execute()
            
            if response.data:
                print(f"\nUsuario agregado exitosamente!")
                print(f"ID: {response.data[0]['id_usuario']}")
                print(f"Nombre: {response.data[0]['nombre']}")
                print(f"Correo: {response.data[0]['correo']}")
                print(f"Tipo: {response.data[0]['tipo_usuario']}")
                return True
            else:
                print("No se pudo agregar el usuario. Verifica los permisos RLS.")
                return False
            
        except Exception as e:
            print(f"Error al agregar el usuario: {str(e)}")
                print(f"Autor: {response.data[0]['autor']}")
                print(f"Tipo: {response.data[0]['tipo']}")
                print(f"Disponible: {response.data[0]['disponible']}")
                print(f"Ubicación: {response.data[0]['ubicacion']}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error al guardar el material: {str(e)}")
            return False

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos"""
        try:
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
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")
            return []

    def obtener_materiales(self):
        """Obtiene todos los materiales de la base de datos"""
        try:
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
                    if row.get('num_paginas') is not None:
                        material.set_num_paginas(row['num_paginas'])
                elif row['tipo'] == 'Revista':
                    material = Revista(
                        titulo=row['titulo'],
                        autor=row['autor'],
                        codigo_inventario=row['codigo_inventario'],
                        ubicacion=row['ubicacion'],
                        disponible=row['disponible']
                    )
                    if row.get('numero_edicion') is not None:
                        material.set_numero_edicion(row['numero_edicion'])
                    if row.get('fecha_publicacion') is not None:
                        material.set_fecha_publicacion(row['fecha_publicacion'])
                elif row['tipo'] == 'DVD':
                    material = DVD(
                        titulo=row['titulo'],
                        autor=row['autor'],
                        codigo_inventario=row['codigo_inventario'],
                        ubicacion=row['ubicacion'],
                        disponible=row['disponible']
                    )
                    if row.get('duracion') is not None:
                        material.set_duracion(row['duracion'])
                    if row.get('formato') is not None:
                        material.set_formato(row['formato'])
                materiales.append(material)
            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {str(e)}")
            return []

    def guardar_prestamo(self, prestamo: Prestamo):
        """Guarda un préstamo en la base de datos"""
        try:
            # Convertir fechas a string en formato ISO
            data = {
                'id_material': prestamo.id_material,
                'id_usuario': prestamo.id_usuario,
                'fecha_prestamo': prestamo.fecha_prestamo.isoformat(),
                'fecha_devolucion': prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
            }
            
            response = self.client.table('prestamos').insert(data).execute()
            return True
            
        except Exception as e:
            print(f"Error al agregar el préstamo: {str(e)}")
            return False

    def devolver_prestamo(self, id_material: str):
        """Marca un préstamo como devuelto y actualiza la disponibilidad del material"""
        try:
            # Verificar si el préstamo ya está devuelto
            prestamo = self.client.table('prestamos')\
                .select('*')\
                .eq('id_material', id_material)\
                .execute()
            
            if not prestamo.data:
                print(f"Error: No se encontró el préstamo para el material {id_material}")
                return False
            
            if prestamo.data[0]['fecha_devolucion']:
                print(f"El préstamo para el material {id_material} ya está devuelto")
                return True
            
            # Actualizar la fecha de devolución del préstamo
            print(f"\nDevuelviendo préstamo para material: {id_material}")
            fecha_devolucion = datetime.now().isoformat()
            self.client.table('prestamos')\
                .update({'fecha_devolucion': fecha_devolucion})\
                .eq('id_material', id_material)\
                .execute()
            
            # Buscar el material para actualizar su disponibilidad
            material = None
            materiales = self.client.table('materiales')\
                .select('*')\
                .eq('codigo_inventario', id_material)\
                .execute()
            
            if materiales.data:
                material = materiales.data[0]
                
                # Actualizar la disponibilidad del material
                self.client.table('materiales')\
                    .update({'disponible': True})\
                    .eq('codigo_inventario', id_material)\
                    .execute()
                
                print(f"\nMaterial {id_material} marcado como disponible")
                return True
            
            print(f"Error: No se encontró el material {id_material}")
            return False
            
        except Exception as e:
            print(f"Error al devolver el préstamo: {str(e)}")
            return False

    def obtener_prestamos(self):
        """Obtiene todos los préstamos de la base de datos"""
        try:
            response = self.client.table('prestamos').select('*').execute()
            # Supabase ya devuelve las fechas en formato ISO, no necesitamos convertirlas
            return response.data
        except Exception as e:
            print(f"Error al obtener préstamos: {str(e)}")
            return []