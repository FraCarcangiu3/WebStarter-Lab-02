from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from ..data.db import events_db, participants_db

router = APIRouter(
    tags=["frontend"]
)

# Configura i templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# Sezione Gestione Eventi
@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    all_events = list(events_db.values())
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})

@router.get("/events/new", response_class=HTMLResponse)
async def new_event_form(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("new_event.html", {"request": request, "error": error})

@router.get("/events/{event_id}", response_class=HTMLResponse)
async def event_detail(request: Request, event_id: str):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    
    event = events_db[event_id]
    return templates.TemplateResponse("event_detail.html", {"request": request, "event": event})

@router.get("/events/{event_id}/participants", response_class=HTMLResponse)
async def list_participants(request: Request, event_id: str):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    
    event = events_db[event_id]
    event_participants = [p for p in participants_db if p.event_id == event_id]
    
    return templates.TemplateResponse("participants.html", {
        "request": request, 
        "event": event,
        "participants": event_participants
    })

# Sezione Registrazione Partecipanti
@router.get("/events/{event_id}/register", response_class=HTMLResponse)
async def register_form(request: Request, event_id: str, error: Optional[str] = None):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    
    event = events_db[event_id]
    return templates.TemplateResponse("register.html", {
        "request": request, 
        "event": event,
        "error": error
    })