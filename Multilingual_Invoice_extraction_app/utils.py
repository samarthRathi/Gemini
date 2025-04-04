import pandas as pd
from io import BytesIO
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
import re

def clean_text(text):
    # """Remove markdown symbols like *, _, etc."""
    return re.sub(r"[*_`]", "", text).strip()

def convert_to_excel(text):
    # Extract key-value pairs
    lines = [line for line in text.split("\n") if ":" in line]
    data = [line.split(":", 1) for line in lines]
    cleaned_data = [[clean_text(k), clean_text(v)] for k, v in data]

    df = pd.DataFrame(cleaned_data, columns=["Field", "Value"])

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracted Data"

    # Write data to sheet
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            # Set font to Calibri, not bold or italic
            cell.font = Font(name='Calibri', bold=False, italic=False)

    # Save to BytesIO for download
    output = BytesIO()
    wb.save(output)
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
