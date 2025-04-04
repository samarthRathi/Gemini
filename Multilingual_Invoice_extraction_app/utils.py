import pandas as pd
from io import BytesIO
from docx import Document

def convert_to_excel(text):
    lines = [line for line in text.split("\n") if ":" in line]
    data = [line.split(":", 1) for line in lines]
    df = pd.DataFrame(data, columns=["Field", "Value"])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def convert_to_word(text):
    doc = Document()
    doc.add_heading("Extracted Data", level=1)
    for line in text.split("\n"):
        doc.add_paragraph(line)
    word_output = BytesIO()
    doc.save(word_output)
    word_output.seek(0)
    return word_output
