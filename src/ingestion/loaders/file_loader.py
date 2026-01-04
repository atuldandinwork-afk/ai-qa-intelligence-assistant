from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from pathlib import Path


def infer_doc_type(file_path: Path) -> str:
    name = file_path.name.lower()

    if "org_project_info" in name:
        return "project_info"
    if "test_case" in name:
        return "test_cases"
    if "defect" in name:
        return "defects"
    if "execution" in name:
        return "execution"
    if "automation" in name:
        return "automation"
    if any(k in name for k in ["concept", "kpi", "testing", "formula"]):
        return "knowledge"

    return "generic"


def load_file(file_path: Path):
    documents = []
    doc_type = infer_doc_type(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    suffix = file_path.suffix.lower()

    # -------------------------
    # Markdown / Text
    # -------------------------
    if suffix in [".md", ".txt"]:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        chunks = splitter.split_text(text)

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path.name,
                        "doc_type": doc_type,
                    },
                )
            )

    # -------------------------
    # CSV
    # -------------------------
    elif suffix == ".csv":
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            row_text = " | ".join(
                f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])
            )

            documents.append(
                Document(
                    page_content=row_text,
                    metadata={
                        "source": file_path.name,
                        "doc_type": doc_type,
                    },
                )
            )

    # -------------------------
    # JSON (safe fallback)
    # -------------------------
    elif suffix == ".json":
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        chunks = splitter.split_text(text)

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path.name,
                        "doc_type": doc_type,
                    },
                )
            )

    return documents


def load_documents_from_folder(folder_path):
    folder_path = Path(folder_path)
    all_docs = []

    for file_path in folder_path.rglob("*"):
        if file_path.suffix.lower() in [".md", ".txt", ".csv", ".json"]:
            all_docs.extend(load_file(file_path))

    return all_docs
