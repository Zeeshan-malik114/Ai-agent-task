import google.generativeai as genai
from app.config import GOOGLE_API_KEY
from app.utils.logger import get_logger
import asyncio

logger = get_logger(__name__)

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)


async def analyze_intent(text: str) -> str:
    """
    Determine intent from user input.
    """
    logger.info(f"Analyzing intent for text: {text}")
    text_lower = text.lower()

    if "email" in text_lower or "send me" in text_lower:
        return "send_email"
    elif "call me" in text_lower or "follow up" in text_lower:
        return "schedule_call"
    elif "rate" in text_lower:
        return "query_rate_plans"
    elif "invoice" in text_lower:
        return "query_invoice"
    else:
        return "other"


async def generate_summary(text: str, context: str = "", length_limit: int = 100) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    if context:
        prompt = f"""
        Give me a summary about:
        Context: {context}
        Request: {text}
        Limit: {length_limit} words.
        """
    else:
        prompt = f"""
        Give me an answer to the question:
        {text}
        Limit: {length_limit} words.
        """

    logger.info(f"Generating summary with prompt: {prompt}")

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return f"(Fallback) Could not generate summary. Raw input: {text}"



async def generate_short_topic(text: str) -> str:
    """
    Generate a concise subject line (1–5 words) from conversation summary.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Summarize this into 2-5 words for an email subject: {text}"
    logger.info(f"Generating short topic with prompt: {prompt}")

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        topic = response.text.strip()
        return " ".join(topic.split()[:5])
    except Exception as e:
        logger.error(f"Error generating short topic: {e}")
        return "Conversation Summary"
