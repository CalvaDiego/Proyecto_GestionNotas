from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Usuario

class UsuarioRepositorio:
    @staticmethod
    def crear_usuario(db: Session, nombre: str, apellido: str, correo: str, contraseña: str, genero: str):
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=contraseña,
            genero=genero
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
