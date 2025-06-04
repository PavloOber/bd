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

    // Función para mostrar campos específicos según el tipo de material
    const mostrarCamposEspecificos = (tipo) => {
        const guardarBtn = document.getElementById('guardar-material');
        guardarBtn.disabled = !tipo;
        
        // Obtener los contenedores de campos específicos
        const camposLibro = document.getElementById('campos-libro');
        const camposRevista = document.getElementById('campos-revista');
        const camposDvd = document.getElementById('campos-dvd');
        
        // Mostrar/ocultar campos según el tipo seleccionado
        camposLibro.style.display = tipo === 'libro' ? 'block' : 'none';
        camposRevista.style.display = tipo === 'revista' ? 'block' : 'none';
        camposDvd.style.display = tipo === 'dvd' ? 'block' : 'none';
    };

    // Añadir el evento al select de tipo de material
    materialTipo.addEventListener('change', (e) => {
        mostrarCamposEspecificos(e.target.value);
    });

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
        e.preventDefault();
        ocultarFormularios();
        mostrarFormulario(formMaterial);
    });
    
    agregarUsuarioBtn.addEventListener('click', () => {
        ocultarFormularios();
        mostrarFormulario(formUsuario);
    });
    
    agregarPrestamoBtn.addEventListener('click', () => {
        ocultarFormularios();
        mostrarFormulario(formPrestamo);
    });

    // Eventos de botones de listar
    listarMaterialesBtn.addEventListener('click', async () => {
        try {
            console.log('Solicitando materiales...');
            const response = await fetch(`${API_BASE_URL}/materiales/`);
            console.log('Respuesta recibida:', response);
            console.log('Estado:', response.status);
            
            if (!response.ok) {
                console.error('Respuesta no OK:', response.statusText);
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Datos recibidos:', data);
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error completo:', error);
            showError(error);
        }
    });

    listarUsuariosBtn.addEventListener('click', async () => {
        try {
            console.log('Solicitando usuarios...');
            const response = await fetch(`${API_BASE_URL}/usuarios/`);
            console.log('Respuesta recibida:', response);
            console.log('Estado:', response.status);
            
            if (!response.ok) {
                console.error('Respuesta no OK:', response.statusText);
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Datos recibidos:', data);
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error completo:', error);
            showError(error);
        }
    });

    listarPrestamosBtn.addEventListener('click', async () => {
        try {
            console.log('Solicitando préstamos...');
            const response = await fetch(`${API_BASE_URL}/prestamos/`);
            console.log('Respuesta recibida:', response);
            console.log('Estado:', response.status);
            
            if (!response.ok) {
                console.error('Respuesta no OK:', response.statusText);
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Datos recibidos:', data);
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            console.error('Error completo:', error);
            showError(error);
        }
    });
    
    // Validar campos requeridos para usuarios
    const validarCamposUsuario = () => {
        const campos = [
            { campo: usuarioNombre, nombre: 'Nombre' },
            { campo: usuarioCorreo, nombre: 'Correo' },
            { campo: usuarioTipo, nombre: 'Tipo de usuario' }
        ];

        for (const { campo, nombre } of campos) {
            if (!campo.value.trim()) {
                throw new Error(`El campo ${nombre} es requerido`);
            }
        }

        // Validar correo
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoRegex.test(usuarioCorreo.value.trim())) {
            throw new Error('El correo electrónico no es válido');
        }

        // Validar tipo de usuario
        const tiposValidos = ['administrador', 'bibliotecario', 'usuario'];
        if (!tiposValidos.includes(usuarioTipo.value)) {
            throw new Error('Debe seleccionar un tipo de usuario válido');
        }
    };

    // Validar campos requeridos para materiales
    const validarCamposMaterial = () => {
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

    // Evento para guardar material
    guardarMaterialBtn.addEventListener('click', async (e) => {
        try {
            validarCamposMaterial();
            
            const tipo = materialTipo.value;
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
    
    // Evento para guardar usuario
    guardarUsuarioBtn.addEventListener('click', async () => {
        try {
            validarCamposUsuario();

            const userData = {
                nombre: usuarioNombre.value.trim(),
                correo: usuarioCorreo.value.trim(),
                tipo_usuario: usuarioTipo.value
            };

            const response = await fetch(`${API_BASE_URL}/usuarios/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
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

    // Evento para listar usuarios
    listarUsuariosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/usuarios/`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            showError(error);
        }
    });

    // Evento para listar materiales
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

    // Evento para listar préstamos
    listarPrestamosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/prestamos/`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            responseDataEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            showError(error);
        }
    });

    // Evento para guardar préstamo
    guardarPrestamoBtn.addEventListener('click', async () => {
        try {
            const prestamoData = {
                material: prestamoMaterial.value,
                usuario: prestamoUsuario.value,
                fecha_prestamo: prestamoFechaPrestamo.value,
                fecha_devolucion: prestamoFechaDevolucion.value
            };

            const response = await fetch(`${API_BASE_URL}/prestamos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(prestamoData),
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
});