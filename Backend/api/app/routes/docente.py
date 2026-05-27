from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Docente, LineaInvestigacion
from schemas import DocenteCreate, DocenteRead, DocenteUpdate

router = APIRouter(prefix="/docentes", tags=["04. Docentes"])


@router.get("/", response_model=list[DocenteRead])
def listar(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    q: str | None = Query(None, min_length=1, max_length=100),
):
    query = db.query(Docente)
    if q:
        filtro = f"%{q.strip()}%"
        query = query.filter(
            (Docente.nombres.ilike(filtro))
            | (Docente.apellidos.ilike(filtro))
            | (Docente.correo.ilike(filtro))
        )
    return query.order_by(Docente.cedula).offset(skip).limit(limit).all()


@router.get("/{cedula}", response_model=DocenteRead)
def obtener(cedula: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.cedula == cedula).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente


@router.post("/", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
def crear(docente: DocenteCreate, db: Session = Depends(get_db)):
    if docente.linea_investigacion_principal is not None:
        linea = db.query(LineaInvestigacion).filter(LineaInvestigacion.id == docente.linea_investigacion_principal).first()
        if linea is None:
            raise HTTPException(status_code=404, detail="La línea de investigación principal no existe")

    nuevo = Docente(**docente.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo crear el docente. La cédula o el correo ya existen.",
        )
    db.refresh(nuevo)
    return nuevo


@router.put("/{cedula}", response_model=DocenteRead)
def actualizar(cedula: int, datos: DocenteUpdate, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.cedula == cedula).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    cambios = datos.model_dump(exclude_unset=True)
    if "linea_investigacion_principal" in cambios and cambios["linea_investigacion_principal"] is not None:
        linea = db.query(LineaInvestigacion).filter(LineaInvestigacion.id == cambios["linea_investigacion_principal"]).first()
        if linea is None:
            raise HTTPException(status_code=404, detail="La línea de investigación principal no existe")

    for campo, valor in cambios.items():
        setattr(docente, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo actualizar el docente. El correo probablemente ya existe.",
        )
    db.refresh(docente)
    return docente


@router.delete("/{cedula}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(cedula: int, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.cedula == cedula).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    db.delete(docente)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el docente porque tiene registros relacionados.",
        )
    return None
