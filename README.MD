


          

# Sistema di Gestione Eventi

Questo progetto è un'applicazione web per la gestione di eventi e partecipanti, sviluppata con FastAPI e Jinja2. L'applicazione permette di creare eventi, visualizzare i dettagli degli eventi e registrare partecipanti.

## Indice

1. [Panoramica del Progetto](#panoramica-del-progetto)
2. [Struttura del Progetto](#struttura-del-progetto)
3. [Funzionalità Frontend](#funzionalità-frontend)
4. [API Backend](#api-backend)
5. [Comunicazione Frontend-Backend](#comunicazione-frontend-backend)
6. [Modelli di Dati](#modelli-di-dati)
7. [Guida all'Installazione](#guida-allinstallazione)
8. [Guida all'Uso](#guida-alluso)

## Panoramica del Progetto

Questo progetto è un sistema di gestione eventi che consente agli utenti di:
- Visualizzare una lista di eventi disponibili
- Creare nuovi eventi
- Visualizzare i dettagli di un evento specifico
- Registrarsi come partecipante a un evento
- Visualizzare la lista dei partecipanti a un evento

L'applicazione è costruita utilizzando:
- **FastAPI**: un framework web moderno e veloce per Python
- **Jinja2**: un motore di template per generare pagine HTML dinamiche
- **Pydantic**: per la validazione dei dati e la definizione dei modelli

## Struttura del Progetto

Il progetto è organizzato secondo una struttura modulare:

```
esercizio_eventi/
├── app/
│   ├── data/
│   │   └── db.py              # Database in-memory per eventi e partecipanti
│   ├── models/
│   │   ├── event.py           # Modello per gli eventi
│   │   └── participant.py     # Modello per i partecipanti
│   ├── routers/
│   │   ├── events.py          # Router per le API degli eventi
│   │   └── frontend.py        # Router per le pagine frontend
│   ├── static/
│   │   └── css/
│   │       └── style.css      # Stili CSS
│   ├── templates/
│   │   ├── base.html          # Template base
│   │   ├── events.html        # Lista eventi
│   │   ├── event_detail.html  # Dettagli evento
│   │   ├── new_event.html     # Form per nuovo evento
│   │   ├── participants.html  # Lista partecipanti
│   │   └── register.html      # Form per registrazione
│   └── main.py                # Punto di ingresso dell'applicazione
└── README.md                  # Documentazione
```

## Funzionalità Frontend

### Pagina Home (`/`)

La pagina principale dell'applicazione che mostra una panoramica del sistema e fornisce link alle principali funzionalità.

```python
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
```

Questa funzione:
- Accetta una richiesta HTTP
- Restituisce il template `base.html` come risposta HTML
- Passa l'oggetto `request` al template (richiesto da Jinja2)

### Lista Eventi (`/events`)

Mostra tutti gli eventi disponibili nel sistema.

```python
@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    all_events = list(events_db.values())
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})
```

Questa funzione:
- Recupera tutti gli eventi dal database
- Passa la lista degli eventi al template `events.html`
- Il template mostra ogni evento con titolo, data, luogo e link alle azioni

### Creazione Nuovo Evento (`/events/new`)

Mostra un form per la creazione di un nuovo evento.

```python
@router.get("/events/new", response_class=HTMLResponse)
async def new_event_form(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("new_event.html", {"request": request, "error": error})
```

Questa funzione:
- Accetta un parametro opzionale `error` per mostrare messaggi di errore
- Renderizza il template `new_event.html` con il form di creazione
- Il form invia i dati a `/events/new` con metodo POST (gestito dal router events)

### Dettagli Evento (`/events/{event_id}`)

Mostra i dettagli di un evento specifico.

```python
@router.get("/events/{event_id}", response_class=HTMLResponse)
async def event_detail(request: Request, event_id: str):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    
    event = events_db[event_id]
    return templates.TemplateResponse("event_detail.html", {"request": request, "event": event})
```

Questa funzione:
- Accetta un parametro `event_id` dall'URL
- Verifica che l'evento esista nel database
- Passa l'evento al template `event_detail.html`
- Mostra titolo, data, luogo, descrizione e link alle azioni

### Lista Partecipanti (`/events/{event_id}/participants`)

Mostra tutti i partecipanti registrati a un evento specifico.

```python
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
```

Questa funzione:
- Verifica che l'evento esista
- Filtra i partecipanti per l'evento specifico
- Passa l'evento e i partecipanti al template `participants.html`
- Mostra una tabella con nome e cognome dei partecipanti

### Registrazione Partecipante (`/events/{event_id}/register`)

Mostra un form per registrarsi come partecipante a un evento.

```python
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
```

Questa funzione:
- Verifica che l'evento esista
- Passa l'evento e un eventuale messaggio di errore al template `register.html`
- Il form invia i dati a `/events/{event_id}/register` con metodo POST (gestito dal router events)

## API Backend

### Creazione Evento API (`/events/api/new`)

API per creare un nuovo evento tramite richiesta JSON.

```python
@router.post("/api/new", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event_api(event: Event):
    if event.id in events_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esiste già un evento con ID {event.id}"
        )
    events_db[event.id] = event
    return event
```

Questa API:
- Accetta un oggetto `Event` nel corpo della richiesta
- Verifica che non esista già un evento con lo stesso ID
- Salva l'evento nel database
- Restituisce l'evento creato con status code 201 (Created)

### Lista Eventi API (`/events/`)

API per ottenere la lista di tutti gli eventi.

```python
@router.get("/", response_model=List[Event])
async def read_events():
    return list(events_db.values())
```

Questa API:
- Restituisce tutti gli eventi come lista di oggetti `Event`
- Il formato di risposta è JSON

### Dettagli Evento API (`/events/{event_id}`)

API per ottenere i dettagli di un evento specifico.

```python
@router.get("/{event_id}", response_model=Event)
async def read_event(event_id: str):
    if event_id not in events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    return events_db[event_id]
```

Questa API:
- Accetta un parametro `event_id` dall'URL
- Verifica che l'evento esista
- Restituisce l'evento come oggetto JSON

### Creazione Partecipante API (`/events/api/{event_id}/participants`)

API per registrare un partecipante a un evento tramite richiesta JSON.

```python
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
```

Questa API:
- Accetta un parametro `event_id` dall'URL e un oggetto `Participant` nel corpo
- Verifica che l'evento esista
- Imposta l'`event_id` del partecipante
- Salva il partecipante nel database
- Restituisce il partecipante creato con status code 201 (Created)

### Lista Partecipanti API (`/events/{event_id}/participants`)

API per ottenere la lista dei partecipanti a un evento specifico.

```python
@router.get("/{event_id}/participants", response_model=List[Participant])
async def read_participants(event_id: str):
    if event_id not in events_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    return [p for p in participants_db if p.event_id == event_id]
```

Questa API:
- Verifica che l'evento esista
- Filtra i partecipanti per l'evento specifico
- Restituisce la lista dei partecipanti come JSON

## Comunicazione Frontend-Backend

### Gestione Form HTML

Il frontend comunica con il backend principalmente attraverso form HTML e reindirizzamenti. Ecco come funziona:

#### Creazione Evento tramite Form (`/events/new`)

```python
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
```

Questo endpoint:
1. Riceve i dati del form tramite parametri `Form`
2. Valida la data e verifica che non esista già un evento per quella data
3. Crea un nuovo evento e lo salva nel database
4. Reindirizza l'utente alla pagina degli eventi o alla pagina del form con un messaggio di errore

#### Registrazione Partecipante tramite Form (`/events/{event_id}/register`)

```python
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
```

Questo endpoint:
1. Riceve i dati del form tramite parametri `Form`
2. Verifica che l'evento esista
3. Crea un nuovo partecipante e lo salva nel database
4. Reindirizza l'utente alla pagina dei partecipanti

### Utilizzo di Templates

Il frontend utilizza Jinja2 per renderizzare le pagine HTML. Ecco come funziona:

```python
templates = Jinja2Templates(directory="app/templates")

@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    all_events = list(events_db.values())
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})
```

Questo codice:
1. Configura Jinja2 per cercare i template nella directory `app/templates`
2. Quando viene richiesta la pagina `/events`, recupera tutti gli eventi dal database
3. Passa i dati al template `events.html` insieme all'oggetto `request` (richiesto da Jinja2)
4. Il template utilizza questi dati per generare HTML dinamico

## Modelli di Dati

### Evento

Il modello `Event` rappresenta un evento con le seguenti proprietà:
- `id`: identificativo univoco (formato dalla data dell'evento)
- `title`: titolo dell'evento
- `description`: descrizione dell'evento
- `date`: data dell'evento
- `location`: luogo dell'evento

### Partecipante

Il modello `Participant` rappresenta un partecipante con le seguenti proprietà:
- `id`: identificativo univoco generato automaticamente
- `first_name`: nome del partecipante
- `last_name`: cognome del partecipante
- `event_id`: ID dell'evento a cui il partecipante è registrato

## Guida all'Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuousername/sistema-gestione-eventi.git
   cd sistema-gestione-eventi
   ```

2. Crea un ambiente virtuale e attivalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install fastapi uvicorn jinja2 python-multipart
   ```

4. Avvia l'applicazione:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Apri il browser e vai a `http://localhost:8000`

## Guida all'Uso

### Visualizzare gli Eventi

1. Vai alla pagina principale (`/`)
2. Clicca su "Accedi alla Gestione Eventi"
3. Visualizza la lista degli eventi disponibili

### Creare un Nuovo Evento

1. Vai alla pagina degli eventi (`/events`)
2. Clicca su "Crea Nuovo Evento"
3. Compila il form con titolo, descrizione, data e luogo
4. Clicca su "Crea Evento"

### Registrarsi a un Evento

1. Vai alla pagina degli eventi (`/events`)
2. Trova l'evento desiderato e clicca su "Registrati"
3. Compila il form con nome e cognome
4. Clicca su "Registrati"

### Visualizzare i Partecipanti

1. Vai alla pagina degli eventi (`/events`)
2. Trova l'evento desiderato e clicca su "Partecipanti"
3. Visualizza la lista dei partecipanti registrati

---

Questo progetto è un esempio didattico per un laboratorio di programmazione web. Sentiti libero di modificarlo e migliorarlo per le tue esigenze!
