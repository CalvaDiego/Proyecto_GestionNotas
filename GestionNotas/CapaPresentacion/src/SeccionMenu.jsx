import { useState, useEffect } from "react";
import "./SeccionMenu.css";
import { useNavigate } from "react-router-dom";
import { FaHome, FaChalkboardTeacher, FaChartBar, FaHistory, FaBell, FaUser } from "react-icons/fa";
import api from "./api";
import { LoginMenu } from "./LoginMenu"; // Importa el componente LoginMenu
import { GradosMenu } from "./GradosMenu";

export function SeccionMenu() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeSection, setActiveSection] = useState("Inicio");
  const [showNotificationDropdown, setShowNotificationDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const [showGradosDropdown, setShowGradosDropdown] = useState(false);
  const [showMateriasDropdown, setShowMateriasDropdown] = useState(null);
  const [showParalelosDropdown, setShowParalelosDropdown] = useState(null);
  const [selectedMateria, setSelectedMateria] = useState(null); // ✅ Nuevo estado
  const [userInfo, setUserInfo] = useState({ fullName: "", correo: "" });
  const [materias, setMaterias] = useState({});
  const [paralelos, setParalelos] = useState({});
  const [grados, setGrados] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.setItem("currentSection", "/seccionMenu");

    const fetchUserInfo = async () => {
      try {
        const response = await api.get("/usuarios/perfil");
        const { nombre, apellido, correo } = response.data;
        const fullName = `${nombre.split(" ")[0]} ${apellido.split(" ")[0]}`;
        setUserInfo({ fullName, correo });
      } catch (error) {
        console.error("Error al obtener los datos del usuario:", error);
      }
    };

    fetchUserInfo();
    
  }, []);

  const fetchGrados = async () => {
    try {
      const response = await api.get("/loginmenu/");
      console.log("Datos recibidos:", response.data);

      const gradosData = response.data.grados || [];

      const materiasData = {};
      const paralelosData = {};

      gradosData.forEach(grado => {
        materiasData[grado.nombre] = grado.materias.map(m => ({
          id_materia: m.id_materia,
          nombre: m.nombre,
          trimestres: m.trimestres.map(t => ({
            id_trimestre: t.id_trimestre,
            nombre: t.nombre,
          })) // ✅ Se incluyen los trimestres
        }));

        paralelosData[grado.nombre] = grado.paralelos.map(p => ({
          id_paralelo: p.id_paralelo,
          nombre: p.nombre,
        }));
      });

      setGrados(gradosData);
      setMaterias(materiasData);
      setParalelos(paralelosData);
    } catch (err) {
      console.error("Error al cargar los datos:", err);
      setError("Error al cargar los datos.");
    }
  };

  useEffect(() => {
    fetchGrados();
  }, []);

  useEffect(() => {
    fetchGrados();
  }, []);

  const handleMateriaClick = (materia, grado, paraleloNombre) => {
    const paraleloObj = paralelos[grado]?.find(p => p.nombre === paraleloNombre);

    // ✅ Obtener el primer trimestre por defecto si existe
    const primerTrimestre = materia.trimestres.length > 0 ? materia.trimestres[0] : null;

    setSelectedMateria({
      id_materia: materia.id_materia,
      id_paralelo: paraleloObj?.id_paralelo || null,
      materia: materia.nombre,
      grado,
      paralelo: paraleloNombre,
      id_trimestre: primerTrimestre?.id_trimestre || null, // ✅ Guardar id_trimestre
    });

    setActiveSection("Grados");
  };

  const toggleMenu = () => setIsCollapsed(!isCollapsed);

  const handleSectionClick = (section) => {
    if (section === "Grados") {
      setShowGradosDropdown(!showGradosDropdown);
      fetchGrados();
    } else {
      setShowGradosDropdown(false);
      setShowMateriasDropdown(null);
      setShowParalelosDropdown(null);
      setActiveSection(section);
    }
};

  const closeDropdowns = () => {
    setShowNotificationDropdown(false);
    setShowUserDropdown(false);
    setShowGradosDropdown(false); // Cierra el menú desplegable de Grados
    setShowMateriasDropdown(null);
     setShowParalelosDropdown(null);
  };

  const renderSectionContent = () => {
    if (activeSection === "Inicio") {
      return <LoginMenu />;
    }
    if (activeSection === "Grados" && selectedMateria) { 
      return <GradosMenu materia={selectedMateria} />;
    }
    return <p>Sección no implementada aún.</p>;
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="app-container" onClick={closeDropdowns}>
      {/* Header */}
      <header className="header" onClick={(e) => e.stopPropagation()}>
        <h1>EduCalifica</h1>
        <div className="header-icons">
          {/* Icono de notificación */}
          <div
            className={`dropdown-container ${showNotificationDropdown ? "active" : ""}`}
          >
            <FaBell
              className={`icon ${showNotificationDropdown ? "active-icon" : ""}`}
              onClick={(e) => {
                e.stopPropagation();
                setShowNotificationDropdown(!showNotificationDropdown);
                setShowUserDropdown(false);
              }}
            />
            {showNotificationDropdown && (
              <div className="dropdown-panel">
                <p>No tienes nuevas notificaciones</p>
              </div>
            )}
          </div>
          {/* Icono de usuario */}
          <div
            className={`dropdown-container ${showUserDropdown ? "active" : ""}`}
          >
            <FaUser
              className={`icon ${showUserDropdown ? "active-icon" : ""}`}
              onClick={(e) => {
                e.stopPropagation();
                setShowUserDropdown(!showUserDropdown);
                setShowNotificationDropdown(false);
              }}
            />
            {showUserDropdown && (
              <div className="dropdown-panel">
                <p>
                  <strong>Nombre:</strong> {userInfo.fullName || "No disponible"}
                </p>
                <p>
                  <strong>Correo:</strong> {userInfo.correo || "No disponible"}
                </p>
                <button className="logout-button" onClick={handleLogout}>
                  Cerrar sesión
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-content">
        <nav className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
          <button className="menu-toggle" onClick={toggleMenu}>
            ☰
          </button>
          <ul>
            <li className={activeSection === "Inicio" ? "active" : ""} onClick={() => handleSectionClick("Inicio")}>
              <FaHome className="menu-icon" />
              {!isCollapsed && <span className="menu-text">Inicio</span>}
            </li>
            
            <li className={`menu-item`} onClick={(e) => { e.stopPropagation(); handleSectionClick("Grados");}}>
              <FaChalkboardTeacher className="menu-icon" />
              {!isCollapsed && <span className="menu-text">Grados</span>}
              
              {showGradosDropdown && (
                <ul className="submenu">
                  {error ? (
                    <li>{error}</li>
                  ) : grados.length > 0 ? (
                    grados.map((grado, index) => (
                    <li key={index} className="submenu-item" onMouseEnter={() => setShowParalelosDropdown(index)}>
                      {grado.nombre}
                      <span className="arrow">&gt;</span>
                      {showParalelosDropdown === index && (
                        <ul className="paralelos-submenu">
                          {(paralelos[grado.nombre] && paralelos[grado.nombre].length > 0) ? (
                            paralelos[grado.nombre].map((paralelo, j) => (
                            <li key={j} className="submenu-itemUno" onMouseEnter={() => setShowMateriasDropdown(j)}>
                              {paralelo.nombre} 
                              <span className="arrowUno">&gt;</span>
                              {showMateriasDropdown === j && (
                                <ul className="materias-submenu">
                                  {(materias[grado.nombre] && materias[grado.nombre].length > 0) ? (
                                    materias[grado.nombre].map((materia, i) => (
                                    <li key={i} onClick={() => handleMateriaClick(materia, grado.nombre, paralelo.nombre)}>{materia.nombre}</li>
                                    ))
                                  ) : (
                                  <li>No hay materias</li>
                                  )}
                                </ul>
                              )}
                            </li>
                            ))
                          ) : (
                          <li>No hay paralelos</li>
                          )}
                        </ul>
                      )}
                    </li>
                    ))
                  ) : (
                  <li>No hay grados</li>
                  )}
                </ul>
              )}
            </li>


            <li
              className={activeSection === "Reportes" ? "active" : ""}
              onClick={() => handleSectionClick("Reportes")}
            >
              <FaChartBar className="menu-icon" />
              {!isCollapsed && <span className="menu-text">Reportes</span>}
            </li>
            <li
              className={activeSection === "Historial" ? "active" : ""}
              onClick={() => handleSectionClick("Historial")}
            >
              <FaHistory className="menu-icon" />
              {!isCollapsed && <span className="menu-text">Historial</span>}
            </li>
          </ul>
        </nav>

        {/* Content */}
        <div className="content-wrapper">
          <div className="content">{renderSectionContent()}</div>
        </div>
      </div>
    </div>
  );
}