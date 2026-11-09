import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Option Analyzer", page_icon="📈")

st.title("📈 محلل صفقات بوكت أوبشن")
st.write("برنامج البحث التلقائي الذكي للنماذج المتاحة.")

api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
uploaded_file = st.file_uploader("اختر صورة الشارت:", type=["jpg", "jpeg", "png"])

if api_key and uploaded_file:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption="الشارت المرفوع", use_column_width=True)
    
    if st.button("🚀 تحليل الشارت الآن"):
        with st.spinner("جاري فحص النماذج المتاحة في حسابك والتحليل..."):
            try:
                # جلب النماذج المتاحة وتجنب أي اسم ثابت قديم
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not available_models:
                    st.error("❌ لا توجد نماذج متاحة مرتبطة بهذا المفتاح.")
                else:
                    # اختيار أول نموذج متاح تلقائياً
                    selected_model_name = available_models[0]
                    model = genai.GenerativeModel(selected_model_name)
                    
                    response = model.generate_content([
                        "أنت خبير تداول في منصة بوكت أوبشن. قم بتحليل هذا الشارت بدقة وأعطني:\n1. التوصية: (CALL صعوداً أو PUT هبوطاً)\n2. مدة الصفقة المقترحة\n3. السبب باختصار.",
                        image
                    ])
                    
                    st.success(f"✅ تم التحليل بنجاح باستخدام النموذج: {selected_model_name}")
                    st.markdown("### 📊 نتيجة التحليل:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
