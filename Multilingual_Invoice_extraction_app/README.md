# 🧠 Gemini Vision - Document Scanning Task Assistant

A user-friendly Streamlit application powered by **Google's Gemini Vision (Gemini 1.5 Flash)** that enables you to upload images and extract meaningful, structured information based on a custom-defined task — like invoice parsing, table extraction, or general document analysis.

## 🚀 Features

- ✅ Define your own assistant role (e.g., invoice parser, table analyzer)
- ✅ Upload an image (PNG, JPG, JPEG)
- ✅ Provide a natural language prompt describing what you want
- ✅ Uses **Google Gemini Vision** for multimodal content understanding
- ✅ Smart prompt engineering with a dynamic default system prompt
- ✅ Result displayed in a **modal popup**
- ✅ Download extracted content as:
  - 📥 Excel (.xlsx)
  - 📥 Word (.docx)
- ✅ Non-refreshing export options for better UX

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Google Generative AI (Gemini)](https://makersuite.google.com/app) — LLM engine
- [Python-Docx](https://python-docx.readthedocs.io/) — Word export
- [Pandas + OpenPyXL](https://pandas.pydata.org/) — Excel export

---

## 🖼️ How It Works

1. The user provides a **task description** (e.g., “act as an invoice parser”).
2. Uploads a relevant image (e.g., a scanned invoice).
3. Types a **prompt** (e.g., “extract invoice number and total”).
4. Gemini generates a response using a pre-configured **system prompt + user prompt + image**.
5. The result is shown in a **modal** popup with export options.

## 📝 Example Use Cases
1. Invoice summarization

2. Resume screening

3. Form data extraction

4. Table parsing

5. Product label reading

6. Image captioning and QA

## 💡 Tips
**Use high-quality images for better results.**

**Be clear and concise in your task prompt.**

**You can define any domain-specific role — Gemini will adapt accordingly.**