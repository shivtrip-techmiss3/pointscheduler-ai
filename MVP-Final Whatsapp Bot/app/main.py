from fastapi import FastAPI
from dotenv import load_dotenv
import os

# 🔑 Load .env BEFORE importing anything else
load_dotenv()

from app.routes.whatsapp_routes import router as whatsapp_router

app = FastAPI()

@app.get("/")
def health():
    return {"status": "Bot running"}

app.include_router(whatsapp_router, prefix="/api")
