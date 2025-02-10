from pydantic import BaseModel, EmailStr, validator
from typing import List



class UsuarioRegistro(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    contraseña: str
    genero: str

class LoginUsuario(BaseModel):
    correo: EmailStr
    contraseña: str

class RecuperarPassword(BaseModel):
    correo: EmailStr

class RestablecerPassword(BaseModel):
    token: str
    contraseña: str


# Institucion 
class GradoCreate(BaseModel):
    nombre: str

class InstitucionCreate(BaseModel):
    nombre: str
    lugar: str
    imagen_institucion: str  # Imagen codificada en Base64
    grados: List[GradoCreate]

class InstitucionResponse(BaseModel):
    id_institucion: int
    nombre: str
    lugar: str
    grados: List[str]

    class Config:
        orm_mode = True



# Esquema para Paralelo (entrada)
class ParaleloCreate(BaseModel):
    nombre: str
    id_grado: int

# Esquema para Paralelo (respuesta)
class ParaleloResponse(BaseModel):
    id_paralelo: int
    nombre: str
    id_grado: int

    class Config:
        orm_mode = True

# Esquema para Grado (respuesta)
class GradoResponse(BaseModel):
    id_grado: int
    nombre: str

    class Config:
        orm_mode = True


# Materia

class AreaResponse(BaseModel):
    id_area: int
    nombre: str

    class Config:
        orm_mode = True

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