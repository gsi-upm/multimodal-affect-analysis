from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware  # Importamos el middleware CORS

app= FastAPI()
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen. Puedes especificar dominios concretos si lo prefieres.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(router)
