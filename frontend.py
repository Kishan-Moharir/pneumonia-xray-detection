import streamlit as st
import requests
from PIL import Image
from datetime import datetime

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Pneumonia Detection System",
    page_icon="🫁",
    layout="centered"
)

# ---------------- Session State ----------------
if "result" not in st.session_state:
    st.session_state.result = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False

# ---------------- Modern Vibrant UI (CSS) ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e3f2fd, #f1f8e9);
}
.main {
    background-color: white;
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
}
.title-text {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #0d47a1;
}
.subtitle-text {
    text-align: center;
    font-size: 16px;
    color: #546e7a;
}
.card {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    padding: 22px;
    border-radius: 16px;
    border-left: 8px solid #1976d2;
    margin-top: 25px;
}
.solution {
    background: linear-gradient(135deg, #e8f5e9, #ffffff);
    padding: 22px;
    border-radius: 16px;
    border-left: 8px solid #2e7d32;
    margin-top: 25px;
}
.stButton>button {
    background: linear-gradient(90deg, #1976d2, #42a5f5);
    color: white;
    border-radius: 30px;
    padding: 10px 25px;
    font-size: 16px;
    font-weight: 600;
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #607d8b;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<div class='title-text'>🫁 Pneumonia Detection System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>AI-powered Chest X-ray Analysis & Health Guidance</div>", unsafe_allow_html=True)
st.divider()

st.info(
    "📌 Upload a chest X-ray image to analyze lung condition.\n\n"
    "⚠️ This system is for educational purposes only."
)

# ---------------- Upload ----------------
uploaded_file = st.file_uploader(
    "📤 Upload Chest X-ray Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.subheader("🖼 Uploaded X-ray Image")
    st.image(image, use_column_width=True)

    if st.button("🔍 Analyze X-ray"):
        with st.spinner("Analyzing X-ray using AI model..."):
            response = requests.post(
                "http://127.0.0.1:5000/predict",
                files={"file": uploaded_file.getvalue()}
            )

        if response.status_code == 200:
            data = response.json()
            st.session_state.result = data["result"]
            st.session_state.confidence = data["confidence"]
            st.session_state.show_solution = False

# ---------------- Result ----------------
if st.session_state.result:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Analysis Result")

    if st.session_state.result.lower().startswith("pneumonia"):
        st.error("⚠️ Pneumonia Detected")
        if st.session_state.confidence > 85:
            risk = "High"
        elif st.session_state.confidence > 65:
            risk = "Medium"
        else:
            risk = "Low"
        st.markdown(f"**Risk Level:** {risk}")
    else:
        st.success("✅ Normal (No Pneumonia Detected)")
        risk = "None"

    st.progress(st.session_state.confidence / 100)
    st.markdown(f"**Confidence Score:** `{st.session_state.confidence}%`")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💡 View Suggested Care & Guidance"):
            st.session_state.show_solution = True

    # ---------------- Report Generation ----------------
    report_text = f"""
PNEUMONIA DETECTION REPORT
-------------------------
Date & Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

Analysis Result: {st.session_state.result}
Confidence Score: {st.session_state.confidence}%
Risk Level: {risk}

Suggested Guidance:
"""
    if st.session_state.result.lower().startswith("pneumonia"):
        report_text += """
- Consult a qualified medical professional
- Follow prescribed medication
- Ensure rest and hydration
- Monitor breathing and oxygen levels
"""
    else:
        report_text += """
- Maintain healthy lifestyle
- Regular exercise and diet
- Periodic medical checkups
"""

    report_text += "\nDisclaimer: This report is for educational purposes only."

    with col2:
        st.download_button(
            label="⬇️ Download Medical Report",
            data=report_text,
            file_name="pneumonia_analysis_report.txt",
            mime="text/plain"
        )

# ---------------- Solution ----------------
if st.session_state.show_solution:
    st.markdown("<div class='solution'>", unsafe_allow_html=True)
    st.subheader("🩺 Suggested Care & Guidance")

    if st.session_state.result.lower().startswith("pneumonia"):
        st.markdown("""
        - Consult a medical professional
        - Complete prescribed medication
        - Proper rest & hydration
        - Avoid smoking
        """)
    else:
        st.markdown("""
        - Maintain good respiratory hygiene
        - Balanced diet & exercise
        """)

    st.warning("⚠️ This is not a medical diagnosis.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Footer ----------------
st.divider()
st.markdown(
    "<div class='footer'>Final Year B.Tech Project | Artificial Intelligence & Data Science</div>",
    unsafe_allow_html=True
)
