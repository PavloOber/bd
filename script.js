document.addEventListener('DOMContentLoaded', () => {
    // Botones principales
    const listarMaterialesBtn = document.getElementById('listar-materiales-btn');
    const listarUsuariosBtn = document.getElementById('listar-usuarios-btn');
    const listarPrestamosBtn = document.getElementById('listar-prestamos-btn');
    const agregarMaterialBtn = document.getElementById('agregar-material-btn');
    const agregarUsuarioBtn = document.getElementById('agregar-usuario-btn');
    const agregarPrestamoBtn = document.getElementById('agregar-prestamo-btn');
    
    // Formularios
    const formularios = document.getElementById('formularios');
    const formMaterial = document.getElementById('form-material');
    const formUsuario = document.getElementById('form-usuario');
    const formPrestamo = document.getElementById('form-prestamo');
    
    // Botones de guardar
    const guardarMaterialBtn = document.getElementById('guardar-material');
    const guardarUsuarioBtn = document.getElementById('guardar-usuario');
    const guardarPrestamoBtn = document.getElementById('guardar-prestamo');
    
    // Campos de los formularios
    const materialTitulo = document.getElementById('material-titulo');
    const materialAutor = document.getElementById('material-autor');
    const materialCodigoInventario = document.getElementById('material-codigo-inventario');
    const materialUbicacion = document.getElementById('material-ubicacion');
    const materialTipo = document.getElementById('material-tipo');
    
    // Campos específicos por tipo
    const materialNumPaginas = document.getElementById('material-num-paginas');
    const materialNumEdicion = document.getElementById('material-num-edicion');
    const materialFechaPublicacion = document.getElementById('material-fecha-publicacion');
    const materialDuracion = document.getElementById('material-duracion');
    const materialFormato = document.getElementById('material-formato');
    
    const usuarioNombre = document.getElementById('usuario-nombre');
    const usuarioCorreo = document.getElementById('usuario-correo');
    const usuarioTipo = document.getElementById('usuario-tipo');
    
    const prestamoMaterial = document.getElementById('prestamo-material');
    const prestamoUsuario = document.getElementById('prestamo-usuario');
    const prestamoFechaPrestamo = document.getElementById('prestamo-fecha-prestamo');
    const prestamoFechaDevolucion = document.getElementById('prestamo-fecha-devolucion');
    
    // Configuración de la API y funciones auxiliares
    const API_BASE_URL = 'http://localhost:8000';
    const responseDataEl = document.getElementById('response-data');
    
    // Función auxiliar para mostrar errores
    const showError = (error) => {
        console.error('Error:', error);
        responseDataEl.textContent = `Error: ${error.message}`;
    };
    
    // Función auxiliar para mostrar formularios
    const mostrarFormulario = (formulario) => {
        formularios.style.display = 'block';
        formulario.style.display = 'block';
    };
    
    // Función auxiliar para ocultar formularios
    const ocultarFormularios = () => {
        formularios.style.display = 'none';
        formMaterial.style.display = 'none';
        formUsuario.style.display = 'none';
        formPrestamo.style.display = 'none';
    };

    // Eventos de botones principales
    agregarMaterialBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevenir cualquier comportamiento por defecto
        ocultarFormularios(); // Ocultar otros formularios
        mostrarFormulario(formMaterial);
    });
    
    agregarUsuarioBtn.addEventListener('click', () => {
        mostrarFormulario(formUsuario);
    });
    
    agregarPrestamoBtn.addEventListener('click', () => {
        mostrarFormulario(formPrestamo);
    });
    
    // Eventos de botones de guardar


    // Validar campos requeridos
    const validarCamposRequeridos = () => {
        const campos = [
            { campo: materialTitulo, nombre: 'Título' },
            { campo: materialAutor, nombre: 'Autor' },
            { campo: materialCodigoInventario, nombre: 'Código de inventario' },
            { campo: materialUbicacion, nombre: 'Ubicación' },
            { campo: materialTipo, nombre: 'Tipo' }
        ];

        for (const { campo, nombre } of campos) {
            if (!campo.value.trim()) {
                throw new Error(`El campo ${nombre} es requerido`);
            }
        }

        // Validar campos específicos según el tipo
        switch (materialTipo.value) {
            case 'libro':
                if (!materialNumPaginas.value.trim()) {
                    throw new Error('El número de páginas es requerido para libros');
                }
                break;
            case 'revista':
                if (!materialNumEdicion.value.trim()) {
                    throw new Error('El número de edición es requerido para revistas');
                }
                if (!materialFechaPublicacion.value.trim()) {
                    throw new Error('La fecha de publicación es requerida para revistas');
                }
                break;
            case 'dvd':
                if (!materialDuracion.value.trim()) {
                    throw new Error('La duración es requerida para DVDs');
                }
                if (!materialFormato.value.trim()) {
                    throw new Error('El formato es requerido para DVDs');
                }
                break;
        }
    };

    guardarMaterialBtn.addEventListener('click', async (e) => {
        // Solo continuar si el botón está habilitado
        if (guardarMaterialBtn.disabled) {
            return;
        }
        try {
            const tipo = materialTipo.value;
            if (!tipo) {
                throw new Error('Debe seleccionar un tipo de material');
            }

            const materialData = {
                codigo_inventario: materialCodigoInventario.value,
                titulo: materialTitulo.value,
                autor: materialAutor.value,
                tipo: tipo,
                disponible: true,
                ubicacion: materialUbicacion.value
            };

            // Agregar campos específicos según el tipo
            if (tipo === 'libro') {
                materialData.num_paginas = parseInt(materialNumPaginas.value) || null;
            } else if (tipo === 'revista') {
                materialData.numero_edicion = materialNumEdicion.value || null;
                materialData.fecha_publicacion = materialFechaPublicacion.value || null;
            } else if (tipo === 'dvd') {
                materialData.duracion = parseInt(materialDuracion.value) || null;
                materialData.formato = materialFormato.value || null;
            }

            const response = await fetch(`${API_BASE_URL}/materiales/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(materialData),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
            ocultarFormularios();
        } catch (error) {
            showError(error);
        }
    });
    
    guardarUsuarioBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/usuarios/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: usuarioNombre.value,
                    correo: usuarioCorreo.value,
                    tipo_usuario: usuarioTipo.value
                }),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
            ocultarFormularios();
        } catch (error) {
            showError(error);
        }
    });
    
    guardarPrestamoBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/prestamos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id_material: prestamoMaterial.value,
                    id_usuario: prestamoUsuario.value,
                    fecha_prestamo: prestamoFechaPrestamo.value,
                    fecha_devolucion: prestamoFechaDevolucion.value
                }),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
            ocultarFormularios();
        } catch (error) {
            showError(error);
        }
    });
    
    // Función para listar materiales
    listarMaterialesBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/materiales/`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            showError(error);
        }
    });

    // Función para listar usuarios
    listarUsuariosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/usuarios/`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error al obtener los usuarios:', error);
            responseDataEl.textContent = `Error: ${error.message}`;
        }
    });

    // Función para listar prestamos
    listarPrestamosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/prestamos/`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error al obtener los prestamos:', error);
            responseDataEl.textContent = `Error: ${error.message}`;
        }
    });

    // Función para agregar material
    agregarMaterialBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/materiales/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: 'Nuevo Material',
                    descripcion: 'Descripción del nuevo material',
                }),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error al agregar el material:', error);
            responseDataEl.textContent = `Error: ${error.message}`;
        }
    });

    // Función para agregar usuario
    agregarUsuarioBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/usuarios/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: 'Nuevo Usuario',
                    apellido: 'Apellido del nuevo usuario',
                    email: 'usuario@example.com',
                }),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error al agregar el usuario:', error);
            responseDataEl.textContent = `Error: ${error.message}`;
        }
    });

    // Función para agregar prestamo
    agregarPrestamoBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/prestamos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    material: 'Material 1',
                    usuario: 'Usuario 1',
                    fecha_prestamo: '2023-01-01',
                    fecha_devolucion: '2023-01-15',
                }),
            });
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error al agregar el prestamo:', error);
            responseDataEl.textContent = `Error: ${error.message}`;
        }
    });
});
