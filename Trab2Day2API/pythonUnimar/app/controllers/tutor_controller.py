from fastapi import APIRouter, HTTPException
from app.models.tutor_request import TutorRequest
from app.services.tutor_service import TutorService

router = APIRouter()
tutor_service = TutorService()

@router.post("/perguntar")
async def perguntar_tutor(req: TutorRequest):
    try:
        resposta = await tutor_service.processar_pergunta(req.pergunta)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
