from pydantic import BaseModel

class TutorRequest(BaseModel):
    pergunta: str
