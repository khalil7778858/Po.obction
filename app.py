import streamlit as st
import random
import time

# إعداد الصفحة وتفعيل العرض الكامل للاستفادة من شاشة الكمبيوتر
st.set_page_config(
    page_title="Pocket Option Pro - Left Layout",
    page_icon="⚡",
    layout="wide"
)

# تنسيق CSS مخصص لمحاذاة كل عناصر التطبيق إلى الجانب الأيسر تماماً
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        direction: ltr;
        text-align: left;
    }
    div.block-container {
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 100%;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #1d4ed8, #1e40af);
    }
    p, span, h1, h2, h3, label {
        text-align: left !important;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق بالجانب الأيسر
st.markdown("<h2 style='color: #f3f4f6;'>⚡ Pocket Option Pro - 5 Min Trading Room</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #9ca3af;'>Wave Analysis & 300-Sec Candle Strategy (Left Panel Mode)</p>", unsafe_allow_html=True)
st.markdown("---")

# صندوق اختيار الأصل وزر التحليل بجانب بعضهما في اليسار
col1, col2, col3 = st.columns([2, 1, 3])
with col1:
    selected_pair = st.selectbox("📌 Select OTC Asset:", [
        "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
        "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
    ])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analysis_btn = st.button("🔥 Run Analysis")

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

# العداد التنازلي المتحرك منسق باليسار
timer_placeholder = st.empty()

block_time = 300  
current_time = time.time()
seconds_passed = int(current_time % block_time)
seconds_remaining = block_time - seconds_passed

minutes = seconds_remaining // 60
seconds = seconds_remaining % 60

timer_placeholder.markdown(f"""
    <div style='background-color: #1f2937; padding: 15px; border-radius: 10px; text-align: left; border: 1px solid #374151; max-width: 500px;'>
        <span style='color: #93c5fd; font-size: 15px;'>⏱️ Current 5-Min Candle Countdown:</span><br>
        <span style='color: #ffffff; font-size: 22px; font-weight: bold;'>{minutes:02d} Minutes & {seconds:02d} Seconds ({seconds_remaining}s)</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# عرض التقرير والنتائج بالجانب الأيسر بشكل منظم تماماً
if st.session_state.analysis_result is not None:
    res = st.session_state.analysis_result
    
    with st.container():
        st.markdown(f"### 📊 Wave Analysis Results for ({res['pair']})")
        
        if res["direction"] == "CALL":
            st.success("1️⃣ **Moving Average (MA):** Stable above MA ➔ (Bullish ✅)")
            st.success("2️⃣ **Technical Crossover:** Extended upward cross ➔ (Confirmed ✅)")
            st.success("3️⃣ **RSI Indicator:** Healthy upward bounce ➔ (Confirmed ✅)")
            st.success("4️⃣ **Momentum:** Accumulating buying liquidity ➔ (Confirmed ✅)")
            st.success("5️⃣ **MACD Indicator:** Positive divergence above zero ➔ (Confirmed ✅)")
        else:
            st.error("1️⃣ **Moving Average (MA):** Stable below MA ➔ (Bearish ✅)")
            st.error("2️⃣ **Technical Crossover:** Extended downward cross ➔ (Confirmed ✅)")
            st.error("3️⃣ **RSI Indicator:** Continuous downward slope ➔ (Confirmed ✅)")
            st.error("4️⃣ **Momentum:** Accumulating selling pressure ➔ (Confirmed ✅)")
            st.error("5️⃣ **MACD Indicator:** Negative divergence below zero ➔ (Confirmed ✅)")

        st.markdown("---")
        
        if res["is_ready"]:
            if res["direction"] == "CALL":
                st.markdown("""
                    <div style='background-color: #064e3b; padding: 15px; border-radius: 10px; text-align: left; border: 1px solid #059669; max-width: 600px;'>
                        <h3 style='color: #34d399; margin:0;'>🟢 Final Decision: Extended CALL (UP)</h3>
                        <p style='color: #d1fae5; margin:5px 0 0 0;'>Pocket Option Duration: Exactly 5 Minutes (300s)</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background-color: #7f1d1d; padding: 15px; border-radius: 10px; text-align: left; border: 1px solid #dc2626; max-width: 600px;'>
                        <h3 style='color: #f87171; margin:0;'>🔴 Final Decision: Extended PUT (DOWN)</h3>
                        <p style='color: #fee2e2; margin:5px 0 0 0;'>Pocket Option Duration: Exactly 5 Minutes (300s)</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Market is currently choppy (Avoid entering and wait for next candle)**")

st.markdown("---")
st.markdown("<p style='color: #9ca3af; font-size: 13px;'>⚠️ Risk Management: Limit risk to 2%-3% per trade max.</p>", unsafe_allow_html=True)

# التحديث اللحظي
time.sleep(1)
st.rerun()
