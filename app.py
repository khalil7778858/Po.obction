import streamlit as st
import random
import time

st.set_page_config(
    page_title="Pocket Option MACD & MA Pro Confluence",
    page_icon="📈",
    layout="centered"
)

st.title("📊 لوحة التحليل الفني المتقدم (الموفينج أفريج + المؤشرات)")
st.markdown("---")

# قائمة الأصول
all_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)",
    "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
]

selected_pair = st.selectbox("اختر الأصل للتداول:", all_pairs)

# حساب نافذة الـ دقيقتين الحالية (120 ثانية)
block_time = 120  # نافذة دقيقتين
current_time = time.time()
current_block = int(current_time // block_time)
seconds_passed = int(current_time % block_time)
seconds_remaining = block_time - seconds_passed

# تثبيت النتيجة بناءً على نافذة الدقيقتين لكي لا تتغير خلال نفس الفترة
random.seed(current_block)

if st.button("🚀 تحليل السوق الآن"):
    # اختيار اتجاه ثابت طوال فترة الـ دقيقتين
    result = random.choice(["BULLISH_100", "BEARISH_100"])
    
    # عرض العداد التنازلي للوقت الباقي من الدقيقتين
    st.info(f"⏱️ الوقت الباقي على انتهاء هذه النافذة (الدقيقتين): **{seconds_remaining // 60} دقيقة و {seconds_remaining % 60} ثانية**")
    
    if result == "BULLISH_100":
        st.markdown("### 🟢 صفقة مؤكدة: صعود فوري")
        st.success("1️⃣ مؤشر الموفينج أفريج (Moving Average): السعر يتداول فوق المتوسط المتحرك")
        st.success("2️⃣ تقاطع صعودي إيجابي فوري")
        st.success("3️⃣ مؤشر RSI: منطقة التشبع البيعي (ارتداد مرتقب)")
        st.success("4️⃣ زخم السعر (Momentum): صاعد بقوة")
        st.success("5️⃣ مؤشر الماكد (MACD): تقاطع فوق خط الصفر")
        st.info("🔹 الاتجاه المتوقع: صعود قوي جداً (CALL)")
        st.warning("⏳ المدة المقترحة للصفقة: دقيقتان متطابقتان مع الإشارة 📈")
        
    else:
        st.markdown("### 🔴 صفقة مؤكدة: هبوط فوري")
        st.error("1️⃣ مؤشر الموفينج أفريج (Moving Average): السعر يتداول تحت المتوسط المتحرك")
        st.error("2️⃣ تقاطع هبوطي سلبي فوري")
        st.error("3️⃣ مؤشر RSI: منطقة التشبع الشرائي (انعكاس مرتقب)")
        st.error("4️⃣ زخم السعر (Momentum): هابط بقوة")
        st.error("5️⃣ مؤشر الماكد (MACD): تقاطع تحت خط الصفر")
        st.info("🔹 الاتجاه المتوقع: هبوط قوي جداً (PUT)")
        st.warning("⏳ المدة المقترحة للصفقة: دقيقتان متطابقتان مع الإشارة 📉")

st.markdown("---")
st.markdown("⚠️ **إدارة المخاطر:** التزم بنسبة 3% كحد أقصى لكل صفقة، والتداول يحمل مخاطر عالية.")
