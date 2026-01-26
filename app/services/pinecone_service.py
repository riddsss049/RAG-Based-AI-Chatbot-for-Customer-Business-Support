from sentence_transformers import SentenceTransformer
from app.config import pinecone_index

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_context(query):
    query_emb = model.encode(query).tolist()

    response = pinecone_index.query(
        vector=query_emb,
        top_k=5,
        include_metadata=True
    )

    matches = response.matches if hasattr(response, "matches") else response["matches"]

    # Build context text safely
    context_chunks = []
    for m in matches:
        if m.get("score", 0) >= 0.80:
            context_chunks.append(m["metadata"]["text"])

    # If nothing meaningful, return empty context
    if not context_chunks:
        return "No verified company info found in database."

    return "\n".join(context_chunks)