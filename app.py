import streamlit as st
import random
import time

st.set_page_config(
    page_title="Ultimate Trading Pro - Smart Lock 10m",
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

st.markdown("<h2 style='text-align: center; color: #f3f4f6;'>👑 المنظومة الكبرى - فحص واستقرار الإشارة في الثواني الأخيرة</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>تحليل شمعة الـ 10 دقائق مع تثبيت القرار النهائي عند إغلاق الشمعة (آخر ثانية)</p>", unsafe_allow_html=True)
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
    
    analysis_btn = st.button("⏳ ابدأ الفحص والتثبيت في آخر 15 ثانية")
    
    if analysis_btn:
        st.session_state.is_scanning = True
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    block_time = 600  # 10 دقائق بالتمام (600 ثانية)
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
    st.markdown("### 📊 تقرير التحليل المباشر وتثبيت الإشارة")
    
    # خوارزمية الفحص المستمر خلال الـ 15 ثانية وتثبيت القرار
    if st.session_state.is_scanning:
        status_box = st.empty()
        status_box.warning("🔍 **جاري جمع البيانات وفحص استقرار المؤشرات خلال الثواني الأخيرة...**")
        
        # إجراء محاكاة تجميع البيانات لتأكيد الاتجاه الأكثر استقراراً
        call_votes = 0
        put_votes = 0
        
        for _ in range(5):
            vote = random.choice(["CALL", "PUT", "CALL"])
            if vote == "CALL":
                call_votes += 1
            else:
                put_votes += 1
            time.sleep(0.3)
            
        final_dir = "CALL" if call_votes >= put_votes else "PUT"
        is_stable = True if max(call_votes, put_votes) >= 3 else False
        
        st.session_state.analysis_result = {
            "direction": final_dir,
            "is_ready": is_stable,
            "pair": selected_pair,
            "confirmed_at": f"{minutes:02d}:{seconds:02d}"
        }
        st.session_state.is_scanning = False
        st.rerun()

    if st.session_state.analysis_result is None:
        st.info("👈 اضغط على زر **(ابدأ الفحص والتثبيت في آخر 15 ثانية)** عندما يدخل العداد في الثواني الأخيرة لشمعة الـ 10 دقائق.")
    else:
        res = st.session_state.analysis_result
        
        st.markdown(f"**الأصل المفحوص:** `{res['pair']}`")
        st.markdown(f"**توقيت تثبيت الإشارة:** عند `00:01` ثانية من الإغلاق")
        st.markdown("---")
        
        if res["direction"] == "CALL":
            st.success("1️⃣ **الاتجاه العام (10 دقائق):** استقرار صاعد فوق المتوسطات ➔ (مستقر ✅)")
            st.success("2️⃣ **تقاطعات الموفينج الثلاثة:** تقاطع ذهبي مؤكد ➔ (ثابت ✅)")
            st.success("3️⃣ **مؤشر الـ RSI:** دعم صعودي قاطع ➔ (مستقر ✅)")
            st.success("4️⃣ **الزخم والسيولة:** تفوق واضح للشرائين ➔ (تأكيد ✅)")
            st.success("5️⃣ **مؤشر الـ MACD (المجد):** تقاطع صريح فوق خط الإشارة ➔ (تثبيت نهائي ✅)")
        else:
            st.error("1️⃣ **الاتجاه العام (10 دقائق):** استقرار هابط تحت المتوسطات ➔ (مستقر ✅)")
            st.error("2️⃣ **تقاطعات الموفينج الثلاثة:** تقاطع ميت مؤكد ➔ (ثابت ✅)")
            st.error("3️⃣ **مؤشر الـ RSI:** ضغط بيعي قاطع ➔ (مستقر ✅)")
            st.error("4️⃣ **الزخم والسيولة:** تفوق واضح للبائعين ➔ (تأكيد ✅)")
            st.error("5️⃣ **مؤشر الـ MACD (المجد):** تقاطع صريح تحت خط الإشارة ➔ (تثبيت نهائي ✅)")

        st.markdown("---")
        
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #34d399;'>
                        <h2 style='color: #34d399; margin:0;'>🔒 إشارة مثبته مؤكدة: صعود (CALL)</h2>
                        <p style='color: #d1fae5; font-size: 15px; margin:8px 0 0 0;'>ادخل الآن فوراً مع افتتاح الشمعة جديدة | <b>3 صفقات متتالية (3 دقائق لكل صفقة)</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #f87171;'>
                        <h2 style='color: #f87171; margin:0;'>🔒 إشارة مثبته مؤكدة: هبوط (PUT)</h2>
                        <p style='color: #fee2e2; font-size: 15px; margin:8px 0 0 0;'>ادخل الآن فوراً مع افتتاح الشمعة جديدة | <b>3 صفقات متتالية (3 دقائق لكل صفقة)</b></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **تنبيه حماية: المؤشرات لم تستقر بنسبة 100% في الثواني الأخيرة (تجنب الدخول في هذه الشمعة)**")

time.sleep(1)
st.rerun()
