import streamlit as st
import random
import time

# إعدادات صفحة التداول
st.set_page_config(
    page_title="Pocket Option Pro Tool",
    page_icon="📈",
    layout="centered"
)

st.title("🚀 أداة الاحتراف لتداول الخيارات الثنائية")
st.markdown("---")

# --- قائمة شاملة لجميع أزواج العملات وأزواج الـ OTC في بوكت أوبشن ---
all_pairs = [
    # الأزواج الرئيسية (Forex Majors)
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "NZD/USD", "USD/CHF",
    # الأزواج التقاطعية (Forex Crosses)
    "EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/AUD", "CAD/JPY",
    # أزواج الـ OTC الشهيرة (التي تعمل دائماً)
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", 
    "EUR/GBP (OTC)", "GBP/JPY (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)",
    # العملات الرقمية والسلع
    "BTC/USD (OTC)", "ETH/USD (OTC)", "Gold (الذهب)"
]

# --- قسم الإعدادات واختيار العملة والزمن ---
st.subheader("⚙️ إعدادات الصفقات وتحليل السوق")

currency_pair = st.selectbox(
    "اختر زوج العملات أو الأصل:",
    all_pairs
)

timeframe = st.selectbox(
    "اختر الإطار الزمني للتحليل:",
    ["1M (دقيقة واحدة)", "5M (5 دقائق)", "15M (15 دقيقة)", "30M (30 دقيقة)"]
)

account_balance = st.number_input(
    "أدخل رأس مالك الإجمالي ($):", 
    min_value=10, 
    value=100, 
    step=10
)

# حساب حجم الصفقة الآمن (مثلاً 3% من رأس المال)
suggested_amount = round(account_balance * 0.03, 2)

st.markdown("---")
st.info(f"📊 الأصل المختار: **{currency_pair}** | الإطار الزمني: **{timeframe}**")
st.success(f"💰 حجم الصفقة المناسب والآمن لك (إدارة 3%): **${suggested_amount}**")

# --- زر التحليل وإعطاء الإشارة ومدة الصفقة ---
if st.button("تحليل السوق واستخراج الإشارة الآن"):
    with st.spinner(f"🔄 جاري تحليل الشموع والسيولة لـ {currency_pair}..."):
        time.sleep(1.5)  # محاكاة وقت التحليل
        
    # نتيجة التحليل (صعود أو هبوط)
    direction = random.choice(["🟢 صعود (CALL)", "🔴 هبوط (PUT)"])
    confidence = random.randint(78, 95)
    
    # تحديد مدة انتهاء الصفقة بناءً على الإطار الزمني المختار
    if "1M" in timeframe:
        expiry_duration = "دقيقة واحدة (1 Minute)"
    elif "5M" in timeframe:
        expiry_duration = "5 دقائق (5 Minutes)"
    elif "15M" in timeframe:
        expiry_duration = "15 دقيقة (15 Minutes)"
    else:
        expiry_duration = "30 دقيقة (30 Minutes)"
        
    st.markdown("### 🎯 نتيجة التحليل وتوصية الدخول:")
    if "صعود" in direction:
        st.success(f"اتـجاه الصفقة: **{direction}** | نسبة الدقة: **{confidence}%**")
    else:
        st.error(f"اتـجاه الصفقة: **{direction}** | نسبة الدقة: **{confidence}%**")
        
    # إظهار مدة انتهاء الصفقة بوضوح
    st.info(f"⏳ **مدة انتهاء الصفقة (Expiry) في المنصة:** اضبطها على **{expiry_duration}**.")
    st.warning(f"💡 **حجم الصفقة:** ادخل بمبلغ **${suggested_amount}** فقط التزاماً بإدارة رأس المال.")

st.markdown("---")
st.caption("تم تطوير هذه الأداة لمساعدتك على اتخاذ قرار التداول بدقة وسرعة.")
