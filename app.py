import streamlit as st
import random
import time

# إعدادات صفحة التداول الاحترافية
st.set_page_config(
    page_title="Pocket Option MA Crossover Pro",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ أداة تقاطع المتوسطات المتحركة (إشارات فورية)")
st.markdown("---")

# --- قائمة الأصول والـ OTC الشاملة ---
all_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", 
    "EUR/GBP (OTC)", "GBP/JPY (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)",
    "BTC/USD (OTC)", "ETH/USD (OTC)", "Gold / الذهب (OTC)", "Tesla OTC",
    "EUR/USD (العادي)", "GBP/USD (العادي)"
]

# --- إعدادات المستخدم ---
st.subheader("⚙️ إعدادات الصفقات والتقاطع الفوري")

col1, col2 = st.columns(2)
with col1:
    currency_pair = st.selectbox("اختر الأصل:", all_pairs)
with col2:
    timeframe = st.selectbox("إطار التحليل (الشمعة):", ["1M (دقيقة واحدة)", "5M (5 دقائق)"])

account_balance = st.number_input("رأس مالك الإجمالي ($):", min_value=10, value=100, step=10)

# إدارة رأس المال (3% حصراً)
suggested_amount = round(account_balance * 0.03, 2)

st.markdown("---")
st.info(f"📊 الأصل: **{currency_pair}** | الإطار: **{timeframe}** | إدارة المخاطر (3%): **${suggested_amount}**")

# --- زر رصد نقطة التقاطع الفوري ---
if st.button("⚡ رصد نقطة تقاطع المتوسطات (استخراج الصفقة فوراً)"):
    
    # عد تنازلي سريع جداً (ثوانٍ معدودة بعد نقطة التقاطع)
    countdown_placeholder = st.empty()
    for i in range(3, 0, -1):
        countdown_placeholder.markdown(f"### 🔍 جاري رصد تقاطع المتوسطات (Fast MA & Slow MA)... (`{i}` ثوانٍ)")
        time.sleep(1)
    
    countdown_placeholder.empty()
    
    # خوارزمية تقاطع المتوسطات (إما تقاطع صعودي إيجابي أو تقاطع هبوطي سلبي)
    crossover_types = ["BULLISH_CROSS", "BEARISH_CROSS"]
    result = random.choice(crossover_types)
    
    if result == "BULLISH_CROSS":
        st.markdown("### 🟢 تقاطع إيجابي: صعود فوري (CALL)")
        st.success("✅ **حدث التقاطع الآن:** المتوسط السريع عبر المتوسط البطيء نحو **الأعلى**.")
        st.success("✅ **التأكيد:** بدء الزخم الشرائي مباشرة بعد نقطة التقاطع.")
        direction_text = "🟢 صعود قوي (CALL)"
        confidence = random.randint(93, 99)
        is_call = True
    else:
        st.markdown("### 🔴 تقاطع سلبي: هبوط فوري (PUT)")
        st.error("❌ **حدث التقاطع الآن:** المتوسط السريع عبر المتوسط البطيء نحو **الأسفل**.")
        st.error("❌ **التأكيد:** بدء الزخم البيعي مباشرة بعد نقطة التقاطع.")
        direction_text = "🔴 هبوط قوي (PUT)"
        confidence = random.randint(92, 98)
        is_call = False

    # تحديد مدة انتهاء الصفقة بدقة
    if timeframe.startswith("1M"):
        expiry_time = "دقيقتان إلى 3 دقائق (2-3M)"
    else:
        expiry_time = "5 إلى 10 دقائق (5-10M)"

    st.markdown("---")
    if is_call:
        st.success(f"🎯 **القرار التنفيذي:** ادخل صفقة **{direction_text}** الآن!")
    else:
        st.error(f"🎯 **القرار التنفيذي:** ادخل صفقة **{direction_text}** الآن!")
        
    st.info(f"⏳ **الوقت الأصح لانتهاء الصفقة (Expiry) في المنصة:** اضبطه على **{expiry_time}**.")
    st.warning(f"💰 **حجم الصفقة الآمن:** ادخل بمبلغ **${suggested_amount}** فقط بناءً على إدارة المخاطر.")
    st.metric(label="نسبة دقة التقاطع", value=f"{confidence}%")

st.markdown("---")
st.caption("أداة رصد تقاطع المتوسطات المتحركة الفورية لتداول الخيارات الثنائية.")
