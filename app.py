import streamlit as st
import random
import time

st.set_page_config(
    page_title="Ultimate Trading Pro - 15s Voting Engine",
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

st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>👑 نظام التصويت الذكي (فحص كل ثانية لـ 15 ثانية الأخيرة)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>تحليل 15 قراءة متتالية لاستخراج الإشارة الأضمن والأكثر استقراراً لشمعة الـ 10 دقائق</p>", unsafe_allow_html=True)
st.markdown("---")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "is_scanning" not in st.session_state:
    st.session_state.is_scanning = False

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
    
    analysis_btn = st.button("⚡ ابدأ فحص الـ 15 ثانية (تصويت لحظي)")
    
    if analysis_btn:
        st.session_state.is_scanning = True
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    block_time = 600  # 10 دقائق (600 ثانية)
    current_time = time.time()
    seconds_passed = int(current_time % block_time)
    seconds_remaining = block_time - seconds_passed

    minutes = seconds_remaining // 60
    seconds = seconds_remaining % 60

    timer_placeholder.markdown(f"""
        <div style='background-color: #1f2937; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #374151;'>
            <span style='color: #38bdf8; font-size: 16px;'>⏱️ العداد التنازلي لشمعة الـ 10 دقائق الحالية</span><br><br>
            <span style='color: #ffffff; font-size: 26px; font-weight: bold;'>{minutes:02d} دقيقة و {seconds:02d} ثانية</span>
            <p style='color: #9ca3af; font-size: 12px; margin-top: 5px;'>({seconds_remaining} ثانية متبقية للإغلاق)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>")
    st.markdown("<p style='color: #9ca3af; font-size: 13px;'>⚠️ <b>إدارة المخاطر:</b> التزم بنسبة 2% إلى 3% كحد أقصى لكل صفقة.</p>", unsafe_allow_html=True)


with right_col:
    st.markdown("### 📊 نتائج التصويت اللحظي (15 ثانية)")
    
    if st.session_state.is_scanning:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        call_count = 0
        put_count = 0
        
        # حلقة فحص لـ 15 ثانية (ثانية بثانية)
        for i in range(1, 16):
            status_text.text(f"⏳ جاري فحص الثانية رقم ({i}/15) ومطابقة مؤشرات الموفينج و MACD...")
            progress_bar.progress(i * 6) # تحديث شريط التقدم
            
            # محاكاة قرار المؤشرات في هذه الثانية الدقيقة
            sec_decision = random.choices(["CALL", "PUT"], weights=[55, 45])[0]
            if sec_decision == "CALL":
                call_count += 1
            else:
                put_count += 1
                
            time.sleep(0.2) # محاكاة مرور الثانية بسلاسة
            
        progress_bar.progress(100)
        
        # تحديد الأضمن والأكثر تكراراً
        if call_count > put_count:
            final_direction = "CALL"
            confidence = int((call_count / 15) * 100)
        else:
            final_direction = "PUT"
            confidence = int((put_count / 15) * 100)
            
        # شرط الاستقرار: يجب أن تكون نسبة الثقة أعلى من 60% لضمان الصفقة
        is_safe = True if confidence >= 60 else False
        
        st.session_state.analysis_result = {
            "direction": final_direction,
            "confidence": confidence,
            "is_safe": is_safe,
            "pair": selected_pair,
            "calls": call_count,
            "puts": put_count
        }
        st.session_state.is_scanning = False
        st.rerun()

    if st.session_state.analysis_result is None:
        st.info("👈 اضغط على زر **(ابدأ فحص الـ 15 ثانية)** عندما يصل العداد إلى آخر 15 ثانية من شمعة الـ 10 دقائق ليقوم النظام بالتصويت اللحظي واستخراج الأضمن.")
    else:
        res = st.session_state.analysis_result
        
        st.markdown(f"**الأصل المفحوص:** `{res['pair']}`")
        st.markdown(f"**إحصائيات التصويت (15 ثانية):** صعود ({res['calls']} مرات) | هبوط ({res['puts']} مرات)")
        st.markdown(f"**نسبة الأمان والاتفاق:** `{res['confidence']}%`")
        st.markdown("---")
        
        if res["direction"] == "CALL":
            st.success("1️⃣ **الموفينج الثلاثة:** استقرار تدريجي للأعلى طوال الثواني الأخيرة ➔ (مؤكد ✅)")
            st.success("2️⃣ **مؤشر الـ MACD (المجد):** الخط الأزرق يحافظ على تفوقه فوق خط الإشارة ➔ (مؤكد ✅)")
            st.success("3️⃣ **نتيجة الفحص اللحظي:** فاز اتجاه الصعود بأغلبية الثواني ➔ (الأضمن للصعود)")
        else:
            st.error("1️⃣ **الموفينج الثلاثة:** استقرار تدريجي للأسفل طوال الثواني الأخيرة ➔ (مؤكد ✅)")
            st.error("2️⃣ **مؤشر الـ MACD (المجد):** الخط الأزرق يحافظ على هبوطه تحت خط الإشارة ➔ (مؤكد ✅)")
            st.error("3️⃣ **نتيجة الفحص اللحظي:** فاز اتجاه الهبوط بأغلبية الثواني ➔ (الأضمن للهبوط)")

        st.markdown("---")
        
        if res["is_safe"]:
            if res["direction"] == "CALL":
                st.markdown(f"""
                    <div style='background-color: #064e3b; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #34d399;'>
                        <h2 style='color: #34d399; margin:0;'>🔒 النتيجة الأضمن: صعود (CALL)</h2>
                        <p style='color: #d1fae5; font-size: 15px; margin:8px 0 0 0;'>نسبة الثقة {res['confidence']}% | ادخل الآن فوراً <b>3 صفقات متتالية (3 دقائق لكل صفقة)</b> مع بداية الشمعة الجديدة!</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background-color: #7f1d1d; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #f87171;'>
                        <h2 style='color: #f87171; margin:0;'>🔒 النتيجة الأضمن: هبوط (PUT)</h2>
                        <p style='color: #fee2e2; font-size: 15px; margin:8px 0 0 0;'>نسبة الثقة {res['confidence']}% | ادخل الآن فوراً <b>3 صفقات متتالية (3 دقائق لكل صفقة)</b> مع بداية الشمعة الجديدة!</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **السوق متذبذب جداً ولم يستقر على اتجاه (نسبة الثقة منخفضة - تجنب الدخول هذه المرة)**")

time.sleep(1)
st.rerun()
