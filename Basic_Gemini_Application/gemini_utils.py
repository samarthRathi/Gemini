import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Models
text_model = genai.GenerativeModel("gemini-1.5-pro-002")
vision_model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(user_input, image_data=None):
    model = vision_model if image_data else text_model
    parts = [user_input, image_data] if image_data and user_input else [image_data or user_input]

    # Just stream the actual content — no token tracking
    stream = model.generate_content(parts, stream=True)
    for chunk in stream:
        if chunk.text:
            yield chunk.text

