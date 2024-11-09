from fastapi import FastAPI
from .webhook import router as webhook_router
from .logging_config import get_logger  

logger = get_logger()
app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello, ON.AI! http://localhost:8000/docs"}

app.include_router(webhook_router)
logger.info("Starting FastAPI server")
