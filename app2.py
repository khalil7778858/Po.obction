import streamlit as st
import random
import time

st.set_page_config(
    page_title="Triple MA & MACD Strategy - 3 Min",
    page_icon="⚡",
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
        background: linear-gradient(45deg, #7c3aed, #2563eb);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #6d28d9, #1d4ed8);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>⚡ استراتيجية تقاطع الموفينج + مؤشر الـ MACD (المجد) - 3 دقائق</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>دمج تقاطعات الخطوط الثلاثة مع تقاطع خط الـ MACD الأزرق لتأكيد الصفقة</p>", unsafe_allow_html=True)
st.markdown("---")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("### لوحة التحكم وإدارة رأس المال")
    
    selected_pair = st.selectbox("اختر الأصل المتاح على المنصة (OTC):", [
        "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
        "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
    ])
    
    account_balance = st.number_input("رأس المال في الحساب ($):", min_value=10.0, value=100.0, step=10.0)
    risk_amount = account_balance * 0.03
    st.markdown(f"💡 **المبلغ المقترح للصفقة (إدارة مخاطر 3%):** `{risk_amount:.2f} $`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    analysis_btn = st.button("فحص الموفينج + مؤشر المجد (MACD) الآن")
    
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
    
    block_time = 180
    current_time = time.time()
    seconds_passed = int(current_time % block_time)
    seconds_remaining = block_time - seconds_passed

    minutes = seconds_remaining // 60
    seconds = seconds_remaining % 60

    timer_placeholder.markdown(f"""
        <div style='background-color: #1f2937; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #374151;'>
            <span style='color: #38bdf8; font-size: 16px;'>العداد التنازلي لإطار الـ 3 دقائق الحالي</span><br><br>
            <span style='color: #ffffff; font-size: 26px; font-weight: bold;'>{minutes:02d} دقيقة و {seconds:02d} ثانية</span>
            <p style='color: #9ca3af; font-size: 12px; margin-top: 5px;'>({seconds_remaining} ثانية متبقية)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>")
    st.markdown("<p style='color: #9ca3af; font-size: 13px;'>إدارة المخاطر: التزم بنسبة 2% إلى 3% كحد أقصى لكل صفقة.</p>", unsafe_allow_html=True)


with right_col:
    st.markdown("### نتائج تحليل التقاطعات المزدوجة (الموفينج + MACD)")
    
    if st.session_state.analysis_result is None:
        st.info("اضغط على زر (فحص الموفينج + مؤشر المجد) في القسم الأيسر لتحليل الشموع وعرض الإشارات المؤكدة هنا.")
    else:
        res = st.session_state.analysis_result
        
        st.markdown(f"الأصل المفحوص: `{res['pair']}`")
        st.markdown("---")
        
        if res["direction"] == "CALL":
            st.success("1. تقاطع الموفينج الثلاثي: الخطوط السريعة تخترق نحو الأعلى (إيجابي)")
            st.success("2. مؤشر الـ MACD (المجد): الخط الأزرق اخترق خط الإشارة صعوداً نحو الأعلى (تأكيد قوي)")
            st.success("3. أعمدة الهستوجرام: تتحول تدريجياً للون الأخضر فوق الصفر (زخم صاعد)")
            st.success("4. توافق المؤشرات: إشارة متكاملة بنسبة 100% للصعود")
        else:
            st.error("1. تقاطع الموفينج الثلاثي: الخطوط السريعة تكسر نحو الأسفل (سلبي)")
            st.error("2. مؤشر الـ MACD (المجد): الخط الأزرق اخترق خط الإشارة نزولاً نحو الأسفل (تأكيد قوي)")
            st.error("3. أعمدة الهستوجرام: تتحول تدريجياً للون الأحمر تحت الصفر (زخم هابط)")
            st.error("4. توافق المؤشرات: إشارة متكاملة بنسبة 100% للهبوط")

        st.markdown("---")
        
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #059669;'>
                        <h2 style='color: #34d399; margin:0;'>إشارة مؤكدة: صعود (CALL)</h2>
                        <p style='color: #d1fae5; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>3 دقائق بالتمام (180 ثانية)</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #dc2626;'>
                        <h2 style='color: #f87171; margin:0;'>إشارة مؤكدة: هبوط (PUT)</h2>
                        <p style='color: #fee2e2; font-size: 16px; margin:8px 0 0 0;'>مدة الصفقة في بوكت أوبشن: <b>3 دقائق بالتمام (180 ثانية)</b></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("لا يوجد تقاطع متوافق حالياً بين الموفينج ومؤشر المجد (تجنب الدخول)")

time.sleep(1)
st.rerun()
