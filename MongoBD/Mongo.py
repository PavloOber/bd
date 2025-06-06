import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from flasgger import Swagger, swag_from
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Inicializar app
app = Flask(__name__)

# Configuración CORS
def configure_cors(app):
    # Configuración básica de CORS
    CORS(app, 
         resources={
             r"/*": {
                 "origins": "*",
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
                 "supports_credentials": True,
                 "expose_headers": ["Content-Type", "Authorization"],
                 "max_age": 600  # Tiempo de caché para preflight requests (en segundos)
             }
         })

    # Manejador para solicitudes OPTIONS (preflight)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({"status": "preflight"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '600')
            return response

    # Headers CORS para todas las respuestas
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '600')
        return response

# Inicializar CORS
configure_cors(app)

# Configuración de Swagger
swagger_config = {
    'swagger': '2.0',
    'info': {
        'title': 'API de Reseñas',
        'description': 'API para gestionar reseñas de materiales',
        'version': '1.0.0',
        'contact': {
            'name': 'Soporte',
            'email': 'soporte@example.com'
        }
    },
    'schemes': ['http', 'https'],
    'consumes': [
        'application/json',
        'application/x-www-form-urlencoded',
        'multipart/form-data'
    ],
    'produces': ['application/json'],
    'securityDefinitions': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type the API key in the input: Bearer &lt;JWT&gt;'
        }
    },
    'security': [
        {
            'api_key': []
        }
    ]
}

# Configuración de la interfaz de Swagger
app.config['SWAGGER'] = {
    'title': 'API de Reseñas',
    'uiversion': 3,
    'specs_route': '/apidocs/',
    'static_url_path': '/flasgger_static'
}

# Inicializar Swagger
swagger = Swagger(app, template=swagger_config)

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DB_NAME")]
resenas = db["resenas"]

# Crear índice para búsquedas más rápidas
resenas.create_index("codigo_inventario")


@app.route('/api/materiales', methods=['GET', 'OPTIONS'])
def obtener_materiales():
    """
    Obtiene la lista de materiales disponibles
    ---
    tags:
      - Materiales
    responses:
      200:
        description: Lista de materiales
        schema:
          type: array
          items:
            type: object
            properties:
              codigo_inventario:
                type: string
                description: Código único del material
                example: "MAT-001"
              titulo:
                type: string
                description: Título del material
                example: "Introducción a Python"
      500:
        description: Error del servidor
    """
    try:
        # Obtener materiales de Supabase
        response = supabase.table('materiales').select('codigo_inventario, titulo').execute()
        materiales = response.data if hasattr(response, 'data') else []
        return jsonify([{"codigo_inventario": m['codigo_inventario'], "titulo": m['titulo']} for m in materiales])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/usuarios', methods=['GET', 'OPTIONS'])
def obtener_usuarios():
    """
    Obtiene la lista de usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            type: object
            properties:
              id_usuario:
                type: string
                description: ID único del usuario
                example: "USR001"
              nombre:
                type: string
                description: Nombre del usuario
                example: "Juan Pérez"
      500:
        description: Error del servidor
    """
    try:
        # Obtener usuarios de Supabase (ajusta según tu esquema de usuarios)
        response = supabase.table('usuarios').select('id_usuario, nombre').execute()
        usuarios = response.data if hasattr(response, 'data') else []
        return jsonify([{"id_usuario": u['id_usuario'], "nombre": u['nombre']} for u in usuarios])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/resenas', methods=['GET', 'POST', 'OPTIONS'])
def crear_resena():
    """
    Crea una nueva reseña para un material
    ---
    tags:
      - Reseñas
    consumes:
      - application/x-www-form-urlencoded
      - multipart/form-data
    parameters:
      - name: codigo_inventario
        in: formData
        type: string
        required: true
        description: Código de inventario del material
        schema:
          type: string
      - name: usuario_id
        in: formData
        type: string
        required: true
        description: ID del usuario
        schema:
          type: string
      - name: calificacion
        in: formData
        type: integer
        required: true
        description: Calificación del 1 al 5
        minimum: 1
        maximum: 5
        schema:
          type: integer
          minimum: 1
          maximum: 5
      - name: comentario
        in: formData
        type: string
        required: true
        description: Comentario sobre el material (entre 10 y 500 caracteres)
        minLength: 10
        maxLength: 500
        schema:
          type: string
          minLength: 10
          maxLength: 500
    responses:
      201:
        description: Reseña creada exitosamente
        schema:
          type: object
          properties:
            mensaje:
              type: string
              example: "Reseña creada exitosamente"
            id_resena:
              type: string
              example: "507f1f77bcf86cd799439011"
      400:
        description: Datos inválidos o faltantes
      404:
        description: Material no encontrado en Supabase
      500:
        description: Error interno del servidor
    """
    if request.method == 'GET':
        """
        Muestra el formulario para crear una nueva reseña
        ---
        responses:
          200:
            description: Formulario HTML para crear una reseña
            content:
              text/html:
                schema:
                  type: string
        """
        try:
            # Obtener materiales de Supabase
            materiales_resp = supabase.table('materiales').select('codigo_inventario, titulo').execute()
            materiales = materiales_resp.data if hasattr(materiales_resp, 'data') else []
            
            # Obtener usuarios de Supabase
            usuarios_resp = supabase.table('usuarios').select('id_usuario, nombre').execute()
            usuarios = usuarios_resp.data if hasattr(usuarios_resp, 'data') else []
            
            # Crear opciones para los selects
            opciones_materiales = [(m['codigo_inventario'], m['titulo']) for m in materiales]
            opciones_usuarios = [(u['id_usuario'], u['nombre']) for u in usuarios]
            
            # Retornar el formulario HTML con las opciones
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Crear Nueva Reseña</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .form-group {{ margin-bottom: 15px; }}
                    label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                    select, input[type="number"], textarea {{ 
                        width: 100%; 
                        padding: 8px; 
                        margin-bottom: 10px; 
                        border: 1px solid #ddd; 
                        border-radius: 4px; 
                        box-sizing: border-box;
                    }}
                    textarea {{ height: 100px; resize: vertical; }}
                    button {{ 
                        background-color: #4CAF50; 
                        color: white; 
                        padding: 10px 15px; 
                        border: none; 
                        border-radius: 4px; 
                        cursor: pointer; 
                        font-size: 16px;
                    }}
                    button:hover {{ background-color: #45a049; }}
                </style>
            </head>
            <body>
                <h2>Crear Nueva Reseña</h2>
                <form method="POST" action="/api/resenas">
                    <div class="form-group">
                        <label for="codigo_inventario">Material:</label>
                        <select id="codigo_inventario" name="codigo_inventario" required>
                            {' '.join(f'<option value="{codigo}">{titulo} ({codigo})</option>' for codigo, titulo in opciones_materiales)}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="usuario_id">Usuario:</label>
                        <select id="usuario_id" name="usuario_id" required>
                            {' '.join(f'<option value="{id_user}">{nombre} ({id_user})</option>' for id_user, nombre in opciones_usuarios)}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="calificacion">Calificación (1-5):</label>
                        <input type="number" id="calificacion" name="calificacion" min="1" max="5" value="5" required>
                    </div>
                    <div class="form-group">
                        <label for="comentario">Comentario (10-500 caracteres):</label>
                        <textarea id="comentario" name="comentario" required minlength="10" maxlength="500"></textarea>
                    </div>
                    <button type="submit">Enviar reseña</button>
                </form>
            </body>
            </html>
            """, 200
        except Exception as e:
            return f"Error al cargar el formulario: {str(e)}", 500
    
    # Procesar el formulario enviado por POST
    try:
        # Obtener datos del formulario o JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'codigo_inventario': request.form.get('codigo_inventario'),
                'usuario_id': request.form.get('usuario_id'),
                'calificacion': int(request.form.get('calificacion')),
                'comentario': request.form.get('comentario')
            }
        
        # Validar datos
        if not all(data.values()):
            return jsonify({"error": "Todos los campos son requeridos"}), 400
            
        if data['calificacion'] < 1 or data['calificacion'] > 5:
            return jsonify({"error": "La calificación debe estar entre 1 y 5"}), 400
            
        if len(data['comentario']) < 10 or len(data['comentario']) > 500:
            return jsonify({"error": "El comentario debe tener entre 10 y 500 caracteres"}), 400
            
    except Exception as e:
        app.logger.error(f"Error al procesar los datos: {str(e)}")
        return jsonify({"error": "Error al procesar los datos: " + str(e)}), 400
    
    try:
        # Verificar si el material existe en Supabase
        material_resp = supabase.table('materiales').select('*').eq('codigo_inventario', data['codigo_inventario']).execute()
        if not hasattr(material_resp, 'data') or not material_resp.data:
            return jsonify({"error": "Material no encontrado"}), 404
            
        # Insertar reseña en MongoDB
        result = resenas.insert_one({
            'codigo_inventario': data['codigo_inventario'],
            'usuario_id': data['usuario_id'],
            'calificacion': data['calificacion'],
            'comentario': data['comentario'],
            'fecha_creacion': datetime.utcnow()
        })
        
        return jsonify({
            "mensaje": "Reseña creada exitosamente",
            "id_resena": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/materiales/<codigo_inventario>/resenas', methods=['GET'])
def obtener_resenas(codigo_inventario):
    """
    Obtiene todas las reseñas de un material
    ---
    tags:
      - Reseñas
    parameters:
      - name: codigo_inventario
        in: path
        type: string
        required: true
        description: Código de inventario del material
        example: "MAT-001"
    responses:
      200:
        description: Lista de reseñas del material
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: ID único de la reseña
                example: "507f1f77bcf86cd799439011"
              codigo_inventario:
                type: string
                description: Código de inventario del material
                example: "MAT-001"
              usuario_id:
                type: string
                description: ID del usuario que hizo la reseña
                example: "USR001"
              calificacion:
                type: integer
                description: Calificación del 1 al 5
                example: 5
              comentario:
                type: string
                description: Comentario de la reseña
                example: "Excelente material, muy útil"
              fecha_creacion:
                type: string
                format: date-time
                description: Fecha de creación de la reseña
                example: "2025-06-05T11:07:21.106000"
      404:
        description: No se encontraron reseñas para el material
      500:
        description: Error del servidor
    """
    try:
        # Obtener reseñas de MongoDB
        cursor = resenas.find({"codigo_inventario": codigo_inventario}).sort("fecha_creacion", -1)
        resenas_list = []
        
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            doc['fecha_creacion'] = doc['fecha_creacion'].isoformat()
            resenas_list.append(doc)
            
        if not resenas_list:
            return jsonify({"error": "No se encontraron reseñas para este material"}), 404
            
        return jsonify(resenas_list)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/materiales/<codigo_inventario>/estadisticas', methods=['GET'])
def obtener_estadisticas(codigo_inventario):
    """
    Obtiene estadísticas de las reseñas de un material
    ---
    tags:
      - Estadísticas
    parameters:
      - name: codigo_inventario
        in: path
        type: string
        required: true
        description: Código de inventario del material
        example: "MAT-001"
    responses:
      200:
        description: Estadísticas de las reseñas
        schema:
          type: object
          properties:
            codigo_inventario:
              type: string
              description: Código de inventario del material
              example: "MAT-001"
            total_resenas:
              type: integer
              description: Número total de reseñas
              example: 5
            promedio_calificacion:
              type: number
              format: float
              description: Promedio de calificaciones (1-5)
              example: 4.2
            distribucion_calificaciones:
              type: object
              description: Número de reseñas por calificación (1-5)
              example: {"1": 0, "2": 1, "3": 1, "4": 1, "5": 2}
      500:
        description: Error del servidor
    """
    try:
        pipeline = [
            {"$match": {"codigo_inventario": codigo_inventario}},
            {"$group": {
                "_id": "$codigo_inventario",
                "total_resenas": {"$sum": 1},
                "promedio_calificacion": {"$avg": "$calificacion"},
                "calificaciones": {"$push": "$calificacion"}
            }}
        ]
        
        result = list(resenas.aggregate(pipeline))
        
        if not result:
            return jsonify({
                "codigo_inventario": codigo_inventario,
                "total_resenas": 0,
                "promedio_calificacion": 0,
                "distribucion_calificaciones": {str(i): 0 for i in range(1, 6)}
            })
            
        # Calcular distribución de calificaciones
        calificaciones = result[0].get('calificaciones', [])
        distribucion = {str(i): calificaciones.count(i) for i in range(1, 6)}
        
        return jsonify({
            "codigo_inventario": result[0]['_id'],
            "total_resenas": result[0]['total_resenas'],
            "promedio_calificacion": round(result[0]['promedio_calificacion'], 2),
            "distribucion_calificaciones": distribucion
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/flasgger_static/<path:path>')
def send_static(path):
    return send_from_directory('flasgger_static', path)

@app.route('/swagger-ui-init.js')
def swagger_ui_init():
    return """
    window.onload = function() {
        // Inicializar Swagger UI
        const ui = SwaggerUIBundle({
            url: "/apispec_1.json",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
        });
        
        // Habilitar CORS
        window.ui = ui;
    }
    """, 200, {'Content-Type': 'application/javascript'}

if __name__ == "__main__":
    app.run(debug=True, port=5000)