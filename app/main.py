from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import frontend, events  # Importa i router

app = FastAPI()

# Monta i file statici
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Includi i router
app.include_router(frontend.router)  # Router per le pagine frontend
app.include_router(events.router, prefix="/api")  # Router per le API

