from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from database import Database
from models import MaterialBiblioteca, Usuario, Libro, Revista, DVD
from prestamo import Prestamo
from datetime import datetime

app = FastAPI(title="API Biblioteca")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear una instancia de la base de datos
db = Database()

# Modelos Pydantic para la API
class MaterialCreate(BaseModel):
    codigo_inventario: str
    titulo: str
    autor: str
    tipo: str
    disponible: bool
    ubicacion: str
    num_paginas: Optional[int] = None
    numero_edicion: Optional[str] = None
    fecha_publicacion: Optional[str] = None
    duracion: Optional[int] = None
    formato: Optional[str] = None

class UsuarioCreate(BaseModel):
    id_usuario: str
    nombre: str
    correo: str
    tipo_usuario: str

class PrestamoCreate(BaseModel):
    id_usuario: str
    codigo_inventario: str

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de la Biblioteca"}

# Endpoints para materiales
@app.post("/materiales/")
async def crear_material(material: MaterialCreate):
    try:
        # Crear el material según su tipo
        if material.tipo.lower() == "libro":
            nuevo_material = Libro(
                codigo_inventario=material.codigo_inventario,
                titulo=material.titulo,
                autor=material.autor,
                disponible=material.disponible,
                ubicacion=material.ubicacion,
                num_paginas=material.num_paginas
            )
        elif material.tipo.lower() == "revista":
            nuevo_material = Revista(
                codigo_inventario=material.codigo_inventario,
                titulo=material.titulo,
                autor=material.autor,
                disponible=material.disponible,
                ubicacion=material.ubicacion,
                numero_edicion=material.numero_edicion,
                fecha_publicacion=material.fecha_publicacion
            )
        else:  # DVD
            nuevo_material = DVD(
                codigo_inventario=material.codigo_inventario,
                titulo=material.titulo,
                autor=material.autor,
                disponible=material.disponible,
                ubicacion=material.ubicacion,
                duracion=material.duracion,
                formato=material.formato
            )

        if db.guardar_material(nuevo_material):
            return {"message": "Material creado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Error al crear el material")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/materiales/")
async def listar_materiales():
    try:
        materiales = db.obtener_materiales()
        return [m.to_dict() for m in materiales]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para usuarios
@app.post("/usuarios/")
async def crear_usuario(usuario: UsuarioCreate):
    try:
        nuevo_usuario = Usuario(
            id_usuario=usuario.id_usuario,
            nombre=usuario.nombre,
            correo=usuario.correo,
            tipo_usuario=usuario.tipo_usuario
        )
        if db.guardar_usuario(nuevo_usuario):
            return {"message": "Usuario creado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Error al crear el usuario")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usuarios/")
async def listar_usuarios():
    try:
        usuarios = db.obtener_usuarios()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints para préstamos
@app.post("/prestamos/")
async def crear_prestamo(prestamo: PrestamoCreate):
    try:
        nuevo_prestamo = Prestamo(
            codigo_inventario=prestamo.codigo_inventario,
            id_usuario=prestamo.id_usuario,
            fecha_prestamo=datetime.now(),
            fecha_devolucion=None
        )
        if db.guardar_prestamo(nuevo_prestamo):
            return {"message": "Préstamo creado exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="Error al crear el préstamo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prestamos/")
async def listar_prestamos():
    try:
        prestamos = db.obtener_prestamos()
        return prestamos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/prestamos/devolver/{codigo_inventario}")
async def devolver_prestamo(codigo_inventario: str):
    try:
        if db.devolver_prestamo(codigo_inventario):
            return {"message": "Préstamo devuelto exitosamente"}
        else:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
