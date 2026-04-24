import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware

# نوٹ: ورسل پر load_dotenv() کی ضرورت نہیں ہوتی، وہ خود ہی Variables اٹھا لیتا ہے

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 1. فنکشن کے اندر کی (Key) حاصل کریں
        api_key = os.getenv("GEMINI_API_KEY")
        
        # 2. اگر کی نہیں ملی تو ایرر دیں (تاکہ ہمیں پتہ چلے مسئلہ کی کا ہے)
        if not api_key:
            return {"description": "Backend Error: GEMINI_API_KEY is missing in Vercel settings!"}

        # 3. کلائنٹ کو یہاں ڈیفائن کریں
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=request.message
        )
        
        return {"description": response.text}
        
    except Exception as e:
        return {"description": f"Backend Error: {str(e)}"}