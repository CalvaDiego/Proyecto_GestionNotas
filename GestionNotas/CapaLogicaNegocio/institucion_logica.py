from fastapi import UploadFile
from sqlalchemy.orm import Session
from CapaAccesoDatos.institucion_repositorio import guardar_institucion, guardar_grado

async def guardar_institucion_y_grados(db: Session, nombre: str, lugar: str, imagen: UploadFile, grados: list, id_usuario: int):
    # Leer la imagen
    imagen_data = await imagen.read()

    # Guardar la institución con el id_usuario
    institucion_id = guardar_institucion(db, nombre, lugar, imagen_data, id_usuario)

    # Guardar los grados asociados
    for nombre_grado in grados:
        guardar_grado(db, nombre_grado, institucion_id)