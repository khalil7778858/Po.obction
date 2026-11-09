import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option Analyzer", page_icon="📈")

st.title("📈 محلل صفقات بوكت أوبشن السريع")

api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
uploaded_file = st.file_uploader("اختر صورة الشارت:", type=["jpg", "jpeg", "png"])

if api_key and uploaded_file:
    genai.configure(api_key=api_key)
    
    # تصغير حجم الصورة تلقائياً لتجنب التعليق والسرعة في المعالجة
    image = Image.open(uploaded_file)
    image.thumbnail((1024, 1024))
    
    st.image(image, caption="الشارت المرفوع", use_column_width=True)
    
    if st.button("🚀 تحليل فوري"):
        with st.spinner("⏳ جارٍ استخراج التوصية..."):
            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                response = model.generate_content([
                    "أنت خبير تداول بوكت أوبشن. حلل الشارت بدقة وأعطني باختصار شديد جداً:\n1. التوصية: (CALL صعوداً أو PUT هبوطاً)\n2. المدة المقترحة\n3. السبب باختصار.",
                    image
                ], request_options={'timeout': 15}) # حماية ضد التعليق
                
                st.success("✅ تمت العملية بنجاح!")
                st.markdown("### 📊 النتيجة:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أو انتهت مهلة الاتصال: {e}")
