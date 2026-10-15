import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="مستشار المؤشرات الأربعة - Pocket Option", page_icon="📊", layout="centered")

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

st.title("📊 مستشار المؤشرات الأربعة المتقدم")
st.caption("يعتمد كلياً على تحليل وتوافق المؤشرات الأربعة (RSI, MACD, Momentum, Moving Average) لإعطاء التوصية")

st.divider()

# المدخلات الأساسية
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
st.subheader("⚙️ ادخل قراءات المؤشرات الأربعة الحالية من شارت المنصة")

col1, col2 = st.columns(2)

with col1:
    rsi_val = st.slider("مؤشر القوة النسبية (RSI):", min_value=0, max_value=100, value=50)
    macd_status = st.selectbox("مؤشر MACD:", ["إيجابي (Bullish) 🟢", "سلبي (Bearish) 🔴"])

with col2:
    mom_status = st.selectbox("مؤشر الزخم (Momentum):", ["قوي صاعد 🚀", "قوي هابط 🔻", "متذبذب / محايد ⚖️"])
    ma_status = st.selectbox("المتوسط المتحرك (MA):", ["فوق المتوسط (اتجاه صاعد) 🟢", "تحت المتوسط (اتجاه هابط) 🔴"])

if st.button("🚀 تحليل المؤشرات وإعطاء القرار النهائي", use_container_width=True):
    # حساب إدارة المخاطر (3%)
    trade_amount = round(balance * 0.03, 2)
    
    # عد الإشارات الإيجابية والسلبية بناءً على اختيار المؤشرات
    bullish_count = 0
    bearish_count = 0

    # تقييم RSI
    if rsi_val > 53 and rsi_val < 75:
        bullish_count += 1
    elif rsi_val < 47 and rsi_val > 25:
        bearish_count += 1

    # تقييم MACD
    if "إيجابي" in macd_status:
        bullish_count += 1
    else:
        bearish_count += 1

    # تقييم Momentum
    if "صاعد" in mom_status:
        bullish_count += 1
    elif "هابط" in mom_status:
        bearish_count += 1

    # تقييم Moving Average
    if "صاعد" in ma_status:
        bullish_count += 1
    else:
        bearish_count += 1

    st.write("---")
    
    # اتخاذ القرار النهائي بناءً على تطابق المؤشرات
    if bullish_count >= 3 and rsi_val < 75:
        decision = "CALL (شراء / صعود) 🟢"
        bg_color = "#10b981"
        advice = "إجماع قوي من المؤشرات الأربعة على قوة الاتجاه الصاعد."
    elif bearish_count >= 3 and rsi_val > 25:
        decision = "PUT (بيع / هبوط) 🔻"
        bg_color = "#ef4444"
        advice = "إجماع قوي من المؤشرات الأربعة على قوة الاتجاه الهابط."
    else:
        decision = "انتظار (WAIT / لا توجد صفقة) ⚠️"
        bg_color = "#f59e0b"
        advice = "تضارب بين قراءات المؤشرات (لا توجد سيطرة واضحة). يُفضل الانتظار لحماية رأس المال."

    # عرض القرار النهائي
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 20px; border-radius: 12px; text-align: center; color: white; font-size: 24px; font-weight: bold;">
        القرار النهائي: {decision}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"💡 **تحليل الخبير:** {advice}")
    
    if "انتظار" not in decision:
        st.success(f"🎯 **التوصية:** تنفيذ صفقة على زوج **{selected_pair}**.\n\n💰 **حجم الصفقة المقترح (3%):** **${trade_amount}**")
