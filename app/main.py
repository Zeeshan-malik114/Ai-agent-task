from fastapi import FastAPI # type: ignore
from app.routes import voice, email, tasks, memory

app = FastAPI(title="Multi-Agent AI Assistant")

# Include routes
app.include_router(voice.router, prefix="/voice")
app.include_router(email.router, prefix="/email")
app.include_router(tasks.router, prefix="/tasks")
app.include_router(memory.router, prefix="/memory")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI Multi-Agent Assistant is running "}
