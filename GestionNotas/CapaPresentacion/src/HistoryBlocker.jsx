import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export function HistoryBlocker() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token"); // Verifica si el usuario está autenticado
  const currentSection = localStorage.getItem("currentSection"); // Sección actual del usuario

  useEffect(() => {
    const handlePopState = () => {
      const protectedPaths = ["/institucion", "/gestionGrados", "/seccionMenu"];
      
      // Si el usuario está autenticado y accede a "/login", redirigir a la sección actual
      if (token && location.pathname === "/") {
        navigate(currentSection || "/institucion", { replace: true });
        return;
      }

      // Bloquear retroceso o avance hacia rutas no válidas
      if (token && !protectedPaths.includes(location.pathname)) {
        navigate(currentSection || "/institucion", { replace: true });
      }
    };

    // Escucha cambios en el historial
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("popstate", handlePopState);
    };
  }, [navigate, location, token, currentSection]);

  return null;
}

