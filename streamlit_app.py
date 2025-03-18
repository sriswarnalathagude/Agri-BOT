import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os

# Set API Key
genai.configure(api_key=st.secrets["api_key"])

# Streamlit UI
st.set_page_config(page_title="AI Agriculture Bot", layout="wide")  # Enable wide layout

# Custom CSS for UI Enhancements
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #2E8B57;
        }
        .sub-title {
            font-size: 24px;
            font-weight: bold;
            color: #228B22;
        }
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #32CD32, #008000);
            color: white;
            font-size: 16px;
            padding: 10px;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #228B22, #006400);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>🌱 AI Agriculture Bot</h1>", unsafe_allow_html=True)

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["🌟 Features", "🩺 Diagnose", "📜 Summary", "💊 Medical Assistance"])

gemini_models = [
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-pro-exp-02-05"
]
model_name = st.sidebar.selectbox("Select AI Model:", gemini_models)

# Local Storage Paths
IMAGE_SAVE_PATH = "saved_images/"
REPORT_SAVE_PATH = "saved_reports/"
os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)
os.makedirs(REPORT_SAVE_PATH, exist_ok=True)


# Save Image Function
def save_image(image, filename):
    image_path = os.path.join(IMAGE_SAVE_PATH, filename)
    image.save(image_path)
    return image_path


# Save AI Diagnosis Report
def save_report(report_text, filename="diagnosis_report.txt"):
    report_path = os.path.join(REPORT_SAVE_PATH, filename)
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)
    return report_path


# Load AI Diagnosis Report
def load_report(filename="diagnosis_report.txt"):
    report_path = os.path.join(REPORT_SAVE_PATH, filename)
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as file:
            return file.read()
    return None


if menu == "🌟 Features":
    st.markdown("<h2 class='sub-title'>Features of Agriculture Bot</h2>", unsafe_allow_html=True)
    features = [
        "🌱 AI-powered plant disease detection",
        "⚡ Multi-model support (Gemini AI)",
        "📸 Instant image upload & analysis",
        "💊 Medical assistance & treatment suggestions"
    ]
    for feature in features:
        st.markdown(f"✅ {feature}")

elif menu == "🩺 Diagnose":
    st.markdown("<h2 class='sub-title'>AI Diagnosis</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload a plant image", type=["jpg", "jpeg", "png"])
        prompt = st.text_area("Enter query:", "Analyze this plant image for diseases and suggest treatments.")
        analyze_button = st.button("🔍 Analyze Plant Image")

    with col2:
        if uploaded_file:
            image = Image.open(uploaded_file)
            image_path = save_image(image, uploaded_file.name)
            st.image(image, caption="Uploaded Plant Image", use_container_width=True)

            if analyze_button:
                img_byte_array = io.BytesIO()
                image.save(img_byte_array, format='PNG')
                img_byte_array = img_byte_array.getvalue()
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_byte_array}])

                diagnosis_report = response.text
                st.markdown("<h3 class='sub-title'>🧬 AI Diagnosis Report</h3>", unsafe_allow_html=True)
                st.write(diagnosis_report)

                # Save diagnosis report
                save_report(diagnosis_report)

elif menu == "📜 Summary":
    st.markdown("<h2 class='sub-title'>📝 Diagnosis Summary</h2>", unsafe_allow_html=True)

    saved_report = load_report()
    if saved_report:
        summary_prompt = f"Summarize the following plant disease diagnosis:\n\n{saved_report}"
        if st.button("📑 Generate Summary"):
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(summary_prompt)
            st.write(response.text)
    else:
        st.warning("No previous diagnosis report found. Please perform a diagnosis first.")

elif menu == "💊 Medical Assistance":
    st.markdown("<h2 class='sub-title'>💊 Medical Assistance & Treatment</h2>", unsafe_allow_html=True)

    saved_report = load_report()
    if saved_report:
        medical_prompt = f"Based on the following diagnosis, suggest treatments and preventive measures:\n\n{saved_report}"
        if st.button("🩺 Get Medical Assistance"):
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(medical_prompt)
            st.write(response.text)
    else:
        st.warning("No previous diagnosis report found. Please perform a diagnosis first.")
