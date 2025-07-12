from FastApiGeoAlert.app.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    categoria = Column(String)
    nivel_alerta = Column(Integer)
    activo = Column(Boolean, default=True)
