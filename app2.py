import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

st.set_page_config(page_title="مستشار صفقات Quotex المباشر", page_icon="🎯", layout="centered")

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
st.caption("يحلل السوق تلقائياً ويعطيك قرار الدخول المباشر")

col1, col2 = st.columns(2)
with col1:
    pair = st.selectbox("اختر زوج العملات:", [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY"
    ])
with col2:
    timeframe = st.selectbox("اختر الفريم الزمني:", [
        "1m (دقيقة واحدة)", "5m (5 دقائق)", "15m (15 دقيقة)"
    ])

@st.cache_data(ttl=20)
def fetch_market_data(symbol, tf):
    base, quote = symbol.split("/")
    yahoo_symbol = f"{base}{quote}=X"
    interval_map = {"1m (دقيقة واحدة)": "1m", "5m (5 دقائق)": "5m", "15m (15 دقيقة)": "15m"}
    interval = interval_map[tf]
    
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?interval={interval}&range=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        result = res['chart']['result'][0]
        timestamps = result['timestamp']
        quote_data = result['indicators']['quote'][0]
        
        df = pd.DataFrame({
            'time': pd.to_datetime(timestamps, unit='s'),
            'open': quote_data['open'],
            'high': quote_data['high'],
            'low': quote_data['low'],
            'close': quote_data['close']
        }).dropna()
        return df
    except Exception:
        return None

def calculate_indicators(df):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['close'].ewm(span=21, adjust=False).mean()
    
    df['BB_Mid'] = df['close'].rolling(window=20).mean()
    df['BB_Std'] = df['close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)
    
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

if st.button("⚡ افحص السوق وأعطني الصفقة الآن"):
    st.cache_data.clear()

df = fetch_market_data(pair, timeframe)

if df is not None and len(df) > 30:
    df = calculate_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    buy_score = 0
    sell_score = 0
    buy_reasons = []
    sell_reasons = []
    
    if last['RSI'] <= 32:
        buy_score += 35
        buy_reasons.append(f"✅ تشبع بيعي قوي (RSI = {last['RSI']:.1f})")
    elif last['RSI'] >= 68:
        sell_score += 35
        sell_reasons.append(f"✅ تشبع شرائي قوي (RSI = {last['RSI']:.1f})")
    elif last['RSI'] < 45:
        buy_score += 10
    elif last['RSI'] > 55:
        sell_score += 10

    if last['EMA_9'] > last['EMA_21']:
        buy_score += 25
        buy_reasons.append("✅ اتجاه صاعد (EMA)")
    else:
        sell_score += 25
        sell_reasons.append("✅ اتجاه هابط (EMA)")

    if last['close'] <= last['BB_Lower']:
        buy_score += 25
        buy_reasons.append("✅ ملامسة دعم البولينجر")
    elif last['close'] >= last['BB_Upper']:
        sell_score += 25
        sell_reasons.append("✅ ملامسة مقاومة البولينجر")

    if last['MACD'] > last['Signal_Line']:
        buy_score += 15
        buy_reasons.append("✅ زخم شرائي (MACD)")
    else:
        sell_score += 15
        sell_reasons.append("✅ زخم بيعي (MACD)")

    suggested_expiry = "دقيقة إلى دقيقتين" if "1m" in timeframe else "5 دقائق"

    if buy_score >= 60 and buy_score > sell_score:
        st.markdown(f"""
        <div class="decision-card call-card">
            <h1 style="margin:0; font-size: 28px;">🟢 ادخل صفقة صعود (CALL)</h1>
            <h3 style="margin:10px 0;">الاحتمال: {buy_score}%</h3>
            <p style="margin:0;">⏱️ المدة المقترحة: {suggested_expiry}</p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("🔍 الأسباب الفنية:")
        for r in buy_reasons:
            st.markdown(f'<div class="reason-item">{r}</div>', unsafe_allow_html=True)

    elif sell_score >= 60 and sell_score > buy_score:
        st.markdown(f"""
        <div class="decision-card put-card">
            <h1 style="margin:0; font-size: 28px;">🔴 ادخل صفقة هبوط (PUT)</h1>
            <h3 style="margin:10px 0;">الاحتمال: {sell_score}%</h3>
            <p style="margin:0;">⏱️ المدة المقترحة: {suggested_expiry}</p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("🔍 الأسباب الفنية:")
        for r in sell_reasons:
            st.markdown(f'<div class="reason-item">{r}</div>', unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="decision-card wait-card">
            <h1 style="margin:0; font-size: 24px;">⚪ لا تدخل الآن (تذبذب)</h1>
            <p style="margin:10px 0;">صعود: {buy_score}% | هبوط: {sell_score}%</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("السعر الحالي", f"{last['close']:.5f}")
    c2.metric("مؤشر RSI", f"{last['RSI']:.1f}")
    c3.metric("الاتجاه", "صاعد ↗️" if last['EMA_9'] > last['EMA_21'] else "هابط ↘️")

else:
    st.error("⚠️ السوق مغلق حالياً (عطلة نهاية الأسبوع). جرب أيام العمل من الإثنين للجمعة.")
