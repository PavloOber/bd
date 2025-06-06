document.addEventListener('DOMContentLoaded', () => {
    // Botones principales
    const listarMaterialesBtn = document.getElementById('listar-materiales-btn');
    const listarUsuariosBtn = document.getElementById('listar-usuarios-btn');
    const listarPrestamosBtn = document.getElementById('listar-prestamos-btn');
    const agregarMaterialBtn = document.getElementById('agregar-material-btn');
    const agregarUsuarioBtn = document.getElementById('agregar-usuario-btn');
    const agregarPrestamoBtn = document.getElementById('agregar-prestamo-btn');
    const agregarResenaBtn = document.getElementById('agregar-resena-btn');
    
    // Formularios
    const formularios = document.getElementById('formularios');
    const formMaterial = document.getElementById('form-material');
    const formUsuario = document.getElementById('form-usuario');
    const formPrestamo = document.getElementById('form-prestamo');
    const formResena = document.getElementById('form-resena');
    
    // Botones de guardar
    const guardarMaterialBtn = document.getElementById('guardar-material');
    const guardarUsuarioBtn = document.getElementById('guardar-usuario');
    const guardarPrestamoBtn = document.getElementById('guardar-prestamo');
    const guardarResenaBtn = document.getElementById('guardar-resena');
    
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
    
    // Elementos de reseñas
    const resenaMaterial = document.getElementById('resena-material');
    const resenaUsuario = document.getElementById('resena-usuario');
    const resenaCalificacion = document.getElementById('resena-calificacion');
    const resenaComentario = document.getElementById('resena-comentario');
    const resenasContainer = document.getElementById('resenas-container');
    
    // Configuración de la API
    const API_MONGO_URL = 'http://localhost:5000/api';    // Para MongoDB (reseñas)
    const API_SUPABASE_URL = 'http://localhost:5001/api'; // Para FastAPI (resto de datos)
    const responseDataEl = document.getElementById('response-data');
    
    // Variables para almacenar datos
    let materiales = [];
    let usuarios = [];
    
    // Función auxiliar para mostrar errores
    const showError = (error) => {
        console.error('Error:', error);
        responseDataEl.textContent = `Error: ${error.message}`;
    };
    
    // Función para mostrar datos en una tabla
    const mostrarDatosEnTabla = (data, titulo) => {
        responseDataEl.innerHTML = '';
        
        if (!Array.isArray(data) || data.length === 0) {
            responseDataEl.innerHTML = `<p>No hay ${titulo.toLowerCase()} disponibles.</p>`;
            return;
        }
        
        const table = document.createElement('table');
        table.className = 'data-table';
        
        // Crear encabezado
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        // Obtener columnas del primer objeto
        const columnas = Object.keys(data[0]);
        
        columnas.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Crear cuerpo de la tabla
        const tbody = document.createElement('tbody');
        
        data.forEach(item => {
            const row = document.createElement('tr');
            
            columnas.forEach(col => {
                const cell = document.createElement('td');
                let value = item[col];
                
                if (col.includes('fecha') || col.includes('fecha_')) {
                    try {
                        value = new Date(value).toLocaleDateString();
                    } catch (e) {
                        // Mantener valor original si no es fecha
                    }
                }
                
                cell.textContent = value ?? '-';
                row.appendChild(cell);
            });
            
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        responseDataEl.innerHTML = `<h3>${titulo}</h3>`;
        responseDataEl.appendChild(table);
        
        // Agregar estilos inline para evitar problemas con CSS externo
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';
        table.style.marginTop = '1rem';
        
        const thCells = table.querySelectorAll('th');
        const tdCells = table.querySelectorAll('td');
        
        thCells.forEach(th => {
            th.style.border = '1px solid #ddd';
            th.style.padding = '8px';
            th.style.textAlign = 'left';
            th.style.backgroundColor = '#f2f2f2';
            th.style.fontWeight = 'bold';
        });
        
        tdCells.forEach(td => {
            td.style.border = '1px solid #ddd';
            td.style.padding = '8px';
            td.style.textAlign = 'left';
        });
        
        const rows = table.querySelectorAll('tr');
        rows.forEach((row, index) => {
            if (index % 2 === 0) {
                row.style.backgroundColor = '#f9f9f9';
            }
            row.addEventListener('mouseover', () => {
                row.style.backgroundColor = '#f1f1f1';
            });
            row.addEventListener('mouseout', () => {
                row.style.backgroundColor = index % 2 === 0 ? '#f9f9f9' : '';
            });
        });
    };

    // Función para mostrar campos específicos según tipo de material
    const mostrarCamposEspecificos = (tipo) => {
        const camposLibro = document.getElementById('campos-libro');
        const camposRevista = document.getElementById('campos-revista');
        const camposDvd = document.getElementById('campos-dvd');
        
        camposLibro.style.display = tipo === 'libro' ? 'block' : 'none';
        camposRevista.style.display = tipo === 'revista' ? 'block' : 'none';
        camposDvd.style.display = tipo === 'dvd' ? 'block' : 'none';
        
        // Habilitar/deshabilitar botón según selección
        guardarMaterialBtn.disabled = !tipo;
    };

    // Añadir evento al select de tipo de material
    materialTipo.addEventListener('change', (e) => {
        mostrarCamposEspecificos(e.target.value);
    });

    // Función para mostrar formularios
    const mostrarFormulario = (formulario) => {
        formularios.style.display = 'block';
        formulario.style.display = 'block';
    };
    
    // Función para cargar datos para formularios
    const cargarMaterialesYUsuarios = async () => {
        try {
            // Cargar materiales
            const materialesRes = await fetch(`${API_SUPABASE_URL}/materiales`);
            if (materialesRes.ok) {
                const data = await materialesRes.json();
                materiales = data;
                actualizarSelectMateriales();
                actualizarSelectPrestamoMateriales();
            } else {
                throw new Error(`Error al cargar materiales: ${materialesRes.status}`);
            }
            
            // Cargar usuarios
            const usuariosRes = await fetch(`${API_SUPABASE_URL}/usuarios`);
            if (usuariosRes.ok) {
                const data = await usuariosRes.json();
                console.log('Datos de usuarios recibidos:', data); // Depuración
                usuarios = data;
                actualizarSelectUsuarios();
                actualizarSelectPrestamoUsuarios();
            } else {
                throw new Error(`Error al cargar usuarios: ${usuariosRes.status}`);
            }
        } catch (error) {
            console.error('Error al cargar datos:', error);
            showError(error);
        }
    };
    
    // Actualizar selects de reseñas
    const actualizarSelectMateriales = () => {
        resenaMaterial.innerHTML = '<option value="">Seleccione un material</option>';
        materiales.forEach(material => {
            const option = document.createElement('option');
            option.value = material.codigo_inventario;
            option.textContent = `${material.titulo} (${material.codigo_inventario})`;
            resenaMaterial.appendChild(option);
        });
    };
    
    const actualizarSelectUsuarios = () => {
        console.log('Actualizando select de usuarios con datos:', usuarios); // Depuración
        resenaUsuario.innerHTML = '<option value="">Seleccione un usuario</option>';
        
        if (!Array.isArray(usuarios)) {
            console.error('Error: usuarios no es un array:', usuarios);
            return;
        }
        
        usuarios.forEach(usuario => {
            try {
                const option = document.createElement('option');
                // Usar las propiedades con prefijo _Usuario__
                const id = usuario._Usuario__id_usuario || usuario.id_usuario || usuario.id;
                const nombre = usuario._Usuario__nombre || usuario.nombre || 'Sin nombre';
                const correo = usuario._Usuario__correo || usuario.correo || 'sin correo';
                
                option.value = id;
                option.textContent = `${nombre} (${correo})`;
                resenaUsuario.appendChild(option);
            } catch (error) {
                console.error('Error al procesar usuario:', usuario, error);
            }
        });
    };
    
    // Actualizar selects de préstamos
    const actualizarSelectPrestamoMateriales = () => {
        prestamoMaterial.innerHTML = '<option value="">Seleccione un material</option>';
        materiales.forEach(material => {
            const option = document.createElement('option');
            option.value = material.codigo_inventario;
            option.textContent = `${material.titulo} (${material.codigo_inventario})`;
            prestamoMaterial.appendChild(option);
        });
    };
    
    const actualizarSelectPrestamoUsuarios = () => {
        prestamoUsuario.innerHTML = '<option value="">Seleccione un usuario</option>';
        usuarios.forEach(usuario => {
            const option = document.createElement('option');
            option.value = usuario.id;
            option.textContent = `${usuario.nombre} (${usuario.correo})`;
            prestamoUsuario.appendChild(option);
        });
    };
    
    // Función para mostrar reseñas
    const mostrarResenas = async () => {
        try {
            // Primero obtenemos todos los materiales
            const materialesRes = await fetch(`${API_SUPABASE_URL}/materiales`);
            if (!materialesRes.ok) {
                throw new Error(`Error al cargar materiales: ${materialesRes.status}`);
            }
            const materiales = await materialesRes.json();
            
            // Obtenemos las reseñas de cada material
            let todasLasResenas = [];
            for (const material of materiales) {
                try {
                    // Agregar timestamp para evitar caché
                    const timestamp = new Date().getTime();
                    const res = await fetch(`${API_MONGO_URL}/materiales/${material.codigo_inventario}/resenas?_=${timestamp}`, {
                        method: 'GET',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    // Si el estado es 404, simplemente continuamos con el siguiente material
                    if (res.status === 404) {
                        continue;
                    }
                    
                    // Si hay otro error, lo registramos pero continuamos
                    if (!res.ok) {
                        console.warn(`Error al cargar reseñas para ${material.codigo_inventario}:`, res.status);
                        continue;
                    }
                    
                    // Si llegamos aquí, la petición fue exitosa
                    const resenasMaterial = await res.json();
                    
                    // Asegurarse de que resenasMaterial sea un array antes de usar spread
                    if (Array.isArray(resenasMaterial)) {
                        todasLasResenas = [...todasLasResenas, ...resenasMaterial];
                    } else {
                        console.warn(`Respuesta inesperada para ${material.codigo_inventario}:`, resenasMaterial);
                    }
                } catch (error) {
                    // Solo mostramos errores que no sean 404
                    if (error.message !== 'Failed to fetch' || !error.message.includes('404')) {
                        console.error(`Error al cargar reseñas para ${material.codigo_inventario}:`, error);
                    }
                }
            }
            
            resenasContainer.innerHTML = '';
            const resenas = todasLasResenas;
            
            if (resenas.length === 0) {
                resenasContainer.innerHTML = '<p>No hay reseñas disponibles.</p>';
                return;
            }
            
            const table = document.createElement('table');
            table.className = 'data-table';
            
            // Crear encabezado
            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th>Material</th>
                    <th>Usuario</th>
                    <th>Calificación</th>
                    <th>Comentario</th>
                    <th>Fecha</th>
                </tr>
            `;
            
            // Crear cuerpo
            const tbody = document.createElement('tbody');
            
            resenas.forEach(resena => {
                const material = materiales.find(m => m.codigo_inventario === resena.codigo_inventario) || {};
                const usuario = usuarios.find(u => u.id === resena.usuario_id) || {};
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${material.titulo || resena.codigo_inventario}</td>
                    <td>${usuario.nombre || resena.usuario_id}</td>
                    <td>${'★'.repeat(resena.calificacion)}${'☆'.repeat(5 - resena.calificacion)}</td>
                    <td>${resena.comentario || 'Sin comentario'}</td>
                    <td>${new Date(resena.fecha).toLocaleDateString()}</td>
                `;
                tbody.appendChild(tr);
            });
            
            table.appendChild(thead);
            table.appendChild(tbody);
            resenasContainer.appendChild(table);
            
        } catch (error) {
            console.error('Error al cargar reseñas:', error);
            resenasContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    };
    
    // Función para enviar reseña
    const enviarResena = async () => {
        try {
            const resenaData = {
                codigo_inventario: resenaMaterial.value,
                usuario_id: resenaUsuario.value,
                calificacion: parseInt(resenaCalificacion.value),
                comentario: resenaComentario.value
            };
            
            const response = await fetch(`${API_MONGO_URL}/resenas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(resenaData),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al guardar la reseña');
            }
            
            formResena.reset();
            alert('Reseña guardada correctamente');
            mostrarResenas();
            
        } catch (error) {
            console.error('Error al enviar reseña:', error);
            alert(`Error: ${error.message}`);
        }
    };
    
    // Evento para guardar reseña
    guardarResenaBtn.addEventListener('click', (e) => {
        e.preventDefault();
        enviarResena();
    });
    
    // Manejar pestañas
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const tabId = button.getAttribute('data-tab');
            document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            if (tabId === 'resenas') {
                mostrarResenas();
            }
        });
    });
    
    // Inicialización
    const inicializar = async () => {
        try {
            await cargarMaterialesYUsuarios();
            mostrarCamposEspecificos(materialTipo.value);
        } catch (error) {
            console.error('Error al inicializar:', error);
        }
    };
    
    // Función para ocultar formularios
    const ocultarFormularios = () => {
        formularios.style.display = 'none';
        formMaterial.style.display = 'none';
        formUsuario.style.display = 'none';
        formPrestamo.style.display = 'none';
        formResena.style.display = 'none';
    };

    // Eventos de botones principales
    agregarMaterialBtn.addEventListener('click', () => {
        ocultarFormularios();
        if (formMaterial) formMaterial.reset();
        mostrarCamposEspecificos(materialTipo.value);
        mostrarFormulario(formMaterial);
    });
    
    agregarUsuarioBtn.addEventListener('click', () => {
        ocultarFormularios();
        formUsuario.reset();
        mostrarFormulario(formUsuario);
    });
    
    agregarPrestamoBtn.addEventListener('click', () => {
        ocultarFormularios();
        formPrestamo.reset();
        mostrarFormulario(formPrestamo);
    });
    
    agregarResenaBtn.addEventListener('click', () => {
        ocultarFormularios();
        formResena.reset();
        mostrarFormulario(formResena);
    });

    // Eventos de listar datos
    listarMaterialesBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_SUPABASE_URL}/materiales`);
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            const data = await response.json();
            mostrarDatosEnTabla(data, 'Materiales');
        } catch (error) {
            showError(error);
        }
    });

    listarUsuariosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_SUPABASE_URL}/usuarios`);
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            const data = await response.json();
            mostrarDatosEnTabla(data, 'Usuarios');
        } catch (error) {
            showError(error);
        }
    });

    listarPrestamosBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_SUPABASE_URL}/prestamos`);
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            const data = await response.json();
            mostrarDatosEnTabla(data, 'Préstamos');
        } catch (error) {
            showError(error);
        }
    });
    
    // Validaciones
    const validarCamposUsuario = () => {
        if (!usuarioNombre.value.trim()) throw new Error('El nombre es requerido');
        if (!usuarioCorreo.value.trim()) throw new Error('El correo es requerido');
        if (!usuarioTipo.value) throw new Error('Seleccione un tipo de usuario');
        
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoRegex.test(usuarioCorreo.value)) {
            throw new Error('Correo electrónico inválido');
        }
    };

    const validarCamposMaterial = () => {
        const camposRequeridos = [
            { campo: materialTitulo, nombre: 'título' },
            { campo: materialAutor, nombre: 'autor' },
            { campo: materialCodigoInventario, nombre: 'código de inventario' },
            { campo: materialUbicacion, nombre: 'ubicación' },
            { campo: materialTipo, nombre: 'tipo de material' }
        ];
        
        camposRequeridos.forEach(({ campo, nombre }) => {
            if (!campo.value.trim()) throw new Error(`El ${nombre} es requerido`);
        });

        switch (materialTipo.value) {
            case 'libro':
                if (!materialNumPaginas.value.trim()) throw new Error('Número de páginas requerido');
                break;
            case 'revista':
                if (!materialNumEdicion.value.trim()) throw new Error('Número de edición requerido');
                if (!materialFechaPublicacion.value.trim()) throw new Error('Fecha de publicación requerida');
                break;
            case 'dvd':
                if (!materialDuracion.value.trim()) throw new Error('Duración requerida');
                if (!materialFormato.value.trim()) throw new Error('Formato requerido');
                break;
        }
    };

    // Guardar material
    guardarMaterialBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            validarCamposMaterial();
            
            const materialData = {
                codigo_inventario: materialCodigoInventario.value,
                titulo: materialTitulo.value,
                autor: materialAutor.value,
                tipo: materialTipo.value,
                disponible: true,
                ubicacion: materialUbicacion.value
            };

            switch (materialTipo.value) {
                case 'libro':
                    materialData.num_paginas = parseInt(materialNumPaginas.value);
                    break;
                case 'revista':
                    materialData.numero_edicion = materialNumEdicion.value;
                    materialData.fecha_publicacion = materialFechaPublicacion.value;
                    break;
                case 'dvd':
                    materialData.duracion = parseInt(materialDuracion.value);
                    materialData.formato = materialFormato.value;
                    break;
            }

            const response = await fetch(`${API_SUPABASE_URL}/materiales`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(materialData),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al guardar el material');
            }
            
            formMaterial.reset();
            alert('Material guardado correctamente');
            ocultarFormularios();
            
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });

    // Guardar usuario
    guardarUsuarioBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            validarCamposUsuario();
            
            const userData = {
                nombre: usuarioNombre.value.trim(),
                correo: usuarioCorreo.value.trim(),
                tipo_usuario: usuarioTipo.value
            };

            const response = await fetch(`${API_SUPABASE_URL}/usuarios`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al guardar el usuario');
            }
            
            formUsuario.reset();
            alert('Usuario guardado correctamente');
            ocultarFormularios();
            
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });

    // Guardar préstamo
    guardarPrestamoBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            if (!prestamoMaterial.value) throw new Error('Seleccione un material');
            if (!prestamoUsuario.value) throw new Error('Seleccione un usuario');
            if (!prestamoFechaPrestamo.value) throw new Error('Fecha de préstamo requerida');

            const prestamoData = {
                material: prestamoMaterial.value,
                usuario: prestamoUsuario.value,
                fecha_prestamo: prestamoFechaPrestamo.value,
                fecha_devolucion: prestamoFechaDevolucion.value || null
            };

            const response = await fetch(`${API_SUPABASE_URL}/prestamos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(prestamoData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al registrar el préstamo');
            }
            
            formPrestamo.reset();
            alert('Préstamo registrado correctamente');
            ocultarFormularios();
            
        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });

    // Inicializar aplicación
    inicializar();
});