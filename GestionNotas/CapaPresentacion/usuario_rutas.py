import traceback
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from CapaLogicaNegocio.usuario_logica import UsuarioLogica
from CapaAccesoDatos.BaseDatos.dependencies import get_db
from CapaAccesoDatos.schemas import UsuarioRegistro, LoginUsuario, RecuperarPassword, RestablecerPassword
from fastapi.security import OAuth2PasswordBearer
from CapaLogicaNegocio.auth import crear_token_jwt, verificar_token_jwt


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

@router.post("/registrar")
def registrar_usuario(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    try:
        nuevo_usuario = UsuarioLogica.registrar_usuario(
            db, usuario.nombre, usuario.apellido, usuario.correo, usuario.contraseña, usuario.genero
        )
        return {"mensaje": "Usuario registrado exitosamente", "usuario": nuevo_usuario}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()  # Imprime el error completo en la consola
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.post("/login")
def login(usuario: LoginUsuario, db: Session = Depends(get_db)):
    try:
        usuario_data = UsuarioLogica.autenticar_usuario(db, usuario.correo, usuario.contraseña)
        # Generar un token JWT
        token = crear_token_jwt({"sub": usuario_data["correo"]}, completado=usuario_data["completado"])
        return {"access_token": token, "token_type": "bearer", "completado": usuario_data["completado"]}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/completado")
def marcar_completado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    usuario = verificar_token_jwt(token, db)
    return UsuarioLogica.marcar_completado(db, usuario.id_usuario)


@router.get("/perfil")
def perfil_usuario(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        usuario = verificar_token_jwt(token, db)
        return {"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellido": usuario.apellido, "correo": usuario.correo}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/recuperar-password")
def recuperar_password(datos: RecuperarPassword, db: Session = Depends(get_db)):
    try:
        return UsuarioLogica.generar_enlace_recuperacion(datos.correo, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
def reset_password(datos: RestablecerPassword, db: Session = Depends(get_db)):
    try:
        return UsuarioLogica.restablecer_password(datos.token, datos.contraseña, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
