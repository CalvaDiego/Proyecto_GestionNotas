import { Navigate, useLocation } from "react-router-dom";
import PropTypes from "prop-types";

export function ProtectedRoute({ children, isPublic = false }) {
  const token = localStorage.getItem("token"); // Verifica si el usuario está autenticado
  const currentSection = localStorage.getItem("currentSection"); // Obtiene la sección actual del usuario
  const location = useLocation();

  // Rutas públicas, como "/login", "/register", "/forgotPassword", etc.
  if (isPublic) {
    // Bloquear acceso a rutas públicas si el usuario está autenticado
    if (token) {
      return <Navigate to={currentSection || "/institucion"} replace />;
    }
    return children; // Si no está autenticado, permite el acceso a rutas públicas
  }

  // Rutas protegidas: solo accesibles si el usuario está autenticado
  if (!token) {
    return <Navigate to="/" replace />;
  }

  // Si la ruta actual no coincide con la sección asignada, redirige a la sección actual
  if (currentSection && location.pathname !== currentSection) {
    return <Navigate to={currentSection} replace />;
  }

  return children; // Si todo es válido, renderiza el contenido
}

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired,
  isPublic: PropTypes.bool, // Define si la ruta es pública
};
