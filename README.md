# GeoAlert API 🚨🌍

Una API REST con FastAPI para gestionar alertas georreferenciadas, diseñada como prueba técnica para postulación a Sistema GmbH (empresa de geodatos).

## Funcionalidades

- Crear, consultar, actualizar y eliminar alertas
- Soporte para filtros por categoría y estado (activo/inactivo)
- Backend en Python con FastAPI + SQLite (cambiable a MySQL)

## Ejecución

```bash
pip install -r requirements.txt
uvicorn main:app --reload
