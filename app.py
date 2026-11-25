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
    .stMarkdown, .stText, p, h1, h2, h3, label {
        text-align: right !important;
        direction: rtl !important;
    }
    h1 {
        font-size: 1.5rem !important;
        line-height: 1.4 !important;
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
        return str(st.secrets["GEMINI_API_KEY
