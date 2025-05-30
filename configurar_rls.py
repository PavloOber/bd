from database import Database

def configurar_rls():
    # Crear una instancia de la base de datos
    db = Database()
    
    try:
        # Habilitar RLS en la tabla usuarios
        print("\nConfigurando RLS para usuarios...")
        db.client.rpc('sql', {
            'query': '''
                ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
                
                -- Política para permitir que los usuarios vean su propio perfil
                CREATE POLICY "Usuarios pueden ver su propio perfil"
                    ON usuarios
                    FOR SELECT
                    USING (auth.uid()::text = id_usuario);
                
                -- Política para permitir que los administradores vean todos los usuarios
                CREATE POLICY "Administradores pueden ver todos los usuarios"
                    ON usuarios
                    FOR SELECT
                    USING (auth.role() = 'authenticated');
            '''
        })
        
        # Habilitar RLS en la tabla materiales
        print("\nConfigurando RLS para materiales...")
        db.client.rpc('sql', {
            'query': '''
                ALTER TABLE materiales ENABLE ROW LEVEL SECURITY;
                
                -- Política para permitir que los usuarios vean todos los materiales
                CREATE POLICY "Todos pueden ver materiales"
                    ON materiales
                    FOR SELECT
                    USING (true);
                
                -- Política para permitir que los administradores puedan modificar materiales
                CREATE POLICY "Administradores pueden modificar materiales"
                    ON materiales
                    FOR ALL
                    USING (auth.role() = 'authenticated');
            '''
        })
        
        # Habilitar RLS en la tabla préstamos
        print("\nConfigurando RLS para préstamos...")
        db.client.rpc('sql', {
            'query': '''
                ALTER TABLE prestamos ENABLE ROW LEVEL SECURITY;
                
                -- Política para permitir que los usuarios vean sus propios préstamos
                CREATE POLICY "Usuarios pueden ver sus propios préstamos"
                    ON prestamos
                    FOR SELECT
                    USING (auth.uid()::text = id_usuario);
                
                -- Política para permitir que los administradores vean todos los préstamos
                CREATE POLICY "Administradores pueden ver todos los préstamos"
                    ON prestamos
                    FOR SELECT
                    USING (auth.role() = 'authenticated');
            '''
        })
        
        print("\n¡RLS configurado exitosamente!")
        
    except Exception as e:
        print(f"Error al configurar RLS: {str(e)}")
        print("Por favor, configura RLS manualmente en el panel de Supabase:")
        print("1. Ve a SQL Editor")
        print("2. Ejecuta las consultas de RLS para cada tabla")

if __name__ == "__main__":
    configurar_rls()
