from sqlalchemy.orm import Session
from CapaBaseDatos.models import Institucion, Grado

def guardar_institucion(db: Session, nombre: str, lugar: str, imagen: bytes, id_usuario: int):
    nueva_institucion = Institucion(
        nombre=nombre,
        lugar=lugar,
        imagen_institucion=imagen,
        id_usuario=id_usuario
    )
    db.add(nueva_institucion)
    db.commit()
    db.refresh(nueva_institucion)
    return nueva_institucion.id_institucion

def guardar_grado(db: Session, nombre_grado: str, institucion_id: int):
    nuevo_grado = Grado(
        nombre=nombre_grado,
        id_institucion=institucion_id
    )
    db.add(nuevo_grado)
    db.commit()