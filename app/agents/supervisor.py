from fastapi import BackgroundTasks
from app.utils.llm_ops import analyze_intent as get_intent
from app.utils.llm_ops import generate_summary, generate_short_topic
from app.agents.memory_ops import save_memory
from app.agents.email_ops import handle_email as send_email
from app.agents.voice_ops import schedule_outbound_call
from app.utils.logger import get_logger
import asyncio

logger = get_logger(__name__)

conversation_loops = {}
last_response = {}


async def handle_inbound_call(caller: str, text: str, background_tasks: BackgroundTasks, call_id: str):
    if not text:
        text = "Caller started conversation"

    logger.info(f"Handling inbound call from {caller} with text: {text}")

    if call_id not in conversation_loops:
        conversation_loops[call_id] = []

    conversation_loops[call_id].append(f"Caller: {text}")

    intent = await get_intent(text)
    logger.info(f"Detected intent: {intent} for caller {caller}")

    follow_up_action = None
    response_text = ""

    if intent == "send_email":
        full_text_for_summary = "\n".join(conversation_loops[call_id])
        conversation_summary = await generate_summary(full_text_for_summary, context="\n".join(conversation_loops[call_id]), length_limit=300)
        logger.info(f"Generated conversation summary for caller {caller}: {conversation_summary}")

        follow_up_action = "email"
        background_tasks.add_task(
            handle_call_end,
            caller,
            conversation_summary,
            email=email,
            memory_data=conversation_loops[call_id]
        )
        response_text = "Sure! I will email you the summary of our last conversation."

    elif intent == "schedule_call":
        follow_up_action = "call"
        schedule_outbound_call(caller)
        response_text = "Okay, I have scheduled a follow-up call for you."

    else:
        response_text = await generate_summary(text, context="", length_limit=150)
        last_response[call_id] = response_text

    # Save conversation memory
    short_summary = await generate_short_topic(response_text)
    save_memory(text=short_summary, contact=caller, channel="voice")
    logger.info(f"Memory saved for caller {caller}: {short_summary}")

    return response_text, follow_up_action, conversation_loops[call_id]


async def handle_call_end(caller: str, conversation_summary: str, email: str, memory_data=None):
    try:
        subject = await generate_short_topic(conversation_summary)
        body = (
            f"Hello,\n\nHere is the summary of our conversation:\n\n"
            f"{conversation_summary}\n\nRegards,\nAI Assistant"
        )
        send_email(to_email=email, subject=f"Follow-Up: {subject}", body=body)
        logger.info(f"Email sent to {email} for caller {caller} with subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send follow-up email to {email} for caller {caller}: {e}")
