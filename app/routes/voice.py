
from fastapi import APIRouter, Form, BackgroundTasks, Request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.agents.supervisor import handle_inbound_call, handle_call_end
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
user_sessions = {}


@router.post("/inbound")
async def voice_inbound(
    From: str = Form(...),
    CallSid: str = Form(...),
    SpeechResult: str = Form(None),
    background_tasks: BackgroundTasks = None
):
    resp = VoiceResponse()
    caller = From

    try:
        if CallSid not in user_sessions:
            user_sessions[CallSid] = {
                "caller": caller,
                "state": "greeting",
                "conversation": []
            }
            gather = resp.gather(input="speech", action="/voice/inbound", method="POST", timeout=5)
            gather.say("Hello, this is your AI assistant. How can I help you today?", voice="alice")
            return Response(content=str(resp), media_type="application/xml")

        if not SpeechResult:
            gather = resp.gather(input="speech", action="/voice/inbound", method="POST", timeout=5)
            gather.say("I didn’t catch that. Could you repeat please?", voice="alice")
            return Response(content=str(resp), media_type="application/xml")

        session = user_sessions[CallSid]
        logger.info(f"Caller said: {SpeechResult}")

        response_text, follow_up_action, memory_data = await handle_inbound_call(
            caller=caller,
            text=SpeechResult,
            background_tasks=background_tasks,
            call_id=CallSid
        )

        session["conversation"].append({"user": SpeechResult, "ai": response_text})
        session["state"] = "waiting_for_followup"
        session["follow_up_type"] = follow_up_action
        session["memory_data"] = memory_data
        session["last_concern"] = SpeechResult

        gather = resp.gather(input="speech", action="/voice/inbound", method="POST", timeout=5)
        if follow_up_action == "email":
            gather.say(response_text + " Would you like me to email you this summary?", voice="alice")
        elif follow_up_action == "call":
            gather.say(response_text + " Should I schedule a follow-up call?", voice="alice")
        else:
            gather.say(response_text, voice="alice")

        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        logger.error(f"Error handling inbound call: {e}")
        resp.say("Sorry, something went wrong. Please try again later.", voice="alice")
        return Response(content=str(resp), media_type="application/xml")


@router.post("/end")
async def voice_end(
    request: Request,
    From: str = Form(None),
    background_tasks: BackgroundTasks = None
):
    caller = From or "unknown"
    logger.info(f"Call ended for caller {caller}")

    try:
        memory_data = None
        background_tasks.add_task(
            handle_call_end,
            caller,
            "Your last conversation summary",
            email=email,
            memory_data=memory_data
        )
        return {"status": "success", "message": "Follow-up tasks scheduled after call end."}
    except Exception as e:
        logger.error(f"Error in call end for caller {caller}: {e}")
        return {"status": "error", "message": str(e)}
