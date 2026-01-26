from fastapi import APIRouter
from app.models.chat_model import ChatRequest
from app.services.pinecone_service import get_context
from app.services.groq_service import generate_reply
from app.services.firebase_service import save_chat

chat_memory = {}
router = APIRouter()

@router.post("/")
async def chat(req: ChatRequest):

    history = chat_memory.get(req.user_id, "")

    context = get_context(req.message)

    prompt = f"""
Conversation so far:
{history}

User: {req.message}

Context Knowledge:
{context}

Respond like JMD Pools representative. Be helpful, clear and professional.
"""

    reply = generate_reply(prompt)

    if not reply:
        reply = "Sorry, I’m having trouble retrieving information right now."

    chat_memory[req.user_id] = history + f"\nUser: {req.message}\nBot: {reply}"

    save_chat(req.user_id, req.message, reply)

    return {"reply": reply}
