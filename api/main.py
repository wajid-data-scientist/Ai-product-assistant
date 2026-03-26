import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware

# 1. .env فائل لوڈ کریں
# ہم یہاں explicit راستہ دے رہے ہیں تاکہ کوئی غلطی نہ ہو
load_dotenv()

# 2. API Key حاصل کریں
api_key = os.getenv("GEMINI_API_KEY")

# 3. چیک کریں کہ کی (Key) موجود ہے یا نہیں
if not api_key:
    # اگر .env نہیں مل رہی تو ہم عارضی طور پر یہاں کی ڈال دیتے ہیں تاکہ آپ کا کام نہ رکے
    # لیکن پروفیشنل طریقہ .env ہی ہے
    api_key = "AIzaSyBVbDZrotpo2QnxMKOnYklu3hrp79u25pQ"
    print("Warning: .env file not found, using backup key.")

# 4. گوگل کلائنٹ صرف ایک بار بنائیں
client = genai.Client(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductInfo(BaseModel):
    product_name: str
    keywords: str
    platform: str

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

@app.post("/generate-description")
async def generate_description(item: ProductInfo):
    print(f"Request for: {item.product_name}")
    try:
        # آپ کا پسندیدہ ماڈل gemini-2.5-flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", # یا gemini-2.0-flash جو آپ کے پاس دستیاب ہو
            contents=f"Write a professional SEO description for {item.product_name} on {item.platform}. Keywords: {item.keywords}"
        )
        
        print("Success!")
        return {"description": response.text}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if "429" in str(e):
            return {"description": "Quota Full. Please wait 1 minute."}
        return {"description": f"Error: {str(e)}"}
     