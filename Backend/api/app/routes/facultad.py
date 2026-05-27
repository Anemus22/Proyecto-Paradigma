from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.models import Facultad
from api.app.schemas import FacultadCreate, FacultadRead, FacultadUpdate

router = APIRouter(prefix="/facultades", tags=["01. Facultades"])


@router.get("/", response_model=list[FacultadRead])
def listar(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
    return db.query(Facultad).order_by(Facultad.id).offset(skip).limit(limit).all()


@router.post("/", response_model=FacultadRead, status_code=status.HTTP_201_CREATED)
def crear(payload: FacultadCreate, db: Session = Depends(get_db)):
    nuevo = Facultad(**payload.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear la facultad")
    db.refresh(nuevo)
    return nuevo


@router.put("/{facultad_id}", response_model=FacultadRead)
def actualizar(facultad_id: int, payload: FacultadUpdate, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(facultad, campo, valor)
    db.commit()
    db.refresh(facultad)
    return facultad


@router.delete("/{facultad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(Facultad).filter(Facultad.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    db.delete(facultad)
    db.commit()
    return None
