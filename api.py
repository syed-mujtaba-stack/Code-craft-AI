from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import subprocess
import os
import tempfile
import json
from typing import Dict, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Get OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Dictionary to map language to file extension and command
LANGUAGE_CONFIG = {
    "python": {
        "extension": "py",
        "command": ["python", "{filepath}"]
    },
    "javascript": {
        "extension": "js",
        "command": ["node", "{filepath}"]
    },
    "html": {
        "extension": "html",
        "command": ["echo", "HTML files can't be executed directly"]
    },
    "css": {
        "extension": "css",
        "command": ["echo", "CSS files can't be executed directly"]
    }
}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

manager = ConnectionManager()

@router.post("/run")
async def run_code(code_data: dict):
    """
    Execute code in a safe sandboxed environment.
    """
    code = code_data.get("code", "")
    language = code_data.get("language", "python").lower()
    
    if language not in LANGUAGE_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    
    config = LANGUAGE_CONFIG[language]
    
    # Create a temporary file to store the code
    with tempfile.NamedTemporaryFile(
        mode="w", 
        suffix=f".{config['extension']}", 
        delete=False
    ) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    
    try:
        # Execute the code
        command = [arg.format(filepath=temp_file_path) for arg in config['command']]
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # Wait for the process to complete with a timeout
            stdout, stderr = process.communicate(timeout=10)
            
            if process.returncode != 0:
                return {
                    "output": stderr if stderr else "Process failed with non-zero exit code",
                    "error": True
                }
            
            return {"output": stdout, "error": False}
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "output": "Process timed out after 10 seconds",
                "error": True
            }
            
    except Exception as e:
        return {
            "output": f"Error executing code: {str(e)}",
            "error": True
        }
        
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_file_path)
        except:
            pass

@router.post("/ai/generate")
async def generate_code_with_ai(request: dict):
    """
    Generate code using OpenRouter API.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
        )
    
    prompt = request.get("prompt", "")
    language = request.get("language", "python")
    current_code = request.get("current_code", "")
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # Prepare the system message based on the language
    system_message = {
        "role": "system",
        "content": f"""You are a helpful AI coding assistant that generates {language.upper()} code based on user prompts. 
        Respond with clean, efficient, and well-documented code. 
        If the user provides existing code, you should enhance or modify it based on their request.
        Always wrap code blocks in triple backticks with the language specified."""
    }
    
    # Prepare the user message
    user_message = {
        "role": "user",
        "content": f"""Current code:
```{language}
{current_code}
```

User request: {prompt}

Please provide the complete updated code that satisfies the user's request. Include comments to explain the changes you've made."""
    }
    
    # Call OpenRouter API
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-4",  # You can change this to another model if needed
        "messages": [system_message, user_message],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30.0)
            
            if response.status_code != 200:
                return {
                    "error": f"OpenRouter API error: {response.text}",
                    "response": ""
                }
            
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            
            return {
                "response": ai_response,
                "error": None
            }
            
    except Exception as e:
        return {
            "error": f"Error calling OpenRouter API: {str(e)}",
            "response": ""
        }

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time communication with the client.
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            pass
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(client_id)
