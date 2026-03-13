# 🔬 Skin Mirror AI - تحليل البشرة الذكي

تطبيق ويب احترافي للتحليل الذكي للبشرة باستخدام **Google Gemini AI** مع واجهة مستخدم جميلة وميزات متقدمة.

---

## ✨ **الميزات الرئيسية**

### 📸 **التقاط مباشر من الكاميرا**
- تشغيل الكاميرا مباشرة من المتصفح
- معاينة حية قبل التحليل
- التقاط صور عالية الجودة
- يعمل على جميع الأجهزة (ديسك، موبايل، تابلت)

### 📊 **تقارير جميلة مع الرسوم البيانية**
- عرض النتائج بشكل احترافي
- رسم بياني راداري (Radar Chart) لتقييم البشرة
- عرض الصورة الملتقطة مع النتائج
- عرض التوصيات بشكل منظم

### 💾 **حفظ السجل التاريخي**
- حفظ النتائج تلقائياً في localStorage
- عرض السجل الكامل للتحليلات السابقة
- مشاهدة النتائج السابقة بنقرة واحدة
- حذف النتائج بشكل فردي أو الكل

### 🤖 **تحليل ذكي**
- استخدام **Google Gemini AI** للتحليل
- كشف الوجه تلقائياً قبل التحليل
- نفس الصورة تعطي نفس النتيجة (Caching)
- رسائل خطأ واضحة باللغة العربية

### 🎨 **واجهة مستخدم احترافية**
- تصميم Dark Mode مظلم احترافي
- تبويبات سهلة الاستخدام
- رسوم متحركة سلسة
- تصميم responsive يعمل على جميع الأجهزة
- دعم اللغة العربية (RTL)

---

## 📋 **البنية الهيكلية**

```
skin-analyzer-ai/
├── backend/                    # 🐍 خادم Python FastAPI
│   ├── api.py                 # API الرئيسي مع Gemini
│   ├── main.py                # API بديل (تحليل مفصل)
│   ├── requirements.txt        # المكتبات المطلوبة
│   ├── runtime.txt             # إصدار Python
│   └── Procfile                # إعدادات النشر
│
├── frontend/                   # 🎨 تطبيق Vue.js
│   ├── src/
│   │   ├── components/        # مكونات Vue
│   │   │   ├── CameraComponent.vue      # التقاط من الكاميرا
│   │   │   ├── ReportComponent.vue      # عرض النتائج
│   │   │   └── HistoryComponent.vue     # السجل التاريخي
│   │   ├── App.vue            # المكون الرئيسي
│   │   ├── main.js            # نقطة البداية
│   │   └── style.css          # الأنماط
│   ├── public/                # ملفات ثابتة
│   ├── package.json           # المكتبات
│   └── vite.config.js         # إعدادات Vite
│
├── .gitignore                 # قواعد Git
└── README.md                  # هذا الملف
```

---

## 🚀 **كيفية البدء**

### المتطلبات
- **Node.js** v16+
- **Python** 3.11+
- **npm** أو **yarn**
- مفتاح **Google Gemini API**

### 1. تثبيت Backend (Python)

```bash
cd backend

# تثبيت المكتبات
pip install -r requirements.txt

# إنشاء ملف .env
echo "GEMINI_API_KEY=your_api_key_here" > .env

# تشغيل الخادم
python api.py
```

الخادم سيعمل على: `http://localhost:8000`

### 2. تثبيت Frontend (Vue.js)

```bash
cd frontend

# تثبيت المكتبات
npm install

# تشغيل dev server
npm run dev
```

التطبيق سيعمل على: `http://localhost:5173`

### 3. الحصول على مفتاح Gemini API

1. اذهب إلى [Google AI Studio](https://aistudio.google.com/app/apikey)
2. انقر على "Create API Key"
3. انسخ المفتاح و ضعه في ملف `.env` في مجلد backend

---

## 🎯 **كيفية الاستخدام**

### 📸 التقاط صورة
1. اذهب لتبويب **"📸 التقاط"**
2. انقر على **"🎥 تشغيل الكاميرا"**
3. اختر زاوية مناسبة و أضاءة جيدة
4. انقر على **"📷 التقط صورة"**
5. انقر على **"🚀 حلل الصورة"**

### 📊 مشاهدة النتائج
1. اذهب لتبويب **"📊 النتائج"**
2. شاهد التقرير الكامل مع:
   - صورتك
   - نوع البشرة والمؤشرات
   - رسم بياني للتقييم
   - التوصيات المخصصة

### 📚 مشاهدة السجل
1. اذهب لتبويب **"📚 السجل"**
2. شاهد جميع التحليلات السابقة
3. انقر على أي نتيجة لمشاهدة التفاصيل

---

## 🔧 **المتطلبات الأساسية**

### Backend Requirements
```
fastapi==0.135.1
uvicorn[standard]==0.32.1
google-generativeai==0.8.6
python-dotenv==1.0.0
python-multipart==0.0.9
pillow==10.2.0
opencv-python==4.8.1.78
face-recognition==1.3.0
```

### Frontend Dependencies
```
vue: ^3.4.0
chart.js: ^4.4.0
axios: ^1.6.0
tailwindcss: ^3.4.0
vite: ^5.0.0
autoprefixer: ^10.4.16
postcss: ^8.4.32
```

---

## 📱 **الميزات التقنية**

### Face Detection 🔍
- استخدام `face-recognition` library
- كشف الوجوه تلقائياً قبل التحليل
- رفض الصور التي لا تحتوي على وجه
- رفض الصور التي تحتوي على أكثر من وجه

### Caching System 💾
- حفظ النتائج بناءً على hash الصورة
- نفس الصورة = نفس النتيجة دائماً
- تحسن الأداء للصور المكررة

### localStorage Integration 🗄️
- حفظ النتائج محلياً في المتصفح
- حفظ آخر 50 نتيجة تحليل
- بيانات لا تحتاج خادم لحفظها

### Real-time Camera 📹
- استخدام `getUserMedia` API
- معاينة حية من الكاميرا
- معالجة الصور في الذاكرة (لا حفظ)

### Chart.js Integration 📊
- رسوم بيانية جميلة وتفاعلية
- Radar Chart لتقييم مؤشرات البشرة
- ألوان احترافية

---

## 🌐 **النشر على الإنترنت**

### نشر Backend على Render

1. أنشئ حساب على [Render.com](https://render.com)
2. اربط مستودع GitHub
3. أنشئ "Web Service"
4. اختر Python كـ Runtime
5. سيتعرف Render على `requirements.txt` و `Procfile` تلقائياً
6. ضع متغيرات البيئة (GEMINI_API_KEY)

### نشر Frontend على Vercel

1. أنشئ حساب على [Vercel.com](https://vercel.com)
2. اربط مستودع GitHub
3. اختر `frontend` كـ Root Directory
4. غير العنوان في `CameraComponent.vue` من `http://localhost:8000` إلى عنوان الخادم الحقيقي
5. أنقر Deploy

---

## 📝 **ملاحظات مهمة**

### أمان البيانات
- الصور لا تُحفظ على الخادم
- تحسب من الذاكرة مباشرة
- localStorage آمن للاستخدام الشخصي

### الأداء
- استخدام PIL بدلاً من base64 للسرعة
- Caching يقلل استدعاءات API
- localStorage يقلل استخدام الـ bandwidth

### التوافقية
- يعمل على Chrome, Firefox, Edge, Safari
- يعمل على iOS و Android
- يعمل بدون إنترنت بعد التحميل الأول (PWA قريباً)

---

## 🔐 **متغيرات البيئة**

### Backend (.env)
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 📧 **الدعم والمساعدة**

إذا واجهت أي مشاكل:

1. تأكد من تثبيت جميع المكتبات
2. تأكد من مفتاح Gemini API صحيح
3. تأكد من أن الكاميرا مفعلة في المتصفح
4. تحقق من console للأخطاء

---

## 📄 **الترخيص**

هذا المشروع مفتوح المصدر. استخدمه بحرية! ✨

---

## 🎉 **شكر خاص**

- Google Gemini AI
- Vue.js Community
- FastAPI Framework
- Chart.js Library

---

**تم تطويره بـ ❤️ من قبل مرام**
