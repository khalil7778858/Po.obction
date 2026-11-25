import streamlit as st
from PIL import Image
import numpy as np

# إعداد الصفحة لتكون خفيفة ومتجاوبة مع الجوال
st.set_page_config(
    page_title="محلل احتمالات الشارت (10 دقائق)",
    page_icon="📊",
    layout="centered"
)

# تنسيق عربي بسيط وواضح
st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stRadio"] > label, div[data-testid="stSelectbox"] > label {
        font-weight: bold;
    }
    .result-box {
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
        margin-bottom: 12px;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 محلل احتمالات الشارت (10 دقائق)")
st.caption("أداة مساعدة لتقدير الاحتمالات عبر دمج EMA + RSI 14 + MACD — وليست ضماناً للنتيجة.")

# 1. رفع لقطة الشاشة
uploaded_file = st.file_uploader("📸 ارفع أو الصق لقطة شاشة الشارت هنا", type=["png", "jpg", "jpeg"])

def quick_image_color_hint(img: Image.Image):
    """فحص بصري أولي بسيط لنسبة الشموع الخضراء والحمراء في منطقة الشارت العليا"""
    small = img.resize((200, 200)).convert("RGB")
    arr = np.array(small, dtype=np.int16)
    # التركيز على النصف العلوي (منطقة الشموع)
    chart_area = arr[:90, :, :]
    r, g, b = chart_area[:, :, 0], chart_area[:, :, 1], chart_area[:, :, 2]
    green_pixels = np.sum((g > r + 25) & (g > b + 20) & (g > 80))
    red_pixels = np.sum((r > g + 25) & (r > b + 20) & (r > 80))
    total = green_pixels + red_pixels
    if total == 0:
        return "غير محدد بصرياً"
    green_pct = round((green_pixels / total) * 100)
    red_pct = 100 - green_pct
    return f"سيطرة لونية أولية في منطقة الشموع: 🟢 {green_pct}% | 🔴 {red_pct}%"

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="لقطة الشارت المرفوعة", use_container_width=True)
    st.info(quick_image_color_hint(image))
else:
    st.warning("ارفع لقطة الشاشة أولاً (ويُفضّل التقاطها قبل إغلاق الشمعة بـ 10 إلى 15 ثانية).")

st.divider()

# 2. مدخلات الفريم وإدارة رأس المال
col1, col2, col3 = st.columns(3)
with col1:
    timeframe = st.selectbox("الإطار الزمني (الفريم)", ["M5 (الأفضل)", "M15", "M1", "M30"], index=0)
with col2:
    balance = st.number_input("الرصيد الحالي ($)", min_value=1.0, value=1000.0, step=10.0)
with col3:
    stake = st.number_input("مبلغ الصفقة ($)", min_value=1.0, value=25.0, step=5.0)

# تنبيه إدارة المخاطر الصارم
risk_pct = (stake / balance) * 100 if balance > 0 else 100
if risk_pct > 5:
    st.error(f"⚠️ تنبيه مخاطرة: مبلغ الصفقة يمثل {risk_pct:.1f}% من رصيدك! يُنصح ألا يتجاوز 1% إلى 3%.")

st.subheader("🔍 قراءة الشروط الأربعة على الشارت")

# 3. تقييم النقاط الأربع
ema_state = st.radio(
    "1️⃣ وضع السعر مع خط Moving Average (EMA):",
    [
        "صاعد: السعر فوق الخط والخط مائل للأعلى",
        "هابط: السعر تحت الخط والخط مائل للأسفل",
        "متداخل / تذبذب عرضي أو بعد قفزة سعرية حادة"
    ],
    index=2
)

candle_state = st.radio(
    "2️⃣ سلوك الشمعة الحالية وقت الإغلاق:",
    [
        "شمعة خضراء مؤكدة للصعود (بدون ذيل علوي طويل معيق)",
        "شمعة حمراء مؤكدة للهبوط (بدون ذيل سفلي طويل معيق)",
        "شمعة صغيرة مترددة / ذيول طويلة / تصحيح غير واضح"
    ],
    index=2
)

rsi_state = st.radio(
    "3️⃣ وضع مؤشر RSI 14:",
    [
        "فوق مستوى 50 ويتجه صعوداً (دون تشبع حاد فوق 75)",
        "تحت مستوى 50 ويتجه هبوطاً (دون تشبع حاد تحت 25)",
        "قرب مستوى 50 (حيرة) أو في تشبع حاد ينذر بارتداد"
    ],
    index=2
)

macd_state = st.radio(
    "4️⃣ وضع مؤشر MACD (12, 26, 9):",
    [
        "زخم صاعد: تقاطع إيجابي أو أعمدة خضراء متصاعدة",
        "زخم هابط: تقاطع سلبي أو أعمدة حمراء متزايدة",
        "ضعيف / متقطع قرب خط الصفر أو يعاكس الاتجاه"
    ],
    index=2
)

# 4. حساب النقاط والاحتمالات
if st.button("🚀 احسب الاحتمال والقرار الآن", use_container_width=True):
    bull_score = 0
    bear_score = 0
    reasons = []

    # تقييم EMA
    if "صاعد" in ema_state:
        bull_score += 1
        reasons.append("✅ السعر مدعوم فوق المتوسط الصاعد.")
    elif "هابط" in ema_state:
        bear_score += 1
        reasons.append("✅ السعر يتحرك أسفل المتوسط الهابط.")
    else:
        reasons.append("⚠️ غياب اتجاه واضح مع EMA أو وجود تذبذب.")

    # تقييم الشمعة
    if "خضراء" in candle_state:
        bull_score += 1
        reasons.append("✅ إغلاق الشمعة يدعم الزخم الشرائي.")
    elif "حمراء" in candle_state:
        bear_score += 1
        reasons.append("✅ إغلاق الشمعة يدعم الزخم البيعي.")
    else:
        reasons.append("⚠️ سلوك الشمعة يُظهر تردداً أو رفضاً سعرياً.")

    # تقييم RSI
    if "فوق مستوى 50" in rsi_state:
        bull_score += 1
        reasons.append("✅ مؤشر RSI 14 يدعم الصعود دون تشبع مفرط.")
    elif "تحت مستوى 50" in rsi_state:
        bear_score += 1
        reasons.append("✅ مؤشر RSI 14 يدعم الهبوط دون تشبع مفرط.")
    else:
        reasons.append("⚠️ مؤشر RSI 14 في منطقة حيرة أو تشبع خطير.")

    # تقييم MACD
    if "زخم صاعد" in macd_state:
        bull_score += 1
        reasons.append("✅ مؤشر MACD يؤكد الزخم الصاعد.")
    elif "زخم هابط" in macd_state:
        bear_score += 1
        reasons.append("✅ مؤشر MACD يؤكد الزخم الهابط.")
    else:
        reasons.append("⚠️ مؤشر MACD ضعيف أو متضارب.")

    # حساب النسبة التقديرية بناءً على تطابق الشروط
    st.divider()
    st.subheader("📌 نتيجة الفحص وتقدير حركة الـ 10 دقائق")

    if risk_pct > 15:
        st.error("🛑 تم إيقاف التوصية بالدخول: مبلغ الصفقة مرتفع جداً مقارنة بالرصيد. خفّض المبلغ أولاً.")
    elif bull_score >= 3 and bear_score == 0:
        prob = 72 if bull_score == 3 else 82
        st.success(f"🟢 القرار: **شراء (CALL)** | قوة التطابق: **{bull_score}/4** (احتمال تقديري: ~{prob}%)")
        st.write("⏱️ **المدة المقترحة:** `00:02:30` إلى `00:03:00` (مع مراقبة استمرار الموجة خلال 10 دقائق).")
    elif bear_score >= 3 and bull_score == 0:
        prob = 72 if bear_score == 3 else 82
        st.error(f"🔴 القرار: **بيع (PUT)** | قوة التطابق: **{bear_score}/4** (احتمال تقديري: ~{prob}%)")
        st.write("⏱️ **المدة المقترحة:** `00:02:30` إلى `00:03:00` (مع مراقبة استمرار الموجة خلال 10 دقائق).")
    else:
        st.warning(f"⏸️ القرار: **تجاوز / لا تدخل الآن (WAIT)** | صعود: `{bull_score}/4` — هبوط: `{bear_score}/4`")
        st.write("السبب: الإشارات غير مكتملة أو متضاربة، واحتمال التذبذب خلال الـ 10 دقائق القادمة مرتفع.")

    for r in reasons:
        st.write(r)
