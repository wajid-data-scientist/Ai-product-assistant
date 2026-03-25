from google import genai

# اپنی API Key یہاں لکھیں
client = genai.Client(api_key="AIzaSyBVbDZrotpo2QnxMKOnYklu3hrp79u25pQ")

def list_my_models():
    try:
        print("--- آپ کے دستیاب ماڈلز کی لسٹ یہ ہے ---")
        # یہ کمانڈ تمام دستیاب ماڈلز کو لسٹ کرے گی
        for model in client.models.list():
            print(f"Model Name: {model.name}")
            print(f"Supported Methods: {model.supported_methods}")
            print("-" * 30)
    except Exception as e:
        print(f"Error fetching models: {str(e)}")

# اس فنکشن کو کال کریں
list_my_models()