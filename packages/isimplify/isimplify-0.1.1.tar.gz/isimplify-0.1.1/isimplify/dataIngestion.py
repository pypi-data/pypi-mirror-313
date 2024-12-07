import pandas as pd
from PyPDF2 import PdfReader

def readFile(file_path):
    print("---reading file---")
    if file_path.endswith('.pdf'):
        try:
            reader = PdfReader(file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return content.lower()
        except Exception as e:
            return f"Error reading PDF file: {e}"




