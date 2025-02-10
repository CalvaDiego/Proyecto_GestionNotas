from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.dependencies import get_db
from CapaAccesoDatos.BaseDatos.models import Grado
from CapaAccesoDatos.schemas import ParaleloCreate, ParaleloResponse, MateriaCreate, MateriaResponse, AreaResponse

from CapaLogicaNegocio.gestionGrados_logica import GestionGradosLogica
from CapaLogicaNegocio.auth import verificar_token_jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/gestionGrados", tags=["Gestión de Grados"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

@router.get("/", response_model=list)
def obtener_grados(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Decodificar el ID del usuario desde el token JWT
        usuario = verificar_token_jwt(token, db)

        # Obtener los grados asociados a la institución del usuario
        grados = db.query(Grado).filter(Grado.institucion.has(id_usuario=usuario.id_usuario)).all()

        return [{"id_grado": grado.id_grado, "nombre": grado.nombre} for grado in grados]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print(f"Error inesperado: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/paralelos/", response_model=ParaleloResponse)
def crear_paralelo(
    paralelo: ParaleloCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Endpoint para crear un nuevo paralelo para un grado específico.
    """
    try:
        # Verificar y decodificar token JWT
        usuario = verificar_token_jwt(token, db)

        # Crear el paralelo
        nuevo_paralelo = GestionGradosLogica.crear_paralelo(db, paralelo.nombre, paralelo.id_grado)

        return nuevo_paralelo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print(f"Error inesperado: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get("/areas/", response_model=list[AreaResponse])
def obtener_areas(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las áreas disponibles.
    """
    try:
        return GestionGradosLogica.obtener_areas(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/materias/", response_model=MateriaResponse)
def crear_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear una nueva materia.
    """
    try:
        print(materia.dict())
        nueva_materia = GestionGradosLogica.crear_materia(db, materia.nombre, materia.id_area, materia.id_grado)
        return nueva_materia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")