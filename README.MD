# Sistema di Gestione Eventi - Lab 02 - FastAPI

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
- **FastAPI**: un framework web moderno e veloce per Python che ci permette di creare API (interfacce di programmazione) in modo semplice
- **Jinja2**: un motore di template che ci permette di creare pagine HTML dinamiche, cioè pagine che cambiano in base ai dati
- **Pydantic**: una libreria che ci aiuta a controllare che i dati siano corretti prima di usarli

## Struttura del Progetto

Il progetto è organizzato secondo una struttura modulare, cioè diviso in parti che hanno ciascuna una funzione specifica:

```
esercizio_eventi/
├── app/                       # Cartella principale dell'applicazione
│   ├── data/
│   │   └── db.py              # Database in-memory per eventi e partecipanti (salva i dati in memoria)
│   ├── models/
│   │   ├── event.py           # Modello per gli eventi (definisce come deve essere un evento)
│   │   └── participant.py     # Modello per i partecipanti (definisce come deve essere un partecipante)
│   ├── routers/
│   │   ├── events.py          # Router per le API degli eventi (gestisce le richieste API)
│   │   └── frontend.py        # Router per le pagine frontend (gestisce le pagine web)
│   ├── static/
│   │   └── css/
│   │       └── style.css      # Stili CSS (per rendere belle le pagine)
│   ├── templates/
│   │   ├── base.html          # Template base (la struttura comune a tutte le pagine)
│   │   ├── events.html        # Lista eventi (pagina che mostra tutti gli eventi)
│   │   ├── event_detail.html  # Dettagli evento (pagina che mostra i dettagli di un evento)
│   │   ├── new_event.html     # Form per nuovo evento (pagina con il modulo per creare un evento)
│   │   ├── participants.html  # Lista partecipanti (pagina che mostra i partecipanti a un evento)
│   │   └── register.html      # Form per registrazione (pagina con il modulo per registrarsi a un evento)
│   └── main.py                # Punto di ingresso dell'applicazione (il file che avvia tutto)
└── README.md                  # Documentazione (questo file che stai leggendo)
```

## Funzionalità Frontend

Il "frontend" è la parte dell'applicazione che l'utente vede e con cui interagisce. È composto da pagine HTML che vengono mostrate nel browser.

### Pagina Home (`/`)

La pagina principale dell'applicazione che mostra una panoramica del sistema e fornisce link alle principali funzionalità.

```python
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
```

Spiegazione passo per passo:
- `@router.get("/")` significa "quando qualcuno visita la pagina principale del sito"
- `response_class=HTMLResponse` significa "la risposta sarà una pagina HTML"
- `async def read_root(request: Request)` definisce una funzione chiamata `read_root` che riceve una richiesta HTTP
- `templates.TemplateResponse("base.html", {"request": request})` prende il file HTML chiamato "base.html", lo riempie con i dati (in questo caso solo l'oggetto richiesta) e lo invia all'utente

In parole semplici: quando un utente visita la pagina principale, il sistema mostra la pagina "base.html".

### Lista Eventi (`/events`)

Mostra tutti gli eventi disponibili nel sistema.

```python
@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    all_events = list(events_db.values())
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})
```

Spiegazione passo per passo:
- `@router.get("/events")` significa "quando qualcuno visita la pagina /events"
- `all_events = list(events_db.values())` recupera tutti gli eventi dal database e li mette in una lista
- `templates.TemplateResponse("events.html", {"request": request, "events": all_events})` prende il file HTML chiamato "events.html", lo riempie con i dati (la richiesta e la lista degli eventi) e lo invia all'utente

In parole semplici: quando un utente visita la pagina degli eventi, il sistema recupera tutti gli eventi dal database e li mostra in una lista.

### Creazione Nuovo Evento (`/events/new`)

Mostra un form (modulo) per la creazione di un nuovo evento.

```python
@router.get("/events/new", response_class=HTMLResponse)
async def new_event_form(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("new_event.html", {"request": request, "error": error})
```

Spiegazione passo per passo:
- `@router.get("/events/new")` significa "quando qualcuno visita la pagina /events/new"
- `error: Optional[str] = None` significa che la funzione può ricevere un messaggio di errore opzionale
- `templates.TemplateResponse("new_event.html", {"request": request, "error": error})` prende il file HTML chiamato "new_event.html", lo riempie con i dati (la richiesta e l'eventuale messaggio di errore) e lo invia all'utente

In parole semplici: quando un utente vuole creare un nuovo evento, il sistema mostra un modulo da compilare. Se c'è stato un errore in precedenza, viene mostrato anche il messaggio di errore.

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

Spiegazione passo per passo:
- `@router.get("/events/{event_id}")` significa "quando qualcuno visita una pagina come /events/123" dove 123 è l'ID dell'evento
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `raise HTTPException(status_code=404, detail="Evento non trovato")` se l'evento non esiste, mostra un errore 404 (pagina non trovata)
- `event = events_db[event_id]` recupera l'evento dal database
- `templates.TemplateResponse("event_detail.html", {"request": request, "event": event})` prende il file HTML chiamato "event_detail.html", lo riempie con i dati (la richiesta e l'evento) e lo invia all'utente

In parole semplici: quando un utente vuole vedere i dettagli di un evento specifico, il sistema controlla se l'evento esiste e, se esiste, mostra tutti i suoi dettagli.

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

Spiegazione passo per passo:
- `@router.get("/events/{event_id}/participants")` significa "quando qualcuno visita una pagina come /events/123/participants"
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `event = events_db[event_id]` recupera l'evento dal database
- `event_participants = [p for p in participants_db if p.event_id == event_id]` crea una lista di tutti i partecipanti che sono registrati a questo evento specifico
- `templates.TemplateResponse("participants.html", {...})` prende il file HTML chiamato "participants.html", lo riempie con i dati (la richiesta, l'evento e i partecipanti) e lo invia all'utente

In parole semplici: quando un utente vuole vedere chi partecipa a un evento, il sistema recupera l'evento e tutti i suoi partecipanti e li mostra in una lista.

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

Spiegazione passo per passo:
- `@router.get("/events/{event_id}/register")` significa "quando qualcuno visita una pagina come /events/123/register"
- `error: Optional[str] = None` significa che la funzione può ricevere un messaggio di errore opzionale
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `event = events_db[event_id]` recupera l'evento dal database
- `templates.TemplateResponse("register.html", {...})` prende il file HTML chiamato "register.html", lo riempie con i dati (la richiesta, l'evento e l'eventuale messaggio di errore) e lo invia all'utente

In parole semplici: quando un utente vuole registrarsi a un evento, il sistema mostra un modulo da compilare con i propri dati. Se c'è stato un errore in precedenza, viene mostrato anche il messaggio di errore.


 
# Spiegazione della Comunicazione tra Frontend e Backend

Ciao! Ho analizzato il README del tuo progetto di gestione eventi e vorrei spiegarti in modo più chiaro come avviene la comunicazione tra frontend e backend, pensando che tu sia un principiante.

## Cosa sono Frontend e Backend?

Prima di tutto, facciamo chiarezza su questi termini:

- **Frontend**: è la parte dell'applicazione che vedi e con cui interagisci nel browser (le pagine HTML, i form, i bottoni, ecc.)
- **Backend**: è la parte "nascosta" dell'applicazione che gestisce i dati e la logica di business (salvataggio dati, verifica delle informazioni, ecc.)

## Come Comunicano tra Loro?

Nel tuo progetto, frontend e backend comunicano principalmente in due modi:

### 1. Attraverso le Pagine HTML (Frontend → Backend → Frontend)

Quando un utente visita una pagina del sito, ecco cosa succede:

1. **Richiesta**: Il browser invia una richiesta al server (es. quando visiti `/events`)
2. **Elaborazione**: Il backend elabora la richiesta, recupera i dati necessari (es. la lista degli eventi)
3. **Risposta**: Il backend invia una pagina HTML completa con i dati inseriti

Esempio pratico - Quando visiti la pagina degli eventi:
```python
@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    # Il backend recupera tutti gli eventi dal database
    all_events = list(events_db.values())
    
    # Il backend inserisce gli eventi nel template HTML e lo invia al browser
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})
```

### 2. Attraverso i Form HTML (Frontend → Backend)

Quando un utente compila un form (es. per creare un evento), ecco cosa succede:

1. **Invio dati**: L'utente compila il form e preme "Invia"
2. **Trasmissione**: I dati del form vengono inviati al backend
3. **Elaborazione**: Il backend controlla i dati, li salva nel database
4. **Reindirizzamento**: Il backend reindirizza l'utente a un'altra pagina

Esempio pratico - Quando crei un nuovo evento:
```python
@router.post("/new", response_class=RedirectResponse)
async def create_event_form(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...)
):
    try:
        # 1. Il backend riceve i dati dal form
        
        # 2. Controlla che la data sia valida
        event_date = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = event_date.strftime("%Y-%m-%d")
        
        # 3. Controlla se esiste già un evento per quella data
        if formatted_date in events_db:
            # Se c'è un errore, reindirizza con un messaggio di errore
            return RedirectResponse(
                url=f"/events/new?error=Esiste già un evento per la data {formatted_date}",
                status_code=303
            )
        
        # 4. Crea e salva il nuovo evento
        new_event = Event(
            id=formatted_date,
            title=title,
            description=description,
            date=date,
            location=location
        )
        events_db[formatted_date] = new_event
        
        # 5. Reindirizza l'utente alla pagina degli eventi
        return RedirectResponse(url="/events", status_code=303)
        
    except ValueError:
        # Se la data non è valida, reindirizza con un messaggio di errore
        return RedirectResponse(
            url="/events/new?error=Formato data non valido. Usa YYYY-MM-DD",
            status_code=303
        )
```

### 3. Attraverso le API (per applicazioni esterne)

Il progetto offre anche delle API che permettono ad altre applicazioni di comunicare con il backend:

1. **Richiesta API**: Un'applicazione esterna invia una richiesta all'API
2. **Elaborazione**: Il backend elabora la richiesta
3. **Risposta JSON**: Il backend invia una risposta in formato JSON (non HTML)

Esempio pratico - API per creare un evento:
```python
@router.post("/api/new", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event_api(event: Event):
    # Controlla se esiste già un evento con lo stesso ID
    if event.id in events_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esiste già un evento con ID {event.id}"
        )
    
    # Salva l'evento nel database
    events_db[event.id] = event
    
    # Restituisce l'evento creato in formato JSON
    return event
```

## Flusso Completo di un'Azione Utente

Vediamo passo per passo cosa succede quando un utente crea un nuovo evento:

1. **Visualizzazione Form**:
   - L'utente visita `/events/new`
   - Il backend invia il template HTML del form

2. **Compilazione Form**:
   - L'utente compila i campi (titolo, descrizione, data, luogo)
   - L'utente preme il pulsante "Crea Evento"

3. **Invio Dati**:
   - Il browser invia i dati al backend all'indirizzo `/events/new` con metodo POST
   - Il backend riceve i dati attraverso i parametri della funzione `create_event_form`

4. **Elaborazione**:
   - Il backend controlla che la data sia valida
   - Il backend verifica che non esista già un evento per quella data
   - Il backend crea un nuovo oggetto `Event` con i dati ricevuti
   - Il backend salva l'evento nel database

5. **Risposta**:
   - Se tutto va bene, il backend reindirizza l'utente alla pagina `/events`
   - Se c'è un errore, il backend reindirizza l'utente alla pagina del form con un messaggio di errore

## Differenza tra Form HTML e API

- **Form HTML**: Usati dagli utenti attraverso il browser. La risposta è una pagina HTML o un reindirizzamento.
- **API**: Usate da altre applicazioni. La risposta è in formato JSON, non HTML.


## API Backend

Il "backend" è la parte dell'applicazione che gestisce i dati e la logica di business. Le API (Application Programming Interface) sono punti di accesso che permettono di interagire con il backend tramite richieste HTTP.

### Creazione Evento API (`/api/events/new`)

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

Spiegazione passo per passo:
- `@router.post("/api/new")` significa "quando qualcuno invia dati (POST) all'indirizzo /api/new"
- `response_model=Event` significa "la risposta sarà un oggetto di tipo Event"
- `status_code=status.HTTP_201_CREATED` significa "se tutto va bene, restituisci il codice di stato 201 (Creato)"
- `async def create_event_api(event: Event)` definisce una funzione che riceve un oggetto Event
- `if event.id in events_db:` controlla se esiste già un evento con lo stesso ID
- `raise HTTPException(...)` se l'evento esiste già, restituisce un errore 400 (Richiesta non valida)
- `events_db[event.id] = event` salva l'evento nel database
- `return event` restituisce l'evento creato

In parole semplici: questa API permette di creare un nuovo evento inviando i dati in formato JSON. Se l'evento viene creato con successo, restituisce l'evento creato con un codice di stato 201.

### Lista Eventi API (`/api/events/`)

API per ottenere la lista di tutti gli eventi.

```python
@router.get("/", response_model=List[Event])
async def read_events():
    return list(events_db.values())
```

Spiegazione passo per passo:
- `@router.get("/")` significa "quando qualcuno richiede (GET) l'indirizzo /api/events/"
- `response_model=List[Event]` significa "la risposta sarà una lista di oggetti Event"
- `async def read_events()` definisce una funzione che non riceve parametri
- `return list(events_db.values())` restituisce una lista di tutti gli eventi nel database

In parole semplici: questa API restituisce tutti gli eventi presenti nel sistema in formato JSON.

### Dettagli Evento API (`/api/events/{event_id}`)

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

Spiegazione passo per passo:
- `@router.get("/{event_id}")` significa "quando qualcuno richiede (GET) un indirizzo come /api/events/123"
- `response_model=Event` significa "la risposta sarà un oggetto Event"
- `async def read_event(event_id: str)` definisce una funzione che riceve l'ID dell'evento
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `raise HTTPException(...)` se l'evento non esiste, restituisce un errore 404 (Non trovato)
- `return events_db[event_id]` restituisce l'evento richiesto

In parole semplici: questa API restituisce i dettagli di un evento specifico in formato JSON. Se l'evento non esiste, restituisce un errore 404.

### Creazione Partecipante API (`/api/events/{event_id}/participants`)

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

Spiegazione passo per passo:
- `@router.post("/api/{event_id}/participants")` significa "quando qualcuno invia dati (POST) a un indirizzo come /api/events/123/participants"
- `response_model=Participant` significa "la risposta sarà un oggetto Participant"
- `status_code=status.HTTP_201_CREATED` significa "se tutto va bene, restituisci il codice di stato 201 (Creato)"
- `async def create_participant_api(event_id: str, participant: Participant)` definisce una funzione che riceve l'ID dell'evento e un oggetto Participant
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `participant.event_id = event_id` imposta l'ID dell'evento nel partecipante
- `participants_db.append(participant)` aggiunge il partecipante al database
- `return participant` restituisce il partecipante creato

In parole semplici: questa API permette di registrare un nuovo partecipante a un evento specifico inviando i dati in formato JSON. Se il partecipante viene registrato con successo, restituisce il partecipante creato con un codice di stato 201.

### Lista Partecipanti API (`/api/events/{event_id}/participants`)

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

Spiegazione passo per passo:
- `@router.get("/{event_id}/participants")` significa "quando qualcuno richiede (GET) un indirizzo come /api/events/123/participants"
- `response_model=List[Participant]` significa "la risposta sarà una lista di oggetti Participant"
- `async def read_participants(event_id: str)` definisce una funzione che riceve l'ID dell'evento
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `return [p for p in participants_db if p.event_id == event_id]` restituisce una lista di tutti i partecipanti registrati a questo evento specifico

In parole semplici: questa API restituisce tutti i partecipanti registrati a un evento specifico in formato JSON. Se l'evento non esiste, restituisce un errore 404.

## Comunicazione Frontend-Backend

Il frontend e il backend comunicano tra loro principalmente attraverso form HTML e reindirizzamenti. Ecco come funziona:

### Gestione Form HTML

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

Spiegazione passo per passo:
- `@router.post("/new")` significa "quando qualcuno invia dati (POST) all'indirizzo /events/new"
- `response_class=RedirectResponse` significa "la risposta sarà un reindirizzamento a un'altra pagina"
- `async def create_event_form(...)` definisce una funzione che riceve i dati del form
- `title: str = Form(...)` significa "prendi il campo 'title' dal form"
- `try:` inizia un blocco di codice che potrebbe generare errori
- `event_date = datetime.strptime(date, "%Y-%m-%d")` converte la stringa della data in un oggetto data
- `if formatted_date in events_db:` controlla se esiste già un evento per quella data
- `return RedirectResponse(...)` se l'evento esiste già, reindirizza alla pagina del form con un messaggio di errore
- `new_event = Event(...)` crea un nuovo oggetto Event con i dati del form
- `events_db[formatted_date] = new_event` salva l'evento nel database
- `return RedirectResponse(url="/events", status_code=303)` reindirizza alla pagina degli eventi
- `except ValueError:` gestisce l'errore se la data non è nel formato corretto
- `return RedirectResponse(...)` reindirizza alla pagina del form con un messaggio di errore

In parole semplici: quando un utente compila il form per creare un nuovo evento, il sistema controlla che i dati siano corretti, crea l'evento e reindirizza l'utente alla pagina degli eventi. Se ci sono errori, l'utente viene reindirizzato al form con un messaggio di errore.

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

Spiegazione passo per passo:
- `@router.post("/{event_id}/register")` significa "quando qualcuno invia dati (POST) a un indirizzo come /events/123/register"
- `async def create_participant_form(...)` definisce una funzione che riceve l'ID dell'evento e i dati del form
- `first_name: str = Form(...)` significa "prendi il campo 'first_name' dal form"
- `if event_id not in events_db:` controlla se l'evento esiste nel database
- `return RedirectResponse(...)` se l'evento non esiste, reindirizza alla pagina degli eventi con un messaggio di errore
- `new_participant = Participant(...)` crea un nuovo oggetto Participant con i dati del form
- `participants_db.append(new_participant)` aggiunge il partecipante al database
- `return RedirectResponse(...)` reindirizza alla pagina dei partecipanti dell'evento

In parole semplici: quando un utente compila il form per registrarsi a un evento, il sistema controlla che l'evento esista, registra il partecipante e reindirizza l'utente alla pagina dei partecipanti. Se l'evento non esiste, l'utente viene reindirizzato alla pagina degli eventi con un messaggio di errore.

### Utilizzo di Templates

Il frontend utilizza Jinja2 per renderizzare le pagine HTML. Ecco come funziona:

```python
templates = Jinja2Templates(directory="app/templates")

@router.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    all_events = list(events_db.values())
    return templates.TemplateResponse("events.html", {"request": request, "events": all_events})
```

Spiegazione passo per passo:
1. `templates = Jinja2Templates(directory="app/templates")` configura Jinja2 per cercare i template nella directory `app/templates`
2. Quando viene richiesta la pagina `/events`, il sistema recupera tutti gli eventi dal database
3. `templates.TemplateResponse("events.html", {"request": request, "events": all_events})` passa i dati al template `events.html`
4. Il template utilizza questi dati per generare HTML dinamico

In parole semplici: Jinja2 è come un "motore" che prende un file HTML con dei "segnaposto" e li sostituisce con i dati reali. Ad esempio, il template potrebbe contenere un ciclo che mostra ogni evento nella lista.

## Modelli di Dati

I modelli di dati definiscono la struttura dei dati utilizzati nell'applicazione. In questo progetto, ci sono due modelli principali:

### Modello Event

```python
class Event(BaseModel):
    id: str
    title: str
    description: str
    date: str
    location: str
```

Questo modello definisce come deve essere un evento:
- `id`: un identificatore unico per l'evento (in questo caso, la data formattata)
- `title`: il titolo dell'evento
- `description`: una descrizione dell'evento
- `date`: la data dell'evento
- `location`: il luogo dell'evento

### Modello Participant

```python
class Participant(BaseModel):
    first_name: str
    last_name: str
    event_id: str
```

Questo modello definisce come deve essere un partecipante:
- `first_name`: il nome del partecipante
- `last_name`: il cognome del partecipante
- `event_id`: l'ID dell'evento a cui il partecipante è registrato

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

## Note
Questo progetto è un esempio didattico per un laboratorio di programmazione web. Sentiti libero di modificarlo e migliorarlo per le tue esigenze!

