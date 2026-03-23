from fastapi import FastAPI
from .routes import router as enrollments_router
app = FastAPI(
    title="Sistema Universitario Mendoza",
    description="API para gestión de inscripciones conectada a Odoo 19",
    version="1.0.0"
)

app.include_router(enrollments_router, prefix="/api", tags=["Gestión Académica"])

@app.get("/", tags=["Sistema"])
async def root():

    return {
        "status": "online",
        "message": "API Universitaria Mendoza Funcionando",
        "docs": "/docs"
    }