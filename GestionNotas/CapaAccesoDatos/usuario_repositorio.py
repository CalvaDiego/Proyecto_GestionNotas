from sqlalchemy.orm import Session
from CapaBaseDatos.models import Usuario

def obtener_usuario_por_correo(db: Session, correo: str):
    """
    Consulta si un usuario con el correo proporcionado ya existe en la base de datos.
    """
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def guardar_usuario(db: Session, datos_usuario):
    """
    Inserta un nuevo usuario en la base de datos.
    """
    nuevo_usuario = Usuario(
        nombre=datos_usuario["nombre"],
        apellido=datos_usuario["apellido"],
        correo=datos_usuario["correo"],
        contraseña=datos_usuario["contraseña"]
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario
