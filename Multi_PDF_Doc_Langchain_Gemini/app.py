import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_title="Multi PDF Document Chatbot", page_icon="📚")
# Theme toggle
theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])
if theme == "Light":
    st.markdown("<style>html { filter: invert(100%); background-color: black; }</style>", unsafe_allow_html=True)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text


def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000,
    )
    return text_splitter.split_text(text)


def get_vector_store(texts):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_chain():
    prompt_template = """
    You are a highly knowledgeable assistant that answers based only on the provided context.

    - Answer in a clear and structured way.
    - Do not make up answers if the context doesn't contain it.
    - Use bullet points where helpful.
    - Respond in the same language as the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(llm, chain_type="stuff", prompt=prompt)


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_chain()
    answer = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    # Typing effect
    placeholder = st.empty()
    typed = ""
    for char in answer["output_text"]:
        typed += char
        placeholder.markdown(f"**Reply:** {typed}▌")
        time.sleep(0.01)


def main():
    st.header("📚 Multi PDF Document Chatbot")

    user_question = st.text_input("Ask a question about the uploaded PDF documents:")
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.subheader("📤 Upload PDF Documents")
        pdf_docs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

        if st.button("Process PDFs"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF document.")
                return

            with st.spinner("Processing PDFs..."):
                text = get_pdf_text(pdf_docs)
                texts = split_text(text)
                get_vector_store(texts)
                st.success("PDF documents processed and vector store created!")


if __name__ == "__main__":
    main()
