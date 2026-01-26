from app.config import db

def save_chat(user, message, reply):
    db.collection("conversations").add({
        "user": user,
        "message": message,
        "reply": reply
    })

def save_lead(data):
    db.collection("leads").add(data)
