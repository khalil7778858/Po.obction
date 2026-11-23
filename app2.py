import streamlit as st
from datetime import datetime

st.set_page_config(page_title="قناص RSI + MACD", layout="centered")

st.markdown("""
<style>
.main { direction: rtl; text-align: right; }
.stButton>button { width: 100%; border-radius: 10px; font-weight: bold; padding: 10px; }
.call-box {
    background-color: rgba(16, 185, 129, 0.16);
    border: 1px solid #10b981;
    color: #a7f3d0;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-top: 12px;
}
.put-box {
    background-color: rgba(239, 68, 68, 0.16);
    border: 1px solid #ef4444;
    color: #fecaca;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-top: 12px;
}
.wait-box {
    background-color: rgba(245, 158, 11, 0.16);
    border: 1px solid #f59e0b;
    color: #fde68a;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ قناص الصفقات (RSI + MACD)")
st.caption("لا يتم إصدار إشارة دخول إلا إذا اتفق مؤشر RSI ومؤشر MACD في نفس الاتجاه")

# عداد شموع 5 دقائق (مرجع لحظي)
now = datetime.now()
rem_m = 4 - (now.minute % 5)
rem_s = 59 - now.second
st.info(f"🕒 الوقت المتبقي لإغلاق شمعة 5 دقائق الحالية: **{rem_m:02d}:{rem_s:02d}**")

st.subheader("1. اختر حالة المؤشرين")

rsi_state = st.radio(
    "مؤشر RSI:",
    [
        "غير محدد / في المنتصف",
        "تشبع شرائي / انحناء هبوطي (بيع)",
        "تشبع بيعي / انحناء صعودي (شراء)"
    ],
    index=0
)

macd_state = st.radio(
    "مؤشر MACD:",
    [
        "غير محدد / متذبذب",
        "تقاطع أو ضعف زخم هبوطي (بيع)",
        "تقاطع أو ضعف زخم صعودي (شراء)"
    ],
    index=0
)

if st.button("فحص التوافق وإعطاء النتيجة"):
    rsi_sell = rsi_state == "تشبع شرائي / انحناء هبوطي (بيع)"
    rsi_buy = rsi_state == "تشبع بيعي / انحناء صعودي (شراء)"

    macd_sell = macd_state == "تقاطع أو ضعف زخم هبوطي (بيع)"
    macd_buy = macd_state == "تقاطع أو ضعف زخم صعودي (شراء)"

    if rsi_sell and macd_sell:
        st.markdown("""
        <div class="put-box">
            <h3>🔴 إشارة مؤكدة: بيع (هبوط / PUT)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على الهبوط.</p>
            <p><b>التنفيذ:</b> ادخل مع بداية شمعة جديدة بمدة 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    elif rsi_buy and macd_buy:
        st.markdown("""
        <div class="call-box">
            <h3>🟢 إشارة مؤكدة: شراء (صعود / CALL)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على الصعود.</p>
            <p><b>التنفيذ:</b> ادخل مع بداية شمعة جديدة بمدة 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="wait-box">
            <h3>⏸️ لا توجد نتيجة — المؤشران غير متفقين</h3>
            <p>تجنب الدخول الآن وانتظر حتى تتطابق إشارة RSI و MACD في نفس الاتجاه.</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.subheader("2. معاينة صورة الشارت (اختياري)")
uploaded_img = st.file_uploader("ارفع لقطة شاشة للشارت للمتابعة البصرية", type=["png", "jpg", "jpeg"])
if uploaded_img is not None:
    st.image(uploaded_img, caption="لقطة الشارت المرفوعة", use_container_width=True)

st.divider()
st.subheader("3. حاسبة الصفقة الآمنة (3%)")
balance = st.number_input("الرصيد الحالي ($)", min_value=1.0, value=1000.0, step=10.0)
safe_stake = balance * 0.03
st.success(f"💰 قيمة الصفقة المقترحة (3%): **${safe_stake:.2f}**")
