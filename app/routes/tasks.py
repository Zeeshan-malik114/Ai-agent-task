from fastapi import APIRouter, Form
from app.agents.voice_ops import schedule_outbound_call

router = APIRouter()


@router.post("/tasks/schedule_call")
async def schedule_call(
    caller: str = Form(...),
    text: str = Form(...),
    delay_minutes: int = Form(1)
):
    success = schedule_outbound_call(caller, text, delay_minutes)
    return {"success": success, "caller": caller, "delay_minutes": delay_minutes}
