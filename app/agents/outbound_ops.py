import os
from twilio.rest import Client
from app.utils.logger import get_logger
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

logger = get_logger(__name__)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def trigger_outbound_call(to_number: str, call_sid: str):
    """
    Start an outbound call using Twilio.
    The call will hit our /voice/outbound webhook.
    """
    try:
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            url="https://<your-domain>/voice/outbound",  # webhook for outbound calls
        )
        logger.info(f"Outbound call scheduled to {to_number} (SID: {call.sid})")
        return call.sid
    except Exception as e:
        logger.error(f"Failed to trigger outbound call to {to_number}: {e}")
        return None