from sqlalchemy.orm import Session
from typing import Optional
from FastApiGeoAlert.app.models import Alerta
import FastApiGeoAlert.app.schemas as schemas

def crear_alerta(db: Session, alerta: schemas.AlertaCreate):
    nueva = Alerta(**alerta.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_alertas(db: Session, skip: int = 0, limit: int = 10, categoria: Optional[str] = None, activo: Optional[bool] = None):
    query = db.query(Alerta)
    if categoria:
        query = query.filter(Alerta.categoria == categoria)
    if activo is not None:
        query = query.filter(Alerta.activo == activo)
    return query.offset(skip).limit(limit).all()

def obtener_alerta(db: Session, alerta_id: int):
    return db.query(Alerta).filter(Alerta.id == alerta_id).first()

def actualizar_alerta(db: Session, alerta_id: int, datos: schemas.AlertaUpdate):
    alerta = obtener_alerta(db, alerta_id)
    if alerta:
        for key, value in datos.model_dump(exclude_unset=True).items():
            setattr(alerta, key, value)
        db.commit()
        db.refresh(alerta)
    return alerta

def eliminar_alerta(db: Session, alerta_id: int):
    alerta = obtener_alerta(db, alerta_id)
    if alerta:
        db.delete(alerta)
        db.commit()
    return alerta
