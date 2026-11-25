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

EMA_OPTIONS = [
    "صاعد: السعر فوق الخط والخط مائل للأعلى",
    "هابط: السعر تحت الخط والخط مائل للأسفل",
    "متداخل / تذبذب عرضي أو بعد قفزة سعرية حادة"
]

CANDLE_OPTIONS = [
    "شمعة خضراء مؤكدة للصعود (بدون ذيل علوي طويل معيق)",
    "شمعة حمراء مؤكدة للهبوط (بدون ذيل سفلي طويل معيق)",
    "شمعة صغيرة مترددة / ذيول طويلة / تصحيح غير واضح"
]

RSI_OPTIONS = [
    "فوق مستوى 50 ويتجه صعوداً (دون تشبع حاد فوق 75)",
    "تحت مستوى 50 ويتجه هبوطاً (دون تشبع حاد تحت 25)",
    "قرب مستوى 50 (حيرة) أو في تشبع حاد ينذر بارتداد"
]

MACD_OPTIONS = [
    "زخم صاعد: تقاطع إيجابي أو أعمدة خضراء متصاعدة",
    "زخم هابط: تقاطع سلبي أو أعمدة حمراء متزايدة",
    "ضعيف / متقطع قرب خط الصفر أو يعاكس الاتجاه"
]


def get_api_key() -> str:
    if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
        return str(st.secrets["GEMINI_API_KEY"]).strip()
    return os.environ.get("GEMINI_API_KEY", "").strip()


def fallback_visual_estimate(img: Image.Image) -> dict:
    small = img.resize((240, 240)).convert("RGB")
    arr = np.array(small, dtype=np.int16)
    h, _, _ = arr.shape
    chart_zone = arr[: int(h * 0.55), :, :]
    r, g, b = chart_zone[:, :, 0], chart_zone[:, :, 1], chart_zone[:, :, 2]

    green = int(np.sum((g > r + 25) & (g > b + 20) & (g > 80)))
    red = int(np.sum((r > g + 25) & (r > b + 20) & (r > 80)))

    if green > red * 1.35:
        return {
            "ema": EMA_OPTIONS[0],
            "candle": CANDLE_OPTIONS[0],
            "rsi": RSI_OPTIONS[0],
            "macd": MACD_OPTIONS[0],
            "summary": f"تقدير أولي بدون API (أخضر: {green}، أحمر: {red}). أضف GEMINI_API_KEY لدقة أعلى."
        }
    if red > green * 1.35:
        return {
            "ema": EMA_OPTIONS[1],
            "candle": CANDLE_OPTIONS[1],
            "rsi": RSI_OPTIONS[1],
            "macd": MACD_OPTIONS[1],
            "summary": f"تقدير أولي بدون API (أخضر: {green}، أحمر: {red}). أضف GEMINI_API_KEY لدقة أعلى."
        }
    return {
        "ema": EMA_OPTIONS[2],
        "candle": CANDLE_OPTIONS[2],
        "rsi": RSI_OPTIONS[2],
        "macd": MACD_OPTIONS[2],
        "summary": f"تقدير أولي بدون API (أخضر: {green}، أحمر: {red}). أضف GEMINI_API_KEY لدقة أعلى."
    }
