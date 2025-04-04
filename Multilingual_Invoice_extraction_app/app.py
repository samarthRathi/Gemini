from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
from gemini_core import GeminiVisionApp
from utils import convert_to_excel, convert_to_word

# Page setup
st.set_page_config(page_title="Gemini Vision App", page_icon="🧠", layout="centered")
st.title("🧠 Gemini Vision Task Assistant")

# Task input
st.header("1. Define Your Assistant")
user_task_name = st.text_input("Who should the model act as? (e.g., invoice parser, form analyzer):")

if "result" not in st.session_state:
    st.session_state.result = None

if user_task_name:
    app = GeminiVisionApp(task_name=user_task_name)

    st.header("2. Upload Image and Describe Your Task")
    user_input = st.text_area("What would you like me to do with the image?")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_image and st.checkbox("Show uploaded image", value=True):
        st.image(Image.open(uploaded_image), caption="Uploaded Image", use_column_width=True)

    if st.button("Submit"):
        if not uploaded_image and not user_input:
            st.warning("Please provide a prompt or upload an image.")
        else:
            image_data = app.format_image(uploaded_image)

            if uploaded_image and not app.validate_image(image_data):
                st.error("🚫 The uploaded image is not relevant to the task.")
            else:
                with st.spinner("Generating response with Gemini..."):
                    result = app.generate_response(user_input, image_data)
                    st.session_state.result = result

# Show results and export
if st.session_state.result:
    st.subheader("💡 Gemini's Response")
    st.write(st.session_state.result)

    export_format = st.radio("Export as:", ["None", "Excel (.xlsx)", "Word (.docx)"], horizontal=True)

    if export_format == "Excel (.xlsx)":
        file_data = convert_to_excel(st.session_state.result)
        st.download_button("📥 Download Excel", file_data, file_name="extracted_data.xlsx")

    elif export_format == "Word (.docx)":
        file_data = convert_to_word(st.session_state.result)
        st.download_button("📥 Download Word", file_data, file_name="extracted_data.docx")

else:
    if user_task_name:
        st.info("📝 Submit a prompt and image to generate a response.")
    else:
        st.info("👋 Please define the assistant role first.")
