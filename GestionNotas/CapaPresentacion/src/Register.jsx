import './Register.css';
import { useState} from 'react';
import { useNavigate } from 'react-router-dom'; // Importamos useNavigate
import api from './api';

export function Register() {
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    correo: '',
    contraseña: '',
    genero: '',
  });

  const [mensaje, setMensaje] = useState('');
  const [errores, setErrores] = useState({});
  const navigate = useNavigate(); // Inicializa navigate


  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Limpia el error específico si el usuario comienza a corregirlo
    if (errores[name]) {
      setErrores((prevErrores) => ({ ...prevErrores, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/usuarios/registrar', formData);
      setMensaje('Usuario registrado exitosamente.');
      console.log(response.data);
    } catch (error) {
      if (error.response?.data?.detail) {
        const nuevosErrores = {};
        if (error.response.data.detail.includes('nombre')) {
          nuevosErrores.nombre = error.response.data.detail;
        }
        if (error.response.data.detail.includes('apellido')) {
          nuevosErrores.apellido = error.response.data.detail;
        }
        if (error.response.data.detail.includes('correo')) {
          nuevosErrores.correo = error.response.data.detail;
        }
        if (error.response.data.detail.includes('contraseña')) {
          nuevosErrores.contraseña = error.response.data.detail;
        }
        if (error.response.data.detail.includes('género') || error.response.data.detail.includes('genero')) {
          nuevosErrores.genero = error.response.data.detail;
        }
        setErrores(nuevosErrores); // Actualiza solo los errores relevantes
      } else {
        setMensaje('Ocurrió un error al registrar el usuario.');
        console.error(error);
      }
    }
  };

  return (
    <div className="register-container">
      <h1>EduCalifica</h1>
      <div className="register-box">
        <h2>Crear una cuenta</h2>
        {mensaje && <p>{mensaje}</p>}
        <form onSubmit={handleSubmit}>
          <div className="name-fields">
            <div>
              <input
                type="text"
                name="nombre"
                placeholder="Nombres"
                title="Ejemplo: Diego Armando"
                required
                className={`register-input ${errores.nombre ? 'input-error' : ''}`}
                value={formData.nombre}
                onChange={handleChange}
              />
              {errores.nombre && (
                <div className="error-message">{errores.nombre}</div>
              )}
            </div>
            <div>
              <input
                type="text"
                name="apellido"
                placeholder="Apellidos"
                title="Ejemplo: Calva Chuquimarca"
                required
                className={`register-input ${errores.apellido ? 'input-error' : ''}`}
                value={formData.apellido}
                onChange={handleChange}
              />
              {errores.apellido && (
                <div className="error-message">{errores.apellido}</div>
              )}
            </div>
          </div>
          <div className="email-container">
            <input
              type="email"
              name="correo"
              placeholder="Correo"
              title="Ejemplo: usuario@ejemplo.com"
              required
              className={`register-input ${errores.correo ? 'input-error' : ''}`}
              value={formData.correo}
              onChange={handleChange}
            />
            {errores.correo && (
              <div className="error-message">{errores.correo}</div>
            )}
          </div>
          <div className="password-container">
            <input
              type="password"
              name="contraseña"
              placeholder="Contraseña"
              title="Mínimo 6 caracteres, incluyendo una mayúscula, un número y un carácter especial."
              required
              className={`register-input ${errores.contraseña ? 'input-error' : ''}`}
              value={formData.contraseña}
              onChange={handleChange}
            />
            {errores.contraseña && (
              <div className="error-message">{errores.contraseña}</div>
            )}
          </div>
          <div className="gender-field">
            <label>
              <input
                type="radio"
                name="genero"
                value="Masculino"
                checked={formData.genero === 'Masculino'}
                onChange={handleChange}
              />
              Masculino
            </label>
            <label>
              <input
                type="radio"
                name="genero"
                value="Femenino"
                checked={formData.genero === 'Femenino'}
                onChange={handleChange}
              />
              Femenino
            </label>
            {errores.genero && (
              <div className="error-message">{errores.genero}</div>
            )}
          </div>
          <button type="submit" className="register-button">
            Crear cuenta
          </button>
        </form>
        <div className="login-link">
          ¿Ya tienes una cuenta?{' '}
          <a onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
            Iniciar Sesión
          </a>
        </div>
      </div>
    </div>
  );
}
