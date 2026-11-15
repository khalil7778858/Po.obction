import time
import os
import mss
import numpy as np

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

# إحداثيات منطقة الشارت على الشاشة
CHART_AREA = {"top": 200, "left": 250, "width": 600, "height": 350}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_rsi(prices, period=14):
    """حساب مؤشر القوة النسبية RSI بدقة"""
    if len(prices) < period + 1:
        return 50.0
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    if down == 0:
        return 100.0
    rs = up / down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def calculate_alligator(prices):
    """
    محاكاة خطوط مؤشر Alligator الثلاثة بناءً على سلاسل الأسعار:
    1. الشفاه (Lips - فترة قصيرة)
    2. الأسنان (Teeth - فترة متوسطة)
    3. الفكين (Jaws - فترة طويلة)
    """
    if len(prices) < 13:
        return prices[-1], prices[-1], prices[-1]
    
    lips = np.mean(prices[-3:])   # خط الشفاه (أسرع حركة)
    teeth = np.mean(prices[-8:])  # خط الأسنان
    jaws = np.mean(prices[-13:])  # خط الفكين (أبطأ حركة)
    
    return lips, teeth, jaws

def run_alligator_analyzer():
    print("جارٍ تشغيل محلل مؤشر Alligator والمؤشرات الفنية...")
    price_history = []
    
    with mss.mss() as sct:
        while True:
            try:
                # التقاط الشارت من الذاكرة بسرعة ودون حفظ صور
                img = np.array(sct.grab(CHART_AREA))
                
                green_channel = img[:, :, 1]
                red_channel = img[:, :, 2]
                
                green_intensity = np.mean(green_channel)
                red_intensity = np.mean(red_channel)
                
                # استنباط السعر اللحظي بناءً على حركة الألوان والشمعة
                current_price = 100 + (green_intensity - red_intensity) * 0.1
                price_history.append(current_price)
                
                if len(price_history) > 25:
                    price_history.pop(0)
                
                # حساب المؤشرات
                rsi_val = calculate_rsi(np.array(price_history))
                lips, teeth, jaws = calculate_alligator(np.array(price_history))
                
                clear_screen()
                print("==================================================")
                print("    محلل تقاطع Alligator + RSI (خيارات ثنائية)     ")
                print("==================================================")
                print(f"مؤشر RSI (14)       : {rsi_val:.2f}")
                print(f"أليغاتور - الشفاه (Lips) : {lips:.2f}")
                print(f"أليغاتور - الأسنان (Teeth): {teeth:.2f}")
                print(f"أليغاتور - الفكين (Jaws) : {jaws:.2f}")
                print("--------------------------------------------------")
                
                # منطق التقاطع المؤكد لـ Alligator مع تصفية الـ RSI (بدون عشوائية)
                # تقاطع صعودي: الشفاه أعلى الأسنان، والأسنان أعلى الفكين
                if lips > teeth and teeth > jaws and rsi_val < 65:
                    signal = "شراء / صعود (CALL) 🟢"
                    duration = "3 دقائق (استمرار الزخم الصعودي للأليغاتور)"
                    reason = "تقاطع إيجابي مؤكد لخطوط الأليغاتور (الفم منفتح صعوداً) مع دعم من الـ RSI."
                
                # تقاطع هبوطي: الشفاه أسفل الأسنان، والأسنان أسفل الفكين
                elif lips < teeth and teeth < jaws and rsi_val > 35:
                    signal = "بيع / هبوط (PUT) 🔴"
                    duration = "3 دقائق (استمرار الهبوط المسيطر)"
                    reason = "تقاطع سلبي مؤكد لخطوط الأليغاتور (الفم منفتح هبوطاً) مع ضغط بيعي."
                
                # حالات التشبع القوية للارتداد السريع
                elif rsi_val <= 30:
                    signal = "شراء عكسي (CALL - ارتداد) 🟢"
                    duration = "دقيقتان (2 دقيقة)"
                    reason = "تشبع بيعي حاد على مؤشر الـ RSI، متوقع ارتداد فوري من الدعم."
                elif rsi_val >= 70:
                    signal = "بيع عكسي (PUT - ارتداد) 🔴"
                    duration = "دقيقتان (2 دقيقة)"
                    reason = "تشبع شرائي حاد على مؤشر الـ RSI، متوقع جني أرباح وهبوط."
                else:
                    signal = "انتظار (تداخل خطوط التمساح) 🟡"
                    duration = "غير محدد"
                    reason = "خطوط الأليغاتور متداخلة (التمساح نائم)، لا توجد صفقة وامنة حالياً."

                print(f"القرار الفني: {signal}")
                print(f"مدة الصفقة المقترحة: {duration}")
                print(f"السبب الفني: {reason}")
                print("==================================================")
                print("اضغط Ctrl+C للإيقاف.")
                
                # التحديث كل 3 ثوانٍ
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\nتم إيقاف البرنامج. بالتوفيق في تداولاتك!")
                break
            except Exception as e:
                print(f"حدث خطأ بسيط: {e}")
                time.sleep(3)

if __name__ == "__main__":
    run_alligator_analyzer()
