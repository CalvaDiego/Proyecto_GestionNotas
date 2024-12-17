from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, Text, LargeBinary,  DateTime
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from .database import Base

# Clase Usuario (ya creada)
class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)
    estado = Column(Boolean, default=False)

# Clase Institución (ya creada)
class Institucion(Base):
    __tablename__ = "institucion"
    id_institucion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    lugar = Column(String, nullable=False)
    imagen_institucion = Column(LargeBinary)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    usuario = relationship("Usuario")

# Clase Grado
class Grado(Base):
    __tablename__ = "grado"
    id_grado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    id_institucion = Column(Integer, ForeignKey("institucion.id_institucion"))
    institucion = relationship("Institucion")

# Clase Paralelo
class Paralelo(Base):
    __tablename__ = "paralelo"
    id_paralelo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    id_grado = Column(Integer, ForeignKey("grado.id_grado"))
    grado = relationship("Grado")

# Clase Estudiante
class Estudiante(Base):
    __tablename__ = "estudiante"
    id_estudiante = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    id_paralelo = Column(Integer, ForeignKey("paralelo.id_paralelo"))
    paralelo = relationship("Paralelo")

# Clase Área
class Area(Base):
    __tablename__ = "area"
    id_area = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

# Clase Materia
class Materia(Base):
    __tablename__ = "materia"
    id_materia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    id_area = Column(Integer, ForeignKey("area.id_area"))
    id_grado = Column(Integer, ForeignKey("grado.id_grado"))
    area = relationship("Area")
    grado = relationship("Grado")

# Clase Trimestre
class Trimestre(Base):
    __tablename__ = "trimestre"
    id_trimestre = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    id_materia = Column(Integer, ForeignKey("materia.id_materia"))
    materia = relationship("Materia")

# Clase Actividad
class Actividad(Base):
    __tablename__ = "actividad"
    id_actividad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Individual o Grupal
    id_trimestre = Column(Integer, ForeignKey("trimestre.id_trimestre"))
    trimestre = relationship("Trimestre")

# Clase Calificación
class Calificacion(Base):
    __tablename__ = "calificacion"
    id_calificacion = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante"))
    id_actividad = Column(Integer, ForeignKey("actividad.id_actividad"))
    nota_aporte = Column(Numeric(5, 2))
    nota_proyecto = Column(Numeric(5, 2))
    nota_evaluacion = Column(Numeric(5, 2))
    promedio_70 = Column(Numeric(5, 2))
    promedio_30 = Column(Numeric(5, 2))
    nota_trimestre = Column(Numeric(5, 2))
    promedio_cualitativo = Column(String)
    estudiante = relationship("Estudiante")
    actividad = relationship("Actividad")

# Clase Calificación Anual
class CalificacionAnual(Base):
    __tablename__ = "calificacion_anual"
    id_anual = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante"))
    id_materia = Column(Integer, ForeignKey("materia.id_materia"))
    promedio_trimestres_70 = Column(Numeric(5, 2))
    nota_proyecto_anual = Column(Numeric(5, 2))
    nota_examen_final = Column(Numeric(5, 2))
    promedio_30 = Column(Numeric(5, 2))
    promedio_anual_cuantitativo = Column(Numeric(5, 2))
    promedio_anual_cualitativo = Column(String)
    estado = Column(String)
    nota_supletorio = Column(Numeric(5, 2))
    estado_final = Column(String)
    estudiante = relationship("Estudiante")
    materia = relationship("Materia")

# Clase Token para recuperación de contraseña
class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id_usuario"))
    token = Column(String, unique=True, nullable=False)
    expiracion = Column(DateTime, nullable=False)
    usuario = relationship("Usuario")

# Configurar la expiración del token (1 hora por ejemplo)
def generar_expiracion():
    return datetime.utcnow() + timedelta(hours=1)