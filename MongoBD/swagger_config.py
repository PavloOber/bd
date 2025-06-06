def swagger_config():
    return {
        'swagger': '2.0',
        'info': {
            'title': 'API de Reseñas',
            'description': 'API para gestionar reseñas de materiales',
            'version': '1.0.0',
        },
        'schemes': ['http'],
        'basePath': '/',
        'tags': [
            {
                'name': 'resenas',
                'description': 'Operaciones con reseñas'
            },
            {
                'name': 'materiales',
                'description': 'Consulta de materiales'
            },
            {
                'name': 'usuarios',
                'description': 'Consulta de usuarios'
            }
        ]
    }

def swagger_template():
    return {
        'swagger': '2.0',
        'info': {
            'title': 'API de Reseñas',
            'description': 'API para gestionar reseñas de materiales',
            'version': '1.0.0',
            'contact': {
                'name': 'Soporte API',
                'email': 'soporte@example.com'
            }
        },
        'schemes': ['http'],
        'consumes': ['application/json'],
        'produces': ['application/json'],
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        },
        'security': [
            {
                'Bearer': []
            }
        ]
    }
