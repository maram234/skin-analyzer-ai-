<template>
  <div :class="['min-h-screen bg-[#050505] text-[#e0e0e0] p-4 md:p-10 selection:bg-cyan-500/30 transition-all duration-700 font-roboto-condensed', currentLang === 'ar' ? 'text-right' : 'text-left']" :dir="currentLang === 'ar' ? 'rtl' : 'ltr'">
    
    <header class="max-w-6xl mx-auto flex justify-between items-center mb-16 animate-fade-down">
      <div class="space-y-1">
        <h1 class="text-3xl md:text-4xl font-black tracking-tighter text-white inline-flex items-center gap-2">
          <span class="bg-cyan-600 px-3 py-1 rounded-xl text-black italic shadow-lg shadow-cyan-600/20">SM</span>
          SKIN MIRROR <span class="text-cyan-500">AI</span>
        </h1>
        <p class="text-slate-500 text-[10px] font-bold uppercase tracking-[0.3em] opacity-80">
          {{ currentLang === 'ar' ? 'مختبر تحليل البشرة الرقمي | النسخة الاحترافية' : 'Digital Skin Analysis Lab | Professional Version' }}
        </p>
      </div>

      <div class="flex items-center gap-1 bg-white/5 p-1 rounded-2xl border border-white/10 backdrop-blur-xl">
        <button @click="currentLang = 'en'" :class="['px-4 py-2 rounded-xl text-xs font-black transition-all duration-300', currentLang === 'en' ? 'bg-cyan-500 text-black shadow-[0_0_20px_rgba(34,211,238,0.4)]' : 'text-slate-400 hover:text-white hover:bg-white/5']">EN</button>
        <button @click="currentLang = 'ar'" :class="['px-4 py-2 rounded-xl text-xs font-black transition-all duration-300', currentLang === 'ar' ? 'bg-cyan-500 text-black shadow-[0_0_20px_rgba(34,211,238,0.4)]' : 'text-slate-400 hover:text-white hover:bg-white/5']">AR</button>
      </div>
    </header>

    <!-- Medical Disclaimer Banner -->
    <div class="max-w-6xl mx-auto mb-10 px-5 py-4 rounded-2xl border border-amber-500/20 bg-amber-500/5 flex items-start gap-4 animate-fade-down">
      <div class="text-amber-400 mt-0.5 shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
      </div>
      <p class="text-amber-300/80 text-[11px] leading-relaxed font-medium">
        <span class="font-black uppercase tracking-widest text-amber-400">{{ currentLang === 'ar' ? 'إخلاء مسؤولية طبي' : 'Medical Disclaimer' }}</span>
        &nbsp;—&nbsp;
        {{ currentLang === 'ar'
          ? 'هذه الأداة مصممة للأغراض المعلوماتية والتوعوية فقط. النتائج المعروضة لا تُعدّ تشخيصًا طبيًا ولا توصية علاجية. يُرجى دائمًا استشارة طبيب أو متخصص في الأمراض الجلدية قبل اتخاذ أي قرار يتعلق بصحة بشرتك.'
          : 'This tool is designed for informational and educational purposes only. Results are not a medical diagnosis or treatment recommendation. Always consult a licensed dermatologist or healthcare professional before making any decisions about your skin health.'
        }}
      </p>
    </div>

    <main class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">

      <!-- Scanning Module -->
      <section class="lg:col-span-5 sticky top-10 animate-fade-left">
        <div class="relative glass-premium rounded-[3rem] p-5 border border-white/10 shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] overflow-hidden">
          <div class="aspect-[4/5] rounded-[2.2rem] overflow-hidden bg-black relative shadow-inner border border-white/5 group">
            
            <div v-if="isCameraOpen || capturedImage" class="h-full relative overflow-hidden">
              <video v-if="isCameraOpen" ref="video" autoplay playsinline class="w-full h-full object-cover opacity-90 scale-105 transition-transform duration-700 group-hover:scale-100"></video>
              <img v-else :src="capturedImage" class="w-full h-full object-cover opacity-80 scale-105 animate-pulse-slow">
              
              <div v-if="loading" class="absolute inset-x-0 top-0 h-[3px] bg-cyan-400 shadow-[0_0_25px_#22d3ee] animate-scan z-20"></div>
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none"></div>
              <div class="absolute inset-0 face-grid opacity-20 pointer-events-none"></div>
            </div>

            <div v-else class="h-full flex flex-col items-center justify-center p-12 text-center bg-[#080808]">
              <div class="w-20 h-20 bg-cyan-500/10 rounded-full flex items-center justify-center mb-8 animate-pulse text-cyan-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
              </div>
              <h3 class="text-white font-black text-xl mb-3 tracking-tight">{{ currentLang === 'ar' ? 'النظام جاهز' : 'System Ready' }}</h3>
              <p class="text-slate-500 text-sm leading-relaxed max-w-[240px]">
                {{ currentLang === 'ar' ? 'ابدأ المسح للحصول على نظرة واضحة عن حالة بشرتك.' : 'Start a scan to receive a clear overview of your skin condition.' }}
              </p>
            </div>
          </div>

          <div class="mt-8 space-y-4 px-2">
            <button v-if="isCameraOpen" @click="captureAndAnalyze" :disabled="loading" 
              class="w-full py-5 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:to-cyan-400 text-white rounded-[1.5rem] font-black tracking-widest transition-all shadow-xl shadow-cyan-900/30 active:scale-95 disabled:opacity-50">
              {{ loading ? (currentLang === 'ar' ? 'جاري التحليل...' : 'ANALYZING...') : (currentLang === 'ar' ? 'بدء فحص الذكاء الاصطناعي' : 'RUN AI DIAGNOSIS') }}
            </button>

            <div v-if="!isCameraOpen" class="grid grid-cols-2 gap-4">
              <button @click="startCamera" class="py-5 bg-white text-black rounded-[1.5rem] font-black text-xs hover:bg-cyan-400 transition-all shadow-lg active:scale-95 text-center flex flex-col items-center justify-center">
                <span class="block">{{ currentLang === 'ar' ? 'مسح مباشر' : 'Live Scan' }}</span>
                <span class="text-[8px] opacity-60 font-normal mt-1 max-w-[80%]">{{ currentLang === 'ar' ? 'تحلل البشرة بالكاميرا' : 'Camera live scanning' }}</span>
              </button>
              <label class="py-5 bg-white/5 text-slate-300 rounded-[1.5rem] font-black text-xs border border-white/10 text-center cursor-pointer hover:bg-white/10 hover:border-white/20 transition-all flex flex-col items-center justify-center active:scale-95">
                <span>{{ currentLang === 'ar' ? 'رفع صورة' : 'Upload Image' }}</span>
                <span class="text-[8px] opacity-40 font-normal mt-1">{{ currentLang === 'ar' ? 'رفع ملف للتحليل' : 'File upload mode' }}</span>
                <input type="file" @change="handleFileUpload" accept="image/*" class="hidden">
              </label>
            </div>
            
            <button v-if="isCameraOpen || capturedImage" @click="resetSession" class="w-full py-2 text-slate-600 hover:text-red-400 text-[11px] font-black tracking-[0.2em] transition-colors uppercase">
              {{ currentLang === 'ar' ? 'إنهاء الجلسة' : 'TERMINATE SESSION' }}
            </button>
          </div>
        </div>
      </section>

      <!-- Analysis Results -->
      <section class="lg:col-span-7 animate-fade-right">
        
        <div v-if="!analysisResult && !loading && !apiError" class="h-[600px] glass-premium rounded-[3rem] flex flex-col items-center justify-center p-16 text-center border-dashed border-2 border-white/10">
          <div class="relative mb-10">
            <div class="absolute inset-0 bg-cyan-500/20 blur-[50px] rounded-full"></div>
            <div class="text-6xl relative animate-float text-cyan-500/50">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-16 h-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
            </div>
          </div>
          <p class="text-slate-400 font-black uppercase tracking-[0.4em] text-xs leading-loose">
            {{ currentLang === 'ar' ? 'في انتظار بدء التحليل...' : 'Waiting for analysis...' }}
          </p>
        </div>

        <div v-if="apiError && !loading" class="glass-premium rounded-[3rem] p-16 flex flex-col items-center justify-center text-center border border-red-500/20 bg-red-500/5 min-h-[500px]">
          <div class="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mb-8 text-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          </div>
          <h3 class="text-red-400 font-black text-2xl mb-4">{{ currentLang === 'ar' ? 'فشل التحليل' : 'Analysis Internal Error' }}</h3>
          <p class="text-red-300 text-sm leading-relaxed max-w-md font-medium">{{ apiError[currentLang === 'ar' ? 'message_ar' : 'message_en'] || apiError.message }}</p>
          <button @click="resetSession" class="mt-10 px-8 py-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl text-xs font-black transition-all">RETRY ANALYSIS</button>
        </div>

        <div v-if="loading" class="glass-premium rounded-[3rem] p-24 flex flex-col items-center justify-center min-h-[500px]">
          <div class="loader-circle mb-10"></div>
          <p class="text-cyan-500 font-black text-sm uppercase tracking-[0.6em] animate-pulse">
            {{ currentLang === 'ar' ? 'جاري تحليل الأنسجة' : 'Deciphering Tissues' }}
          </p>
        </div>

        <div v-if="analysisResult" class="space-y-8 animate-fade-up">
          
          <!-- Key Metrics -->
          <div v-if="analysisResult[currentLang]" class="glass-premium p-10 rounded-[3rem] relative overflow-hidden backdrop-blur-3xl shadow-2xl">
             <div class="flex justify-between items-center mb-10">
               <h3 class="text-sm font-black uppercase tracking-widest text-slate-300 flex items-center gap-3">
                 <span class="w-1.5 h-4 bg-cyan-500 rounded-full shadow-[0_0_10px_#22d3ee]"></span> 
                 {{ currentLang === 'ar' ? 'الملاحظات السريرية' : 'Clinical Observations' }}
               </h3>
               <div v-if="analysisResult[currentLang].report_header" class="px-4 py-2 bg-white/5 rounded-2xl border border-white/10 text-[10px] font-black text-cyan-400 uppercase tracking-widest">
                 Conf: {{ analysisResult[currentLang].report_header.analysis_confidence }}
               </div>
             </div>
             
             <!-- clinical_observations as text cards -->
             <div v-if="analysisResult[currentLang].clinical_observations" class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
               <div v-for="(obs, name) in analysisResult[currentLang].clinical_observations" :key="name" class="p-5 bg-white/5 rounded-2xl border border-white/5 hover:border-cyan-500/20 transition-all group">
                 <span class="text-[11px] font-black uppercase text-cyan-500 tracking-widest block mb-2">{{ name }}</span>
                 <p class="text-slate-300 text-[13px] leading-relaxed font-medium">{{ obs }}</p>
               </div>
             </div>
          </div>

          <!-- Age & Skin Profile -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-if="analysisResult[currentLang] && analysisResult[currentLang].report_header" class="glass-premium p-10 rounded-[3rem] group hover:bg-cyan-500/5 transition-all">
              <span class="text-[11px] font-black text-slate-500 uppercase mb-4 block tracking-[0.3em]">{{ currentLang === 'ar' ? 'العمر التقريبي' : 'ESTIMATED BIO-AGE' }}</span>
              <div class="text-4xl font-black text-white italic tracking-tighter group-hover:text-cyan-400 transition-colors">
                {{ analysisResult[currentLang].report_header.approximate_age || 'N/A' }} 
                <span class="text-xs text-slate-600 ml-2 uppercase font-bold">{{ currentLang === 'ar' ? 'سنة' : 'Years' }}</span>
              </div>
            </div>

            <div v-if="analysisResult[currentLang] && analysisResult[currentLang].report_header" class="glass-premium p-10 rounded-[3rem] flex flex-col justify-center items-start group hover:bg-cyan-500/5 transition-all">
              <span class="text-[11px] font-black text-slate-500 uppercase mb-4 block tracking-[0.3em]">{{ currentLang === 'ar' ? 'تصنيف الحالة' : 'SKIN CLASSIFICATION' }}</span>
              <div class="text-2xl font-black text-cyan-500 uppercase tracking-tighter italic">
                {{ analysisResult[currentLang].report_header.skin_type }}
              </div>
            </div>

            <div v-if="analysisResult[currentLang] && analysisResult[currentLang].report_header && analysisResult[currentLang].report_header.overall_assessment" class="glass-premium p-10 rounded-[3rem] group hover:bg-cyan-500/5 transition-all">
              <span class="text-[11px] font-black text-slate-500 uppercase mb-4 block tracking-[0.3em]">{{ currentLang === 'ar' ? 'التقييم العام' : 'OVERALL ASSESSMENT' }}</span>
              <div class="text-base font-bold text-slate-300 leading-relaxed">
                {{ analysisResult[currentLang].report_header.overall_assessment }}
              </div>
            </div>
          </div>

          <!-- Concerns & Routine -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-if="analysisResult[currentLang] && analysisResult[currentLang].key_skin_concerns" class="glass-premium p-10 rounded-[3rem]">
              <h4 class="text-red-400/80 font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-2">
                <span class="w-1.5 h-3 bg-red-400 rounded-full"></span>
                {{ currentLang === 'ar' ? 'المشاكل المرصودة' : 'DETECTED CONCERNS' }}
              </h4>
              <ul class="space-y-4">
                <li v-for="(item, i) in analysisResult[currentLang].key_skin_concerns" :key="i" class="flex items-start gap-4 p-4 bg-white/5 rounded-2xl border border-white/5 hover:border-red-500/20 transition-all">
                  <span class="text-red-400 mt-1.5 w-1.5 h-1.5 rounded-full bg-red-400 shadow-[0_0_5px_#f87171]"></span>
                  <span class="text-slate-300 text-[13px] leading-relaxed font-medium">{{ item }}</span>
                </li>
              </ul>
            </div>

            <div v-if="analysisResult[currentLang].routine_recommendations" class="glass-premium p-10 rounded-[3rem]">
              <h4 class="text-cyan-400 font-black text-xs uppercase tracking-widest mb-6 flex items-center gap-2">
                <span class="w-1.5 h-3 bg-cyan-400 rounded-full"></span>
                {{ currentLang === 'ar' ? 'توصيات الروتين' : 'AI ROUTINE PROTOCOL' }}
              </h4>
              <ul class="space-y-4">
                <li v-for="(item, i) in analysisResult[currentLang].routine_recommendations" :key="i" class="flex items-start gap-4 p-4 bg-white/5 rounded-2xl border border-white/5 hover:border-cyan-500/20 transition-all">
                  <span class="text-cyan-400 mt-1">✓</span>
                  <span class="text-slate-300 text-[13px] leading-relaxed font-medium">{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Daily Routine -->
          <div v-if="analysisResult[currentLang] && analysisResult[currentLang].daily_routine" class="glass-premium p-10 rounded-[3rem]">
            <h4 class="text-cyan-400 font-black text-xs uppercase tracking-widest mb-8 flex items-center gap-2">
              <span class="w-1.5 h-3 bg-cyan-400 rounded-full"></span>
              {{ currentLang === 'ar' ? 'الروتين اليومي المقترح' : 'DAILY SKINCARE ROUTINE' }}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- Morning -->
              <div>
                <p class="text-[10px] font-black uppercase tracking-[0.3em] text-amber-400 mb-4 flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                  {{ currentLang === 'ar' ? 'الصباح' : 'Morning' }}
                </p>
                <ul class="space-y-3">
                  <li v-for="(step, i) in analysisResult[currentLang].daily_routine.morning" :key="'m'+i" class="flex items-start gap-3 p-3 bg-white/5 rounded-2xl border border-white/5 hover:border-amber-400/20 transition-all">
                    <span class="text-amber-400 font-black text-xs mt-0.5">{{ i+1 }}</span>
                    <span class="text-slate-300 text-[13px] leading-relaxed font-medium">{{ step }}</span>
                  </li>
                </ul>
              </div>
              <!-- Evening -->
              <div>
                <p class="text-[10px] font-black uppercase tracking-[0.3em] text-indigo-400 mb-4 flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
                  {{ currentLang === 'ar' ? 'المساء' : 'Evening' }}
                </p>
                <ul class="space-y-3">
                  <li v-for="(step, i) in analysisResult[currentLang].daily_routine.evening" :key="'e'+i" class="flex items-start gap-3 p-3 bg-white/5 rounded-2xl border border-white/5 hover:border-indigo-400/20 transition-all">
                    <span class="text-indigo-400 font-black text-xs mt-0.5">{{ i+1 }}</span>
                    <span class="text-slate-300 text-[13px] leading-relaxed font-medium">{{ step }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Advanced Clinical Summary -->
          <div v-if="summaryText" class="glass-premium p-12 rounded-[3.5rem] bg-gradient-to-br from-cyan-900/10 to-transparent border border-cyan-500/10 relative overflow-hidden">
            <div class="absolute -top-10 -right-10 w-40 h-40 bg-cyan-500/5 blur-[80px] rounded-full"></div>
            <h4 class="text-cyan-400 font-black text-xs uppercase tracking-[0.5em] mb-8 text-center">{{ currentLang === 'ar' ? 'التقرير المختبري التفصيلي' : 'DETAILED CLINICAL BIO-REPORT' }}</h4>
            <p class="text-slate-300 text-lg leading-[2] italic font-medium opacity-95 text-center px-4">
              "{{ summaryText }}"
            </p>
            <div class="mt-10 pt-10 border-t border-white/5 text-center">
              <span class="text-[9px] font-black tracking-[0.4em] text-slate-600 uppercase italic">Digital Analysis Result | Professional v2.0</span>
            </div>
          </div>

        </div>

        <div class="mt-24 glass-premium p-12 rounded-[3rem] border border-white/10 animate-on-scroll">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
            <div class="space-y-8">
              <h2 class="text-3xl font-black text-white flex items-center gap-4">
                {{ currentLang === 'ar' ? 'عن Skin Mirror' : 'About Skin Mirror' }}
              </h2>
              <div class="space-y-6 text-slate-400 text-base leading-relaxed font-medium">
                <p>
                  {{ currentLang === 'ar' 
                    ? 'Skin Mirror هو نظام رقمي لتحليل البشرة يساعد المستخدمين على فهم حالة بشرتهم بشكل أفضل. يقوم النظام بمراجعة مظهر البشرة وتقديم ملاحظات تساعد على تكوين صورة أوضح عن حالة الجلد والعوامل المرتبطة به.' 
                    : 'Skin Mirror is a digital skin analysis platform designed to help users better understand their skin. The system reviews visual skin features and provides helpful observations that offer a clearer overview of skin condition.' 
                  }}
                </p>
                <p>
                  {{ currentLang === 'ar' 
                    ? 'هدفنا هو تقديم تجربة بسيطة تساعد المستخدم على التعرف على احتياجات بشرته بطريقة سهلة وواضحة.' 
                    : 'Our goal is to provide a simple and accessible way for users to explore their skin characteristics and gain useful insights.' 
                  }}
                </p>
              </div>
            </div>

            <div class="space-y-10">
              <h2 class="text-2xl font-black text-white px-2">
                {{ currentLang === 'ar' ? 'المميزات' : 'Key Features' }}
              </h2>
              <div class="grid gap-6">
                <div class="p-6 bg-white/5 rounded-3xl border border-white/5 hover:bg-white/10 transition-colors">
                  <h4 class="text-cyan-500 font-black text-sm uppercase mb-2 tracking-widest">{{ currentLang === 'ar' ? 'ملاحظات واضحة' : 'Clear Insights' }}</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">{{ currentLang === 'ar' ? 'ملاحظات واضحة تساعد على فهم حالة البشرة.' : 'Helpful observations to better understand your skin.' }}</p>
                </div>
                <div class="p-6 bg-white/5 rounded-3xl border border-white/5 hover:bg-white/10 transition-colors">
                  <h4 class="text-cyan-500 font-black text-sm uppercase mb-2 tracking-widest">{{ currentLang === 'ar' ? 'تجربة بسيطة' : 'Simple Experience' }}</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">{{ currentLang === 'ar' ? 'واجهة بسيطة وسهلة الاستخدام مصممة لتحليل سريع.' : 'Easy and smooth interface designed for quick analysis.' }}</p>
                </div>
                <div class="p-6 bg-white/5 rounded-3xl border border-white/5 hover:bg-white/10 transition-colors">
                  <h4 class="text-cyan-500 font-black text-sm uppercase mb-2 tracking-widest">{{ currentLang === 'ar' ? 'تركيز على الخصوصية' : 'Privacy Focused' }}</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">{{ currentLang === 'ar' ? 'حماية خصوصية المستخدم أثناء عملية التحليل.' : 'Your data and images remain private during the analysis process.' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>
    </main>

    <!-- Footer -->
    <footer class="max-w-6xl mx-auto mt-32 mb-16 border-t border-white/5 pt-16 animate-fade-up">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12 items-start opacity-70 hover:opacity-100 transition-opacity duration-500">
        
        <div class="md:col-span-5 space-y-6">
          <h2 class="text-2xl font-black tracking-tight text-white flex items-center gap-2">
            <span class="text-cyan-500">SM</span> SKIN MIRROR AI
          </h2>
          <p class="text-zinc-500 text-sm leading-relaxed max-w-sm">
            {{ currentLang === 'ar' 
              ? 'منصة رقمية تساعد المستخدمين على فهم حالة بشرتهم من خلال تحليل بصري بسيط وواضح.' 
              : 'A digital platform focused on helping users explore and understand their skin condition through visual analysis.' 
            }}
          </p>
        </div>

        <div class="md:col-span-4 flex flex-col items-center md:items-start space-y-4">
          <h4 class="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-400">{{ currentLang === 'ar' ? 'روابط' : 'Connect' }}</h4>
            <div class="flex gap-4">
              <a href="https://github.com/maram234" target="_blank" class="text-zinc-500 hover:text-white transition-colors">
                <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.042-1.416-4.042-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.003.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
              </a>
              <a href="https://linkedin.com" target="_blank" class="text-zinc-500 hover:text-cyan-500 transition-colors">
                 <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
              </a>
            </div>
          </div>


        <div class="md:col-span-3 text-right space-y-4">
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-zinc-500 leading-relaxed">
            Designed & Developed by <br/> 
            <span class="text-zinc-300 text-xs">Maram Mohamed</span>
          </p>
          <div class="pt-4 border-t border-white/5 space-y-2">
            <p class="text-[9px] font-bold text-zinc-600">© 2026 SKIN MIRROR AI LABS. ALL RIGHTS RESERVED.</p>
            <p class="text-[9px] text-zinc-700 leading-relaxed">
              {{ currentLang === 'ar'
                ? 'هذا البرنامج لأغراض تعليمية فقط وليس بديلاً عن الاستشارة الطبية المتخصصة.'
                : 'This software is for educational purposes only and is not a substitute for professional medical advice.'
              }}
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// State Variables
const currentLang = ref('ar')
const video = ref(null)
const loading = ref(false)
const isCameraOpen = ref(false)
const analysisResult = ref(null)
const apiError = ref(null)
const capturedImage = ref(null)

// التعديل: استهداف بورت البايثون مباشرة
const API_BASE_URL = "http://127.0.0.1:8000"

const summaryText = computed(() => {
  if (!analysisResult.value || !analysisResult.value[currentLang.value]) return ""
  const s = analysisResult.value[currentLang.value].clinical_summary
  return Array.isArray(s) ? s[0] : (s || "")
})

// Helper functions for UI
const getIconForMetric = (name) => {
  return "" // Emojis removed as requested
}

// Functions
const startCamera = async () => {
  isCameraOpen.value = true
  capturedImage.value = null
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    setTimeout(() => { if (video.value) video.value.srcObject = stream }, 100)
  } catch (err) { 
    alert("Camera access denied.")
    isCameraOpen.value = false 
  }
}

const stopCamera = () => {
  if (video.value?.srcObject) {
    video.value.srcObject.getTracks().forEach(track => track.stop())
  }
  isCameraOpen.value = false
}

const resetSession = () => {
  stopCamera()
  capturedImage.value = null
  analysisResult.value = null
  apiError.value = null
}

const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    capturedImage.value = URL.createObjectURL(file)
    sendToServer(file)
  }
}

const captureAndAnalyze = () => {
  const canvas = document.createElement("canvas")
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  canvas.getContext("2d").drawImage(video.value, 0, 0)
  canvas.toBlob(blob => {
    capturedImage.value = URL.createObjectURL(blob)
    sendToServer(blob)
  }, 'image/jpeg')
}

const sendToServer = async (file) => {
  loading.value = true
  analysisResult.value = null
  apiError.value = null
  
  const form = new FormData()
  form.append("file", file)

  try {
    const res = await axios.post(
      `${API_BASE_URL}/analyze`,
      form,
      { 
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000
      }
    )

    const data = res.data.analysis

    if (data.status === 'error') {
      apiError.value = data
      if (isCameraOpen.value) stopCamera()
      return
    }

    analysisResult.value = data
    console.log("Professional Analysis Ready:", analysisResult.value)
    if (isCameraOpen.value) stopCamera()
  } catch (e) {
    console.error("Communication Error:", e)

    let msgEn = "Connection error. Please try again."
    let msgAr = "خطأ في الاتصال. حاولي مرة أخرى."

    if (e.code === 'ECONNABORTED') {
      msgEn = "Analysis timed out. The model took too long — please try again."
      msgAr = "انتهى وقت التحليل. استغرق الموديل وقتًا طويلًا — حاولي مجددًا."
    } else if (e.response?.data?.detail) {
      msgEn = "Server Error: " + e.response.data.detail
      msgAr = "خطأ في السيرفر: " + e.response.data.detail
    } else if (e.response?.data?.analysis?.message_en) {
      msgEn = e.response.data.analysis.message_en
      msgAr = e.response.data.analysis.message_ar
    } else if (e.message) {
      msgEn = e.message
      msgAr = e.message
    }

    apiError.value = { message_en: msgEn, message_ar: msgAr }
  } finally {
    loading.value = false
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&family=Cairo:wght@300;400;700;900&display=swap');

.font-roboto-condensed { font-family: 'Roboto Condensed', sans-serif; }
.font-cairo { font-family: 'Cairo', sans-serif; }

body { background: #050505; color: #e0e0e0; overflow-x: hidden; }

.glass-premium { 
  backdrop-filter: blur(40px) saturate(180%); 
  background: rgba(255, 255, 255, 0.03); 
  border: 1px solid rgba(255, 255, 255, 0.08); 
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.glass-premium:hover {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.face-grid { 
  background-image: radial-gradient(rgba(34, 211, 238, 0.2) 1px, transparent 1px); 
  background-size: 40px 40px; 
}

@keyframes scan { 
  0% { transform: translateY(0); opacity: 0; } 
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { transform: translateY(480px); opacity: 0; } 
}

.animate-scan { animation: scan 3s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite; position: absolute; width: 100%; pointer-events: none; }

.loader-circle {
  width: 60px;
  height: 60px;
  border: 3px solid rgba(34, 211, 238, 0.1);
  border-top: 3px solid #22d3ee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}
.animate-float { animation: float 6s ease-in-out infinite; }

.animate-fade-up { animation: fadeUp 0.8s ease-out forwards; }
.animate-fade-down { animation: fadeDown 0.8s ease-out forwards; }
.animate-fade-left { animation: fadeLeft 1s ease-out forwards; }
.animate-fade-right { animation: fadeRight 1s ease-out forwards; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeDown { from { opacity: 0; transform: translateY(-40px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeLeft { from { opacity: 0; transform: translateX(-40px); } to { opacity: 1; transform: translateX(0); } }
@keyframes fadeRight { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: translateX(0); } }

.animate-pulse-slow { animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
@keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 0.4; } }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #1a1a1a; border-radius: 10px; border: 2px solid #050505; }
::-webkit-scrollbar-thumb:hover { background: #333; }

@keyframes fade { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>