import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="Pocket Option Analyzer", page_icon="📈")

st.markdown("<h2 style='text-align: center; color: #2E8B57;'>📈 محلل صفقات بوكت أوبشن النهائي</h2>", unsafe_allow_html=True)

api_key = st.text_input("🔑 أدخل مفتاح Gemini API Key:", type="password")
uploaded_file = st.file_uploader("📂 اختر صورة الشارت:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="الشارت المرفوع", use_column_width=True)

if st.button("🚀 تحليل الشارت الآن", type="primary"):
    if not api_key:
        st.error("⚠️ الرجاء إدخال مفتاح الـ API.")
    elif not uploaded_file:
        st.error("⚠️ الرجاء رفع صورة الشارت.")
    else:
        with st.spinner("⏳ جاري تحليل الشارت واستخراج التوصية بدقة..."):
            try:
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
                # استخدام أحدث مسار مباشر ومستقر تماماً لخوادم جوجل
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [
                            {
                                "text": (
                                    "أنت خبير تداول محترف في منصة بوكت أوبشن (Pocket Option). "
                                    "قم بتحليل الشارت المرفق بدقة متناهية وأعطني باختصار شديد:\n"
                                    "1. التوصية: (CALL لشراء صعوداً 🟢 أو PUT لبيع هبوطاً 🔴)\n"
                                    "2. مدة الصفقة المقترحة (مثلاً: دقيقة أو دقيقتان)\n"
                                    "3. السبب باختصار شديد."
                                )
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": img_str
                                }
                            }
                        ]
                    }]
                }
                
                response = requests.post(url, json=payload, headers=headers)
                result = response.json()
                
                if response.status_code == 200:
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ تمت عملية التحليل بنجاح!")
                    st.markdown("---")
                    st.markdown("### 📊 نتيجة التوصية:")
                    st.markdown(ai_text)
                else:
                    error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
                    st.error(f"❌ خطأ من الخادم: {error_msg}")
                    
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {e}")
