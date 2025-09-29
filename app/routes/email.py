from fastapi import APIRouter # type: ignore
from pydantic import BaseModel # type: ignore
from app.agents.email_ops import handle_email

router = APIRouter()

# Define the request body model
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

@router.post("/send")
def send_email(req: EmailRequest):
    """
    Test endpoint to send an email using JSON body.
    """
    result = handle_email(req.to, req.subject, req.body)
    return {"status": result}