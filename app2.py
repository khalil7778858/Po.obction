import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="قناص RSI + MACD السريع", layout="centered")

st.markdown("""
<style>
.main { direction: rtl; text-align: right; }
.state-card {
    background-color: rgba(30, 41, 59, 0.55);
    border: 1px solid #334155;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
}
.call-box {
    background-color: rgba(16, 185, 129, 0.16);
    border: 1px solid #10b981;
    color: #a7f3d0;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-top: 10px;
}
.put-box {
    background-color: rgba(239, 68, 68, 0.16);
    border: 1px solid #ef4444;
    color: #fecaca;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-top: 10px;
}
.wait-box {
    background-color: rgba(245, 158, 11, 0.16);
    border: 1px solid #f59e0b;
    color: #fde68a;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ قناص بوكت أوبشن السريع (RSI + MACD)")

now = datetime.now()
rem_m = 4 - (now.minute % 5)
rem_s = 59 - now.second
st.caption(f"🕒 المتبقي لإغلاق شمعة 5 دقائق: **{rem_m:02d}:{rem_s:02d}**")


@st.cache_data(show_spinner=False)
def fast_read_indicators(file_bytes: bytes, sensitivity: float = 1.15):
    """قراءة سريعة جداً لحالة RSI و MACD من الصورة مع تخزين مؤقت فوري"""
    from io import BytesIO
    img = Image.open(BytesIO(file_bytes)).convert("RGB")

    # تصغير سريع جداً لتسريع الحسابات بشكل كبير
    w_fast = 300
    h_fast = max(int(img.height * (w_fast / max(img.width, 1))), 140)
    img_small = img.resize((w_fast, h_fast))
    arr = np.asarray(img_small, dtype=np.int16)[::2, ::2]

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    green = (g - r > 16) & (g - b > 10) & (g > 65)
    red = (r - g > 18) & (r - b > 14) & (r > 80)

    h, w = arr.shape[0], arr.shape[1]
    x_start = int(w * 0.42)

    rsi_y1, rsi_y2 = int(h * 0.54), int(h * 0.68)
    macd_y1, macd_y2 = int(h * 0.68), int(h * 0.83)

    rsi_g = int(green[rsi_y1:rsi_y2, x_start:w].sum())
    rsi_r = int(red[rsi_y1:rsi_y2, x_start:w].sum())

    macd_g = int(green[macd_y1:macd_y2, x_start:w].sum())
    macd_r = int(red[macd_y1:macd_y2, x_start:w].sum())

    if rsi_r > rsi_g * sensitivity and rsi_r > 4:
        rsi_state, rsi_label = "SELL", "🔴 حالة RSI: هبوط / بيع"
    elif rsi_g > rsi_r * sensitivity and rsi_g > 4:
        rsi_state, rsi_label = "BUY", "🟢 حالة RSI: صعود / شراء"
    else:
        rsi_state, rsi_label = "NEUTRAL", "⚪ حالة RSI: متذبذب / غير واضح"

    if macd_r > macd_g * sensitivity and macd_r > 5:
        macd_state, macd_label = "SELL", "🔴 حالة MACD: هبوط / بيع"
    elif macd_g > macd_r * sensitivity and macd_g > 5:
        macd_state, macd_label = "BUY", "🟢 حالة MACD: صعود / شراء"
    else:
        macd_state, macd_label = "NEUTRAL", "⚪ حالة MACD: متذبذب / غير واضح"

    return rsi_state, rsi_label, macd_state, macd_label


sensitivity = st.slider("حساسية المطابقة", 1.05, 1.75, 1.15, 0.05)
uploaded_file = st.file_uploader("أرفق لقطة الشاشة", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_bytes = uploaded_file.getvalue()
    st.image(raw_bytes, caption="لقطة الشاشة", width=360)

    rsi_state, rsi_label, macd_state, macd_label = fast_read_indicators(raw_bytes, sensitivity)

    st.markdown(f'<div class="state-card"><b>{rsi_label}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="state-card"><b>{macd_label}</b></div>', unsafe_allow_html=True)

    if rsi_state == "SELL" and macd_state == "SELL":
        st.markdown("""
        <div class="put-box">
            <h3>🔴 النتيجة: بيع (هبوط / PUT)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على البيع — المدة: 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    elif rsi_state == "BUY" and macd_state == "BUY":
        st.markdown("""
        <div class="call-box">
            <h3>🟢 النتيجة: شراء (صعود / CALL)</h3>
            <p>مؤشر RSI ومؤشر MACD متفقان على الصعود — المدة: 2 إلى 3 دقائق.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="wait-box">
            <h3>⏸️ لا توجد نتيجة — المؤشران غير متفقين</h3>
            <p>لا توجد إشارة متوافقة حالياً؛ انتظر توافق RSI و MACD.</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
balance = st.number_input("الرصيد الحالي ($)", min_value=1.0, value=1000.0, step=10.0)
st.success(f"💰 قيمة الصفقة المقترحة (3%): **${balance * 0.03:.2f}**")
