from fastapi import HTTPException
import secrets
from sqlalchemy.orm import Session
from CapaAccesoDatos.usuario_repositorio import guardar_usuario, obtener_usuario_por_correo
from CapaAccesoDatos.token_repositorio import guardar_token, validar_token, actualizar_contrasena
from passlib.hash import bcrypt

def registrar_usuario(db: Session, datos_usuario):
    # Verificar si el correo ya existe en la base de datos
    usuario_existente = obtener_usuario_por_correo(db, datos_usuario["correo"])
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Encriptar la contraseña
    datos_usuario["contraseña"] = bcrypt.hash(datos_usuario["contraseña"])

    # Guardar el usuario en la base de datos
    nuevo_usuario = guardar_usuario(db, datos_usuario)

    return {"id_usuario": nuevo_usuario.id_usuario, "correo": nuevo_usuario.correo}


def validar_credenciales(db: Session, correo: str, contraseña: str):
    # Obtener usuario por correo
    usuario = obtener_usuario_por_correo(db, correo)
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    # Verificar contraseña
    if not bcrypt.verify(contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    return usuario

def enviar_enlace_recuperacion(db: Session, correo: str):
    usuario = obtener_usuario_por_correo(db, correo)
    if not usuario:
        raise HTTPException(status_code=404, detail="El correo no está asociado a ninguna cuenta")

    # Generar un token único
    token = secrets.token_urlsafe(32)

    # Guardar el token en la base de datos
    guardar_token(db, usuario.id_usuario, token)

    # Aquí se simula el envío del enlace por correo (en un entorno real usarías una librería como `smtplib` o un servicio)
    enlace = f"http://127.0.0.1:8080/restablecer-contrasena/?token={token}"
    print(f"Enlace de recuperación enviado: {enlace}")

    return "Enlace de recuperación enviado al correo registrado."



def restablecer_contrasena(db: Session, token: str, nueva_contrasena: str):
    # Validar token
    usuario_id = validar_token(db, token)
    if not usuario_id:
        raise HTTPException(status_code=400, detail="El enlace de recuperación no es válido o ha expirado")

    # Validar requisitos de la nueva contraseña (mínimo 8 caracteres, por ejemplo)
    if len(nueva_contrasena) < 8:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")

    # Encriptar la nueva contraseña
    nueva_contrasena_encriptada = bcrypt.hash(nueva_contrasena)

    # Actualizar la contraseña en la base de datos
    actualizar_contrasena(db, usuario_id, nueva_contrasena_encriptada)

    return "Contraseña restablecida con éxito."