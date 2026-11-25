import json
import os
import re
import numpy as np
from PIL import Image
import streamlit as st

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

st.set_page_config(
    page_title="محلل الشارت التلقائي (10 دقائق)",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stRadio"] > label, div[data-testid="stSelectbox"] > label {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 محلل الشارت التلقائي (10 دقائق)")
st.caption("ارفع لقطة الشارت ليقوم النظام بقراءتها وحساب الاحتمالات تلقائياً — أداة مساعدة وليست ضماناً للنتيجة.")

def get_api_key() -> str:
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
        return str(st.secrets["GEMINI_API_KEY"]).strip()
    return os.environ.get("GEMINI_API_KEY", "").strip()

def fallback_visual_estimate(img: Image.Image) -> dict:
    """تقدير بصري أولي في حال عدم توفر مفتاح API"""
    small = img.resize((240, 240)).convert("RGB")
    arr = np.array(small, dtype=np.int16)
    h, w, _ = arr.shape
    chart_zone = arr[: int(h * 0.55), :, :]
    r, g, b = chart_zone[:, :, 0], chart_zone[:, :, 1], chart_zone[:, :, 2]

    green = int(np.sum((g > r + 25) & (g > b + 20) & (g > 80)))
    red = int(np.sum((r > g + 25) & (r > b + 20) & (r > 80)))

    if green > red * 1.35:
        ema_s = "صاعد: السعر فوق الخط والخط مائل للأعلى"
        candle_s = "شمعة خضراء مؤكدة للصعود (بدون ذيل علوي طويل معيق)"
        rsi_s = "فوق مستوى 50 ويتجه صعوداً (دون تشبع حاد فوق 75)"
        macd_s = "زخم صاعد: تقاطع إيجابي أو أعمدة خضراء متصاعدة"
    elif red > green * 1.35:
        ema_s = "هابط: السعر تحت الخط والخط مائل للأسفل"
        candle_s = "شمعة حمراء مؤكدة للهبوط (بدون ذيل سفلي طويل معيق)"
        rsi_s = "تحت مستوى 50 ويتجه هبوطاً (دون تشبع حاد تحت 25)"
        macd_s = "زخم هابط: تقاطع سلبي أو أعمدة حمراء متزايدة"
    else:
        ema_s = "متداخل / تذبذب عرضي أو بعد قفزة سعرية حادة"
        candle_s = "شمعة صغيرة مترددة / ذيول طويلة / تصحيح غير واضح"
        rsi_s = "قرب مستوى 50 (حيرة) أو في تشبع حاد ينذر بارتداد"
        macd_s = "ضعيف / متقطع قرب خط الصفر أو يعاكس الاتجاه"

    return {
        "ema": ema_s,
        "candle": candle_s,
        "rsi": rsi_s,
        "macd": macd_s,
        "summary": f"تقدير لوني أولي بدون API (أخضر: {green}، أحمر: {red}). أضف GEMINI_API_KEY لقراءة دقيقة للشموع والمؤشرات."
    }

def analyze_chart_with_gemini(img: Image.Image, timeframe: str, api_key: str) -> dict:
    client = genai.Client(api_key=api_key)
    prompt = f"""
أنت محلل فني خبير لشارت التداول على إطار {timeframe}.
انظر إلى صورة الشارت المرفقة بدقة وحدد الحالة الفنية لكل عنصر من العناصر الأربعة التالية:

1. "ema": اختر بدقة واحدة فقط من هذه العبارات الثلاث:
   - "صاعد: السعر فوق الخط والخط مائل للأعلى"
   - "هابط: السعر تحت الخط والخط مائل للأسفل"
   - "متداخل / تذبذب عرضي أو بعد قفزة سعرية حادة"

2. "candle": اختر بدقة واحدة فقط من هذه العبارات الثلاث:
   - "شمعة خضراء مؤكدة للصعود (بدون ذيل علوي طويل معيق)"
   - "شمعة حمراء مؤكدة للهبوط (بدون ذيل سفلي طويل معيق)"
   - "شمعة صغيرة مترددة / ذيول طويلة / تصحيح غير واضح"

3. "rsi": اختر بدقة واحدة فقط من هذه العبارات الثلاث:
   - "فوق مستوى 50 ويتجه صعوداً (دون تشبع حاد فوق 75)"
   - "تحت مستوى 50 ويتجه هبوطاً (دون تشبع حاد تحت 25)"
   - "قرب مستوى 50 (حيرة) أو في تشبع حاد ينذر بارتداد"

4. "macd": اختر بدقة واحدة فقط من هذه العبارات الثلاث:
   - "زخم صاعد: تقاطع إيجابي أو أعمدة خضراء متصاعدة"
   - "زخم هابط: تقاطع سلبي أو أعمدة حمراء متزايدة"
   - "ضعيف / متقطع قرب خط الصفر أو يعاكس الاتجاه"

5. "summary": ملخص قصير جداً ومباشر بالعربية (سطر أو سطرين) عن حركة الشارت واحتمال الـ 10 دقائق، مع التنبيه إذا كانت الصورة مقصوصة أو الشموع غير واضحة.

أعد النتيجة بصيغة JSON صالحة فقط دون أي نص إضافي خارج JSON.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[img, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    raw = (response.text or "").strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    data = json.loads(match.group(0) if match else raw)
    return data

uploaded_file = st.file_uploader("📸 ارفع لقطة شاشة الشارت هنا", type=["png", "jpg", "jpeg"])

col1, col2, col3 = st.columns(3)
with col1:
    timeframe = st.selectbox("الإطار الزمني", ["M5 (الأفضل)", "M15", "M1", "M30"], index=0)
with col2:
    balance = st.number_input("الرصيد ($)", min_value=1.0, value=1000.0, step=10.0)
with col3:
    stake = st.number_input("مبلغ الصفقة ($)", min_value=1.0, value=25.0, step=5.0)

risk_pct = (stake / balance) * 100 if balance > 0 else 100
if risk_pct > 5:
    st.error(f"⚠️ تنبيه مخاطرة: مبلغ الصفقة يمثل {risk_pct:.1f}% من رصيدك! يُنصح ألا يتجاوز 1%–3%.")

ema_options = [
    "صاعد: السعر فوق الخط والخط مائل للأعلى",
    "هابط: السعر تحت الخط والخط مائل للأسفل",
    "متداخل / تذبذب عرضي أو بعد قفزة سعرية حادة"
]
candle_options = [
    "شمعة خضراء مؤكدة للصعود (بدون ذيل علوي طويل معيق)",
    "شمعة حمراء مؤكدة للهبوط (
