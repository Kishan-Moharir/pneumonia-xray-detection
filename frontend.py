import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Pneumonia Detection System",
    page_icon="🫁",
    layout="centered"
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background-color: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 20px;
}
h1 {
    color: #0f4c75;
    text-align: center;
}
.result-box {
    padding: 20px;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
}
.pneumonia {
    background-color: #ffcccc;
    color: #8b0000;
}
.normal {
    background-color: #ccffcc;
    color: #006400;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1>🫁 Pneumonia X-Ray Detection</h1>", unsafe_allow_html=True)
st.write("Upload a chest X-ray image to analyze for pneumonia.")

# -------------------- LOAD MODEL --------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("pneumonia_model.h5", compile=False)

model = load_model()

# -------------------- IMAGE UPLOAD --------------------
uploaded_file = st.file_uploader(
    "📤 Upload Chest X-ray Image",
    type=["jpg", "jpeg", "png"]
)

# -------------------- ANALYZE BUTTON --------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded X-ray", use_column_width=True)

    if st.button("🔍 Analyze X-Ray"):
        # Preprocess image
        img = image.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)[0][0]
        confidence = float(prediction) * 100

        if prediction > 0.5:
            result = "Pneumonia Detected"
            css_class = "pneumonia"
            suggestions = """
            • Consult a physician immediately  
            • Antibiotics or antivirals may be required  
            • Take adequate rest and fluids  
            • Avoid smoking and pollution  
            """
        else:
            result = "Normal"
            css_class = "normal"
            suggestions = """
            • No pneumonia detected  
            • Maintain good respiratory hygiene  
            • Eat healthy and exercise regularly  
            """

        st.markdown(
            f"<div class='result-box {css_class}'>"
            f"{result}<br>Confidence: {confidence:.2f}%</div>",
            unsafe_allow_html=True
        )

        # -------------------- SUGGESTIONS BUTTON --------------------
        with st.expander("💡 View Medical Suggestions"):
            st.markdown(suggestions)

        # -------------------- DOWNLOAD REPORT --------------------
        report = f"""
PNEUMONIA X-RAY DETECTION REPORT
--------------------------------
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Result: {result}
Confidence: {confidence:.2f}%

Suggestions:
{suggestions}
"""

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="pneumonia_report.txt",
            mime="text/plain"
        )
