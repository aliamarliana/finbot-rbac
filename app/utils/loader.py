import os
import pandas as pd

BASE_PATH = "resources/data"


def load_markdown_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_csv_file(path: str) -> str:
    df = pd.read_csv(path)
    return df.to_csv(index=False)


def load_all_documents():
    documents = {}

    for department in os.listdir(BASE_PATH):
        dept_path = os.path.join(BASE_PATH, department)
        if not os.path.isdir(dept_path):
            continue

        documents[department] = []

        for file in os.listdir(dept_path):
            file_path = os.path.join(dept_path, file)

            if file.endswith(".md"):
                text = load_markdown_file(file_path)
                documents[department].append(
                    {"source": file, "content": text}
                )

            elif file.endswith(".csv"):
                text = load_csv_file(file_path)
                documents[department].append(
                    {"source": file, "content": text}
                )

    print("Loaded documents:", {k: len(v) for k, v in documents.items()})
    return documents
