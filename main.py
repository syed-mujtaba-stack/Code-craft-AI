from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from typing import Dict, List, Optional
import asyncio

# Load environment variables
load_dotenv()

# Import API router
from api import router as api_router

app = FastAPI(
    title="CodeCraft AI",
    description="AI-Powered Multi-Language Coding Playground",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Create necessary directories
Path("templates").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)
Path("static/js").mkdir(exist_ok=True)
Path("static/css").mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

# WebSocket for real-time features
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Handle different types of WebSocket messages
                if message.get("type") == "code_execution":
                    # Handle code execution request
                    pass
                elif message.get("type") == "ai_generation":
                    # Handle AI code generation request
                    pass
                # Add more message types as needed
                
                # Echo the message back for now
                await manager.send_personal_message(
                    f"Message received: {message}", 
                    client_id
                )
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    "Error: Invalid JSON format",
                    client_id
                )
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f"Client {client_id} disconnected")

@app.on_event("startup")
async def startup_event():
    """Initialize application services."""
    # Initialize any required services here
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    # Cleanup resources here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        ssl_keyfile=os.getenv("SSL_KEYFILE"),
        ssl_certfile=os.getenv("SSL_CERTFILE")
    )
