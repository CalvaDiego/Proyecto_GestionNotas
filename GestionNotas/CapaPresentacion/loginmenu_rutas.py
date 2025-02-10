from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from CapaLogicaNegocio.loginmenu_logica import LoginMenuLogica
from CapaAccesoDatos.BaseDatos.dependencies import get_db
from CapaAccesoDatos.loginmenu_schemas import (
    InstitucionCreate, GradoCreate, ParaleloCreate, MateriaCreate,
    GradoEdit, ParaleloEdit, MateriaEdit, TrimestreResponse, EstudianteCreate, 
    EstudianteUpdate, ActividadCreate, SubActividadCreate, ActividadResponse,
    SubActividadResponse, ActividadUpdate, SubActividadUpdate, CalificacionDetalleCreate)
from CapaLogicaNegocio.auth import verificar_token_jwt
from fastapi.security import OAuth2PasswordBearer
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

router = APIRouter(prefix="/loginmenu", tags=["LoginMenu"])

# Obtener datos de la institución
@router.get("/")
def obtener_datos_institucion(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        usuario = verificar_token_jwt(token, db)  # Obtener usuario autenticado
        return LoginMenuLogica.obtener_datos_institucion(db, usuario.id_usuario)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# Editar institución
@router.put("/institucion")
def editar_institucion(institucion: InstitucionCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_institucion(db, institucion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Agregar grado
@router.post("/grado")
def agregar_grado(grado: GradoCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_grado(db, grado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Editar grado
@router.put("/grado/{id_grado}")
def editar_grado(id_grado: int, grado: GradoEdit, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_grado(db, id_grado, grado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar grado
@router.delete("/grado/{id_grado}")
def eliminar_grado(id_grado: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_grado(db, id_grado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

# Agregar paralelo
@router.post("/paralelo")
def agregar_paralelo(paralelo: ParaleloCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_paralelo(db, paralelo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Editar paralelo
@router.put("/paralelo/{id_paralelo}")
def editar_paralelo(id_paralelo: int, paralelo: ParaleloEdit, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_paralelo(db, id_paralelo, paralelo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar paralelo
@router.delete("/paralelo/{id_paralelo}")
def eliminar_paralelo(id_paralelo: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_paralelo(db, id_paralelo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Agregar materia
@router.post("/materia")
def agregar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_materia(db, materia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Editar materia
@router.put("/materia/{id_materia}")
def editar_materia(id_materia: int, materia: MateriaEdit, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_materia(db, id_materia, materia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Eliminar materia
@router.delete("/materia/{id_materia}")
def eliminar_materia(id_materia: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_materia(db, id_materia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todas las áreas
@router.get("/areas")
def obtener_areas(db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.obtener_areas(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Nueva ruta para obtener los trimestres de una materia
@router.get("/trimestres/{id_materia}", response_model=List[TrimestreResponse])
def obtener_trimestres(id_materia: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.obtener_trimestres(db, id_materia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/estudiante")
def agregar_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_estudiante(db, estudiante)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/estudiantes/{id_paralelo}")
def obtener_estudiantes(id_paralelo: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.obtener_estudiantes(db, id_paralelo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/estudiante/{id_estudiante}")
def eliminar_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_estudiante(db, id_estudiante)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/estudiante/{id_estudiante}")
def actualizar_estudiante(id_estudiante: int, estudiante: EstudianteUpdate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_estudiante(db, id_estudiante, estudiante)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/actividad")
def agregar_actividad(actividad: ActividadCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_actividad(db, actividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/subactividad")
def agregar_subactividad(subactividad: SubActividadCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.agregar_subactividad(db, subactividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/actividades/{id_trimestre}", response_model=List[ActividadResponse])
def obtener_actividades(id_trimestre: int, db: Session = Depends(get_db)):
    """
    Obtiene las actividades de un trimestre específico.
    """
    try:
        return LoginMenuLogica.obtener_actividades(db, id_trimestre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subactividades/{id_actividad}", response_model=List[SubActividadResponse])
def obtener_subactividades(id_actividad: int, db: Session = Depends(get_db)):
    """
    Obtiene las subactividades de una actividad específica.
    """
    try:
        return LoginMenuLogica.obtener_subactividades(db, id_actividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete("/actividad/{id_actividad}")
def eliminar_actividad(id_actividad: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_actividad(db, id_actividad)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/subactividad/{id_subactividad}")
def eliminar_subactividad(id_subactividad: int, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.eliminar_subactividad(db, id_subactividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Editar actividad
@router.put("/actividad/{id_actividad}")
def editar_actividad(id_actividad: int, actividad: ActividadUpdate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_actividad(db, id_actividad, actividad.nombre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Editar subactividad
@router.put("/subactividad/{id_subactividad}")
def editar_subactividad(id_subactividad: int, subactividad: SubActividadUpdate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.editar_subactividad(db, id_subactividad, subactividad.nombre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calificaciondetalle")
def registrar_calificaciondetalle(calificacion: CalificacionDetalleCreate, db: Session = Depends(get_db)):
    try:
        return LoginMenuLogica.registrar_calificaciondetalle(db, calificacion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/calificaciondetalle/{id_estudiante}/{id_subactividad}")
def obtener_calificaciondetalle(id_estudiante: int, id_subactividad: int, db: Session = Depends(get_db)):
    """
    Obtiene la calificación de un estudiante en una subactividad específica.
    """
    try:
        return LoginMenuLogica.obtener_calificaciondetalle(db, id_estudiante, id_subactividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/calificaciondetalle/{id_estudiante}/{id_subactividad}")
def eliminar_calificaciondetalle(id_estudiante: int, id_subactividad: int, db: Session = Depends(get_db)):
    """
    Elimina una calificación de la base de datos.
    """
    try:
        return LoginMenuLogica.eliminar_calificaciondetalle(db, id_estudiante, id_subactividad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    