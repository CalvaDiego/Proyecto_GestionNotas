import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Login } from "./Login";
import { Register } from "./Register";
import { ForgotPassword } from "./ForgotPassword";
import { ResetPassword } from "./ResetPassword";
import { Institucion } from "./Institucion";
import { GestionGrados } from "./GestionGrados";
import { SeccionMenu } from "./SeccionMenu";
import { ProtectedRoute } from "./ProtectedRoute";
import { HistoryBlocker } from "./HistoryBlocker";

ReactDOM.createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <HistoryBlocker />
      <Routes>
        {/* Rutas públicas */}
        <Route
          path="/"
          element={
            <ProtectedRoute isPublic>
              <Login />
            </ProtectedRoute>
          }
        />
        <Route
          path="/register"
          element={
            <ProtectedRoute isPublic>
              <Register />
            </ProtectedRoute>
          }
        />
        <Route
          path="/forgotPassword"
          element={
            <ProtectedRoute isPublic>
              <ForgotPassword />
            </ProtectedRoute>
          }
        />
        <Route
          path="/resetPassword/:token"
          element={
            <ProtectedRoute isPublic>
              <ResetPassword />
            </ProtectedRoute>
          }
        />

        {/* Rutas protegidas */}
        <Route
          path="/institucion"
          element={
            <ProtectedRoute>
              <Institucion />
            </ProtectedRoute>
          }
        />
        <Route
          path="/gestionGrados"
          element={
            <ProtectedRoute>
              <GestionGrados />
            </ProtectedRoute>
          }
        />
        <Route
          path="/seccionMenu"
          element={
            <ProtectedRoute>
              <SeccionMenu />
            </ProtectedRoute>
          }
        />

        {/* Ruta por defecto (catch-all) */}
        <Route
          path="*"
          element={
            <Navigate to={localStorage.getItem("currentSection") || "/"} replace />
          }
        />
      </Routes>
    </Router>
  </StrictMode>
);



/*
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
//import { Institucion } from './Institucion';
//import { Register } from './Register';
//import { ForgotPassword } from './ForgotPassword';
//import { ResetPassword } from './ResetPassword';
import { GestionGrados } from './GestionGrados';

//import { Login } from './Login';


createRoot(document.getElementById('root')).render(
  <StrictMode>
    < GestionGrados />

  </StrictMode>
);
*/