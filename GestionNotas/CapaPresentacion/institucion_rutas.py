from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from CapaLogicaNegocio.institucion_logica import InstitucionLogica
from CapaAccesoDatos.BaseDatos.dependencies import get_db
from CapaAccesoDatos.schemas import InstitucionCreate, InstitucionResponse
from fastapi.security import OAuth2PasswordBearer
from CapaAccesoDatos.BaseDatos.models import Grado 
from CapaLogicaNegocio.auth import verificar_token_jwt

router = APIRouter(prefix="/instituciones", tags=["Instituciones"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

@router.post("/", response_model=InstitucionResponse)
def crear_institucion(
    institucion: InstitucionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Decodificar el ID del usuario desde el token JWT
        
        usuario = verificar_token_jwt(token, db)

        # Crear la institución
        nueva_institucion = InstitucionLogica.crear_institucion(
            db,
            nombre=institucion.nombre,
            lugar=institucion.lugar,
            imagen_institucion=institucion.imagen_institucion,
            grados=institucion.grados,
            id_usuario=usuario.id_usuario
        )

        # Consultar los grados asociados a la institución recién creada
        grados_asociados = db.query(Grado).filter_by(id_institucion=nueva_institucion.id_institucion).all()

        return {
            "id_institucion": nueva_institucion.id_institucion,
            "nombre": nueva_institucion.nombre,
            "lugar": nueva_institucion.lugar,
            "grados": [grado.nombre for grado in grados_asociados]
        }
    except ValueError as e:
        print(f"ValueError: {str(e)}")  # Imprime el error específico
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print(f"Error inesperado: {traceback.format_exc()}")  # Imprime el error completo
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/")
def obtener_grados(db: Session = Depends(get_db)):
    grados = db.query(Grado).all()
    return [{"id_grado": grado.id_grado, "nombre": grado.nombre} for grado in grados]