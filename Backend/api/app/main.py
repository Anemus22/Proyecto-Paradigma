from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from api.app.database import Base, engine, get_db
from api.app.routes import docente, evaluacion, facultad, linea, programa
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Gestión Profesoral Pro",
    description=(
        "API REST organizada para la administración de docentes, programas, facultades, "
        "líneas de investigación y evaluaciones, con navegación por módulos y documentación automática."
    ),
    version="4.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Error de integridad: revisa claves duplicadas o relaciones foráneas."},
    )


@app.exception_handler(SQLAlchemyError)
async def sql_error_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"detail": "Error interno de base de datos."})


@app.get("/")
def root():
    return {
        "message": "API de Gestión Profesoral Pro",
        "version": "4.0.0",
        "status": "ok",
        "navigation": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "resumen": "/api/v1/resumen",
            "facultades": "/api/v1/facultades",
            "lineas": "/api/v1/lineas",
            "programas": "/api/v1/programas",
            "docentes": "/api/v1/docentes",
            "evaluaciones": "/api/v1/evaluaciones",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/resumen")
def resumen():
    from api.app.database import SessionLocal
    from api.app.models import Facultad, LineaInvestigacion, Programa, Docente, EvaluacionDocente

    db = SessionLocal()
    try:
        return {
            "facultades": db.query(Facultad).count(),
            "lineas": db.query(LineaInvestigacion).count(),
            "programas": db.query(Programa).count(),
            "docentes": db.query(Docente).count(),
            "evaluaciones": db.query(EvaluacionDocente).count(),
        }
    finally:
        db.close()


app.include_router(facultad.router, prefix="/api/v1")
app.include_router(linea.router, prefix="/api/v1")
app.include_router(programa.router, prefix="/api/v1")
app.include_router(docente.router, prefix="/api/v1")
app.include_router(evaluacion.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    # Esto inicia el servidor y lo mantiene abierto
    uvicorn.run("api.app.main:app", host="127.0.0.1", port=8000, reload=True)
