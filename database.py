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
                ids_prestamos = [str(item['id']) for item in prestamos.data]
                self.client.table('prestamos').delete().in_('id', ids_prestamos).execute()
            
            # Eliminar materiales
            materiales = self.client.table('materiales').select('codigo_inventario').execute()
            if materiales.data:
                codigos = [item['codigo_inventario'] for item in materiales.data]
                self.client.table('materiales').delete().in_('codigo_inventario', codigos).execute()
            
            # Eliminar usuarios (excepto el usuario de prueba)
            usuarios = self.client.table('usuarios').select('id_usuario').execute()
            if usuarios.data:
                ids_usuarios = [item['id_usuario'] for item in usuarios.data if item['id_usuario'] != 'usuario_prueba']
                if ids_usuarios:
                    self.client.table('usuarios').delete().in_('id_usuario', ids_usuarios).execute()
            
            print("Datos eliminados exitosamente")
            return True
        except Exception as e:
            print(f"Error al eliminar datos: {str(e)}")
            return False

    def guardar_material(self, material: MaterialBiblioteca):
        """Guarda un material en la base de datos"""
        try:
            # Validar datos antes de guardar
            material.validar_datos()
            
            data = {
                'codigo_inventario': material.get_codigo_inventario(),
                'titulo': material.get_titulo(),
                'autor': material.get_autor(),
                'tipo': material.get_tipo(),
                'disponible': material.get_disponible(),
                'ubicacion': material.get_ubicacion()
            }
            
            # Agregar campos específicos según el tipo de material
            if isinstance(material, Libro):
                if material.get_num_paginas() is not None:
                    data['num_paginas'] = material.get_num_paginas()
            elif isinstance(material, Revista):
                data['numero_edicion'] = material.get_numero_edicion()
                data['fecha_publicacion'] = material.get_fecha_publicacion()
            elif isinstance(material, DVD):
                data['duracion'] = material.get_duracion()
                data['formato'] = material.get_formato()
            
            # Guardar en la base de datos
            response = self.client.table('materiales').insert(data).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error al guardar material: {str(e)}")
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
            if not self.eliminar_datos():
                print("Advertencia: No se pudieron eliminar los datos existentes")
            
            # 2. Verificar/Crear tablas
            self._verificar_tablas()
            
            # 3. Insertar datos de prueba
            self._insertar_datos_iniciales()
            
            # 4. Configurar RLS (RLS configuration is handled via Supabase dashboard)
            # Note: RLS configuration is handled via Supabase dashboard, not programmatically
            
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
                # Intentar seleccionar datos de la tabla
                result = self.client.table(tabla).select('*').limit(1).execute()
                if result.data:
                    print(f"Tabla {tabla} ya existe y tiene datos")
                else:
                    print(f"Tabla {tabla} ya existe pero está vacía")
            except Exception as e:
                print(f"Error al verificar tabla {tabla}: {str(e)}")
                # Si no existe, crear tabla usando RPC
                try:
                    if tabla == 'usuarios':
                        self.client.rpc('create_usuarios_table').execute()
                        print("Tabla usuarios creada")
                    elif tabla == 'materiales':
                        self.client.rpc('create_materiales_table').execute()
                        print("Tabla materiales creada")
                    elif tabla == 'prestamos':
                        self.client.rpc('create_prestamos_table').execute()
                        print("Tabla prestamos creada")
                except Exception as rpc_error:
                    print(f"Error al crear tabla {tabla}: {str(rpc_error)}")
                    return False
        return True

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
        """Configura Row Level Security usando el método correcto de Supabase"""
        try:
            # Configurar políticas para usuarios
            self.client.table('usuarios').enable_rls().execute()
            
            self.client.table('usuarios').create_policy(
                name="ver_perfil",
                condition="auth.uid() = id_usuario",
                using="SELECT"
            ).execute()
            
            self.client.table('usuarios').create_policy(
                name="ver_todos",
                condition="EXISTS (SELECT 1 FROM usuarios WHERE id_usuario = auth.uid() AND tipo_usuario = 'administrador')",
                using="SELECT"
            ).execute()
            
            self.client.table('usuarios').create_policy(
                name="actualizar_perfil",
                condition="auth.uid() = id_usuario",
                using="UPDATE"
            ).execute()
            
            # Configurar políticas para materiales
            self.client.table('materiales').enable_rls().execute()
            
            self.client.table('materiales').create_policy(
                name="ver_materiales",
                condition="true",
                using="SELECT"
            ).execute()
            
            self.client.table('materiales').create_policy(
                name="modificar_materiales",
                condition="EXISTS (SELECT 1 FROM usuarios WHERE id_usuario = auth.uid() AND tipo_usuario = 'administrador')",
                using="ALL"
            ).execute()
            
            # Configurar políticas para préstamos
            self.client.table('prestamos').enable_rls().execute()
            
            self.client.table('prestamos').create_policy(
                name="ver_propios",
                condition="id_usuario = auth.uid()",
                using="SELECT"
            ).execute()
            
            self.client.table('prestamos').create_policy(
                name="ver_todos",
                condition="EXISTS (SELECT 1 FROM usuarios WHERE id_usuario = auth.uid() AND tipo_usuario = 'administrador')",
                using="SELECT"
            ).execute()
            
            self.client.table('prestamos').create_policy(
                name="crear_prestamo",
                condition="id_usuario = auth.uid()",
                using="INSERT"
            ).execute()
            
            self.client.table('prestamos').create_policy(
                name="modificar",
                condition="EXISTS (SELECT 1 FROM usuarios WHERE id_usuario = auth.uid() AND tipo_usuario = 'administrador')",
                using="ALL"
            ).execute()
            
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
                
                tipo = row['tipo'].lower()  # Convertir a minúsculas para coincidir con la base de datos
                if tipo == 'libro':
                    material = Libro(**base_data)
                    if 'num_paginas' in row:
                        material.set_num_paginas(row['num_paginas'])
                elif tipo == 'revista':
                    material = Revista(**base_data)
                    if 'numero_edicion' in row:
                        material.set_numero_edicion(row['numero_edicion'])
                    if 'fecha_publicacion' in row:
                        material.set_fecha_publicacion(row['fecha_publicacion'])
                elif tipo == 'dvd':
                    material = DVD(**base_data)
                    if 'duracion' in row:
                        material.set_duracion(row['duracion'])
                    if 'formato' in row:
                        material.set_formato(row['formato'])
                else:
                    # Si el tipo no es reconocido, saltar este registro
                    print(f"Advertencia: Tipo de material no reconocido: {tipo}")
                    continue
                
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