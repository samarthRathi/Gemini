# 📚 Multi PDF Document Chatbot using Gemini + LangChain

## 🔍 Overview
This is a Streamlit-based web application that allows users to upload multiple PDF documents, process them into vector embeddings using Google's Gemini API and LangChain, and then interact with the content via natural language queries. The app uses a Retrieval-Augmented Generation (RAG) approach under the hood, making it an excellent beginner-friendly example for exploring RAG architectures.

## 🚀 Features
- Upload multiple PDF documents
- Extract and chunk text from PDFs
- Embed content using Google Generative AI embeddings
- Store embeddings locally with FAISS
- Ask questions in natural language and receive answers with Gemini 1.5 Flash
- Light/Dark theme toggle for user experience
- Typing animation for AI responses

## 🧰 Tech Stack
- Python
- Streamlit
- LangChain
- Google Generative AI (Gemini)
- FAISS (for vector storage)
- PyPDF2 (for PDF parsing)
- dotenv (for environment variable management)

## 📦 Installation
```bash
git clone https://github.com/samarthRathi/pdf-chatbot-gemini.git
cd pdf-chatbot-gemini
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Environment Setup
Create a `.env` file in the root directory and add your API key:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

## 🧪 How It Works
1. PDFs are read and text is extracted using `PyPDF2`.
2. The text is chunked using LangChain's `RecursiveCharacterTextSplitter`.
3. Each chunk is embedded using `GoogleGenerativeAIEmbeddings`.
4. FAISS is used to store and later retrieve similar chunks.
5. The user inputs a question, which is matched against relevant chunks.
6. The Gemini model (`gemini-1.5-flash`) is used to generate an answer using those chunks as context.

## 🖥️ Usage
```bash
streamlit run app.py
```
1. Upload PDFs from the sidebar
2. Click "Process PDFs"
3. Ask questions in the main input field

## 📂 File Structure
```
.
├── app.py               # Main Streamlit application
├── .env                 # Environment variables
├── faiss_index/         # Folder to store FAISS vector index
├── requirements.txt     # Python dependencies
```

## 📝 To-Do (Future Enhancements)
- Show retrieved context alongside answers
- Add support for markdown, table, or JSON formatting in answers
- Enable chat history and export
- Add RAG enhancements using LangChain's `RetrievalQA`

## 🙋‍♂️ Author
Built by Samarth Rathi — Learning RAG with Gemini and LangChain.

---
**Note**: You must have access to Google's Generative AI APIs to run this project.
