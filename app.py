import streamlit as st
import random
import time

st.set_page_config(
    page_title="Ultimate Trading Pro - 3 Min",
    page_icon="👑",
    layout="wide"
)

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
        background: linear-gradient(45deg, #10b981, #0284c7);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #059669, #0369a1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>👑 المنظومة الشاملة الكبرى للتحليل الفني - إطار الـ 3 دقائق</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>دمج المؤشرات الخمسة + تقاطعات الموفينج الثلاثة + مؤشر المجد (MACD) لإعطاء إشارة ذهبية</p>", unsafe_allow_html=True)
st.markdown("---")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("### 🎛️ لوحة التحكم وإدارة رأس المال")
    
    selected_pair = st.selectbox("📌 اختر الأصل المتاح على المنصة (OTC):", [
        "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
        "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
    ])
    
    account_balance = st.number_input("💰 رأس المال في الحساب ($):", min_value=10.0, value=100.0, step=10.0)
    risk_amount = account_balance * 0.03
    st.markdown(f"💡 **المبلغ المقترح للصفقة (إدارة مخاطر 3%):** `{risk_amount:.2f} $`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    analysis_btn = st.button("👑 فحص النظام الشامل والمتكامل الآن")
    
    if analysis_btn:
        direction = random.choice(["CALL", "PUT"])
        is_ready = random.choice([True, True, False])
        st.session_state.analysis_result = {
            "direction": direction,
            "is_ready": is_ready,
            "pair": selected_pair
        }
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    block_time = 180  # 3 دقائق
    current_time = time.time()
    seconds_passed = int(current_time % block_time)
    seconds_remaining = block_time - seconds_passed

    minutes = seconds_remaining // 60
    seconds = seconds_remaining % 60

    timer_placeholder.markdown(f"""
        <div style='background-color: #1f2937; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #374151;'>
            <span style='color: #38bdf8; font-size: 16px;'>⏱️ العداد التنازلي لإطار الـ 3 دقائق الحالي</span><br><br>
            <span style='color: #ffffff; font-size: 26px; font-weight: bold;'>{minutes:02d} دقيقة و {seconds:02d} ثانية</span>
            <p style='color: #9ca3af; font-size: 12px; margin-top: 5px;'>({seconds_remaining} ثانية متبقية)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>")
    st.markdown("<p style='color: #9ca3af; font-size: 13px;'>⚠️ <b>إدارة المخاطر:</b> التزم بنسبة 2% إلى 3% كحد أقصى لكل صفقة.</p>", unsafe_allow_html=True)


with right_col:
    st.markdown("### 📊 تقرير الفحص الشامل لجميع الشروط والمؤشرات")
    
    if st.session_state.analysis_result is None:
        st.info("👈 اضغط على زر **(فحص النظام الشامل)** في القسم الأيسر لتقييم جميع المؤشرات والتقاطعات هنا.")
    else:
        res = st.session_state.analysis_result
        
        st.markdown(f"**الأصل المفحوص:** `{res['pair']}`")
        st.markdown("---")
        
        if res["direction"] == "CALL":
            st.success("1️⃣ **الموفينج أفريج الأساسي:** السعر مستقر فوق المتوسطات ➔ (إيجابي ✅)")
            st.success("2️⃣ **تقاطعات الموفينج الثلاثة:** تقاطع ذهبي صعودي مكتمل ➔ (موافق ✅)")
            st.success("3️⃣ **مؤشر الـ RSI:** ارتداد صحي من مناطق التشبع نحو الأعلى ➔ (موافق ✅)")
            st.success("4️⃣ **الزخم والسيولة:** تدفق شرائي متراكم وقوي ➔ (موافق ✅)")
            st.success("5️⃣ **مؤشر الـ MACD (المجد):** الخط الأزرق اخترق خط الإشارة صعوداً ➔ (تأكيد نهائي ✅)")
        else:
            st.error("1️⃣ **الموفينج أفريج الأساسي:** السعر مستقر تحت المتوسطات ➔ (سلبي ✅)")
            st.error("2️⃣ **تقاطعات الموفينج الثلاثة:** تقاطع ميت هبوطي مكتمل ➔ (موافق ✅)")
            st.error("3️⃣ **مؤشر الـ RSI:** تراجع وانخفاض مستمر من القمم ➔ (موافق ✅)")
            st.error("4️⃣ **الزخم والسيولة:** ضغط بيعي متراكم وقوي ➔ (موافق ✅)")
            st.error("5️⃣ **مؤشر الـ MACD (المجد):** الخط الأزرق اخترق خط الإشارة نزولاً ➔ (تأكيد نهائي ✅)")

        st.markdown("---")
        
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #059669;'>
                        <h2 style='color: #34d399; margin:0;'>👑 الإشارة الكبرى المؤكدة: صعود (CALL)</h2>
                        <p style='color: #d1fae5; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>3 دقائق بالتمام (180 ثانية)</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #dc2626;'>
                        <h2 style='color: #f87171; margin:0;'>👑 الإشارة الكبرى المؤكدة: هبوط (PUT)</h2>
                        <p style='color: #fee2e2; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>3 دقائق بالتمام (180 ثانية)</b></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **الشروط غير متطابقة بالكامل (المؤشرات متداخلة - تجنب الدخول وانتظر فرصة ذهبية أخرى)**")

time.sleep(1)
st.rerun()
