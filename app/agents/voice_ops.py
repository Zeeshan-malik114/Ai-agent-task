import requests
from app.utils.logger import get_logger
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, INBOUND_URL
from app.routes import voice  # Import inbound handler route
from fastapi import BackgroundTasks

logger = get_logger(__name__)

def schedule_outbound_call(caller_number: str):
    """
    Schedule an outbound call that will route back to inbound handler.
    This ensures conversation continues seamlessly.
    """

    logger.info(f"Scheduling outbound call to {caller_number}")

    try:
        payload = {
            "to": caller_number,
            "from": TWILIO_PHONE_NUMBER,
            "url": INBOUND_URL
        }

        # Example: POST to Twilio API to create outbound call
        twilio_api_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Calls.json"
        auth = ({TWILIO_ACCOUNT_SID}, {TWILIO_AUTH_TOKEN})

        response = requests.post(twilio_api_url, data=payload, auth=auth)

        if response.status_code == 201 or response.status_code == 200:
            logger.info(f"Outbound call scheduled successfully for {caller_number}")
            return True
        else:
            logger.error(f"Failed to schedule call for {caller_number}: {response.text}")
            return False

    except Exception as e:
        logger.error(f"Error scheduling call for {caller_number}: {e}")
        return False

