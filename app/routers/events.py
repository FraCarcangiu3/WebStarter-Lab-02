from fastapi import APIRouter, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from typing import List
from datetime import datetime

from ..models.event import Event
from ..models.participant import Participant
from ..data.db import events_db, participants_db

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Non trovato"}}
)

# API per la gestione degli eventi
@router.post("/api/new-events", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event_api(event: Event):
    if event.id in events_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esiste già un evento con ID {event.id}"
        )
    events_db[event.id] = event
    return event

@router.get("/", response_model=List[Event])
async def read_events():
    return list(events_db.values())

@router.get("/{event_id}", response_model=Event)
async def read_event(event_id: str):
    if event_id not in events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    return events_db[event_id]

# API per la gestione dei partecipanti
@router.post("/api/{event_id}/participants", response_model=Participant, status_code=status.HTTP_201_CREATED)
async def create_participant_api(event_id: str, participant: Participant):
    if event_id not in events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    participant.event_id = event_id
    participants_db.append(participant)
    return participant

@router.get("/{event_id}/participants", response_model=List[Participant])
async def read_participants(event_id: str):
    if event_id not in events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    return [p for p in participants_db if p.event_id == event_id]

# Endpoint per gestire i form HTML
@router.post("/new", response_class=RedirectResponse)
async def create_event_form(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...)
):
    try:
        # Verifica che la data sia nel formato corretto
        event_date = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = event_date.strftime("%Y-%m-%d")
        
        # Verifica se esiste già un evento per quella data
        if formatted_date in events_db:
            # Reindirizza con errore
            return RedirectResponse(
                url=f"/events/new?error=Esiste già un evento per la data {formatted_date}",
                status_code=303
            )
        
        # Crea il nuovo evento
        new_event = Event(
            id=formatted_date,
            title=title,
            description=description,
            date=date,
            location=location
        )
        
        # Salva l'evento nel database
        events_db[formatted_date] = new_event
        
        # Reindirizza alla pagina degli eventi
        return RedirectResponse(url="/events", status_code=303)
        
    except ValueError:
        # Reindirizza con errore
        return RedirectResponse(
            url="/events/new?error=Formato data non valido. Usa YYYY-MM-DD",
            status_code=303
        )

@router.post("/{event_id}/register", response_class=RedirectResponse)
async def create_participant_form(
    event_id: str,
    first_name: str = Form(...),
    last_name: str = Form(...)
):
    # Verifica che l'evento esista
    if event_id not in events_db:
        return RedirectResponse(
            url=f"/events?error=Evento non trovato",
            status_code=303
        )
    
    # Crea il nuovo partecipante
    new_participant = Participant(
        first_name=first_name,
        last_name=last_name,
        event_id=event_id
    )
    
    # Salva il partecipante nel database
    participants_db.append(new_participant)
    
    # Reindirizza alla pagina dei partecipanti
    return RedirectResponse(url=f"/events/{event_id}/participants", status_code=303)