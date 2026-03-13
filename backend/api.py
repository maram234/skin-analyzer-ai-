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

app = FastAPI()

# Cache للنتائج لضمان الاتساق
analysis_cache = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

        # Deterministic clinical prompt — user-defined v2
        prompt = """ACT AS: A Board-Certified Dermatologist and AI Skin Imaging Specialist.

TASK: Perform a clinical-grade digital facial skin analysis based strictly on visible evidence in the provided facial image.

SCIENTIFIC CONSISTENCY RULE (CRITICAL):
The analysis MUST be deterministic.
The same image must always produce the same observations and conclusions.
Base all conclusions strictly on visible dermatological indicators such as pore visibility, lesion count, redness patches, pigmentation spots, texture irregularities, dryness signs, and oil shine.
Do NOT guess medical history or non-visible conditions.

AGE ESTIMATION RULE:
Estimate the approximate age range based on fine lines, skin elasticity, wrinkle depth, skin smoothness, and facial structure.
Return an age range such as: "20-25", "25-30", "30-35".

PHASE 0 — IMAGE VALIDATION
Verify that: a single human face is clearly visible, the face is sufficiently illuminated, skin areas are observable.
If the image is invalid return:
{"status":"error","message_en":"Clear human face not detected.","message_ar":"لم يتم اكتشاف وجه بشري واضح."}

PHASE 1 — CLINICAL VISUAL ANALYSIS
Evaluate the following dermatological indicators:
Acne / Breakouts, Hydration level, Skin redness / irritation, Skin texture smoothness, Pigmentation and tone uniformity, Pore visibility and size, Rosacea pattern indicators.
All observations must be short clinical descriptions based strictly on visible evidence.

PHASE 2 — PROFESSIONAL REPORT GENERATION
Create a structured dermatological report including:
• Skin type classification
• Approximate age range
• Overall skin condition assessment
• Individual clinical observations
• Key skin concerns
• Recommended skincare actions
• Suggested daily routine
Avoid exaggerated medical claims.

PHASE 3 — OUTPUT FORMAT
Return ONLY the following JSON structure:
{
"status":"success",
"en":{
"report_header":{
"skin_type":"",
"overall_assessment":"",
"approximate_age":"",
"analysis_confidence":"High / Medium"
},
"clinical_observations":{
"Acne":"","Hydration":"","Redness":"","Texture":"","Pigmentation":"","Pores":"","Rosacea":""
},
"key_skin_concerns":["","",""],
"routine_recommendations":["","",""],
"daily_routine":{
"morning":["Gentle cleanser","Vitamin C serum","Moisturizer","SPF 50 sunscreen"],
"evening":["Cleanser","Treatment serum","Moisturizer"]
},
"clinical_summary":"2-3 sentence professional dermatological summary."
},
"ar":{
"report_header":{
"skin_type":"",
"overall_assessment":"",
"approximate_age":"",
"analysis_confidence":"عالية / متوسطة"
},
"clinical_observations":{
"Acne":"","Hydration":"","Redness":"","Texture":"","Pigmentation":"","Pores":"","Rosacea":""
},
"key_skin_concerns":["","",""],
"routine_recommendations":["","",""],
"daily_routine":{
"morning":["غسول لطيف","سيروم فيتامين سي","مرطب","واقي شمس SPF 50"],
"evening":["غسول","سيروم علاجي","مرطب"]
},
"clinical_summary":"ملخص طبي احترافي من 2-3 جمل."
}
}

CRITICAL RULES:
1. Return ONLY the JSON object. Do NOT include markdown, explanations, or extra text.
2. All clinical observations must be based strictly on visible evidence in the image.
3. approximate_age must ALWAYS be filled.
4. The analysis must remain deterministic and reproducible for the same image.
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
