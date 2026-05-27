from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.models import LineaInvestigacion
from api.app.schemas import LineaCreate, LineaRead, LineaUpdate

router = APIRouter(prefix="/lineas", tags=["02. Líneas de investigación"])


@router.get("/", response_model=list[LineaRead])
def listar(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
    return db.query(LineaInvestigacion).order_by(LineaInvestigacion.id).offset(skip).limit(limit).all()


@router.post("/", response_model=LineaRead, status_code=status.HTTP_201_CREATED)
def crear(payload: LineaCreate, db: Session = Depends(get_db)):
    nuevo = LineaInvestigacion(**payload.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear la línea de investigación")
    db.refresh(nuevo)
    return nuevo


@router.put("/{linea_id}", response_model=LineaRead)
def actualizar(linea_id: int, payload: LineaUpdate, db: Session = Depends(get_db)):
    linea = db.query(LineaInvestigacion).filter(LineaInvestigacion.id == linea_id).first()
    if not linea:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(linea, campo, valor)
    db.commit()
    db.refresh(linea)
    return linea


@router.delete("/{linea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(linea_id: int, db: Session = Depends(get_db)):
    linea = db.query(LineaInvestigacion).filter(LineaInvestigacion.id == linea_id).first()
    if not linea:
        raise HTTPException(status_code=404, detail="Línea no encontrada")
    db.delete(linea)
    db.commit()
    return None
