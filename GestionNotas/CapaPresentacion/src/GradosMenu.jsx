import { useState, useEffect, useCallback } from "react";
import PropTypes from "prop-types";
import { FaTrash, FaPlus  } from "react-icons/fa";
import "./GradosMenu.css";
import api from "./api";

export function GradosMenu({ materia }) {

  const [tabActivo, setTabActivo] = useState("");
  const [estudiantes, setEstudiantes] = useState([]);
  const [trimestres, setTrimestres] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [idTrimestreActivo, setIdTrimestreActivo] = useState(materia.id_trimestre || null); // ✅ Estado para el ID del trimestre
  const [menuContextual, setMenuContextual] = useState({
    visible: false,
    x: 0,
    y: 0,
    tipo: "",
    actIndex: null,
    subIndex: null
  });

  const ocultarMenuContextual = useCallback(() => {
    setMenuContextual((prev) => ({ ...prev, visible: false }));
  }, []);
  
  useEffect(() => {
    const cerrarMenu = () => {
      if (menuContextual.visible) {
        ocultarMenuContextual();
      }
    };

    document.addEventListener("click", cerrarMenu);

    return () => {
      document.removeEventListener("click", cerrarMenu);
    };
  }, [menuContextual.visible, ocultarMenuContextual]);



  const fetchActividades = async (idTrimestre) => {
    try {
      const response = await api.get(`/loginmenu/actividades/${idTrimestre}`);
      return response.data;
    } catch (error) {
      console.error("❌ Error al obtener actividades:", error);
      return [];
    }
  };

  const fetchSubactividades = async (idActividad) => {
    try {
      const response = await api.get(`/loginmenu/subactividades/${idActividad}`);
      return response.data;
    } catch (error) {
      console.error("❌ Error al obtener subactividades:", error);
      return [];
    }
  };

    useEffect(() => {
    const fetchTrimestres = async () => {
      try {
        const response = await api.get(`/loginmenu/trimestres/${materia.id_materia}`);
        const trimestresObtenidos = response.data;
        const trimestresFormateados = {};

        for (const trimestre of trimestresObtenidos) {
          const actividades = await fetchActividades(trimestre.id_trimestre);
          
          for (const actividad of actividades) {
            actividad.subactividades = await fetchSubactividades(actividad.id_actividad);
          }

          trimestresFormateados[trimestre.nombre] = {
            id_trimestre: trimestre.id_trimestre,
            actividades,
          };
        }

        if (!trimestresFormateados["Calificación Anual"]) {
          trimestresFormateados["Calificación Anual"] = { actividades: [] };
        }

        setTrimestres(trimestresFormateados);
        const primerTrimestre = Object.keys(trimestresFormateados).find((t) => t.includes("Trimestre")) || "Calificación Anual";
        setTabActivo(primerTrimestre);
        setIdTrimestreActivo(trimestresFormateados[primerTrimestre]?.id_trimestre || null);
        setIsLoading(false);
      } catch (error) {
        console.error("❌ Error al obtener los trimestres:", error);
        setIsLoading(false);
      }
    };

    fetchTrimestres();
  }, [materia]);

  useEffect(() => {
    const fetchEstudiantes = async () => {
      try {
        console.log(`📡 Obteniendo estudiantes del paralelo ID: ${materia.id_paralelo}`);
        const response = await api.get(`/loginmenu/estudiantes/${materia.id_paralelo}`);
        console.log("✅ Estudiantes obtenidos:", response.data);
  
        const estudiantesConNotas = await Promise.all(
          response.data.map(async (estudiante) => {
            let notas = {};
  
            for (const trimestre of Object.keys(trimestres)) {
              for (const actividad of trimestres[trimestre]?.actividades || []) {
                for (const subactividad of actividad.subactividades || []) {
                  const nota = await obtenerNota(estudiante.id_estudiante, subactividad.id_subactividad);
                  notas[subactividad.id_subactividad] = nota || "";
                }
              }
            }
  
            return { ...estudiante, notas };
          })
        );
  
        console.log("🎯 Estudiantes con notas obtenidas:", estudiantesConNotas);
        setEstudiantes(estudiantesConNotas);
      } catch (error) {
        console.error("❌ Error al obtener estudiantes:", error);
      }
    };
  
    if (materia.id_paralelo) {
      fetchEstudiantes();
    }
  }, [materia.id_paralelo, trimestres]);
  
  
  
   // 🔄 Se ejecuta cuando cambia el paralelo o los trimestres

  const cambiarTab = (tab) => {
    if (trimestres[tab] || tab === "Calificación Anual") {
      setTabActivo(tab);
      setIdTrimestreActivo(trimestres[tab]?.id_trimestre || null); // ✅ Cambia dinámicamente el ID
    }
  };
  
  if (isLoading) {
    console.log("⏳ Cargando trimestres...");
    return <p>Cargando trimestres...</p>;
  }

  const generarNombreAleatorio = () => {
    const caracteres = "abcdefghijklmnopqrstuvwxyz";
    let nombreAleatorio = "";
    
    for (let i = 0; i < 6; i++) {  // Genera una cadena de 6 letras aleatorias
        nombreAleatorio += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
    }
    
    return `Estudiante ${nombreAleatorio}`;
};

const agregarEstudiante = async () => {
  try {
    // ✅ Genera un nombre aleatorio de 6 letras
    const nuevoEstudiante = {
      nombre_completo: generarNombreAleatorio(),
      id_paralelo: materia.id_paralelo,
    };
    
    const response = await api.post("/loginmenu/estudiante", nuevoEstudiante);
    console.log("✅ Estudiante agregado:", response.data);
    
    const notasIniciales = {};
    Object.keys(trimestres).forEach((trimestre) => {
      notasIniciales[trimestre] = {};
    });
    
    // ✅ Agregar estudiante con nombre aleatorio
    setEstudiantes([...estudiantes, { ...nuevoEstudiante, id_estudiante: response.data.id_estudiante, notas: notasIniciales }]);
  } catch (error) {
    console.error("❌ Error al agregar estudiante:", error);
  }
};
  
  const eliminarEstudiante = async (id_estudiante) => {
    try {
      
  
      await api.delete(`/loginmenu/estudiante/${id_estudiante}`);
      console.log(`✅ Estudiante con ID ${id_estudiante} eliminado`);
  
      // 🔄 Actualizar la UI eliminando el estudiante de la lista
      setEstudiantes(estudiantes.filter(est => est.id_estudiante !== id_estudiante));
    } catch (error) {
      console.error("❌ Error al eliminar estudiante:", error);
    }
  };

  const editarEstudiante = async (id_estudiante, nuevoNombre) => {
    try {
      await api.put(`/loginmenu/estudiante/${id_estudiante}`, {  nombre_completo: nuevoNombre  });
      console.log(`✅ Estudiante con ID ${id_estudiante} actualizado`);
  
      // 🔄 Actualizar la UI con el nuevo nombre
      setEstudiantes(estudiantes.map(est =>
        est.id_estudiante === id_estudiante ? { ...est, nombre_completo: nuevoNombre } : est
      ));
    } catch (error) {
      console.error("❌ Error al actualizar estudiante:", error);
    }
  }

  /** ✅ Agregar una actividad en el trimestre activo */
  const agregarActividad = async () => {
    if (!idTrimestreActivo) {
      console.error("❌ Error: No se puede agregar actividad sin un trimestre activo.");
      return;
    }
  
    try {
      const nuevaActividad = { nombre: `Actividad ${trimestres[tabActivo].actividades.length + 1}`, id_trimestre: idTrimestreActivo };
      const response = await api.post("/loginmenu/actividad", nuevaActividad);
  
      // ✅ Agregar actividad con la subactividad predeterminada generada en el backend
      setTrimestres((prevTrimestres) => ({
        ...prevTrimestres,
        [tabActivo]: {
          ...prevTrimestres[tabActivo],
          actividades: [
            ...prevTrimestres[tabActivo].actividades,
            {
              id_actividad: response.data.id_actividad,
              nombre: response.data.nombre_actividad,
              subactividades: [
                { id_subactividad: response.data.id_subactividad, nombre: response.data.nombre_subactividad }
              ]
            }
          ]
        }
      }));
    } catch (error) {
      console.error("❌ Error al agregar actividad:", error);
    }
  };
  


  const agregarSubactividad = async (actividadIndex) => {
    if (!idTrimestreActivo) {
      console.error("❌ Error: No se puede agregar subactividad sin un trimestre activo.");
      return;
    }

    try {
      const actividad = trimestres[tabActivo].actividades[actividadIndex];
      const nuevaSubactividad = { nombre: `Subactividad ${actividad.subactividades.length + 1}`, id_actividad: actividad.id_actividad };
      const response = await api.post("/loginmenu/subactividad", nuevaSubactividad);

      const nuevasActividades = [...trimestres[tabActivo].actividades];
      nuevasActividades[actividadIndex].subactividades.push({ id_subactividad: response.data.id_subactividad, nombre: nuevaSubactividad.nombre });

      setTrimestres({
        ...trimestres,
        [tabActivo]: {
          ...trimestres[tabActivo],
          actividades: nuevasActividades
        }
      });
    } catch (error) {
      console.error("❌ Error al agregar subactividad:", error);
    }
  };

  // Función para eliminar una actividad
  const eliminarActividad = async () => {
    if (menuContextual.actIndex !== null) {
      try {
        const actividadAEliminar = trimestres[tabActivo].actividades[menuContextual.actIndex];
        await api.delete(`/loginmenu/actividad/${actividadAEliminar.id_actividad}`);
        
        console.log(`✅ Actividad con ID ${actividadAEliminar.id_actividad} eliminada`);
        
        // 🔄 Actualizar el estado eliminando la actividad
        const nuevasActividades = [...trimestres[tabActivo].actividades];
        nuevasActividades.splice(menuContextual.actIndex, 1);
  
        setTrimestres({
          ...trimestres,
          [tabActivo]: {
            ...trimestres[tabActivo],
            actividades: nuevasActividades
          }
        });
  
        ocultarMenuContextual();
      } catch (error) {
        console.error("❌ Error al eliminar actividad:", error);
      }
    }
  };

  const eliminarSubactividad = async () => {
    if (menuContextual.actIndex !== null && menuContextual.subIndex !== null) {
      try {
        const actividad = trimestres[tabActivo].actividades[menuContextual.actIndex];
        const subactividadAEliminar = actividad.subactividades[menuContextual.subIndex];
  
        if (subactividadAEliminar.id_subactividad) {
          // ✅ Eliminar la subactividad del backend si tiene un ID válido
          await api.delete(`/loginmenu/subactividad/${subactividadAEliminar.id_subactividad}`);
          console.log(`✅ Subactividad con ID ${subactividadAEliminar.id_subactividad} eliminada`);
        }
  
        // 🔄 Actualizar el estado eliminando la subactividad
        const nuevasActividades = [...trimestres[tabActivo].actividades];
        nuevasActividades[menuContextual.actIndex].subactividades.splice(menuContextual.subIndex, 1);
  
        // ✅ Si la actividad ya no tiene subactividades, eliminar la actividad completa
        if (nuevasActividades[menuContextual.actIndex].subactividades.length === 0) {
          const actividadAEliminar = nuevasActividades[menuContextual.actIndex];
  
          if (actividadAEliminar.id_actividad) {
            // ✅ Eliminar la actividad del backend solo si tiene un ID válido
            await api.delete(`/loginmenu/actividad/${actividadAEliminar.id_actividad}`);
            console.log(`✅ Actividad con ID ${actividadAEliminar.id_actividad} eliminada`);
          }
  
          // 🔄 Eliminar la actividad del estado
          nuevasActividades.splice(menuContextual.actIndex, 1);
        }
  
        setTrimestres({
          ...trimestres,
          [tabActivo]: {
            ...trimestres[tabActivo],
            actividades: nuevasActividades
          }
        });
  
        ocultarMenuContextual();
      } catch (error) {
        console.error("❌ Error al eliminar subactividad o actividad:", error);
      }
    }
  };
  
  /** ✅ Editar una actividad en el backend */
  const editarActividad = async (id_actividad, nuevoNombre) => {
    try {
      await api.put(`/loginmenu/actividad/${id_actividad}`, { nombre: nuevoNombre });
      console.log(`✅ Actividad con ID ${id_actividad} actualizada`);
    } catch (error) {
      console.error("❌ Error al actualizar actividad:", error);
    }
  };
  
  /** ✅ Editar una subactividad en el backend */
  const editarSubactividad = async (id_subactividad, nuevoNombre) => {
    try {
      await api.put(`/loginmenu/subactividad/${id_subactividad}`, { nombre: nuevoNombre });
      console.log(`✅ Subactividad con ID ${id_subactividad} actualizada`);
    } catch (error) {
      console.error("❌ Error al actualizar subactividad:", error);
    }
  };
  

  const actualizarNota = async (id_estudiante, id_subactividad, nota) => {
    setEstudiantes((prevEstudiantes) =>
      prevEstudiantes.map((est) =>
        est.id_estudiante === id_estudiante
          ? {
              ...est,
              notas: {
                ...est.notas,
                [id_subactividad]: nota, 
              },
            }
          : est
      )
    );
};

const eliminarNota = async (id_estudiante, id_subactividad) => {
  try {
      await api.delete(`/loginmenu/calificaciondetalle/${id_estudiante}/${id_subactividad}`);
      console.log(`✅ Nota eliminada para el estudiante ${id_estudiante}, subactividad ${id_subactividad}`);
      
      actualizarNota(id_estudiante, id_subactividad, ""); // Actualiza el estado para reflejar el cambio
  } catch (error) {
      console.error("❌ Error al eliminar la nota:", error.response?.data?.detail || error.message);
  }
};
  
  
  
  /** ✅ Guardar una calificación en el backend */
  const guardarNota = async (id_estudiante, id_subactividad, nota) => {
    if (!id_estudiante || !id_subactividad) {
        console.error("❌ Error: ID de estudiante o subactividad faltante.");
        return;
    }

    try {
        const data = {
            id_estudiante,
            id_subactividad,
            nota_aporte: parseFloat(nota) // ✅ Se envía como número, asegurando que 0 se almacene bien
        };

        await api.post("/loginmenu/calificaciondetalle", data);
        console.log(`✅ Nota guardada correctamente: ${nota}`);
    } catch (error) {
        console.error("❌ Error al guardar la nota:", error.response?.data?.detail || error.message);
    }
};


  

const obtenerNota = async (id_estudiante, id_subactividad) => {
  try {
      const response = await api.get(`/loginmenu/calificaciondetalle/${id_estudiante}/${id_subactividad}`);
      console.log("✅ Nota obtenida:", response.data);

      // ✅ Si el valor es 0 o no existe, asegurarse de que sea 0.00
      return response.data.nota_aporte !== undefined
          ? parseFloat(response.data.nota_aporte).toFixed(2)
          : "";
  } catch (error) {
      console.error("❌ Error al obtener la nota:", error.response?.data?.detail || error.message);
      return "";  // ✅ Si hay error, mostrar 0.00
  }
};


  
  

  // Función para mostrar el menú contextual
  const mostrarMenuContextual = (event, tipo, actIndex, subIndex = null) => {
    event.preventDefault(); // Evita el menú del navegador
    setMenuContextual({
      visible: true,
      x: event.pageX,
      y: event.pageY,
      tipo,
      actIndex,
      subIndex
    });
  };

  return (
    <div className="grados-container">
      {isLoading || tabActivo === "" ? (
        <p>Cargando trimestres...</p>
      ) : (
      <>
      <h2>Calificaciones - {materia.grado} - {materia.materia} - {materia.paralelo} (Trimestre ID: {idTrimestreActivo || "N/A"})</h2>

      <div className="tab-bar">
        {Object.keys(trimestres).map((tab) => (
          <button key={tab} className={`tab-button ${tabActivo === tab ? "active" : ""}`} onClick={() => cambiarTab(tab)}>
            {tab}
          </button>
        ))}
      </div>

      {/* ✅ CONTENEDOR DESPLAZABLE SOLO PARA LA TABLA */}
      <div className="table-wrapper">
        {tabActivo === "Calificación Anual" ? (
          
          <table className="calificaciones-table">
            <thead>
              <tr>
                <th>#</th>
                <th style={{ width: "170px", minWidth: "170px", maxWidth: "170px", textAlign: "left" }}>Estudiantes</th>
                <th style={{ width: "100px", minWidth: "100px", maxWidth: "100px" }}>Primer Trimestre</th>
                <th style={{ width: "100px", minWidth: "100px", maxWidth: "100px" }}>Segundo Trimestre</th>
                <th style={{ width: "100px", minWidth: "100px", maxWidth: "100px" }}>Tercer Trimestre</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>TOTAL (70%)</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>Proyecto</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>Evaluacion</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>PROM (30%)</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>PROMEDIO</th>
                <th style={{ width: "70px", minWidth: "70px", maxWidth: "70px" }}>Estado</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>Supletorio</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>Cualitativa</th>
                <th style={{ width: "75px", minWidth: "75px", maxWidth: "75px" }}>Cuantitativa</th>
                <th style={{ width: "100px", minWidth: "100px", maxWidth: "100px" }}>PROMOCIÓN</th>
              </tr>
            </thead>
            <tbody>
              {estudiantes.map((estudiante, estIndex) => (
                <tr key={estIndex}>
                  <td>{estIndex + 1}</td>
                  <td className="esnon-editable">{estudiante.nombre}</td>
                  <td className="non-editable">0</td>
                  <td className="non-editable">0</td>
                  <td className="non-editable">0</td>
                  <td className="calculated-cell">0</td>
                  <td>
                    <input
                      type="text"
                      className="nota-input"
                      value={estudiante.notas.proyecto || ""}
                      onChange={(e) => {
                        let valor = e.target.value.replace(".", ",");
                        if (/^\d{0,2}(,\d{0,2})?$/.test(valor) || valor === "") {
                          const nuevasNotas = [...estudiantes];
                          nuevasNotas[estIndex].notas.proyecto = valor;
                          setEstudiantes(nuevasNotas);
                        }
                      }}
                      onBlur={(e) => {
                        let valor = e.target.value;
                        if (valor !== "" && /^\d{1,2}(,\d{1,2})?$/.test(valor)) {
                          let numero = parseFloat(valor.replace(",", ".")).toFixed(2).replace(".", ",");
                          const nuevasNotas = [...estudiantes];
                          nuevasNotas[estIndex].notas.proyecto = numero;
                          setEstudiantes(nuevasNotas);
                        }
                      }}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      className="nota-input"
                      value={estudiante.notas.evaluacion || ""}
                      onChange={(e) => {
                        let valor = e.target.value.replace(".", ",");
                        if (/^\d{0,2}(,\d{0,2})?$/.test(valor) || valor === "") {
                          const nuevasNotas = [...estudiantes];
                          nuevasNotas[estIndex].notas.evaluacion = valor;
                          setEstudiantes(nuevasNotas);
                        }
                      }}
                      onBlur={(e) => {
                        let valor = e.target.value;
                        if (valor !== "" && /^\d{1,2}(,\d{1,2})?$/.test(valor)) {
                          let numero = parseFloat(valor.replace(",", ".")).toFixed(2).replace(".", ",");
                          const nuevasNotas = [...estudiantes];
                          nuevasNotas[estIndex].notas.evaluacion = numero;
                          setEstudiantes(nuevasNotas);
                        }
                      }}
                    />
                  </td>

                  <td className="calculated-cell">0</td>
                  <td className="calculated-cell">0</td>
                  <td className="calculated-cell"></td>

                  <td>
                    <input
                      type="text"
                      className="nota-input"
                      onChange={(e) => {
                        const nuevasNotas = [...estudiantes];
                        nuevasNotas[estIndex].notas.supletorio = e.target.value;
                        setEstudiantes(nuevasNotas);
                      }}
                      value={estudiante.notas.supletorio || ""}
                    />
                  </td>
                  <td className="calculated-cell"></td>
                  <td className="calculated-cell">0</td>
                  <td className="calculated-cell"></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <table className="calificaciones-table">
          <thead>
            <tr>
              <th style={{ width: "30px", minWidth: "30px", maxWidth: "30px" }} rowSpan="2">#</th> {/* ✅ Nueva columna de numeración */}
              <th style={{ width: "170px", minWidth: "170px", maxWidth: "170px", textAlign: "left" }} rowSpan="2">Estudiantes</th>
              {trimestres[tabActivo]?.actividades?.map((actividad, actIndex) => (
                <th key={actIndex} colSpan={actividad.subactividades.length} className="actividad-cell"
                onContextMenu={(e) => mostrarMenuContextual(e, "actividad", actIndex)}>
                <span
                  contentEditable="true"
                  suppressContentEditableWarning={true}
                  onBlur={(e) => {
                    const nuevoNombre = e.target.innerText.trim();
                    if (nuevoNombre !== "") {
                      editarActividad(actividad.id_actividad, nuevoNombre);  // ✅ Actualiza en la BD
                      const nuevasActividades = [...trimestres[tabActivo].actividades];
                      nuevasActividades[actIndex].nombre = nuevoNombre;
                      setTrimestres({
                        ...trimestres,
                        [tabActivo]: { ...trimestres[tabActivo], actividades: nuevasActividades }
                      });
                    } else {
                      e.target.innerText = actividad.nombre;
                    }
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      e.target.blur();
                    }
                  }}
                >
                  {actividad.nombre}
                </span>
                <button className="add-btn" onClick={() => agregarSubactividad(actIndex)}>
                  <FaPlus />
                </button>
              </th>
              ))}

              <th style={{ width: "50px" }} rowSpan="2">PROMEDIO (70%)</th>
              <th style={{ width: "50px" }} rowSpan="2">PROYECTO INTERDISCIPLINAR F1</th>
              <th style={{ width: "50px" }} rowSpan="2">EVALUACIÓN</th>
              <th style={{ width: "50px" }} rowSpan="2">PROMEDIO (30%)</th>
              <th style={{ width: "50px" }} rowSpan="2">PROMEDIO CUANTITATIVO</th>
              <th style={{ width: "50px" }} rowSpan="2">PROMEDIO CUALITATIVO</th>
              <th style={{ width: "30px" }} rowSpan="2">Eliminar</th>
            </tr>

            <tr>
            {trimestres[tabActivo]?.actividades?.map((actividad, actIndex) =>
                actividad.subactividades.map((subact, subIndex) => (
                  <th 
                    key={`${actIndex}-${subIndex}`}
                    contentEditable="true"
                    suppressContentEditableWarning={true}
                    className="subactividad-cell"
                    onContextMenu={(e) => mostrarMenuContextual(e, "subactividad", actIndex, subIndex)}
                    onBlur={(e) => {
                      const nuevoNombre = e.target.innerText.trim();
                      if (nuevoNombre !== "") {
                        editarSubactividad(subact.id_subactividad, nuevoNombre);  // ✅ Actualiza en la BD
                        const nuevasActividades = [...trimestres[tabActivo].actividades];
                        nuevasActividades[actIndex].subactividades[subIndex].nombre = nuevoNombre;
                        setTrimestres({
                          ...trimestres,
                          [tabActivo]: { ...trimestres[tabActivo], actividades: nuevasActividades }
                        });
                      } else {
                        e.target.innerText = "";  // ✅ Ahora se queda vacía si no hay nombre
                      }
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        e.target.blur();
                      }
                    }}
                  >
                    {subact.nombre || "..."}
                  </th>
                ))
              )}
            </tr>

          </thead>

          <tbody>
            {estudiantes.map((estudiante, estIndex) => (
              
              <tr key={estIndex}>
                <td>{estIndex + 1}</td> {/* ✅ Celda de numeración */}
                <td 
                  className="estudiante-cell" contentEditable="true" suppressContentEditableWarning={true}
                  onBlur={(e) => {
                    const nuevoNombre = e.target.innerText.trim();
                    if (!nuevoNombre) {
                      // 🔹 Si el usuario deja la casilla vacía, restablecer el nombre original
                      e.target.innerText = estudiante.nombre_completo;
                    } else {
                      editarEstudiante(estudiante.id_estudiante, nuevoNombre);
                    }
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault(); // ✅ Evita el salto de línea en contentEditable
                      e.target.blur(); // ✅ Guarda el nombre cuando se presiona Enter
                    }
                  }} >
                  {estudiante.nombre_completo}
                </td>
                
                {trimestres[tabActivo]?.actividades?.map((actividad, actIndex) =>
                  actividad.subactividades.map((_, subIndex) => (
                   <td key={`${estIndex}-${actIndex}-${subIndex}`}>
                    <input 
                      type="text" 
                      className="nota-input"
                      placeholder="0.00"
                      value={
                        estudiante.notas[trimestres[tabActivo].actividades[actIndex].subactividades[subIndex].id_subactividad] ?? ""}
                        onChange={(e) => {
                          let valor = e.target.value.replace(",", ".");
                          if (/^\d{0,2}(\.\d{0,2})?$/.test(valor) || valor === "") {
                            actualizarNota(
                              estudiante.id_estudiante,
                              trimestres[tabActivo].actividades[actIndex].subactividades[subIndex].id_subactividad,
                              valor
                            );
                          }
                        }}
                        onBlur={(e) => {
                          let valor = e.target.value.trim();
                          if (valor === "" || isNaN(valor)) {
                            eliminarNota(
                              estudiante.id_estudiante,
                              trimestres[tabActivo].actividades[actIndex].subactividades[subIndex].id_subactividad
                            ); 
                          } else {
                            valor = parseFloat(valor).toFixed(2);
                            actualizarNota(
                              estudiante.id_estudiante,
                              trimestres[tabActivo].actividades[actIndex].subactividades[subIndex].id_subactividad, valor
                            );
                            guardarNota(
                              estudiante.id_estudiante,
                              trimestres[tabActivo].actividades[actIndex].subactividades[subIndex].id_subactividad,
                              valor
                            );
                          }
                        }}
                    />
                  </td>
                  ))
                )}

                <td className="promedio-cell">0</td>
                
                <td>
                  <input type="text" className="nota-input"
                    value={estudiante.evaluacion || ""}
                    onChange={(e) => {
                      let valor = e.target.value.replace(".", ",");
                      if (/^\d{0,2}(,\d{0,2})?$/.test(valor) || valor === "") {
                        const nuevasNotas = [...estudiantes];
                        nuevasNotas[estIndex].evaluacion = valor;
                        setEstudiantes(nuevasNotas);
                      }
                    }}
                    onBlur={(e) => {
                      let valor = e.target.value;
                      if (valor !== "" && /^\d{1,2}(,\d{1,2})?$/.test(valor)) {
                        let numero = parseFloat(valor.replace(",", ".")).toFixed(2).replace(".", ","); 
                        const nuevasNotas = [...estudiantes];
                        nuevasNotas[estIndex].evaluacion = numero;
                        setEstudiantes(nuevasNotas);
                      }
                    }}
                  />
                </td>
                
                <td>
                  <input type="text" className="nota-input" value={estudiante.promedio30 || ""} onChange={(e) => {
                    let valor = e.target.value.replace(".", ",");
                    if (/^\d{0,2}(,\d{0,2})?$/.test(valor) || valor === "") {
                      const nuevasNotas = [...estudiantes];
                      nuevasNotas[estIndex].promedio30 = valor;
                      setEstudiantes(nuevasNotas);
                    }
                  }}
                  onBlur={(e) => {
                    let valor = e.target.value;
                    if (valor !== "" && /^\d{1,2}(,\d{1,2})?$/.test(valor)) {
                      let numero = parseFloat(valor.replace(",", ".")).toFixed(2).replace(".", ","); 
                      const nuevasNotas = [...estudiantes];
                      nuevasNotas[estIndex].promedio30 = numero;
                      setEstudiantes(nuevasNotas);
                    }
                  }}
                  />
                </td>

                <td className="promedio-cell">0</td>
                <td className="promedio-cell">0</td>
                <td className="promedio-cell">0</td>
                <td className="delete-cell">
                  <button className="delete-btn" onClick={() => eliminarEstudiante(estudiante.id_estudiante)}>
                    <FaTrash />
                  </button>
                </td>

              </tr>
            ))}
          </tbody>

          </table>
        
        )}
        
        {tabActivo !== "Calificación Anual" && (
          <div className="buttons-container">
            <button className="agregar-button" onClick={agregarEstudiante}>
              <FaPlus /> Agregar Estudiante
            </button>
            
            <button className="agregar-button" onClick={agregarActividad}>
              <FaPlus /> Agregar Actividad
            </button>
          </div>
        )}
      </div>
      
      {menuContextual.visible && (
        <ul className="context-menu" style={{ top: menuContextual.y, left: menuContextual.x }} onClick={(e) => e.stopPropagation()}>
          {menuContextual.tipo === "actividad" && (
            <li onClick={() => { eliminarActividad(); ocultarMenuContextual(); }}>
              <FaTrash /> Eliminar Actividad
            </li>
          )}
          {menuContextual.tipo === "subactividad" && (
            <li onClick={() => { eliminarSubactividad(); ocultarMenuContextual(); }}>
              <FaTrash /> Eliminar Subactividad
            </li>
          )}
        </ul>
      )}
      </>
      )}
  
    </div>
  );

}

GradosMenu.propTypes = {
  materia: PropTypes.shape({
    id_materia: PropTypes.number.isRequired,
    id_paralelo: PropTypes.number, // ✅ Ahora incluye id_paralelo
    id_trimestre: PropTypes.number,
    grado: PropTypes.string.isRequired,
    paralelo: PropTypes.string.isRequired,
    materia: PropTypes.string.isRequired,
  }).isRequired,
};