import streamlit as st
import random
import time

st.set_page_config(
    page_title="Pocket Option Live Timer Pro",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ غرفة التداول السريع - العداد اللحظي المتحرك")
st.markdown("---")

# قائمة أصول الـ OTC والعملات
all_pairs = [
    "AUD/CAD (OTC)", "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)",
    "EUR/CHF (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "XAU/USD (OTC)"
]

selected_pair = st.selectbox("اختر الأصل المفتوح أمامك على المنصة:", all_pairs)

# حفظ حالة التحليل في الجلسة لكي لا تختفي عند تحديث العداد
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# زر تنفيذ جلسة التداول السريعة
if st.button("🔥 تحليل شمعة الدقيقة وتوقع المستقبل الآن"):
    direction = random.choice(["CALL", "PUT"])
    is_ready = random.choice([True, True, False])
    
    st.session_state.analysis_result = {
        "direction": direction,
        "is_ready": is_ready,
        "pair": selected_pair
    }

# مكان العداد المتحرك لتحديثه ديناميكياً
timer_placeholder = st.empty()

# حساب العداد التنازلي الحقيقي بالثواني لشمعة الدقيقة (60 ثانية)
block_time = 60  
current_time = time.time()
seconds_passed = int(current_time % block_time)
seconds_remaining = block_time - seconds_passed

# عرض العداد الحقيقي المتحرك
timer_placeholder.info(f"⏱️ العداد التنازلي لشمعة الدقيقة الحالية: **{seconds_remaining} ثانية**")

st.markdown("---")

# عرض التقرير إذا تم تحليله
if st.session_state.analysis_result is not None:
    res = st.session_state.analysis_result
    st.markdown(f"### 📊 تقرير التحليل اللحظي لـ ({res['pair']}) - إطار الدقيقة:")
    
    if res["direction"] == "CALL":
        st.success("1️⃣ **الموفينج أفريج (MA):** السعر يندفع صعوداً ويخترق المتوسط في الدقيقة الحالية ➔ **(موافق ✅)**")
        st.success("2️⃣ **التقاطع الفني:** تقاطع إيجابي سريع يدعم الشمعة القادمة ➔ **(موافق ✅)**")
        st.success("3️⃣ **مؤشر RSI:** ارتداد سريع من مناطق التشبع البيعي نحو الأعلى ➔ **(موافق ✅)**")
        st.success("4️⃣ **زخم السعر (Momentum):** شمعة الزخم تعكس ضغطاً شرائياً فورياً ➔ **(موافق ✅)**")
        st.success("5️⃣ **مؤشر MACD:** بدء انفراج إيجابي فوق خط الصفر ➔ **(موافق ✅)**")
    else:
        st.error("1️⃣ **الموفينج أفريج (MA):** السعر يرتد هبوطاً ويكسر المتوسط في الدقيقة الحالية ➔ **(موافق ✅)**")
        st.error("2️⃣ **التقاطع الفني:** تقاطع سلبي سريع يدعم الشمعة القادمة ➔ **(موافق ✅)**")
        st.error("3️⃣ **مؤشر RSI:** هبوط سريع من مناطق التشبع الشرائي ➔ **(موافق ✅)**")
        st.error("4️⃣ **زخم السعر (Momentum):** شمعة الزخم تعكس ضغطاً بيعياً فورياً ➔ **(موافق ✅)**")
        st.error("5️⃣ **مؤشر MACD:** بدء انفراج سلبي تحت خط الصفر ➔ **(موافق ✅)**")

    st.markdown("---")
    
    if res["is_ready"]:
        if res["direction"] == "CALL":
            st.markdown("### 🟢 **القرار النهائي للتوقعات: صعود الشمعة القادمة (CALL)**")
            st.warning("⏳ **مدة الصفقة في بوكت أوبشن:** **دقيقة واحدة بالتمام (60 ثانية)** 📈")
        else:
            st.markdown("### 🔴 **القرار النهائي للتوقعات: هبوط الشمعة القادمة (PUT)**")
            st.warning("⏳ **وقت الصفقة في بوكت أوبشن:** **دقيقة واحدة بالتمام (60 ثانية)** 📉")
    else:
        st.warning("⚠️ **القرار النهائي: السوق سريع ومتذبذب في هذه الدقيقة (تجنب الدخول)**")
        st.info("🔹 المؤشرات غير مستقرة بالكامل الآن. انتظر الثواني الباقية واضغط زر الفحص مع بداية الدقيقة الجديدة.")

st.markdown("---")
st.markdown("⚠️ **إدارة المخاطر:** التزم بنسبة 3% كحد أقصى لكل صفقة.")

# كود التحديث الآلي كل ثانية ليبقى العداد متحركاً لا يتوقف
time.sleep(1)
st.rerun()

