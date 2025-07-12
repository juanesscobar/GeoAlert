from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import FastApiGeoAlert.app.models as models, FastApiGeoAlert.app.schemas as schemas, FastApiGeoAlert.app.crud as crud
from FastApiGeoAlert.app.database import SessionLocal, engine
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="GeoAlert API", description="API para gestionar alertas georreferenciadas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Crear las tablas en la base de datos

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GeoAlert API", description="API para gestionar alertas georreferenciadas")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/alertas", response_model=schemas.AlertaOut, status_code=status.HTTP_201_CREATED)
def crear_alerta(alerta: schemas.AlertaCreate, db: Session = Depends(get_db)):
    return crud.crear_alerta(db, alerta)

@app.get("/alertas", response_model=List[schemas.AlertaOut])
def listar_alertas(skip: int = 0, limit: int = 10, categoria: Optional[str] = None, activo: Optional[bool] = None, db: Session = Depends(get_db)):
    if limit > 100:
        limit = 100
    return crud.obtener_alertas(db, skip, limit, categoria, activo)


@app.get("/alertas/{alerta_id}", response_model=schemas.AlertaOut)
def obtener_alerta(alerta_id: int, db: Session = Depends(get_db)):
    alerta = crud.obtener_alerta(db, alerta_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta

@app.put("/alertas/{alerta_id}", response_model=schemas.AlertaOut)
def actualizar_alerta(alerta_id: int, datos: schemas.AlertaUpdate, db: Session = Depends(get_db)):
    alerta = crud.actualizar_alerta(db, alerta_id, datos)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta

@app.delete("/alertas/{alerta_id}")
def eliminar_alerta(alerta_id: int, db: Session = Depends(get_db)):
    alerta = crud.eliminar_alerta(db, alerta_id)
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": f"Alerta {alerta_id} eliminada correctamente"}

# --- Inserta aquí el nuevo endpoint ---

SENTINEL_CLIENT_ID = "5b0f9bcc-9ec3-4f01-9398-3e6e4287cb7f"
SENTINEL_CLIENT_SECRET = "2AYIzZM82bjBhy51GFdEFuDScaAln4jp"
SENTINEL_TOKEN_URL = "https://services.sentinel-hub.com/oauth/token"

async def obtener_token_sentinel():
    data = {
        "grant_type": "client_credentials",
        "client_id": SENTINEL_CLIENT_ID,
        "client_secret": SENTINEL_CLIENT_SECRET
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(SENTINEL_TOKEN_URL, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="No se pudo obtener el token de Sentinel Hub")
        return response.json()["access_token"]

@app.get("/sentinel/imagenes")
async def obtener_imagenes_sentinel(bbox: str, fecha: str):
    token = await obtener_token_sentinel()
    url = "https://services.sentinel-hub.com/api/v1/catalog/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "bbox": [float(x) for x in bbox.split(",")],
        "datetime": f"{fecha}T00:00:00Z/{fecha}T23:59:59Z",
        "collections": ["sentinel-2-l1c"]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Error consultando Sentinel Hub: {response.text}")
        data = response.json()
        if not data.get("features"):
            return {"mensaje": "No se encontraron imágenes para los parámetros dados."}
        return data
