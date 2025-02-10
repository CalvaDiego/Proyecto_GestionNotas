from sqlalchemy.orm import Session
from CapaAccesoDatos.repositorios.loginmenu_repositorio import LoginMenuRepositorio
from CapaAccesoDatos.loginmenu_schemas import (
    TrimestreResponse, EstudianteUpdate, EstudianteCreate,
    ActividadCreate, SubActividadCreate, ActividadResponse, SubActividadResponse,
    CalificacionDetalleCreate, CalificacionDetalleUpdate)

class LoginMenuLogica:
    @staticmethod
    def obtener_datos_institucion(db: Session, id_usuario: int):
        return LoginMenuRepositorio.obtener_datos_institucion(db, id_usuario)

    @staticmethod
    def editar_institucion(db: Session, institucion):
        return LoginMenuRepositorio.editar_institucion(db, institucion)

    @staticmethod
    def agregar_grado(db: Session, grado):
        return LoginMenuRepositorio.agregar_grado(db, grado)

    @staticmethod
    def editar_grado(db: Session, id_grado, grado):
        return LoginMenuRepositorio.editar_grado(db, id_grado, grado)

    @staticmethod
    def eliminar_grado(db: Session, id_grado):
        return LoginMenuRepositorio.eliminar_grado(db, id_grado)

    @staticmethod
    def agregar_paralelo(db: Session, paralelo):
        return LoginMenuRepositorio.agregar_paralelo(db, paralelo)

    @staticmethod
    def editar_paralelo(db: Session, id_paralelo, paralelo):
        return LoginMenuRepositorio.editar_paralelo(db, id_paralelo, paralelo)

    @staticmethod
    def eliminar_paralelo(db: Session, id_paralelo: int):
        """
        Llama al repositorio para eliminar un paralelo y sus estudiantes.
        """
        return LoginMenuRepositorio.eliminar_paralelo(db, id_paralelo)

    @staticmethod
    def agregar_materia(db: Session, materia):
        """
        Lógica para agregar una materia y automáticamente crear tres trimestres asociados.
        """
        # Crear la materia
        nueva_materia = LoginMenuRepositorio.agregar_materia(db, materia)

        # Crear los trimestres asociados
        nombres_trimestres = ["Primer Trimestre", "Segundo Trimestre", "Tercer Trimestre"]
        for nombre_trimestre in nombres_trimestres:
            LoginMenuRepositorio.agregar_trimestre(db, nombre=nombre_trimestre, id_materia=nueva_materia["id_materia"])

        return nueva_materia
    
    @staticmethod
    def editar_materia(db: Session, id_materia, materia):
        return LoginMenuRepositorio.editar_materia(db, id_materia, materia)

    @staticmethod
    def eliminar_materia(db: Session, id_materia):
        return LoginMenuRepositorio.eliminar_materia(db, id_materia)
    
    @staticmethod
    def obtener_areas(db: Session):
        return LoginMenuRepositorio.obtener_areas(db)
    
   
    @staticmethod
    def obtener_trimestres(db: Session, id_materia: int):
        """
        Obtiene los trimestres de una materia específica.
        """
        trimestres = LoginMenuRepositorio.obtener_trimestres(db, id_materia)
        return [TrimestreResponse(**t) for t in trimestres]
    
    @staticmethod
    def agregar_estudiante(db: Session, estudiante: EstudianteCreate):
        if not estudiante.nombre_completo.strip():
            raise ValueError("El nombre completo del estudiante no puede estar vacío.")
        return LoginMenuRepositorio.agregar_estudiante(db, estudiante)
    
    @staticmethod
    def obtener_estudiantes(db: Session, id_paralelo: int):
        return LoginMenuRepositorio.obtener_estudiantes(db, id_paralelo)
    
    @staticmethod
    def eliminar_estudiante(db: Session, id_estudiante: int):
        return LoginMenuRepositorio.eliminar_estudiante(db, id_estudiante)

    @staticmethod
    def editar_estudiante(db: Session, id_estudiante: int, estudiante: EstudianteUpdate):
        if not estudiante.nombre_completo.strip():
            raise ValueError("El nombre completo del estudiante no puede estar vacío.")
        return LoginMenuRepositorio.editar_estudiante(db, id_estudiante, estudiante)
    

    @staticmethod
    def agregar_actividad(db: Session, actividad: ActividadCreate):
        if not actividad.nombre.strip():
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        return LoginMenuRepositorio.agregar_actividad(db, actividad)
    

    @staticmethod
    def agregar_subactividad(db: Session, subactividad: SubActividadCreate):
        if not subactividad.nombre.strip():
            raise ValueError("El nombre de la subactividad no puede estar vacío.")
        return LoginMenuRepositorio.agregar_subactividad(db, subactividad)
    
    @staticmethod
    def obtener_actividades(db: Session, id_trimestre: int):
        """
        Obtiene las actividades de un trimestre específico.
        """
        actividades = LoginMenuRepositorio.obtener_actividades(db, id_trimestre)
        return [ActividadResponse(**act) for act in actividades]

    @staticmethod
    def obtener_subactividades(db: Session, id_actividad: int):
        """
        Obtiene las subactividades de una actividad específica.
        """
        subactividades = LoginMenuRepositorio.obtener_subactividades(db, id_actividad)
        return [SubActividadResponse(**sub) for sub in subactividades]
    
    @staticmethod
    def eliminar_actividad(db: Session, id_actividad: int):
        return LoginMenuRepositorio.eliminar_actividad(db, id_actividad)

    
    @staticmethod
    def eliminar_subactividad(db: Session, id_subactividad: int):
        return LoginMenuRepositorio.eliminar_subactividad(db, id_subactividad)
    

    @staticmethod
    def editar_actividad(db: Session, id_actividad: int, nombre: str):
        if not nombre.strip():
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        return LoginMenuRepositorio.editar_actividad(db, id_actividad, nombre)
    
    @staticmethod
    def editar_subactividad(db: Session, id_subactividad: int, nombre: str):
        if not nombre.strip():
            raise ValueError("El nombre de la subactividad no puede estar vacío.")
        return LoginMenuRepositorio.editar_subactividad(db, id_subactividad, nombre)
    
    @staticmethod
    def registrar_calificaciondetalle(db: Session, calificaciondetalle: CalificacionDetalleCreate):
        return LoginMenuRepositorio.agregar_o_actualizar_calificaciondetalle(
            db, calificaciondetalle.id_estudiante, calificaciondetalle.id_subactividad, calificaciondetalle.nota_aporte)
    

    @staticmethod
    def obtener_calificaciondetalle(db: Session, id_estudiante: int, id_subactividad: int):
        return LoginMenuRepositorio.obtener_calificaciondetalle(db, id_estudiante, id_subactividad)
    
    @staticmethod
    def eliminar_calificaciondetalle(db: Session, id_estudiante: int, id_subactividad: int):
        return LoginMenuRepositorio.eliminar_calificaciondetalle(db, id_estudiante, id_subactividad)
    