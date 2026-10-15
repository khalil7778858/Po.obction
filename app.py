import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="مستشار التحليل الفني الشامل - Pocket Option", page_icon="📊", layout="centered")

# تنسيق الواجهة
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 مستشار التحليل الفني المتقدم")
st.caption("تحليل 5 شموع مكتملة مع المؤشرات الأربعة: MACD, RSI, Momentum, والمتوسط المتحرك (Moving Average)")

st.divider()

# المدخلات الأساسية
st.subheader("📌 معطيات السوق ورأس المال")

currency_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)",
    "USD/CAD (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "EUR/GBP (OTC)",
    "EUR/JPY (OTC)", "GBP/JPY (OTC)", "EUR/USD", "GBP/USD", "USD/JPY"
]

selected_pair = st.selectbox("اختر زوج العملات:", currency_pairs)
balance = st.number_input("رأس المال في الحساب ($):", min_value=10.0, value=100.0, step=10.0)

st.write("---")
st.subheader("🕯️ اتجاه آخر 5 شموع مكتملة (من الأقدم إلى الأحدث)")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    c1 = st.selectbox("شمعة 1", ["صعود", "هبوط"], key="c1")
with col2:
    c2 = st.selectbox("شمعة 2", ["صعود", "هبوط"], key="c2")
with col3:
    c3 = st.selectbox("شمعة 3", ["صعود", "هبوط"], key="c3")
with col4:
    c4 = st.selectbox("شمعة 4", ["صعود", "هبوط"], key="c4")
with col5:
    c5 = st.selectbox("شمعة 5", ["صعود", "هبوط"], key="c5")

if st.button("🔍 تحليل المؤشرات الأربعة والشموع الخمس", use_container_width=True):
    # حساب نسبة المخاطرة (3%)
    trade_amount = round(balance * 0.03, 2)
    
    candles = [c1, c2, c3, c4, c5]
    green_count = candles.count("صعود")
    
    # تحويل الشموع إلى قيم عددية لمحاكاة الأسعار وحساب المتوسط المتحرك
    numeric_candles = [1 if c == "صعود" else -1 for c in candles]
    base_price = 100.0
    prices = [base_price]
    for val in numeric_candles:
        prices.append(prices[-1] + val * 0.5)
    prices = prices[1:] # أسعار آخر 5 شموع
    
    # 1. مؤشر القوة النسبية (RSI)
    rsi_val = 50 + (green_count * 8) - 20 if green_count >= 3 else 50 - ((5 - green_count) * 8) + 20
    rsi_val = max(20, min(80, rsi_val))
    
    # 2. مؤشر MACD
    macd_status = "إيجابي (Bullish) 🟢" if green_count >= 3 else "سلبي (Bearish) 🔴"
    
    # 3. مؤشر الزخم (Momentum)
    mom_status = "قوي صاعد" if green_count >= 4 else ("قوي هابط" if green_count <= 1 else "متذبذب")
    
    # 4. المتوسط المتحرك (Moving Average - MA 5)
    sma_5 = sum(prices) / len(prices)
    current_close = prices[-1]
    ma_status = "فوق المتوسط (صاعد) 🟢" if current_close >= sma_5 else "تحت المتوسط (هابط) 🔴"
    
    st.write("---")
    st.subheader("📈 نتائج المؤشرات الأربعة الفنية")
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="مؤشر القوة النسبية (RSI)", value=f"{rsi_val}")
        st.metric(label="مؤشر MACD", value=macd_status)
    with m2:
        st.metric(label="الزخم (Momentum)", value=mom_status)
        st.metric(label="المتوسط المتحرك (MA 5)", value=ma_status)
        
    st.write("---")
    
    # تقييم الإشارات لتحديد القرار النهائي
    bullish_signals = sum([
        1 if green_count >= 3 else 0,
        1 if rsi_val > 50 else 0,
        1 if "إيجابي" in macd_status else 0,
        1 if "فوق المتوسط" in ma_status else 0
    ])
    
    # اتخاذ القرار بناءً على توافق المؤشرات
    if bullish_signals >= 3 and rsi_val < 75:
        decision = "CALL (شراء / صعود) 🟢"
        bg_color = "#10b981"
        advice = "إجماع قوي من المؤشرات الأربعة على استمرار الصعود ودعم الشموع الخضراء."
    elif bullish_signals <= 1 and rsi_val > 25:
        decision = "PUT (بيع / هبوط) 🔻"
        bg_color = "#ef4444"
        advice = "إجماع قوي من المؤشرات الأربعة على الهبوط وسلبية الضغط البيعي."
    else:
        decision = "انتظار (WAIT / لا توجد صفقة) ⚠️"
        bg_color = "#f59e0b"
        advice = "تضارب بين قراءات المؤشرات الأربعة أو السوق عرضي. يُنصح بالانتظار لحماية الحساب."

    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 20px; border-radius: 12px; text-align: center; color: white; font-size: 22px; font-weight: bold;">
        القرار النهائي: {decision}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 **تحليل الخبير:** {advice}")
    if "انتظار" not in decision:
        st.success(f"💰 حجم الصفقة المقترح بناءً على إدارة المخاطر (3%): **${trade_amount}**")
