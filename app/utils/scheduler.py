import asyncio
from datetime import datetime, timedelta
from app.agents.outbound_ops import trigger_outbound_call
from app.utils.logger import get_logger

logger = get_logger(__name__)

scheduled_tasks = {}


async def schedule_call(caller: str, call_sid: str, delay_minutes: int = 5):
    """
    Schedule a follow-up outbound call.
    """
    run_time = datetime.utcnow() + timedelta(minutes=delay_minutes)
    logger.info(f"Scheduling outbound call to {caller} at {run_time}")

    async def delayed_trigger():
        await asyncio.sleep(delay_minutes * 60)
        trigger_outbound_call(to_number=caller, call_sid=call_sid)

    task = asyncio.create_task(delayed_trigger())
    scheduled_tasks[call_sid] = task