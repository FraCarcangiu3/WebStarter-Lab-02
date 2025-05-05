from typing import Dict, List # mi servono per indicare il tipo di dato che viene restituito dalla funzione
from ..models.event import Event
from ..models.participant import Participant

# Database simulato
events_db: Dict[str, Event] = {} # Eventi registrati, la notazione indica che è un dizionario con chiave stringa e valori di tipo Event (ovvero un oggett
participants_db: List[Participant] = []