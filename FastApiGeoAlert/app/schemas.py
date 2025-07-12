from pydantic import BaseModel, ConfigDict
from typing import Optional

class AlertaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    titulo: str
    descripcion: Optional[str] = None
    latitud: float
    longitud: float
    categoria: str
    nivel_alerta: Optional[int] = 1
    activo: Optional[bool] = True

class AlertaCreate(AlertaBase):
    pass

class AlertaUpdate(BaseModel):
    """
    Schema for updating an alert.

    Attributes:
        titulo (Optional[str]): The title of the alert.
        descripcion (Optional[str]): A description of the alert.
        latitud (Optional[float]): Latitude coordinate of the alert location.
        longitud (Optional[float]): Longitude coordinate of the alert location.
        categoria (Optional[str]): Category of the alert.
        nivel_alerta (Optional[int]): Alert level (severity or priority).
        activo (Optional[bool]): Indicates if the alert is active.
    """
    model_config = ConfigDict(from_attributes=True)
    titulo: Optional[str]
    descripcion: Optional[str]
    latitud: Optional[float]
    longitud: Optional[float]
    categoria: Optional[str]
    nivel_alerta: Optional[int]
    activo: Optional[bool]

class AlertaOut(AlertaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
