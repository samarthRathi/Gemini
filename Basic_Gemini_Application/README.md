# 🧠 Gemini Chat & Vision App

This is a Streamlit-based AI assistant that uses Google's **Gemini models** (via the `google.generativeai` API). It supports:
- Text-only queries
- Image-only queries
- Combined text + image input
- Real-time response streaming
- Markdown or plain text output
- Chat history tracking
- Model information viewer

---

## 🚀 Features

✅ Choose between **Text Only**, **Text + Image**, or **Image Only** interaction modes  
✅ Upload and preview images directly in the app  
✅ Live streamed responses from Gemini models  
✅ Switch between **Markdown** or **Plain Text** output  
✅ Sidebar model info viewer (auto-loaded from Gemini API)  
✅ Full chat history with Q&A, image previews, and responses  
✅ Clean modular code split into 3 reusable files

---

## 🧩 File Structure
gemini_app/ 

app.py # Main Streamlit interface 

gemini_utils.py # Gemini model setup and API interaction 

ui_utils.py # UI elements: text input, image upload


---

## 🔐 Setup

1. **Clone the repo**

bash
git clone https://github.com/your-username/gemini-chat-app.git
cd gemini-chat-app

2. **Install dependencies**
pip install -r requirements.txt
Make sure you have Python 3.9 or higher.

3. **Create .env file**

GOOGLE_API_KEY=your_google_api_key_here
You can get your key from Google AI Studio.

4. **Run the app**
streamlit run app.py

⚙️ Built With
Streamlit — for UI

Google Generative AI (Gemini) — for LLM responses

Python — core logic

Pillow — image handling


✅ Future Improvements
 Model selector for live model switching

 Token usage stats (input/output token count)

 Export chat history (Markdown or text)

 Multi-turn conversations (chat-style memory)



🙋‍♂️ Author
@samarthRathi
Built as a learning + experimentation project to explore Google's Gemini models in real-world usage.

