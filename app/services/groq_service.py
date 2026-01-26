import hashlib
from app.config import groq_client

MODEL_NAME = "llama-3.1-8b-instant"


def generate_reply(prompt):
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JMD Pools AI Assistant.\n"
                        "Respond ONLY in neat bullet points.\n"
                        "RULES:\n"
                        "• 4–6 bullet points maximum.\n"
                        "• Short, crisp, business-friendly points.\n"
                        "• Prefer factual, useful, customer-helpful information.\n"
                        "• First try to answer from provided context.\n"
                        "• If context is limited, use general pool industry knowledge BUT:\n"
                        "  - Keep it realistic\n"
                        "  - India relevant\n"
                        "  - Do NOT hallucinate owners, founders, office locations, dates, or awards.\n"
                        "• Do NOT redirect to website unless user explicitly asks.\n"
                        "• Tone: Friendly, trustworthy, professional, supportive.\n"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response.choices[0].message.content.strip()

        # Just in case model ignores rules, enforce bullet formatting lightly
        if not reply.startswith("•") and "-" not in reply[:3]:
            reply = "\n".join([f"• {line.strip()}" for line in reply.split("\n") if line.strip()])

        return reply

    except Exception as e:
        print("Groq Error:", e)
        return (
            "• Sorry, I'm having trouble responding right now.\n"
            "• Please try again in a moment.\n"
            "• If it continues, let the team know."
        )


# ---------- TEMP EMBEDDINGS ----------
# deterministic fake embedding but CORRECT Pinecone length

def embed_text(text: str, dim: int = 1024):
    """
    Groq has no embeddings (yet),
    so we create deterministic pseudo embeddings
    compatible with Pinecone dimensions.
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    base = [float(b) / 255.0 for b in h]

    # repeat hash to required dimension
    vector = (base * (dim // len(base) + 1))[:dim]
    return vector
