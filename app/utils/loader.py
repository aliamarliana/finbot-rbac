# app/utils/loader.py
import os
import pandas as pd

BASE_PATH = "resources/data"
VALID_MARKDOWN = (".md", ".markdown", ".txt")
VALID_CSV = (".csv",)

def load_markdown_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_csv_file(path: str) -> str:
    df = pd.read_csv(path)
    # Limit rows to 1000 for safety
    if len(df) > 1000:
        df = df.head(1000)
    rows = []
    for i, r in df.iterrows():
        rows.append(", ".join([f"{c}: {str(r[c])}" for c in df.columns]))
    return "\n".join(rows)

def discover_documents():
    """
    Returns list of dicts:
    [
      {"department": "finance", "source": "file.md", "content": "..."},
      ...
    ]
    """
    documents = []
    if not os.path.isdir(BASE_PATH):
        raise FileNotFoundError(f"{BASE_PATH} not found. Ensure dataset is present.")

    for dept in sorted(os.listdir(BASE_PATH)):
        dept_path = os.path.join(BASE_PATH, dept)
        if not os.path.isdir(dept_path):
            continue
        for fname in sorted(os.listdir(dept_path)):
            fpath = os.path.join(dept_path, fname)
            if fname.lower().endswith(VALID_MARKDOWN):
                content = load_markdown_file(fpath)
            elif fname.lower().endswith(VALID_CSV):
                content = load_csv_file(fpath)
            else:
                # skip unknown file types
                continue
            documents.append({
                "department": dept,
                "source": fname,
                "content": content
            })
    return documents
