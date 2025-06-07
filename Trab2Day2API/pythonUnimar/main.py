from fastapi import FastAPI
from app.controllers import tutor_controller

app = FastAPI(title="Tutor IA API")

app.include_router(tutor_controller.router, prefix="/tutor")

