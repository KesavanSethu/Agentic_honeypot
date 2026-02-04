import random
from memory import get_state, set_state
from extractor import extract_intel

CONFUSED = [
    "Wait… I don’t understand. Can you explain slowly?",
    "Sorry I’m not good with phones. What should I do?",
    "This message scared me… is it real?",
    "My son usually handles this. Tell again?",
]

COOPERATIVE = [
    "Okay okay… what do you need from me?",
    "I’m trying to do it, tell me next step",
    "It’s asking details… is this safe?",
]

VERIFYING = [
    "Before sending, can you confirm once?",
    "I see something, is this correct?",
    "This looks risky… are you sure?"
]

STALLING = [
    "My phone is hanging, wait",
    "Network issue, one minute",
    "Battery low, I’ll reply",
]

def agent_reply(message, history, scam):
    if not scam:
        return "Okay, thanks for letting me know."

    extracted = extract_intel(message)
    session_id = history[0][0] if history else "default"

    state = get_state(session_id)

    if extracted["upi"] or extracted["bank_accounts"]:
        state = "verifying"
    elif extracted["links"]:
        state = "cooperative"
    elif len(history) > 6:
        state = "stalling"
    else:
        state = "confused"

    set_state(session_id, state)

    if state == "confused":
        return random.choice(CONFUSED)
    if state == "cooperative":
        return random.choice(COOPERATIVE)
    if state == "verifying":
        return random.choice(VERIFYING)
    return random.choice(STALLING)
