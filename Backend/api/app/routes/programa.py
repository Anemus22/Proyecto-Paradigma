from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Facultad, Programa
from schemas import ProgramaCreate, ProgramaRead, ProgramaUpdate

router = APIRouter(prefix="/programas", tags=["03. Programas"])


@router.get("/", response_model=list[ProgramaRead])
def listar(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    q: str | None = Query(None, min_length=1, max_length=100),
):
    query = db.query(Programa)
    if q:
        filtro = f"%{q.strip()}%"
        query = query.filter(Programa.nombre.ilike(filtro))
    return query.order_by(Programa.id).offset(skip).limit(limit).all()


@router.get("/{programa_id}", response_model=ProgramaRead)
def obtener(programa_id: int, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa


@router.post("/", response_model=ProgramaRead, status_code=status.HTTP_201_CREATED)
def crear(payload: ProgramaCreate, db: Session = Depends(get_db)):
    if payload.facultad_id is not None:
        facultad = db.query(Facultad).filter(Facultad.id == payload.facultad_id).first()
        if facultad is None:
            raise HTTPException(status_code=404, detail="La facultad indicada no existe")

    nuevo = Programa(**payload.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear el programa")
    db.refresh(nuevo)
    return nuevo


@router.put("/{programa_id}", response_model=ProgramaRead)
def actualizar(programa_id: int, payload: ProgramaUpdate, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    cambios = payload.model_dump(exclude_unset=True)
    if "facultad_id" in cambios and cambios["facultad_id"] is not None:
        facultad = db.query(Facultad).filter(Facultad.id == cambios["facultad_id"]).first()
        if facultad is None:
            raise HTTPException(status_code=404, detail="La facultad indicada no existe")

    for campo, valor in cambios.items():
        setattr(programa, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo actualizar el programa")
    db.refresh(programa)
    return programa


@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(programa_id: int, db: Session = Depends(get_db)):
    programa = db.query(Programa).filter(Programa.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    db.delete(programa)
    db.commit()
    return None
