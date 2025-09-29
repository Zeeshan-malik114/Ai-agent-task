# AI Agent Task

A voice-enabled AI assistant built with **FastAPI**, **Twilio**, and **Google Gemini**.  
This assistant handles inbound voice calls, processes caller requests, answers questions in a conversational loop, and can send email summaries or schedule follow-up calls.

---

## Features

- **Voice Conversation Loop**: AI answers caller questions dynamically until a summary or follow-up is requested.
- **Intent Detection**: Uses Google Gemini to detect caller intent (e.g., send email, schedule call, general query).
- **Email Summaries**: Summarizes conversation and sends via email.
- **Follow-up Calls**: Schedules follow-up calls if requested.
- **Conversation Memory**: Keeps conversation context for a single call session.

---

## Project Structure

Ai-agent-task/
│
├── app/ # Core application
│ ├── agents/ # AI conversation handlers
│ ├── routes/ # API routes
│ ├── utils/ # Utility functions
│ └── config.py # Configurations
│
├── db/ # ChromaDB data store
│
├── docker/ # Docker configuration
│
├── logs/ # Log files
│
├── postman_collection.json
├── README.md
├── requirements.txt
└── Dockerfile


---

## Prerequisites

- Docker & Docker Compose
- Twilio account with voice phone number
- Google API Key for Gemini
- Python 3.11+
- Git
- ngrok

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-repo/Ai-agent-task.git
cd Ai-agent-task

Add Environment Variables

Create a .env file in the root directory:

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
GOOGLE_API_KEY=your_google_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_email_app_password


Run with Docker

docker-compose -f docker/docker-compose.yaml build
docker run -it -p 8000:8000 docker-ai-agent:latest
http://0.0.0.0:8000/docs#/ # Endpoint


Run Locally

If not using Docker:

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
ngrok http 8080

Logging

'Logs are stored in logs/assistant.log'.

## Project Structure

Twilio sends inbound calls to /voice/inbound.
The AI processes the speech, detects intent, and responds dynamically.
Keeps conversation memory until call ends.
On "send email" intent, it generates a summary and sends it via email.
On "schedule call" intent, it schedules a follow-up call.