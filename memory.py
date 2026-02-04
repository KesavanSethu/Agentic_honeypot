import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def _save(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def get_session(session_id):
    data = _load()
    return data.get(session_id, {
        "history": [],
        "state": "confused"
    })

def save_turn(session_id, user, bot):
    data = _load()
    session = data.get(session_id, {
        "history": [],
        "state": "confused"
    })
    session["history"].append((user, bot))
    data[session_id] = session
    _save(data)

def get_history(session_id):
    return get_session(session_id)["history"]

def get_state(session_id):
    return get_session(session_id)["state"]

def set_state(session_id, state):
    data = _load()
    session = data.get(session_id, {"history": [], "state": "confused"})
    session["state"] = state
    data[session_id] = session
    _save(data)
