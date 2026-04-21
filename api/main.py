import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# 1. API Key حاصل کریں
api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyBVbDZrotpo2QnxMKOnYklu3hrp79u25pQ"

# 2. کلائنٹ سیٹ اپ
client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# یہ وہ ماڈل ہے جو فرنٹ اینڈ سے آنے والے "message" کو سنبھالے گا
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

# --- یہاں سے وہ کوڈ شروع ہوتا ہے جو غائب تھا ---
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # جیمنائی کو میسج بھیجنا
        response = client.models.generate_content(
            model="gemini-2.0-flash", # جیمنائی 2.0 فلیش بہترین ہے
            contents=request.message
        )
        
        return {"description": response.text}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"description": f"Error: {str(e)}"}
# --- یہاں ختم ہوتا ہے ---