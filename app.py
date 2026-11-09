import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option Analyzer", page_icon="📈")

st.title("📈 محلل صفقات بوكت أوبشن")
st.write("النسخة النهائية المستقرة.")

api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
uploaded_file = st.file_uploader("اختر صورة الشارت:", type=["jpg", "jpeg", "png"])

if api_key and uploaded_file:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت الآن"):
        with st.spinner("جاري التحليل..."):
            try:
                # استخدام النموذج المحدث الذي طلبه الخادم صراحة في رسالة الخطأ الأخيرة
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                response = model.generate_content([
                    "أنت خبير تداول في منصة بوكت أوبشن. قم بتحليل هذا الشارت بدقة وأعطني:\n1. التوصية: (CALL صعوداً أو PUT هبوطاً)\n2. مدة الصفقة المقترحة\n3. السبب باختصار.",
                    image
                ])
                
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("### 📊 نتيجة التحليل:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
