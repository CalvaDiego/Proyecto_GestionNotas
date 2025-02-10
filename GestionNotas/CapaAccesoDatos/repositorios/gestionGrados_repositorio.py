from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Paralelo, Materia, Area, Trimestre

class GestionGradosRepositorio:
    @staticmethod
    def crear_paralelo(db: Session, nombre: str, id_grado: int):
        """
        Crea un nuevo paralelo en la base de datos.
        """
        nuevo_paralelo = Paralelo(nombre=nombre, id_grado=id_grado)
        db.add(nuevo_paralelo)
        db.commit()
        db.refresh(nuevo_paralelo)
        return nuevo_paralelo

    @staticmethod
    def obtener_paralelos_por_grado(db: Session, id_grado: int):
        """
        Obtiene todos los paralelos de un grado.
        """
        return db.query(Paralelo).filter_by(id_grado=id_grado).all()
    
    # Métodos para Materias
    @staticmethod
    def crear_materia(db: Session, nombre: str, id_area: int, id_grado: int):
        nueva_materia = Materia(nombre=nombre, id_area=id_area, id_grado=id_grado)
        db.add(nueva_materia)
        db.commit()
        db.refresh(nueva_materia)
        return nueva_materia
    
    @staticmethod
    def crear_trimestre(db: Session, nombre: str, id_materia: int):
        """
        Crea un nuevo trimestre asociado a una materia.
        """
        nuevo_trimestre = Trimestre(nombre=nombre, id_materia=id_materia)
        db.add(nuevo_trimestre)
        db.commit()
        db.refresh(nuevo_trimestre)
        return nuevo_trimestre

    @staticmethod
    def obtener_areas(db: Session):
        return db.query(Area).all()
    
