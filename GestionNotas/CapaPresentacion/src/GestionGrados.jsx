import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Importar para redirigir
import api from "./api";
import "./GestionGrados.css";

export function GestionGrados() {
  const [grados, setGrados] = useState([]);
  const [areas, setAreas] = useState([]); // Áreas para la asignación de materias
  const [selectedGrado, setSelectedGrado] = useState(null);
  const [modalContent, setModalContent] = useState(""); // Controla qué modal mostrar
  const [paralelos, setParalelos] = useState([""]); // Lista de paralelos
  const [materias, setMaterias] = useState([{ nombre: "", area: "" }]); // Lista de materias
  const [error, setError] = useState("");
  const navigate = useNavigate(); // Hook para redirigir

  useEffect(() => {
    // Establece la sección actual
    localStorage.setItem("currentSection", "/gestionGrados");
  }, []);

  // Lista fija de materias sugeridas
  const materiasSugeridas = [
    "Matemáticas",
    "Lengua y Literatura",
    "Ciencias Naturales",
    "Física",
    "Química",
    "Historia",
    "Geografía",
    "Arte",
    "Educación Física",
    "Informática",
  ];

  useEffect(() => {
    const fetchGrados = async () => {
      try {
        const response = await api.get("/gestionGrados/");
        setGrados(response.data);
      } catch (error) {
        console.error("Error al cargar los grados:", error);
      }
    };

    const fetchAreas = async () => {
      try {
        const response = await api.get("/gestionGrados/areas/");
        setAreas(response.data);
      } catch (error) {
        console.error("Error al cargar las áreas:", error);
      }
    };

    fetchGrados();
    fetchAreas();
  }, []);

  const openModal = (grado, type) => {
    setSelectedGrado(grado);
    setModalContent(type);
    setParalelos([""]);
    setMaterias([{ nombre: "", area: "" }]);
    setError("");
  };

  const closeModal = () => {
    setSelectedGrado(null);
    setModalContent("");
    setParalelos([""]);
    setMaterias([{ nombre: "", area: "" }]);
    setError("");
  };

  // Paralelos
  const handleAddParaleloInput = () => {
    if (paralelos.length >= 10) {
      setError("Solo puedes agregar hasta 10 paralelos.");
      return;
    }
    setParalelos([...paralelos, ""]);
  };

  const handleRemoveParaleloInput = (index) => {
    const updatedParalelos = paralelos.filter((_, i) => i !== index);
    setParalelos(updatedParalelos);
  };

  const handleChangeParalelo = (index, value) => {
    const regex = /^[A-Z]$/;
    if (regex.test(value) || value === "") {
      const updatedParalelos = [...paralelos];
      updatedParalelos[index] = value;
      setParalelos(updatedParalelos);
    }
  };

  const handleSaveParalelos = async () => {
    try {
      for (const paralelo of paralelos) {
        if (!paralelo.trim()) {
          setError("Todos los campos de paralelo deben estar llenos.");
          return;
        }

        if (!/^[A-Z]$/.test(paralelo)) {
          setError("Todos los paralelos deben ser una sola letra mayúscula (A-Z).");
          return;
        }
      }

      await Promise.all(
        paralelos.map((paralelo) =>
          api.post("/gestionGrados/paralelos/", {
            nombre: paralelo,
            id_grado: selectedGrado.id_grado,
          })
        )
      );

      closeModal();
    } catch (error) {
      console.error("Error al guardar los paralelos:", error);
      setError("Error al guardar los paralelos.");
    }
  };

  // Materias
  const handleAddMateriaRow = () => {
    if (materias.length >= 10) {
      setError("Solo puedes agregar hasta 10 materias.");
      return;
    }
    setMaterias([...materias, { nombre: "", area: "" }]);
  };

  const handleRemoveMateriaRow = (index) => {
    const updatedMaterias = materias.filter((_, i) => i !== index);
    setMaterias(updatedMaterias);
  };

  const handleChangeMateria = (index, field, value) => {
    const updatedMaterias = [...materias];
    updatedMaterias[index][field] = value;
    if (field === "nombre") {
      updatedMaterias[index].suggestions = getSuggestions(value);
    }
    setMaterias(updatedMaterias);
  };

  const handleSaveMaterias = async () => {
    try {
      for (const materia of materias) {
        if (!materia.nombre.trim() || !materia.area) {
          setError("Todos los campos de materia y área deben estar llenos.");
          return;
        }
      }

      await Promise.all(
        materias.map((materia) =>
          api.post("/gestionGrados/materias/", {
            nombre: materia.nombre,
            id_area: parseInt(materia.area),
            id_grado: selectedGrado.id_grado,
          })
        )
      );

      closeModal();
    } catch (error) {
      console.error("Error al guardar las materias:", error);
      setError("Error al guardar las materias.");
    }
  };



   // Función para obtener sugerencias basadas en la entrada del usuario
   const getSuggestions = (inputValue) => {
    if (!inputValue.trim()) return [];
    return materiasSugeridas.filter((materia) =>
      materia.toLowerCase().startsWith(inputValue.toLowerCase())
    );
  };

  const handleFinalizeProcess = async() => {
    await api.put('/usuarios/completado');
    localStorage.setItem("currentSection", "/seccionMenu");
    navigate("/seccionMenu", { replace: true });
  };



  const isSingleCard = grados.length === 1;

  return (
    <div className="gestion-grados-container">
      <h1>Gestión de Grados</h1>
      <div  className="grados-wrapper">
        <div className={`grados-grid ${isSingleCard ? "single-card" : ""}`}>
          {grados.map((grado) => (
            <div key={grado.id_grado} className="grado-card">
              <h2>{grado.nombre}</h2>
              <button onClick={() => openModal(grado, "paralelo")}>Agregar Paralelo</button>
              <button onClick={() => openModal(grado, "materia")}>Agregar Materia</button>
              </div>
            ))}
        </div>
        {/* Botón Finalizar Proceso */}
        <button className="finalizar-proceso-button" onClick={handleFinalizeProcess}>
          Finalizar Proceso
        </button>
      </div>
      

      {/* Modal */}
      {selectedGrado && modalContent === "paralelo" && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>{`Agregar Paralelos al ${selectedGrado.nombre}`}</h2>
            {error && <p className="error-message">{error}</p>}
            <button className="add-button" onClick={handleAddParaleloInput}>
              + Añadir paralelo
            </button>
            {paralelos.map((paralelo, index) => (
              <div key={index} className="paralelo-input-group">
                <input
                  type="text"
                  placeholder="Escribe una letra (A-Z)"
                  maxLength={1}
                  value={paralelo}
                  className={paralelo === "" ? "input-error" : ""}
                  onChange={(e) => handleChangeParalelo(index, e.target.value)}
                />
                <button
                  className="trash-button"
                  onClick={() => handleRemoveParaleloInput(index)}
                >
                  🗑️
                </button>
              </div>
            ))}
            <div className="modal-actions">
              <button className="save-button" onClick={handleSaveParalelos}>
                Guardar
              </button>
              <button className="close-modal" onClick={closeModal}>
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {selectedGrado && modalContent === "materia" && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>{`Agregar Materias al ${selectedGrado.nombre}`}</h2>
            {error && <p className="error-message">{error}</p>}
            <button className="add-button" onClick={handleAddMateriaRow}>
              + Añadir Materia
            </button>
            <table className="materias-table">
              <thead>
                <tr>
                  <th>Área</th>
                  <th>Materia</th>
                  <th>Eliminar</th>
                </tr>
              </thead>
              <tbody>
                {materias.map((materia, index) => (
                  <tr key={index}>
                     <td>
                      <select
                        value={materia.area}
                        onChange={(e) => handleChangeMateria(index, "area", e.target.value)}
                        onBlur={() => {
                          setTimeout(
                            () =>
                              handleChangeMateria(index, "suggestions", []),
                            200
                          );
                        }}
                      >
                        <option value="">Selecciona un área</option>
                        {areas.map((area) => (
                          <option key={area.id_area} value={area.id_area}>
                            {area.nombre}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td style={{ position: "relative" }}>
                      <input
                        type="text"
                        placeholder="Nombre de la materia"
                        value={materia.nombre}
                        onChange={(e) => handleChangeMateria(index, "nombre", e.target.value)}
                      />
                      {materia.suggestions?.length > 0 && (
                        <ul className="suggestions-dropdown">
                          {materia.suggestions.map((suggestion, suggestionIndex) => (
                            <li
                              key={suggestionIndex}
                              onClick={() => {
                                handleChangeMateria(index, "nombre", suggestion);
                                handleChangeMateria(index, "suggestions", []);
                              }}
                            >
                              {suggestion}
                            </li>
                          ))}
                        </ul>
                      )}
                    </td>
                   

                    <td>
                      <button
                        className="trash-button"
                        onClick={() => handleRemoveMateriaRow(index)}
                      >
                        🗑️
                      </button>
                    </td>
                    
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="modal-actions">
              <button className="save-button" onClick={handleSaveMaterias}>
                Guardar
              </button>
              <button className="close-modal" onClick={closeModal}>
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
