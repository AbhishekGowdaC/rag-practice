from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders  import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader
import pdfplumber
from langchain_core.documents import Document


def load_all_documents(data_dir: str) ->List[Any]:

    data_path = Path(data_dir).resolve()
    print(f"[DEBUG] Data path: {data_path}")
    documents = []

    pdf_files = list(data_path.glob('**/*.pdf'))

    print(f"[DEBUG] Found {len(pdf_files)} PDF files: {[str(f) for f in pdf_files]}")
    for pdf_file in pdf_files:
        print(f"[DEBUG] Loading PDF: {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} PDF docs from {pdf_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")


    text_files = list(data_path.glob("**/*.txt"))
    for text_file in text_files:
        print(f"[DEBUG] Loading text file: {text_file}")

        try:
            loader = TextLoader(str(text_file), encoding="utf-8")
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} text docs from {text_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load text {text_file}: {e}")


    csv_files = list(data_path.glob("**/*.csv"))
    for csv_file in csv_files:
        print(f"[DEBUG] Loading csv files: {csv_file}")

        try:
            loader = CSVLoader(str(csv_file))
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} text docs from {csv_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load csv file {csv_file}: {e}")


    
    return documents


# def load_pdf_tables(pdf_path: str) -> List[Document]:
#     documents = []
#     pdf_path = Path(pdf_path)

#     with pdfplumber.open(pdf_path) as pdf:
#         for page_number, page in enumerate(pdf.pages, start=1):
#             tables = page.extract_tables()

#             for table_number, table in enumerate(tables, start=1):
#                 if not table:
#                     continue

#                 rows = []

#                 for row in table:
#                     cleaned_row = [
#                         str(cell).strip() if cell is not None else ""
#                         for cell in row
#                     ]
#                     rows.append(" | ".join(cleaned_row))

#                 table_text = "\n".join(rows)

#                 if table_text.strip():
#                     documents.append(
#                         Document(
#                             page_content=table_text,
#                             metadata={
#                                 "source": str(pdf_path),
#                                 "page": page_number,
#                                 "type": "table",
#                                 "table_number": table_number,
#                             },
#                         )
#                     )

#     return documents


# table_docs = load_pdf_tables(
#     "data/pdf_documents/BAD703-module-3-textbook.pdf"
# )

# print("Tables extracted:", len(table_docs))

# for doc in table_docs[:3]:
#     print("\nMetadata:", doc.metadata)
#     print(doc.page_content[:500])

# print(table_docs)