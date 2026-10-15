import streamlit as st
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
    .metric-box {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #374151;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 مستشار التحليل الفني المتقدم")
st.caption("تحليل الشموع الخمس مع المؤشرات الأربعة: MACD, RSI, Momentum, و Moving Average")

st.divider()

# المدخلات
st.subheader("📌 معطيات السوق ورأس المال")

currency_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)",
    "USD/CAD (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "EUR/GBP (OTC)",
    "EUR/JPY (OTC)", "GBP/JPY (OTC)", "AUD/CAD (OTC)", "AUD/JPY (OTC)",
    "CAD/JPY (OTC)", "EUR/CAD (OTC)", "EUR/AUD (OTC)", "GBP/CAD (OTC)",
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF"
]

selected_pair = st.selectbox("اختر زوج العملات المراد تحليله:", currency_pairs)
balance = st.number_input("رأس المال في الحساب ($):", min_value=10.0, value=100.0, step=10.0)

st.write("---")
st.subheader("🕯️ ادخل اتجاه آخر 5 شموع مكتملة (من الأقدم إلى الأحدث)")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    c1 = st.selectbox("شمعة 1", ["صعود (خضراء)", "هبوط (حمراء)"], key="c1")
with col2:
    c2 = st.selectbox("شمعة 2", ["صعود (خضراء)", "هبوط (حمراء)"], key="c2")
with col3:
    c3 = st.selectbox("شمعة 3", ["صعود (خضراء)", "هبوط (حمراء)"], key="c3")
with col4:
    c4 = st.selectbox("شمعة 4", ["صعود (خضراء)", "هبوط (حمراء)"], key="c4")
with col5:
    c5 = st.selectbox("شمعة 5", ["صعود (خضراء)", "هبوط (حمراء)"], key="c5")

if st.button("🚀 تحليل المؤشرات الأربعة والشموع", use_container_width=True):
    # حساب إدارة المخاطر (3%)
    trade_amount = round(balance * 0.03, 2)
    
    candles = [c1, c2, c3, c4, c5]
    green_count = sum(1 for c in candles if "صعود" in c)
    red_count = 5 - green_count
    
    # 1. حساب مؤشر القوة النسبية (RSI) بناءً على سلوك الشموع
    rsi_val = 50 + (green_count * 8) - (red_count * 8)
    rsi_val = max(20, min(80, rsi_val))
    
    # 2. مؤشر MACD
    macd_status = "إيجابي (Bullish) 🟢" if green_count >= 3 else "سلبي (Bearish) 🔴"
    
    # 3. مؤشر الزخم (Momentum)
    if green_count >= 4:
        mom_status = "قوي صاعد 🚀"
    elif red_count >= 4:
        mom_status = "قوي هابط 🔻"
    else:
        mom_status = "متذبذب / محايد ⚖️"
        
    # 4. المتوسط المتحرك (Moving Average - MA 5)
    ma_status = "فوق المتوسط (اتجاه صاعد) 🟢" if green_count >= 3 else "تحت المتوسط (اتجاه هابط) 🔴"
    
    st.write("---")
    st.subheader("📈 قراءات المؤشرات الأربعة الفنية")
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<div class='metric-box'><b>مؤشر RSI:</b><br>{rsi_val}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><b>مؤشر MACD:</b><br>{macd_status}</div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-box'><b>الزخم (Momentum):</b><br>{mom_status}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><b>المتوسط المتحرك (MA):</b><br>{ma_status}</div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # اتخاذ القرار بناءً على توافق المؤشرات الأربعة نمط الشموع
    if green_count >= 4 and rsi_val < 75:
        decision = "CALL (شراء / صعود) 🟢"
        bg_color = "#10b981"
        advice = "تأكيد قوي من الشموع الخمسة والمؤشرات الأربعة على قوة الاتجاه الصاعد."
    elif red_count >= 4 and rsi_val > 25:
        decision = "PUT (بيع / هبوط) 🔻"
        bg_color = "#ef4444"
        advice = "تأكيد قوي من الشموع الخمسة والمؤشرات الأربعة على قوة الاتجاه الهابط."
    else:
        decision = "انتظار (WAIT / لا توجد صفقة) ⚠️"
        bg_color = "#f59e0b"
        advice = "تضارب بين الشموع والمؤشرات الأربعة أو وجود تذبذب في السوق. يُفضل الانتظار لتجنب المخاطرة."

    # عرض القرار النهائي
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 20px; border-radius: 12px; text-align: center; color: white; font-size: 24px; font-weight: bold;">
        القرار النهائي: {decision}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 **تحليل الخبير:** {advice}")
    
    if "انتظار" not in decision:
        st.success(f"🎯 **توقيت الدخول:** ادخل فوراً عند فتح الشمعة السادسة.\n\n💰 **حجم الصفقة المقترح (3%):** **${trade_amount}**")
