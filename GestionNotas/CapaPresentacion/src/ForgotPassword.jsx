import { useState} from "react";
import api from "./api";
import { useNavigate } from 'react-router-dom'; // Importamos useNavigate
import "./ForgotPassword.css";

export function ForgotPassword() {
  const [correo, setCorreo] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // Inicializa navigate



  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");
    try {
      const response = await api.post("/usuarios/recuperar-password", { correo });
      setMensaje(response.data.mensaje);
    } catch (error) {
      setError(error.response?.data?.detail || "Ocurrió un error.");
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-box">
        <h2>Recuperar Contraseña</h2>
        <p>Ingresa tu correo y te enviaremos un enlace para restablecer tu contraseña.</p>
        {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Correo electrónico"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
          />
          <button type="submit">Enviar</button>
        </form>
  
        <a onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>Volver al inicio de sesión</a>
      </div>
    </div>
  );
}