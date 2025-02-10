from sqlalchemy.orm import Session
from CapaAccesoDatos.repositorios.institucion_repositorio import InstitucionRepositorio


class InstitucionLogica:
    @staticmethod
    def crear_institucion(db: Session, nombre: str, lugar: str, imagen_institucion: str, grados: list, id_usuario: int):
        """
        Lógica para crear una institución con grados.
        """
        # Verificar si el usuario ya tiene una institución registrada
        if InstitucionRepositorio.obtener_institucion_por_usuario(db, id_usuario):
            raise ValueError("El usuario ya tiene una institución registrada.")
        
        # Verificar si el usuario existe
        usuario = InstitucionRepositorio.obtener_usuario(db, id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        # Crear la institución
        nueva_institucion = InstitucionRepositorio.crear_institucion(
            db, nombre, lugar, imagen_institucion, id_usuario
        )

        # Crear los grados asociados
        InstitucionRepositorio.crear_grados(db, grados, nueva_institucion.id_institucion)

        return nueva_institucion
