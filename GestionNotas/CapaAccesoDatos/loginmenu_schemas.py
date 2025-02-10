from pydantic import BaseModel
from typing import List, Optional

# Esquema para Paralelo
class ParaleloCreate(BaseModel):
    nombre: str
    id_grado: int

class ParaleloResponse(BaseModel):
    id_paralelo: int
    nombre: str
    id_grado: int

    class Config:
        orm_mode = True

class ParaleloEdit(BaseModel):
    nombre: str

# Esquema para Materia
class MateriaCreate(BaseModel):
    nombre: str
    id_area: int
    id_grado: int

class MateriaResponse(BaseModel):
    id_materia: int
    nombre: str
    id_area: int
    id_grado: int

    class Config:
        orm_mode = True

class MateriaEdit(BaseModel):
    nombre: str
    id_area: Optional[int] = None

# Esquema para Grado
class GradoCreate(BaseModel):
    nombre: str
    id_institucion: int

class GradoResponse(BaseModel):
    id_grado: int
    nombre: str

    class Config:
        orm_mode = True

class GradoEdit(BaseModel):
    nombre: str


# Esquema para Institución
class InstitucionCreate(BaseModel):
    nombre: str
    imagen_institucion: Optional[str] = None  # Imagen en Base64
    grados: Optional[List[GradoCreate]] = None  # Grados opcionales

class InstitucionResponse(BaseModel):
    id_institucion: int
    nombre: str
    imagen_institucion: Optional[str] = None
    grados: List[GradoResponse]

    class Config:
        orm_mode = True

class AreaResponse(BaseModel):
    id_area: int
    nombre: str

    class Config:
        orm_mode = True


# Esquema para Trimestre
class TrimestreResponse(BaseModel):
    id_trimestre: int
    nombre: str

    class Config:
        orm_mode = True

# Esquema para estudiantes
class EstudianteCreate(BaseModel):
    nombre_completo: str
    id_paralelo: int

class EstudianteUpdate(BaseModel):
     nombre_completo: str




class ActividadCreate(BaseModel):
    nombre: str
    id_trimestre: int

class ActividadResponse(BaseModel):
    id_actividad: int
    nombre: str
    id_trimestre: int

    class Config:
        from_attributes = True

class SubActividadCreate(BaseModel):
    nombre: str
    id_actividad: int

class SubActividadResponse(BaseModel):
    id_subactividad: int
    nombre: str
    id_actividad: int

    class Config:
        from_attributes = True


class ActividadResponse(BaseModel):
    id_actividad: int
    nombre: str

    class Config:
        from_attributes = True

class SubActividadResponse(BaseModel):
    id_subactividad: int
    nombre: str

    class Config:
        from_attributes = True

class ActividadUpdate(BaseModel):
    nombre: str

class SubActividadUpdate(BaseModel):
    nombre: str

class CalificacionDetalleCreate(BaseModel):
    id_estudiante: int
    id_subactividad: int
    nota_aporte: float
    

class CalificacionDetalleUpdate(BaseModel):
    nota_aporte: float


