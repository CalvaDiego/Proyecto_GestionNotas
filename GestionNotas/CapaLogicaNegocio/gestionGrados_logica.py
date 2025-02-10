from sqlalchemy.orm import Session
from CapaAccesoDatos.repositorios.gestionGrados_repositorio import GestionGradosRepositorio
from CapaAccesoDatos.BaseDatos.models import Grado, Area

class GestionGradosLogica:
    @staticmethod
    def crear_paralelo(db: Session, nombre: str, id_grado: int):
        """
        Valida y crea un nuevo paralelo para un grado específico.
        """
        # Verificar si el grado existe
        grado = db.query(Grado).filter_by(id_grado=id_grado).first()
        if not grado:
            raise ValueError("El grado no existe.")

        # Crear y retornar el paralelo
        return GestionGradosRepositorio.crear_paralelo(db, nombre, id_grado)

    @staticmethod
    def crear_materia(db: Session, nombre: str, id_area: int, id_grado: int):
        """
        Lógica para validar y crear una nueva materia.
        """
        # Verificar si el grado existe
        grado = db.query(Grado).filter_by(id_grado=id_grado).first()
        if not grado:
            raise ValueError("El grado no existe.")

        # Verificar si el área existe
        area = db.query(Area).filter_by(id_area=id_area).first()
        if not area:
            raise ValueError("El área no existe.")

       # Crear la materia
        nueva_materia = GestionGradosRepositorio.crear_materia(db, nombre, id_area, id_grado)

        # Crear automáticamente tres trimestres para la materia
        nombres_trimestres = ["Primer Trimestre", "Segundo Trimestre", "Tercer Trimestre"]
        for nombre_trimestre in nombres_trimestres:
            GestionGradosRepositorio.crear_trimestre(db, nombre_trimestre, nueva_materia.id_materia)

        return nueva_materia

    @staticmethod
    def obtener_areas(db: Session):
        return GestionGradosRepositorio.obtener_areas(db)