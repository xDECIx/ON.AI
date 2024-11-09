import httpx
from .logging_config import get_logger 
logger = get_logger()

async def send_callback(callback_url: str, data: dict):
    try:
        callback_url_str = str(callback_url)
        print(callback_url_str)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(callback_url_str, json=data)
            response.raise_for_status()
            logger.info(f"Callback sent successfully to {callback_url_str}") 
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred while sending callback: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during callback: {e}")
