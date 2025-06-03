import supabase
from config import SUPABASE_URL, SUPABASE_KEY
from models import MaterialBiblioteca, Usuario, Libro, Revista, DVD
from prestamo import Prestamo
from datetime import datetime

class Database:
    def __init__(self):
        self.client = supabase.Client(SUPABASE_URL, SUPABASE_KEY)

    def eliminar_datos(self):
        """
        Elimina datos de las tablas, manteniendo el usuario de prueba.
        """
        try:
            # Eliminar préstamos
            prestamos = self.client.table('prestamos').select('id').execute()
            if prestamos.data:
                ids_prestamos = [item['id'] for item in prestamos.data]
                self.client.table('prestamos').delete().in_('id', ids_prestamos).execute()
            
            # Eliminar materiales
            materiales = self.client.table('materiales').select('codigo_inventario').execute()
            if materiales.data:
                codigos_materiales = [item['codigo_inventario'] for item in materiales.data]
                self.client.table('materiales').delete().in_('codigo_inventario', codigos_materiales).execute()
            
            # Eliminar usuarios (excepto el de prueba)
            usuarios = self.client.table('usuarios').select('id_usuario').execute()
            if usuarios.data:
                ids_usuarios = [item['id_usuario'] for item in usuarios.data if item['id_usuario'] != 'USR000']
                self.client.table('usuarios').delete().in_('id_usuario', ids_usuarios).execute()
            
            # Recrear las tablas y políticas
            self.client.rpc('create_usuarios_table').execute()
            self.client.rpc('create_materiales_table').execute()
            self.client.rpc('create_prestamos_table').execute()
            self.client.rpc('create_usuarios_policies').execute()
            self.client.rpc('create_materiales_policies').execute()
            self.client.rpc('create_prestamos_policies').execute()
            
            print("Datos eliminados y tablas recreadas exitosamente")
            return True
        except Exception as e:
            print(f"Error al eliminar datos: {str(e)}")
            return False

    def obtener_materiales(self):
        """Obtiene todos los materiales"""
        try:
            response = self.client.table('materiales').select('*').execute()
            materiales = []
            for row in response.data:
                base_data = {
                    'titulo': row['titulo'],
                    'autor': row['autor'],
                    'codigo_inventario': row['codigo_inventario'],
                    'ubicacion': row['ubicacion'],
                    'disponible': row['disponible']
                }
                
                tipo = row['tipo'].lower()
                if tipo == 'libro':
                    material = Libro(**base_data)
                    if 'num_paginas' in row:
                        material.set_num_paginas(row['num_paginas'])
                elif tipo == 'revista':
                    material = Revista(
                        **base_data,
                        numero_edicion=row.get('numero_edicion', ''),
                        fecha_publicacion=row.get('fecha_publicacion', '')
                    )
                elif tipo == 'dvd':
                    material = DVD(
                        **base_data,
                        duracion=row.get('duracion', 0),
                        formato=row.get('formato', '')
                    )
                else:
                    print(f"Advertencia: Tipo de material no reconocido: {tipo}")
                    continue
                
                materiales.append(material)
            
            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {str(e)}")
            return []

    def guardar_material(self, material: MaterialBiblioteca):
        """Guarda un material en la base de datos"""
        try:
            material.validar_datos()
            
            data = {
                'codigo_inventario': material.get_codigo_inventario(),
                'titulo': material.get_titulo(),
                'autor': material.get_autor(),
                'tipo': material.get_tipo(),
                'disponible': material.get_disponible(),
                'ubicacion': material.get_ubicacion()
            }
            
            if isinstance(material, Libro):
                if material.get_num_paginas() is not None:
                    data['num_paginas'] = material.get_num_paginas()
            elif isinstance(material, Revista):
                data['numero_edicion'] = material.get_numero_edicion()
                data['fecha_publicacion'] = material.get_fecha_publicacion()
            elif isinstance(material, DVD):
                data['duracion'] = material.get_duracion()
                data['formato'] = material.get_formato()
            
            response = self.client.table('materiales').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error al guardar material: {str(e)}")
            return False

    def guardar_prestamo(self, prestamo: Prestamo):
        """Guarda un préstamo en la base de datos"""
        try:
            data = {
                'id_usuario': prestamo.id_usuario,
                'codigo_inventario': prestamo.codigo_inventario,
                'fecha_prestamo': prestamo.fecha_prestamo.isoformat(),
                'fecha_devolucion': prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
            }

            response = self.client.table('prestamos').insert(data).execute()
            
            if response.data:
                self.client.table('materiales')\
                    .update({'disponible': False})\
                    .eq('codigo_inventario', prestamo.codigo_inventario)\
                    .execute()
                return True
            
            return False
        except Exception as e:
            print(f"Error al guardar préstamo: {str(e)}")
            return False

    def init_db(self):
        """
        Inicializa la base de datos:
        1. Verifica que las tablas existan
        2. Inserta datos iniciales si no existen
        """
        try:
            if not self._verificar_tablas():
                print("Error al verificar/crear tablas")
                return False
            
            if not self._insertar_datos_iniciales():
                print("Error al insertar datos iniciales")
                return False
            
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
                result = self.client.table(tabla).select('*').limit(1).execute()
                if result.data:
                    print(f"Tabla {tabla} ya existe y tiene datos")
                else:
                    print(f"Tabla {tabla} ya existe pero está vacía")
            except Exception as e:
                print(f"Error al verificar tabla {tabla}: {str(e)}")
                try:
                    if tabla == 'usuarios':
                        self.client.rpc('create_usuarios_table').execute()
                        print("Tabla usuarios creada")
                    elif tabla == 'materiales':
                        self.client.rpc('create_materiales_table').execute()
                        print("Tabla materiales creada")
                    elif tabla == 'prestamos':
                        try:
                            # Intenta eliminar políticas y tabla si existen
                            try:
                                self.client.rpc('drop_prestamos_policies').execute()
                            except:
                                print("No se pudieron eliminar políticas de préstamos, probablemente no existían")
                            
                            try:
                                self.client.rpc('drop_prestamos_table').execute()
                            except:
                                print("No se pudo eliminar tabla prestamos, probablemente no existía")
                            
                            print("Tabla prestamos eliminada")
                            
                            self.client.rpc('create_prestamos_table').execute()
                            print("Tabla prestamos creada")
                            
                            # Verificar estructura de la tabla
                            columns = self.client.rpc('get_prestamos_columns').execute()
                            if columns.data:
                                required_columns = ['id', 'id_usuario', 'codigo_inventario', 'fecha_prestamo', 'fecha_devolucion']
                                existing_columns = [col['column_name'] for col in columns.data]
                                missing_columns = [col for col in required_columns if col not in existing_columns]
                                
                                if missing_columns:
                                    raise ValueError(f"Columnas faltantes: {missing_columns}")
                                    
                                expected_types = {
                                    'id': 'integer',
                                    'id_usuario': 'integer',
                                    'codigo_inventario': 'character varying',
                                    'fecha_prestamo': 'timestamp without time zone',
                                    'fecha_devolucion': 'timestamp without time zone'
                                }
                                
                                for col in columns.data:
                                    if col['column_name'] in expected_types:
                                        expected_type = expected_types[col['column_name']]
                                        if col['data_type'] != expected_type:
                                            raise ValueError(f"Tipo incorrecto para {col['column_name']}: {col['data_type']}, esperado: {expected_type}")
                                
                                print("Estructura de la tabla prestamos verificada")
                                self.client.rpc('create_prestamos_policies').execute()
                                print("Políticas RLS creadas")
                        except Exception as e:
                            print(f"Error al crear tabla prestamos: {str(e)}")
                            return False
                except Exception as e:
                    print(f"Error al crear tabla {tabla}: {str(e)}")
                    return False
        
        return True

    def _insertar_datos_iniciales(self):
        """Inserta datos iniciales de prueba si no existen"""
        try:
            # Insertar usuario de prueba
            usuario_existente = self.client.table('usuarios')\
                .select('*')\
                .eq('correo', 'prueba@example.com')\
                .execute()
        
            if not usuario_existente.data:
                usuario_data = {
                    'id_usuario': 'USR000',
                    'nombre': 'Usuario de prueba',
                    'correo': 'prueba@example.com',
                    'tipo_usuario': 'administrador'
                }
                self.client.table('usuarios').insert(usuario_data).execute()
                print("Usuario de prueba creado")
        
            # Insertar material de prueba
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
                    'ubicacion': 'Sección A',
                    'num_paginas': 100  # Campo específico para libro
                }
                self.client.table('materiales').insert(material_data).execute()
                print("Material de prueba creado")
        
            return True
        except Exception as e:
            print(f"Error al insertar datos iniciales: {str(e)}")
            return False

    def configurar_rls(self):
        """Configura Row Level Security usando RPCs"""
        try:
            # Configurar políticas usando RPCs
            self.client.rpc('create_usuarios_policies').execute()
            self.client.rpc('create_materiales_policies').execute()
            self.client.rpc('create_prestamos_policies').execute()
            
            print("Políticas RLS configuradas exitosamente")
            return True
        except Exception as e:
            print(f"Error al configurar RLS: {str(e)}")
            return False

    def guardar_usuario(self, usuario: Usuario):
        """Guarda un usuario en la base de datos"""
        try:
            data = {
                'id_usuario': usuario.get_id_usuario(),
                'nombre': usuario.get_nombre(),
                'correo': usuario.get_correo(),
                'tipo_usuario': usuario.get_tipo_usuario()
            }
            
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

    def devolver_prestamo(self, id_inventario: str):
        """Marca un préstamo como devuelto"""
        try:
            # Actualizar préstamo
            self.client.table('prestamos')\
                .update({'fecha_devolucion': datetime.now().isoformat()})\
                .eq('codigo_inventario', id_inventario)\
                .is_('fecha_devolucion', 'null')\
                .execute()
            
            # Actualizar disponibilidad del material
            self.client.table('materiales')\
                .update({'disponible': True})\
                .eq('codigo_inventario', id_inventario)\
                .execute()
            
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