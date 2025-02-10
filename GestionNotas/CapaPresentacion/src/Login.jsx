import './Login.css';
import { useState} from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

export function Login() {
  const [formData, setFormData] = useState({
    correo: '',
    contraseña: '',
  });

  const [errores, setErrores] = useState({});
  const navigate = useNavigate(); // Hook para redirigir
  

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Actualizar estado del formulario
    setFormData({ ...formData, [name]: value });

    // Limpiar errores específicos
    if (errores[name]) {
      setErrores((prevErrores) => ({ ...prevErrores, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post('/usuarios/login', formData);
      console.log('Inicio de sesión exitoso:', response.data);


       // Guardar el token en localStorage
       localStorage.setItem('token', response.data.access_token);

      const initialSection = response.data.completado ? "/seccionMenu" : "/institucion";
      localStorage.setItem("currentSection", initialSection);
      navigate(initialSection, { replace: true });
    } catch (error) {
      const nuevosErrores = {};
      if (error.response?.data?.detail) {
        const errorMsg = error.response.data.detail;
        if (errorMsg.includes('Correo')) {
          nuevosErrores.correo = errorMsg;
        } else if (errorMsg.includes('Contraseña')) {
          nuevosErrores.contraseña = errorMsg;
        }
      }
      setErrores(nuevosErrores); // Actualizar errores
    }
  };

  return (
    <div className="container">
      <div className="info">
        <h1>EduCalifica</h1>
        <p>
          Organiza calificaciones, genera libretas y predice el éxito académico
          de tus estudiantes.
        </p>
      </div>
      <div className="login-box">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <input
              type="email"
              name="correo"
              placeholder="Correo Electrónico"
              value={formData.correo}
              onChange={handleChange}
              required
              className={`login-input ${errores.correo ? 'input-error' : ''}`}
            />
            {errores.correo && (
              <div className="error-message">{errores.correo}</div>
            )}
          </div>
          <div className="input-group">
            <input
              type="password"
              name="contraseña"
              placeholder="Contraseña"
              value={formData.contraseña}
              onChange={handleChange}
              required
              className={`login-input ${errores.contraseña ? 'input-error' : ''}`}
            />
            {errores.contraseña && (
              <div className="error-message">{errores.contraseña}</div>
            )}
          </div>
          <button type="submit" className="login-button">Iniciar Sesión</button>
          <a onClick={() => navigate('/forgotPassword')} style={{ cursor: 'pointer' }}
           className="forgot-password">¿Olvidaste tu contraseña?</a>
          <button
            type="button"
            className="create-account-button"
            onClick={() => navigate('/register')}
          >
            Crear cuenta
          </button>
        </form>
      </div>
    </div>
  );
}
