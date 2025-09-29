from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.memory_ops import save_memory, search_memory

router = APIRouter()

class MemoryRequest(BaseModel):
    contact: str
    channel: str
    text: str

@router.post("/save")
def save_memory_endpoint(req: MemoryRequest):
    save_memory(req.contact, req.text, req.channel)
    return {"status": "memory saved"}

@router.get("/memory/search")
def search(query: str):
    results = search_memory(query)
    return {"results": "results"}