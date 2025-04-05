import os
import google.generativeai as genai

class GeminiVisionApp:
    def __init__(self, task_name="image understanding", model_name="gemini-1.5-flash"):
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
        Your job is to analyze the uploaded image and/or text and provide meaningful insights or structured outputs.
        If the image is blurry or incomplete, do your best. Keep your responses concise and relevant to the task.
        """

    def format_image(self, uploaded_file):
        if uploaded_file:
            return [{
                "mime_type": uploaded_file.type,
                "data": uploaded_file.getvalue()
            }]
        return [None]

    def validate_image(self, image_parts):
        check_prompt = f"Is this image relevant to the task of {self.task_name}? Just answer Yes or No."
        response = self.model.generate_content([check_prompt, image_parts[0]])
        return "yes" in response.text.strip().lower()

    def generate_response(self, user_input, image_parts):
        prompt_chain = [self.default_prompt]
        if user_input:
            prompt_chain.append(user_input)
        if image_parts[0]:
            prompt_chain.append(image_parts[0])
        response = self.model.generate_content(prompt_chain)
        return response.text if hasattr(response, 'text') else str(response)

    def moderate_response(self, text):
        moderation_prompt = """
        Does the following content contain any unethical, harmful, offensive, or sensitive information?
        Just answer Yes or No.
        """
        response = self.model.generate_content([moderation_prompt, text])
        return "yes" in response.text.strip().lower()