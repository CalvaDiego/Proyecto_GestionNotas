from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Institucion, Grado, Usuario
import base64


class InstitucionRepositorio:
    @staticmethod
    def crear_institucion(db: Session, nombre: str, lugar: str, imagen_institucion: str, id_usuario: int):
        """
        Crea una nueva institución en la base de datos.
        """
        # Decodificar la imagen Base64
        try:
            imagen_decodificada = base64.b64decode(imagen_institucion)
        except Exception:
            raise ValueError("La imagen no tiene un formato Base64 válido.")

        # Crear la institución
        nueva_institucion = Institucion(
            nombre=nombre,
            lugar=lugar,
            imagen_institucion=imagen_decodificada,
            id_usuario=id_usuario
        )
        db.add(nueva_institucion)
        db.commit()
        db.refresh(nueva_institucion)

        return nueva_institucion

    @staticmethod
    def crear_grados(db: Session, grados: list, id_institucion: int):
        try:
            print(f"Creando grados para la institución con ID {id_institucion}")
            print(f"Datos de los grados: {grados}")
            if not grados:
                raise ValueError("No se proporcionaron grados para crear.")
            
            for grado in grados:
                nuevo_grado = Grado(
                    nombre=grado.nombre,
                    id_institucion=id_institucion
                )
                db.add(nuevo_grado)
            db.commit()
        
        except Exception as e:
            print(f"Error al crear grados: {str(e)}")
            db.rollback()
            raise ValueError("Error al crear los grados.")


    @staticmethod
    def obtener_usuario(db: Session, id_usuario: int):
        """
        Verifica si el usuario existe en la base de datos.
        """
        return db.query(Usuario).filter_by(id_usuario=id_usuario).first()

    @staticmethod
    def obtener_institucion_por_usuario(db: Session, id_usuario: int):
        """
        Retorna la institución asociada a un usuario si existe.
        """
        return db.query(Institucion).filter_by(id_usuario=id_usuario).first()