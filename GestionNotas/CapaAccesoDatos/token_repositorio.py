from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from CapaBaseDatos.models import Token, Usuario

def guardar_token(db: Session, usuario_id: int, token: str):
    nuevo_token = Token(
        usuario_id=usuario_id,
        token=token,
        expiracion=datetime.utcnow() + timedelta(minutes=30)
    )
    db.add(nuevo_token)
    db.commit()

def validar_token(db: Session, token: str):
    token_db = db.query(Token).filter(Token.token == token).first()
    if token_db and token_db.expiracion > datetime.utcnow():
        return token_db.usuario_id
    return None

def actualizar_contrasena(db: Session, usuario_id: int, nueva_contrasena: str):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario:
        usuario.contraseña = nueva_contrasena
        db.commit()
