import time
from iqoptionapi.stable_api import IQOption
import talib
import numpy as np

# 1. تسجيل الدخول إلى حسابك في IQ Option
# استبدل الإيميل وكلمة المرور ببيانات حسابك الفعلي أو التجريبي
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

print("جاري الاتصال بمنصة IQ Option...")
api = IQOption(EMAIL, PASSWORD)
api.connect()

if api.check_connect():
    print("تم الاتصال بنجاح بمنصة IQ Option!")
else:
    print("فشل الاتصال، تحقق من البريد الإلكتروني أو كلمة المرور.")
    exit()

# اختيار الحساب (practice للتجريبي أو real للحقيقي)
api.change_balance("practice") 

# إعدادات الأصول وإطار الوقت (مثال: EURUSD لمدة 5 دقائق = 300 ثانية)
ASSET = "EURUSD"
TIMEFRAME = 300  # 5 دقائق

def analyze_and_get_signal(asset, timeframe):
    print(جاري جلب وتحليل بيانات شمعة الـ 5 دقائق للأصل {asset}...)
    
    # سحب آخر 100 شمعة من المنصة
    candles = api.get_candles(asset, timeframe, 100, time.time())
    
    if not candles:
        print("تعذر جلب بيانات الشموع حالياً.")
        return None

    # استخراج أسعار الإغلاق (Close Prices)
    closes = np.array([float(c['close']) for c in candles])
    
    # حساب المؤشرات الفنية بدقة
    ema_20 = talib.EMA(closes, timeperiod=20)
    ema_50 = talib.EMA(closes, timeperiod=50)
    rsi = talib.RSI(closes, timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    
    # القراءات الأخيرة للمؤشرات
    current_rsi = rsi[-1]
    current_ema20 = ema_20[-1]
    current_ema50 = ema_50[-1]
    prev_ema20 = ema_20[-2]
    prev_ema50 = ema_50[-2]
    
    current_macd = macd[-1]
    current_signal = macdsignal[-1]
    
    # شروط إعطاء الإشارة والدقة
    signal = "NEUTRAL"
    strength = "منخفضة"
    
    # شروط الصعود (CALL)
    # تقاطع إيجابي لـ EMA + تشبع بيعي أو صعود في RSI + تقاطع MACD إيجابي
    if (prev_ema20 <= prev_ema50 and current_ema20 > current_ema50) and (current_rsi < 55) and (current_macd > current_signal):
        signal = "CALL (صعود)"
        strength = "عالية ومؤكدة"
        
    # شروط الهبوط (PUT)
    # تقاطع سلبي لـ EMA + صعود RSI لمناطق التشبع + تقاطع MACD سلبي
    elif (prev_ema20 >= prev_ema50 and current_ema20 < current_ema50) and (current_rsi > 45) and (current_macd < current_signal):
        signal = "PUT (هبوط)"
        strength = "عالية ومؤكدة"
        
    # تحديد وقت الدخول والإغلاق
    current_time = time.strftime('%H:%M:%S', time.localtime())
    expiry_time_calculated = time.strftime('%H:%M:%S', time.localtime(time.time() + 300)) # بعد 5 دقائق بالضبط
    
    result = {
        "time": current_time,
        "asset": asset,
        "signal": signal,
        "strength": strength,
        "entry_time": current_time,
        "expiry_time": expiry_time_calculated,
        "rsi_val": round(current_rsi, 2)
    }
    return result

# حلقة تكرارية لمراقبة السوق وإعطاء الإشارات
while True:
    signal_data = analyze_and_get_signal(ASSET, TIMEFRAME)
    if signal_data and signal_data["signal"] != "NEUTRAL":
        print("\n" + "="*40)
        print("🔥 تم رصد إشارة تداول جديدة بناءً على مؤشراتك!")
        print(f"⏰ وقت الإصدار: {signal_data['time']}")
        print(f"💱 الأصل: {signal_data['asset']}")
        print(f"📊 التوصية: {signal_data['signal']}")
        print(f"💪 نسبة القوة: {signal_data['strength']}")
        print(f"⏱️ وقت دخول الصفقة: {signal_data['entry_time']}")
        print(f"⏳ وقت إغلاق الصفقة (بعد 5 دقائق): {signal_data['expiry_time']}")
        print(f"📈 قيمة مؤشر RSI: {signal_data['rsi_val']}")
        print("="*40 + "\n")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] السوق في وضع حيادي، جاري مراقبة الشمعة القادمة...")
        
    # الانتظار لمدة دقيقة قبل الفحص التالي
    time.sleep(60)
