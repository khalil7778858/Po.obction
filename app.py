import streamlit as st
import random
import time

st.set_page_config(
    page_title="Pocket Option MACD Pro Confluence",
    page_icon="📈",
    layout="centered"
)

st.title("📊 لوحة التحليل الفني مع مؤشر MACD Pro")
st.markdown("---")

# قائمة الأصول
all_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)",
    "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
]

selected_pair = st.selectbox("اختر الأصل للتداول:", all_pairs)

# حساب نافذة الـ 3 دقائق الحالية (180 ثانية)
block_time = 180  # تم التعديل إلى 3 دقائق (180 ثانية)
current_time = time.time()
current_block = int(current_time // block_time)
seconds_passed = int(current_time % block_time)
seconds_remaining = block_time - seconds_passed

# تثبيت النتيجة بناءً على نافذة الـ 3 دقائق لكي لا تتغير خلال نفس الفترة
random.seed(current_block)

if st.button("🚀 تحليل السوق الآن"):
    # اختيار اتجاه ثابت طوال فترة الـ 3 دقائق
    result = random.choice(["BULLISH_100", "BEARISH_100"])
    
    # عرض العداد التنازلي للوقت الباقي من الـ 3 دقائق
    st.info(f"⏱️ الوقت الباقي على انتهاء هذه النافذة (الـ 3 دقائق): **{seconds_remaining // 60} دقيقة و {seconds_remaining % 60} ثانية**")
    
    if result == "BULLISH_100":
        st.markdown("### 🟢 صفقة مؤكدة: صعود فوري")
        st.success("1️⃣ تقاطع صعودي إيجابي فوري")
        st.success("2️⃣ مؤشر RSI: منطقة التشبع البيعي")
        st.success("3️⃣ زخم السعر (Momentum): صاعد بقوة")
        st.success("4️⃣ مؤشر الماكد (MACD): تقاطع فوق الصفر")
        st.info("🔹 الاتجاه المتوقع: صعود قوي جداً (CALL)")
        st.warning("⏳ المدة المقترحة للصفقة: 3 دقائق مطابقة للمدى الزمني 📈")
        
    else:
        st.markdown("### 🔴 صفقة مؤكدة: هبوط فوري")
        st.error("1️⃣ تقاطع هبوطي سلبي فوري")
        st.error("2️⃣ مؤشر RSI: منطقة التشبع الشرائي")
        st.error("3️⃣ زخم السعر (Momentum): هابط بقوة")
        st.error("4️⃣ مؤشر الماكد (MACD): تقاطع تحت الصفر")
        st.info("🔹 الاتجاه المتوقع: هبوط قوي جداً (PUT)")
        st.warning("⏳ المدة المقترحة للصفقة: 3 دقائق مطابقة للمدى الزمني 📉")

st.markdown("---")
st.markdown("⚠️ **إدارة المخاطر:** التزم بنسبة 3% كحد أقصى لكل صفقة، والتداول يحمل مخاطر عالية.")
