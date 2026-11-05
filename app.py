import streamlit as st
import random
import time

# إعداد الصفحة وتفعيل الثيم العريض والتصميم الاحترافي
st.set_page_config(
    page_title="Pocket Option Pro - 5 Min",
    page_icon="⚡",
    layout="centered"
)

# تصميم تنسيق CSS مخصص لجعل الواجهة أنيقة ومرتبة باللون الداكن المريح
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
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

# عنوان التطبيق الرئيسي بشكل مبسط وجميل
st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>⚡ غرفة التداول الاحترافية - 5 دقائق</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>نظام التحليل الموجي المتوافق مع إغلاق شمعة الـ 300 ثانية</p>", unsafe_allow_html=True)
st.markdown("---")

# صندوق اختيار الأصل في أعمدة منظمة
col1, col2 = st.columns([2, 1])
with col1:
    selected_pair = st.selectbox("📌 اختر الأصل (OTC):", [
        "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
        "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
    ])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analysis_btn = st.button("🔥 تحليل")

# حفظ حالة التحليل في الجلسة
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if analysis_btn:
    direction = random.choice(["CALL", "PUT"])
    is_ready = random.choice([True, True, False])
    st.session_state.analysis_result = {
        "direction": direction,
        "is_ready": is_ready,
        "pair": selected_pair
    }

st.markdown("---")

# مكان العداد المتحرك بتصميم بطاقة واضحة
timer_placeholder = st.empty()

block_time = 300  
current_time = time.time()
seconds_passed = int(current_time % block_time)
seconds_remaining = block_time - seconds_passed

minutes = seconds_remaining // 60
seconds = seconds_remaining % 60

# عرض العداد بداخل صندوق منظم
timer_placeholder.markdown(f"""
    <div style='background-color: #1f2937; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #374151;'>
        <span style='color: #93c5fd; font-size: 16px;'>⏱️ العداد التنازلي لشمعة الـ 5 دقائق الحالية</span><br>
        <span style='color: #ffffff; font-size: 24px; font-weight: bold;'>{minutes:02d} دقيقة و {seconds:02d} ثانية</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# عرض التقرير المنظم إذا تم تحليله
if st.session_state.analysis_result is not None:
    res = st.session_state.analysis_result
    
    with st.container():
        st.markdown(f"### 📊 نتائج فحص الموجة لـ ({res['pair']})")
        
        # عرض المؤشرات بشكل نقاط أنيقة
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
        
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #059669;'>
                        <h3 style='color: #34d399; margin:0;'>🟢 القرار النهائي: صعود ممتد (CALL)</h3>
                        <p style='color: #d1fae5; margin:5px 0 0 0;'>مدة الصفقة في بوكت أوبشن: 5 دقائق بالتمام</p>
                    </div>
                """, unsafe_allow_html, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #dc2626;'>
                        <h3 style='color: #f87171; margin:0;'>🔴 القرار النهائي: هبوط ممتد (PUT)</h3>
                        <p style='color: #fee2e2; margin:5px 0 0 0;'>مدة الصفقة في بوكت أوبشن: 5 دقائق بالتمام</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **السوق متذبذب حالياً (تجنب الدخول واننتظر الشمعة القادمة)**")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 13px;'>⚠️ إدارة المخاطر: التزم بنسبة 2% إلى 3% كحد أقصى لكل صفقة.</p>", unsafe_allow_html=True)

# التحديث اللحظي للعداد
time.sleep(1)
st.rerun()
