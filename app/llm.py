import google.generativeai as genai
import asyncio
from dotenv import load_dotenv
import os
from .logging_config import get_logger  

load_dotenv()
logger = get_logger() 


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

async def get_gemini_response(user_message: str) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, model.generate_content, user_message)
    
    logger.info(f"User: {user_message}\n LLM: {response.text}")
     
    return response.text