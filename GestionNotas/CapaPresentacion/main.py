from fastapi import FastAPI, Form, Depends, HTTPException, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from fastapi import Query
from sqlalchemy.orm import Session
from CapaLogicaNegocio.usuario_logica import registrar_usuario
from CapaLogicaNegocio.usuario_logica import validar_credenciales
from CapaLogicaNegocio.usuario_logica import enviar_enlace_recuperacion
from CapaLogicaNegocio.usuario_logica import restablecer_contrasena
from CapaAccesoDatos.token_repositorio import validar_token
from CapaLogicaNegocio.institucion_logica import guardar_institucion_y_grados
from CapaAccesoDatos.dependencies import get_db

app = FastAPI()

templates = Jinja2Templates(directory="CapaPresentacion/templates")

@app.get("/crear-cuenta/")
async def formulario_usuario():
    return templates.TemplateResponse("registro_usuario.html", {"request": {}})

@app.post("/usuarios/")
async def crear_usuario(
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Llamar a la capa de lógica de negocio para registrar el usuario
        resultado = registrar_usuario(db=db, datos_usuario={
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contraseña": contraseña
        })
        return {"mensaje": "Usuario registrado con éxito", "usuario": resultado}
    except HTTPException as e:
        raise e
    
@app.get("/")
async def formulario_iniciar_sesion():
    return templates.TemplateResponse("iniciar_sesion.html", {"request": {}})

@app.post("/iniciar-sesion/")
async def iniciar_sesion(
     response: Response,
    correo: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Validar credenciales en la capa de lógica de negocio
        usuario = validar_credenciales(db=db, correo=correo, contraseña=contraseña)
        response = RedirectResponse(url="/configurar-institucion/", status_code=303)
        response.set_cookie(key="id_usuario", value=usuario.id_usuario, httponly=True)
        return response
    except HTTPException as e:
        raise e
    

@app.get("/recuperar-contrasena/")
async def formulario_recuperar_contrasena():
    return templates.TemplateResponse("recuperar_contrasena.html", {"request": {}})

@app.post("/recuperar-contrasena/")
async def enviar_correo_recuperacion(correo: str = Form(...), db: Session = Depends(get_db)):
    try:
        mensaje = enviar_enlace_recuperacion(db=db, correo=correo)
        return {"mensaje": mensaje}
    except HTTPException as e:
        raise e

#@app.get("/restablecer-contrasena/")
#async def formulario_restablecer_contrasena(token: str):
#   return templates.TemplateResponse("restablecer_contrasena.html", {"request": {}, "token": token})

@app.get("/restablecer-contrasena/")
async def formulario_restablecer_contrasena(request: Request, token: str, db: Session = Depends(get_db)):
    # Validar el token
    usuario_id = validar_token(db, token)
    if not usuario_id:
        raise HTTPException(status_code=400, detail="El enlace de recuperación ha expirado o no es válido.")

    # Renderizar el formulario solo si el token es válido
    return templates.TemplateResponse("restablecer_contrasena.html", {"request": request, "token": token})

@app.post("/restablecer-contrasena/")
async def restablecer_nueva_contrasena(
    token: str = Form(...),
    nueva_contrasena: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        mensaje = restablecer_contrasena(db=db, token=token, nueva_contrasena=nueva_contrasena)
        return {"mensaje": mensaje}
    except HTTPException as e:
        raise e
    

@app.get("/configurar-institucion/")
async def formulario_configuracion_institucion(request: Request):
    # Verificar si el usuario tiene una cookie activa
    id_usuario = request.cookies.get("id_usuario")
    if not id_usuario:
        raise HTTPException(status_code=401, detail="No autorizado. Inicia sesión.")
    
    return templates.TemplateResponse("configuracion_institucion.html", {"request": request})

@app.post("/configurar-institucion/")
async def configurar_institucion(
    request: Request,
    nombre: str = Form(...),
    lugar: str = Form(...),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Obtener el id_usuario desde la cookie
    id_usuario = request.cookies.get("id_usuario")
    if not id_usuario:
        raise HTTPException(status_code=401, detail="No autorizado. Inicia sesión.")
    
    # Leer los campos dinámicos del formulario
    form_data = await request.form()
    grados = [value for key, value in form_data.items() if key.startswith("grado_")]

    # Guardar institución y grados
    await guardar_institucion_y_grados(db, nombre, lugar, imagen, grados, id_usuario)
    return RedirectResponse(url="/", status_code=303)

