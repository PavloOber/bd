-- Crear tabla usuarios
CREATE OR REPLACE FUNCTION create_usuarios_table()
RETURNS void AS $$
BEGIN
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(100) UNIQUE NOT NULL,
        tipo_usuario VARCHAR(20) NOT NULL
    );
END;
$$ LANGUAGE plpgsql;

-- Crear tabla materiales
CREATE OR REPLACE FUNCTION create_materiales_table()
RETURNS void AS $$
BEGIN
    CREATE TABLE IF NOT EXISTS materiales (
        codigo_inventario VARCHAR(20) PRIMARY KEY,
        titulo VARCHAR(100) NOT NULL,
        autor VARCHAR(100),
        ubicacion VARCHAR(50),
        disponible BOOLEAN DEFAULT true,
        tipo VARCHAR(20) NOT NULL,
        num_paginas INTEGER,
        numero_edicion VARCHAR(20),
        fecha_publicacion DATE,
        duracion INTEGER,
        formato VARCHAR(20)
    );
END;
$$ LANGUAGE plpgsql;

-- Crear tabla préstamos
CREATE OR REPLACE FUNCTION public.create_prestamos_table()
RETURNS void AS $$
BEGIN
    CREATE TABLE IF NOT EXISTS public.prestamos (
        id SERIAL PRIMARY KEY,
        id_usuario INTEGER REFERENCES public.usuarios(id_usuario),
        id_material VARCHAR(20) REFERENCES public.materiales(codigo_inventario),
        fecha_prestamo TIMESTAMP WITHOUT TIME ZONE,
        fecha_devolucion TIMESTAMP WITHOUT TIME ZONE,
        devuelto BOOLEAN DEFAULT false
    );
END;
$$ LANGUAGE plpgsql;

-- Función para eliminar tabla préstamos
CREATE OR REPLACE FUNCTION public.drop_prestamos_table()
RETURNS void AS $$
BEGIN
    DROP TABLE IF EXISTS public.prestamos;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener columnas de la tabla préstamos
CREATE OR REPLACE FUNCTION public.get_prestamos_columns()
RETURNS TABLE(column_name text, data_type text) AS $$
BEGIN
    RETURN QUERY
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'prestamos';
END;
$$ LANGUAGE plpgsql;

-- Función para obtener políticas RLS de la tabla préstamos
CREATE OR REPLACE FUNCTION public.get_prestamos_policies()
RETURNS TABLE(policy_name text, command text, using_expression text) AS $$
BEGIN
    RETURN QUERY
    SELECT policyname, cmd, using_expression
    FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'prestamos';
END;
$$ LANGUAGE plpgsql;

-- Crear políticas RLS para usuarios
CREATE OR REPLACE FUNCTION create_usuarios_policies()
RETURNS void AS $$
BEGIN
    ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY "Usuarios pueden ver todos los usuarios" ON usuarios
    FOR SELECT
    TO authenticated
    USING (true);
    
    CREATE POLICY "Usuarios pueden crear nuevos usuarios" ON usuarios
    FOR INSERT
    TO authenticated
    WITH CHECK (true);
    
    CREATE POLICY "Usuarios pueden actualizar sus propios datos" ON usuarios
    FOR UPDATE
    TO authenticated
    USING (auth.uid()::text = correo);
    
    CREATE POLICY "Usuarios pueden eliminar sus propios datos" ON usuarios
    FOR DELETE
    TO authenticated
    USING (auth.uid()::text = correo);
END;
$$ LANGUAGE plpgsql;

-- Crear políticas RLS para materiales
CREATE OR REPLACE FUNCTION create_materiales_policies()
RETURNS void AS $$
BEGIN
    ALTER TABLE materiales ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY "Usuarios pueden ver todos los materiales" ON materiales
    FOR SELECT
    TO authenticated
    USING (true);
    
    CREATE POLICY "Administradores pueden crear nuevos materiales" ON materiales
    FOR INSERT
    TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
    
    CREATE POLICY "Administradores pueden actualizar materiales" ON materiales
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
    
    CREATE POLICY "Administradores pueden eliminar materiales" ON materiales
    FOR DELETE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
END;
$$ LANGUAGE plpgsql;

-- Crear políticas RLS para préstamos
CREATE OR REPLACE FUNCTION create_prestamos_policies()
RETURNS void AS $$
BEGIN
    ALTER TABLE prestamos ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY "Usuarios pueden ver sus propios préstamos" ON prestamos
    FOR SELECT
    USING (
        id_usuario = auth.uid()
    );

    CREATE POLICY "Administradores pueden ver todos los préstamos" ON prestamos
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.id_usuario = auth.uid() 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
    
    CREATE POLICY "Usuarios pueden crear préstamos" ON prestamos
    FOR INSERT
    TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
        )
    );
    
    CREATE POLICY "Usuarios pueden actualizar sus propios préstamos" ON prestamos
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.id_usuario = prestamos.id_usuario
        )
    );
    
    CREATE POLICY "Administradores pueden actualizar cualquier préstamo" ON prestamos
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
    
    CREATE POLICY "Administradores pueden eliminar préstamos" ON prestamos
    FOR DELETE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.correo = auth.uid()::text 
            AND usuarios.tipo_usuario = 'administrador'
        )
    );
END;
$$ LANGUAGE plpgsql;
