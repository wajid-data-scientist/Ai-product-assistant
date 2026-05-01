import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
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
        # 1. API Key حاصل کریں
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"description": "Error: GEMINI_API_KEY not found in Vercel settings!"}
            
        # 2. کنفیگر کریں
        genai.configure(api_key=api_key)
        
        # 3. ماڈل ڈیفائن کریں (بغیر 'models/' کے لکھیں)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 4. جواب حاصل کریں
        response = model.generate_content(request.message)
        
        return {"description": response.text}
    except Exception as e:
        return {"description": f"Backend Error: {str(e)}"}