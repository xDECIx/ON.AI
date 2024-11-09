from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl
from .llm import get_gemini_response
from .callback import send_callback
from .logging_config import get_logger  

router = APIRouter()
logger = get_logger()


class WebhookRequest(BaseModel):
    message: str
    callback_url: HttpUrl


@router.post("/webhook")
async def webhook(request: WebhookRequest, background_tasks: BackgroundTasks):
    try:
        logger.info("Received webhook request")

        response_text = await get_gemini_response(request.message)

        logger.info(
            f"Sending response to callback URL: {request.callback_url}")

        background_tasks.add_task(log_callback, request.callback_url, {
                                  "response": response_text})

        return {
            "status": "processing",
            "message": "Request is being processed",
            "llm_response": response_text
        }
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=500, detail="Error processing request.")


async def log_callback(callback_url: str, data: dict):
    try:
        await send_callback(callback_url, data)
        logger.info(f"Callback sent successfully to {callback_url}")
    except Exception as e:
        logger.warning(f"Failed to send callback to {callback_url}: {e}")
