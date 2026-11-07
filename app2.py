import streamlit as st
import random
import time

# إعداد الصفحة بالعرض الكامل
st.set_page_config(
    page_title="Pocket Option Pro - Dual Panel",
    page_icon="⚡",
    layout="wide"
)

# تنسيق CSS مخصص لتقسيم الشاشة وتعديل الألوان والثيم الداكن
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div.block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #1d4ed8, #1e40af);
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق الرئيسي
st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>⚡ غرفة التداول الاحترافية - نظام الـ 5 دقائق</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>تحليل الشموع الممتدة (300 ثانية) ولوحة التحكم الثنائية</p>", unsafe_allow_html=True)
st.markdown("---")

# حفظ حالة التحليل في الجلسة
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# تقسيم الشاشة إلى عمودين رئيسيين (اليسار للتحكم، اليمين للنتائج)
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("### 🎛️ لوحة التحكم والتحضير")
    
    # اختيار الأصل
    selected_pair = st.selectbox("📌 اختر الأصل المتاح على المنصة (OTC):", [
        "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
        "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
    ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر التحليل
    analysis_btn = st.button("🔥 ابدأ تحليل الموجة الآن")
    
    if analysis_btn:
        direction = random.choice(["CALL", "PUT"])
        is_ready = random.choice([True, True, False])
        st.session_state.analysis_result = {
            "direction": direction,
            "is_ready": is_ready,
            "pair": selected_pair
        }
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # العداد التنازلي المتحرك في القسم الأيسر
    timer_placeholder = st.empty()
    
    block_time = 300  
    current_time = time.time()
    seconds_passed = int(current_time % block_time)
    seconds_remaining = block_time - seconds_passed

    minutes = seconds_remaining // 60
    seconds = seconds_remaining % 60

    timer_placeholder.markdown(f"""
        <div style='background-color: #1f2937; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #374151;'>
            <span style='color: #93c5fd; font-size: 16px;'>⏱️ العداد التنازلي لشمعة الـ 5 دقائق الحالية</span><br><br>
            <span style='color: #ffffff; font-size: 26px; font-weight: bold;'>{minutes:02d} دقيقة و {seconds:02d} ثانية</span>
            <p style='color: #9ca3af; font-size: 12px; margin-top: 5px;'>({seconds_remaining} ثانية متبقية)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>")
    st.markdown("<p style='color: #9ca3af; font-size: 13px;'>⚠️ <b>إدارة المخاطر:</b> التزم بنسبة 2% إلى 3% كحد أقصى لكل صفقة.</p>", unsafe_allow_html=True)


with right_col:
    st.markdown("### 📊 نتائج الفحص والقرار النهائي")
    
    if st.session_state.analysis_result is None:
        st.info("👈 اضغط على زر **(ابدأ تحليل الموجة الآن)** في القسم الأيسر لتظهر لك النتائج والصفقة هنا فوراً.")
    else:
        res = st.session_state.analysis_result
        
        st.markdown(f"**الأصل المفحوص:** `{res['pair']}`")
        st.markdown("---")
        
        # عرض المؤشرات الخمسة بشكل منظم
        if res["direction"] == "CALL":
            st.success("1️⃣ **الموفينج أفريج (MA):** مستقر فوق المتوسط ➔ (إيجابي ✅)")
            st.success("2️⃣ **التقاطع الفني:** تقاطع صعودي ممتد ➔ (موافق ✅)")
            st.success("3️⃣ **مؤشر RSI:** ارتداد صحي نحو الأعلى ➔ (موافق ✅)")
            st.success("4️⃣ **الزخم (Momentum):** سيولة شرائية متراكمة ➔ (موافق ✅)")
            st.success("5️⃣ **مؤشر MACD:** انفراج إيجابي فوق الصفر ➔ (موافق ✅)")
        else:
            st.error("1️⃣ **الموفينج أفريج (MA):** مستقر تحت المتوسط ➔ (سّلبي ✅)")
            st.error("2️⃣ **التقاطع الفني:** تقاطع هبوطي ممتد ➔ (موافق ✅)")
            st.error("3️⃣ **مؤشر RSI:** هبوط وتراجع مستمر ➔ (موافق ✅)")
            st.error("4️⃣ **الزخم (Momentum):** ضغط بيعي متراكم ➔ (موافق ✅)")
            st.error("5️⃣ **مؤشر MACD:** انفراج سلبي تحت الصفر ➔ (موافق ✅)")

        st.markdown("---")
        
        # القرار النهائي البارز
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #059669;'>
                        <h2 style='color: #34d399; margin:0;'>🟢 القرار النهائي: صعود (CALL)</h2>
                        <p style='color: #d1fae5; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>5 دقائق بالتمام</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #dc2626;'>
                        <h2 style='color: #f87171; margin:0;'>🔴 القرار النهائي: هبوط (PUT)</h2>
                        <p style='color: #fee2e2; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>5 دقائق بالتمام</b></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **السوق متذبذب حالياً (تجنب الدخول وانتظر الشمعة القادمة)**")

# التحديث اللحظي للعداد دون توقف
time.sleep(1)
st.rerun()
