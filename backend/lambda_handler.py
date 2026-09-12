"""Adaptador para correr la misma app FastAPI (sin cambios) dentro de AWS
Lambda. Mangum traduce el evento de Lambda (via Function URL) a una
peticion ASGI normal y la respuesta de vuelta -- no se reimplementa nada
de la logica de la app aca, solo se expone."""

from mangum import Mangum

from app.main import app

handler = Mangum(app)
