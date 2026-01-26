import json
import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

# ========= KEYS =========
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

if not PINECONE_API_KEY:
    raise Exception("PINECONE_API_KEY missing in .env")

pc = Pinecone(api_key=PINECONE_API_KEY)

# ========= CREATE INDEX IF NOT EXISTS =========
existing_indexes = [idx["name"] for idx in pc.list_indexes()]

if INDEX_NAME not in existing_indexes:
    print("Index not found. Creating new index...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        ),
    )

index = pc.Index(INDEX_NAME)

# ========= SAFE FILE PATH =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "..", "data", "jmd_knowledge.json")

print("Loading knowledge file:", FILE_PATH)

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(f"Knowledge file missing: {FILE_PATH}")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Loaded knowledge entries:", len(data))

# ========= EMBEDDINGS =========
model = SentenceTransformer("all-MiniLM-L6-v2")


vectors = []

for i, item in enumerate(data):
    text = f"{item['category']} — {item['content']}"
    emb = model.encode(text).tolist()

    vectors.append(
        (
            f"doc_{i}",
            emb,
            {
                "category": item["category"],
                "source": item["source"],
                "text": item["content"]
            }
        )
    )

# ========= UPLOAD =========
print("Uploading to Pinecone...")
index.upsert(vectors=vectors)

print("UPLOAD COMPLETE ✅")