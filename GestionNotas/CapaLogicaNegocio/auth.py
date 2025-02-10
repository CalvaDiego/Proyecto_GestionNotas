import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Usuario

# Cargar variables de entorno
load_dotenv()

# Claves y configuraciones para JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def crear_token_jwt(data: dict, completado: bool):
    """
    Genera un token JWT con los datos proporcionados.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "completado": completado})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_jwt(token: str, db: Session):
    """
    Verifica la validez de un token JWT y devuelve el usuario asociado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise ValueError("Token inválido.")
        usuario = db.query(Usuario).filter_by(correo=correo).first()
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario
    except JWTError:
        raise ValueError("Token inválido o expirado.")
