import pandas as pd
from io import BytesIO
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from docx import Document
import re
import json
import os
from datetime import datetime

session_logs = {}

def clean_text(text):
    return re.sub(r"[*_`\[\]]", "", text).strip()

def censor_text(text):
    flagged_words = ["fraud", "violence", "abuse", "drugs"]
    for word in flagged_words:
        text = re.sub(fr"\b{word}\b", "[REDACTED]", text, flags=re.IGNORECASE)
    return text

def convert_to_excel(text):
    lines = [line for line in text.split("\n") if ":" in line]
    data = [line.split(":", 1) for line in lines]
    cleaned_data = [[clean_text(k), clean_text(v)] for k, v in data]
    df = pd.DataFrame(cleaned_data, columns=["Field", "Value"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracted Data"
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            cell.font = Font(name='Calibri', bold=False, italic=False)
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def convert_to_word(text):
    doc = Document()
    doc.add_heading("Extracted Data", level=1)
    for line in text.split("\n"):
        doc.add_paragraph(clean_text(line))
    word_output = BytesIO()
    doc.save(word_output)
    word_output.seek(0)
    return word_output

def start_session_log(user_id):
    session_logs[user_id] = {
        "session_start": datetime.now().isoformat(),
        "user_id": user_id,
        "interactions": []
    }

def add_session_interaction(user_id, prompt, image_name, response, unethical):
    session_logs[user_id]["interactions"].append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "image_name": image_name,
        "response_summary": response[:300],
        "flagged_unethical": unethical
    })

def end_session_log(user_id):
    session_logs[user_id]["session_end"] = datetime.now().isoformat()
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"{user_id}_session_log.json")
    with open(log_path, "w") as f:
        json.dump(session_logs[user_id], f, indent=2)


def verify_user(username, password):
    valid_users = {
        "testuser123": "123456"
    }
    return valid_users.get(username) == password