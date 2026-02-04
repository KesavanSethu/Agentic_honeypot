from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from detector import is_scam
from agent import agent_reply
from memory import get_history, save_turn
from extractor import extract_intel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ui", StaticFiles(directory="static"), name="static")

class Message(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: Message):
    history = get_history(req.session_id)

    scam = is_scam(req.message)
    reply = agent_reply(req.message, history, scam, req.session_id)
    extracted = extract_intel(req.message)

    save_turn(req.session_id, req.message, reply)

    return {
        "reply": reply,
        "scam": scam,
        "extracted": extracted
    }

@app.get("/")
def serve_ui():
    return FileResponse("static/ui.html")
