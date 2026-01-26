import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from pinecone import Pinecone, ServerlessSpec
from groq import Groq

load_dotenv()

# ===================== FIREBASE =====================
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ===================== PINECONE =====================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX", "jmd-bot-index")

pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if it does NOT exist
existing_indexes = [idx["name"] for idx in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1536,      # must match your embedding model!
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        )
    )

pinecone_index = pc.Index(PINECONE_INDEX_NAME)

# ===================== GROQ =====================
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
