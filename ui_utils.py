import streamlit as st
from PIL import Image

def user_input_form():
    return st.text_input("Enter your question or prompt:")

def image_uploader():
    uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Remove Image"):
            st.experimental_rerun()
        return image
    return None
