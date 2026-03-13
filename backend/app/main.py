import os
import io
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

# ضبط الإعدادات لتكون النتائج ثابتة (Deterministic)
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite-preview",
    generation_config=generation_config,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # بورت الـ Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    try:
      
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        
        # Optimize image size before sending to Google AI for much faster response time
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.thumbnail((800, 800))

 
        prompt = """
 ACT AS: A Board-Certified Dermatologist and AI Skin Imaging Specialist.
TASK: Perform a Clinical Digital Facial Skin Analysis.
OUTPUT: MUST BE A SINGLE, VALID JSON OBJECT. NO MARKDOWN. NO CODE BLOCKS.

PHASE 0 – IMAGE VALIDATION:
- Verify a single, clear human face. 
- If validation fails (no face, blur, poor lighting), return:
{ "status": "error", "message_en": "Clear human face not detected.", "message_ar": "لم يتم اكتشاف وجه بشري واضح." }

PHASE 1 – QUANTITATIVE SCORING (0-100):
- Indicators: Acne, Hydration, Redness, Texture, Pigmentation, Pores, Rosacea.
- Score 100 = Perfect condition. Score 0 = Severe concern.

PHASE 2 – STRUCTURED JSON OUTPUT (STRICT SCHEMA):
If valid, return exactly this structure:

{
  "status": "success",
  "en": {
    "report_header": { "skin_type": "string", "overall_confidence": "string" },
    "quantitative_scoring": {
      "Acne": 0, "Hydration": 0, "Redness": 0, "Texture": 0, "Pigmentation": 0, "Pores": 0, "Rosacea": 0
    },
    "observations": {
      "Acne": "string", "Hydration": "string", "Redness": "string", "Texture": "string", "Pigmentation": "string", "Pores": "string", "Rosacea": "string"
    },
    "clinical_summary": "string"
  },
  "ar": {
    "report_header": { "skin_type": "string", "overall_confidence": "string" },
    "quantitative_scoring": {
      "Acne": 0, "Hydration": 0, "Redness": 0, "Texture": 0, "Pigmentation": 0, "Pores": 0, "Rosacea": 0
    },
    "observations": {
      "Acne": "وصف سريري بالعربي", 
      "Hydration": "وصف سريري بالعربي",
      "Redness": "وصف سريري بالعربي",
      "Texture": "وصف سريري بالعربي",
      "Pigmentation": "وصف سريري بالعربي",
      "Pores": "وصف سريري بالعربي",
      "Rosacea": "وصف سريري بالعربي"
    },
    "clinical_summary": "جمل طبية دقيقة"
  }
}

CRITICAL: Keep the keys in "quantitative_scoring" EXACTLY as (Acne, Hydration, etc.) in both 'en' and 'ar' so the Frontend can map them to the UI bars. Only translate the values.
        """

        response = model.generate_content([prompt, img])

        text = response.text

        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            clean_text = match.group(0)
        else:
            clean_text = text.replace("```json", "").replace("```", "").strip()

        try:
            parsed_json = json.loads(clean_text)
        except Exception:
            # Fallback: return raw text if JSON parsing fails
            parsed_json = clean_text

        return {"analysis": parsed_json}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

