from pydantic import BaseModel
from uuid import uuid4 # Importa la funzione uuid4 che mi serve per generare un ID univoco per ogni evento

class Participant(BaseModel):
    id: str = str(uuid4())
    first_name: str
    last_name: str
    event_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Mario",
                "last_name": "Rossi",
                "event_id": "2023-11-15"
            }
        }

'''       
# Spiegazione del Modello Participant

Il modello `Participant` è stato creato per rappresentare i partecipanti agli eventi nel sistema di gestione eventi. Vediamo perché è necessario e come avresti potuto capirlo.

## Perché è necessario questo modello?

Il modello `Participant` è necessario per:

1. **Strutturare i dati dei partecipanti**: Definisce quali informazioni vengono raccolte quando un utente si registra a un evento (nome, cognome e l'ID dell'evento a cui partecipa).

2. **Validazione dei dati**: Utilizzando Pydantic (`BaseModel`), il sistema può automaticamente verificare che i dati inseriti siano del tipo corretto.

3. **Serializzazione/Deserializzazione**: Facilita la conversione tra JSON (usato nelle API) e oggetti Python.

4. **Documentazione API**: La classe `Config` con `json_schema_extra` fornisce esempi per la documentazione automatica dell'API.

## Come avresti dovuto capirlo?

Avresti potuto capire la necessità di questo modello analizzando i requisiti del sistema:

> "Una API per registrarsi a un evento come partecipante, indicando nome e cognome dell'utente."

Questo requisito indica chiaramente che:
1. Il sistema deve gestire partecipanti
2. Ogni partecipante ha un nome e un cognome
3. I partecipanti sono associati a eventi specifici

In un'applicazione FastAPI ben strutturata, è una pratica comune creare modelli Pydantic per ogni entità del sistema. Dato che il sistema gestisce eventi e partecipanti, è logico avere:
- Un modello `Event` per gli eventi
- Un modello `Participant` per i partecipanti
  '''