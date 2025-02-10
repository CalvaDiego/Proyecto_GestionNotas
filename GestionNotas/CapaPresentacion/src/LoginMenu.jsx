import { useState, useEffect } from "react";
import "./LoginMenu.css";
import api from "./api";
import { FaEdit, FaPlus, FaTrash  } from "react-icons/fa";

export function LoginMenu() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState({});
  const [editMateriaMode, setEditMateriaMode] = useState(false);
  const [editMateriaData, setEditMateriaData] = useState({});
  const [showAddModal, setShowAddModal] = useState(false); // Controlar modal para agregar
  const [newParalelo, setNewParalelo] = useState(""); // Nombre del nuevo paralelo
  const [showAddMateriaModal, setShowAddMateriaModal] = useState(false); // Modal para agregar materia
  const [newMateria, setNewMateria] = useState("");
  const [selectedArea, setSelectedArea] = useState("");
  const [areas, setAreas] = useState([]);
  const [showAddGradoModal, setShowAddGradoModal] = useState(false); // Controla la visibilidad del modal
  const [newGrado, setNewGrado] = useState(""); // Almacena el nombre del nuevo grado

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/loginmenu/");
        console.log("Datos cargados desde la API:", response.data); // Verifica la estructura aquí
        setData(response.data);
        setLoading(false);
      } catch (err) {
        console.error("Error al cargar los datos:", err);
        setError("Error al cargar los datos.");
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleDeleteGrado = async (idGrado) => {
  try {
    // Enviar la solicitud DELETE al backend
    await api.delete(`/loginmenu/grado/${idGrado}`);
    
    // Actualizar el estado eliminando el grado de la lista
    setData((prevData) => ({
      ...prevData,
      grados: prevData.grados.filter((grado) => grado.id_grado !== idGrado),
    }));
    console.log(`Grado con ID ${idGrado} eliminado con éxito.`);
  } catch (err) {
    console.error("Error al eliminar el grado:", err);
    alert("Hubo un error al eliminar el grado. Intenta nuevamente.");
  }
};

  const handleAddGrado = async () => {
    if (!newGrado.trim()) {
      alert("El nombre del grado no puede estar vacío.");
      return;
    }
  
    const institutionId = data?.institucion?.id_institucion;
    if (!institutionId) {
      console.error("ID de institución no encontrado. Verifica los datos:", data);
      alert("No se encontró el ID de la institución. Intenta recargar la página.");
      return;
    }
  
    try {
      const response = await api.post("/loginmenu/grado", {
        nombre: newGrado,
        id_institucion: institutionId,
      });
  
      // Actualizar el estado con el nuevo grado
      setData((prevData) => ({
        ...prevData,
        grados: [
          ...prevData.grados,
          {
            id_grado: response.data.id_grado, // ID del grado desde el backend
            nombre: newGrado, // Nombre del grado ingresado
            paralelos: [], // Inicialmente sin paralelos
            materias: [], // Inicialmente sin materias
          },
        ],
      }));
  
      // Limpiar y cerrar el modal
      setShowAddGradoModal(false);
      setNewGrado("");
    } catch (err) {
      console.error("Error al agregar el grado:", err);
    }
  };

  const handleDeleteMateria = async (idMateria, idGrado) => {
    try {
      await api.delete(`/loginmenu/materia/${idMateria}`);
      setData((prevData) => ({
        ...prevData,
        grados: prevData.grados.map((grado) =>
          grado.id_grado === idGrado
            ? {
                ...grado,
                materias: grado.materias.filter(
                  (materia) => materia.id_materia !== idMateria
                ),
              }
            : grado
        ),
      }));
    } catch (err) {
      console.error("Error al eliminar la materia:", err);
    }
  };

  const handleDeleteParalelo = async (idParalelo, idGrado) => {
    try {
      await api.delete(`/loginmenu/paralelo/${idParalelo}`);
      setData((prevData) => ({
        ...prevData,
        grados: prevData.grados.map((grado) =>
          grado.id_grado === idGrado
            ? {
                ...grado,
                paralelos: grado.paralelos.filter(
                  (paralelo) => paralelo.id_paralelo !== idParalelo
                ),
              }
            : grado
        ),
      }));
    } catch (err) {
      console.error("Error al eliminar el paralelo:", err);
    }
  };
  

  const handleEditMateriaSave = async () => {
    try {
      const { id, currentName, selectedArea } = editMateriaData;
      await api.put(`/loginmenu/materia/${id}`, {
        nombre: currentName,
        id_area: selectedArea,
      });
  
      // Actualizar estado local
      setData((prevData) => ({
        ...prevData,
        grados: prevData.grados.map((grado) => ({
          ...grado,
          materias: grado.materias.map((materia) =>
            materia.id_materia === id
              ? { ...materia, nombre: currentName, id_area: selectedArea }
              : materia
          ),
        })),
      }));
  
      setEditMateriaMode(false); // Cerrar el modal
    } catch (err) {
      console.error("Error al editar la materia:", err);
    }
  };


  useEffect(() => {
    const fetchAreas = async () => {
      try {
        const response = await api.get("/loginmenu/areas");
        setAreas(response.data);
      } catch (err) {
        console.error("Error al cargar las áreas:", err);
      }
    };
    fetchAreas();
  }, []);

  const handleAddMateria = async (gradoId) => {
    if (!newMateria.trim() || !selectedArea) {
      alert("Debe completar el área y el nombre de la materia.");
      return;
    }
    try {
      const response = await api.post("/loginmenu/materia", {
        nombre: newMateria,
        id_area: selectedArea,
        id_grado: gradoId,
      });
      setData((prevData) => ({
        ...prevData,
        grados: prevData.grados.map((grado) =>
          grado.id_grado === gradoId
            ? {
                ...grado,
                materias: [
                  ...grado.materias,
                  { id_materia: response.data.id_materia, nombre: newMateria },
                ],
              }
            : grado
        ),
      }));
      setShowAddMateriaModal(false);
      setNewMateria("");
      setSelectedArea("");
    } catch (err) {
      console.error("Error al agregar la materia:", err);
    }
  };

  const handleAddParalelo = async (gradoId) => {
    if (!newParalelo.trim()) {
      alert("El nombre del paralelo no puede estar vacío.");
      return;
    }
    try {
      const response = await api.post("/loginmenu/paralelo", {
        nombre: newParalelo,
        id_grado: gradoId,
      });
      setData((prevData) => ({
        ...prevData,
        grados: prevData.grados.map((grado) =>
          grado.id_grado === gradoId
            ? {
                ...grado,
                paralelos: [
                  ...grado.paralelos,
                  { id_paralelo: response.data.id_paralelo, nombre: newParalelo },
                ],
              }
            : grado
        ),
      }));
      setShowAddModal(false);
      setNewParalelo("");
    } catch (err) {
      console.error("Error al agregar el paralelo:", err);
    }
  };

  

  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = async () => {
      try {
        const base64Image = reader.result.split(",")[1]; // Convertir a Base64
        // Enviar al backend
        await api.put("/loginmenu/institucion", {
          nombre: data.institucion.nombre, // Mantener el nombre actual
          imagen_institucion: base64Image, // Enviar la nueva imagen en Base64
        });

        // Actualizar el estado con la nueva imagen
        setData((prevData) => ({
          ...prevData,
          institucion: {
            ...prevData.institucion,
            imagen: base64Image, // Reemplazar la imagen en el estado
          },
        }));
      } catch (err) {
        console.error("Error al actualizar la imagen:", err);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleEditClick = (type, id, currentName, areaId) => {
    if (type === "materia") {
      setEditMateriaData({ id, currentName, selectedArea: areaId });
      setEditMateriaMode(true);
    } else {
      setEditData({ type, id, currentName });
      setEditMode(true);
    }
  };

  const handleEditSave = async () => {
    try {
      const { type, id, currentName } = editData;
      let endpoint;

      switch (type) {
        case "institucion":
          endpoint = `/loginmenu/institucion`;
          await api.put(endpoint, { nombre: currentName });
          setData((prevData) => ({
            ...prevData,
            institucion: { ...prevData.institucion, nombre: currentName },
          }));
          break;
        case "grado":
          endpoint = `/loginmenu/grado/${id}`;
          await api.put(endpoint, { nombre: currentName });
          setData((prevData) => ({
            ...prevData,
            grados: prevData.grados.map((grado) =>
              grado.id_grado === id ? { ...grado, nombre: currentName } : grado
            ),
          }));
          break;
        case "paralelo":
          endpoint = `/loginmenu/paralelo/${id}`;
          await api.put(endpoint, { nombre: currentName });
          setData((prevData) => ({
            ...prevData,
            grados: prevData.grados.map((grado) => ({
              ...grado,
              paralelos: grado.paralelos.map((paralelo) =>
                paralelo.id_paralelo === id
                  ? { ...paralelo, nombre: currentName }
                  : paralelo
              ),
            })),
          }));
          break;

        default:
          throw new Error("Tipo de edición no válido");
      }

      setEditMode(false);
    } catch (err) {
      console.error("Error al guardar los cambios:", err);
    }
  };

  if (loading) return <p>Cargando datos...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="login-menu-container">
      <h2>
        Institución: {data.institucion.nombre}{" "}
        <button
          className="edit-institucion-button"
          onClick={() =>
            handleEditClick("institucion", data.institucion.id_institucion, data.institucion.nombre)
          }
        >
          <FaEdit />
        </button>
      </h2>

      <div className="login-menu-image-container">
        {data.institucion.imagen && (
          <img
          src={`data:image/png;base64,${data.institucion.imagen}`}
          alt="Logo de la institución"
          className="login-menu-institucion-imagen"
          />
        )}
        <div className="login-menu-file-container">
          <label htmlFor="fileInput">Cambiar imagen</label>
          <input
          id="fileInput"
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          />
        </div>
      </div>
      
      <div className="login-menu-grados-titulo-container">
        <h3 className="login-menu-grados-titulo">Grados</h3>
        <button className="login-menu-add-grado-button" onClick={() => setShowAddGradoModal(true)}>
          <FaPlus />
        </button>
      </div>
      
      <div className="login-menu-grados-container">
        {data.grados.map((grado) => (
          <div key={grado.id_grado} className="login-menu-grado-card">
            <h3>
              {grado.nombre}{" "}

              <button className="edit-grado-button" onClick={() => handleEditClick("grado", grado.id_grado, grado.nombre)}>
                <FaEdit />
              </button>
              
              <button className="delete-grado-button" onClick={() => handleDeleteGrado(grado.id_grado)}>
                <FaTrash />
              </button>

            </h3>
            <p>
              <strong>Paralelos: {" "}
                <button
                className="login-menu-add-button"
                onClick={() => setShowAddModal(grado.id_grado)}
                >
                  <FaPlus />
                </button>
              </strong>
              <ul className="login-menu-paralelos">
                {grado.paralelos.map((paralelo) => (
                  <li key={paralelo.id_paralelo} className="paralelo-item">
                    <span>{paralelo.nombre}{" "} </span>

                    <div>
                      <button className="edit-paralelo-button" onClick={() => handleEditClick("paralelo", paralelo.id_paralelo, paralelo.nombre)}>
                        <FaEdit />
                      </button>
                      <button className="delete-button" onClick={() => handleDeleteParalelo(paralelo.id_paralelo, grado.id_grado)}>
                        <FaTrash />
                      </button>
                    </div>
                    
                  </li>
                ))}
              </ul>
            </p>
            <p>
              <strong>Materias:{" "}
                <button
                className="login-menu-add-button"
                onClick={() => setShowAddMateriaModal(grado.id_grado)}
                >
                  <FaPlus />
                </button>
              </strong>
              <ul className="login-menu-materias">
                {grado.materias.map((materia) => (
                  <li key={materia.id_materia} className="materia-item">
                    <span>{materia.nombre}{" "} </span>

                    <div>
                      <button className="edit-materia-button" onClick={() => handleEditClick("materia", materia.id_materia, materia.nombre)}>
                        <FaEdit />
                      </button>
                      <button className="delete-button" onClick={() => handleDeleteMateria(materia.id_materia, grado.id_grado)}>
                        <FaTrash />
                      </button>
                    </div>
                    

                  </li>
                ))}
              </ul>
            </p>
          </div>
        ))}
      </div>
      
      {editMode && (
        <div className="login-menu-modal">
          <div className="login-menu-modal-content">
            <h3 className="login-menu-modal-title">Editar {editData.type}</h3>
            <input type="text" className="login-menu-modal-input" value={editData.currentName} onChange={(e) =>
            setEditData((prev) => ({ ...prev, currentName: e.target.value }))} placeholder={`Nuevo nombre para ${editData.type}`}/>
            <div className="login-menu-modal-actions">
              <button className="login-menu-modal-save" onClick={handleEditSave}>
                Guardar
              </button>
              <button className="login-menu-modal-close" onClick={() => setEditMode(false)}>
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
      
      {showAddModal && (
        <div className="add-paralelo-modal">
          <div className="add-paralelo-modal-content">
            <h3 className="add-paralelo-modal-title">Agregar Paralelo</h3>
            <input type="text" className="add-paralelo-modal-input" value={newParalelo} 
            onChange={(e) => setNewParalelo(e.target.value)} placeholder="Nombre del paralelo"/>
            <div className="add-paralelo-modal-actions">
              <button className="add-paralelo-modal-save" onClick={() => handleAddParalelo(showAddModal)}>
                Guardar
              </button>
              <button className="add-paralelo-modal-close" onClick={() => setShowAddModal(false)}>
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
      
      {showAddMateriaModal && (
        <div className="materia-modal">
          <div className="materia-modal-content">
            <h3 className="materia-modal-title">Agregar Materia</h3> {/* Título del modal */}
            <table className="materia-modal-table">
              <thead>
                <tr>
                  <th className="materia-modal-header">Área</th>
                  <th className="materia-modal-header">Materia</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="materia-modal-cell">
                    <select className="materia-modal-select" value={selectedArea} onChange={(e) => setSelectedArea(e.target.value)}>
                      <option value="">Selecciona un área</option>
                      {areas.map((area) => (
                        <option key={area.id_area} value={area.id_area}>
                          {area.nombre}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="materia-modal-cell">
                    <input type="text" className="materia-modal-input" value={newMateria} onChange={(e) => setNewMateria(e.target.value)} placeholder="Nombre de la materia"/>
                  </td>
                </tr>
              </tbody>
            </table>
            <div className="materia-modal-actions">
              <button className="materia-modal-save" onClick={() => handleAddMateria(showAddMateriaModal)}>
                Guardar
              </button>
              <button className="materia-modal-close" onClick={() => setShowAddMateriaModal(false)}>
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
      
      {editMateriaMode && (
        <div className="edit-materia-modal">
          <div className="edit-materia-modal-content">
            <h3 className="edit-materia-modal-title">Editar Materia</h3>
            <table className="edit-materia-modal-table">
              <thead>
                <tr>
                  <th className="edit-materia-modal-header">Área</th>
                  <th className="edit-materia-modal-header">Nombre</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="edit-materia-modal-cell">
                    <select
                    className="edit-materia-modal-select" value={editMateriaData.selectedArea || ""} onChange={(e) => setEditMateriaData((prev) => ({
                      ...prev, selectedArea: e.target.value, }))}>
                        <option value="">Selecciona un área</option>
                        {areas.map((area) => (
                          <option key={area.id_area} value={area.id_area}>
                            {area.nombre}
                            </option>
                        ))}
                    </select>
                  </td>
                  <td className="edit-materia-modal-cell">
                    <input type="text" className="edit-materia-modal-input" value={editMateriaData.currentName || ""} onChange={(e) =>
                    setEditMateriaData((prev) => ({ ...prev, currentName: e.target.value, }))} placeholder="Nombre de la materia"/>
                  </td>
                </tr>
              </tbody>
            </table>
            <div className="edit-materia-modal-actions">
              <button className="edit-materia-modal-save" onClick={handleEditMateriaSave}>
                Guardar
              </button>
              <button className="edit-materia-modal-close" onClick={() => setEditMateriaMode(false)}>
                Cancelar
              </button>
            </div>
          </div>
        </div>)}
        
        {showAddGradoModal && (
          <div className="add-grado-modal">
            <div className="add-grado-modal-content">
              <h3 className="add-grado-modal-title">Agregar Grado</h3>
              <input type="text" className="add-grado-modal-input" value={newGrado} onChange={(e) => setNewGrado(e.target.value)} placeholder="Nombre del grado"/>
              <div className="add-grado-modal-actions">
                <button className="add-grado-modal-save" onClick={handleAddGrado}>
                  Guardar
                </button>
                <button className="add-grado-modal-close" onClick={() => setShowAddGradoModal(false)}>
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        )}


    </div>
  );
}
