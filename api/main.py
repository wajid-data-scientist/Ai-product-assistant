import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        
        # یہاں 'http_options' شامل کیا ہے تاکہ وہ زبردستی v1 پر رہے
        client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1'}
        )
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=request.message
        )
        
        return {"description": response.text}
    except Exception as e:
        return {"description": f"Backend Error: {str(e)}"}