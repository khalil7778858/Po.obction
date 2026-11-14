import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="مستشار صفقات Quotex المباشر", page_icon="🎯", layout="centered")

# تنسيق عربي احترافي وواضح للعين
st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; font-weight: bold; font-size: 18px; padding: 12px; border-radius: 10px; background-color: #0066cc; color: white; }
    .decision-card { padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .call-card { background-color: #e6f9ed; border: 2px solid #00c853; color: #004d20; }
    .put-card { background-color: #ffebee; border: 2px solid #ff1744; color: #7f0000; }
    .wait-card { background-color: #fff8e1; border: 2px solid #ffb300; color: #664600; }
    .reason-item { background-color: #f8f9fa; padding: 10px 15px; border-radius: 8px; margin-bottom: 8px; border-right: 4px solid #0066cc; font-size: 15px; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 مستشار صفقات Quotex المباشر")
st.caption("يحلل السوق تلقائياً ويعطيك قرار الدخول المباشر بدون الحاجة لأي خطوات إضافية")

# اختيار الزوج والفريم الزمني
col1, col2 = st.columns(2)
with col1:
    pair = st.selectbox("اختر زوج العملات (السوق الحقيقي):", [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY"
    ])
with col2:
    timeframe = st.selectbox("اختر الفريم الزمني:", [
        "1m (دقيقة واحدة)", "5m (5 دقائق)", "15m (15 دقيقة)"
    ])

# دالة جلب البيانات الحية
@st.cache_data(ttl=20) # تحديث سريع كل 20 ثانية
def fetch_market_data(symbol, tf):
    base, quote = symbol.split("/")
    yahoo_symbol = f"{base}{quote}=
