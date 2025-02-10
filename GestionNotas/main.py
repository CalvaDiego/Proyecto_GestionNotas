from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from CapaPresentacion.usuario_rutas import router as usuario_router
from CapaPresentacion.institucion_rutas import router as institucion_rutas
from CapaPresentacion.gestionGrados_rutas import router as gestion_grados_rutas
from CapaPresentacion.loginmenu_rutas import router as loginmenu_router  # Importar rutas de loginmenu




app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes de origen (puedes restringirlo a dominios específicos)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Registrar las rutas de usuario
app.include_router(usuario_router)

app.include_router(institucion_rutas)

# Registrar las rutas de gestión de grados
app.include_router(gestion_grados_rutas)

app.include_router(loginmenu_router)  # Registrar rutas de loginmenu





@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API del Sistema de Calificaciones"}