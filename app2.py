import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# إعدادات الصفحة لتكون خفيفة وسريعة
st.set_page_config(page_title="محلل صفقات Quotex", page_icon="📈", layout="centered")

# تنسيق عربي نظيف
st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; }
    .signal-box { padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 محلل احتمالات Quotex الذكي")
st.caption("يجلب بيانات السوق الحية ويحسب المؤشرات الفنية لتقليد أفضل فرص الدخول")

# اختيار الزوج والفريم الزمني
col1, col2 = st.columns(2)
with col1:
    pair = st.selectbox("اختر زوج العملات (السوق الحقيقي):", [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "EUR/JPY", "GBP/JPY"
    ])
with col2:
    timeframe = st.selectbox("الفريم الزمني (مدة الشمعة):", [
        "1m (دقيقة واحدة)", "5m (5 دقائق)", "15m (15 دقيقة)"
    ])

# دالة جلب البيانات الحية (من مصدر مجاني سريع بدون مفتاح API معقد)
@st.cache_data(ttl=30) # تحديث البيانات كل 30 ثانية لتسريع التطبيق ومنع البطء
def fetch_market_data(symbol, tf):
    base, quote = symbol.split("/")
    # استخدام Binance للعملات الرقمية أو API مجاني للأسعار الحية كمحاكاة/بيانات حقيقية
    # ملاحظة: لجلب بيانات فوركس حية مجانية بدون قيود، نستخدم API Yahoo Finance المباشر
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
    except Exception as e:
        return None

# دالة حساب المؤشرات الفنية
def calculate_indicators(df):
    # 1. RSI (14)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 2. EMA (9 & 21)
    df['EMA_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['close'].ewm(span=21, adjust=False).mean()
    
    # 3. Bollinger Bands (20, 2)
    df['BB_Mid'] = df['close'].rolling(window=20).mean()
    df['BB_Std'] = df['close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)
    
    # 4. MACD (12, 26, 9)
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

# زر التحديث الفوري
if st.button("🔄 تحديث البيانات وتحليل السوق الآن"):
    st.cache_data.clear()

df = fetch_market_data(pair, timeframe)

if df is not None and len(df) > 30:
    df = calculate_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    # حساب نقاط الاحتمالية (من 100%)
    buy_score = 0
    sell_score = 0
    reasons = []
    
    # تحليل RSI
    if last['RSI'] < 30:
        buy_score += 30
        reasons.append(f"RSI في تشبع بيعي ({last['RSI']:.1f}) -> يدعم الصعود")
    elif last['RSI'] > 70:
        sell_score += 30
        reasons.append(f"RSI في تشبع شرائي ({last['RSI']:.1f}) -> يدعم الهبوط")
    elif last['RSI'] < 45:
        buy_score += 10
    elif last['RSI'] > 55:
        sell_score += 10

    # تحليل EMA
    if last['EMA_9'] > last['EMA_21']:
        buy_score += 25
        reasons.append("تقاطع EMA 9 فوق EMA 21 -> اتجاه صاعد")
    else:
        sell_score += 25
        reasons.append("تقاطع EMA 9 تحت EMA 21 -> اتجاه هابط")

    # تحليل Bollinger Bands
    if last['close'] <= last['BB_Lower']:
        buy_score += 25
        reasons.append("السعر لامس الحد السفلي للبولينجر -> احتمال ارتداد صاعد")
    elif last['close'] >= last['BB_Upper']:
        sell_score += 25
        reasons.append("السعر لامس الحد العلوي للبولينجر -> احتمال ارتداد هابط")

    # تحليل MACD
    if last['MACD'] > last['Signal_Line']:
        buy_score += 20
        reasons.append("زخم MACD إيجابي (فوق خط الإشارة)")
    else:
        sell_score += 20
        reasons.append("زخم MACD سلبي (تحت خط الإشارة)")

    # تحديد القرار النهائي
    st.divider()
    if buy_score > sell_score and buy_score >= 60:
        st.success(f"### 🟢 إشارة صعود (CALL) — نسبة الاحتمال: {buy_score}%")
    elif sell_score > buy_score and sell_score >= 60:
        st.error(f"### 🔴 إشارة هبوط (PUT) — نسبة الاحتمال: {sell_score}%")
    else:
        st.warning(f"### ⚪ السوق متذبذب (انتظر فرصة أوضح) | صعود: {buy_score}% - هبوط: {sell_score}%")

    # عرض القيم الرقمية
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("السعر الحالي", f"{last['close']:.5f}")
    c2.metric("مؤشر RSI", f"{last['RSI']:.1f}")
    c3.metric("EMA 9 / 21", "صاعد" if last['EMA_9'] > last['EMA_21'] else "هابط")
    c4.metric("MACD", f"{last['MACD']:.6f}")

    # مربع نص جاهز للنسخ وإرساله لي في المحادثة لأحلله لك بعمق
    st.subheader("📋 تقرير البيانات الجاهز للتحليل (انسخه وأرسله لي)")
    report_text = f"""تحليل زوج {pair} على فريم {timeframe}:
- السعر الحالي: {last['close']:.5f} (الشمعة السابقة: {prev['close']:.5f})
- مؤشر RSI (14): {last['RSI']:.2f}
- المتوسطات: EMA9 = {last['EMA_9']:.5f} | EMA21 = {last['EMA_21']:.5f}
- البولينجر: العلوي = {last['BB_Upper']:.5f} | السفلي = {last['BB_Lower']:.5f}
- مؤشر MACD: {last['MACD']:.6f} | Signal: {last['Signal_Line']:.6f}
- تقييم النظام: صعود {buy_score}% / هبوط {sell_score}%
ما رأيك في الدخول الآن؟"""
    
    st.code(report_text, language="text")

else:
    st.error("⚠️ تعذر جلب البيانات حالياً (قد يكون السوق مغلقاً في عطلة نهاية الأسبوع). جرب لاحقاً أو اختر زوجاً آخر.")
