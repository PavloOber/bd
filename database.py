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
            self.client.table('prestamos').delete().neq('id_usuario', '').execute()
            print("Datos de préstamos eliminados")
            
            # Eliminar datos de materiales
            self.client.table('materiales').delete().neq('codigo_inventario', '').execute()
            print("Datos de materiales eliminados")
                
            # Eliminar datos de usuarios
            self.client.table('usuarios').delete().neq('correo', '').execute()
            print("Datos de usuarios eliminados")
                
            print("\nTodos los datos han sido eliminados exitosamente")
            return True
        except Exception as e:
            print(f"Error al eliminar datos: {str(e)}")
            return False

    def init_db(self):
        """
        Inicializa la base de datos:
        1. Elimina datos existentes
        2. Crea tablas si no existen
        3. Inserta datos de prueba
        4. Configura RLS
        """
        try:
            # 1. Eliminar datos existentes
            self.eliminar_datos()
            
            # 2. Verificar/Crear tablas
            self._verificar_tablas()
            
            # 3. Insertar datos de prueba
            self._insertar_datos_iniciales()
            
            # 4. Configurar RLS
            self.configurar_rls()
            
            print("\nBase de datos inicializada exitosamente")
            return True
        except Exception as e:
            print(f"Error al inicializar la base de datos: {str(e)}")
            return False

    def _verificar_tablas(self):
        """Verifica que las tablas existan, las crea si no"""
        tablas = ['usuarios', 'materiales', 'prestamos']
        
        for tabla in tablas:
            try:
                self.client.table(tabla).select('*').limit(1).execute()
                print(f"Tabla {tabla} ya existe")
            except:
                # Si no existe, crear tabla básica
                if tabla == 'usuarios':
                    self.client.rpc('create_usuarios_table').execute()
                elif tabla == 'materiales':
                    self.client.rpc('create_materiales_table').execute()
                elif tabla == 'prestamos':
                    self.client.rpc('create_prestamos_table').execute()
                print(f"Tabla {tabla} creada")

    def _insertar_datos_iniciales(self):
        """Inserta datos iniciales de prueba si no existen"""
        try:
            # Verificar si el usuario de prueba ya existe
            usuario_existente = self.client.table('usuarios')\
                .select('*')\
                .eq('correo', 'prueba@example.com')\
            .execute()
        
            if not usuario_existente.data:
                usuario_data = {
                    'nombre': 'Usuario de prueba',
                    'correo': 'prueba@example.com',
                    'tipo_usuario': 'administrador'
                }
                usuario = self.client.table('usuarios').insert(usuario_data).execute()
                usuario_id = usuario.data[0]['id_usuario']
                print("Usuario de prueba creado")
            else:
                usuario_id = usuario_existente.data[0]['id_usuario']
                print("Usuario de prueba ya existe")
        
            # Verificar si el material de prueba ya existe
            material_existente = self.client.table('materiales')\
                .select('*')\
                .eq('codigo_inventario', 'MAT001')\
                .execute()
                
            if not material_existente.data:
                material_data = {
                    'codigo_inventario': 'MAT001',
                    'titulo': 'Material de prueba',
                    'autor': 'Autor de prueba',
                    'tipo': 'libro',
                    'disponible': True,
                    'ubicacion': 'Sección A'
                }
                self.client.table('materiales').insert(material_data).execute()
                print("Material de prueba creado")
        
            return True
        except Exception as e:
            print(f"Error al insertar datos iniciales: {str(e)}")
            return False

    def configurar_rls(self):
        """Configura Row Level Security usando RPC existente"""
        try:
            # Configurar políticas para usuarios
            self.client.rpc('create_usuarios_policies').execute()
            
            # Configurar políticas para materiales
            self.client.rpc('create_materiales_policies').execute()
            
            # Configurar políticas para préstamos
            self.client.rpc('create_prestamos_policies').execute()
            
            print("Políticas RLS configuradas exitosamente")
            return True
        except Exception as e:
            print(f"Error al configurar RLS: {str(e)}")
            return False

    # Métodos CRUD para usuarios
    def guardar_usuario(self, usuario: Usuario):
        """Guarda un usuario en la base de datos"""
        data = {
            'id_usuario': usuario.get_id_usuario(),
            'nombre': usuario.get_nombre(),
            'correo': usuario.get_correo(),
            'tipo_usuario': usuario.get_tipo_usuario()
        }
        
        try:
            response = self.client.table('usuarios').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error al guardar usuario: {str(e)}")
            return False

    def obtener_usuarios(self):
        """Obtiene todos los usuarios"""
        try:
            response = self.client.table('usuarios').select('*').execute()
            return [Usuario(**u) for u in response.data]
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")
            return []

    # Métodos CRUD para materiales
    def guardar_material(self, material: MaterialBiblioteca):
        """Guarda un material en la base de datos"""
        data = {
            'codigo_inventario': material.get_codigo_inventario(),
            'titulo': material.get_titulo(),
            'autor': material.get_autor(),
            'tipo': material.get_tipo(),
            'disponible': material.get_disponible(),
            'ubicacion': material.get_ubicacion()
        }
        
        # Campos específicos por tipo
        if isinstance(material, Libro):
            data['num_paginas'] = material.get_num_paginas()
        elif isinstance(material, Revista):
            data['numero_edicion'] = material.get_numero_edicion()
            data['fecha_publicacion'] = material.get_fecha_publicacion()
        elif isinstance(material, DVD):
            data['duracion'] = material.get_duracion()
            data['formato'] = material.get_formato()

        try:
            response = self.client.table('materiales').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error al guardar material: {str(e)}")
            return False

    def obtener_materiales(self):
        """Obtiene todos los materiales"""
        try:
            response = self.client.table('materiales').select('*').execute()
            materiales = []
            for row in response.data:
                base_data = {
                    'codigo_inventario': row['codigo_inventario'],
                    'titulo': row['titulo'],
                    'autor': row['autor'],
                    'tipo': row['tipo'],
                    'disponible': row['disponible'],
                    'ubicacion': row['ubicacion']
                }
                
                if row['tipo'] == 'Libro':
                    material = Libro(**base_data)
                    if 'num_paginas' in row:
                        material.set_num_paginas(row['num_paginas'])
                elif row['tipo'] == 'Revista':
                    material = Revista(**base_data)
                    if 'numero_edicion' in row:
                        material.set_numero_edicion(row['numero_edicion'])
                    if 'fecha_publicacion' in row:
                        material.set_fecha_publicacion(row['fecha_publicacion'])
                elif row['tipo'] == 'DVD':
                    material = DVD(**base_data)
                    if 'duracion' in row:
                        material.set_duracion(row['duracion'])
                    if 'formato' in row:
                        material.set_formato(row['formato'])
                else:
                    material = MaterialBiblioteca(**base_data)
                
                materiales.append(material)
            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {str(e)}")
            return []

    # Métodos para préstamos
    def guardar_prestamo(self, prestamo: Prestamo):
        """Guarda un préstamo en la base de datos"""
        data = {
            'id_usuario': prestamo.id_usuario,
            'codigo_material': prestamo.id_material,
            'fecha_prestamo': prestamo.fecha_prestamo.isoformat(),
            'fecha_devolucion': prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
        }
        
        try:
            response = self.client.table('prestamos').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error al guardar préstamo: {str(e)}")
            return False

    def devolver_prestamo(self, id_material: str):
        """Marca un préstamo como devuelto"""
        try:
            # Actualizar préstamo
            self.client.table('prestamos').update({
                'fecha_devolucion': datetime.now().isoformat()
            }).eq('codigo_material', id_material).execute()
            
            # Actualizar disponibilidad del material
            self.client.table('materiales').update({
                'disponible': True
            }).eq('codigo_inventario', id_material).execute()
            
            return True
        except Exception as e:
            print(f"Error al devolver préstamo: {str(e)}")
            return False

    def obtener_prestamos(self):
        """Obtiene todos los préstamos"""
        try:
            response = self.client.table('prestamos').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error al obtener préstamos: {str(e)}")
            return []