from pydantic import BaseModel
from datetime import date
from typing import Optional

class Event(BaseModel):
    id: str
    title: str
    description: str
    date: str
    location: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "2023-11-15",
                "title": "Workshop Python",
                "description": "Workshop introduttivo a Python",
                "date": "2023-11-15",
                "location": "Aula Magna"
            }
        }
    