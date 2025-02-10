import bcrypt
import re
import requests
import secrets
import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Usuario, TokenRecuperacion

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class UsuarioLogica:

    @staticmethod
    def validar_genero(genero: str):
        # Verificar que el género sea uno de los valores permitidos
        generos_validos = ["Masculino", "Femenino"]
        if genero not in generos_validos:
            raise ValueError(f"El género es obligatorio y debe ser 'Masculino' o 'Femenino'.")


    @staticmethod
    def validar_nombre_apellido(campo: str, tipo_campo: str):
        # Verificar que tenga exactamente dos palabras
        if len(campo.split()) != 2:
            if tipo_campo == "nombre":
                raise ValueError("El nombre debe contener dos palabras (por ejemplo: Diego Armando).")
            elif tipo_campo == "apellido":
                raise ValueError("El apellido debe contener dos palabras (por ejemplo: Calva Chuquimarca).")

        # Verificar que cada palabra comience con mayúscula y contenga solo letras
        if not all(re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+$", palabra) for palabra in campo.split()):
            if tipo_campo == "nombre":
                raise ValueError("Cada palabra en el nombre debe comenzar con mayúscula y no contener caracteres inválidos.")
            elif tipo_campo == "apellido":
                raise ValueError("Cada palabra en el apellido debe comenzar con mayúscula y no contener caracteres inválidos.")

    @staticmethod
    def validar_contraseña(contraseña: str):
        # Longitud mínima
        if len(contraseña) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        # Longitud máxima
        if len(contraseña) > 64:
            raise ValueError("La contraseña no puede exceder los 64 caracteres.")
        # Al menos una letra mayúscula
        if not any(char.isupper() for char in contraseña):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula.")
        # Al menos una letra minúscula
        if not any(char.islower() for char in contraseña):
            raise ValueError("La contraseña debe tener al menos una letra minúscula.")
        # Al menos un número
        if not any(char.isdigit() for char in contraseña):
            raise ValueError("La contraseña debe tener al menos un número.")
        # Al menos un carácter especial
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contraseña):
            raise ValueError("La contraseña debe tener al menos un carácter especial.")

    @staticmethod
    def validar_correo(correo: str):
        # Llama a la API de Mailboxlayer para verificar el correo
        api_key = "3c120477f870b9dd3ce811fc8eb7625e"  # Reemplaza con tu clave de API de Mailboxlayer
        url = f"http://apilayer.net/api/check?access_key={api_key}&email={correo}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError("Error al verificar el correo con Mailboxlayer.")

        data = response.json()
        # Revisa si el correo es válido según los datos de Mailboxlayer
        if not data.get("format_valid", False):
            raise ValueError("El formato del correo no es válido.")
        if not data.get("mx_found", False):
            raise ValueError("No se encontraron registros MX para el correo.")
        if not data.get("smtp_check", False):
            raise ValueError("El servidor SMTP no pudo verificar el correo.")
        return True

    @staticmethod
    def registrar_usuario(db: Session, nombre: str, apellido: str, correo: str, contraseña: str, genero: str):
        
        # Validar nombre y apellido
        UsuarioLogica.validar_nombre_apellido(nombre, "nombre")
        UsuarioLogica.validar_nombre_apellido(apellido, "apellido")

        # Validar género
        UsuarioLogica.validar_genero(genero)

       
        # Verificar si el correo ya está registrado
        usuario_existente = db.query(Usuario).filter_by(correo=correo).first()
        if usuario_existente:
            raise ValueError("El correo ya está registrado. Intenta con otro.")
        
        
        # Validar correo
        UsuarioLogica.validar_correo(correo)
        
        # Validar contraseña
        UsuarioLogica.validar_contraseña(contraseña)

        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=hashed_password,  # Guardar la contraseña encriptada
            genero=genero
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def autenticar_usuario(db: Session, correo: str, contraseña: str):
        usuario = db.query(Usuario).filter_by(correo=correo).first()
        if not usuario:
            raise ValueError("Correo no registrado.")
        if not bcrypt.checkpw(contraseña.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            raise ValueError("Contraseña incorrecta.")
        return {"id_usuario": usuario.id_usuario, "correo": usuario.correo, "completado": usuario.completado}
    
    @staticmethod
    def marcar_completado(db: Session, id_usuario: int):
        usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.completado = True
        db.commit()
        return {"mensaje": "Usuario marcado como completado."}
    

    @staticmethod
    def generar_enlace_recuperacion(correo: str, db: Session):
        usuario = db.query(Usuario).filter_by(correo=correo).first()
        if not usuario:
            raise ValueError("El correo no está registrado.")

        # Generar un token único
        token = secrets.token_urlsafe(32)

        # Guardar el token en la tabla
        token_recuperacion = TokenRecuperacion(
            token=token,
            id_usuario=usuario.id_usuario,
            fecha_expiracion=datetime.utcnow() + timedelta(hours=1)
        )
        db.add(token_recuperacion)
        db.commit()

        # Enviar el enlace al correo
        enlace = f"http://localhost:5173/resetPassword/{token}"
        UsuarioLogica.enviar_correo(correo, enlace)

        return {"mensaje": "Se envió un enlace de recuperación a tu correo."}

    @staticmethod
    def enviar_correo(destinatario: str, enlace: str):
        # Asunto y contenido del correo
        asunto = "Recuperación de Contraseña"
        cuerpo = f"Haz clic en el enlace para restablecer tu contraseña: {enlace}"
        mensaje = MIMEText(cuerpo)
        mensaje["Subject"] = asunto
        mensaje["From"] = os.getenv("EMAIL_USER")  # Remitente configurado en .env
        mensaje["To"] = destinatario

        try:
            # Configuración del servidor SMTP de Gmail
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Iniciar comunicación segura
                server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))  # Autenticación
                server.sendmail(os.getenv("EMAIL_USER"), destinatario, mensaje.as_string())  # Enviar correo
        except Exception as e:
            # Manejo de errores
            raise ValueError(f"Error al enviar el correo: {e}")

    @staticmethod
    def restablecer_password(token: str, nueva_contraseña: str, db: Session):
        token_recuperacion = db.query(TokenRecuperacion).filter_by(token=token).first()
        if not token_recuperacion or token_recuperacion.fecha_expiracion < datetime.utcnow():
            raise ValueError("El token es inválido o ha expirado.")

        usuario = token_recuperacion.usuario

        # Validar contraseña
        if len(nueva_contraseña) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        # Actualizar contraseña y eliminar token
        usuario.contraseña = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.delete(token_recuperacion)
        db.commit()

        return {"mensaje": "La contraseña se ha restablecido exitosamente."}