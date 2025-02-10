import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "./api";
import "./ResetPassword.css";

export function ResetPassword() {
  const { token } = useParams(); // Recibe el token desde la URL
  const [contraseña, setContraseña] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setError("");
    try {
      const response = await api.post("/usuarios/reset-password", { token, contraseña });
      setMensaje(response.data.mensaje); // Mensaje de éxito
      setTimeout(() => navigate("/"), 3000); // Redirige al login después de 3 segundos
    } catch (error) {
      setError(error.response?.data?.detail || "Ocurrió un error.");
    }
  };

  return (
    <div className="reset-password-container">
      <div className="reset-password-box">
        <h2>Restablecer Contraseña</h2>
        <p>Ingresa tu nueva contraseña.</p>
        {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            placeholder="Nueva Contraseña"
            value={contraseña}
            onChange={(e) => setContraseña(e.target.value)}
            required
          />
          <button type="submit">Restablecer Contraseña</button>
        </form>
      </div>
    </div>
  );
}
