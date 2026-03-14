from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from PIL import Image
import io
import hashlib

load_dotenv()

# قراءة مفتاح الـ API من متغيرات البيئة (مطلوب لـ Hugging Face Spaces)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY must be set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Cache للنتائج لضمان الاتساق
analysis_cache = {}

# السماح لجميع الـ origins (Vue.js على Vercel وغيره) بالوصول للـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# الموديل زي ما هو بناءً على طلبك مع تفعيل نظام الـ Determinism لثبات النتائج
model = genai.GenerativeModel(
    "gemini-3.1-flash-lite-preview",
    generation_config={
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
)


def get_image_hash(image_bytes):
    return hashlib.md5(image_bytes).hexdigest()


@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_hash = get_image_hash(image_bytes)

        if image_hash in analysis_cache:
            return analysis_cache[image_hash]

        image = Image.open(io.BytesIO(image_bytes))

        # تقرير طبي احترافي للمنظور (تحليل البشرة) — بدون نسب مئوية، تحليل لحالة البشرة + نصائح روتين
        prompt = """You are a Board-Certified Dermatologist and AI Skin Imaging Specialist.

TASK: Produce a professional medical skin analysis report (تقرير طبي احترافي لتحليل البشرة) based ONLY on visible evidence in the provided facial image.

IMPORTANT:
- Do NOT output percentages or numeric scores. Output descriptive analysis only.
- Be deterministic: the same image must always yield the same report.
- Base everything on what is visible: skin type, texture, hydration signs, pigmentation, pores, redness, acne/breakouts, etc. Do not guess medical history.

IMAGE VALIDATION:
If no single clear human face is visible, or lighting is too poor, return ONLY this JSON (no other text):
{"status":"error","message_en":"Clear human face not detected.","message_ar":"لم يتم اكتشاف وجه بشري واضح."}

OUTPUT FORMAT:
Return a SINGLE valid JSON object only. No markdown, no code fences, no extra text. Structure:

{
  "status": "success",
  "en": {
    "report_header": {
      "skin_type": "e.g. Oily, Dry, Combination, Normal, Sensitive",
      "overall_assessment": "2-3 sentence professional assessment of current skin condition",
      "approximate_age": "e.g. 20-25, 25-30",
      "analysis_confidence": "High or Medium"
    },
    "clinical_observations": {
      "Acne": "short descriptive observation",
      "Hydration": "short descriptive observation",
      "Redness": "short descriptive observation",
      "Texture": "short descriptive observation",
      "Pigmentation": "short descriptive observation",
      "Pores": "short descriptive observation",
      "Rosacea": "short descriptive observation"
    },
    "key_skin_concerns": ["concern 1", "concern 2", "concern 3"],
    "routine_recommendations": ["recommendation 1", "recommendation 2", "recommendation 3"],
    "daily_routine": {
      "morning": ["step 1", "step 2", "step 3", "step 4"],
      "evening": ["step 1", "step 2", "step 3"]
    },
    "clinical_summary": "2-3 sentence professional dermatological summary of the analysis."
  },
  "ar": {
    "report_header": {
      "skin_type": "مثال: دهنية، جافة، مختلطة، عادية، حساسة",
      "overall_assessment": "جملتان أو ثلاث لتقييم حالة البشرة",
      "approximate_age": "مثال: 20-25، 25-30",
      "analysis_confidence": "عالية أو متوسطة"
    },
    "clinical_observations": {
      "Acne": "ملاحظة سريرية قصيرة",
      "Hydration": "ملاحظة سريرية قصيرة",
      "Redness": "ملاحظة سريرية قصيرة",
      "Texture": "ملاحظة سريرية قصيرة",
      "Pigmentation": "ملاحظة سريرية قصيرة",
      "Pores": "ملاحظة سريرية قصيرة",
      "Rosacea": "ملاحظة سريرية قصيرة"
    },
    "key_skin_concerns": ["مشكلة 1", "مشكلة 2", "مشكلة 3"],
    "routine_recommendations": ["توصية 1", "توصية 2", "توصية 3"],
    "daily_routine": {
      "morning": ["خطوة 1", "خطوة 2", "خطوة 3", "خطوة 4"],
      "evening": ["خطوة 1", "خطوة 2", "خطوة 3"]
    },
    "clinical_summary": "ملخص طبي احترافي من 2-3 جمل."
  }
}

RULES:
1. Output ONLY the JSON object. No markdown, no explanations.
2. Fill every field. approximate_age and skin_type are required.
3. clinical_observations: short descriptive text per category, no percentages.
4. key_skin_concerns: list of main issues to address. routine_recommendations: actionable tips. daily_routine: concrete morning/evening steps.
"""

        # Try calling the AI model separately so we can return a clear 500 error
        try:
            response = model.generate_content([prompt, image])
        except Exception as ai_err:
            raise HTTPException(
                status_code=500,
                detail=f"AI model error: {str(ai_err)}"
            )

        text = response.text.strip()

        # Clean text
        cleaned_text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_text)

        if "status" not in data:
            data["status"] = "success"

        final_output = {"analysis": data}
        analysis_cache[image_hash] = final_output
        return final_output

    except Exception as e:
        return {
            "analysis": {
                "status": "error",
                "message_en": f"Analysis failed: {str(e)}",
                "message_ar": f"فشل التحليل: {str(e)}"
            }
        }


# تشغيل السيرفر على البورت 7860 والـ host 0.0.0.0 (مطلوب لـ Hugging Face Spaces)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

