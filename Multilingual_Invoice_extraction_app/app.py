from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# ----------------------------------------
# 🎯 Gemini Vision App Class
# ----------------------------------------

class GeminiVisionApp:
    def __init__(self, task_name="invoice extraction", model_name="gemini-1.5-flash"):
        self.task_name = task_name
        self.model_name = model_name
        self.model = self.configure_model()
        self.default_prompt = self.get_default_prompt()

    def configure_model(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_name=self.model_name)

    def get_default_prompt(self):
        return f"""
        You are an expert in {self.task_name}.
        Your job is to extract key structured information from the uploaded image and respond in a clean, clear, and useful format.
        Only respond with data that can be interpreted from the image. If the image is blurry or irrelevant, say so clearly.
        """

    def format_image(self, uploaded_file):
        if uploaded_file:
            return [{
                "mime_type": uploaded_file.type,
                "data": uploaded_file.getvalue()
            }]
        return [None]

    def validate_image(self, image_parts):
        check_prompt = f"Is this image relevant to {self.task_name}? Just answer Yes or No."
        response = self.model.generate_content([check_prompt, image_parts[0]])
        return "yes" in response.text.strip().lower()

    def generate_response(self, user_prompt, image_parts):
        prompt_chain = [self.default_prompt]

        if user_prompt:
            prompt_chain.append(user_prompt)
        if image_parts[0]:
            prompt_chain.append(image_parts[0])

        response = self.model.generate_content(prompt_chain)
        return response.text

# ----------------------------------------
# 🖼️ Streamlit UI
# ----------------------------------------

st.set_page_config(page_title="Gemini Vision App", page_icon="🧠", layout="centered")
st.title("🧠 Document Extraction Assistant")

# Initialize app (default task is invoice extraction)
app = GeminiVisionApp()

# Input: One prompt + one image
st.header("Upload Image and Describe What You Need")
user_prompt = st.text_area("What would you like me to extract or summarize from the image?", height=100)
uploaded_image = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# Show image preview
if uploaded_image:
    if st.checkbox("Show uploaded image", value=True):
        st.image(Image.open(uploaded_image), caption="Uploaded Image", use_column_width=True)

# Submit
if st.button("Submit"):
    if not uploaded_image and not user_prompt:
        st.warning("Please provide a prompt or upload an image.")
    else:
        image_data = app.format_image(uploaded_image)

        if uploaded_image and not app.validate_image(image_data):
            st.error("🚫 The uploaded image does not appear relevant to the task. Please upload a valid document.")
        else:
            with st.spinner("Generating response with Gemini..."):
                result = app.generate_response(user_prompt, image_data)
            st.subheader("💡 Gemini's Response")
            st.write(result)
