import streamlit as st
import hashlib
import time

# إعدادات الصفحة
st.set_page_config(page_title="استراتيجية القمة والقاع - السكالبينغ", page_icon="⚡", layout="centered")

# تنسيق الواجهة
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .status-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
    }
    .timer-box {
        background-color: #1f2937;
        border: 2px solid #3b82f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #60a5fa;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ مستشار السكالبينغ (قمة/قاع 15 ثانية)")
st.caption("نظام التنبيه المسبق والدخول الدقيق للشمعة رقم 21")

st.divider()

# المدخلات
st.subheader("📌 معطيات التحليل")

trend_type = st.radio("نوع نقطة بداية العد (الشمعة 1):", ["من أعلى قمة (Top High)", "من أدنى قاع (Bottom Low)"], horizontal=True)

candle_15_color = st.selectbox(
    "اتجاه/لون الشمعة رقم 15 المكتملة:",
    ["هبوط (حمراء - Red)", "صعود (خضراء - Green)", "ضعيفة / غير واضحة (Doji)"]
)

balance = st.number_input("رأس المال في الحساب ($):", min_value=10.0, value=100.0, step=10.0)

if st.button("🚀 بدء التحليل والعد التنازلي", use_container_width=True):
    
    # حساب نسبة المخاطرة (3%)
    trade_amount = round(balance * 0.03, 2)
    
    # تحليلات الاستراتيجية
    if "ضعيفة" in candle_15_color:
        st.warning("⚠️ السوق غير مستقر (شمعة دوجي/ضعيفة). يُنصح بالانتظار وعدم التداول الآن لحماية حسابك.")
    else:
        # تحديد اتجاه التوصية بناءً على الشمعة 15
        if "هبوط" in candle_15_color:
            direction = "PUT (هبوط/أسفل) 🔻"
            color_code = "#ef4444"
        else:
            direction = "CALL (صعود/أعلى) 🟢"
            color_code = "#10b981"

        st.info("🔄 جاري مزامنة التوقيت وحساب زمن الوصول للشمعة رقم 21...")
        
        # إنشاء مكان للعد التنازلي
        timer_placeholder = st.empty()
        
        # العد التنازلي (90 ثانية - الوقت المتبقي لافتتاح الشمعة 21)
        # 15s x 6 شموع = 90 ثانية
        total_seconds = 90 
        
        for remaining in range(total_seconds, 0, -1):
            timer_placeholder.markdown(f"""
            <div class="timer-box">
                ⏱️ جهّز نفسك في Pocket Option<br>
                الصفقة القادمة: <span style="color: {color_code};">{direction}</span><br>
                متبقي على نقطة الدخول: <span style="color: #f59e0b;">{remaining} ثانية</span>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            
        # إشارة الدخول المباشرة فور انتهاء العد التنازلي
        timer_placeholder.markdown(f"""
        <div class="status-card" style="background-color: {color_code}; color: white; font-size: 26px;">
            🚨 ادخل الصفقة الآن فوراً! 🚨<br><br>
            الاتجاه: <b>{direction}</b><br>
            مدة الصفقة: <b>30 ثانية</b><br>
            حجم الصفقة المقترح (3%): <b>${trade_amount}</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ تم إرسال إشارة الدخول. يرجى التنفيذ فوراً عند فتح الشمعة!")
