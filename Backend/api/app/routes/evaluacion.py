from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models import Docente, EvaluacionDocente
from schemas import EvaluacionCreate, EvaluacionRead, EvaluacionUpdate

router = APIRouter(prefix="/evaluaciones", tags=["05. Evaluaciones"])


@router.get("/", response_model=list[EvaluacionRead])
def listar(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return (
        db.query(EvaluacionDocente)
        .order_by(EvaluacionDocente.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/", response_model=EvaluacionRead, status_code=status.HTTP_201_CREATED)
def crear(payload: EvaluacionCreate, db: Session = Depends(get_db)):
    docente = db.query(Docente).filter(Docente.cedula == payload.docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail="No existe el docente asociado")

    nueva = EvaluacionDocente(
        calificacion=payload.calificacion,
        semestre=payload.semestre,
        docente=payload.docente,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/{evaluacion_id}", response_model=EvaluacionRead)
def obtener(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(EvaluacionDocente).filter(EvaluacionDocente.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion


@router.put("/{evaluacion_id}", response_model=EvaluacionRead)
def actualizar(evaluacion_id: int, payload: EvaluacionUpdate, db: Session = Depends(get_db)):
    evaluacion = db.query(EvaluacionDocente).filter(EvaluacionDocente.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    cambios = payload.model_dump(exclude_unset=True)
    if "docente" in cambios:
        docente = db.query(Docente).filter(Docente.cedula == cambios["docente"]).first()
        if not docente:
            raise HTTPException(status_code=404, detail="No existe el docente asociado")

    for campo, valor in cambios.items():
        setattr(evaluacion, campo, valor)

    db.commit()
    db.refresh(evaluacion)
    return evaluacion


@router.delete("/{evaluacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(EvaluacionDocente).filter(EvaluacionDocente.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    db.delete(evaluacion)
    db.commit()
    return None
