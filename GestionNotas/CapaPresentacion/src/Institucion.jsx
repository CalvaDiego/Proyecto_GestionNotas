import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Importa el hook useNavigate
import './Institucion.css';
import api from './api';

export function Institucion() {
  const [formData, setFormData] = useState({
    nombre: '',
    lugar: '',
    imagen_institucion: '',
    grados: [],
  });
  const [gradoInputs, setGradoInputs] = useState(['']);
  const [errores, setErrores] = useState({});
  const navigate = useNavigate(); // Hook para redirigir

  // Establecer la sección actual en localStorage
  useEffect(() => {
    localStorage.setItem('currentSection', '/institucion');
  }, []); // Se ejecuta solo una vez al montar el componente

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    if (errores[name]) {
      setErrores((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleImageChange = (e) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setFormData({ ...formData, imagen_institucion: reader.result.split(',')[1] });
    };
    reader.readAsDataURL(e.target.files[0]);
  };

  const handleGradoChange = (index, value) => {
    const nuevosGrados = [...gradoInputs];
    nuevosGrados[index] = value;
    setGradoInputs(nuevosGrados);
  };

  const agregarGrado = () => setGradoInputs([...gradoInputs, '']);
  const eliminarGrado = (index) => setGradoInputs(gradoInputs.filter((_, i) => i !== index));

  const handleSubmit = async (e) => {
    e.preventDefault();
    const grados = gradoInputs.map((grado) => ({ nombre: grado }));

    try {
      await api.post('/instituciones', { ...formData, grados }); // Se elimina la asignación a response

      localStorage.setItem("currentSection", "/gestionGrados");
      navigate("/gestionGrados", { replace: true });
    
    } catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        setErrores({ general: error.response.data.detail });
      } else {
        setErrores({ general: 'Error inesperado al crear la institución.' });
      }
    }
  };

  return (
    <div className="institucion-container">
      <h1>Registrar Institución</h1>
      <div className="institucion-box">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Nombre de la Institución</label>
            <input
              type="text"
              name="nombre"
              className="institucion-input"
              value={formData.nombre}
              onChange={handleChange}
              placeholder="Ej: Colegio Ejemplar"
              required
            />
          </div>

          <div className="input-group">
            <label>Lugar</label>
            <input
              type="text"
              name="lugar"
              className="institucion-input"
              value={formData.lugar}
              onChange={handleChange}
              placeholder="Ej: Quito, Ecuador"
              required
            />
          </div>

          <div className="image-upload">
            <label>Imagen de la Institución</label>
            <input type="file" accept="image/*" required onChange={handleImageChange} />
          </div>

          <div className="input-group">
            <label>Grados</label>
            {gradoInputs.map((grado, index) => (
              <div key={index} className="grado-input">
                <input
                  type="text"
                  value={grado}
                  className="institucion-input"
                  onChange={(e) => handleGradoChange(index, e.target.value)}
                  placeholder={`Grado ${index + 1}`}
                  required
                />
                <button
                  type="button"
                  className="grado-remove"
                  onClick={() => eliminarGrado(index)}
                >
                  Eliminar
                </button>
              </div>
            ))}
            <button type="button" className="grado-add" onClick={agregarGrado}>
              + Agregar Grado
            </button>
          </div>

          <button type="submit" className="institucion-button">
            Crear Institución
          </button>
          {errores.general && <p className="error-message">{errores.general}</p>}
        </form>
      </div>
    </div>
  );
}
