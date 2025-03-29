import streamlit as st
from gemini_utils import get_gemini_response
from ui_utils import user_input_form, image_uploader
import google.generativeai as genai

st.set_page_config(page_title="🧠 Gemini Chat & Vision")

st.title("💬 Chat with Gemini")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Gemini model info
st.sidebar.header("ℹ️ Gemini Models Available")

def get_available_models():
    models = genai.list_models()
    model_info = {}
    for model in models:
        name = model.name.split("/")[-1]
        description = getattr(model, "description", "No description available.")
        model_info[name] = description
    return model_info

models = get_available_models()
model_names = list(models.keys())
selected_model = st.sidebar.selectbox("Select a model to view info:", model_names)

if selected_model:
    st.sidebar.info(f"**{selected_model}**\n\n{models[selected_model]}")

# --- Mode selection ---
st.subheader("Select Usage Mode")
mode = st.radio("How would you like to interact with Gemini?", ["Text Only", "Text + Image", "Image Only"])

# --- Response format selection ---
render_mode = st.radio("Response format:", ["Formatted (Markdown)", "Plain Text"], horizontal=True)

st.markdown("---")

# --- Inputs ---
user_text = ""
image_data = None

if mode == "Text Only":
    user_text = user_input_form()

elif mode == "Text + Image":
    user_text = user_input_form()
    image_data = image_uploader()

elif mode == "Image Only":
    image_data = image_uploader()

# --- Submit and stream response ---
button_label = "Submit"
if mode == "Image Only":
    button_label = "Tell me about this image"

if st.button(button_label):
    if mode == "Text Only" and not user_text:
        st.warning("Please enter a prompt.")
    elif mode == "Text + Image" and not (user_text or image_data):
        st.warning("Please enter a prompt or upload an image.")
    elif mode == "Image Only" and not image_data:
        st.warning("Please upload an image.")
    else:
        with st.spinner("Thinking..."):
            st.subheader("Response:")
            response_placeholder = st.empty()
            response_text = ""

            for chunk in get_gemini_response(user_text, image_data):
                response_text += chunk
                if render_mode == "Formatted (Markdown)":
                    response_placeholder.markdown(response_text)
                else:
                    response_placeholder.text(response_text)

            # Save chat
            st.session_state.chat_history.append({
                "question": user_text,
                "image": image_data,
                "response": response_text
            })

# --- Chat history ---
st.markdown("---")
st.subheader("🕘 Chat History")

for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
    st.markdown(f"**Q{i}:** {chat['question']}")
    if chat['image']:
        st.image(chat['image'], width=200, caption="Uploaded Image")
    st.markdown(f"**A{i}:**\n{chat['response']}")
    st.markdown("---")
