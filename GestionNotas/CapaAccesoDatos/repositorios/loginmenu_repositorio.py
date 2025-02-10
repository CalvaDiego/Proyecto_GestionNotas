from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.models import Institucion, Grado, Paralelo, Materia, Area, Trimestre, Estudiante, Actividad, SubActividad, CalificacionDetalle
from CapaAccesoDatos.loginmenu_schemas import EstudianteUpdate, EstudianteCreate,  ActividadCreate, SubActividadCreate
import base64
from fastapi import HTTPException

class LoginMenuRepositorio:
    @staticmethod
    def obtener_datos_institucion(db: Session, id_usuario: int):
        institucion = db.query(Institucion).filter_by(id_usuario=id_usuario).first()
        if not institucion:
            return {"mensaje": "No hay institución registrada para este usuario."}
        
        grados = db.query(Grado).filter_by(id_institucion=institucion.id_institucion).all()
        
        data = {
            "institucion": {
                "id_institucion": institucion.id_institucion,
                "nombre": institucion.nombre,
                "imagen": base64.b64encode(institucion.imagen_institucion).decode("utf-8") 
                if institucion.imagen_institucion else None,
            },
            "grados": [
                {
                    "id_grado": grado.id_grado,
                    "nombre": grado.nombre,
                    "paralelos": [
                        {"id_paralelo": paralelo.id_paralelo, "nombre": paralelo.nombre}
                        for paralelo in db.query(Paralelo).filter_by(id_grado=grado.id_grado).all()
                    ],
                    "materias": [
                        {
                            "id_materia": materia.id_materia,
                            "nombre": materia.nombre,
                            "trimestres": [
                                {"id_trimestre": trimestre.id_trimestre, "nombre": trimestre.nombre}
                                for trimestre in db.query(Trimestre).filter_by(id_materia=materia.id_materia).all()
                            ]
                        }
                        for materia in db.query(Materia).filter_by(id_grado=grado.id_grado).all()
                    ],
                }
                for grado in grados
            ],
        }
        return data

    @staticmethod
    def editar_institucion(db: Session, institucion):
        institucion_actual = db.query(Institucion).first()
        if not institucion_actual:
            raise ValueError("Institución no encontrada.")
        institucion_actual.nombre = institucion.nombre
        institucion_actual.imagen_institucion = base64.b64decode(institucion.imagen_institucion) if institucion.imagen_institucion else institucion_actual.imagen_institucion
        db.commit()
        return {"mensaje": "Institución actualizada con éxito."}

    @staticmethod
    def agregar_grado(db: Session, grado):
        nuevo_grado = Grado(nombre=grado.nombre, id_institucion=grado.id_institucion)
        db.add(nuevo_grado)
        db.commit()
        db.refresh(nuevo_grado)
        return {"mensaje": "Grado agregado con éxito.", "id_grado": nuevo_grado.id_grado}

    @staticmethod
    def editar_grado(db: Session, id_grado, grado):
        grado_actual = db.query(Grado).filter_by(id_grado=id_grado).first()
        if not grado_actual:
            raise ValueError("Grado no encontrado.")
        grado_actual.nombre = grado.nombre
        db.commit()
        return {"mensaje": "Grado actualizado con éxito."}
    
    @staticmethod
    def eliminar_grado(db: Session, id_grado: int):
        """
        Elimina un grado, incluyendo sus estudiantes, paralelos, materias y trimestres asociados.
        """
        grado_actual = db.query(Grado).filter_by(id_grado=id_grado).first()
        if not grado_actual:
            raise ValueError("Grado no encontrado.")

        # ✅ PASO 1: Eliminar los estudiantes de los paralelos asociados
        paralelos = db.query(Paralelo).filter_by(id_grado=id_grado).all()
        for paralelo in paralelos:
            estudiantes = db.query(Estudiante).filter_by(id_paralelo=paralelo.id_paralelo).all()
            for estudiante in estudiantes:
                db.delete(estudiante)

        db.commit()  # ✅ Confirmamos eliminación de estudiantes antes de seguir

        # ✅ PASO 2: Eliminar paralelos asociados al grado
        for paralelo in paralelos:
            db.delete(paralelo)

        db.commit()  # ✅ Confirmamos eliminación de paralelos antes de seguir

        # ✅ PASO 3: Eliminar trimestres de las materias del grado
        materias = db.query(Materia).filter_by(id_grado=id_grado).all()
        for materia in materias:
            trimestres = db.query(Trimestre).filter_by(id_materia=materia.id_materia).all()
            for trimestre in trimestres:
                db.delete(trimestre)

        db.commit()  # ✅ Confirmamos eliminación de trimestres antes de seguir

        # ✅ PASO 4: Eliminar materias asociadas al grado
        for materia in materias:
            db.delete(materia)

        db.commit()  # ✅ Confirmamos eliminación de materias antes de seguir

        # ✅ PASO 5: Eliminar el grado
        db.delete(grado_actual)
        db.commit()

        return {"mensaje": "Grado, paralelos, estudiantes, materias y trimestres eliminados con éxito."}

    @staticmethod
    def agregar_paralelo(db: Session, paralelo):
        nuevo_paralelo = Paralelo(nombre=paralelo.nombre, id_grado=paralelo.id_grado)
        db.add(nuevo_paralelo)
        db.commit()
        db.refresh(nuevo_paralelo)
        return {"mensaje": "Paralelo agregado con éxito.", "id_paralelo": nuevo_paralelo.id_paralelo}

    @staticmethod
    def editar_paralelo(db: Session, id_paralelo, paralelo):
        paralelo_actual = db.query(Paralelo).filter_by(id_paralelo=id_paralelo).first()
        if not paralelo_actual:
            raise ValueError("Paralelo no encontrado.")
        paralelo_actual.nombre = paralelo.nombre
        db.commit()
        return {"mensaje": "Paralelo actualizado con éxito."}

    @staticmethod
    def eliminar_paralelo(db: Session, id_paralelo: int):
        """
        Elimina un paralelo y todos los estudiantes asociados a él.
        """
        paralelo = db.query(Paralelo).filter_by(id_paralelo=id_paralelo).first()
        if not paralelo:
            raise ValueError("Paralelo no encontrado.")

        # ✅ Eliminar los estudiantes asociados a este paralelo
        estudiantes = db.query(Estudiante).filter_by(id_paralelo=id_paralelo).all()
        for estudiante in estudiantes:
            db.delete(estudiante)

        db.commit()  # ✅ Confirmar cambios antes de eliminar el paralelo

        # ✅ Ahora eliminar el paralelo
        db.delete(paralelo)
        db.commit()

        return {"mensaje": "Paralelo y estudiantes eliminados con éxito."}

    @staticmethod
    def agregar_materia(db: Session, materia):
        nueva_materia = Materia(nombre=materia.nombre, id_area=materia.id_area, id_grado=materia.id_grado)
        db.add(nueva_materia)
        db.commit()
        db.refresh(nueva_materia)
        return {"mensaje": "Materia agregada con éxito.", "id_materia": nueva_materia.id_materia}
    
    @staticmethod
    def agregar_trimestre(db: Session, nombre: str, id_materia: int):
        """
        Agrega un trimestre asociado a una materia en la base de datos.
        """
        nuevo_trimestre = Trimestre(nombre=nombre, id_materia=id_materia)
        db.add(nuevo_trimestre)
        db.commit()
        db.refresh(nuevo_trimestre)
        return {"mensaje": f"Trimestre '{nombre}' agregado con éxito.", "id_trimestre": nuevo_trimestre.id_trimestre}

    @staticmethod
    def editar_materia(db: Session, id_materia, materia):
        materia_actual = db.query(Materia).filter_by(id_materia=id_materia).first()
        if not materia_actual:
            raise ValueError("Materia no encontrada.")
        if materia.nombre:
            materia_actual.nombre = materia.nombre
        if materia.id_area:
            materia_actual.id_area = materia.id_area
        db.commit()
        return {"mensaje": "Materia actualizada con éxito."}

    @staticmethod
    def eliminar_materia(db: Session, id_materia):
        materia_actual = db.query(Materia).filter_by(id_materia=id_materia).first()
        if not materia_actual:
            raise ValueError("Materia no encontrada.")
        
        # Buscar y eliminar los trimestres asociados a la materia
        trimestres = db.query(Trimestre).filter_by(id_materia=id_materia).all()
        for trimestre in trimestres:
            db.delete(trimestre)

        db.delete(materia_actual)
        db.commit()
        return {"mensaje": "Materia eliminada con éxito."}
    
    @staticmethod
    def obtener_areas(db: Session):
        areas = db.query(Area).all()
        return [{"id_area": area.id_area, "nombre": area.nombre} for area in areas]
    
    
    @staticmethod
    def obtener_trimestres(db: Session, id_materia: int):
        """
        Obtiene los trimestres asociados a una materia.
        """
        trimestres = db.query(Trimestre).filter_by(id_materia=id_materia).all()
        return [{"id_trimestre": t.id_trimestre, "nombre": t.nombre} for t in trimestres]
    
    @staticmethod
    def agregar_estudiante(db: Session, estudiante: EstudianteCreate):
        nuevo_estudiante = Estudiante(
            nombre_completo=estudiante.nombre_completo,  # ✅ Nuevo campo único
            id_paralelo=estudiante.id_paralelo
        )
        db.add(nuevo_estudiante)
        db.commit()
        db.refresh(nuevo_estudiante)
        return {"mensaje": "Estudiante agregado con éxito.", "id_estudiante": nuevo_estudiante.id_estudiante}
    
    
    @staticmethod
    def obtener_estudiantes(db: Session, id_paralelo: int):
        estudiantes = db.query(Estudiante).filter_by(id_paralelo=id_paralelo).all()
        return [{"id_estudiante": e.id_estudiante, "nombre_completo": e.nombre_completo} for e in estudiantes]
    
    @staticmethod
    def eliminar_estudiante(db: Session, id_estudiante: int):
        estudiante = db.query(Estudiante).filter(Estudiante.id_estudiante == id_estudiante).first()
        
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        db.delete(estudiante)
        db.commit()
        return {"mensaje": "Estudiante eliminado con éxito."}
    
    @staticmethod
    def editar_estudiante(db: Session, id_estudiante: int, estudiante_data: EstudianteUpdate):
        estudiante = db.query(Estudiante).filter_by(id_estudiante=id_estudiante).first()
        if not estudiante:
            raise ValueError("Estudiante no encontrado.")
        estudiante.nombre_completo = estudiante_data.nombre_completo  # ✅ Ahora se actualiza correctamente
        db.commit()
        db.refresh(estudiante)
        return estudiante
    
    @staticmethod
    def agregar_actividad(db: Session, actividad: ActividadCreate):
        """
        Agrega una nueva actividad y automáticamente crea una subactividad predeterminada.
        """
        nueva_actividad = Actividad(
            nombre=actividad.nombre,
            id_trimestre=actividad.id_trimestre
        )
        db.add(nueva_actividad)
        db.commit()
        db.refresh(nueva_actividad)
        
        # ✅ Crear subactividad automática asociada a la actividad recién creada
        nueva_subactividad = SubActividad(
            nombre="Subactividad 1",
            id_actividad=nueva_actividad.id_actividad
        )
        db.add(nueva_subactividad)
        db.commit()
        db.refresh(nueva_subactividad)
        return {
            "mensaje": "Actividad y subactividad creadas con éxito.",
            "id_actividad": nueva_actividad.id_actividad,
            "nombre_actividad": nueva_actividad.nombre,
            "id_subactividad": nueva_subactividad.id_subactividad,
            "nombre_subactividad": nueva_subactividad.nombre
        }

    @staticmethod
    def agregar_subactividad(db: Session, subactividad: SubActividadCreate):
        nueva_subactividad = SubActividad(
            nombre=subactividad.nombre,
            id_actividad=subactividad.id_actividad
        )
        db.add(nueva_subactividad)
        db.commit()
        db.refresh(nueva_subactividad)
        return {"mensaje": "Subactividad agregada con éxito.", "id_subactividad": nueva_subactividad.id_subactividad}
    
    @staticmethod
    def obtener_actividades(db: Session, id_trimestre: int):
        """
        Obtiene todas las actividades asociadas a un trimestre.
        """
        actividades = db.query(Actividad).filter_by(id_trimestre=id_trimestre).all()
        return [{"id_actividad": act.id_actividad, "nombre": act.nombre} for act in actividades]

    @staticmethod
    def obtener_subactividades(db: Session, id_actividad: int):
        """
        Obtiene todas las subactividades asociadas a una actividad.
        """
        subactividades = db.query(SubActividad).filter_by(id_actividad=id_actividad).all()
        return [{"id_subactividad": sub.id_subactividad, "nombre": sub.nombre} for sub in subactividades]
    
    @staticmethod
    def eliminar_actividad(db: Session, id_actividad: int):
        actividad = db.query(Actividad).filter(Actividad.id_actividad == id_actividad).first()
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        db.query(SubActividad).filter(SubActividad.id_actividad == id_actividad).delete()
        
        db.delete(actividad)
        db.commit()
        
        return {"mensaje": "Actividad y sus subactividades eliminadas con éxito."}
    
    @staticmethod
    def eliminar_subactividad(db: Session, id_subactividad: int):
        subactividad = db.query(SubActividad).filter(SubActividad.id_subactividad == id_subactividad).first()
        if not subactividad:
            raise HTTPException(status_code=404, detail="Subactividad no encontrada")
        
        db.delete(subactividad)
        db.commit()
        
        return {"mensaje": "Subactividad eliminada con éxito."}
    
    @staticmethod
    def editar_actividad(db: Session, id_actividad: int, nombre: str):
        """
        Edita una actividad en la base de datos.
        """
        actividad = db.query(Actividad).filter_by(id_actividad=id_actividad).first()
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        actividad.nombre = nombre  # Actualiza el nombre de la actividad
        db.commit()
        db.refresh(actividad)
        return {"mensaje": "Actividad actualizada con éxito."}
    
    @staticmethod
    def editar_subactividad(db: Session, id_subactividad: int, nombre: str):
        """
        Edita una subactividad en la base de datos.
        """
        subactividad = db.query(SubActividad).filter_by(id_subactividad=id_subactividad).first()
        if not subactividad:
            raise HTTPException(status_code=404, detail="Subactividad no encontrada")
        
        subactividad.nombre = nombre  # Actualiza el nombre de la subactividad
        db.commit()
        db.refresh(subactividad)
        return {"mensaje": "Subactividad actualizada con éxito."}
    
    @staticmethod
    def agregar_o_actualizar_calificaciondetalle(db: Session, id_estudiante: int, id_subactividad: int, nota_aporte: float):
        # 🔹 Verificar si el estudiante existe
        estudiante = db.query(Estudiante).filter_by(id_estudiante=id_estudiante).first()
        if not estudiante:
            raise HTTPException(status_code=404, detail=f"El estudiante con ID {id_estudiante} no existe.")
        
        # 🔹 Verificar si la subactividad existe
        subactividad = db.query(SubActividad).filter_by(id_subactividad=id_subactividad).first()
        if not subactividad:
            raise HTTPException(status_code=404, detail=f"La subactividad con ID {id_subactividad} no existe.")
            
        # 🔹 Verificar si la calificación ya existe
        calificaciondetalle = db.query(CalificacionDetalle).filter_by(
            id_estudiante=id_estudiante, id_subactividad=id_subactividad
        ).first()
        
        if calificaciondetalle :
            # Si ya existe, actualizar la nota
            calificaciondetalle .nota_aporte = nota_aporte
            mensaje = "Calificación actualizada con éxito."
        else:
            # Si no existe, crear una nueva
            nueva_calificaciondetalle  = CalificacionDetalle(
                id_estudiante=id_estudiante,
                id_subactividad=id_subactividad,
                nota_aporte=nota_aporte
            )
            db.add(nueva_calificaciondetalle)
            mensaje = "Calificación agregada con éxito."
        db.commit()
        return {"mensaje": mensaje, "id_estudiante": id_estudiante, "id_subactividad": id_subactividad, "nota_aporte": nota_aporte}
    
    @staticmethod
    def obtener_calificaciondetalle (db: Session, id_estudiante: int, id_subactividad: int):
        calificaciondetalle  = db.query(CalificacionDetalle).filter_by(id_estudiante=id_estudiante, id_subactividad=id_subactividad).first()
        if calificaciondetalle :
            return {
                "id_calificacion": calificaciondetalle .id_calificacion,
                 "nota_aporte": round(float(calificaciondetalle.nota_aporte), 2)
            }
        else:
            return {"mensaje": "Calificación no encontrada."}
        
    @staticmethod
    def eliminar_calificaciondetalle (db: Session, id_estudiante: int, id_subactividad: int):
        """
        Elimina una calificación de un estudiante en una subactividad.
        """
        calificaciondetalle = db.query(CalificacionDetalle).filter_by(id_estudiante=id_estudiante, id_subactividad=id_subactividad).first()
        if not calificaciondetalle:
            raise HTTPException(status_code=404, detail="Calificación no encontrada.")
        
        db.delete(calificaciondetalle)
        db.commit()
        
        return {"mensaje": "Calificación eliminada con éxito."}
    
    