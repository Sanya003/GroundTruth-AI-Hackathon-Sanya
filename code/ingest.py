import pandas as pd
import sqlite3, pdfplumber
import os

def load_files(paths):
    dfs, pdf_texts = [], []

    if isinstance(paths, str):
        paths = [paths]

    for p in paths:
        ext = os.path.splitext(p)[1].lower()

        if ext in [".csv"]:
            dfs.append(pd.read_csv(p))

        elif ext in [".xls", ".xlsx"]:
            dfs.append(pd.read_excel(p))

        elif ext in [".sqlite", ".db"]:
            conn = sqlite3.connect(p)
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)["name"]
            for t in tables:
                dfs.append(pd.read_sql(f"SELECT * FROM {t}", conn))
            conn.close()

        elif ext == ".pdf":
            text = ""
            with pdfplumber.open(p) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            pdf_texts.append(text)

        else:
            print(f"Unsupported file format: {p}")

    return dfs, pdf_texts
