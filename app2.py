import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="قناص RSI + MACD بالصورة", layout="centered")

st.markdown("""
<style>
.main { direction: rtl; text-align: right; }
.stButton>button { width: 100%; border-radius: 10px; font-weight: bold; padding: 11px; }
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

st.title("⚡ قناص الصفقات بالصورة (RSI + MACD)")
st.caption("أرفق لقطة الشاشة ليقوم البرنامج بفحص المؤشرين وإعطاء النتيجة فقط عند توافقهما")

now = datetime.now()
rem_m = 4 - (now.minute % 5)
rem_s = 59 - now.second
st.info(f"🕒 المتبقي لإغلاق شمعة 5 دقائق الحالية: **{rem_m:02d}:{rem_s:02d}**")


def analyze_chart_image(pil_img: Image.Image):
    """تحليل بصري خفيف لمنطقة RSI و MACD والشموع الأخيرة في لقطة الشاشة"""
    img = pil_img.convert("RGB")
    # توحيد العرض لثبات التحليل على مختلف الشاشات
    target_w = 540
    ratio = target_w / max(img.width, 1)
    target_h = max(int(img.height * ratio), 200)
    img = img.resize((target_w, target_h))
    arr = np.array(img, dtype=np.int16)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # قناع البكسلات الخضراء والحمراء الواضحة
    green_mask = (g - r > 22) & (g - b > 15) & (g > 75)
    red_mask = (r - g > 25) & (r - b > 20) & (r > 90)

    # تحديد مناطق الشارت: الشموع (12% إلى 55%)، RSI (56% إلى 68%)، MACD (68% إلى 80%)
    h = target_h
    w = target_w
    right_start = int(w * 0.55)

    rsi_y1, rsi_y2 = int(h * 0.56), int(h * 0.68)
    macd_y1, macd_y2 = int(h * 0.68), int(h * 0.80)
    candle_y1, candle_y2 = int(h * 0.14), int(h * 0.55)

    rsi_g = int(np.sum(green_mask[rsi_y1:rsi_y2, right_start:w]))
    rsi_r = int(np.sum(red_mask[rsi_y1:rsi_y2, right_start:w]))

    macd_g = int(np.sum(green_mask[macd_y1:macd_y2, right_start:w]))
    macd_r = int(np.sum(red_mask[macd_y1:macd_y2, right_start:w]))

    candle_g = int(np.sum(green_mask[candle_y1:candle_y2, right_start:w]))
    candle_r = int(np.sum(red_mask[candle_y1:candle_y2, right_start:w]))

    # تحديد إشارة RSI (انحناء صعودي/شراء أم هبوطي/بيع أم محايد)
    if rsi_g > rsi_r * 1.35 and rsi_g > 25:
        rsi_sig = "BUY"
        rsi_txt = "صعود / شراء (تشبع أو زخم إيجابي)"
    elif rsi_r > rsi_g * 1.35 and rsi_r > 25:
        rsi_sig = "SELL"
        rsi_txt = "هبوط / بيع (تشبع أو زخم سلبي)"
    else:
        rsi_sig = "NEUTRAL"
        rsi_txt = "غير حاسم / متقارب"

    # تحديد إشارة MACD
    if macd_g > macd_r * 1.25 and macd_g > 30:
        macd_sig = "BUY"
        macd_txt = "زخم صعودي / شراء"
    elif macd_r > macd_g * 1.25 and macd_r > 30:
        macd_sig = "SELL"
        macd_txt = "زخم هبوطي / بيع"
    else:
        macd_sig = "NEUTRAL"
        macd_txt = "تذبذب / غير حاسم"

    return {
        "rsi_sig": rsi_sig,
        "macd_sig": macd_sig,
        "rsi_txt": rsi_txt,
        "macd_txt": macd_txt,
        "candle_g": candle_g,
        "candle_r": candle_r,
    }


st.subheader("1. أرفق صورة الشارت للحصول على النتيجة")
uploaded_img = st.file_uploader(
    "اختر لقطة الشاشة من هاتفك أو جهازك",
    type=["png", "jpg", "jpeg"]
)

if uploaded_img is not None:
    image = Image.open(uploaded_img)
    st.image(image, caption="لقطة الشارت المرفقة", use_container_width=True)

    res = analyze_chart_image(image)

    st.markdown("**قراءة المؤشرين من الصورة:**")
    st.write(f"- **مؤشر RSI:** {res['rsi_txt']}")
    st.write(f"- **مؤشر MACD:** {res['macd_txt']}")

    if res["rsi_sig"] == "SELL" and res["macd_sig"] == "SELL":
        st.markdown("""
        <div class="put-box">
            <h3>🔴 النتيجة: بيع (هبوط / PUT)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على الهبوط في الصورة.</p>
            <p><b>التنفيذ:</b> ادخل مع بداية شمعة جديدة بمدة 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    elif res["rsi_sig"] == "BUY" and res["macd_sig"] == "BUY":
        st.markdown("""
        <div class="call-box">
            <h3>🟢 النتيجة: شراء (صعود / CALL)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على الصعود في الصورة.</p>
            <p><b>التنفيذ:</b> ادخل مع بداية شمعة جديدة بمدة 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="wait-box">
            <h3>⏸️ لا توجد نتيجة — المؤشران غير متفقين</h3>
            <p>لم يتوافق RSI و MACD في نفس الاتجاه بوضوح — تجنب الدخول وانتظر إشارة أوضح.</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("قم بإرفاق صورة الشارت أولاً ليقوم البرنامج بفحص RSI و MACD وإعطائك النتيجة.")

st.divider()
st.subheader("2. حاسبة الصفقة الآمنة (3%)")
balance = st.number_input("الرصيد الحالي ($)", min_value=1.0, value=1000.0, step=10.0)
st.success(f"💰 قيمة الصفقة المقترحة (3%): **${balance * 0.03:.2f}**")
