from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes.chat_routes import router as chat_router
from app.routes.lead_routes import router as lead_router

app = FastAPI(title="JMD Pools Chatbot API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_ui():
    return FileResponse("frontend/index.html")

# API Routes
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(lead_router, prefix="/lead", tags=["Lead"])
